from typing import Optional, Type

import yfinance as yf
from crewai.tools import BaseTool
from loguru import logger
from pydantic import BaseModel, Field


class YFinanceToolInput(BaseModel):
    """Input schema for YFinanceTool."""

    ticker: str = Field(..., description="Stock ticker symbol (e.g. AAPL, NVDA)")
    period: str = Field(
        default="6mo", description="Data period (e.g. 1mo, 3mo, 6mo, 1y)"
    )


class YFinanceTool(BaseTool):
    name: str = "stock_data_fetcher"
    description: str = (
        "IMPORTANT: This tool is called 'stock_data_fetcher' - use this exact name. "
        "This is the ONLY tool available for fetching stock data. "
        "DO NOT attempt to call any other tools like 'technical_calculator' or 'stock_info'. "
        "Fetches comprehensive stock data including price, fundamentals, "
        "technicals (RSI, MACD, MAs), volume analysis, and insider transactions. "
        "Returns ALL technical metrics in one call - no additional tools needed."
    )
    args_schema: Type[BaseModel] = YFinanceToolInput
    target_date: Optional[str] = None  # Class field for Pydantic model

    def __init__(self, target_date: Optional[str] = None):
        """Initialize YFinanceTool with optional historical date for backtesting.

        Args:
            target_date: Optional date string in format "YYYY-MM-DD". If provided,
                        fetches data as of this historical date for point-in-time analysis.
        """
        super().__init__()
        self.target_date = target_date

    def _run(self, ticker: str, period: str = "6mo") -> str:
        try:
            if self.target_date:
                logger.info(f"Fetching stock data for {ticker} (period={period}, end={self.target_date})")
            else:
                logger.info(f"Fetching stock data for {ticker} (period={period})")

            stock = yf.Ticker(ticker)

            # If target_date is provided, fetch historical data up to that date
            if self.target_date:
                hist = stock.history(period=period, end=self.target_date)
            else:
                hist = stock.history(period=period)

            if hist.empty:
                return f"Error: No historical data found for ticker '{ticker}'."

            info = stock.info

            # Current price
            current_price = hist["Close"].iloc[-1]

            # 52-week high/low
            fifty_two_week_high = info.get("fiftyTwoWeekHigh", "N/A")
            fifty_two_week_low = info.get("fiftyTwoWeekLow", "N/A")

            # Fundamentals
            market_cap = info.get("marketCap", "N/A")
            sector = info.get("sector", "N/A")
            industry = info.get("industry", "N/A")
            pe_ratio = info.get("trailingPE", "N/A")
            forward_pe = info.get("forwardPE", "N/A")

            # 50-day Moving Average
            ma_50 = hist["Close"].rolling(window=50).mean().iloc[-1]

            # 200-day Moving Average
            if len(hist) >= 200:
                ma_200 = hist["Close"].rolling(window=200).mean().iloc[-1]
            else:
                ma_200 = None

            # MA Crossover
            if ma_200 is not None:
                if ma_50 > ma_200:
                    ma_crossover = "Golden Cross"
                else:
                    ma_crossover = "Death Cross"
            else:
                ma_crossover = "Insufficient Data"

            # RSI (14-day)
            delta = hist["Close"].diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi_series = 100 - (100 / (1 + rs))
            rsi_14 = round(rsi_series.iloc[-1], 2)

            if rsi_14 > 70:
                rsi_signal = "Overbought"
            elif rsi_14 < 30:
                rsi_signal = "Oversold"
            else:
                rsi_signal = "Neutral"

            # MACD
            ema_12 = hist["Close"].ewm(span=12, adjust=False).mean()
            ema_26 = hist["Close"].ewm(span=26, adjust=False).mean()
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            macd_value = round(macd_line.iloc[-1], 4)
            macd_signal_value = round(signal_line.iloc[-1], 4)
            macd_crossover = "Bullish" if macd_value > macd_signal_value else "Bearish"

            # Volume analysis
            volume_current = int(hist["Volume"].iloc[-1])
            volume_20d_avg = int(hist["Volume"].tail(20).mean())
            volume_ratio = round(volume_current / volume_20d_avg, 2) if volume_20d_avg > 0 else 0.0

            if volume_ratio > 1.2:
                volume_trend = "Increasing"
            elif volume_ratio < 0.8:
                volume_trend = "Decreasing"
            else:
                volume_trend = "Stable"

            # Support/Resistance (20-day rolling)
            support_level = round(hist["Low"].tail(20).min(), 2)
            resistance_level = round(hist["High"].tail(20).max(), 2)

            # Insider transactions
            insider_buys = 0
            insider_sells = 0
            try:
                insider_txns = stock.insider_transactions
                if insider_txns is not None and not insider_txns.empty:
                    for _, row in insider_txns.iterrows():
                        text = str(row.get("Text", "")).lower()
                        if "sale" in text or "sell" in text:
                            insider_sells += 1
                        elif "purchase" in text or "buy" in text:
                            insider_buys += 1
            except Exception:
                logger.debug("Could not fetch insider transactions")

            # Overall technical bias
            bullish_signals = 0
            bearish_signals = 0
            if rsi_signal == "Oversold":
                bullish_signals += 1
            elif rsi_signal == "Overbought":
                bearish_signals += 1
            if macd_crossover == "Bullish":
                bullish_signals += 1
            else:
                bearish_signals += 1
            if ma_crossover == "Golden Cross":
                bullish_signals += 1
            elif ma_crossover == "Death Cross":
                bearish_signals += 1

            if bullish_signals > bearish_signals:
                overall_bias = "Bullish"
            elif bearish_signals > bullish_signals:
                overall_bias = "Bearish"
            else:
                overall_bias = "Neutral"

            result = {
                "ticker": ticker.upper(),
                "current_price": round(current_price, 2),
                "fifty_two_week_high": fifty_two_week_high,
                "fifty_two_week_low": fifty_two_week_low,
                "market_cap": str(market_cap),
                "sector": sector,
                "industry": industry,
                "pe_ratio": pe_ratio,
                "forward_pe": forward_pe,
                "ma_50": round(ma_50, 2),
                "ma_200": round(ma_200, 2) if ma_200 is not None else None,
                "ma_crossover": ma_crossover,
                "rsi_14": rsi_14,
                "rsi_signal": rsi_signal,
                "macd_value": macd_value,
                "macd_signal_line": macd_signal_value,
                "macd_crossover": macd_crossover,
                "volume_current": volume_current,
                "volume_20d_avg": volume_20d_avg,
                "volume_ratio": volume_ratio,
                "volume_trend": volume_trend,
                "support_level": support_level,
                "resistance_level": resistance_level,
                "insider_sells_90d": insider_sells,
                "insider_buys_90d": insider_buys,
                "overall_technical_bias": overall_bias,
            }

            logger.info(f"Successfully fetched data for {ticker}")
            return str(result)

        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return f"Error fetching stock data for '{ticker}': {str(e)}"
