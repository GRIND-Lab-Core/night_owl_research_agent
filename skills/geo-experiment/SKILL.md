---
name: geo-experiment
description: Designs and executes spatial analysis experiments with explicit sprint contracts. DESIGN mode writes EXPERIMENT_PLAN.md with hard pass/fail criteria before any code runs. EXECUTE mode runs the plan and a separate evaluator checks each result against the contract. Calls geo_benchmark/run_benchmark.py for OLS/GWR/MGWR comparisons.
tools: Bash, Read, Write
---

# Skill: geo-experiment

You design and run geo/spatial experiments. Python files are tools you call — you decide what to run and in what order.

**Sprint contract rule**: Before any experiment runs, both you (generator) and the evaluator must agree on what constitutes a PASS. Run DESIGN mode first; confirm the contract; then run EXECUTE mode.

---

## Mode: DESIGN — Write the Experiment Contract

Produce `EXPERIMENT_PLAN.md` from `research_contract.md`. This file IS the sprint contract — it defines success before any code runs.

### Steps

1. Read `research_contract.md` for: problem, proposed method, datasets, success criteria.
2. Read `configs/default.yaml` for scoring thresholds and domain constraints.
3. For each planned experiment, define the following contract fields:

```markdown
### Experiment: [name]

| Field | Value |
|---|---|
| Command | `python geo_benchmark/...` |
| Dataset | path/to/dataset.csv |
| Target variable | [col name] |
| Features | [col1, col2, ...] |
| Expected output path | geo_benchmark/results/[name].json |
| Estimated runtime | [N] minutes |

#### Pass/Fail Criteria (hard — evaluator checks these, not you)
- [ ] EXIT CODE 0 (non-zero = automatic FAIL, regardless of partial output)
- [ ] R² > [threshold] (e.g., 0.40 for OLS; failing this means proposed method shows no signal)
- [ ] Moran's I residuals p-value > 0.05 (spatial autocorrelation removed)
- [ ] MGWR R² > GWR R² > OLS R² (expected hierarchy; if violated, explain why)
- [ ] No NaN/Inf in coefficient outputs
- [ ] Runtime < [N] minutes (if exceeded, mark as TIMEOUT and subsample)

#### Evaluator Notes
[What should the evaluator pay particular attention to? What would surprise you?]
```

4. Required experiments (in this order):
   a. **Sanity check** — small sample to verify pipeline works end-to-end
   b. **OLS baseline** — global regression, establishes minimum R²
   c. **GWR baseline** — local regression with fixed bandwidth
   d. **MGWR baseline** — multiscale local regression (most complex, runs last)
   e. **Proposed method** — your custom model compared against (a–d)
   f. **Ablation experiments** — one component removed at a time (run only if (e) passes)

5. Write to `EXPERIMENT_PLAN.md` using template `templates/EXPERIMENT_PLAN_TEMPLATE.md`.

### Sanity Check (required before writing full plan)

Run the smallest experiment first. If it fails, do not write the plan — debug first (up to 3 attempts):
```bash
python geo_benchmark/run_benchmark.py \
  --dataset geo_benchmark/datasets/sample.csv \
  --models ols \
  --sample 200
```
If this still fails after 3 attempts: write a `BLOCKED_EXPERIMENTS.md` explaining the failure and stop. Do not fabricate a plan around a broken pipeline.

---

## Mode: EXECUTE — Run the Contract

Run experiments from `EXPERIMENT_PLAN.md`. A separate evaluator (not you) checks each result against the contract.

### Generator/Evaluator Split in Execution

You are the **generator**: run experiments, collect raw output, write to `EXPERIMENT_LOG.md`.
The **evaluator** is `spatial-analysis` skill: it reads results and determines PASS/FAIL against the contract criteria. You do not decide if your own experiment passed.

### Steps

1. Read `EXPERIMENT_PLAN.md`. Check `EXPERIMENT_LOG.md` for experiments already marked complete — skip them.
2. Run pending experiments in dependency order (baselines before proposed method, proposed method before ablations).
3. For each experiment:

   **Generator (you):**
   a. Execute the command exactly as written in the contract
   b. Capture stdout, stderr, and output file contents
   c. Write raw result to `EXPERIMENT_LOG.md`:
      ```
      [TIMESTAMP] EXPERIMENT: [name]
      Command: [exact command run]
      Exit code: [0 or N]
      Output file: [path]
      Key metrics (raw): R²=[value], RMSE=[value], runtime=[N]s
      Status: PENDING_EVAL
      ```

   **Evaluator (spatial-analysis skill):**
   d. Invoke skill `spatial-analysis` with the result and the contract criteria
   e. `spatial-analysis` returns: PASS / FAIL / PARTIAL per criterion
   f. Update `EXPERIMENT_LOG.md` status: SUCCESS / FAILED / PARTIAL

4. If an experiment fails the contract:

   | Failure type | Action |
   |---|---|
   | Exit code non-zero / import error | Check error; `pip install` if in requirements.txt; retry once |
   | MemoryError (GWR) | Retry with `--max-n 3000` |
   | MemoryError (MGWR) | Retry with `--max-n 1000` |
   | Runtime > limit | Retry with `--sample [N/2]`; mark as TIMEOUT-SUBSAMPLED |
   | R² below threshold | Do NOT retry; mark FAILED with note; continue to next experiment |
   | Moran's I p < 0.05 | Mark PARTIAL; note spatial autocorrelation remains in residuals |
   | Still failing after 2 retries | Mark as FAILED; continue; flag for human review in `findings.md` |

5. After all experiments complete:
   - Append one-line summary per result to `findings.md`
   - Write consolidated comparison to `memory/approved_claims.md` (only for PASS experiments)
   - Do NOT write claims from FAILED or PARTIAL experiments to approved_claims.md

### Key Python Tools

| Task | Command |
|---|---|
| Full OLS/GWR/MGWR benchmark | `python geo_benchmark/run_benchmark.py --dataset [path] --models ols gwr mgwr --target [col]` |
| OLS only | `python geo_benchmark/baselines/ols_baseline.py --dataset [path] --target [col] --features [cols]` |
| GWR only | `python geo_benchmark/baselines/gwr_baseline.py --dataset [path] --target [col] --features [cols] --max-n 5000` |
| MGWR only | `python geo_benchmark/baselines/mgwr_baseline.py --dataset [path] --target [col] --features [cols] --max-n 3000` |
| Download benchmark datasets | `python geo_benchmark/download_data.py` |
| Custom analysis | `python core/code_executor.py --script [path]` |

---

## Outputs

- `EXPERIMENT_PLAN.md` — sprint contract with hard pass/fail criteria (DESIGN mode)
- `EXPERIMENT_LOG.md` — execution record with PASS/FAIL status per criterion (EXECUTE mode)
- `findings.md` — one-line discoveries appended per run (both modes)
- `memory/approved_claims.md` — verified claims from PASS experiments only (EXECUTE mode)
- `geo_benchmark/results/` — model comparison JSON files (EXECUTE mode)

---

## Contract Violation Protocol

If you discover mid-execution that the contract criteria are impossible to meet with the available data:
1. Stop execution (do not run remaining experiments)
2. Write a `CONTRACT_VIOLATION.md` explaining: which criterion is impossible, why, what evidence you have
3. Propose revised criteria (do not silently lower the bar)
4. Set HUMAN_CHECKPOINT in `outputs/REVIEW_STATE.json` to require user review before continuing
