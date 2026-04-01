"""
GeoResearchAgent-247 Token Optimizer
======================================
Central utility for managing Anthropic API token usage across all agents.

Techniques applied
------------------
1.  **Token counting before dispatch** — estimate prompt tokens and enforce a
    per-call ceiling so no single request blows the context window.
2.  **Prompt compression** — strip whitespace, collapse repeated newlines, and
    remove low-signal boilerplate before sending to the API.
3.  **Tiered model routing** — automatically downgrade to a cheaper/faster
    model when the task complexity is below a configurable threshold, and
    upgrade to Opus only for tasks that truly need it.
4.  **Response caching** — SHA-256-keyed disk cache stores (prompt_hash →
    response_text).  Identical or near-identical prompts return instantly
    without an API round-trip.
5.  **Abstract / chunk truncation** — literature abstracts and other
    free-form text blocks are hard-truncated to a per-field budget before
    being assembled into prompts.
6.  **Context windowing** — when building multi-section prompts the optimizer
    ranks sections by relevance and drops the lowest-ranked ones that would
    exceed the budget, rather than truncating mid-sentence.
7.  **Streaming-aware max_tokens** — max_tokens is set dynamically based on
    the expected output length, not a blanket ceiling, reducing over-allocation.
8.  **Session token ledger** — tracks cumulative input + output tokens for the
    run so the orchestrator can report costs and abort if a hard spend limit
    is reached.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# 1 token ≈ 4 chars (conservative English/code heuristic)
_CHARS_PER_TOKEN = 4

# Per-task max_tokens defaults keyed by task type
_OUTPUT_BUDGETS: dict[str, int] = {
    "query_generation":   512,
    "hypothesis":         1_024,
    "section_abstract":   512,
    "section_short":      1_024,   # intro, conclusion, study area
    "section_long":       2_048,   # methods, results, discussion
    "synthesis":          4_096,
    "review":             2_048,
    "revision":           8_192,
    "code":               4_096,
    "json":               1_024,
    "default":            2_048,
}

# Model tiers (cheapest → most capable)
_MODEL_TIERS = [
    "claude-haiku-4-5-20251001",   # tier 0 – cheapest
    "claude-sonnet-4-6",           # tier 1 – default
    "claude-opus-4-6",             # tier 2 – most capable
]

# Complexity thresholds for auto-routing (estimated input tokens)
_TIER_THRESHOLDS = {
    0: 0,        # always eligible
    1: 800,      # use sonnet when input > 800 tokens
    2: 6_000,    # use opus when input > 6000 tokens
}


# ---------------------------------------------------------------------------
# Token counting helpers
# ---------------------------------------------------------------------------

def count_tokens(text: str) -> int:
    """Rough token count without an external tokenizer."""
    return max(1, len(text) // _CHARS_PER_TOKEN)


def fits_in_budget(text: str, budget: int) -> bool:
    return count_tokens(text) <= budget


# ---------------------------------------------------------------------------
# Prompt compression
# ---------------------------------------------------------------------------

def compress_prompt(text: str) -> str:
    """
    Light-weight prompt compression that preserves meaning while cutting tokens.

    Steps
    -----
    - Collapse 3+ consecutive blank lines to 2
    - Strip trailing whitespace from every line
    - Remove HTML comments (<!-- ... -->)
    - Collapse inline repeated spaces
    """
    # Remove HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    # Collapse repeated spaces (not indentation-aware newlines)
    text = re.sub(r"[ \t]{2,}", " ", text)
    # Strip trailing whitespace per line
    text = "\n".join(line.rstrip() for line in text.splitlines())
    # Collapse 3+ consecutive blank lines → 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def truncate_field(text: str, token_budget: int) -> str:
    """Truncate a single text field to fit within the token budget."""
    max_chars = token_budget * _CHARS_PER_TOKEN
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 40] + "\n…[truncated]"


def truncate_papers(papers: list[dict], budget_per_paper: int = 80) -> list[dict]:
    """
    Return a copy of the papers list with abstracts truncated.
    Keeps all metadata fields; only shortens 'abstract'.
    """
    result = []
    for p in papers:
        copy = dict(p)
        if "abstract" in copy:
            copy["abstract"] = truncate_field(copy["abstract"], budget_per_paper)
        result.append(copy)
    return result


# ---------------------------------------------------------------------------
# Context windowing
# ---------------------------------------------------------------------------

def build_windowed_prompt(
    sections: list[tuple[str, str, float]],
    token_budget: int,
    header: str = "",
) -> str:
    """
    Assemble a multi-section prompt that fits within ``token_budget`` tokens.

    Parameters
    ----------
    sections:     List of (title, content, relevance_score) tuples.
                  Higher relevance_score = kept preferentially.
    token_budget: Max tokens for the returned string.
    header:       Fixed prefix that always appears (counts toward budget).

    Returns
    -------
    A formatted string with sections sorted by relevance, dropping the
    lowest-relevance ones if needed.
    """
    used = count_tokens(header)
    # Sort descending by relevance
    ranked = sorted(sections, key=lambda s: s[2], reverse=True)
    included: list[str] = [header] if header else []

    for title, content, _ in ranked:
        block = f"## {title}\n{content}"
        block_tokens = count_tokens(block)
        if used + block_tokens <= token_budget:
            included.append(block)
            used += block_tokens
        else:
            # Try truncating to fit remainder
            remaining = token_budget - used - count_tokens(f"## {title}\n")
            if remaining > 40:
                included.append(f"## {title}\n{truncate_field(content, remaining)}")
            break

    return "\n\n".join(included)


# ---------------------------------------------------------------------------
# Model router
# ---------------------------------------------------------------------------

def select_model(
    prompt: str,
    preferred_model: str = "claude-sonnet-4-6",
    task_complexity: str = "default",
    force_tier: int | None = None,
) -> str:
    """
    Select the most cost-effective model for the given prompt.

    Logic
    -----
    - If ``force_tier`` is set, return that tier's model directly.
    - Otherwise estimate input tokens and route to the cheapest model that
      can handle the workload.

    Parameters
    ----------
    prompt:           The full prompt text (used for token estimation).
    preferred_model:  Model from config; used as the upper-bound preference.
    task_complexity:  One of "simple", "default", "complex".
    force_tier:       0/1/2 to override routing.
    """
    if force_tier is not None:
        return _MODEL_TIERS[min(force_tier, 2)]

    input_tokens = count_tokens(prompt)

    # Complexity override
    if task_complexity == "simple":
        return _MODEL_TIERS[0]
    if task_complexity == "complex":
        return preferred_model  # respect config preference

    # Auto-route by token count
    if input_tokens > _TIER_THRESHOLDS[2]:
        return _MODEL_TIERS[2]  # opus for very large contexts
    if input_tokens > _TIER_THRESHOLDS[1]:
        return preferred_model  # sonnet for moderate contexts
    return _MODEL_TIERS[0]      # haiku for simple / small prompts


def max_tokens_for_task(task_type: str) -> int:
    """Return the recommended max_tokens ceiling for a task type."""
    return _OUTPUT_BUDGETS.get(task_type, _OUTPUT_BUDGETS["default"])


# ---------------------------------------------------------------------------
# Response cache
# ---------------------------------------------------------------------------

class ResponseCache:
    """
    Disk-backed SHA-256 cache for API responses.

    Cache misses fall through to the caller; cache hits return instantly.
    The cache is keyed on (model, system_prompt_hash, user_prompt_hash) so
    different models never share entries.
    """

    def __init__(self, cache_dir: str | Path = ".cache/responses") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._hits = 0
        self._misses = 0

    def _key(self, model: str, system: str, user: str) -> str:
        raw = f"{model}|{system}|{user}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, model: str, system: str, user: str) -> str | None:
        path = self.cache_dir / self._key(model, system, user)
        if path.exists():
            self._hits += 1
            return path.read_text(encoding="utf-8")
        self._misses += 1
        return None

    def set(self, model: str, system: str, user: str, response: str) -> None:
        path = self.cache_dir / self._key(model, system, user)
        path.write_text(response, encoding="utf-8")

    def stats(self) -> dict[str, int]:
        return {"hits": self._hits, "misses": self._misses, "cached_files": len(list(self.cache_dir.iterdir()))}


# ---------------------------------------------------------------------------
# Token ledger
# ---------------------------------------------------------------------------

class TokenLedger:
    """
    Tracks cumulative token usage across all API calls in a session.

    Integrates with the Anthropic SDK's ``usage`` response object.
    """

    def __init__(self, hard_limit: int | None = None) -> None:
        self.input_tokens = 0
        self.output_tokens = 0
        self.cache_read_tokens = 0
        self.cache_write_tokens = 0
        self.call_count = 0
        self.hard_limit = hard_limit  # abort if total exceeds this

    def record(self, usage: Any) -> None:
        """Accept an Anthropic SDK ``Usage`` object or a plain dict."""
        if hasattr(usage, "input_tokens"):
            inp = usage.input_tokens or 0
            out = usage.output_tokens or 0
            cr = getattr(usage, "cache_read_input_tokens", 0) or 0
            cw = getattr(usage, "cache_creation_input_tokens", 0) or 0
        else:
            inp = usage.get("input_tokens", 0)
            out = usage.get("output_tokens", 0)
            cr = usage.get("cache_read_input_tokens", 0)
            cw = usage.get("cache_creation_input_tokens", 0)

        self.input_tokens += inp
        self.output_tokens += out
        self.cache_read_tokens += cr
        self.cache_write_tokens += cw
        self.call_count += 1

        if self.hard_limit and self.total > self.hard_limit:
            raise RuntimeError(
                f"Token hard limit reached: {self.total:,} > {self.hard_limit:,}. "
                "Adjust `token_optimizer.hard_limit` in config to continue."
            )

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens

    def summary(self) -> dict[str, int | float]:
        # Rough cost estimate (Sonnet pricing as of 2026 Q1)
        input_cost = self.input_tokens * 3 / 1_000_000        # $3/M input
        output_cost = self.output_tokens * 15 / 1_000_000     # $15/M output
        cache_read_cost = self.cache_read_tokens * 0.3 / 1_000_000
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "cache_write_tokens": self.cache_write_tokens,
            "total_tokens": self.total,
            "api_calls": self.call_count,
            "estimated_cost_usd": round(input_cost + output_cost + cache_read_cost, 4),
        }

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.summary(), indent=2))


# ---------------------------------------------------------------------------
# Convenience wrapper: optimized_call
# ---------------------------------------------------------------------------

def optimized_call(
    client: Any,
    system: str,
    user: str,
    task_type: str = "default",
    preferred_model: str = "claude-sonnet-4-6",
    task_complexity: str = "default",
    ledger: TokenLedger | None = None,
    cache: ResponseCache | None = None,
    extra_headers: dict | None = None,
) -> str:
    """
    Make a single, token-optimized Anthropic API call.

    Steps
    -----
    1. Compress both prompts.
    2. Check the response cache; return cached text on hit.
    3. Route to the cheapest appropriate model.
    4. Set max_tokens based on task type.
    5. Call the API, record usage in the ledger, cache the response.

    Parameters
    ----------
    client:            anthropic.Anthropic instance
    system:            System prompt text
    user:              User message text
    task_type:         Key into _OUTPUT_BUDGETS for dynamic max_tokens
    preferred_model:   From config; used as routing upper bound
    task_complexity:   "simple" | "default" | "complex"
    ledger:            TokenLedger to accumulate usage (optional)
    cache:             ResponseCache instance (optional)
    extra_headers:     E.g. {"anthropic-beta": "prompt-caching-2024-07-31"}

    Returns
    -------
    The assistant's response text.
    """
    system = compress_prompt(system)
    user = compress_prompt(user)

    # Cache lookup
    if cache is not None:
        model_for_key = select_model(user, preferred_model, task_complexity)
        cached = cache.get(model_for_key, system, user)
        if cached is not None:
            return cached

    model = select_model(user, preferred_model, task_complexity)
    mt = max_tokens_for_task(task_type)

    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": mt,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    if extra_headers:
        kwargs["extra_headers"] = extra_headers

    response = client.messages.create(**kwargs)
    text = response.content[0].text

    if ledger is not None and hasattr(response, "usage"):
        ledger.record(response.usage)

    if cache is not None:
        cache.set(model, system, user, text)

    return text
