from __future__ import annotations

from pathlib import Path

from loguru import logger

from src.rag.vector_store import VectorStore
from src.rag.document_loader import load_earnings_transcript, clean_text


class DocumentEmbedder:
    """Pipeline for embedding documents into the vector store."""

    def __init__(self):
        self.vector_store = VectorStore()

    def embed_transcript(self, filepath: str, ticker: str) -> int:
        """Embed a single earnings transcript file."""
        try:
            transcript = load_earnings_transcript(filepath)
            text = clean_text(transcript["text"])

            if not text:
                logger.warning(f"Empty transcript: {filepath}")
                return 0

            metadata = {
                "source": Path(filepath).name,
                "company": transcript["company"],
                "quarter": transcript["quarter"],
                "date": transcript["date"],
            }

            chunk_count = self.vector_store.ingest_transcript(
                ticker, text, metadata
            )
            logger.info(f"Embedded {chunk_count} chunks from {filepath}")
            return chunk_count

        except Exception as e:
            logger.error(f"Error embedding transcript {filepath}: {e}")
            return 0

    def embed_directory(self, directory: str, ticker: str) -> int:
        """Embed all .txt transcript files in a directory."""
        total_chunks = 0
        dir_path = Path(directory)

        if not dir_path.exists():
            logger.warning(f"Directory not found: {directory}")
            return 0

        for filepath in dir_path.glob("*.txt"):
            chunks = self.embed_transcript(str(filepath), ticker)
            total_chunks += chunks

        logger.info(f"Total chunks embedded from {directory}: {total_chunks}")
        return total_chunks
