# Findings Log

> One line per discovery. Append only — never delete. Used by COMPACT_MODE in auto-review-loop to save context. Date-stamped entries only.

**Format**: `[YYYY-MM-DD HH:MM] [TYPE] <one-line finding>`

Types: `RESULT` | `ALERT` | `DECISION` | `ANOMALY` | `CLAIM_VERIFIED` | `CLAIM_REMOVED`

---

<!-- Examples:
[2026-04-01 22:15] RESULT MGWR AICc=1234.5 beats GWR AICc=1289.3 on CA housing dataset (Δ=−54.8)
[2026-04-01 22:30] RESULT Moran's I residuals: OLS=0.31 → GWR=0.12 → MGWR=0.04 (p=0.21, not sig)
[2026-04-01 23:00] ALERT Experiment 4 FAILED — MemoryError on n=8402; retrying with max-n=3000
[2026-04-02 00:10] RESULT After subsampling: MGWR R²=0.73 vs GWR R²=0.65 (Δ=+0.08)
[2026-04-02 00:45] DECISION Dropping predictor Z (VIF=18.3, causes MGWR instability)
[2026-04-02 07:00] CLAIM_VERIFIED "MGWR outperforms GWR" verified in 4/4 datasets
[2026-04-02 07:30] CLAIM_REMOVED "20% improvement" overclaim — actual is 12% median across datasets
-->
