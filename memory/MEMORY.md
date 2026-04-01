# GeoResearchAgent-247 — Session Memory

> **Read this file at the start of every Claude Code session.**
> The stop hook updates it automatically. Keep it under 200 lines — archive older entries to `memory/archive/`.

---

## Current Research State

```
Topic:           [not set — pass via --topic or program.md]
Mode:            [quick | full-auto | codex-hybrid | benchmark-only]
Stage:           not started
Target journal:  [not set — pass via --journal]
Run ID:          —
Last updated:    —
Overall status:  —
```

---

## Active Paper Draft

```
File:                    —
Sections completed:      0 / 9
Sections accepted:       0
Review round:            —
Review decision:         —
Final paper path:        —
```

---

## Token Usage (Last Run)

```
Input tokens:       —
Output tokens:      —
Cache read tokens:  —
Total tokens:       —
API calls:          —
Estimated cost:     —
Cache hit rate:     —
```

---

## Key Papers Retrieved

*(Populated by literature agent — add entries after each lit-review stage)*

| # | Authors | Year | Title (short) | Venue | Method | Gap addressed |
|---|---------|------|--------------|-------|--------|--------------|
| — | — | — | — | — | — | — |

---

## Identified Research Gaps

*(Updated by literature agent)*

1. —
2. —
3. —

---

## Hypotheses Evaluated

| # | Hypothesis (short) | Dataset | Model | Result | Decision |
|---|-------------------|---------|-------|--------|---------|
| — | — | — | — | — | — |

---

## GeoBenchmark Results

*(Populated by benchmark runs — `python GeoBenchmark/run_benchmark.py`)*

| Dataset | OLS R² | GWR R² | MGWR R² | Best model | Moran's I (best) |
|---------|--------|--------|---------|-----------|-----------------|
| — | — | — | — | — | — |

---

## Section Quality Scores

*(Track iterative improvement — accept if score ≥ 7.5)*

| Section | Iteration | Novelty | Rigor | Lit | Clarity | Impact | Total | Decision |
|---------|-----------|---------|-------|-----|---------|--------|-------|---------|
| — | — | — | — | — | — | — | — | — |

---

## Long-term Memory Highlights

*(Summarized from `.memory/long_term.json` — key facts worth surfacing in conversations)*

- —

---

## Patterns Learned

*(What has worked / not worked — update when something surprising happens)*

- —

---

## Successful Search Queries

*(Record high-yield queries for reuse)*

- arXiv: —
- Semantic Scholar: —

---

## Runtime Notes

*(API limits, data issues, environment quirks)*

- mgwr library: GWR/MGWR requires subsampling for n > 3,000–5,000 (memory constraint)
- Abstract token budget: set to 80 tokens (≈320 chars) — increase in `configs/*.yaml` if synthesis feels shallow
- Response cache: stored in `.cache/responses/` — delete to force fresh API calls
