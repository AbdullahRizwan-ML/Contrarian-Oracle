from __future__ import annotations

from dataclasses import dataclass

from loguru import logger

from src.config.settings import settings


@dataclass
class DivergenceComponents:
    """Individual component scores for the divergence calculation."""

    technical_divergence: float = 0.0
    sentiment_uniformity: float = 0.0
    insider_activity: float = 0.0
    fundamental_risk: float = 0.0
    macro_headwinds: float = 0.0


class DivergenceCalculator:
    """Core divergence scoring algorithm."""

    def __init__(self, weights: dict | None = None):
        self.weights = weights or {
            "technical_divergence": settings.weight_technical_divergence,
            "sentiment_uniformity": settings.weight_sentiment_uniformity,
            "insider_activity": settings.weight_insider_activity,
            "fundamental_risk": settings.weight_fundamental_risk,
            "macro_headwinds": settings.weight_macro_headwinds,
        }

    def calculate_technical_divergence(
        self,
        price_trend: str,
        rsi: float,
        rsi_trend: str,
        volume_trend: str,
        macd_signal: str,
        ma_crossover: str,
    ) -> float:
        """Calculate technical divergence component (0-100)."""
        score = 0.0

        # Price up + RSI falling = bearish divergence
        if price_trend == "up" and rsi_trend == "falling":
            score += 35

        # RSI overbought signals
        if rsi > 80:
            score += 30
        elif rsi > 70:
            score += 20

        # Price up + volume decreasing = weak rally
        if price_trend == "up" and volume_trend == "Decreasing":
            score += 20

        # Price up + MACD bearish = momentum loss
        if price_trend == "up" and macd_signal == "Bearish":
            score += 15

        # Death Cross
        if ma_crossover == "Death Cross":
            score += 10

        return min(score, 100.0)

    def calculate_sentiment_uniformity(
        self,
        sentiment_score: float,
        uniformity: float,
        num_bullish: int,
        num_bearish: int,
        num_total: int,
    ) -> float:
        """Calculate sentiment uniformity component (0-100)."""
        score = 0.0

        # High uniformity = contrarian signal
        if uniformity > 0.85:
            score += 40
        elif uniformity > 0.70:
            score += 25
        elif uniformity > 0.55:
            score += 10

        # Extreme sentiment
        if abs(sentiment_score) > 0.8:
            score += 30
        elif abs(sentiment_score) > 0.6:
            score += 15

        # No dissent
        if num_total > 0:
            bull_ratio = num_bullish / num_total
            if bull_ratio > 0.85 or bull_ratio < 0.15:
                score += 30

        return min(score, 100.0)

    def calculate_insider_activity(
        self,
        net_sells_90d: int,
        ceo_sold: bool,
        total_value_sold: float,
        market_cap: float,
    ) -> float:
        """Calculate insider activity component (0-100)."""
        score = 0.0

        # Net insider sells
        if net_sells_90d > 10:
            score += 35
        elif net_sells_90d > 5:
            score += 20
        elif net_sells_90d > 2:
            score += 10

        # CEO sold
        if ceo_sold:
            score += 25

        # Sell value relative to market cap
        if market_cap > 0:
            sell_ratio = total_value_sold / market_cap
            if sell_ratio > 0.001:
                score += 25
            elif sell_ratio > 0.0005:
                score += 15
            elif sell_ratio > 0.0001:
                score += 5

        return min(score, 100.0)

    def calculate_fundamental_risk(
        self,
        num_risk_factors: int,
        max_severity: str,
        has_earnings_miss: bool,
        guidance_lowered: bool,
    ) -> float:
        """Calculate fundamental risk component (0-100)."""
        score = 0.0

        # Severity of worst risk factor
        severity_map = {"Low": 5, "Medium": 15, "High": 30, "Critical": 50}
        score += severity_map.get(max_severity, 0)

        # Number of risk factors (capped contribution)
        score += min(num_risk_factors * 5, 25)

        # Earnings miss
        if has_earnings_miss:
            score += 15

        # Guidance lowered
        if guidance_lowered:
            score += 20

        return min(score, 100.0)

    def calculate_macro_headwinds(
        self,
        rate_sensitive: bool,
        rates_rising: bool,
        sector_rotating_away: bool,
        recession_risk_elevated: bool,
    ) -> float:
        """Calculate macro headwinds component (0-100)."""
        score = 0.0

        # Rate sensitive AND rates rising
        if rate_sensitive and rates_rising:
            score += 30

        # Sector rotation away
        if sector_rotating_away:
            score += 35

        # Recession risk
        if recession_risk_elevated:
            score += 25

        return min(score, 100.0)

    def compute_final_score(
        self, components: DivergenceComponents
    ) -> tuple[int, str]:
        """Compute weighted final score and label."""
        score = (
            self.weights["technical_divergence"] * components.technical_divergence
            + self.weights["sentiment_uniformity"] * components.sentiment_uniformity
            + self.weights["insider_activity"] * components.insider_activity
            + self.weights["fundamental_risk"] * components.fundamental_risk
            + self.weights["macro_headwinds"] * components.macro_headwinds
        )

        final_score = int(round(min(max(score, 0), 100)))

        # Determine label
        if final_score <= 20:
            label = "Consensus Aligned"
        elif final_score <= 40:
            label = "Minor Cracks"
        elif final_score <= 60:
            label = "Significant Divergence"
        elif final_score <= 80:
            label = "High Alert"
        else:
            label = "Extreme Divergence"

        logger.info(f"Divergence Score: {final_score} ({label})")
        return final_score, label
