"""
GeoResearchAgent-247 Main Orchestrator
Entry point for running the full research loop or individual agent stages.

Usage:
    python core/orchestrator.py --config configs/full_auto.yaml --topic "..."
    python core/orchestrator.py --config configs/quick_mode.yaml --topic "..." --agents literature,writing
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import AgentConfig, load_config, get_default_config
from .research_loop import ResearchLoop
from .literature_manager import LiteratureManager
from .code_executor import CodeExecutor
from .paper_generator import PaperGenerator

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="GeoResearchAgent-247: Autonomous research agent for geoscientists",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full overnight research loop
  python core/orchestrator.py --config configs/full_auto.yaml --topic "Spatial non-stationarity in urban heat islands"

  # Quick draft
  python core/orchestrator.py --config configs/quick_mode.yaml --topic "GWR for house price prediction"

  # Claude + Codex hybrid
  python core/orchestrator.py --config configs/codex_hybrid.yaml --topic "SAR flood mapping"

  # Run only literature + writing, skip experiment and review
  python core/orchestrator.py --topic "MGWR applications" --agents literature,writing

  # GeoBenchmark only
  python core/orchestrator.py --config configs/benchmark_only.yaml
        """,
    )
    parser.add_argument("--config", type=str, default="configs/default.yaml", help="Path to YAML config file")
    parser.add_argument("--topic", type=str, default="", help="Research topic or hypothesis")
    parser.add_argument("--journal", type=str, default="", help="Target journal (e.g. IJGIS, RSE, IEEE_TGRS)")
    parser.add_argument(
        "--agents",
        type=str,
        default="",
        help="Comma-separated list of agents to run (literature,experiment,writing,review)",
    )
    parser.add_argument(
        "--skip",
        type=str,
        default="",
        help="Comma-separated list of agents to skip",
    )
    parser.add_argument("--backend", type=str, choices=["claude-only", "codex-hybrid"], default="", help="Override backend mode")
    parser.add_argument("--output-dir", type=str, default="", help="Override output directory")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    return parser.parse_args()


def build_run_id() -> str:
    return f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def resolve_config(args: argparse.Namespace) -> AgentConfig:
    """Load config and apply CLI overrides."""
    config_path = Path(args.config)
    if config_path.exists():
        config = load_config(config_path)
    else:
        console.print(f"[yellow]Config file {args.config} not found, using defaults.[/yellow]")
        config = get_default_config()

    if args.topic:
        config.topic = args.topic
    if args.journal:
        config.writing.journal = args.journal
    if args.output_dir:
        config.output.base_dir = args.output_dir
    if args.agents:
        config.enabled_agents = [a.strip() for a in args.agents.split(",")]
    if args.skip:
        skip = {a.strip() for a in args.skip.split(",")}
        config.enabled_agents = [a for a in config.enabled_agents if a not in skip]
    if args.backend == "codex-hybrid":
        config.backend.coding_workers.provider = "openai"
        config.mode = "codex-hybrid"
    elif args.backend == "claude-only":
        config.backend.coding_workers.provider = "claude"

    return config


def print_banner(config: AgentConfig, run_id: str) -> None:
    console.print(
        Panel(
            f"[bold cyan]GeoResearchAgent-247[/bold cyan]\n\n"
            f"[white]Topic:[/white]   {config.topic or '(not set)'}\n"
            f"[white]Mode:[/white]    {config.mode}\n"
            f"[white]Backend:[/white] {config.backend.orchestrator}"
            + (f" + Codex ({config.backend.coding_workers.model})" if config.backend.coding_workers.provider == "openai" else "")
            + f"\n[white]Journal:[/white] {config.writing.journal}\n"
            f"[white]Agents:[/white]  {', '.join(config.enabled_agents)}\n"
            f"[white]Run ID:[/white]  {run_id}",
            title="[bold green]Starting Research Session[/bold green]",
            border_style="green",
        )
    )


def save_manifest(run_dir: Path, config: AgentConfig, run_id: str) -> None:
    """Save run manifest for reproducibility."""
    manifest = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "topic": config.topic,
        "mode": config.mode,
        "enabled_agents": config.enabled_agents,
        "backend": {
            "orchestrator": config.backend.orchestrator,
            "coding_worker_provider": config.backend.coding_workers.provider,
            "coding_worker_model": config.backend.coding_workers.model,
        },
        "journal": config.writing.journal,
    }
    with open(run_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)


def main() -> None:
    args = parse_args()
    config = resolve_config(args)
    run_id = build_run_id()

    # Setup output directory
    run_dir = Path(config.output.base_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    print_banner(config, run_id)

    if args.dry_run:
        console.print("[yellow]Dry run mode — no actions will be executed.[/yellow]")
        return

    if not config.topic and config.mode != "benchmark-only":
        console.print("[red]Error: --topic is required for non-benchmark modes.[/red]")
        return

    save_manifest(run_dir, config, run_id)

    # Execute research loop
    loop = ResearchLoop(config=config, run_dir=run_dir)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Running research loop...", total=None)

        try:
            result = loop.run()
            progress.update(task, description="[green]Research loop complete![/green]")
        except KeyboardInterrupt:
            progress.update(task, description="[yellow]Interrupted — saving checkpoint...[/yellow]")
            loop.save_checkpoint()
            console.print(f"\n[yellow]Session paused. Resume with: --run-id {run_id}[/yellow]")
            return
        except Exception as e:
            progress.update(task, description=f"[red]Error: {e}[/red]")
            raise

    console.print(
        Panel(
            f"[green]Research session complete![/green]\n\n"
            f"Outputs saved to: [cyan]{run_dir}[/cyan]\n"
            f"Final paper: [cyan]{run_dir / 'paper_final.md'}[/cyan]",
            title="[bold green]Done[/bold green]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()
