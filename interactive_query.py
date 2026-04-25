"""
interactive_query.py
--------------------
Run an interactive loop where you can type your own questions
against the RAG system. Assumes documents are already ingested.
Run: python interactive_query.py
"""

import os
import sys
import time

from qdrant_client import QdrantClient

from rag_pipeline import (
    GEMINI_API_KEY,
    QDRANT_URL,
    COLLECTION_NAME,
    rag_query,
    create_collection,
    ingest_documents,
)
from dataset import DOCUMENTS


def main():
    if not GEMINI_API_KEY:
        print("❌  Set GEMINI_API_KEY in your .env file first.")
        sys.exit(1)

    client = QdrantClient(url=QDRANT_URL)

    try:
        existing = [c.name for c in client.get_collections().collections]
    except Exception as e:
        print(f"❌  Cannot reach Qdrant: {e}")
        print("    Run: docker-compose up -d")
        sys.exit(1)

    # Check if collection exists and has vectors
    should_ingest = False
    if COLLECTION_NAME not in existing:
        create_collection(client)
        should_ingest = True
    else:
        info = client.get_collection(collection_name=COLLECTION_NAME)
        if info.points_count == 0:
            should_ingest = True

    if should_ingest:
        print("Collection empty or missing — ingesting documents...\n")
        ingest_documents(client, DOCUMENTS)

    print("\n🔍  RAG Demo — Interactive Query")
    print("    Type your question and press Enter. Type 'exit' to quit.\n")

    while True:
        try:
            query = input("Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        rag_query(client, query)
        time.sleep(1)


if __name__ == "__main__":
    main()
