#!/usr/bin/env python3
"""
GeoResearchAgent-247 — Interactive Launcher

Run this script to start a research session. You will be prompted to choose
your backend (Anthropic API or Claude Code subscription) before anything else runs.

Usage:
    python launch.py
    python launch.py --backend api --topic "GWR for flood risk" --journal IJGIS
    python launch.py --backend claude-code
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


# ── ANSI colours ──────────────────────────────────────────────────────────────
BOLD  = "\033[1m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED   = "\033[91m"
RESET = "\033[0m"


def banner() -> None:
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════╗
║          GeoResearchAgent-247  •  Research Launcher          ║
║   Geo / Remote Sensing / GIScience  •  Autoresearch Loop     ║
╚══════════════════════════════════════════════════════════════╝{RESET}
""")


def choose_backend() -> str:
    """Interactive prompt to select the runtime backend."""
    print(f"{BOLD}How would you like to run GeoResearchAgent-247?{RESET}\n")
    print(f"  {CYAN}1{RESET}  {BOLD}Anthropic API{RESET}  (requires ANTHROPIC_API_KEY)")
    print(f"     • Full autonomous pipeline — runs without you in the loop")
    print(f"     • Token optimizer, response cache, tiered model routing")
    print(f"     • geo_benchmark, Codex hybrid mode, harness hooks")
    print(f"     • Best for: overnight batch runs, reproducible experiments\n")
    print(f"  {CYAN}2{RESET}  {BOLD}Claude Code subscription{RESET}  (no API key needed)")
    print(f"     • Claude Code itself is the AI runtime — uses your claude.ai plan")
    print(f"     • Slash commands: /geo-search  /run-experiment  /write-section")
    print(f"     • Markdown agents, domain skills, MCP servers included")
    print(f"     • Best for: interactive research, step-by-step sessions\n")

    while True:
        choice = input(f"{BOLD}Enter 1 or 2 (or 'api' / 'claude-code'): {RESET}").strip().lower()
        if choice in ("1", "api"):
            return "api"
        if choice in ("2", "claude-code", "cc", "subscription"):
            return "claude-code"
        print(f"{YELLOW}  Please enter 1 or 2.{RESET}")


# ── API backend ───────────────────────────────────────────────────────────────

def check_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        env_file = Path(".env")
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["ANTHROPIC_API_KEY"] = key
                    break
    if not key:
        print(f"\n{RED}Error:{RESET} ANTHROPIC_API_KEY is not set.")
        print("Options:")
        print("  1. Create a .env file:  echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env")
        print("  2. Export it:           export ANTHROPIC_API_KEY=sk-ant-...")
        print(f"\nSee {CYAN}.env.example{RESET} for the full template.")
        sys.exit(1)
    masked = key[:10] + "..." + key[-4:]
    print(f"\n{GREEN}✓{RESET} ANTHROPIC_API_KEY found: {masked}")
    return key


def run_api_mode(args: argparse.Namespace) -> None:
    """Validate environment and launch the Python orchestrator pipeline."""
    print(f"\n{BOLD}{CYAN}── API Mode ─────────────────────────────────────────────────{RESET}")
    check_api_key()

    # Optional: check for extra API keys
    ss_key = os.environ.get("SEMANTIC_SCHOLAR_KEY", "")
    if ss_key:
        print(f"{GREEN}✓{RESET} SEMANTIC_SCHOLAR_KEY found (higher rate limits enabled)")
    else:
        print(f"{YELLOW}○{RESET} SEMANTIC_SCHOLAR_KEY not set (public rate limits apply)")

    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if openai_key:
        print(f"{GREEN}✓{RESET} OPENAI_API_KEY found (Codex hybrid mode available)")
    else:
        print(f"{YELLOW}○{RESET} OPENAI_API_KEY not set (Codex hybrid mode disabled)")

    # Read program.md if it exists and topic/journal not overridden
    program_file = Path("program.md")
    if program_file.exists() and not args.topic:
        print(f"\n{GREEN}✓{RESET} program.md found — using research brief")
    elif not args.topic and not program_file.exists():
        print(f"\n{YELLOW}Warning:{RESET} No --topic and no program.md found.")
        print(f"  Fill in {CYAN}program.md{RESET} before running the full pipeline.")
        print(f"  Quick start: python launch.py --backend api --topic \"Your topic\" --journal IJGIS")

    # Select run mode
    mode_map = {
        "quick":          "configs/quick_mode.yaml",
        "full":           "configs/full_auto.yaml",
        "benchmark":      "configs/benchmark_only.yaml",
        "codex":          "configs/codex_hybrid.yaml",
        "default":        "configs/default.yaml",
    }
    config_path = mode_map.get(args.mode, "configs/default.yaml")
    print(f"\n{BOLD}Run mode:{RESET}    {args.mode}  →  {config_path}")
    if args.topic:
        print(f"{BOLD}Topic:{RESET}       {args.topic}")
    if args.journal:
        print(f"{BOLD}Journal:{RESET}     {args.journal}")

    # Build orchestrator command
    py = shutil.which("python3") or shutil.which("python") or shutil.which("py") or "python"
    cmd: list[str] = [py, "core/orchestrator.py", "--config", config_path]
    if args.topic:
        cmd += ["--topic", args.topic]
    if args.journal:
        cmd += ["--journal", args.journal]
    if args.mode == "benchmark":
        cmd = [py, "geo_benchmark/run_benchmark.py"]

    print(f"\n{BOLD}Command:{RESET} {' '.join(cmd)}\n")
    confirm = input(f"{BOLD}Launch? [Y/n]: {RESET}").strip().lower()
    if confirm in ("", "y", "yes"):
        print(f"\n{GREEN}Starting pipeline...{RESET}\n{'─'*60}\n")
        subprocess.run(cmd, check=False)
    else:
        print("Aborted.")


