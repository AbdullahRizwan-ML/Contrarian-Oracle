from typing import Type

from crewai.tools import BaseTool
from ddgs import DDGS
from loguru import logger
from pydantic import BaseModel, Field

from src.config.settings import settings


class NewsSearchInput(BaseModel):
    """Input schema for FinancialNewsSearchTool."""

    query: str = Field(..., description="Search query for financial news")


class FinancialNewsSearchTool(BaseTool):
    name: str = "financial_news_search"
    description: str = (
        "Use this tool (and ONLY this tool) to search for financial news. "
        "Tool name: 'financial_news_search'. "
        "Pass a search query about a stock ticker. Returns recent news articles "
        "with titles, sources, dates, snippets, and URLs. "
        "DO NOT attempt to call 'brave_search' or any other search tool - this is the only news search tool available."
    )
    args_schema: Type[BaseModel] = NewsSearchInput

    def _run(self, query: str) -> str:
        max_results = settings.max_news_results
        try:
            logger.info(f"Searching news for: '{query}' (max={max_results})")

            results = list(DDGS().news(query, max_results=max_results, timelimit="w"))

            if not results:
                return f"No news articles found for query: '{query}'"

            output_lines = [f"=== Financial News Results for '{query}' ===\n"]

            for i, article in enumerate(results, 1):
                title = article.get("title", "No title")
                body = article.get("body", "No snippet available")
                source = article.get("source", "Unknown")
                date = article.get("date", "Unknown date")
                url = article.get("url", "")

                output_lines.append(
                    f"--- Article {i} ---\n"
                    f"Title: {title}\n"
                    f"Source: {source}\n"
                    f"Date: {date}\n"
                    f"Snippet: {body}\n"
                    f"URL: {url}\n"
                )

            logger.info(f"Found {len(results)} news articles")
            return "\n".join(output_lines)

        except Exception as e:
            logger.error(f"Error searching news for '{query}': {e}")
            return f"Error searching news: {str(e)}"
