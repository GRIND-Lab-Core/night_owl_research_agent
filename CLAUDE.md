# GeoResearchAgent-247 — Dashboard

> Read this file at the start of every session. Then read `memory/MEMORY.md`.

---

## Pipeline Status

```
Active idea:     [not set — fill in research_contract.md]
Stage:           not started
Last action:     —
Review score:    —/10
Sections done:   0/7
```

---

## Control Flags

Edit these before starting a long run:

```yaml
AUTO_PROCEED: false       # true = auto-select top idea after discovery; false = wait for user approval
HUMAN_CHECKPOINT: true    # true = pause after each review round; false = run all 4 rounds autonomously
COMPACT_MODE: false       # true = use findings.md instead of full logs (saves context in long runs)
EXTERNAL_REVIEW: false    # true = use MCP claude-review or gemini-review for adversarial review
```

---

## Backend Choice

| Mode | How to start | API key needed? | Best for |
|---|---|---|---|
| **Anthropic API** | `python launch.py --backend api` | Yes — `ANTHROPIC_API_KEY` | Overnight autonomous runs |
| **Claude Code subscription** | Open in Claude Code / `python launch.py --backend claude-code` | No | Interactive research sessions |

---

## Session Start Checklist

1. Read `memory/MEMORY.md` for pipeline stage and token usage
2. Read `research_contract.md` for active idea (or `program.md` if not yet committed)
3. If COMPACT_MODE: read `findings.md` instead of full experiment logs
4. If resuming review loop: read `REVIEW_STATE.json` for current round
5. Confirm stage with user before taking any action

---

## Key Files

| File | Purpose | Updated by |
|---|---|---|
| `research_contract.md` | Active idea: problem, method, success criteria | You (after idea-discovery) |
| `program.md` | Full research brief (12 sections) | Researcher |
| `findings.md` | Compact one-line discoveries log | All skills (append) |
| `EXPERIMENT_LOG.md` | Complete experiment record | skill `geo-experiment` |
| `AUTO_REVIEW.md` | All review rounds with scores | skill `auto-review-loop` |
| `REVIEW_STATE.json` | Review loop state for recovery | skill `auto-review-loop` |
| `memory/MEMORY.md` | Session state, scores, token usage | Stop hook |
| `memory/paper-cache/` | Retrieved paper JSON files | skill `geo-lit-review` |
| `memory/synthesis-*.md` | Literature synthesis | skill `geo-lit-review` |
| `memory/gap-analysis.md` | Ranked research gaps | skill `geo-lit-review` |
| `memory/approved_claims.md` | Verified claims only (never fabricate) | skill `result-to-claim` |
| `IDEA_REPORT.md` | Ranked idea candidates with pilot scores | skill `idea-discovery` |
| `EXPERIMENT_PLAN.md` | Experiment design with commands | skill `geo-experiment` |
| `outputs/papers/` | Written section files | skill `paper-write` |
| `outputs/figures/` | All generated figures | skill `paper-figure` |
| `GeoBenchmark/results/` | OLS/GWR/MGWR result JSONs | geo-experiment / python tools |

---

## How Skills Work

**Skills describe workflow logic in Markdown. Python files are tools that skills call.**

- Claude reads a skill (`skills/<name>/SKILL.md`) to understand the workflow
- The skill tells Claude *when* and *which* Python tools to run
- Claude decides the exact sequence based on context
- Python files in `GeoBenchmark/`, `tools/`, and `core/` are callable tools — they do not call Claude

```
You (or /slash command)
    ↓ invokes
Skill SKILL.md  ←─── reads domain knowledge from skills/knowledge/
    ↓ decides to call
Python tools (GeoBenchmark/run_benchmark.py, tools/arxiv_fetch.py, etc.)
    ↓ produce
Output files (results JSON, paper-cache, figures)
    ↓ read by
Next skill in pipeline
```

---

## Workflow Skills (invoke by name or /slash-command)

