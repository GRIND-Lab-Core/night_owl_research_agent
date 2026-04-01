# GeoResearchAgent-247 — Session Memory

> **Read this file at the start of every Claude Code session.**
> The stop hook updates it automatically. Keep it under 200 lines — archive older entries to `memory/archive/`.

---

## Current Research State

```
Topic:           [not set — fill in program.md Section 1]
Mode:            [api | claude-code]
Stage:           not started
Target journal:  [not set — fill in program.md Section 2]
Run ID:          —
Last updated:    —
Overall status:  —
```

---

## Pipeline Stage Status

*(Updated by orchestrator and stop hook after each completed stage)*

- [ ] Stage 1: Literature Search — 0 papers cached
- [ ] Stage 2: Synthesis — file: —
- [ ] Stage 3: Gap Analysis — 0 gaps identified
- [ ] Stage 4: Hypothesis Generation — 0 hypotheses scored
- [ ] Stage 5: Outline — sections: —
- [ ] Stage 6: Section Writing
  - [ ] Abstract — score: pending
  - [ ] Introduction — score: pending
  - [ ] Literature Review — score: pending
  - [ ] Methodology — score: pending
  - [ ] Results — score: pending
  - [ ] Discussion — score: pending
  - [ ] Conclusion — score: pending
- [ ] Stage 7: References — status: pending

---

## Active Paper Draft

```
File:                    —
Sections completed:      0 / 7
Sections accepted:       0
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
|---|---------|------|--------------|-------|--------|--------------|\
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
|---|-------------------|---------|-------|-------|---------|\
| — | — | — | — | — | — |

---

## GeoBenchmark Results

*(Populated by benchmark runs — `python GeoBenchmark/run_benchmark.py`)*

| Dataset | OLS R² | GWR R² | MGWR R² | Best model | Moran's I (best) |
|---------|--------|--------|---------|-----------|-----------------|\
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
