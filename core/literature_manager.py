"""
Literature Manager — caches and manages fetched papers to avoid redundant API calls.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class LiteratureManager:
    """Simple file-based cache for fetched papers and search results."""

    def __init__(self, cache_dir: str | Path = ".cache/literature") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def cache_key(self, query: str) -> str:
        return hashlib.md5(query.encode()).hexdigest()[:12]

    def get(self, query: str) -> list[dict] | None:
        key = self.cache_key(query)
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None

    def set(self, query: str, papers: list[dict]) -> None:
        key = self.cache_key(query)
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps(papers, indent=2))

    def get_or_fetch(self, query: str, fetch_fn) -> list[dict]:
        cached = self.get(query)
        if cached is not None:
            return cached
        result = fetch_fn(query)
        self.set(query, result)
        return result
