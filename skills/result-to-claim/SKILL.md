---
name: result-to-claim
description: Validates that every claim in output/EXPERIMENT_PLAN.md is supported by actual results in output/EXPERIMENT_LOG.md. Removes or qualifies unsupported claims. Safety gate before paper writing. Prevents fabrication.
tools: Read, Write
---

# Skill: result-to-claim

You act as a claim auditor. No paper section may contain a claim not backed by a result in the experiment log.

---

## Phase 1: Extract Claims

Read `output/EXPERIMENT_PLAN.md` and any drafted paper sections.
Extract every testable claim as a list:
- "MGWR outperforms GWR on dataset X" — testable claim
- "Spatial non-stationarity is significant across all variables" — testable claim
- "Adding predictor Z improves R² by 15%" — testable claim
- "The effect of [variable] is larger in urban areas" — testable claim

---

## Phase 2: Match Claims to Results

For each claim, find the supporting result in `output/EXPERIMENT_PLAN.md`:
- Exact matching: find the specific model/dataset/metric value
- Mark as: VERIFIED (number found), QUALIFIED (directionally supported but different magnitude), UNSUPPORTED (no matching result)

---

## Phase 3: Handle Unsupported Claims

For each UNSUPPORTED claim:
1. Check if the experiment was planned but not yet run → add to `output/EXPERIMENT_PLAN.md` pending list
2. Check if the experiment was run but failed → mark claim as "planned future work"
3. If impossible to verify: REMOVE the claim

Write changes:
- Update paper sections to remove/qualify unsupported claims
- Add "Future Work" items for desirable but unrun experiments
- Write audit report to `memory/CLAIM_AUDIT_YYYY-MM-DD.md`

**Hard rule**: Do not proceed to paper writing if any critical claim (in Abstract or Contributions list) is UNSUPPORTED.

---

## Phase 4: Approved Claim List

Write verified claim list to `memory/APPROVED_CLAIMS.md`:
```
# Approved Claims — Verified Against Results

## Strong Claims (exact number in results)
- MGWR AICc = 1234.5 vs GWR AICc = 1289.3 (verified in output/results/mgwr_results.json)
- ...

## Qualified Claims (directional support, cite uncertainty)
- MGWR tends to outperform GWR on spatially non-stationary data (4/5 datasets tested)
- ...

## Future Work (not yet verified)
- Integration of temporal dynamics (planned, not implemented)
```
