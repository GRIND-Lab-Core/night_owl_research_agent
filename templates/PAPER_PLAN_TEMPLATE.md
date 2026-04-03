# Paper Plan

**Title (working)**: [title]
**Target venue**: [venue] | **Word limit**: [N] | **Type**: empirical / review / methods
**Created**: [YYYY-MM-DD]

---

## Section Checklist

| Section | Word budget | Status | Score | File |
|---------|------------|--------|-------|------|
| Abstract | 250 | ⏳ pending | — | — |
| Introduction | 800 | ⏳ pending | — | — |
| Literature Review | 1500 | ⏳ pending | — | — |
| Methodology | 1200 | ⏳ pending | — | — |
| Results | 1000 | ⏳ pending | — | — |
| Discussion | 700 | ⏳ pending | — | — |
| Conclusion | 400 | ⏳ pending | — | — |
| References | — | ⏳ pending | — | — |

---

## Section 1: Abstract (250 words)

Key claims to include (from memory/approved_claims.md):
- [Claim 1 with specific number]
- [Claim 2]

Required elements: problem / gap / method / result / contribution

---

## Section 2: Introduction (800 words)

| Paragraph | Content | Key citations |
|-----------|---------|--------------|
| P1 Broad problem | [societal/scientific importance] | [2-3 authoritative] |
| P2 Scale/significance | [quantified stakes] | [WHO/IPCC/USGS] |
| P3 Current approaches | [state of field, strategic summary] | [5-6 representative] |
| P4 The gap | [precise gap statement] | [boundary papers from gap-analysis.md] |
| P5 Contribution | [numbered contributions from approved_claims.md] | — |
| P6 Organization | "The remainder of this paper..." | — |

---

## Section 3: Literature Review (1500 words, 3 themes)

| Theme | Papers | Focus |
|-------|--------|-------|
| [Theme 1: methods] | [list of papers] | [compare approaches] |
| [Theme 2: applications] | [list of papers] | [compare results/regions] |
| [Theme 3: evaluation] | [list of papers] | [compare datasets/metrics] |

Gap paragraph: bridge from synthesis to contribution.

---

## Section 4: Methodology (1200 words)

| Subsection | Content |
|-----------|---------|
| 4.1 Study Area | [coords/bbox, CRS, area km², why chosen] |
| 4.2 Data | [table: dataset, source, resolution, CRS, preprocessing] |
| 4.3 Methods | [OLS → GWR → MGWR pipeline + proposed; mgwr library] |
| 4.4 Evaluation | [metrics: R², AICc, RMSE, Moran's I; spatial CV protocol] |

CRS to state: [EPSG:XXXX] for storage; [EPSG:XXXX] for analysis.

---

## Section 5: Results (1000 words)

| Subsection | Content | Figure/Table |
|-----------|---------|-------------|
| 5.1 Model comparison | Lead with best approved claim + number | Table 1 |
| 5.2 Spatial patterns | Local R², coefficient maps | Figure 2, 3 |
| 5.3 Residual diagnostics | Moran's I before/after | Figure 4 |
| [5.4 if needed] | [additional analysis] | Figure 5 |

---

## Section 6: Discussion (700 words)

| Subsection | Content |
|-----------|---------|
| 6.1 Hypothesis | Confirm/refute RQs from research_contract.md |
| 6.2 Comparison | vs. prior work (specific metric values) |
| 6.3 Limitations | Specific (not generic); 3-5 items |
| 6.4 Implications | Who uses this? What decisions does it support? |

---

## Section 7: Conclusion (400 words)

Numbered contributions (mirror Introduction list).
Broader implications.
Future work: [3-5 specific directions from claim audit].

---

## Figures List

| Figure | Type | Data source | Command | Status |
|--------|------|------------|---------|--------|
| Fig 1 | Study area map | [path] | `python geo_benchmark/evaluation/visualize.py --type study_area ...` | ⏳ |
| Fig 2 | Model comparison | geo_benchmark/results/ | `python geo_benchmark/evaluation/visualize.py --type comparison_table ...` | ⏳ |
| Fig 3 | Local R² map | GWR/MGWR results | `python geo_benchmark/evaluation/visualize.py --type local_r2_map ...` | ⏳ |
| Fig 4 | Coefficient map | MGWR results | `python geo_benchmark/evaluation/visualize.py --type coefficient_map ...` | ⏳ |
| Fig 5 | Residual map | OLS/GWR results | `python geo_benchmark/evaluation/visualize.py --type residual_map ...` | ⏳ |
