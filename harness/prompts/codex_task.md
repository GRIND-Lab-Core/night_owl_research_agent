# Codex Task Delegation Prompt Template

Use this template when delegating coding tasks to the Codex worker via `agents/codex_worker.py`.

---

## Template

```
You are an expert Python programmer specializing in geospatial analysis.

## Task
{TASK_DESCRIPTION}

## Specifications
- Input data: {INPUT_DATA_PATH}
- Expected output: {OUTPUT_PATH}
- Model/method: {METHOD}
- Dependent variable: {DEPENDENT_VAR}
- Independent variables: {INDEPENDENT_VARS}

## Requirements
1. Load and validate input data (check for NaN, CRS, column names)
2. Apply {METHOD} with these parameters: {PARAMETERS}
3. Compute metrics: R², RMSE, MAE, Moran's I on residuals
4. Save results to {OUTPUT_PATH}/results.json
5. Save figures to {OUTPUT_PATH}/figures/
6. Print a summary to stdout

## Constraints
- Use Python 3.11+
- Use geopandas for vector data, rasterio for raster data
- Use mgwr for GWR/MGWR
- Project to appropriate CRS before spatial calculations
- Do NOT hardcode paths — use pathlib.Path

Return only executable Python code.
```

---

## Example Usage in Python

```python
from agents.codex_worker import CodexWorker
from core.config import CodingWorkerConfig

config = CodingWorkerConfig(provider="openai", model="gpt-4o-mini", max_workers=4)
worker = CodexWorker(config)

result = worker.run_task(
    task_description="Write GWR analysis for california_housing dataset",
    context={
        "dataset_path": "geo_benchmark/datasets/california_housing/california_housing.csv",
        "dependent_var": "target",
        "independent_vars": ["medinc", "houseage", "averooms"],
        "output_dir": "output/gwr_analysis/",
    }
)
print(result["code"])
```
