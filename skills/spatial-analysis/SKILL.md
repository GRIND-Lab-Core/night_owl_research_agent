---
name: spatial-analysis
description: Interprets spatial regression results. Reads GeoBenchmark outputs, computes and explains Moran's I, R², AICc comparisons, coefficient maps. Decides which spatial model best fits the data and why. Writes analysis narrative to findings.md and memory/MEMORY.md.
tools: Bash, Read, Write
---

# Skill: spatial-analysis

You interpret spatial analysis results and decide what they mean for the research. You call Python tools to compute statistics and then write the interpretation.

---

## Phase 1: Load Results

Read from `GeoBenchmark/results/` and `EXPERIMENT_LOG.md`:
- OLS results JSON: R², Adj-R², RMSE, MAE, AIC, BIC, Moran's I residuals
- GWR results JSON: R² (global), AICc, bandwidth, Moran's I residuals
- MGWR results JSON: R² (global), AICc, per-variable bandwidths, Moran's I residuals

If results don't exist yet, run skill `geo-experiment` in EXECUTE mode first.

---

## Phase 2: Model Comparison

Compare models systematically:

1. **Spatial autocorrelation check on OLS residuals**:
   If Moran's I p-value < 0.05: spatial model needed; OLS assumption violated.
   If Moran's I p-value ≥ 0.05: OLS may be sufficient; note this.

2. **GWR vs OLS improvement**:
   - ΔR² = GWR_R² - OLS_R² — report as improvement
   - ΔAIC = GWR_AIC - OLS_AIC — negative = GWR better
   - GWR Moran's I residuals < OLS Moran's I: spatial non-stationarity captured

3. **MGWR vs GWR improvement**:
   - Per-variable bandwidths: small (< 20 neighbors) = local process; large (> n/2) = global
   - Report which variables are local vs. regional vs. global scale
   - Interpret: "Variable X operates at local scale (bw=15), indicating hyper-local variation"

4. **Best model selection**:
   - Best AICc AND best Moran's I residuals (closest to 0) → preferred model
   - Write: "MGWR outperforms GWR (ΔR²=+0.08, ΔAIC=-24.3) and OLS (Moran's I: 0.31→0.04)"

---

## Phase 3: Coefficient Interpretation

For GWR/MGWR: read local coefficient CSV from results.

For each significant predictor:
- Compute: mean, std, % positive, % significant (p < 0.05 local)
- Identify spatial clusters of high/low coefficients using Moran's I on coefficients
- Write: "The effect of [predictor] is strongest in [region] (coef=X, p<0.01) and weakest in [region]"

To compute spatial stats:
```bash
python -c "
import geopandas as gpd, libpysal, esda, json
# read local coefficients CSV and compute stats
"
```

Or call the evaluation module:
```bash
python GeoBenchmark/evaluation/metrics.py --results [path] --output [path]
```

---

## Phase 4: Write Narrative

Write 3-5 paragraph analysis to `memory/spatial_analysis_YYYY-MM-DD.md`:
- Para 1: Data summary (N, spatial extent, outcome variable stats)
- Para 2: Spatial autocorrelation diagnostics
- Para 3: Model comparison table + interpretation
- Para 4: Key spatially varying effects
- Para 5: Implications for the research question

Append key findings to `findings.md` (one line each).
Update `memory/MEMORY.md` GeoBenchmark Results table.
