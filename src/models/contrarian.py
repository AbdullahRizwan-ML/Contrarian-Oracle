from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ContrarianEvidence(BaseModel):
    """A single piece of contrarian evidence."""

    category: str
    description: str
    severity: Literal["Low", "Medium", "High", "Critical"]
    source: str


class ContrarianAnalysis(BaseModel):
    """Pydantic model for Agent 3 (Contrarian Skeptic) output."""

    ticker: str
    evidence: list[ContrarianEvidence]
    contrarian_narrative: str
    evidence_strength_score: int = Field(ge=0, le=100)
    key_risks: list[str]
