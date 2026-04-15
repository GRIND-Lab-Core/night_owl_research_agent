# NARRATIVE_REPORT.md

> Purpose: Single source-of-truth narrative consumed by the `paper-writing-pipeline`
> (`paper-plan` → `paper-figure-generate` → `paper-draft` → `paper-review-loop` → `paper-convert`).
> Rule: Be explicit, concrete, evidence-based. Every non-trivial statement must point to a source file.
> Writing-agent instruction: If it is not here, it will not appear in the paper. Do not paraphrase numbers.

---

## 0. Document Status

- **Narrative version**: [v0.1]
- **Last updated**: [YYYY-MM-DD]
- **Project codename**: [PROJECT_NAME]
- **Active idea** (from `research_contract.md`): [one-line]
- **Target venue**: [IJGIS / TGIS / RSE / NeurIPS / IEEE_JOURNAL / ...]
- **Manuscript type**: [Research Article / Methods / Short Communication]
- **Page budget**: [N pages, style: single/double column]
- **Overall confidence**: [High / Medium / Low]
- **Pipeline stage at time of writing**: [post-experiment / post-review / ...]

### Source Files Consumed
- `output/LIT_REVIEW_REPORT.md` — [one-line summary]
- `output/IDEA_REPORT.md` — [one-line summary]
- `output/refine-logs/FINAL_PROPOSAL.md` — [one-line summary]
- `output/refine-logs/EXPERIMENT_PLAN.md` — [one-line summary]
- `output/EXPERIMENT_RESULT.md` — [one-line summary]
- `output/AUTO_REVIEW._REPORT.md` — [one-line summary]
- [additional files scanned from the project]

### Missing / Unread Inputs
- [ ] [file] — [why missing, impact on narrative]

---

## 1. One-Paragraph Paper Summary

### Working Title
[Proposed manuscript title]

### One-Sentence Contribution
[Central claim — specific, defensible, evidence-backed.]

### Abstract-Style Summary (150–250 words)
[Problem → gap → method → data → main findings (with numbers) → significance.]

### Keywords
- [keyword 1]
- [keyword 2]
- [keyword 3]
- [keyword 4]
- [keyword 5]

---

## 2. Problem & Motivation

### Broad Problem
[2–4 sentences. Source: LIT_REVIEW_REPORT §Introduction-context, FINAL_PROPOSAL §Motivation.]

### Quantified Scale / Significance
[Numbers from literature or domain sources. Include citation keys.]

### Current Approaches and Their Shortcomings
[Condensed from LIT_REVIEW_REPORT thematic synthesis.]

---

## 3. Gap Analysis

Gaps closed by this work (from `LIT_REVIEW_REPORT.md §Gap Analysis`):

| # | Gap | Boundary citation(s) | How this work closes it |
|---|-----|----------------------|-------------------------|
| 1 | … | [key1, key2] | … |

---

## 4. Contributions

Numbered. Each must tie to a specific experiment, claim, and figure.

1. [Contribution 1] — evidence: `EXPERIMENT_RESULT.md §X`, Table 1, Fig 2
2. [Contribution 2] — evidence: …
3. [Contribution 3] — evidence: …

---

## 5. Method

### Study Area / Domain
[Coords, CRS, area, temporal window, why chosen. Source: `FINAL_PROPOSAL.md`, `data/DATA_MANIFEST.md`.]

### Datasets
| Dataset | Source | Resolution | Temporal | Preprocessing | Manifest ref |
|---------|--------|-----------|----------|---------------|--------------|
| …       | …      | …         | …        | …             | `data/DATA_MANIFEST.md §…` |

### Model / Pipeline
[Step-by-step description sufficient for `paper-draft` Methods section. Include baselines and proposed approach.]

### Hyperparameters and Training Setup
[Exact values. Source: `EXPERIMENT_PLAN.md`.]

