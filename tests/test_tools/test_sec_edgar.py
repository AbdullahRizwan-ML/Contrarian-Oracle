"""Tests for the SEC EDGAR tool."""

import pytest

from src.tools.sec_edgar_tool import SECEdgarTool


class TestSECEdgarTool:
    def test_sec_edgar_valid_ticker(self):
        """Test SEC EDGAR with a known ticker."""
        tool = SECEdgarTool()
        result = tool._run(ticker="AAPL", filing_type="10-K", count=2)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_sec_edgar_invalid_ticker(self):
        """Test SEC EDGAR with an invalid ticker."""
        tool = SECEdgarTool()
        result = tool._run(ticker="XYZXYZ123", filing_type="10-K", count=1)
        assert isinstance(result, str)
        assert "Could not find CIK" in result or "Error" in result
