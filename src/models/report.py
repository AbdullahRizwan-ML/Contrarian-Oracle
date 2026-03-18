from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from src.models.market_data import TechnicalSnapshot
from src.models.sentiment import NarrativeAnalysis
from src.models.contrarian import ContrarianAnalysis


class FinalReport(BaseModel):
    """Pydantic model for Agent 4 (Final Arbitrator) output."""

    ticker: str
    analysis_timestamp: datetime
    divergence_score: int = Field(ge=0, le=100)
    divergence_label: Literal[
        "Consensus Aligned",
        "Minor Cracks",
        "Significant Divergence",
        "High Alert",
        "Extreme Divergence",
    ]
    score_breakdown: dict
    bull_case_summary: str
    bear_case_summary: str
    key_risk_factors: list[str]
    verdict: str
    confidence_level: Literal["Low", "Medium", "High"]
    technical: TechnicalSnapshot
    narrative: NarrativeAnalysis
    contrarian: ContrarianAnalysis
