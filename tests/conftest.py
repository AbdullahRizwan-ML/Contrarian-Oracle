"""Shared pytest fixtures for The Contrarian Oracle tests."""

import pytest
import pandas as pd
import numpy as np

from src.models.sentiment import HeadlineSentiment
from src.scoring.divergence_calculator import DivergenceComponents


@pytest.fixture
def sample_ticker() -> str:
    return "NVDA"


@pytest.fixture
def sample_hist_data() -> pd.DataFrame:
    """Return a mock DataFrame with 100 rows of OHLCV data."""
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=100, freq="B")
    base_price = 500.0
    close_prices = base_price + np.cumsum(np.random.randn(100) * 5)

    return pd.DataFrame(
        {
            "Open": close_prices - np.random.rand(100) * 2,
            "High": close_prices + np.random.rand(100) * 3,
            "Low": close_prices - np.random.rand(100) * 3,
            "Close": close_prices,
            "Volume": np.random.randint(1_000_000, 50_000_000, size=100),
        },
        index=dates,
    )


@pytest.fixture
def sample_headlines() -> list[HeadlineSentiment]:
    """Return a list of 10 mock HeadlineSentiment objects."""
    return [
        HeadlineSentiment(
            title="NVDA stock surges on AI demand",
            source="Reuters",
            timestamp="2024-03-15",
            url="https://example.com/1",
            sentiment="Bullish",
            confidence=0.9,
        ),
        HeadlineSentiment(
            title="NVIDIA beats earnings expectations",
            source="Bloomberg",
            timestamp="2024-03-15",
            url="https://example.com/2",
            sentiment="Bullish",
            confidence=0.85,
        ),
        HeadlineSentiment(
            title="Data center spending drives NVDA growth",
            source="CNBC",
            timestamp="2024-03-14",
            url="https://example.com/3",
            sentiment="Bullish",
            confidence=0.8,
        ),
        HeadlineSentiment(
            title="NVIDIA faces chip export restrictions",
            source="WSJ",
            timestamp="2024-03-14",
            url="https://example.com/4",
            sentiment="Bearish",
            confidence=0.7,
        ),
        HeadlineSentiment(
            title="AI chip competition heats up",
            source="TechCrunch",
            timestamp="2024-03-14",
            url="https://example.com/5",
            sentiment="Neutral",
            confidence=0.6,
        ),
        HeadlineSentiment(
            title="NVDA raises guidance for next quarter",
            source="MarketWatch",
            timestamp="2024-03-13",
            url="https://example.com/6",
            sentiment="Bullish",
            confidence=0.88,
        ),
        HeadlineSentiment(
            title="Analysts upgrade NVDA price target",
            source="Barrons",
            timestamp="2024-03-13",
            url="https://example.com/7",
            sentiment="Bullish",
            confidence=0.75,
        ),
        HeadlineSentiment(
            title="NVIDIA valuation concerns grow",
            source="FT",
            timestamp="2024-03-13",
            url="https://example.com/8",
            sentiment="Bearish",
            confidence=0.65,
        ),
        HeadlineSentiment(
            title="Tech sector rally continues",
            source="Yahoo Finance",
            timestamp="2024-03-12",
            url="https://example.com/9",
            sentiment="Bullish",
            confidence=0.7,
        ),
        HeadlineSentiment(
            title="Market steady ahead of Fed decision",
            source="AP",
            timestamp="2024-03-12",
            url="https://example.com/10",
            sentiment="Neutral",
            confidence=0.5,
        ),
    ]


@pytest.fixture
def sample_components() -> DivergenceComponents:
    """Return a sample DivergenceComponents instance."""
    return DivergenceComponents(
        technical_divergence=45.0,
        sentiment_uniformity=60.0,
        insider_activity=30.0,
        fundamental_risk=20.0,
        macro_headwinds=25.0,
    )
