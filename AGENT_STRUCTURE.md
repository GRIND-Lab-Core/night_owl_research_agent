# GeoResearchAgent-247: Architecture & Structure

## Overview

GeoResearchAgent-247 is a fully autonomous AI-powered research agent designed specifically for **Geoscientists**, **Remote Sensing researchers**, and **GIScientists**. It combines large-language-model orchestration with domain-specific tools, journal templates, spatial benchmarks, and harness engineering to accelerate the full research lifecycle — from literature review through experiment, paper writing, and peer-review simulation.

---

## Directory Structure

```
geo_research_agent_247/
│
├── launch.py                   ← START HERE: backend selector (API vs Claude Code)
├── program.md                  ← Research brief (12 sections, edit before run)
├── research_contract.md        ← Active idea context (condensed, agents read this)
├── findings.md                 ← Compact one-line discovery log (append-only)
├── EXPERIMENT_LOG.md           ← Complete experiment record (append-only)
├── handoff.json                ← Context-reset handoff (written by stop hook on exit)
├── CLAUDE.md                   ← Agent dashboard: flags, key files, skill table
├── AGENT_STRUCTURE.md          ← You are here: visual map of the system
├── README.md                   ← Full usage guide and quick-start
├── settings.json               ← Claude Code hooks, permissions, env vars
├── pyproject.toml              ← Python package & dependency declaration
│
├── .claude/
│   ├── commands/               ← Slash commands (user-invocable, 7 total)
│   │   ├── launcher.md         ← /launcher  — interactive entry point (backend + task choice)
│   │   ├── full-pipeline.md    ← /full-pipeline — 4-stage autonomous research run
│   │   ├── find-gaps.md        ← /find-gaps <topic> — idea discovery from literature gaps
│   │   ├── lit-review.md       ← /lit-review <topic> — full literature review pipeline
│   │   ├── geo-search.md       ← /geo-search <topic> — targeted ArXiv + Scholar search
│   │   ├── write-section.md    ← /write-section <name> — write one paper section
│   │   └── review-draft.md     ← /review-draft <file> — adversarial review loop
│   │
│   └── agents/                 ← Specialist sub-agent definitions (9 total)
│       ├── orchestrator.md     ← Coordinates pipeline stages
│       ├── literature-scout.md ← Searches ArXiv + Semantic Scholar
│       ├── synthesis-analyst.md← Synthesizes papers into narrative
│       ├── gap-finder.md       ← Identifies research gaps
│       ├── hypothesis-generator.md ← Proposes novel research ideas
│       ├── geo-specialist.md   ← Injects geo/RS domain knowledge
│       ├── paper-writer.md     ← Writes paper sections (generator)
│       ├── peer-reviewer.md    ← Scores sections independently (evaluator)
│       └── citation-manager.md ← APA 7th edition citation formatting
│
├── skills/                     ← Skill logic: Markdown workflow files (13 + knowledge/)
│   ├── research-pipeline/SKILL.md  ← 4-stage master pipeline (evening→overnight→morning)
│   ├── geo-lit-review/SKILL.md     ← Search + synthesize + gap analysis
│   ├── idea-discovery/SKILL.md     ← Generate + score 6-10 candidate ideas
│   ├── novelty-check/SKILL.md      ← Verify idea is genuinely new
│   ├── geo-experiment/SKILL.md     ← Design + execute OLS/GWR/MGWR experiments
│   ├── spatial-analysis/SKILL.md   ← Interpret spatial results, compute Moran's I
│   ├── result-to-claim/SKILL.md    ← Validate claims vs actual results (safety gate)
│   ├── auto-review-loop/SKILL.md   ← Adversarial review (4 rounds, per-criterion floors)
│   ├── paper-plan/SKILL.md         ← Build section outline + figure plan
│   ├── paper-write/SKILL.md        ← Write sections with autoresearch scoring loop
│   ├── paper-figure/SKILL.md       ← Generate spatial figures + captions
│   ├── training-check/SKILL.md     ← Monitor running experiments
│   ├── submit-check/SKILL.md       ← Validate manuscript vs journal requirements
│   └── knowledge/                  ← Domain reference (read by skills, not invoked)
│       ├── academic-writing.md
│       ├── apa-citations.md
│       ├── spatial-methods.md
│       ├── geoai-domain.md
│       ├── disaster-resilience.md
│       ├── environmental-health.md
│       ├── literature-mining.md
│       └── research-iteration.md
│
├── core/                       ← Core orchestration engine (API backend)
│   ├── orchestrator.py         ← Main entry point: runs the full research loop
│   ├── research_loop.py        ← Iterative idea → experiment → write → review cycle
│   ├── paper_generator.py      ← LaTeX/Markdown paper assembly and section writing
│   ├── code_executor.py        ← Sandboxed code execution manager
│   ├── literature_manager.py   ← ArXiv/Semantic Scholar search & cache
│   ├── memory_manager.py       ← Three-layer memory (working/session/long-term)
│   ├── token_optimizer.py      ← 8-technique token cost reduction
│   └── config.py               ← Pydantic settings & YAML config loader
│
├── harness/                    ← Claude Code harness (hooks + prompts)
│   ├── hooks/
│   │   ├── pre_tool_use.sh     ← Validates tool calls before execution; blocks dangerous ops
│   │   ├── post_tool_use.sh    ← Logs tool calls, updates experiment state
│   │   ├── stop_hook.sh        ← On stop: updates MEMORY.md, writes handoff.json
│   │   └── notification.sh     ← Desktop/Slack/email notifications
│   └── prompts/
│       ├── system_geo.md       ← System prompt: geo-domain expert persona
│       ├── literature_review.md
│       ├── experiment_design.md
│       ├── paper_writing.md
│       ├── peer_review.md
│       └── codex_task.md       ← Prompt template for Codex coding workers
│
├── tools/                      ← Standalone Python CLI utilities (called by skills)
│   ├── arxiv_fetch.py          ← ArXiv Atom API search; --query, --ids, --output
│   └── semantic_scholar_fetch.py ← Semantic Scholar API; priority venue detection
│
├── geo_benchmark/              ← Geospatial regression benchmark suite
│   ├── run_benchmark.py        ← Full OLS/GWR/MGWR comparison run
│   ├── download_data.py        ← Auto-download all open datasets
│   ├── datasets/               ← California Housing, London Prices, Beijing PM2.5, etc.
│   ├── baselines/
│   │   ├── ols_baseline.py     ← OLS via statsmodels (heteroskedasticity-robust SEs)
│   │   ├── gwr_baseline.py     ← GWR via mgwr (max 5,000 obs)
│   │   └── mgwr_baseline.py    ← Multiscale GWR via mgwr (max 3,000 obs)
│   └── evaluation/
│       ├── metrics.py          ← R², RMSE, MAE, Moran's I residuals
│       └── visualize.py        ← Choropleth maps, coefficient maps, residual plots
│
├── configs/                    ← YAML run-mode configurations
│   ├── default.yaml            ← Scoring weights, priority venues, domain keywords
│   ├── full_auto.yaml          ← Overnight autonomous run
│   ├── quick_mode.yaml         ← Fast single-pass draft (~10 min)
│   ├── codex_hybrid.yaml       ← Claude orchestrator + Codex coding workers
│   └── benchmark_only.yaml     ← Benchmark without paper writing
│
├── templates/                  ← Journal-specific paper templates + file format templates
│   ├── geoscience/             ← Nature Geoscience, JGR, GRL, Earth System Sci
│   ├── remote_sensing/         ← RSE, IEEE TGRS, ISPRS, Remote Sensing MDPI
│   ├── giscience/              ← IJGIS, TGIS, AAG, CAGIS, Env & Planning B
│   ├── RESEARCH_CONTRACT_TEMPLATE.md
│   ├── EXPERIMENT_PLAN_TEMPLATE.md
│   ├── EXPERIMENT_LOG_TEMPLATE.md
│   ├── FINDINGS_TEMPLATE.md
│   ├── IDEA_CANDIDATES_TEMPLATE.md
│   ├── PAPER_PLAN_TEMPLATE.md
│   ├── REVIEW_STATE_TEMPLATE.json
│   └── HANDOFF_TEMPLATE.json
│
├── mcp/                        ← MCP server implementations
│   ├── geo_mcp_server.py       ← Spatial data: GADM, OSM, GEE, Census, CRS utilities
│   └── README_MCP.md
│
├── memory/                     ← Persistent session memory
│   ├── MEMORY.md               ← Session state, scores, token usage (updated by stop hook)
│   ├── paper-cache/            ← Retrieved paper JSON files (from arxiv/scholar)
│   ├── synthesis-*.md          ← Literature synthesis documents
│   ├── gap-analysis.md         ← Ranked research gaps
│   ├── approved_claims.md      ← Verified claims only (gate before paper-write)
│   ├── hypotheses.md           ← Generated hypothesis candidates
│   └── outline.md              ← Paper outline
│
├── outputs/                    ← All generated outputs
│   ├── AUTO_REVIEW.md          ← Review loop history (all rounds, per-criterion scores)
│   ├── REVIEW_STATE.json       ← Review loop state for recovery
│   ├── papers/                 ← Written section files (per paper slug)
│   ├── figures/                ← Spatial maps, plots, captions.md
│   └── reports/                ← Literature reviews, submit-check reports
│
└── research_architect/         ← Collaborative workspace (add custom scripts/templates)
```

