from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from loguru import logger

from src.config.settings import settings


class DataCache:
    """SQLite-based caching layer for API responses."""

    def __init__(self, db_path: str = "data/cache/oracle_cache.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """Create the cache table if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS cache (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        created_at REAL NOT NULL,
                        ttl_hours REAL NOT NULL
                    )
                    """
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Error initializing cache DB: {e}")

    def get(self, key: str) -> str | None:
        """Return cached value if not expired, else None."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                row = conn.execute(
                    "SELECT value, created_at, ttl_hours FROM cache WHERE key = ?",
                    (key,),
                ).fetchone()

                if row is None:
                    return None

                value, created_at, ttl_hours = row
                if time.time() - created_at > ttl_hours * 3600:
                    conn.execute("DELETE FROM cache WHERE key = ?", (key,))
                    conn.commit()
                    return None

                return value
        except Exception as e:
            logger.error(f"Cache get error for '{key}': {e}")
            return None

    def set(self, key: str, value: str, ttl_hours: int | None = None) -> None:
        """Store a value with TTL (defaults to settings.cache_ttl_hours)."""
        if ttl_hours is None:
            ttl_hours = settings.cache_ttl_hours
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO cache (key, value, created_at, ttl_hours)
                    VALUES (?, ?, ?, ?)
                    """,
                    (key, value, time.time(), ttl_hours),
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Cache set error for '{key}': {e}")

    def is_valid(self, key: str) -> bool:
        """Check if a cache entry exists and is not expired."""
        return self.get(key) is not None

    def clear(self, ticker: str | None = None) -> None:
        """Clear cache for a specific ticker or all entries."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                if ticker:
                    conn.execute(
                        "DELETE FROM cache WHERE key LIKE ?",
                        (f"%{ticker.upper()}%",),
                    )
                else:
                    conn.execute("DELETE FROM cache")
                conn.commit()
                logger.info(
                    f"Cache cleared{f' for {ticker}' if ticker else ' (all)'}"
                )
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
