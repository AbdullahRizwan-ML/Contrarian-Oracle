"""Tests for the Divergence Calculator scoring engine."""

import pytest

from src.scoring.divergence_calculator import DivergenceCalculator, DivergenceComponents
from src.scoring.weights import get_weights, DEFAULT_WEIGHTS


class TestDivergenceCalculator:
    def test_consensus_aligned(self):
        """All low scores should produce a score in 0-20 range."""
        calc = DivergenceCalculator()
        components = DivergenceComponents(
            technical_divergence=10,
            sentiment_uniformity=5,
            insider_activity=0,
            fundamental_risk=10,
            macro_headwinds=5,
        )
        score, label = calc.compute_final_score(components)
        assert 0 <= score <= 20
        assert label == "Consensus Aligned"

    def test_extreme_divergence(self):
        """All high scores should produce a score in 81-100 range."""
        calc = DivergenceCalculator()
        components = DivergenceComponents(
            technical_divergence=95,
            sentiment_uniformity=90,
            insider_activity=100,
            fundamental_risk=85,
            macro_headwinds=90,
        )
        score, label = calc.compute_final_score(components)
        assert 81 <= score <= 100
        assert label == "Extreme Divergence"

    def test_weight_normalization(self):
        """Verify default weights sum to approximately 1.0."""
        weights = DEFAULT_WEIGHTS
        total = sum(weights.values())
        assert abs(total - 1.0) < 0.01

    def test_individual_technical_divergence(self):
        """Test technical divergence component calculator."""
        calc = DivergenceCalculator()
        score = calc.calculate_technical_divergence(
            price_trend="up",
            rsi=75.0,
            rsi_trend="falling",
            volume_trend="Decreasing",
            macd_signal="Bearish",
            ma_crossover="Death Cross",
        )
        # Should be high: RSI falling + overbought + vol decreasing + MACD bearish + Death Cross
        assert score == 100.0  # 35 + 20 + 20 + 15 + 10 = 100

    def test_individual_sentiment_uniformity(self):
        """Test sentiment uniformity component calculator."""
        calc = DivergenceCalculator()
        score = calc.calculate_sentiment_uniformity(
            sentiment_score=0.9,
            uniformity=0.9,
            num_bullish=9,
            num_bearish=0,
            num_total=10,
        )
        assert score == 100.0  # 40 + 30 + 30 = 100

    def test_individual_insider_activity(self):
        """Test insider activity component calculator."""
        calc = DivergenceCalculator()
        score = calc.calculate_insider_activity(
            net_sells_90d=3,
            ceo_sold=False,
            total_value_sold=200000,
            market_cap=1_000_000_000,
        )
        assert score == 15.0  # 10 + 0 + 5 (sell_ratio=0.0002 > 0.0001)

    def test_individual_fundamental_risk(self):
        """Test fundamental risk component calculator."""
        calc = DivergenceCalculator()
        score = calc.calculate_fundamental_risk(
            num_risk_factors=3,
            max_severity="High",
            has_earnings_miss=True,
            guidance_lowered=False,
        )
        assert score == 60.0  # 30 + 15 + 15

    def test_individual_macro_headwinds(self):
        """Test macro headwinds component calculator."""
        calc = DivergenceCalculator()
        score = calc.calculate_macro_headwinds(
            rate_sensitive=True,
            rates_rising=True,
            sector_rotating_away=False,
            recession_risk_elevated=True,
        )
        assert score == 55.0  # 30 + 0 + 25

    def test_score_label_mapping(self):
        """Verify correct labels for each score range."""
        calc = DivergenceCalculator()

        test_cases = [
            (DivergenceComponents(10, 10, 10, 10, 10), "Consensus Aligned"),
            (DivergenceComponents(35, 35, 35, 35, 35), "Minor Cracks"),
            (DivergenceComponents(55, 55, 55, 55, 55), "Significant Divergence"),
            (DivergenceComponents(75, 75, 75, 75, 75), "High Alert"),
            (DivergenceComponents(95, 95, 95, 95, 95), "Extreme Divergence"),
        ]

        for components, expected_label in test_cases:
            _, label = calc.compute_final_score(components)
            assert label == expected_label, f"Expected {expected_label}, got {label}"


class TestWeightProfiles:
    def test_get_default_weights(self):
        """Test getting default weight profile."""
        weights = get_weights("default")
        assert weights == DEFAULT_WEIGHTS

    def test_get_aggressive_weights(self):
        """Test getting aggressive weight profile."""
        weights = get_weights("aggressive")
        assert weights["insider_activity"] > DEFAULT_WEIGHTS["insider_activity"]

    def test_get_unknown_profile_returns_default(self):
        """Test that unknown profile falls back to default."""
        weights = get_weights("unknown_profile")
        assert weights == DEFAULT_WEIGHTS
