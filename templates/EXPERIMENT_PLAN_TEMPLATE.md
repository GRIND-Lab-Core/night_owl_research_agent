# Experiment Plan

**Research contract**: [link to research_contract.md]
**Created**: [YYYY-MM-DD]
**Status**: [ ] Draft  [ ] Sanity-checked  [ ] Approved  [ ] Running  [ ] Complete

---

## Experiments Overview

| # | Name | Model | Dataset | Success Metric | Est. Runtime | Status |
|---|------|-------|---------|---------------|-------------|--------|
| 1 | OLS baseline | OLS | [dataset] | R², Moran's I | 1 min | pending |
| 2 | GWR baseline | GWR | [dataset] | R², AICc | 10 min | pending |
| 3 | MGWR baseline | MGWR | [dataset] | R², AICc, bws | 30 min | pending |
| 4 | Proposed method | [method] | [dataset] | [metric] | [time] | pending |
| 5 | Ablation: [component] | [method -X] | [dataset] | [metric] | [time] | pending |

---

## Detailed Experiment Specs

### Experiment 1: OLS Baseline

**Command:**
```bash
python GeoBenchmark/baselines/ols_baseline.py \
  --dataset [path/to/data.csv] \
  --target [outcome_col] \
  --features [col1] [col2] [col3] \
  --output GeoBenchmark/results/exp1_ols.json
```

**Expected output**: `GeoBenchmark/results/exp1_ols.json`
**Success criteria**: R² > 0, Moran's I p-value computed
**Notes**: [any preprocessing needed]

---

### Experiment 2: GWR Baseline

**Command:**
```bash
python GeoBenchmark/baselines/gwr_baseline.py \
  --dataset [path/to/data.csv] \
  --target [outcome_col] \
  --lat-col [lat] --lon-col [lon] \
  --features [col1] [col2] [col3] \
  --kernel bisquare --adaptive \
  --max-n 5000 \
  --output GeoBenchmark/results/exp2_gwr.json
```

**Expected output**: `GeoBenchmark/results/exp2_gwr.json` + `exp2_gwr_local_coefficients.csv`
**Success criteria**: AICc < OLS AICc, Moran's I residuals < OLS Moran's I
**Notes**: Subsample flag `--max-n 5000` if dataset > 5000 rows

---

### Experiment 3: MGWR Baseline

**Command:**
```bash
python GeoBenchmark/baselines/mgwr_baseline.py \
  --dataset [path/to/data.csv] \
  --target [outcome_col] \
  --lat-col [lat] --lon-col [lon] \
  --features [col1] [col2] [col3] \
  --max-n 3000 --max-features 8 \
  --output GeoBenchmark/results/exp3_mgwr.json
```

**Expected output**: `GeoBenchmark/results/exp3_mgwr.json`
**Success criteria**: Per-variable bandwidths computed; AICc competitive with GWR
**Notes**: More intensive than GWR; max 3000 obs, max 8 features

---

### Experiment 4: Proposed Method

**Command:**
```bash
[command for proposed method]
```

**Expected output**: [path]
**Success criteria**: [specific threshold vs. baseline]
**Notes**: [implementation details]

---

### Experiment 5: Ablation — [Component Name]

**Command:**
```bash
[command with component removed]
```

**Expected output**: [path]
**Success criteria**: Performance drops vs. Exp 4 (validates component contribution)

---

## Success Gate

The experiment set is successful if:
- [ ] MGWR Moran's I residuals < 0.10 (spatial autocorrelation resolved)
- [ ] MGWR AICc < GWR AICc (multi-scale model justified)
- [ ] Proposed method meets criteria in research_contract.md
- [ ] All ablations completed (at least one confirms component contribution)

If gate fails: consult research_contract.md to decide whether to pivot method or dataset.

---

## Dataset Preprocessing

[Document any preprocessing steps BEFORE running experiments:]
1. [Step 1: e.g., project to UTM Zone X (EPSG:XXXXX)]
2. [Step 2: e.g., remove rows with NaN in target or features]
3. [Step 3: e.g., standardize features to mean=0, std=1]

```bash
# Preprocessing commands (if applicable)
python -c "[preprocessing code]"
```
