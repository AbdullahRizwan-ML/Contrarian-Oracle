from __future__ import annotations

from typing import Optional

from crewai import Agent

from src.config.prompts import (
    ARBITRATOR_ROLE,
    ARBITRATOR_GOAL,
    ARBITRATOR_BACKSTORY,
)


def create_final_arbitrator(llm_model_name: str, tools: Optional[list] = None) -> Agent:
    """Create Agent 4: Quant judge (no tools — pure reasoning only).

    Args:
        llm_model_name: LLM model identifier
        tools: Optional list of tools. Defaults to empty list (no tools for arbitrator)
    """
    if tools is None:
        tools = []

    return Agent(
        role=ARBITRATOR_ROLE,
        goal=ARBITRATOR_GOAL,
        backstory=ARBITRATOR_BACKSTORY,
        tools=tools,
        llm=llm_model_name,
        verbose=True,
        memory=False,
        max_iter=2,  # No tools, pure formatting - 2 iterations max
        allow_delegation=False,
    )
