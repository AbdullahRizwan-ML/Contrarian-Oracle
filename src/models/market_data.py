from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class TechnicalSnapshot(BaseModel):
    """Pydantic model for Agent 1 (Trend Scraper) output."""

    ticker: str
    current_price: float
    fifty_two_week_high: float
    fifty_two_week_low: float
    market_cap: str
    sector: str
    industry: str
    pe_ratio: float | str
    forward_pe: float | str
    ma_50: float
    ma_200: float | None = None
    ma_crossover: Literal[
        "Golden Cross", "Death Cross", "Neutral", "Insufficient Data"
    ]
    rsi_14: float
    rsi_signal: Literal["Overbought", "Oversold", "Neutral"]
    macd_value: float
    macd_signal_line: float
    macd_crossover: Literal["Bullish", "Bearish"]
    volume_current: int
    volume_20d_avg: int
    volume_ratio: float
    volume_trend: Literal["Increasing", "Decreasing", "Stable"]
    support_level: float
    resistance_level: float
    insider_sells_90d: int
    insider_buys_90d: int
    overall_technical_bias: Literal["Bullish", "Bearish", "Neutral"]
