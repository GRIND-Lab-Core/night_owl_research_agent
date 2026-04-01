# Experiment Log

> Append results here as experiments complete. Never delete entries. Mark status with ✓ (SUCCESS), ✗ (FAILED), ⏳ (RUNNING), ⏸ (PENDING).

**Project**: [topic slug]
**Started**: [YYYY-MM-DD]

---

## Experiment 1 — OLS Baseline

**Status**: ⏳ PENDING
**Command**:
```bash
python GeoBenchmark/baselines/ols_baseline.py ...
```
**Run at**: —
**Duration**: —
**Output**: `GeoBenchmark/results/exp1_ols.json`

**Results**:
| Metric | Value |
|--------|-------|
| R² | — |
| Adj R² | — |
| RMSE | — |
| AIC | — |
| Moran's I residuals | — |
| Moran's I p-value | — |

**Notes**: —

---

## Experiment 2 — GWR Baseline

**Status**: ⏳ PENDING
**Command**:
```bash
python GeoBenchmark/baselines/gwr_baseline.py ...
```
**Run at**: —
**Duration**: —
**Output**: `GeoBenchmark/results/exp2_gwr.json`

**Results**:
| Metric | Value |
|--------|-------|
| R² | — |
| AICc | — |
| Bandwidth (adaptive) | — |
| Moran's I residuals | — |

**Notes**: —

---

## Experiment 3 — MGWR Baseline

**Status**: ⏳ PENDING
**Output**: `GeoBenchmark/results/exp3_mgwr.json`

**Results**:
| Metric | Value |
|--------|-------|
| R² | — |
| AICc | — |
| Per-variable bandwidths | — |
| Moran's I residuals | — |

---

## [Add experiments below as they run]

<!-- Template for new entry:
## Experiment N — [Name]
**Status**: ⏳ PENDING
**Command**: `python ...`
**Run at**: YYYY-MM-DD HH:MM
**Duration**: X min
**Output**: path
**Results**: [table]
**Notes**: [errors, observations, surprises]
-->
