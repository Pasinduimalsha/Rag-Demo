import os
import time
import textwrap
from google import genai

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from dotenv import load_dotenv

from dataset import DOCUMENTS

load_dotenv()

# ── Configuration ─────────────────────────────────────────────────────────────

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

QDRANT_URL = os.environ.get("QDRANT_URL")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
EMBEDDING_DIM = int(os.environ.get("EMBEDDING_DIM"))
GENERATION_MODEL = os.environ.get("GENERATION_MODEL")

TOP_K_RETRIEVE = int(os.environ.get("TOP_K_RETRIEVE"))
TOP_K_RERANKED = int(os.environ.get("TOP_K_RERANKED"))


genai_client = genai.Client(api_key=GEMINI_API_KEY)


# ── Embedding helpers ──────────────────────────────────────────────────────────

def embed_text(text: str) -> list[float]:
    response = genai_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )
    return response.embeddings[0].values


def embed_batch(texts: list[str]) -> list[list[float]]:
    return [embed_text(t) for t in texts]


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL)


def create_collection(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        print(f"Collection '{COLLECTION_NAME}' already exists — skipping creation.")
        return
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
    )
    print(f"Created collection '{COLLECTION_NAME}'.")


def ingest_documents(client: QdrantClient, documents: list[dict]):
    print(f"\n── Ingesting {len(documents)} documents into Qdrant ─────────────")
    
    # Meaningful format: Include Category and Title in the vector representation
    texts = [
        f"Category: {doc['category']}\nTitle: {doc['title']}\nContent: {doc['content']}" 
        for doc in documents
    ]
    
    embeddings = embed_batch(texts)

    if len(embeddings) != len(documents):
        print(f"Error: Embedding count mismatch ({len(embeddings)} vs {len(documents)})")
        return

    points = [
        PointStruct(
            id=doc["id"],
            vector=embedding,
            payload={
                "title": doc["title"],
                "content": doc["content"],
                "category": doc["category"]
            }
        )
        for doc, embedding in zip(documents, embeddings)
    ]

    client.upsert(collection_name=COLLECTION_NAME, wait=True, points=points)
    print(f"Successfully indexed all data.\n")


def retrieve(client: QdrantClient, query: str, top_k: int = TOP_K_RETRIEVE) -> list[dict]:
    query_vector = embed_text(query)
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )
    return [
        {
            "title": r.payload["title"],
            "content": r.payload["content"],
            "category": r.payload["category"],
            "score": r.score,
        }
        for r in results.points
    ]


def rerank_with_gemini(query: str, candidates: list[dict], top_k: int = TOP_K_RERANKED) -> list[dict]:
    print(f"\n── Reranking {len(candidates)} candidates with Gemini ─────────────")

    scored = []

    for i, doc in enumerate(candidates):
        prompt = textwrap.dedent(f"""
            You are a relevance scoring assistant.

            Query: {query}

            Document Title: {doc['title']}
            Document Content: {doc['content']}

            Score the document's relevance to the query on a scale of 1 to 10.
            Output ONLY the number.
        """).strip()

        try:
            response = genai_client.models.generate_content(
                model=GENERATION_MODEL,
                contents=prompt
            )
            score_str = response.text.strip()
            score = int("".join(filter(str.isdigit, score_str)) or 1)
        except:
            score = 1

        print(f"  [{i + 1}] '{doc['title']}' — Gemini relevance score: {score}/10")
        scored.append({**doc, "rerank_score": score})

    # Sort by rerank score descending, take top_k
    reranked = sorted(scored, key=lambda x: x["rerank_score"], reverse=True)[:top_k]
    return reranked


def generate_answer(query: str, context_docs: list[dict]) -> str:
    context_blocks = "\n\n".join(
        f"[Source {i + 1}: {doc['title']}]\n{doc['content']}"
        for i, doc in enumerate(context_docs)
    )

    prompt = textwrap.dedent(f"""
        You are a knowledgeable AI assistant. Use ONLY the provided context to answer the question.
        If the context does not contain enough information, say so.
        Always cite which source(s) you used.

        === CONTEXT ===
        {context_blocks}

        === QUESTION ===
        {query}

        === ANSWER ===
    """).strip()

    try:
        response = genai_client.models.generate_content(
            model=GENERATION_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating answer: {e}"


def rag_query(client: QdrantClient, query: str) -> str:
    print(f"\n{'═' * 60}")
    print(f" QUERY: {query}")
    print(f"{'═' * 60}")

    print(f"\n── Retrieving top-{TOP_K_RETRIEVE} from Qdrant ────────────────────────")
    candidates = retrieve(client, query, top_k=TOP_K_RETRIEVE)
    for i, doc in enumerate(candidates):
        print(f"  [{i + 1}] '{doc['title']}' (score: {doc['score']:.4f})")

    reranked = rerank_with_gemini(query, candidates, top_k=TOP_K_RERANKED)
    print(f"\n  Top-{TOP_K_RERANKED} after reranking:")
    for i, doc in enumerate(reranked):
        print(f"  [{i + 1}] '{doc['title']}' (rerank score: {doc['rerank_score']}/10)")

    print("\n── Generating answer with Gemini ─────────────────────────────")
    answer = generate_answer(query, reranked)

    print(f"\n── ANSWER ────────────────────────────────────────────────────")
    print(textwrap.fill(answer, width=80))
    print()
    return answer


def main():
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("Please set your GEMINI_API_KEY environment variable.")
        return

    client = get_qdrant_client()

    # Check Qdrant is reachable
    try:
        client.get_collections()
    except Exception as e:
        print(f"Cannot connect to Qdrant at {QDRANT_URL}")
        return

    # Check if collection exists and has vectors
    existing = [c.name for c in client.get_collections().collections]
    
    should_ingest = False
    if COLLECTION_NAME not in existing:
        create_collection(client)
        should_ingest = True
    else:
        # Check if collection is empty
        info = client.get_collection(collection_name=COLLECTION_NAME)
        if info.points_count == 0:
            should_ingest = True

    if should_ingest:
        ingest_documents(client, DOCUMENTS)
    else:
        print(f"Vectors already exist in '{COLLECTION_NAME}' — skipping ingestion.")

    queries = [
        "How does a RAG system work?",
        # "What is the difference between fine-tuning and RAG?",
        # "How does the Transformer architecture handle long-range dependencies?",
    ]

    for query in queries:
        rag_query(client, query)
        time.sleep(2)   # avoid rate limits between queries

if __name__ == "__main__":
    main()
