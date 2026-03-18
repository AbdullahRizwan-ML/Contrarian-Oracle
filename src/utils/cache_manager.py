"""Simple file-based cache to avoid redundant API calls."""
from __future__ import annotations

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any


class CacheManager:
    """Manages caching of expensive API/tool results."""

    def __init__(self, cache_dir: str = "data/cache", ttl_hours: int = 4):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _get_cache_key(self, operation: str, params: dict) -> str:
        """Generate cache key from operation + params."""
        key_string = f"{operation}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, operation: str, params: dict) -> Any | None:
        """Retrieve cached result if valid."""
        cache_key = self._get_cache_key(operation, params)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r") as f:
                cached = json.load(f)

            # Check if cache is still valid
            cached_time = datetime.fromisoformat(cached["timestamp"])
            if datetime.now() - cached_time > self.ttl:
                return None

            return cached["result"]
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

    def set(self, operation: str, params: dict, result: Any) -> None:
        """Store result in cache."""
        cache_key = self._get_cache_key(operation, params)
        cache_file = self.cache_dir / f"{cache_key}.json"

        cached_data = {
            "operation": operation,
            "params": params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }

        with open(cache_file, "w") as f:
            json.dump(cached_data, f, indent=2)

    def clear_old(self) -> int:
        """Remove expired cache entries."""
        removed = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r") as f:
                    cached = json.load(f)
                cached_time = datetime.fromisoformat(cached["timestamp"])
                if datetime.now() - cached_time > self.ttl:
                    cache_file.unlink()
                    removed += 1
            except Exception:
                continue
        return removed


# Global cache instance
cache_manager = CacheManager()
