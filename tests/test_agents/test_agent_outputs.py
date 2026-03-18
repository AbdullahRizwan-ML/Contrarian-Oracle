"""Tests for agent output validation."""

import pytest

from src.models.market_data import TechnicalSnapshot
from src.models.sentiment import HeadlineSentiment, NarrativeAnalysis
from src.models.contrarian import ContrarianEvidence, ContrarianAnalysis
from src.models.report import FinalReport


class TestAgentOutputModels:
    def test_technical_snapshot_creation(self):
        """Test TechnicalSnapshot model creation."""
        snapshot = TechnicalSnapshot(
            ticker="NVDA",
            current_price=800.0,
            fifty_two_week_high=900.0,
            fifty_two_week_low=400.0,
            market_cap="2T",
            sector="Technology",
            industry="Semiconductors",
            pe_ratio=65.0,
            forward_pe=45.0,
            ma_50=780.0,
            ma_200=650.0,
            ma_crossover="Golden Cross",
            rsi_14=72.0,
            rsi_signal="Overbought",
            macd_value=5.2,
            macd_signal_line=4.8,
            macd_crossover="Bullish",
            volume_current=50000000,
            volume_20d_avg=45000000,
            volume_ratio=1.11,
            volume_trend="Stable",
            support_level=750.0,
            resistance_level=850.0,
            insider_sells_90d=3,
            insider_buys_90d=1,
            overall_technical_bias="Bullish",
        )
        assert snapshot.ticker == "NVDA"
        assert snapshot.rsi_signal == "Overbought"

    def test_headline_sentiment_validation(self):
        """Test HeadlineSentiment confidence validation."""
        h = HeadlineSentiment(
            title="Test",
            source="Test",
            timestamp="2024-01-01",
            url="https://example.com",
            sentiment="Bullish",
            confidence=0.9,
        )
        assert h.confidence == 0.9

    def test_contrarian_evidence_creation(self):
        """Test ContrarianEvidence model."""
        ev = ContrarianEvidence(
            category="Insider Selling",
            description="CEO sold 1M shares",
            severity="High",
            source="SEC Filing",
        )
        assert ev.severity == "High"