| Skill | Invoke | What it does |
|---|---|---|
| `research-pipeline` | `/full-pipeline` | 4-stage master pipeline (evening→overnight→morning) |
| `geo-lit-review` | `/geo-search <topic>` | Search + synthesize + gap analysis |
| `idea-discovery` | `/find-gaps <topic>` | Generate + score candidate ideas from gaps |
| `novelty-check` | (called by idea-discovery) | Verify idea is genuinely new |
| `geo-experiment` | `/run-experiment` | Design + execute OLS/GWR/MGWR experiments |
| `spatial-analysis` | (called by geo-experiment) | Interpret spatial results, compute Moran's I |
| `result-to-claim` | (called before paper-write) | Verify claims against actual results |
| `auto-review-loop` | `/review-draft <file>` | Up to 4 adversarial review rounds |
| `paper-plan` | (called before paper-write) | Build section outline + figure plan |
| `paper-write` | `/write-section <name>` | Write section with autoresearch scoring |
| `paper-figure` | `/geo-plot` | Generate spatial figures and captions |
| `training-check` | (called by research-pipeline Stage 3) | Monitor running experiments |

Skills live in `skills/<name>/SKILL.md`. Domain knowledge lives in `skills/knowledge/`.

---

## Python Tools (called by skills, not directly by you)

| Tool | Path | When skills call it |
|---|---|---|
| ArXiv search | `tools/arxiv_fetch.py` | geo-lit-review, novelty-check |
| Semantic Scholar search | `tools/semantic_scholar_fetch.py` | geo-lit-review, novelty-check |
| Full benchmark | `GeoBenchmark/run_benchmark.py` | geo-experiment |
| OLS baseline | `GeoBenchmark/baselines/ols_baseline.py` | geo-experiment |
| GWR baseline | `GeoBenchmark/baselines/gwr_baseline.py` | geo-experiment |
| MGWR baseline | `GeoBenchmark/baselines/mgwr_baseline.py` | geo-experiment |
| Download datasets | `GeoBenchmark/download_data.py` | geo-experiment (if data missing) |
| Visualize results | `GeoBenchmark/evaluation/visualize.py` | paper-figure |
| Evaluate metrics | `GeoBenchmark/evaluation/metrics.py` | spatial-analysis |
| Orchestrator (API mode) | `core/orchestrator.py` | launch.py (API backend only) |
| Memory manager | `core/memory_manager.py` | core/research_loop.py |
| Token optimizer | `core/token_optimizer.py` | core/research_loop.py |

---

## Autoresearch Scoring Loop

Every paper section uses this loop. Never skip it.

```
Write draft → self-score (0–10) → accept if ≥ 7.5 → else revise → max 3 attempts
```

Scoring dimensions (`configs/default.yaml`):
- **Novelty** 30% — contribution clearly and defensibly stated
- **Rigor** 25% — spatially valid, reproducible, baselines compared
- **Literature coverage** 20% — ≥ 15 citations, majority ≥ 2020, geo venues
- **Clarity** 15% — active voice, specific numbers, no vague claims
- **Impact** 10% — practical or scientific significance

Spatial regression papers additionally require: OLS + GWR + MGWR comparison, Moran's I residuals.

---

## Geo Conventions (always apply)

- State CRS for all spatial data: `WGS84 (EPSG:4326)` or `UTM Zone 10N (EPSG:32610)`
- Never compute distances or areas in WGS84 degrees
- Project to local UTM or equal-area (EPSG:5070 for CONUS) before analysis
- Report Moran's I residuals for every regression model
- Use spatial (not random) cross-validation
- Subsampling limits: GWR ≤ 5,000 obs, MGWR ≤ 3,000 obs

---

## Allowed Behaviors

- Read/write in `output/`, `outputs/`, `GeoBenchmark/`, `memory/`, `tools/`, `skills/`
- Call Python tools listed above when skills require them
- Git commit accepted sections: `feat: accept <section> — score <X.X>`
- Download open-source datasets via `GeoBenchmark/download_data.py`
- Append to `findings.md`, `EXPERIMENT_LOG.md`, `AUTO_REVIEW.md`

## Prohibited Behaviors

- Do NOT fabricate results, citations, or claims not in `memory/approved_claims.md`
- Do NOT execute Python files directly without a skill invoking them
- Do NOT delete `findings.md`, `EXPERIMENT_LOG.md`, or `AUTO_REVIEW.md` entries
- Do NOT push to remote without explicit user instruction
- Do NOT run `rm -rf` or destructive shell commands
- Do NOT skip `result-to-claim` before `paper-write`

---

## Recovery from Context Overflow

