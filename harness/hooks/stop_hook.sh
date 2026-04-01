#!/usr/bin/env bash
# GeoResearchAgent-247 — Stop Hook
# Saves session checkpoint, updates memory/MEMORY.md, and notifies the user.

set -euo pipefail

CHECKPOINT_DIR="${GEO_AGENT_CHECKPOINT_DIR:-.checkpoints}"
LOG_DIR="${GEO_AGENT_LOG_DIR:-harness/logs}"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION_ID="${GEO_AGENT_SESSION_ID:-session_$(date +%s)}"
MEMORY_FILE="memory/MEMORY.md"

mkdir -p "$CHECKPOINT_DIR" "$LOG_DIR" memory

echo "${TS} | STOP | Session ${SESSION_ID} ended" >> "${LOG_DIR}/sessions.log"

# Copy current output to checkpoint
if [ -d "output" ]; then
    cp -r output "${CHECKPOINT_DIR}/${SESSION_ID}_output" 2>/dev/null || true
fi

# Update memory/MEMORY.md from the most recent run's output files
python3 - <<'PYEOF'
import json, os, glob, re
from pathlib import Path
from datetime import datetime, timezone

MEMORY_FILE = Path("memory/MEMORY.md")
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Find the most recent run directory ────────────────────────────────────────
output_dirs = sorted(
    [d for d in Path("output").glob("run_*") if d.is_dir()],
    key=lambda d: d.stat().st_mtime,
    reverse=True,
) if Path("output").exists() else []

run_dir = output_dirs[0] if output_dirs else None

# ── Collect stats ──────────────────────────────────────────────────────────────
token_stats = {}
if run_dir and (run_dir / "token_usage.json").exists():
    try:
        token_stats = json.loads((run_dir / "token_usage.json").read_text())
    except Exception:
        pass

manifest = {}
if run_dir and (run_dir / "manifest.json").exists():
    try:
        manifest = json.loads((run_dir / "manifest.json").read_text())
    except Exception:
        pass

hypotheses = []
if run_dir and (run_dir / "hypotheses.json").exists():
    try:
        hypotheses = json.loads((run_dir / "hypotheses.json").read_text())
    except Exception:
        pass

# Benchmark results (look in GeoBenchmark/results/)
bench_rows = []
for result_file in sorted(Path("GeoBenchmark/results").glob("**/*.json"))[:5] if Path("GeoBenchmark/results").exists() else []:
    try:
        r = json.loads(result_file.read_text())
        if isinstance(r, dict) and r.get("model"):
            bench_rows.append(r)
    except Exception:
        pass

# ── Build replacement blocks ───────────────────────────────────────────────────
def fmt_state():
    topic = manifest.get("topic") or "[not set]"
    mode  = manifest.get("mode")  or "[not set]"
    stage = "complete" if run_dir and (run_dir / "paper_final.md").exists() else (
            "writing"  if run_dir and (run_dir / "draft_v1.md").exists() else (
            "experiment" if run_dir and (run_dir / "experiment_log.json").exists() else (
            "literature" if run_dir and (run_dir / "literature_review.md").exists() else
            "not started")))
    journal = manifest.get("journal") or "[not set]"
    run_id  = run_dir.name if run_dir else "—"
    return (
        "```\n"
        f"Topic:           {topic}\n"
        f"Mode:            {mode}\n"
        f"Stage:           {stage}\n"
        f"Target journal:  {journal}\n"
        f"Run ID:          {run_id}\n"
        f"Last updated:    {TS}\n"
        f"Overall status:  {stage}\n"
        "```"
    )

def fmt_draft():
    if not run_dir:
        return "```\nFile: —\nSections completed: 0 / 9\n```"
    sections_done = sum(1 for s in [
        "abstract","introduction","study_area","data","methods",
        "results","discussion","conclusion","references"
    ] if any((run_dir / f"sections/{s}_{manifest.get('journal','')}_" ).parent.exists() for _ in [1]))
    final = run_dir / "paper_final.md"
    review_files = sorted(run_dir.glob("review_round_*.md"))
    decision = "—"
    if review_files:
        txt = review_files[-1].read_text()[:400]
        for d in ["Accept", "Minor Revision", "Major Revision", "Reject"]:
            if d.lower() in txt.lower():
                decision = d; break
    return (
        "```\n"
        f"File:                    {str(final) if final.exists() else 'draft_v1.md'}\n"
        f"Sections completed:      {len(list(run_dir.glob('sections/*.md')))} / 9\n"
        f"Sections accepted:       —\n"
        f"Review round:            {len(review_files)}\n"
        f"Review decision:         {decision}\n"
        f"Final paper path:        {str(final) if final.exists() else '—'}\n"
        "```"
    )

