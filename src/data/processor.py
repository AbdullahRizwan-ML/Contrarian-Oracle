from __future__ import annotations

from loguru import logger
from textblob import TextBlob

from src.models.market_data import TechnicalSnapshot
from src.models.sentiment import HeadlineSentiment


def clean_market_data(raw: dict) -> TechnicalSnapshot:
    """Clean and transform raw market data into a TechnicalSnapshot."""
    try:
        return TechnicalSnapshot(
            ticker=raw.get("ticker", ""),
            current_price=raw.get("current_price", 0.0),
            fifty_two_week_high=raw.get("fifty_two_week_high", 0.0),
            fifty_two_week_low=raw.get("fifty_two_week_low", 0.0),
            market_cap=str(raw.get("market_cap", "N/A")),
            sector=raw.get("sector", "N/A"),
            industry=raw.get("industry", "N/A"),
            pe_ratio=raw.get("pe_ratio", "N/A"),
            forward_pe=raw.get("forward_pe", "N/A"),
            ma_50=raw.get("ma_50", 0.0),
            ma_200=raw.get("ma_200"),
            ma_crossover=raw.get("ma_crossover", "Neutral"),
            rsi_14=raw.get("rsi_14", 50.0),
            rsi_signal=raw.get("rsi_signal", "Neutral"),
            macd_value=raw.get("macd_value", 0.0),
            macd_signal_line=raw.get("macd_signal_line", 0.0),
            macd_crossover=raw.get("macd_crossover", "Bullish"),
            volume_current=raw.get("volume_current", 0),
            volume_20d_avg=raw.get("volume_20d_avg", 0),
            volume_ratio=raw.get("volume_ratio", 1.0),
            volume_trend=raw.get("volume_trend", "Stable"),
            support_level=raw.get("support_level", 0.0),
            resistance_level=raw.get("resistance_level", 0.0),
            insider_sells_90d=raw.get("insider_sells_90d", 0),
            insider_buys_90d=raw.get("insider_buys_90d", 0),
            overall_technical_bias=raw.get("overall_technical_bias", "Neutral"),
        )
    except Exception as e:
        logger.error(f"Error cleaning market data: {e}")
        raise


def clean_news_data(raw: list[dict]) -> list[HeadlineSentiment]:
    """Clean raw news data and classify sentiment for each headline."""
    headlines = []
    for article in raw:
        title = article.get("title", "")
        if not title:
            continue

        blob = TextBlob(title)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            sentiment = "Bullish"
            confidence = min(abs(polarity), 1.0)
        elif polarity < -0.1:
            sentiment = "Bearish"
            confidence = min(abs(polarity), 1.0)
        else:
            sentiment = "Neutral"
            confidence = 1.0 - abs(polarity)

        headlines.append(
            HeadlineSentiment(
                title=title,
                source=article.get("source", "Unknown"),
                timestamp=article.get("date", ""),
                url=article.get("url", ""),
                sentiment=sentiment,
                confidence=round(confidence, 3),
            )
        )

    return headlines


def normalize_sentiment_score(headlines: list[HeadlineSentiment]) -> float:
    """Calculate overall sentiment score from -1.0 to +1.0."""
    if not headlines:
        return 0.0

    score_map = {"Bullish": 1.0, "Bearish": -1.0, "Neutral": 0.0}
    weighted_sum = sum(
        score_map[h.sentiment] * h.confidence for h in headlines
    )
    return round(weighted_sum / len(headlines), 4)


def calculate_sentiment_uniformity(headlines: list[HeadlineSentiment]) -> float:
    """Calculate sentiment uniformity (0.0 to 1.0, where 1.0 = total consensus)."""
    if not headlines:
        return 0.0

    sentiments = [h.sentiment for h in headlines]
    total = len(sentiments)

    # Count most common sentiment
    from collections import Counter

    counts = Counter(sentiments)
    most_common_count = counts.most_common(1)[0][1]

    return round(most_common_count / total, 4)