### Evaluation Protocol
[Metrics, splits, spatial CV, diagnostics (e.g., Moran's I). Source: `EXPERIMENT_PLAN.md §Evaluation`.]

---

## 6. Experiments & Results

For each experiment in `EXPERIMENT_PLAN.md`:

### Experiment [ID] — [name]
- **Hypothesis**: …
- **Setup**: …
- **Success criteria** (from plan): …
- **Headline numbers** (verbatim from `EXPERIMENT_RESULT.md`): …
- **Tables/figures produced**: Table [id], Fig [id]
- **Pass / fail / partial**: …
- **Interpretation**: …

### Deferred / Not Executed
[Experiments proposed in FINAL_PROPOSAL / EXPERIMENT_PLAN but not run, and why.]

---

## 7. Claims–Evidence Matrix

| Claim | Source file | Quantitative support | Figure / Table | Status |
|-------|-------------|----------------------|----------------|--------|
| [claim 1] | `EXPERIMENT_RESULT.md §…` | R² = 0.78 | Fig 1 | approved |
| [claim 2] | `APPROVED_CLAIMS.md §…` | +4.2 pts vs baseline | Table 1 | approved |
| [claim 3] | — | — | — | [NEEDS_EVIDENCE] |

---

## 8. Figure & Table Plan

| ID | Type | Description | Data source | Priority | Auto/Manual |
|----|------|-------------|-------------|----------|-------------|
| Fig 1 | Hero | [detailed: what is compared, visual expectation, skim-reader takeaway] | manual | HIGH | manual |
| Fig 2 | Map | Local R² across study area | `output/spatial-analysis/local_r2.geojson` | HIGH | auto |
| Fig 3 | Bar | Ablation: component contribution | `output/figures/ablation.json` | MEDIUM | auto |
| Table 1 | Comparison | Main results vs baselines | `output/figures/main_results.json` | HIGH | auto |

### Hero Figure Specification
- **What it shows**: …
- **What is compared**: …
- **Expected visual difference**: …
- **Draft caption**: …
- **Why it helps a skim reader**: …

---

## 9. Related Work Synthesis

Grouped the way the paper will cite them. Source: `LIT_REVIEW_REPORT.md §Synthesis`.

### Theme 1: [name]
- [key_1] — one-line takeaway
- [key_2] — …

### Theme 2: [name]
- …

### Bridging paragraph to our contribution
[How these papers leave the gap this work fills.]

---

## 10. Limitations & Threats to Validity

Concrete, not generic. Include anything the reviewer raised but was not fixed.

- …
- …

---

## 11. Reviewer-Raised Issues & Resolution Status

Mirror of `AUTO_REVIEW._REPORT.md`.

| Severity | Issue | Round | Status | Resolution / Rationale |
|----------|-------|-------|--------|------------------------|
| CRITICAL | … | R1 | addressed | `EXPERIMENT_RESULT.md §…` |
| MAJOR | … | R2 | deferred | rationale |
| MINOR | … | R1 | rejected | rationale |

---

## 12. Future Work

3–5 specific directions derived from limitations and deferred experiments.

1. …
2. …
3. …

---

## 13. Venue Target & Page Budget

- **Venue**: [name]
- **Page limit**: [N pages, references counted? yes/no]
- **Citation style**: [natbib / IEEE cite / ACM / …]
- **Style-file location** (if known): `templates/…`
- **Anonymization required**: [yes/no]

---

## 14. Citation Seed List

Verified keys already in `LIT_REVIEW_REPORT.md` (paper-draft will reuse these, not re-verify):

- [key_1] — [short context: intro / related / method]
- [key_2] — …
- [key_3] — …

> Do NOT invent BibTeX here. `paper-draft` builds `references.bib` from verified keys.

---

## 15. Appendix: File-Level Provenance

| File | Role | Key content pulled |
|------|------|--------------------|
| `output/LIT_REVIEW_REPORT.md` | gap + synthesis | §Gap Analysis, §Theme-level syntheses |
| `output/IDEA_REPORT.md` | idea rationale | top-ranked idea justification |
| `output/refine-logs/FINAL_PROPOSAL.md` | problem / method | full method spec |
| `output/refine-logs/EXPERIMENT_PLAN.md` | experiment design | success criteria, run order |
| `output/EXPERIMENT_RESULT.md` | results | headline metrics |
| `output/AUTO_REVIEW._REPORT.md` | review issues | CRITICAL/MAJOR items |
| `memory/APPROVED_CLAIMS.md` | claim gate | verified claims only |
| `data/DATA_MANIFEST.md` | data provenance | dataset rows |
| `output/spatial-analysis/` | diagnostics | Moran's I, local R² |
| `output/figures/` | figure assets | JSON/CSV data for plots |
| [other scanned files] | … | … |

### Missing Inputs Recap
- [file] — impact: …
