from __future__ import annotations

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from loguru import logger

from src.config.settings import settings


class VectorStore:
    """ChromaDB vector store management for earnings transcripts."""

    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model
        )
        logger.info(f"VectorStore initialized (persist_dir={settings.chroma_persist_dir})")

    def get_or_create_collection(self, ticker: str):
        """Get or create a ChromaDB collection for a ticker."""
        collection_name = f"oracle_{ticker.lower()}"
        collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
        )
        return collection

    def add_documents(
        self,
        ticker: str,
        documents: list[str],
        metadatas: list[dict],
        ids: list[str],
    ) -> None:
        """Upsert documents into a ticker's collection."""
        collection = self.get_or_create_collection(ticker)
        collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
        logger.info(f"Added {len(documents)} documents to oracle_{ticker.lower()}")

    def query(
        self, ticker: str, query_text: str, n_results: int = 5
    ) -> dict:
        """Query a ticker's collection with semantic search."""
        collection = self.get_or_create_collection(ticker)
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
        )
        return results

    def ingest_transcript(
        self, ticker: str, transcript_text: str, metadata: dict
    ) -> int:
        """Chunk and ingest an earnings transcript into the vector store."""
        chunks = self._chunk_text(
            transcript_text,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
        )

        documents = []
        metadatas = []
        ids = []

        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({**metadata, "chunk_index": i})
            ids.append(f"{ticker.lower()}_{metadata.get('date', 'unknown')}_{i}")

        self.add_documents(ticker, documents, metadatas, ids)
        logger.info(f"Ingested {len(chunks)} chunks for {ticker}")
        return len(chunks)

    def _chunk_text(
        self, text: str, chunk_size: int = 512, overlap: int = 50
    ) -> list[str]:
        """Split text into overlapping word-based chunks."""
        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start = end - overlap

        return chunks