def fmt_tokens():
    if not token_stats:
        return "```\nInput tokens:  —\nOutput tokens: —\n```"
    total = token_stats.get("total_tokens", 0)
    calls = token_stats.get("api_calls", 1) or 1
    cr    = token_stats.get("cache_read_tokens", 0)
    hit_rate = f"{cr/(total+cr)*100:.0f}%" if (total + cr) else "—"
    return (
        "```\n"
        f"Input tokens:       {token_stats.get('input_tokens', '—'):,}\n"
        f"Output tokens:      {token_stats.get('output_tokens', '—'):,}\n"
        f"Cache read tokens:  {cr:,}\n"
        f"Total tokens:       {total:,}\n"
        f"API calls:          {calls:,}\n"
        f"Estimated cost:     ${token_stats.get('estimated_cost_usd', 0):.4f}\n"
        f"Cache hit rate:     {hit_rate}\n"
        "```"
    )

def fmt_hypotheses():
    if not hypotheses:
        return "| — | — | — | — | — | — |"
    rows = []
    for i, h in enumerate(hypotheses[:5], 1):
        hyp   = str(h.get("hypothesis", "—"))[:60]
        ds    = str(h.get("suggested_dataset", "—"))[:20]
        meth  = str(h.get("suggested_method", "—"))[:20]
        rows.append(f"| {i} | {hyp} | {ds} | {meth} | — | — |")
    return "\n".join(rows)

def fmt_benchmark():
    if not bench_rows:
        return "| — | — | — | — | — | — |"
    by_dataset: dict = {}
    for r in bench_rows:
        ds = Path(r.get("dataset","unknown")).stem
        by_dataset.setdefault(ds, {})[r.get("model","?")] = r
    rows = []
    for ds, models in by_dataset.items():
        ols  = models.get("OLS",  {}).get("r2", "—")
        gwr  = models.get("GWR",  {}).get("r2", "—")
        mgwr = models.get("MGWR", {}).get("r2", "—")
        r2s = {m: models[m].get("r2", 0) for m in models}
        best = max(r2s, key=r2s.get) if r2s else "—"
        mi   = models.get(best, {}).get("morans_i_residuals", "—")
        rows.append(f"| {ds} | {ols} | {gwr} | {mgwr} | {best} | {mi} |")
    return "\n".join(rows) if rows else "| — | — | — | — | — | — |"

# ── Patch MEMORY.md blocks ─────────────────────────────────────────────────────
if not MEMORY_FILE.exists():
    print("memory/MEMORY.md not found — skipping update")
    exit(0)

content = MEMORY_FILE.read_text()

def replace_block(content, section_header, new_block):
    """Replace the first code block (```...```) after section_header."""
    pattern = re.compile(
        rf"(## {re.escape(section_header)}.*?)(```.*?```)",
        re.DOTALL,
    )
    return pattern.sub(lambda m: m.group(1) + new_block, content, count=1)

content = replace_block(content, "Current Research State", fmt_state())
content = replace_block(content, "Active Paper Draft", fmt_draft())
content = replace_block(content, "Token Usage (Last Run)", fmt_tokens())

# Hypotheses table — replace the single data row placeholder
def replace_table_data(content, section_header, new_rows):
    pattern = re.compile(
        rf"(## {re.escape(section_header)}.*?\|[-| ]+\|\n)(.*?)(\n---)",
        re.DOTALL,
    )
    return pattern.sub(lambda m: m.group(1) + new_rows + "\n" + m.group(3), content, count=1)

if hypotheses:
    content = replace_table_data(content, "Hypotheses Evaluated", fmt_hypotheses())
if bench_rows:
    content = replace_table_data(content, "GeoBenchmark Results", fmt_benchmark())

MEMORY_FILE.write_text(content)
print(f"memory/MEMORY.md updated ({TS})")
PYEOF

# Send desktop notification
bash harness/hooks/notification.sh "GeoResearchAgent-247 session ended — MEMORY.md updated" 2>/dev/null || true

exit 0
