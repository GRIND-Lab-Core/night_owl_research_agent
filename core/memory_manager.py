"""
GeoResearchAgent-247 Memory Manager
====================================
Provides three layers of memory that work together to keep context focused
and token usage efficient across agent stages and research sessions.

Layers
------
1. **Working memory** (in-process dict)
   Ephemeral per-run store; cleared when the process exits.  Agents read from
   and write to this during a single research loop without hitting disk.

2. **Session memory** (JSON on disk, per run_id)
   Survives an interrupted run and lets the orchestrator resume from a
   checkpoint.  Keys are stage names; values are compressed summaries, not
   raw outputs.

3. **Long-term memory** (JSON on disk, shared across runs)
   Stores reusable facts: literature embeddings, topic summaries, previously
   tested hypotheses, and their results.  Growing entries are automatically
   pruned to a configurable size budget.

Token-Aware Retrieval
---------------------
Every ``get`` path returns content that fits within a caller-specified
``token_budget``.  Older, lower-priority, or lower-similarity entries are
dropped first so the most relevant context always makes it into the prompt.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Rough token estimator (avoids tiktoken dependency)
# 1 token ≈ 4 characters for English / code (OpenAI heuristic)
# ---------------------------------------------------------------------------
def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _truncate_to_budget(text: str, budget: int) -> str:
    """Hard-truncate text so it fits within the token budget."""
    max_chars = budget * 4
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 40] + "\n...[truncated to fit token budget]"


# ---------------------------------------------------------------------------
# MemoryEntry — the atomic unit stored in session / long-term memory
# ---------------------------------------------------------------------------

class MemoryEntry:
    __slots__ = ("key", "value", "summary", "tokens", "timestamp", "priority", "tags")

    def __init__(
        self,
        key: str,
        value: Any,
        summary: str = "",
        priority: float = 1.0,
        tags: list[str] | None = None,
    ) -> None:
        self.key = key
        self.value = value
        self.summary = summary or _auto_summarize(value)
        self.tokens = _estimate_tokens(self.summary)
        self.timestamp = time.time()
        self.priority = priority
        self.tags = tags or []

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "summary": self.summary,
            "tokens": self.tokens,
            "timestamp": self.timestamp,
            "priority": self.priority,
            "tags": self.tags,
            # value is NOT persisted to avoid bloating the JSON file;
            # only the summary is stored long-term
        }

    @classmethod
    def from_dict(cls, d: dict) -> "MemoryEntry":
        e = cls.__new__(cls)
        e.key = d["key"]
        e.value = None          # value not persisted — summary is the long-term record
        e.summary = d["summary"]
        e.tokens = d.get("tokens", _estimate_tokens(e.summary))
        e.timestamp = d.get("timestamp", 0.0)
        e.priority = d.get("priority", 1.0)
        e.tags = d.get("tags", [])
        return e


def _auto_summarize(value: Any, max_chars: int = 600) -> str:
    """Convert an arbitrary value to a short text summary."""
    if isinstance(value, str):
        text = value
    elif isinstance(value, dict):
        # Keep only top-level string values and first element of lists
        parts = []
        for k, v in list(value.items())[:10]:
            if isinstance(v, str):
                parts.append(f"{k}: {v[:120]}")
            elif isinstance(v, list) and v:
                parts.append(f"{k}: [{str(v[0])[:80]}...]")
        text = "\n".join(parts)
    elif isinstance(value, list):
        text = "\n".join(str(item)[:120] for item in value[:8])
    else:
        text = str(value)
    return text[:max_chars].strip()


# ---------------------------------------------------------------------------
# MemoryManager
# ---------------------------------------------------------------------------

class MemoryManager:
    """
    Three-layer memory manager for GeoResearchAgent-247.

    Usage
    -----
    >>> mm = MemoryManager(run_id="run_20260331_143000")
    >>> mm.store("literature", result, priority=1.5, tags=["giscience"])
    >>> context = mm.build_context(["literature", "geo_context"], token_budget=2000)
    >>> mm.remember("hypothesis_h1_failed", "MGWR diverged on small n", long_term=True)
    >>> mm.persist()
    """

    # Max long-term memory entries before pruning triggers
    LT_MAX_ENTRIES = 200
    # Max tokens the full long-term store may occupy (used for budget checks)
    LT_TOKEN_BUDGET = 32_000

    def __init__(
        self,
        run_id: str = "default",
        session_dir: str | Path = ".checkpoints",
        long_term_dir: str | Path = ".memory",
    ) -> None:
        self.run_id = run_id
        self.session_path = Path(session_dir) / f"{run_id}_memory.json"
        self.long_term_path = Path(long_term_dir) / "long_term.json"

        Path(session_dir).mkdir(parents=True, exist_ok=True)
        Path(long_term_dir).mkdir(parents=True, exist_ok=True)

        # Working memory: fast in-process dict (stage → MemoryEntry)
        self._working: dict[str, MemoryEntry] = {}

        # Session memory: loaded from disk, covers current run_id
        self._session: dict[str, MemoryEntry] = {}

        # Long-term memory: shared across runs
        self._long_term: dict[str, MemoryEntry] = {}

        self._load_session()
        self._load_long_term()

    # ------------------------------------------------------------------
    # Public write API
    # ------------------------------------------------------------------

    def store(
        self,
        key: str,
        value: Any,
        summary: str = "",
        priority: float = 1.0,
        tags: list[str] | None = None,
        long_term: bool = False,
    ) -> None:
        """
        Store a value in working memory (and optionally long-term memory).

        Parameters
        ----------
        key:        Logical name, e.g. "literature", "hypothesis_h1"
        value:      Raw value (not persisted long-term; summary is)
        summary:    Human-readable summary; auto-generated if empty
        priority:   Higher = kept longer during pruning (default 1.0)
        tags:       Searchable labels, e.g. ["giscience", "spatial_lag"]
        long_term:  If True, also write to the shared long-term store
        """
        entry = MemoryEntry(key, value, summary=summary, priority=priority, tags=tags)
        self._working[key] = entry
        self._session[key] = entry
        if long_term:
            self._long_term[key] = entry
            self._prune_long_term()

    def remember(self, key: str, fact: str, priority: float = 1.0, tags: list[str] | None = None) -> None:
        """
        Store a plain-text fact in long-term memory (e.g. a failed hypothesis).
        Convenience wrapper around ``store(..., long_term=True)``.
        """
        self.store(key, fact, summary=fact, priority=priority, tags=tags, long_term=True)

    def update_priority(self, key: str, delta: float) -> None:
        """Adjust priority of an existing entry (e.g. boost after successful use)."""
        for store in (self._working, self._session, self._long_term):
            if key in store:
                store[key].priority = max(0.0, store[key].priority + delta)

    # ------------------------------------------------------------------
    # Public read API
    # ------------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve raw value from working memory (falls back to session)."""
        entry = self._working.get(key) or self._session.get(key)
        return entry.value if entry else default

    def get_summary(self, key: str, token_budget: int = 500) -> str:
        """Return the summary for a single key, truncated to budget."""
        entry = self._working.get(key) or self._session.get(key) or self._long_term.get(key)
        if not entry:
            return ""
        return _truncate_to_budget(entry.summary, token_budget)

    def build_context(
        self,
        keys: list[str],
        token_budget: int = 3000,
        include_long_term: bool = False,
        tags_filter: list[str] | None = None,
    ) -> str:
        """
        Build a token-budget-aware context string from the requested keys.

        Entries are ranked by priority (desc) then recency (desc).
        Lower-priority entries are dropped when the budget is exhausted.

        Parameters
        ----------
        keys:             Ordered list of keys to include (checked in all layers)
        token_budget:     Maximum tokens for the returned string
        include_long_term: Also search long-term store for unmatched keys
        tags_filter:      If set, only include entries that share at least one tag

        Returns
        -------
        A formatted string ready to embed in a prompt.
        """
        candidates: list[MemoryEntry] = []

        stores = [self._working, self._session]
        if include_long_term:
            stores.append(self._long_term)

        seen: set[str] = set()
        for key in keys:
            for store in stores:
                if key in store and key not in seen:
                    entry = store[key]
                    if tags_filter and not any(t in entry.tags for t in tags_filter):
                        continue
                    candidates.append(entry)
                    seen.add(key)
                    break

        # Sort: priority desc, then timestamp desc
        candidates.sort(key=lambda e: (e.priority, e.timestamp), reverse=True)

        lines: list[str] = []
        used_tokens = 0
        for entry in candidates:
            section = f"### {entry.key}\n{entry.summary}"
            section_tokens = _estimate_tokens(section)
            if used_tokens + section_tokens > token_budget:
                # Try to fit a truncated version
                remaining = token_budget - used_tokens - 10  # 10-token header buffer
                if remaining > 40:
                    section = f"### {entry.key}\n{_truncate_to_budget(entry.summary, remaining)}"
                    lines.append(section)
                break
            lines.append(section)
            used_tokens += section_tokens

        return "\n\n".join(lines)

    def search_long_term(self, query: str, token_budget: int = 1000, top_k: int = 5) -> str:
        """
        Simple keyword-based search over long-term memory summaries.
        Returns a formatted context string within the token budget.
        """
        query_tokens = set(re.split(r"\W+", query.lower()))
        scored: list[tuple[float, MemoryEntry]] = []

        for entry in self._long_term.values():
            text_tokens = set(re.split(r"\W+", entry.summary.lower()))
            overlap = len(query_tokens & text_tokens)
            if overlap > 0:
                score = overlap * entry.priority
                scored.append((score, entry))

        scored.sort(reverse=True)
        top = [e for _, e in scored[:top_k]]

        if not top:
            return ""

        lines: list[str] = ["## Relevant Long-term Memory"]
        used = _estimate_tokens(lines[0])
        for entry in top:
            section = f"**{entry.key}**: {entry.summary}"
            tok = _estimate_tokens(section)
            if used + tok > token_budget:
                break
            lines.append(section)
            used += tok
        return "\n".join(lines)

    def token_usage_report(self) -> dict[str, int]:
        """Return estimated token counts per memory layer."""
        return {
            "working_tokens": sum(e.tokens for e in self._working.values()),
            "session_tokens": sum(e.tokens for e in self._session.values()),
            "long_term_tokens": sum(e.tokens for e in self._long_term.values()),
            "long_term_entries": len(self._long_term),
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def persist(self) -> None:
        """Flush session and long-term memory to disk."""
        self._save_session()
        self._save_long_term()

    def _save_session(self) -> None:
        data = {k: v.to_dict() for k, v in self._session.items()}
        self.session_path.write_text(json.dumps(data, indent=2, default=str))

    def _save_long_term(self) -> None:
        data = {k: v.to_dict() for k, v in self._long_term.items()}
        self.long_term_path.write_text(json.dumps(data, indent=2, default=str))

    def _load_session(self) -> None:
        if self.session_path.exists():
            try:
                raw = json.loads(self.session_path.read_text())
                self._session = {k: MemoryEntry.from_dict(v) for k, v in raw.items()}
            except (json.JSONDecodeError, KeyError):
                self._session = {}

    def _load_long_term(self) -> None:
        if self.long_term_path.exists():
            try:
                raw = json.loads(self.long_term_path.read_text())
                self._long_term = {k: MemoryEntry.from_dict(v) for k, v in raw.items()}
            except (json.JSONDecodeError, KeyError):
                self._long_term = {}

    # ------------------------------------------------------------------
    # Pruning
    # ------------------------------------------------------------------

    def _prune_long_term(self) -> None:
        """
        Remove lowest-priority entries when the long-term store exceeds limits.
        Two criteria are checked: entry count and total token budget.
        """
        if len(self._long_term) <= self.LT_MAX_ENTRIES:
            total_tokens = sum(e.tokens for e in self._long_term.values())
            if total_tokens <= self.LT_TOKEN_BUDGET:
                return

        # Sort ascending by (priority, timestamp) — lowest priority / oldest first
        sorted_entries = sorted(
            self._long_term.items(),
            key=lambda kv: (kv[1].priority, kv[1].timestamp),
        )

        # Drop entries until both constraints are satisfied
        while sorted_entries:
            total_tokens = sum(e.tokens for e in self._long_term.values())
            if (
                len(self._long_term) <= self.LT_MAX_ENTRIES
                and total_tokens <= self.LT_TOKEN_BUDGET
            ):
                break
            key_to_remove, _ = sorted_entries.pop(0)
            self._long_term.pop(key_to_remove, None)
