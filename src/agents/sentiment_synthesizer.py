from __future__ import annotations

from crewai import Agent

from src.config.prompts import (
    SENTIMENT_SYNTH_ROLE,
    SENTIMENT_SYNTH_GOAL,
    SENTIMENT_SYNTH_BACKSTORY,
)
from src.tools.news_search_tool import FinancialNewsSearchTool


def create_sentiment_synthesizer(llm_model_name: str) -> Agent:
    """Create Agent 2: Narrative analyst."""
    return Agent(
        role=SENTIMENT_SYNTH_ROLE,
        goal=SENTIMENT_SYNTH_GOAL,
        backstory=SENTIMENT_SYNTH_BACKSTORY,
        tools=[FinancialNewsSearchTool()],
        llm=llm_model_name,
        verbose=True,
        memory=False,
        max_iter=3,  # Simple news search + sentiment - 3 iterations enough
        allow_delegation=False,
    )
