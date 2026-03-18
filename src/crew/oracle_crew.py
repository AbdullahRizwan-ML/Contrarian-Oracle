from __future__ import annotations

from crewai import Crew, Process
from loguru import logger

from src.crew.tasks import create_tasks


class OracleCrew:
    """Crew assembly and execution for The Contrarian Oracle."""

    def __init__(self, ticker: str, llm_model_name: str):
        self.ticker = ticker.upper()
        self.llm_model_name = llm_model_name
        self.result = None

    def run(self):
        """Assemble the crew and kick off analysis. Returns CrewOutput object."""
        logger.info(f"Starting Contrarian Oracle analysis for {self.ticker}")

        task_data = create_tasks(self.ticker, self.llm_model_name)

        crew = Crew(
            agents=task_data["agents"],
            tasks=task_data["tasks"],
            process=Process.sequential,
            verbose=True,
            memory=False,
            full_output=True,
            max_rpm=8,
        )

        self.result = crew.kickoff()
        logger.info(f"Analysis complete for {self.ticker}")
        return self.result

    def get_result(self) -> str:
        """Return the stored result."""
        return str(self.result) if self.result else ""
