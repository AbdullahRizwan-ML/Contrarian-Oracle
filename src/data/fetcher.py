from __future__ import annotations

import json

import requests
import yfinance as yf
from ddgs import DDGS
from loguru import logger

from src.config.settings import settings
from src.data.cache import DataCache


class DataFetcher:
    """Unified data fetcher that orchestrates all data collection with caching."""

    def __init__(self, cache: DataCache | None = None):
        self.cache = cache or DataCache()

    def fetch_market_data(self, ticker: str) -> dict:
        """Fetch stock market data via yfinance, checking cache first."""
        cache_key = f"market_{ticker.upper()}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for market data: {ticker}")
            return json.loads(cached)

        try:
            logger.info(f"Fetching market data for {ticker}")
            stock = yf.Ticker(ticker)
            hist = stock.history(period=settings.yfinance_period)
            info = stock.info

            data = {
                "ticker": ticker.upper(),
                "info": info,
                "history_length": len(hist),
                "current_price": float(hist["Close"].iloc[-1]) if not hist.empty else None,
            }

            self.cache.set(cache_key, json.dumps(data, default=str))
            return data

        except Exception as e:
            logger.error(f"Error fetching market data for {ticker}: {e}")
            return {"ticker": ticker.upper(), "error": str(e)}

    def fetch_news(self, ticker: str) -> list[dict]:
        """Fetch financial news via DuckDuckGo, checking cache first."""
        cache_key = f"news_{ticker.upper()}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for news: {ticker}")
            return json.loads(cached)

        try:
            logger.info(f"Fetching news for {ticker}")
            query = f"{ticker} stock news"

            with DDGS() as ddgs:
                results = list(
                    ddgs.news(
                        query,
                        max_results=settings.max_news_results,
                        timelimit="w",
                    )
                )

            articles = []
            for r in results:
                articles.append(
                    {
                        "title": r.get("title", ""),
                        "body": r.get("body", ""),
                        "source": r.get("source", ""),
                        "date": r.get("date", ""),
                        "url": r.get("url", ""),
                    }
                )

            self.cache.set(cache_key, json.dumps(articles))
            return articles

        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return []

    def fetch_sec_filings(self, ticker: str) -> list[dict]:
        """Fetch SEC filings via EDGAR, checking cache first."""
        cache_key = f"sec_{ticker.upper()}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for SEC filings: {ticker}")
            return json.loads(cached)

        try:
            logger.info(f"Fetching SEC filings for {ticker}")
            headers = {"User-Agent": settings.sec_user_agent}

            # Look up CIK
            resp = requests.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers=headers,
                timeout=10,
            )
            resp.raise_for_status()
            tickers_data = resp.json()

            cik = None
            for entry in tickers_data.values():
                if entry.get("ticker", "").upper() == ticker.upper():
                    cik = str(entry["cik_str"]).zfill(10)
                    break

            if not cik:
                return []

            # Fetch filings
            url = f"https://data.sec.gov/submissions/CIK{cik}.json"
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            recent = data.get("filings", {}).get("recent", {})
            forms = recent.get("form", [])
            dates = recent.get("filingDate", [])
            accessions = recent.get("accessionNumber", [])

            filings = []
            for i, form in enumerate(forms[:20]):
                filings.append(
                    {
                        "form": form,
                        "date": dates[i] if i < len(dates) else "",
                        "accession": accessions[i] if i < len(accessions) else "",
                    }
                )

            self.cache.set(cache_key, json.dumps(filings))
            return filings

        except Exception as e:
            logger.error(f"Error fetching SEC filings for {ticker}: {e}")
            return []

    def fetch_macro_data(self) -> dict:
        """Fetch macroeconomic data from FRED, checking cache first."""
        cache_key = "macro_data"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info("Cache hit for macro data")
            return json.loads(cached)

        try:
            if not settings.fred_api_key:
                return {"error": "FRED API key not configured"}

            logger.info("Fetching macro data from FRED")
            series_ids = ["DFF", "T10Y2Y", "UNRATE", "CPIAUCSL", "VIXCLS"]
            data = {}

            for series_id in series_ids:
                url = "https://api.stlouisfed.org/fred/series/observations"
                params = {
                    "series_id": series_id,
                    "api_key": settings.fred_api_key,
                    "file_type": "json",
                    "sort_order": "desc",
                    "limit": 10,
                }
                resp = requests.get(url, params=params, timeout=10)
                resp.raise_for_status()
                observations = resp.json().get("observations", [])

                if observations:
                    for obs in observations:
                        if obs["value"] != ".":
                            data[series_id] = {
                                "value": float(obs["value"]),
                                "date": obs["date"],
                            }
                            break

            self.cache.set(cache_key, json.dumps(data))
            return data

        except Exception as e:
            logger.error(f"Error fetching macro data: {e}")
            return {"error": str(e)}
