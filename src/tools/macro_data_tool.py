from typing import Optional, Type

import requests
from crewai.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field

from src.config.settings import settings


class MacroDataInput(BaseModel):
    """Input schema for MacroDataTool."""

    indicator: str = Field(
        default="all",
        description="Macro indicator to fetch: 'all', 'rates', 'yield_curve', 'unemployment', 'inflation', 'vix'",
    )


FRED_SERIES = {
    "DFF": "Federal Funds Rate",
    "T10Y2Y": "10Y-2Y Treasury Spread (Yield Curve)",
    "UNRATE": "Unemployment Rate",
    "CPIAUCSL": "CPI (Inflation)",
    "VIXCLS": "VIX Volatility Index",
}


class MacroDataTool(BaseTool):
    name: str = "macro_economic_data"
    description: str = (
        "Fetches macroeconomic data from the FRED API including Federal Funds Rate, "
        "yield curve, unemployment, CPI inflation, and VIX volatility."
    )
    args_schema: Type[BaseModel] = MacroDataInput

    def _fetch_fred_series(self, series_id: str) -> Optional[dict]:
        """Fetch a FRED series and return latest + 3-month-ago values."""
        try:
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                "series_id": series_id,
                "api_key": settings.fred_api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 100,
            }
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            observations = resp.json().get("observations", [])

            if not observations:
                return None

            # Get latest value
            latest = None
            for obs in observations:
                if obs["value"] != ".":
                    latest = {"date": obs["date"], "value": float(obs["value"])}
                    break

            # Get value from ~3 months ago
            three_month_ago = None
            for obs in observations[60:]:
                if obs["value"] != ".":
                    three_month_ago = {
                        "date": obs["date"],
                        "value": float(obs["value"]),
                    }
                    break

            if latest is None:
                return None

            change = None
            if three_month_ago:
                change = round(latest["value"] - three_month_ago["value"], 4)

            return {
                "latest": latest,
                "three_month_ago": three_month_ago,
                "change": change,
            }

        except Exception as e:
            logger.error(f"Error fetching FRED series {series_id}: {e}")
            return None

    def _run(self, indicator: str = "all") -> str:
        try:
            if not settings.fred_api_key:
                return (
                    "FRED API key not configured. Set FRED_API_KEY in your .env file. "
                    "Get a free key at https://fred.stlouisfed.org/docs/api/api_key.html"
                )

            logger.info(f"Fetching macro data (indicator={indicator})")

            output_lines = ["=== Macroeconomic Dashboard ===\n"]

            for series_id, name in FRED_SERIES.items():
                data = self._fetch_fred_series(series_id)
                if data is None:
                    output_lines.append(f"{name}: Data unavailable\n")
                    continue

                latest_val = data["latest"]["value"]
                latest_date = data["latest"]["date"]
                change = data["change"]

                # Direction
                if change is not None:
                    direction = "↑ Rising" if change > 0 else "↓ Falling" if change < 0 else "→ Flat"
                    change_str = f"{change:+.4f}"
                else:
                    direction = "N/A"
                    change_str = "N/A"

                # Flags
                flags = []
                if series_id == "DFF" and change is not None and change > 0:
                    flags.append("⚠️ Rates Rising")
                if series_id == "T10Y2Y" and latest_val < 0:
                    flags.append("🚨 Yield Curve INVERTED")
                if series_id == "VIXCLS" and latest_val > 20:
                    flags.append("⚠️ VIX Elevated (>20)")

                flag_str = " | ".join(flags) if flags else ""

                output_lines.append(
                    f"--- {name} ({series_id}) ---\n"
                    f"Latest: {latest_val} (as of {latest_date})\n"
                    f"3-Month Change: {change_str} ({direction})\n"
                    f"{f'Flags: {flag_str}' if flag_str else ''}\n"
                )

            return "\n".join(output_lines)

        except Exception as e:
            logger.error(f"Error fetching macro data: {e}")
            return f"Error fetching macroeconomic data: {str(e)}"
