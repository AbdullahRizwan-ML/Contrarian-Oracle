from typing import Optional, Type

import requests
from crewai.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

from src.config.settings import settings


class SECEdgarInput(BaseModel):
    """Input schema for SECEdgarTool."""

    ticker: str = Field(..., description="Stock ticker symbol")
    filing_type: str = Field(
        default="10-K", description="SEC filing type (e.g. 10-K, 10-Q, 8-K)"
    )
    count: int = Field(default=1, description="Number of recent filings to fetch")


class SECEdgarTool(BaseTool):
    name: str = "sec_edgar_filing_fetcher"
    description: str = (
        "Fetches recent SEC EDGAR filings (10-K, 10-Q, 8-K) for a given "
        "stock ticker. Returns filing dates, types, and links."
    )
    args_schema: Type[BaseModel] = SECEdgarInput

    def _get_cik(self, ticker: str) -> Optional[str]:
        """Look up CIK number for a ticker from SEC company tickers JSON."""
        try:
            headers = {"User-Agent": settings.sec_user_agent}
            resp = requests.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers=headers,
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()

            ticker_upper = ticker.upper()
            for entry in data.values():
                if entry.get("ticker", "").upper() == ticker_upper:
                    cik = str(entry["cik_str"]).zfill(10)
                    return cik

            return None
        except Exception as e:
            logger.error(f"Error looking up CIK for {ticker}: {e}")
            return None

    def _run(
        self, ticker: str, filing_type: str = "10-K", count: int = 1
    ) -> str:
        try:
            logger.info(
                f"Fetching SEC filings for {ticker} (type={filing_type}, count={count})"
            )
            cik = self._get_cik(ticker)
            if not cik:
                return f"Could not find CIK for ticker '{ticker}'. Verify the ticker symbol."

            headers = {"User-Agent": settings.sec_user_agent}
            url = f"https://data.sec.gov/submissions/CIK{cik}.json"
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            recent = data.get("filings", {}).get("recent", {})
            forms = recent.get("form", [])
            dates = recent.get("filingDate", [])
            accessions = recent.get("accessionNumber", [])
            primary_docs = recent.get("primaryDocument", [])

            filings_found = []
            for i, form in enumerate(forms):
                if form == filing_type and len(filings_found) < count:
                    accession_clean = accessions[i].replace("-", "")
                    filing_url = (
                        f"https://www.sec.gov/Archives/edgar/data/"
                        f"{cik.lstrip('0')}/{accession_clean}/{primary_docs[i]}"
                    )
                    filings_found.append(
                        {
                            "type": form,
                            "date": dates[i],
                            "accession": accessions[i],
                            "url": filing_url,
                        }
                    )

            if not filings_found:
                return (
                    f"No {filing_type} filings found for {ticker} (CIK: {cik})."
                )

            output_lines = [
                f"=== SEC EDGAR Filings for {ticker.upper()} ({filing_type}) ===\n"
            ]
            for j, filing in enumerate(filings_found, 1):
                output_lines.append(
                    f"--- Filing {j} ---\n"
                    f"Type: {filing['type']}\n"
                    f"Date: {filing['date']}\n"
                    f"Accession: {filing['accession']}\n"
                    f"URL: {filing['url']}\n"
                )

            logger.info(f"Found {len(filings_found)} {filing_type} filings for {ticker}")
            return "\n".join(output_lines)

        except Exception as e:
            logger.error(f"Error fetching SEC filings for {ticker}: {e}")
            return f"Error fetching SEC filings: {str(e)}"
