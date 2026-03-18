from __future__ import annotations

from loguru import logger

from src.rag.vector_store import VectorStore


class TranscriptRetriever:
    """High-level RAG retrieval interface for earnings transcripts."""

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def search(
        self, ticker: str, query: str, top_k: int = 5
    ) -> list[dict]:
        """Search for relevant transcript passages."""
        try:
            results = self.vector_store.query(ticker, query, n_results=top_k)

            documents = results.get("documents", [[]])
            metadatas = results.get("metadatas", [[]])
            distances = results.get("distances", [[]])

            if not documents or not documents[0]:
                return []

            output = []
            for doc, meta, dist in zip(documents[0], metadatas[0], distances[0]):
                output.append(
                    {
                        "content": doc,
                        "source": meta.get("source", "Unknown") if meta else "Unknown",
                        "date": meta.get("date", "Unknown") if meta else "Unknown",
                        "relevance_score": round(1 - dist, 4),
                    }
                )

            return output

        except Exception as e:
            logger.error(f"Error searching transcripts for {ticker}: {e}")
            return []

    def search_risks(self, ticker: str) -> list[dict]:
        """Pre-built query for risk factors in earnings transcripts."""
        return self.search(
            ticker,
            "risk factors challenges headwinds concerns weakness declining",
        )

    def search_guidance(self, ticker: str) -> list[dict]:
        """Pre-built query for forward guidance in earnings transcripts."""
        return self.search(
            ticker,
            "forward guidance outlook expectations revenue growth forecast",
        )
