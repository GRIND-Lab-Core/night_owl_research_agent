# CLAIM_SUPPORT_MAP.md — template

> Every non-trivial claim in the manuscript draft gets one row.
> A "non-trivial claim" is any sentence that states a novel finding, a number, a
> comparison to prior work, or a contribution. Background sentences do not need rows.

| Claim ID | Section | Claim (verbatim or paraphrased) | Evidence Source | Evidence Type | Confidence | Notes |
|---|---|---|---|---|---|---|
| C1 | Abstract | [ ] | `memory/APPROVED_CLAIMS.md#C1` | approved-claim | High | — |
| C2 | Introduction §1.5 | [ ] | `output/EXPERIMENT_LOG.md#EXP-2` | experiment-log | Medium | softened from plan §5 |
| C3 | Results §6.1 | [ ] | `output/LIT_REVIEW_REPORT.md#synthesis-2026-04-10-RS-literature` | synthesis | High | — |
| C4 | Results §6.2 | [ ] | — | — | — | **PLACEHOLDER — depends on EXP-4** |
| C5 | Discussion §7.3 | [ ] | `output/spatial-analysis/autocorr_report.md` | spatial-analysis | Medium | qualified as "consistent with" |

## Evidence-type vocabulary

- `approved-claim` — row in `memory/APPROVED_CLAIMS.md`
- `experiment-log` — entry in `output/EXPERIMENT_LOG.md`
- `spatial-analysis` — report under `output/spatial-analysis/`
- `synthesis` — dated Synthesis section in `output/LIT_REVIEW_REPORT.md`
- `paper-cache` — record in `memory/paper-cache/<id>.json`
- `figure-manifest` — row in `output/figures/FIGURE_MANIFEST.md`
- `plan-only` — present in `PAPER_PLAN.md` but no independent evidence yet → **must be placeholder or cut**
- `external` — cited paper from synthesis; confidence set by how recent / central the source is

## Confidence rubric

- **High** — direct, primary, verified evidence; number or result can be stated precisely.
- **Medium** — indirect or partial evidence; claim must be stated cautiously ("we observed," "is consistent with").
- **Low** — evidence is a single signal, an ablation without replication, or a single-region analysis → claim belongs in Discussion, not Abstract or Results headline.
- **—** (blank) — no evidence → the claim must be a marked placeholder or cut.

## Unsupported or weak claims

List claims that appear in `PAPER_PLAN.md` but lack evidence in this draft. These feed `COVERAGE_GAPS.md`.

- [ ]
- [ ]
- [ ]
