#!/usr/bin/env bash
# NORA — Stop Hook
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

# Benchmark results (look in geo_benchmark/results/)
bench_rows = []
for result_file in sorted(Path("geo_benchmark/results").glob("**/*.json"))[:5] if Path("geo_benchmark/results").exists() else []:
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
    content = replace_table_data(content, "geo_benchmark Results", fmt_benchmark())

MEMORY_FILE.write_text(content)
print(f"memory/MEMORY.md updated ({TS})")
PYEOF

# ── Write structured handoff.json for context-reset recovery ──────────────────
python3 - <<'PYEOF'
import json, os, glob
from pathlib import Path
from datetime import datetime, timezone

TS = datetime.now(timezone.utc).isoformat()

handoff = {
    "timestamp": TS,
    "schema_version": 1,
    "session_id": os.environ.get("GEO_AGENT_SESSION_ID", "unknown"),

    # Pipeline position — what stage are we at and what was last done?
    "pipeline": {
        "stage": None,
        "last_completed_step": None,
        "next_step": None,
        "auto_proceed": None,
    },

    # Review loop state — full copy from outputs/REVIEW_STATE.json if it exists
    "review_state": None,

    # Most recent experiment results (compact — just what the next agent needs)
    "last_experiment": {
        "dataset": None,
        "best_model": None,
        "best_r2": None,
        "morans_i": None,
        "ols_r2": None,
        "gwr_r2": None,
        "mgwr_r2": None,
    },

    # Paper draft state
    "paper": {
        "sections_accepted": [],
        "sections_pending": [],
        "last_written": None,
        "last_score": None,
    },

    # Token budget remaining (from token_usage.json if available)
    "token_budget": {
        "total_used": None,
        "estimated_cost_usd": None,
        "budget_remaining_pct": None,
    },

    # Recovery hints — what the next session should do first
    "recovery": {
        "read_first": [],
        "resume_skill": None,
        "human_checkpoint_needed": False,
        "notes": [],
    },
}

# ── Load outputs/REVIEW_STATE.json ─────────────────────────────────────────────────────
review_state_path = Path("outputs/REVIEW_STATE.json")
if review_state_path.exists():
    try:
        rs = json.loads(review_state_path.read_text())
        handoff["review_state"] = rs
        round_n = rs.get("round", 0)
        score = rs.get("score", 0)
        status = rs.get("status", "in_progress")
        if status != "complete":
            handoff["pipeline"]["stage"] = "Stage 6: Section Writing — review loop"
            handoff["pipeline"]["next_step"] = f"resume auto-review-loop at round {round_n + 1}"
            handoff["recovery"]["resume_skill"] = "auto-review-loop"
            handoff["recovery"]["read_first"].append("outputs/REVIEW_STATE.json")
            handoff["recovery"]["read_first"].append("outputs/AUTO_REVIEW.md")
            if score < 6.0:
                handoff["recovery"]["human_checkpoint_needed"] = True
                handoff["recovery"]["notes"].append(
                    f"Review score is {score}/10 — below 6.0; human review recommended"
                )
    except Exception as e:
        handoff["recovery"]["notes"].append(f"outputs/REVIEW_STATE.json parse error: {e}")

