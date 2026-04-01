---
name: geo-experiment
description: Designs and executes spatial analysis experiments. Calls GeoBenchmark/run_benchmark.py for OLS/GWR/MGWR comparisons, individual baseline scripts for focused runs, and core/code_executor.py for custom analysis. Writes EXPERIMENT_LOG.md. Operates in two modes: DESIGN (produce plan) and EXECUTE (run plan).
tools: Bash, Read, Write
---

# Skill: geo-experiment

You design and run geo/spatial experiments. Python files are tools you call — you decide what to run and in what order.

---

## Mode: DESIGN

Produce `EXPERIMENT_PLAN.md` from `research_contract.md`.

### Steps

1. Read `research_contract.md` for: problem, proposed method, success criteria, dataset path.
2. Read `configs/default.yaml` for scoring thresholds.
3. Define experiments in this order:
   a. **Baseline experiments** (always required):
      - OLS: `python GeoBenchmark/baselines/ols_baseline.py --dataset [path] --target [col] --features [cols]`
      - GWR: `python GeoBenchmark/baselines/gwr_baseline.py --dataset [path] --target [col] --features [cols]`
      - MGWR: `python GeoBenchmark/baselines/mgwr_baseline.py --dataset [path] --target [col] --features [cols]`
      - Full benchmark: `python GeoBenchmark/run_benchmark.py --dataset [path] --models ols gwr mgwr`
   b. **Proposed method** experiment (custom code or modified baseline)
   c. **Ablation experiments** (remove one component at a time)
4. For each experiment, specify: command, expected output path, success criteria, estimated runtime.
5. Write to `EXPERIMENT_PLAN.md` using template `templates/EXPERIMENT_PLAN_TEMPLATE.md`.

### Sanity Check

Before writing the full plan, run the smallest experiment:
```bash
python GeoBenchmark/run_benchmark.py --dataset GeoBenchmark/datasets/sample.csv --models ols --sample 200
```
If this fails, debug the error (up to 3 attempts) before writing the plan.

---

## Mode: EXECUTE

Run experiments from `EXPERIMENT_PLAN.md` and collect results.

### Steps

1. Read `EXPERIMENT_PLAN.md`. Check which experiments are already marked complete in `EXPERIMENT_LOG.md`.
2. Run pending experiments in dependency order.
3. For each experiment:
   a. Execute the command
   b. Parse stdout/stderr and output files
   c. Record in `EXPERIMENT_LOG.md`: command, result path, key metrics, status (SUCCESS/FAILED/TIMEOUT)
   d. Append to `findings.md`: one line per meaningful result
4. If an experiment fails:
   - Check error type (missing data, import error, memory error)
   - For memory errors on GWR/MGWR: add `--max-n 3000` or `--max-n 1000` to subsample
   - For import errors: call `pip install <package>` if in `requirements.txt`
   - Retry up to 2 times
   - If still failing: mark as FAILED in log, continue with remaining experiments

### Key Python Tools Available

| Task | Command |
|---|---|
| Full OLS/GWR/MGWR benchmark | `python GeoBenchmark/run_benchmark.py --dataset [path] --models ols gwr mgwr --target [col]` |
| OLS only | `python GeoBenchmark/baselines/ols_baseline.py --dataset [path] --target [col] --features [cols]` |
| GWR only | `python GeoBenchmark/baselines/gwr_baseline.py --dataset [path] --target [col] --features [cols] --max-n 5000` |
| MGWR only | `python GeoBenchmark/baselines/mgwr_baseline.py --dataset [path] --target [col] --features [cols] --max-n 3000` |
| Download benchmark datasets | `python GeoBenchmark/download_data.py` |
| Custom analysis via executor | `python core/code_executor.py --script [path]` |

---

## Outputs

- `EXPERIMENT_PLAN.md` — structured experiment plan (DESIGN mode)
- `EXPERIMENT_LOG.md` — execution record with results (EXECUTE mode)
- `findings.md` — one-line discoveries appended per run
- `GeoBenchmark/results/` — model comparison JSON files
