"""
Experiment Agent — designs, executes, and analyzes geospatial experiments.
Delegates code generation to either Claude Code or Codex workers.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import anthropic

from core.config import AgentConfig

EXPERIMENT_SYSTEM_PROMPT = """\
You are a rigorous geoscientist designing reproducible experiments.
Always:
- Define clear evaluation metrics (R², RMSE, MAE, Moran's I)
- Include baseline comparisons (at minimum OLS)
- Specify train/test splits or cross-validation strategy
- Account for spatial autocorrelation in model evaluation
- Use established open-source datasets when possible
"""


class ExperimentAgent:
    """
    Designs experiment plans, generates or delegates code, executes it in a sandbox,
    and collects structured results.
    """

    def __init__(
        self,
        client: anthropic.Anthropic,
        config: AgentConfig,
        run_dir: Path,
    ) -> None:
        self.client = client
        self.config = config
        self.run_dir = run_dir
        self.results_dir = run_dir / "results"
        self.results_dir.mkdir(exist_ok=True)

    def run(
        self,
        hypotheses: list[dict[str, Any]],
        geo_context: dict[str, Any],
        coding_backend: Any | None = None,  # CodexWorker or None
    ) -> dict[str, Any]:
        """
        For each hypothesis: design → generate code → execute → collect results.
        """
        all_results = []

        for hyp in hypotheses[:self.config.experiment.max_iterations]:
            plan = self._design_experiment(hyp, geo_context)
            code = self._generate_code(plan, coding_backend)
            result = self._execute_code(code, hyp.get("id", "H?"))
            analysis = self._analyze_results(result, plan)
            all_results.append({
                "hypothesis": hyp,
                "plan": plan,
                "code": code,
                "raw_output": result,
                "analysis": analysis,
            })

        return {
            "results": all_results,
            "methods": self._extract_methods(all_results),
        }

    def _design_experiment(self, hypothesis: dict[str, Any], geo_context: dict[str, Any]) -> dict[str, Any]:
        """Use Claude to design an experiment plan for a hypothesis."""
        prompt = f"""Design a rigorous experiment to test this hypothesis:

## Hypothesis
{json.dumps(hypothesis, indent=2)}

## Domain Context
{json.dumps(geo_context, indent=2)}

Return a JSON object with:
- "title": short experiment title
- "dataset": recommended open dataset (name + source)
- "dependent_var": dependent variable
- "independent_vars": list of independent variables
- "model": primary model (e.g. "MGWR")
- "baseline": baseline model(s) for comparison
- "evaluation_metrics": list of metrics
- "spatial_validation": how to account for spatial autocorrelation
- "code_tasks": list of coding subtasks (strings)

Return ONLY valid JSON."""

        response = self.client.messages.create(
            model=self.config.backend.orchestrator,
            max_tokens=1024,
            system=EXPERIMENT_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"title": "Experiment", "model": "MGWR", "baseline": "OLS", "code_tasks": []}

    def _generate_code(self, plan: dict[str, Any], coding_backend: Any | None) -> str:
        """Generate experiment code via Codex worker or Claude."""
        task = f"""Write a complete Python experiment script for:
- Dataset: {plan.get('dataset', 'California Housing')}
- Dependent variable: {plan.get('dependent_var', 'y')}
- Independent variables: {plan.get('independent_vars', ['x1', 'x2'])}
- Primary model: {plan.get('model', 'MGWR')}
- Baseline models: {plan.get('baseline', 'OLS')}
- Metrics: {plan.get('evaluation_metrics', ['R2', 'RMSE'])}
- Output directory: {str(self.results_dir)}

The script must:
1. Load data and validate inputs
2. Run baseline (OLS) first
3. Run primary model
4. Compute all metrics
5. Save results to JSON: {str(self.results_dir)}/results.json
6. Generate coefficient map (for GWR/MGWR)
7. Run Moran's I test on residuals"""

        if coding_backend is not None:
            result = coding_backend.run_task(task, context=plan)
            return result.get("code", "")
        else:
            # Use Claude for code generation
            response = self.client.messages.create(
                model=self.config.backend.orchestrator,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": f"Write Python code only (no explanation):\n\n{task}"}
                ],
            )
            code = response.content[0].text
            # Strip markdown fences
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0]
            return code.strip()

    def _execute_code(self, code: str, hypothesis_id: str) -> dict[str, Any]:
        """Execute generated code in a subprocess sandbox."""
        if not self.config.experiment.save_intermediate:
            return {"status": "skipped", "stdout": "", "stderr": ""}

        # Write code to temp file
        code_file = self.results_dir / f"experiment_{hypothesis_id}.py"
        code_file.write_text(code)

        try:
            proc = subprocess.run(
                ["python", str(code_file)],
                capture_output=True,
                text=True,
                timeout=self.config.experiment.sandbox_timeout_sec,
                cwd=str(self.run_dir.parent.parent),  # project root
            )
            return {
                "status": "success" if proc.returncode == 0 else "error",
                "stdout": proc.stdout[:2000],
                "stderr": proc.stderr[:1000],
                "returncode": proc.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "stdout": "", "stderr": "Execution timed out"}
        except Exception as e:
            return {"status": "error", "stdout": "", "stderr": str(e)}

    def _analyze_results(self, execution_result: dict[str, Any], plan: dict[str, Any]) -> str:
        """Use Claude to interpret execution results."""
        prompt = f"""Analyze these experiment results for a geospatial study.

## Experiment Plan
{json.dumps(plan, indent=2)[:500]}

## Execution Output
Status: {execution_result.get('status')}
Stdout: {execution_result.get('stdout', '')[:1000]}
Stderr: {execution_result.get('stderr', '')[:500]}

Provide a brief (3–4 sentences) interpretation:
1. What do the results show?
2. Do they support the hypothesis?
3. Any spatial patterns worth noting?
4. Limitations of this experiment."""

        response = self.client.messages.create(
            model=self.config.backend.orchestrator,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    @staticmethod
    def _extract_methods(results: list[dict[str, Any]]) -> list[str]:
        methods = set()
        for r in results:
            plan = r.get("plan", {})
            if plan.get("model"):
                methods.add(plan["model"])
            if plan.get("baseline"):
                baseline = plan["baseline"]
                if isinstance(baseline, list):
                    methods.update(baseline)
                else:
                    methods.add(baseline)
        return list(methods)