---

## Key Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Skill-first architecture** | `SKILL.md` files encode workflow logic; Python tools are passive CLI utilities called by skills |
| **Generator-evaluator separation** | `paper-writer` agent writes; `peer-reviewer` agent scores independently — never the same context |
| **Sprint contracts** | `geo-experiment` DESIGN mode writes pass/fail criteria per experiment before any code runs |
| **Hard per-criterion floors** | Review accepts only if all 5 dimensions (Novelty/Rigor/Literature/Clarity/Impact) meet their floor |
| **Context-reset handoffs** | `stop_hook.sh` writes `handoff.json` on every session end; next session reads it first |
| **Dual backend** | `launch.py` or `/launcher` offers API mode (autonomous) or Claude Code mode (interactive) |
| **Domain-aware orchestration** | `geo-specialist` agent injects GIS/RS domain knowledge; `skills/knowledge/` provides reference |
| **Reproducible benchmarks** | `geo_benchmark/` provides fixed datasets, baselines (OLS/GWR/MGWR), and metrics |
| **Journal-aligned output** | Templates match exact structure of 12+ target journals |
| **MCP extensibility** | Drop in new MCP servers to add capabilities without modifying core code |

---

## Data Flow

```
User Input
    │
    ▼
launch.py / /launcher
    ├── Backend: API ──────────────────────────────────────────────────┐
    │   └── core/orchestrator.py                                       │
    │       └── core/research_loop.py                                  │
    │           ├── agents/literature_agent.py                         │
    │           ├── agents/experiment_agent.py ── codex_worker.py      │
    │           ├── agents/writing_agent.py                            │
    │           └── agents/review_agent.py                             │
    │                                                                  │
    └── Backend: Claude Code ────────────────────────────────────────  │
        └── /slash-command or SKILL.md                                 │
            │                                                          │
            ├── Stage 1: geo-lit-review skill                          │
            │   ├── tools/arxiv_fetch.py                               │
            │   └── tools/semantic_scholar_fetch.py                    │
            │   → memory/paper-cache/, memory/synthesis-*.md           │
            │                                                          │
            ├── Stage 2: idea-discovery + novelty-check skills         │
            │   → IDEA_REPORT.md → research_contract.md               │
            │                                                          │
            ├── Stage 3: geo-experiment skill                          │
            │   ├── geo_benchmark/run_benchmark.py                     │
            │   ├── geo_benchmark/baselines/ols_baseline.py            │
            │   ├── geo_benchmark/baselines/gwr_baseline.py            │
            │   └── geo_benchmark/baselines/mgwr_baseline.py           │
            │   → EXPERIMENT_LOG.md, geo_benchmark/results/            │
            │   [evaluator: spatial-analysis skill checks PASS/FAIL]   │
            │                                                          │
            ├── Stage 4a: result-to-claim skill (safety gate)          │
            │   → memory/approved_claims.md                            │
            │                                                          │
            ├── Stage 4b: paper-plan skill                             │
            │   → memory/outline.md                                    │
            │                                                          │
            ├── Stage 5: paper-write + paper-figure skills             │
            │   [generator: paper-writer agent]                        │
            │   [evaluator: peer-reviewer agent — separate context]    │
            │   [scoring: Novelty≥6.5, Rigor≥7.0, Lit≥6.5,           │
            │    Clarity≥6.0, Impact≥6.0; avg≥7.5]                   │
            │   → outputs/papers/<slug>/*.md                           │
            │   → outputs/figures/                                     │
            │                                                          │
            ├── Stage 6: auto-review-loop skill (up to 4 rounds)       │
            │   → outputs/AUTO_REVIEW.md                               │
            │   → outputs/REVIEW_STATE.json                            │
            │                                                          │
            └── Stage 7: submit-check skill                            │
                → outputs/reports/submit_check_<journal>_*.md  ←──────┘
                    │
                    ▼
              Final Paper Ready
```

