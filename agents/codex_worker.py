"""
Codex Worker — integrates OpenAI Codex / GPT-4o as a coding sub-worker.

When backend is set to "codex-hybrid", the orchestrator spawns these workers
for code generation tasks while Claude handles planning, writing, and review.
"""

from __future__ import annotations

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from core.config import CodingWorkerConfig


CODEX_SYSTEM_PROMPT = """\
You are an expert Python programmer specializing in geospatial analysis, remote sensing, and GIScience.
You write clean, well-documented, reproducible code. Always use:
- geopandas for vector data
- rasterio for raster data
- mgwr for GWR/MGWR models
- statsmodels for OLS/regression
- matplotlib or seaborn for plots
- pathlib.Path for file paths

Return ONLY executable Python code, no explanation outside of inline comments.
Always include a brief docstring at the top of each function.
"""


class CodexWorker:
    """
    Wraps OpenAI's API to act as a coding sub-agent for the research loop.

    Usage:
        worker = CodexWorker(config)
        result = worker.run_task("Write GWR analysis for california_housing dataset")
        # or run multiple tasks in parallel:
        results = worker.run_tasks_parallel([task1, task2, task3])
    """

    def __init__(self, config: CodingWorkerConfig) -> None:
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package not installed. Run: pip install openai")

        self.config = config
        self.client = openai.OpenAI()
        self.model = config.model

    def run_task(self, task_description: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Submit a single coding task to the Codex worker.

        Args:
            task_description: Natural language description of the coding task
            context: Optional dict with additional context (data paths, variable names, etc.)

        Returns:
            Dict with 'code' (str), 'language' (str), 'explanation' (str)
        """
        messages = [{"role": "system", "content": CODEX_SYSTEM_PROMPT}]

        user_content = task_description
        if context:
            user_content += f"\n\nContext:\n```json\n{json.dumps(context, indent=2)}\n```"

        messages.append({"role": "user", "content": user_content})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,  # low temperature for code generation
            max_tokens=4096,
        )

        code = response.choices[0].message.content or ""
        # Strip markdown code fences if present
        if code.startswith("```python"):
            code = code[9:]
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]

        return {
            "code": code.strip(),
            "language": "python",
            "model": self.model,
            "task": task_description,
        }

    def run_tasks_parallel(
        self, tasks: list[str], contexts: list[dict[str, Any]] | None = None
    ) -> list[dict[str, Any]]:
        """
        Run multiple coding tasks in parallel using a thread pool.

        Args:
            tasks: List of task descriptions
            contexts: Optional list of context dicts (same length as tasks)

        Returns:
            List of result dicts in the same order as input tasks
        """
        if contexts is None:
            contexts = [None] * len(tasks)

        results = [None] * len(tasks)
        max_workers = min(self.config.max_workers, len(tasks))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {
                executor.submit(self.run_task, task, ctx): i
                for i, (task, ctx) in enumerate(zip(tasks, contexts))
            }
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                results[idx] = future.result()

        return results

    def run_geo_analysis_task(
        self,
        analysis_type: str,
        dataset_path: str,
        dependent_var: str,
        independent_vars: list[str],
        output_dir: str = "output/",
    ) -> dict[str, Any]:
        """
        Convenience method for standard geospatial regression tasks.

        Args:
            analysis_type: One of "ols", "gwr", "mgwr", "kriging"
            dataset_path: Path to input data (CSV or GeoPackage)
            dependent_var: Name of dependent variable column
            independent_vars: List of independent variable column names
            output_dir: Directory to save results

        Returns:
            Generated code dict
        """
        task = f"""
Write a complete Python script to perform {analysis_type.upper()} analysis with the following specifications:

- Input data: {dataset_path}
- Dependent variable: {dependent_var}
- Independent variables: {', '.join(independent_vars)}
- Output directory: {output_dir}

The script should:
1. Load the data and validate columns
2. Handle missing values appropriately
3. Run the {analysis_type.upper()} model with appropriate parameters
4. Print model summary statistics (R², AIC, coefficients)
5. Save results to {output_dir}
6. Generate a map of local coefficients (for GWR/MGWR) or residuals
7. Run Moran's I test on residuals to check for spatial autocorrelation
"""
        context = {
            "analysis_type": analysis_type,
            "dataset_path": dataset_path,
            "dependent_var": dependent_var,
            "independent_vars": independent_vars,
            "output_dir": output_dir,
        }
        return self.run_task(task, context)
