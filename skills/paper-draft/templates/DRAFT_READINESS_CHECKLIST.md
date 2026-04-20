# DRAFT_READINESS_CHECKLIST.md — template

> Run before selecting `DRAFT_MODE`. First block of "No" answers forces a lower mode.

## A. Plan completeness

- [ ] `PAPER_PLAN.md` §1 working title, one-sentence claim, short summary, keywords present
- [ ] §2 target journal + audience + tone set
- [ ] §4 gap statement is specific (names the unresolved dimension, not just "limited work exists")
- [ ] §5 contributions list is specific and matches contribution types
- [ ] §12 claim-to-evidence map has ≥1 row per contribution
- [ ] §19 section outline committed
- [ ] §25 readiness assessment filled in

## B. Evidence availability

- [ ] `memory/APPROVED_CLAIMS.md` contains ≥1 claim per core contribution
- [ ] `output/EXPERIMENT_LOG.md` has no `FAILED` entry for an experiment feeding a core claim
- [ ] `output/PROJ_NOTES.md` covers the main findings at a one-line level
- [ ] `output/LIT_REVIEW_REPORT.md` exists with Synthesis and Gap Analysis sections recent enough to ground Related Work

## C. Figures and tables

- [ ] `output/figures/FIGURE_MANIFEST.md` exists
- [ ] Every figure in `PAPER_PLAN.md` §13 either has `Status: Ready` or is marked manual-pending
- [ ] Hero / architecture figure is Ready (for system papers) or specified in detail (for skeleton mode)

## D. Citations

- [ ] Every "must cite" paper in plan §15 / §22 is in `memory/paper-cache/` or synthesis
- [ ] No citation in the plan is flagged `[VERIFY]` without resolution

## E. Review / governance

- [ ] `memory/MEMORY.md` does not flag pending accept / reject state that would block drafting
- [ ] `output/CONTRACT_VIOLATION.md` does not exist
- [ ] `output/AUTO_REVIEW.md` feedback from prior round (if any) has been folded into the plan

## Mode decision

- All of A + B + C + D + E pass → `full`
- A + partial B + C + D pass, but some results or figures pending → `partial`
- A partially fails, B mostly empty, or C missing manifest → `skeleton`

Record the chosen mode + the specific failing items in `DRAFT_README.md`.
