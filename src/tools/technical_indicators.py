from __future__ import annotations

import pandas as pd
import numpy as np
from loguru import logger


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index."""
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(
    prices: pd.Series,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Calculate MACD line, signal line, and histogram."""
    ema_12 = prices.ewm(span=12, adjust=False).mean()
    ema_26 = prices.ewm(span=26, adjust=False).mean()
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(
    prices: pd.Series, period: int = 20, std: int = 2
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Calculate Bollinger Bands (upper, middle, lower)."""
    middle = prices.rolling(window=period).mean()
    rolling_std = prices.rolling(window=period).std()
    upper = middle + (rolling_std * std)
    lower = middle - (rolling_std * std)
    return upper, middle, lower


def detect_divergence(
    prices: pd.Series, indicator: pd.Series, lookback: int = 14
) -> str:
    """Detect price/indicator divergence over the lookback period."""
    if len(prices) < lookback or len(indicator) < lookback:
        return "No Divergence"

    recent_prices = prices.tail(lookback)
    recent_indicator = indicator.tail(lookback)

    price_trend = recent_prices.iloc[-1] - recent_prices.iloc[0]
    indicator_trend = recent_indicator.iloc[-1] - recent_indicator.iloc[0]

    # Bullish divergence: price falling, indicator rising
    if price_trend < 0 and indicator_trend > 0:
        return "Bullish Divergence"
    # Bearish divergence: price rising, indicator falling
    elif price_trend > 0 and indicator_trend < 0:
        return "Bearish Divergence"
    else:
        return "No Divergence"


def identify_support_resistance(
    hist: pd.DataFrame, window: int = 20
) -> dict:
    """Identify support and resistance levels from historical data."""
    if len(hist) < window:
        return {"support": None, "resistance": None}

    recent = hist.tail(window)
    support = round(float(recent["Low"].min()), 2)
    resistance = round(float(recent["High"].max()), 2)

    return {"support": support, "resistance": resistance}
