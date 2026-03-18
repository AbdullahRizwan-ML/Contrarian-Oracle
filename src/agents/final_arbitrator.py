from __future__ import annotations

from crewai import Agent

from src.config.prompts import (
    ARBITRATOR_ROLE,
    ARBITRATOR_GOAL,
    ARBITRATOR_BACKSTORY,
)


def create_final_arbitrator(llm_model_name: str) -> Agent:
    """Create Agent 4: Quant judge (no tools — pure reasoning only)."""
    return Agent(
        role=ARBITRATOR_ROLE,
        goal=ARBITRATOR_GOAL,
        backstory=ARBITRATOR_BACKSTORY,
        tools=[],
        llm=llm_model_name,
        verbose=True,
        memory=False,
        max_iter=2,  # No tools, pure formatting - 2 iterations max
        allow_delegation=False,
    )
