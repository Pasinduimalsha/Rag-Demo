# RAG Demo — Qdrant + Gemini

A minimal **Retrieval-Augmented Generation** pipeline using:

| Component | Tool |
|-----------|------|
| Vector DB | [Qdrant](https://qdrant.tech/) (local via Docker) |
| Embeddings | Gemini `text-embedding-004` |
| Reranking | Gemini `gemini-1.5-flash` (prompt-based scoring) |
| Generation | Gemini `gemini-1.5-flash` |

---

## Project Structure

```
rag-demo/
├── docker-compose.yml      # Spins up Qdrant locally
├── dataset.py              # 10 sample documents on AI/ML topics
├── rag_pipeline.py         # Full RAG pipeline (ingest + query)
├── interactive_query.py    # Interactive CLI for your own questions
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Get a free Gemini API key

Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and create a free API key.

### 2. Export your API key

```bash
export GEMINI_API_KEY="your-key-here"
```

### 3. Start Qdrant with Docker

```bash
docker-compose up -d
```

Verify Qdrant is running:
```bash
curl http://localhost:6333/collections
```

### 4. Set up a virtual environment (Recommended)

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 5. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the demo pipeline

Ingests all documents and runs 3 sample queries:

```bash
python rag_pipeline.py
```

### 7. Run interactive mode

Ask your own questions:

```bash
python interactive_query.py
```

---

## How It Works

```
User Query
    │
    ▼
[Gemini Embed] ──► Query Vector
    │
    ▼
[Qdrant Search] ──► Top-5 candidate documents (cosine similarity)
    │
    ▼
[Gemini Rerank] ──► Scores each candidate 1-10 for relevance
    │                   Keeps top-3
    ▼
[Gemini Generate] ──► Final answer grounded in retrieved context
    │
    ▼
  Answer + Sources
```

### Pipeline steps in detail

1. **Ingestion** — Each document is embedded with `text-embedding-004` (768 dimensions) and stored in Qdrant with its metadata.

2. **Retrieval** — The user query is embedded with `task_type=RETRIEVAL_QUERY` and the top-5 nearest neighbors are fetched from Qdrant using cosine similarity.

3. **Reranking** — Gemini scores each candidate document's relevance to the query (1–10). This corrects for embedding similarity not always aligning with true relevance. Top-3 are kept.

4. **Generation** — A prompt assembles the reranked context and asks Gemini to answer using only those sources, with citation.

---

## Dataset

10 documents covering:
- Neural networks & deep learning
- Transformer architecture & attention mechanisms
- RAG systems & chunking strategies
- Vector databases
- Embeddings & semantic search
- RLHF & LLM alignment
- Fine-tuning vs RAG

---

## Customization

- **Add your own documents** — Edit `dataset.py` and re-run `rag_pipeline.py`.
- **Change the collection** — Set `COLLECTION_NAME` in `rag_pipeline.py`.
- **Tune retrieval** — Adjust `TOP_K_RETRIEVE` and `TOP_K_RERANKED` constants.
- **Filter by category** — Use Qdrant's `Filter` API in the `retrieve()` function.
