"""
geo_benchmark Runner — executes all or selected baselines and generates comparison report.

Usage:
    python geo_benchmark/run_benchmark.py --all
    python geo_benchmark/run_benchmark.py --dataset california_housing --models ols,gwr,mgwr
    python geo_benchmark/run_benchmark.py --dataset us_county_health --models ols,mgwr --output results/
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

DATASETS = ["california_housing", "boston_housing", "beijing_pm25", "us_county_health"]
MODELS = ["ols", "gwr", "mgwr", "kriging", "rf_spatial"]

MODEL_MODULES = {
    "ols": "geo_benchmark.baselines.ols_baseline",
    "gwr": "geo_benchmark.baselines.gwr_baseline",
    "mgwr": "geo_benchmark.baselines.mgwr_baseline",
}


def run_model(model_name: str, dataset_path: Path, output_dir: Path, target: str = "target") -> dict | None:
    """Import and run a baseline model."""
    if model_name not in MODEL_MODULES:
        console.print(f"[yellow]Model '{model_name}' not yet implemented, skipping.[/yellow]")
        return None

    try:
        import importlib
        module = importlib.import_module(MODEL_MODULES[model_name])
        start = time.time()
        result = module.run(
            dataset_path=dataset_path,
            dependent_var=target,
            output_dir=output_dir / model_name,
        )
        result["runtime_sec"] = round(time.time() - start, 1)
        return result
    except Exception as e:
        console.print(f"[red]Error running {model_name}: {e}[/red]")
        return {"model": model_name, "error": str(e)}


def print_comparison_table(results: list[dict]) -> None:
    """Print a rich comparison table of all model results."""
    table = Table(title="geo_benchmark Results", show_header=True, header_style="bold cyan")
    table.add_column("Model", style="bold")
    table.add_column("R²", justify="right")
    table.add_column("RMSE", justify="right")
    table.add_column("MAE", justify="right")
    table.add_column("AICc", justify="right")
    table.add_column("Moran's I", justify="right")
    table.add_column("Runtime (s)", justify="right")

    best_r2 = max((r.get("r2", 0) for r in results if "error" not in r), default=0)

    for r in results:
        if "error" in r:
            table.add_row(r.get("model", "?"), "[red]ERROR[/red]", "", "", "", "", "")
            continue

        r2_str = f"{r.get('r2', 0):.4f}"
        if r.get("r2", 0) == best_r2:
            r2_str = f"[green bold]{r2_str}[/green bold]"

        morans = r.get("morans_i_residuals", "N/A")
        morans_str = f"{morans:.4f}" if isinstance(morans, float) else str(morans)
        if isinstance(morans, float) and abs(morans) > 0.1 and r.get("morans_i_p_value", 1) < 0.05:
            morans_str = f"[red]{morans_str}[/red]"

        table.add_row(
            r.get("model", "?"),
            r2_str,
            f"{r.get('rmse', 0):.4f}",
            f"{r.get('mae', 0):.4f}",
            f"{r.get('aic', 0):.1f}",
            morans_str,
            f"{r.get('runtime_sec', 0):.1f}",
        )

    console.print(table)
    console.print("\n[dim]Moran's I > 0.1 in red = significant spatial autocorrelation in residuals[/dim]")


def generate_report(results: list[dict], dataset_name: str, output_dir: Path) -> None:
    """Generate a Markdown comparison report."""
    report = [
        f"# geo_benchmark Results: {dataset_name}\n",
        f"Generated: {pd.Timestamp.now().isoformat()}\n\n",
        "## Model Comparison\n\n",
        "| Model | R² | RMSE | MAE | AICc | Moran's I | Runtime (s) |\n",
        "|-------|-----|------|-----|------|-----------|-------------|\n",
    ]

    for r in results:
        if "error" in r:
            report.append(f"| {r.get('model')} | ERROR | | | | | |\n")
        else:
            report.append(
                f"| {r.get('model')} "
                f"| {r.get('r2', 0):.4f} "
                f"| {r.get('rmse', 0):.4f} "
                f"| {r.get('mae', 0):.4f} "
                f"| {r.get('aic', 0):.1f} "
                f"| {r.get('morans_i_residuals', 'N/A')} "
                f"| {r.get('runtime_sec', 0):.1f} |\n"
            )

    report.append("\n## Notes\n\n")
    report.append("- Moran's I close to 0 = no spatial autocorrelation in residuals (good)\n")
    report.append("- GWR/MGWR local R² variation reveals spatial non-stationarity\n")
    report.append("- MGWR per-variable bandwidths reveal scale of each relationship\n")

    # MGWR bandwidth interpretation
    mgwr_result = next((r for r in results if r.get("model") == "MGWR" and "error" not in r), None)
    if mgwr_result and mgwr_result.get("bandwidths_per_variable"):
        report.append("\n## MGWR Variable Bandwidths\n\n")
        n = mgwr_result.get("n_observations", 1)
        for var, bw in mgwr_result["bandwidths_per_variable"].items():
            pct = bw / n * 100
            scale = "global (>80%)" if pct > 80 else ("regional (30–80%)" if pct > 30 else "local (<30%)")
            report.append(f"- **{var}**: bandwidth={bw} ({pct:.1f}% of obs) → {scale} scale\n")

    report_path = output_dir / f"benchmark_report_{dataset_name}.md"
    report_path.write_text("".join(report))
    console.print(f"\nReport saved to [cyan]{report_path}[/cyan]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run geo_benchmark")
    parser.add_argument("--all", action="store_true", help="Run all datasets and models")
    parser.add_argument("--dataset", type=str, help="Dataset name")
    parser.add_argument("--models", type=str, default="ols,gwr,mgwr", help="Comma-separated model list")
    parser.add_argument("--output", type=str, default="geo_benchmark/results/", help="Output directory")
    parser.add_argument("--target", type=str, default="target", help="Target variable column name")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_run = DATASETS if args.all else ([args.dataset] if args.dataset else ["california_housing"])
    models_to_run = [m.strip() for m in args.models.split(",")]

    all_results = {}

    for dataset_name in datasets_to_run:
        console.rule(f"[bold cyan]Dataset: {dataset_name}[/bold cyan]")

        dataset_path = Path("geo_benchmark/datasets") / dataset_name / f"{dataset_name}.csv"
        if not dataset_path.exists():
            console.print(f"[yellow]Dataset not found: {dataset_path}[/yellow]")
            console.print("Run: python geo_benchmark/download_data.py first")
            continue

        dataset_results = []
        for model_name in models_to_run:
            console.print(f"\n[bold]Running {model_name.upper()}...[/bold]")
            result = run_model(model_name, dataset_path, output_dir / dataset_name, args.target)
            if result:
                dataset_results.append(result)

        if dataset_results:
            print_comparison_table(dataset_results)
            generate_report(dataset_results, dataset_name, output_dir)

            all_results[dataset_name] = dataset_results

    # Save master results JSON
    master_path = output_dir / "all_results.json"
    master_path.write_text(json.dumps(all_results, indent=2, default=str))
    console.print(f"\nAll results → [cyan]{master_path}[/cyan]")


if __name__ == "__main__":
    main()
