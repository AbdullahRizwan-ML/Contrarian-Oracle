from __future__ import annotations

from crewai import Agent

from src.config.prompts import (
    CONTRARIAN_ROLE,
    CONTRARIAN_GOAL,
    CONTRARIAN_BACKSTORY,
)
from src.tools.news_search_tool import FinancialNewsSearchTool
from src.tools.sec_edgar_tool import SECEdgarTool
from src.tools.rag_query_tool import RAGQueryTool


def create_contrarian_skeptic(llm_model_name: str) -> Agent:
    """Create Agent 3: Red team adversarial analyst."""
    return Agent(
        role=CONTRARIAN_ROLE,
        goal=CONTRARIAN_GOAL,
        backstory=CONTRARIAN_BACKSTORY,
        tools=[FinancialNewsSearchTool(), SECEdgarTool(), RAGQueryTool()],
        llm=llm_model_name,
        verbose=True,
        memory=False,
        max_iter=4,  # Reduced to 4 to stay under token limits
        allow_delegation=False,
    )
