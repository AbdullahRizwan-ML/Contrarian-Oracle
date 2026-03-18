"""Tests for the Financial News Search tool."""

import pytest

from src.tools.news_search_tool import FinancialNewsSearchTool


class TestNewsSearchTool:
    def test_news_search_returns_results(self):
        """Test news search with a common query."""
        tool = FinancialNewsSearchTool()
        result = tool._run(query="NVDA stock news")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_news_search_empty_query(self):
        """Test news search with an obscure/unlikely query."""
        tool = FinancialNewsSearchTool()
        result = tool._run(query="xyznonexistentstockticker98765 obscure query")
        assert isinstance(result, str)
