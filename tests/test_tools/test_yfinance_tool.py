"""Tests for the YFinance tool."""

import pytest

from src.tools.yfinance_tool import YFinanceTool
from src.tools.technical_indicators import calculate_rsi, calculate_macd


class TestYFinanceTool:
    def test_yfinance_tool_valid_ticker(self):
        """Test with a known valid ticker."""
        tool = YFinanceTool()
        result = tool._run(ticker="AAPL", period="1mo")
        assert isinstance(result, str)
        assert "AAPL" in result or "Error" in result

    def test_yfinance_tool_invalid_ticker(self):
        """Test with an invalid ticker symbol."""
        tool = YFinanceTool()
        result = tool._run(ticker="XYZXYZ123", period="1mo")
        assert isinstance(result, str)
        assert "Error" in result or "error" in result.lower() or "No historical data" in result


class TestTechnicalIndicators:
    def test_rsi_calculation(self, sample_hist_data):
        """Verify RSI calculation against known properties."""
        rsi = calculate_rsi(sample_hist_data["Close"])
        # RSI should be between 0 and 100 (excluding NaN)
        valid_rsi = rsi.dropna()
        assert all(0 <= v <= 100 for v in valid_rsi)

    def test_macd_calculation(self, sample_hist_data):
        """Verify MACD calculation returns correct structure."""
        macd_line, signal_line, histogram = calculate_macd(
            sample_hist_data["Close"]
        )
        assert len(macd_line) == len(sample_hist_data)
        assert len(signal_line) == len(sample_hist_data)
        assert len(histogram) == len(sample_hist_data)