# ── Claude Code subscription backend ─────────────────────────────────────────

CLAUDE_CODE_INSTRUCTIONS = f"""
{BOLD}{CYAN}── Claude Code Subscription Mode ────────────────────────────{RESET}

{BOLD}You are using Claude Code as the AI runtime.{RESET}
No API key required — your claude.ai subscription powers the agents.

{BOLD}Step 1{RESET} — Open this project in Claude Code:
  {CYAN}claude{RESET}                       (from this directory)
  or open in VS Code and use the Claude Code extension

{BOLD}Step 2{RESET} — Fill in your research brief:
  Edit  {CYAN}program.md{RESET}  to describe your topic, target journal,
  research questions, domain focus, and constraints.

{BOLD}Step 3{RESET} — Choose how to run:

  {BOLD}Full automated pipeline:{RESET}
    {CYAN}/full-pipeline{RESET}
    Runs all 12 pipeline stages end-to-end: literature search →
    synthesis → gap analysis → hypothesis generation → outline →
    section writing (with iterative scoring) → peer review →
    references → final paper assembly.

  {BOLD}Individual stages:{RESET}
    {CYAN}/geo-search{RESET}          Literature search using ArXiv + Semantic Scholar
    {CYAN}/lit-review <topic>{RESET}  Build literature review for a topic
    {CYAN}/find-gaps <topic>{RESET}   Identify research gaps from literature
    {CYAN}/run-experiment{RESET}      Run geo_benchmark (OLS / GWR / MGWR)
    {CYAN}/write-section{RESET}       Write a specific paper section
    {CYAN}/review-paper{RESET}        Simulated peer review
    {CYAN}/geo-plot{RESET}            Spatial visualization
    {CYAN}/submit-check{RESET}        Pre-submission validation

  {BOLD}Delegate to specialized agents:{RESET}
    In any message, Claude Code will route to the right specialist:
    • orchestrator      — full pipeline manager
    • literature-scout  — paper retrieval
    • synthesis-analyst — deep reading and extraction
    • gap-finder        — research gap identification
    • hypothesis-generator — novel angle generation
    • paper-writer      — section drafting
    • peer-reviewer     — critique and scoring
    • citation-manager  — APA 7th formatting
    • geo-specialist    — domain context injection

{BOLD}Memory & State:{RESET}
  Session state is tracked in  {CYAN}memory/MEMORY.md{RESET}
  Long-term findings in        {CYAN}.memory/long_term.json{RESET}
  Checkpoints in               {CYAN}.checkpoints/{RESET}

{BOLD}MCP Servers:{RESET}
  Configured in {CYAN}.mcp.json{RESET} — includes geo_mcp, arxiv_mcp, filesystem.
  These give Claude Code access to spatial data APIs.

{BOLD}Tip:{RESET} For an end-to-end overnight run with the API backend, use:
  {CYAN}python launch.py --backend api --mode full{RESET}
"""


def run_claude_code_mode(args: argparse.Namespace) -> None:
    print(CLAUDE_CODE_INSTRUCTIONS)

    # Check if 'claude' CLI is available
    claude_bin = shutil.which("claude")
    if claude_bin:
        print(f"{GREEN}✓{RESET} Claude Code CLI found at: {claude_bin}")
        launch = input(f"\n{BOLD}Launch Claude Code now? [Y/n]: {RESET}").strip().lower()
        if launch in ("", "y", "yes"):
            print(f"\n{GREEN}Starting Claude Code...{RESET}\n")
            subprocess.run(["claude"], check=False)
    else:
        print(f"{YELLOW}○{RESET} Claude Code CLI ('claude') not found in PATH.")
        print("  Install from: https://claude.ai/download")
        print("  Or open this folder directly in VS Code with the Claude Code extension.")


# ── CLI argument parser ───────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GeoResearchAgent-247 launcher — choose API or Claude Code backend",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python launch.py                                      # interactive
          python launch.py --backend api                        # API, use program.md
          python launch.py --backend claude-code                # subscription mode
          python launch.py --backend api --topic "GWR for urban heat island" --journal RSE
          python launch.py --backend api --mode benchmark       # geo_benchmark only
          python launch.py --backend api --mode codex           # Claude + Codex hybrid
        """),
    )
    p.add_argument(
        "--backend", choices=["api", "claude-code"],
        help="Runtime backend: 'api' (Anthropic API key) or 'claude-code' (subscription)",
    )
    p.add_argument("--topic", help="Research topic (overrides program.md)")
    p.add_argument("--journal", help="Target journal name")
    p.add_argument(
        "--mode",
        choices=["default", "quick", "full", "benchmark", "codex"],
        default="default",
        help="Run mode (API backend only)",
    )
    return p


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    banner()
    parser = build_parser()
    args = parser.parse_args()

    backend = args.backend or choose_backend()

    if backend == "api":
        run_api_mode(args)
    else:
        run_claude_code_mode(args)


if __name__ == "__main__":
    main()
