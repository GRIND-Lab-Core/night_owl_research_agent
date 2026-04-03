---
name: paper-plan
description: Produces a detailed paper outline from research_contract.md, findings.md, and approved_claims.md. Creates section-by-section plan with word budgets, key claims per section, and figures list. Uses journal templates from templates/ for venue-specific formatting.
tools: Read, Write
---

# Skill: paper-plan

You produce a concrete, actionable paper outline before any writing begins.

---

## Phase 1: Gather Context

Read:
- `research_contract.md` — problem, method, contributions
- `memory/approved_claims.md` — verified results to highlight
- `memory/gap-analysis.md` — gaps addressed by this paper
- `memory/synthesis-YYYY-MM-DD.md` — related work context
- `outputs/AUTO_REVIEW.md` — if review has run, incorporate reviewer feedback into outline
- Target venue from `program.md` Section 2

---

## Phase 2: Select Template

Choose the appropriate template from `templates/`:
- Geoscience: `templates/geoscience/` — GRL, Nature Geoscience, JGR
- Remote Sensing: `templates/remote_sensing/` — RSE, IEEE TGRS, ISPRS
- GIScience: `templates/giscience/` — IJGIS, Transactions in GIS, AAG Annals

---

## Phase 3: Build Outline

Write `memory/outline.md` with:
- For each section: title, word budget, key claims to make, evidence to cite (from approved_claims.md), figures/tables needed
- Especially for Methods: list every tool/dataset/parameter to document
- For Results: reference specific table/figure numbers (pre-assign them)

Example structure:
```markdown
# Paper Outline: [Title]
Target: [venue] | Word limit: N | Type: empirical

## Section 1: Abstract (250 words)
Claims: [top 2-3 approved claims]
Required: problem / gap / method / 1+ specific number / contribution

## Section 2: Introduction (800 words)
Para 1: Broad problem (cite 2-3 authoritative sources)
Para 2: Scale/significance (quantified)
Para 3: Current approaches + shortcomings
Para 4: The specific gap (cite boundary papers from gap-analysis.md)
Para 5: Your contribution (numbered, match approved_claims.md)
Para 6: Paper organization

## Section 3: Literature Review (1500 words, 3 subsections)
Theme 1: [GWR/spatial methods — 8 papers]
Theme 2: [domain application — 10 papers]
Theme 3: [datasets and evaluation — 7 papers]
Gap paragraph: bridge to contribution

## Section 4: Methodology (1200 words)
4.1 Study Area (coords, CRS, area in km², why chosen)
4.2 Data (each dataset: source, resolution, temporal, preprocessing)
4.3 Methods (OLS → GWR → MGWR pipeline; proposed method)
4.4 Evaluation (metrics: R², AICc, Moran's I, RMSE; spatial CV protocol)

## Section 5: Results (1000 words)
Table 1: Model comparison (OLS/GWR/MGWR + proposed)
Figure 1: Local R² map
Figure 2: Key coefficient map
5.1 Main results — lead with best approved claim
5.2 Spatial patterns — coefficient variation
5.3 Moran's I residuals — spatial autocorrelation diagnostic

## Section 6: Discussion (700 words)
6.1 Confirm/refute hypothesis from research_contract.md
6.2 Compare to cited papers (specific numbers)
6.3 Limitations (specific, not generic)
6.4 Implications

## Section 7: Conclusion (400 words)
Numbered contributions (mirror Introduction)
Broader implications
Future work (3-5 specific directions from claim audit)
```

---

## Phase 4: Figure List

List all figures/tables with:
- Figure N: description, data source, which Python script to call
- `python geo_benchmark/evaluation/visualize.py --results [path] --type [map|scatter|comparison]`
- Or use `.claude/agents/geo-specialist.md` to suggest appropriate visualization

Write figure list to `memory/figure_plan.md`.
