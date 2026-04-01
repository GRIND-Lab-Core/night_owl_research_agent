---
name: run-experiment
description: Invoke skill geo-experiment to design and execute spatial experiments (OLS/GWR/MGWR). Reads EXPERIMENT_PLAN.md if it exists; otherwise runs geo-experiment in DESIGN mode first. Python tools are called by the skill, not directly.
---

Invoke skill `skills/geo-experiment/SKILL.md` with arguments: $ARGUMENTS

The skill decides which Python tools to call (GeoBenchmark/run_benchmark.py, baselines, etc.) based on context. Follow these steps:

1. **Parse arguments**: Accept either a YAML config path or a model name + dataset name.
   - If a YAML path is given, load it from `configs/`
   - If just a model name (ols/gwr/mgwr), use defaults from `configs/benchmark_only.yaml`

2. **Validate data**: Check that the specified dataset exists in `GeoBenchmark/datasets/`. If not, run:
   ```bash
   python GeoBenchmark/download_data.py --dataset {DATASET_NAME}
   ```

3. **Run the experiment**:
   - For OLS: `python GeoBenchmark/baselines/ols_baseline.py --dataset {DATASET} --output output/experiments/`
   - For GWR: `python GeoBenchmark/baselines/gwr_baseline.py --dataset {DATASET} --output output/experiments/`
   - For MGWR: `python GeoBenchmark/baselines/mgwr_baseline.py --dataset {DATASET} --output output/experiments/`
   - For full benchmark: `python GeoBenchmark/run_benchmark.py --all`

4. **Report results**: After execution, read the results JSON and report:
   - Model: R², RMSE, MAE
   - Moran's I on residuals (spatial autocorrelation check)
   - Key spatial patterns observed
   - Comparison table if multiple models were run

5. **Generate visualizations**: Run `python GeoBenchmark/evaluation/visualize.py` to produce maps and plots.

6. **Output**: Save a summary to `output/experiment_results_{timestamp}.md`.
