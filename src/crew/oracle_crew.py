from __future__ import annotations

from typing import Optional

from crewai import Crew, Process
from loguru import logger

from src.crew.tasks import create_tasks


class OracleCrew:
    """Crew assembly and execution for The Contrarian Oracle."""

    def __init__(self, ticker: str, llm_model_name: str, target_date: Optional[str] = None):
        """Initialize OracleCrew.

        Args:
            ticker: Stock ticker symbol
            llm_model_name: LLM model identifier
            target_date: Optional historical date (YYYY-MM-DD) for backtesting
        """
        self.ticker = ticker.upper()
        self.llm_model_name = llm_model_name
        self.target_date = target_date
        self.result = None

    def run(self):
        """Assemble the crew and kick off analysis. Returns CrewOutput object."""
        if self.target_date:
            logger.info(f"Starting Contrarian Oracle analysis for {self.ticker} (target_date={self.target_date})")
        else:
            logger.info(f"Starting Contrarian Oracle analysis for {self.ticker}")

        task_data = create_tasks(self.ticker, self.llm_model_name, target_date=self.target_date)

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
