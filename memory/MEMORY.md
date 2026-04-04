# GeoResearchAgent-247 — Session Memory

> **Read this file at the start of every Claude Code session.**
> The stop hook updates it automatically. Keep it under 200 lines — archive older entries to `memory/archive/`.

---

## Current Research State

```
Topic:           [not set — fill in program.md]
Mode:            —
Stage:           not started
Target journal:  [not set]
Run ID:          —
Last updated:    —
Overall status:  —
```

---

## Pipeline Stage Status

*(Updated by orchestrator and stop hook after each completed stage)*

- [ ] Stage 1: Literature Search
- [ ] Stage 2: Synthesis
- [ ] Stage 3: Gap Analysis
- [ ] Stage 4: Hypothesis Generation
- [ ] Stage 5: Outline
- [ ] Stage 6: Section Writing
  - [ ] Abstract
  - [ ] Introduction
  - [ ] Literature Review
  - [ ] Methodology
  - [ ] Results
  - [ ] Discussion
  - [ ] Conclusion
- [ ] Stage 7: References

---

## Active Paper Draft

```
File:                    —
Sections completed:      0 / 7
Sections accepted:       —
Review round:            —
Review decision:         —
Final paper path:        —
```

---

## Section Quality Scores

*(Track iterative improvement — accept if score ≥ 7.5)*

| Section | Draft 1 | Draft 2 | Draft 3 | Final | Status |
|---------|---------|---------|---------|-------|--------|
| Abstract | — | — | — | — | pending |
| Introduction | — | — | — | — | pending |
| Literature Review | — | — | — | — | pending |
| Methodology | — | — | — | — | pending |
| Results | — | — | — | — | pending |
| Discussion | — | — | — | — | pending |
| Conclusion | — | — | — | — | pending |

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

*(Populated by literature-scout — add entries after each lit-review stage)*

| # | Authors | Year | Title (short) | Venue | Method | Gap addressed |
|---|---------|------|--------------|-------|--------|--------------|
| — | — | — | — | — | — | — |

---

## Identified Research Gaps

*(Updated by gap-finder agent)*

1. —
2. —
3. —

---

## Hypotheses Evaluated

| # | Hypothesis (short) | Dataset | Model | Score | Decision |
|---|-------------------|---------|-------|-------|---------|
| — | — | — | — | — | — |

---

## geo_benchmark Results

*(Populated by benchmark runs — `python geo_benchmark/run_benchmark.py`)*

| Dataset | OLS R² | GWR R² | MGWR R² | Best model | Moran's I (best) |
|---------|--------|--------|---------|-----------|-----------------|
| — | — | — | — | — | — |

---

## Issues Log

*(API limits, blockers, human review flags)*

- —

## Last Action

- —

---

## Long-term Memory Highlights

*(Summarized from `.memory/long_term.json` — key facts worth surfacing)*

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
- Spatial CV: always use block CV or buffered LOBO, never random CV for spatial data
- CRS rule: always project to local UTM or equal-area before any distance/area computation
