---
name: idea-discovery
description: Generates 6-10 novel geo research ideas from literature gaps. Evaluates each on novelty, feasibility, and geo-domain fit. Requires geo-lit-review to have run first. Produces IDEA_REPORT.md.
tools: Read, Write
---

# Skill: idea-discovery

You generate and evaluate novel geo research ideas from the literature synthesis.

---

## Prerequisites

- `memory/synthesis-YYYY-MM-DD.md` must exist (run geo-lit-review first)
- `memory/gap-analysis.md` must exist

---

## Phase 1: Ideation

Read `memory/gap-analysis.md` and `memory/synthesis-YYYY-MM-DD.md`, then generate 6-10 candidate ideas. Each idea must:
- Address a specific identified gap
- Be testable with available data (open datasets only unless specified)
- Be feasible with tools available in this project (GeoBenchmark, mgwr, geopandas, rasterio)
- Connect to the domain focus in `research_contract.md` or `program.md`

**Geo-specific idea templates** (use as inspiration, not templates to fill):
- "Apply MGWR to [outcome] to detect multi-scale spatial non-stationarity in [region]"
- "Use [foundation model] embeddings as spatial features for [task] and compare to handcrafted geo features"
- "Integrate [sensor A] + [sensor B] to improve [metric] for [application] compared to single-sensor baselines"
- "Detect [spatial process] at [scale] using change detection in [temporal dataset] — first study in [underrepresented region]"
- "Add equity/EJ dimension to [existing method] by incorporating [vulnerability index] — address gap in [domain]"

For each idea, write:
- Title (≤ 12 words)
- Problem statement (2 sentences)
- Proposed method
- Suggested dataset (with source)
- Expected metric improvement over baseline
- Novelty justification: what exactly makes this new vs. cited papers

---

## Phase 2: Scoring

Score each idea on:
| Dimension | Weight | Criteria |
|---|---|---|
| Novelty | 35% | Not already published; cite the boundary paper |
| Geo-Feasibility | 30% | Can be done with open data + mgwr/geopandas/rasterio/sklearn |
| Domain Impact | 20% | Matters to geo/RS/GIScience community |
| Speed to Pilot | 15% | Can a pilot be run in < 3 CPU hours? |

**Reject ideas scoring < 5.0 total.** Document rejection reason in `IDEA_REPORT.md`.

---

## Phase 3: Produce IDEA_REPORT.md

Use template `templates/IDEA_CANDIDATES_TEMPLATE.md`. Include:
- Ranked idea table (title, scores, status: live/rejected)
- Full description of each live idea
- Recommended top idea with rationale

**Update** `findings.md`: append one line per live idea.
