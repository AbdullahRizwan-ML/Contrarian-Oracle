from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-20b"  # Fast model for Agents 1, 2, 3 (data collection)
    groq_model_smart: str = "openai/gpt-oss-120b"  # Smart model for Agent 4 (final arbitration)
    news_lookback_hours: int = 48
    max_news_results: int = 3
    yfinance_period: str = "6mo"
    cache_ttl_hours: int = 4
    chroma_persist_dir: str = "data/vectordb"
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k_retrieval: int = 2
    weight_technical_divergence: float = 0.25
    weight_sentiment_uniformity: float = 0.20
    weight_insider_activity: float = 0.25
    weight_fundamental_risk: float = 0.15
    weight_macro_headwinds: float = 0.15
    sec_user_agent: str = "ContrariOracle research@example.com"
    fred_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