If context overflows mid-session:
1. Read `REVIEW_STATE.json` for review loop state
2. Read `memory/MEMORY.md` for pipeline stage
3. Read `findings.md` (COMPACT_MODE) or `EXPERIMENT_LOG.md` (full)
4. Resume from last incomplete stage — never re-run completed stages

---

## MCP Servers (`.mcp.json`)

- `geo_mcp` — spatial data: GADM boundaries, OSM Overpass, Census ACS, CRS utilities
- `arxiv_mcp` — paper search (alternative to `tools/arxiv_fetch.py`)
- `filesystem` — local file access
- `fetch` — web content retrieval
- `claude-review` *(optional)* — external Claude reviewer for adversarial review loop
- `gemini-review` *(optional)* — Gemini reviewer for adversarial review loop

---

## Project Layout

```
geo_research_agent_247/
├── launch.py                    ← START HERE (choose backend)
├── program.md                   ← EDIT: full research brief (12 sections)
├── research_contract.md         ← Active idea context (condensed)
├── findings.md                  ← Compact one-line discovery log
├── EXPERIMENT_LOG.md            ← Complete experiment record
├── AUTO_REVIEW.md               ← Review loop history (created on first review)
├── REVIEW_STATE.json            ← Review loop state for recovery (created on first review)
├── CLAUDE.md                    ← this file (dashboard)
│
├── skills/
│   ├── research-pipeline/SKILL.md   ← 4-stage master pipeline
│   ├── geo-lit-review/SKILL.md      ← literature search + synthesis
│   ├── idea-discovery/SKILL.md      ← ideation from gaps
│   ├── novelty-check/SKILL.md       ← verify idea novelty
│   ├── geo-experiment/SKILL.md      ← design + run experiments
│   ├── spatial-analysis/SKILL.md    ← interpret spatial results
│   ├── result-to-claim/SKILL.md     ← validate claims vs results
│   ├── auto-review-loop/SKILL.md    ← adversarial review (4 rounds)
│   ├── paper-plan/SKILL.md          ← section outline + figure plan
│   ├── paper-write/SKILL.md         ← autoresearch section writing
│   ├── paper-figure/SKILL.md        ← spatial figures + captions
│   ├── training-check/SKILL.md      ← monitor running experiments
│   └── knowledge/                   ← domain reference (read by skills)
│       ├── academic-writing.md
│       ├── apa-citations.md
│       ├── spatial-methods.md
│       ├── geoai-domain.md
│       ├── disaster-resilience.md
│       ├── environmental-health.md
│       ├── literature-mining.md
│       └── research-iteration.md
│
├── tools/                       ← callable Python utilities (called by skills)
│   ├── arxiv_fetch.py
│   └── semantic_scholar_fetch.py
│
├── .claude/
│   ├── agents/                  ← specialist agent definitions (9 agents)
│   └── commands/                ← slash commands (6 commands)
│
├── templates/                   ← standard file format templates
│   ├── RESEARCH_CONTRACT_TEMPLATE.md
│   ├── EXPERIMENT_PLAN_TEMPLATE.md
│   ├── EXPERIMENT_LOG_TEMPLATE.md
│   ├── FINDINGS_TEMPLATE.md
│   ├── IDEA_CANDIDATES_TEMPLATE.md
│   ├── PAPER_PLAN_TEMPLATE.md
│   └── REVIEW_STATE_TEMPLATE.json
│
├── GeoBenchmark/                ← spatial regression benchmark suite
│   ├── run_benchmark.py         ← full OLS/GWR/MGWR comparison
│   ├── baselines/               ← individual baseline implementations
│   ├── datasets/                ← open-source datasets
│   ├── evaluation/              ← metrics + visualize
│   └── download_data.py
│
├── configs/                     ← run mode configurations
│   ├── default.yaml             ← scoring weights, venues, domain keywords
│   ├── full_auto.yaml
│   ├── quick_mode.yaml
│   ├── codex_hybrid.yaml
│   └── benchmark_only.yaml
│
├── agents/                      ← Python agent implementations (API mode)
├── core/                        ← orchestrator, memory, token optimizer
├── harness/hooks/               ← Claude Code lifecycle hooks
├── mcp/                         ← custom MCP server implementations
├── memory/                      ← MEMORY.md + paper-cache
├── outputs/                     ← generated papers, figures, reports
└── ResearchArchitect/           ← collaborative workspace
```
