from typing import Type

from crewai.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

from src.rag.vector_store import VectorStore


class RAGQueryInput(BaseModel):
    """Input schema for RAGQueryTool."""

    ticker: str = Field(..., description="Stock ticker symbol")
    query: str = Field(..., description="Semantic search query for earnings transcripts")


class RAGQueryTool(BaseTool):
    name: str = "earnings_transcript_search"
    description: str = (
        "Searches indexed earnings call transcripts using semantic search (RAG). "
        "Finds relevant passages about risks, guidance, and key topics."
    )
    args_schema: Type[BaseModel] = RAGQueryInput

    def _run(self, ticker: str, query: str) -> str:
        try:
            logger.info(f"RAG query for {ticker}: '{query}'")
            store = VectorStore()
            results = store.query(ticker, query, n_results=5)

            documents = results.get("documents", [[]])
            metadatas = results.get("metadatas", [[]])
            distances = results.get("distances", [[]])

            if not documents or not documents[0]:
                return (
                    f"No earnings transcript data found for {ticker}. "
                    "The RAG store has not been populated yet. "
                    "Upload earnings transcripts to enable this search."
                )

            output_lines = [
                f"=== Earnings Transcript Search Results for {ticker.upper()} ===\n"
                f"Query: '{query}'\n"
            ]

            for i, (doc, meta, dist) in enumerate(
                zip(documents[0], metadatas[0], distances[0]), 1
            ):
                relevance = round((1 - dist) * 100, 1)
                source = meta.get("source", "Unknown") if meta else "Unknown"
                date = meta.get("date", "Unknown") if meta else "Unknown"
                output_lines.append(
                    f"--- Result {i} (Relevance: {relevance}%) ---\n"
                    f"Source: {source}\n"
                    f"Date: {date}\n"
                    f"Content: {doc}\n"
                )

            return "\n".join(output_lines)

        except Exception as e:
            logger.error(f"Error querying RAG store for {ticker}: {e}")
            return f"Error querying earnings transcripts: {str(e)}"
