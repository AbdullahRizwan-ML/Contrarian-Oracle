from __future__ import annotations

from typing import Optional

from crewai import Agent

from src.config.prompts import (
    CONTRARIAN_ROLE,
    CONTRARIAN_GOAL,
    CONTRARIAN_BACKSTORY,
)
from src.tools.news_search_tool import FinancialNewsSearchTool
from src.tools.sec_edgar_tool import SECEdgarTool
from src.tools.rag_query_tool import RAGQueryTool


def create_contrarian_skeptic(llm_model_name: str, tools: Optional[list] = None) -> Agent:
    """Create Agent 3: Red team adversarial analyst.

    Args:
        llm_model_name: LLM model identifier
        tools: Optional list of tools. If None, defaults to news/SEC/RAG tools
    """
    if tools is None:
        tools = [FinancialNewsSearchTool(), SECEdgarTool(), RAGQueryTool()]

    return Agent(
        role=CONTRARIAN_ROLE,
        goal=CONTRARIAN_GOAL,
        backstory=CONTRARIAN_BACKSTORY,
        tools=tools,
        llm=llm_model_name,
        verbose=True,
        memory=False,
        max_iter=4,  # Reduced to 4 to stay under token limits
        allow_delegation=False,
    )
