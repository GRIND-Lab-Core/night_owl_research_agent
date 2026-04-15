# CLAIM_RISK_CHECKLIST.md — claim-wording-vs-evidence audit

> One row per non-trivial claim in the manuscript. Feeds `CLAIM_RISK_REPORT.md`.
> Every claim from `CLAIM_SUPPORT_MAP.md` is audited, plus any claim found in the
> draft that is *not* in the map (those default to `CRITICAL-unsupported`).

---

## Schema

| Column | Meaning |
|---|---|
| `ClaimID` | Same id as `CLAIM_SUPPORT_MAP.md`; `Cx-new` for claims found in the draft but absent from the map. |
| `Section` | Where the claim appears in the draft. |
| `Wording` | Verbatim or paraphrased draft sentence. |
| `Evidence` | Pointer: `APPROVED_CLAIMS.md#Cx` · `EXPERIMENT_LOG.md#EXP-N` · `LIT_REVIEW_REPORT.md#synthesis-theme` · `spatial-analysis/...` · `FIGURE_MANIFEST.md#FigN` · `—` |
| `EvidenceType` | `approved-claim` · `experiment-log` · `spatial-analysis` · `synthesis` · `paper-cache` · `figure-manifest` · `plan-only` · `none`. |
| `Confidence` | `High` · `Medium` · `Low` · `—`. |
| `Risk` | See risk categories below. |
| `RevisionAction` | `precise` · `soften` · `move-to-discussion` · `placeholder` · `cut` · `add-citation` · `ok` |
| `Resolved` | `yes` / `no` / `deferred` |

---

## Risk categories

- **CRITICAL-overclaim** — strong wording with no or weak evidence. Must be softened or cut before submission. Revision action: `soften` or `cut`.
- **CRITICAL-unsupported** — claim present in draft, absent from `CLAIM_SUPPORT_MAP.md`, no evidence locatable. Revision action: `cut` unless evidence can be produced in this round.
- **MAJOR-understated** — strong, direct evidence is available but the draft hedges unnecessarily. Revision action: `precise`.
- **MAJOR-misplaced** — low-confidence claim is stated as fact in Abstract or Results headline. Revision action: `move-to-discussion` with hedged language.
- **MAJOR-uncited** — claim about prior work without a citation; evidence is in `memory/paper-cache/` or the Synthesis section of `output/LIT_REVIEW_REPORT.md` but not surfaced. Revision action: `add-citation`.
- **MODERATE-drift** — wording has drifted from plan §12 in ways not justified by evidence. Revision action: `soften` or `precise` to re-align with plan.
- **MODERATE-placeholder** — claim is a known placeholder awaiting experiment results; draft should mark it clearly. Revision action: `placeholder`.
- **OK** — wording matches evidence confidence. Revision action: `ok`.

---

## Example rows

```markdown
| ClaimID | Section | Wording | Evidence | EvidenceType | Confidence | Risk | RevisionAction | Resolved |
|---|---|---|---|---|---|---|---|---|
| C1 | Abstract | "We achieve state-of-the-art macro-F1 of 0.87 on [dataset]" | APPROVED_CLAIMS.md#C1 (macro-F1 = 0.87, no SOTA comparison) | approved-claim | Medium | CRITICAL-overclaim | soften → "achieves a macro-F1 of 0.87, competitive with the strongest published baseline ([CITE: ...])" | yes |
| C4 | Results §6.2 | "This demonstrates the robustness of the method across regions" | — | none | — | CRITICAL-unsupported | cut — robustness not evaluated | yes |
| C7 | Introduction §1.3 | "GNN-based approaches dominate GeoAI segmentation" | LIT_REVIEW_REPORT.md#synthesis-2026-04-10-gnn-seg | synthesis | High | MAJOR-uncited | add-citation to 3 representative papers from synthesis | no |
| C9 | Discussion §7.2 | "Our system may generalize to other urban contexts" | spatial-analysis/transfer_pilot.md | spatial-analysis | Low | OK | ok | — |
```

---

## Audit procedure

1. For every row in `CLAIM_SUPPORT_MAP.md`, locate the claim in the draft. If missing, note as silently-dropped and decide whether to restore (evidence supports) or accept (plan §12 intended to cut).
2. Grep the draft for claim-like sentences (numbers, "first," "state-of-the-art," "outperforms," "significantly," novelty language) and match them against the map. Unmatched claims → `Cx-new`.
3. For each row: evidence type vs. wording strength. Apply the risk categories.
4. Decide the minimum revision action. Prefer `soften` / `precise` / `add-citation` over rewrites.
5. Apply revisions in `sections_revised/*.md`; mark row `Resolved = yes` and log before/after in `REVISION_LOG.md`.

## What never happens in this audit

- Inventing a metric number to upgrade a claim.
- Inventing a citation key to resolve `MAJOR-uncited`.
- Deleting a plan §17 limitation to resolve a Discussion-level claim-risk flag.
- Moving an overclaim from Abstract to Conclusion unchanged — overclaims are softened, not relocated.
