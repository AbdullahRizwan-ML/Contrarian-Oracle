from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class HeadlineSentiment(BaseModel):
    """Sentiment data for a single news headline."""

    title: str
    source: str
    timestamp: str
    url: str
    sentiment: Literal["Bullish", "Bearish", "Neutral"]
    confidence: float = Field(ge=0.0, le=1.0)


class NarrativeAnalysis(BaseModel):
    """Pydantic model for Agent 2 (Sentiment Synthesizer) output."""

    ticker: str
    headlines: list[HeadlineSentiment]
    overall_sentiment_score: float = Field(ge=-1.0, le=1.0)
    sentiment_uniformity: float = Field(
        ge=0.0, le=1.0, description="1.0 = total consensus"
    )
    mainstream_narrative: str
    narrative_confidence: Literal["Low", "Medium", "High"]
    num_bullish: int
    num_bearish: int
    num_neutral: int