---

## Agent Roles

| Agent | Role | Separation |
|---|---|---|
| `orchestrator` | Coordinates stage sequencing | — |
| `literature-scout` | Searches ArXiv + Semantic Scholar | — |
| `synthesis-analyst` | Synthesizes papers into narrative gaps | — |
| `gap-finder` | Ranks research gaps from synthesis | — |
| `hypothesis-generator` | Proposes and scores research ideas | Generator |
| `geo-specialist` | Injects GIS/RS domain knowledge | — |
| `paper-writer` | Writes paper sections | **Generator** |
| `peer-reviewer` | Scores sections independently | **Evaluator** |
| `citation-manager` | APA 7th edition citation formatting | — |

---

## Skill → Tool Call Map

| Skill | Python Tool Called |
|---|---|
| `geo-lit-review` | `tools/arxiv_fetch.py`, `tools/semantic_scholar_fetch.py` |
| `geo-experiment` | `geo_benchmark/run_benchmark.py`, `baselines/*.py` |
| `spatial-analysis` | `geo_benchmark/evaluation/metrics.py` |
| `paper-figure` | `geo_benchmark/evaluation/visualize.py` |
| `submit-check` | Reads paper files + journal templates |
| All others | File reads/writes only (no Python subprocess) |

---

## Harness Engineering

