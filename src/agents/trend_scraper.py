from __future__ import annotations

from crewai import Agent

from src.config.prompts import (
    TREND_SCRAPER_ROLE,
    TREND_SCRAPER_GOAL,
    TREND_SCRAPER_BACKSTORY,
)
from src.tools.yfinance_tool import YFinanceTool


def create_trend_scraper(llm_model_name: str) -> Agent:
    """Create Agent 1: Market data collector."""
    return Agent(
        role=TREND_SCRAPER_ROLE,
        goal=TREND_SCRAPER_GOAL,
        backstory=TREND_SCRAPER_BACKSTORY,
        tools=[YFinanceTool()],
        llm=llm_model_name,
        verbose=True,
        memory=False,
        max_iter=3,  # Simple data fetch - 3 iterations enough
        allow_delegation=False,
    )