# ── Load latest geo_benchmark results ─────────────────────────────────────────
bench_results_dir = Path("geo_benchmark/results")
if bench_results_dir.exists():
    result_files = sorted(bench_results_dir.glob("**/*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    by_dataset: dict = {}
    for rf in result_files[:20]:
        try:
            r = json.loads(rf.read_text())
            if isinstance(r, dict) and r.get("model"):
                ds = Path(r.get("dataset", "unknown")).stem
                by_dataset.setdefault(ds, {})[r["model"]] = r
        except Exception:
            pass
    if by_dataset:
        ds_name = next(iter(by_dataset))
        models = by_dataset[ds_name]
        r2s = {m: models[m].get("r2", 0) for m in models}
        best = max(r2s, key=r2s.get) if r2s else None
        handoff["last_experiment"] = {
            "dataset": ds_name,
            "best_model": best,
            "best_r2": r2s.get(best),
            "morans_i": models.get(best, {}).get("morans_i_residuals"),
            "ols_r2": r2s.get("OLS"),
            "gwr_r2": r2s.get("GWR"),
            "mgwr_r2": r2s.get("MGWR"),
        }

# ── Load paper draft state ────────────────────────────────────────────────────
sections_dir = Path("outputs/papers")
accepted, pending = [], []
EXPECTED_SECTIONS = ["abstract", "introduction", "literature_review",
                     "methodology", "results", "discussion", "conclusion"]
if sections_dir.exists():
    written = {f.stem.lower() for f in sections_dir.glob("*.md")}
    for s in EXPECTED_SECTIONS:
        if any(s in w for w in written):
            accepted.append(s)
        else:
            pending.append(s)
    # Most recently written section
    latest = max(sections_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, default=None)
    handoff["paper"]["last_written"] = str(latest.name) if latest else None

handoff["paper"]["sections_accepted"] = accepted
handoff["paper"]["sections_pending"] = pending

# Derive overall stage if not already set by review loop
if not handoff["pipeline"]["stage"]:
    if len(accepted) == len(EXPECTED_SECTIONS):
        handoff["pipeline"]["stage"] = "Stage 7: References"
        handoff["pipeline"]["next_step"] = "compile references and finalize paper"
        handoff["recovery"]["resume_skill"] = "paper-write"
    elif accepted:
        next_sec = pending[0] if pending else None
        handoff["pipeline"]["stage"] = f"Stage 6: Section Writing — {next_sec or 'unknown'} next"
        handoff["pipeline"]["next_step"] = f"write {next_sec} section"
        handoff["recovery"]["resume_skill"] = "paper-write"
    elif Path("EXPERIMENT_LOG.md").exists():
        handoff["pipeline"]["stage"] = "Stage 5: Outline or Section Writing"
        handoff["pipeline"]["next_step"] = "run paper-plan or paper-write"
        handoff["recovery"]["resume_skill"] = "paper-plan"
    elif Path("memory/gap-analysis.md").exists():
        handoff["pipeline"]["stage"] = "Stage 3-4: Gap Analysis or Hypothesis Generation"
        handoff["pipeline"]["next_step"] = "run idea-discovery or geo-experiment"
        handoff["recovery"]["resume_skill"] = "idea-discovery"
    else:
        handoff["pipeline"]["stage"] = "Stage 1-2: Literature Search or Synthesis"
        handoff["pipeline"]["next_step"] = "run geo-lit-review"
        handoff["recovery"]["resume_skill"] = "geo-lit-review"

# ── Load token usage ──────────────────────────────────────────────────────────
output_dirs = sorted(
    [d for d in Path("output").glob("run_*") if d.is_dir()],
    key=lambda d: d.stat().st_mtime,
    reverse=True,
) if Path("output").exists() else []

if output_dirs:
    token_path = output_dirs[0] / "token_usage.json"
    if token_path.exists():
        try:
            tu = json.loads(token_path.read_text())
            handoff["token_budget"]["total_used"] = tu.get("total_tokens")
            handoff["token_budget"]["estimated_cost_usd"] = tu.get("estimated_cost_usd")
        except Exception:
            pass

# ── Standard recovery read list ───────────────────────────────────────────────
for f in ["memory/MEMORY.md", "research_contract.md", "findings.md"]:
    if Path(f).exists() and f not in handoff["recovery"]["read_first"]:
        handoff["recovery"]["read_first"].insert(0, f)

# ── Write handoff.json ────────────────────────────────────────────────────────
Path("handoff.json").write_text(json.dumps(handoff, indent=2, default=str))
print(f"handoff.json written ({TS}) — next stage: {handoff['pipeline']['stage']}")
PYEOF

# Send desktop notification
bash harness/hooks/notification.sh "NORA session ended — MEMORY.md + handoff.json updated" 2>/dev/null || true

exit 0