Hooks are configured in `settings.json` and executed automatically by Claude Code:

| Hook | Trigger | Action |
|---|---|---|
| `PreToolUse` | Before any Bash call | Block `rm -rf`, force push, system dir writes; log intent |
| `PostToolUse` | After Write or Bash | Log tool call; update experiment state |
| `Stop` | Agent session ends | Update `memory/MEMORY.md`; write `handoff.json` for next session |
| `Notification` | Long-running task completes | Desktop/Slack alert |

Context-reset handoff (`handoff.json`) written on every Stop contains: pipeline stage, review loop per-criterion scores, latest experiment metrics, paper section status, and recovery instructions for the next session.

---

## Slash Commands → Skill Routing

| Command | Routes to Skill |
|---|---|
| `/launcher` | Interactive: choose backend, then routes below |
| `/full-pipeline` | `research-pipeline` |
| `/find-gaps <topic>` | `idea-discovery` (calls `geo-lit-review` first) |
| `/lit-review <topic>` | `geo-lit-review` |
| `/geo-search <topic>` | `geo-lit-review` (search only) |
| `/write-section <name>` | `paper-write` |
| `/review-draft <file>` | `auto-review-loop` |

---

## Agent Modes

| Mode | Description | Entry point |
|---|---|---|
| `quick` | Single-pass draft (~10 min) | `python launch.py --mode quick` |
| `full-auto` | Overnight autonomous run | `python launch.py --mode full-auto` |
| `codex-hybrid` | Claude orchestrates, Codex runs coding tasks | `python launch.py --mode codex-hybrid` |
| `benchmark-only` | Benchmark without writing paper | `python launch.py --mode benchmark-only` |
| `claude-code` | Interactive skill-driven session | Open folder in Claude Code, use `/launcher` |
