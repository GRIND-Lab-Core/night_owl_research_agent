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
EXTERNAL_REVIEW: false    # true = use claude subagent or external reviewer LLM for adversarial review
```

---

## Backend Choice

| Mode | How to start | API key needed? | Best for |
|---|---|---|---|
| **Anthropic API** | `python launch.py --backend api` | Yes — `ANTHROPIC_API_KEY` | Overnight autonomous runs |
| **Claude Code subscription** | Open in Claude Code / `/launcher` | No | Interactive research sessions |

---

## Session Start Checklist

1. Read `handoff.json` — fastest way to recover current stage, last action, and what to do next
2. Read `memory/MEMORY.md` for pipeline stage and token usage
3. Read `research_contract.md` for active idea (or `program.md` if not yet committed)
4. If COMPACT_MODE: read `findings.md` instead of full experiment logs
5. If resuming review loop: read `outputs/REVIEW_STATE.json` for current round and per-criterion scores
6. Confirm stage with user before taking any action

**`handoff.json` fields to act on immediately:**
- `pipeline.next_step` — the one thing to do first
- `recovery.human_checkpoint_needed` — if true, pause and show user before proceeding
- `review_state.pending_fixes` — implements these before resuming the review loop
- `recovery.resume_skill` — the skill to invoke to resume

---

## Key Files

| File | Purpose | Updated by |
|---|---|---|
| `research_contract.md` | Active idea: problem, method, success criteria | You (after idea-discovery) |
| `program.md` | Full research brief (12 sections) | Researcher |
| `findings.md` | Compact one-line discoveries log | All skills (append) |
| `EXPERIMENT_LOG.md` | Complete experiment record | skill `geo-experiment` |
| `outputs/AUTO_REVIEW.md` | All review rounds with scores | skill `auto-review-loop` |
| `outputs/REVIEW_STATE.json` | Review loop state (per-criterion scores) | skill `auto-review-loop` |
| `handoff.json` | Structured context-reset handoff (written on Stop) | stop hook |
| `memory/MEMORY.md` | Session state, scores, token usage | Stop hook |
| `memory/paper-cache/` | Retrieved paper JSON files | skill `geo-lit-review` |
| `memory/synthesis-*.md` | Literature synthesis | skill `geo-lit-review` |
| `memory/gap-analysis.md` | Ranked research gaps | skill `geo-lit-review` |
| `memory/approved_claims.md` | Verified claims only (never fabricate) | skill `result-to-claim` |
| `IDEA_REPORT.md` | Ranked idea candidates with pilot scores | skill `idea-discovery` |
| `EXPERIMENT_PLAN.md` | Experiment design with commands | skill `geo-experiment` |
| `data/DATA_MANIFEST.md` | Downloaded dataset provenance log | skill `data-download` |
| `data/raw/` | Raw downloaded datasets (never modified) | skill `data-download` |
| `spatial-analysis-outputs/` | Spatial analysis reports, figures, scripts | skill `spatial-analysis` |
| `outputs/papers/` | Written section files | skill `paper-write` |
| `outputs/figures/` | All generated figures | skill `paper-figure` |
| `geo_benchmark/results/` | OLS/GWR/MGWR result JSONs | geo-experiment / python tools |

---

## How Skills Work

**Skills describe workflow logic in Markdown. Python files are tools that skills call.**

- Claude reads a skill (`skills/<name>/SKILL.md`) to understand the workflow
- The skill tells Claude *when* and *which* Python tools to run
- Claude decides the exact sequence based on context
- Python files in `geo_benchmark/`, `tools/`, and `core/` are callable tools — they do not call Claude

```
You (or /slash command)
    ↓ invokes
Skill SKILL.md  ←─── reads domain knowledge from skills/knowledge/
    ↓ decides to call
Python tools (geo_benchmark/run_benchmark.py, tools/arxiv_fetch.py, etc.)
    ↓ produce
Output files (results JSON, paper-cache, figures)
    ↓ read by
Next skill in pipeline
```

---

## Workflow Skills (invoke by name or /slash-command)

| Skill | Invoke | What it does |
|---|---|---|
| `full-pipeline` | `/full-pipeline` | 5-stage master pipeline: idea discovery → experiment design → execution → review → report |
| `lit-review` | `/lit-review <topic>` | Search + synthesize + gap analysis (ArXiv, Semantic Scholar, local papers, Zotero, Obsidian) |
| `idea-discovery` | `/find-gaps <topic>` | Full idea pipeline: lit-review → generate-idea → novelty-check → research-review → experiment-design-pipeline |
| `generate-idea` | (called by idea-discovery) | Brainstorm 8-12 ideas, filter, pilot-test top 3, rank |
| `novelty-check` | (called by idea-discovery) | Verify idea is genuinely new via multi-source search + GPT-5.4 |
| `idea-review` | (called by idea-discovery) | External critical review of research ideas via Codex MCP |
| `refine-research` | `/refine-research` | Iterative method refinement via GPT-5.4 review (up to 5 rounds, score ≥ 9 target) |
| `experiment-design` | `/experiment-design` | Claim-driven experiment roadmap with run order, budget, decision gates |
| `experiment-design-pipeline` | (called by idea-discovery) | One-shot wrapper: refine-research → experiment-design |
| `deploy-experiment` | `/deploy-experiment` | Deploy experiments to local/remote/Modal GPU |
| `data-download` | `/data-download` | Discover, evaluate, download datasets from the internet with provenance tracking |
| `spatial-analysis` | `/spatial-analysis` | Research-question-driven spatial analysis: question classification → ESDA → method selection → diagnostics → interpretation |
| `result-to-claim` | (called before paper-write) | Verify claims against actual results (safety gate) |
| `auto-review-loop` | `/review-draft <file>` | Up to 4 adversarial review rounds with per-criterion floors |
| `paper-plan` | (called before paper-write) | Build section outline + figure plan |
| `paper-write` | `/write-section <name>` | Write section with iterative scoring loop |
| `paper-figure` | `/geo-plot` | Generate spatial figures and captions with cartographic conventions |
| `submit-check` | `/submit-check` | Validate manuscript against journal requirements |
| `training-check` | (called by full-pipeline Stage 3) | Monitor running experiments for stalls/failures |

Skills live in `skills/<name>/SKILL.md`. Domain knowledge lives in `skills/knowledge/`.

---

## Python Tools (called by skills, not directly by you)

| Tool | Path | When skills call it |
|---|---|---|
| ArXiv search | `tools/arxiv_fetch.py` | geo-lit-review, novelty-check |
| Semantic Scholar search | `tools/semantic_scholar_fetch.py` | geo-lit-review, novelty-check |
| Full benchmark | `geo_benchmark/run_benchmark.py` | geo-experiment |
| OLS baseline | `geo_benchmark/baselines/ols_baseline.py` | geo-experiment |
| GWR baseline | `geo_benchmark/baselines/gwr_baseline.py` | geo-experiment |
| MGWR baseline | `geo_benchmark/baselines/mgwr_baseline.py` | geo-experiment |
| Download datasets | `geo_benchmark/download_data.py` | geo-experiment (if data missing) |
| Visualize results | `geo_benchmark/evaluation/visualize.py` | paper-figure |
| Evaluate metrics | `geo_benchmark/evaluation/metrics.py` | spatial-analysis |
| Orchestrator (API mode) | `core/orchestrator.py` | launch.py (API backend only) |
| Memory manager | `core/memory_manager.py` | core/research_loop.py |
| Token optimizer | `core/token_optimizer.py` | core/research_loop.py |

---

## Autoresearch Scoring Loop

Every paper section uses this loop. Never skip it.

```
paper-writer writes draft
    ↓
peer-reviewer scores it (separate context — generator-evaluator separation)
    ↓
All 5 dimension floors met AND weighted avg ≥ 7.5? → ACCEPT
    ↓ (else)
paper-writer revises (max 3 attempts total)
    ↓
If still not accepted after 3 attempts → flag for human review
```

**The writer does NOT score its own work.** Always use `peer-reviewer` as evaluator.

Scoring dimensions and hard floors (`configs/default.yaml` + `auto-review-loop/SKILL.md`):

| Dimension | Weight | Hard floor | What to check |
|---|---|---|---|
| Novelty | 30% | ≥ 6.5 | Decided by model |
| Rigor | 25% | ≥ 7.0 | Decided by model |
| Literature coverage | 20% | ≥ 6.5 | ≥ 15 citations, majority ≥ 2020, includes key GeoAI/soundscape papers |
| Clarity | 15% | ≥ 6.0 | Decided by model |
| Impact | 10% | ≥ 6.0 | Practical application or scientific significance stated |

Accept requires: weighted avg ≥ 7.5 AND all five floors met (failing one floor = reject, regardless of average).

---


## Allowed Behaviors

- Read/write in `output/`, `outputs/`, `geo_benchmark/`, `memory/`, `tools/`, `skills/`
- Call Python tools listed above when skills require them
- Git commit accepted sections: `feat: accept <section> — score <X.X>`
- Append to `findings.md`, `EXPERIMENT_LOG.md`, `outputs/AUTO_REVIEW.md`

## Prohibited Behaviors

- Do NOT fabricate results, citations, or claims not in `memory/approved_claims.md`
- Do NOT execute Python files directly without a skill invoking them
- Do NOT delete `findings.md`, `EXPERIMENT_LOG.md`, or `outputs/AUTO_REVIEW.md` entries
- Do NOT push to remote without explicit user instruction
- Do NOT run `rm -rf` or destructive shell commands
- Do NOT skip `result-to-claim` before `paper-write`
- Do NOT self-score your own written sections — always use `peer-reviewer` as evaluator
- Do NOT proceed to paper writing if any experiment result is FAILED in `EXPERIMENT_LOG.md` and that result is claimed in the paper
- Do NOT silently lower experiment pass/fail criteria mid-execution — write `CONTRACT_VIOLATION.md` instead

---

## Context-Reset Protocol

Context overflow is handled by structured handoffs, not compaction. Compaction causes "context anxiety" — models prematurely wrap work as context fills, producing shallow outputs.

### On Session End (automated)
The Stop hook writes `handoff.json` with:
- Current pipeline stage and next step
- Review loop state (round, per-criterion scores, pending fixes)
- Latest experiment results (compact — just key metrics)
- Paper draft state (accepted/pending sections)
- Recovery hints (what to read, which skill to resume, whether human review is needed)

### On Session Start (you must do this)
1. Read `handoff.json` — it tells you exactly where you are and what to do next
2. Read only the files listed in `handoff.recovery.read_first`
3. Do NOT re-read all experiment logs unless `handoff.recovery.read_first` specifically lists them

### Mid-Session Context Reset (when context is nearly full)
If you notice context is getting large and you still have work to do:
1. Write current state to `findings.md` (one-line summary of what was just learned)
2. Append current experiment results to `EXPERIMENT_LOG.md`
3. Update `outputs/REVIEW_STATE.json` with current scores and pending fixes
4. Tell the user: "Context is getting large — I recommend starting a new session. `handoff.json` will be updated on stop."
5. Do NOT continue trying to squeeze more work into an overfull context

### What to Resume vs Re-run
- **Never re-run** experiments marked SUCCESS in `EXPERIMENT_LOG.md`
- **Never re-run** sections marked ACCEPTED in `outputs/REVIEW_STATE.json` or `memory/MEMORY.md`
- **Always resume** from the stage listed in `handoff.pipeline.stage`
- If in doubt, check `findings.md` — it is the authoritative compact log of all discoveries

---

## Generator-Evaluator Separation

The entity that writes content does NOT score it. This is enforced everywhere:

| Stage | Generator | Evaluator |
|---|---|---|
| Paper sections | `paper-writer` agent | `peer-reviewer` agent (separate context) |
| Experiment results | `geo-experiment` / `deploy-experiment` skill | `spatial-analysis` skill |
| Claims validation | `geo-experiment` + `paper-writer` | `result-to-claim` skill |
| Review rounds | previous writer context | `auto-review-loop` → `peer-reviewer` (no writer context) |

If you find yourself both writing and scoring in the same context window, stop and re-invoke the evaluator skill in a fresh invocation.

---

## Harness Stress-Test Checklist

Re-examine these assumptions periodically — as models improve, some harness scaffolding becomes unnecessary overhead:

| Component | Assumption it encodes | Still needed? |
|---|---|---|
| `result-to-claim` gate | Models fabricate results if not checked | Check every 3 months |
| 3-attempt write loop | Models rarely hit 7.5 on first draft | Check if first-draft scores are rising |
| Generator-evaluator split | Models can't evaluate their own work objectively | Check if self-scores correlate with external review |
| Max 4 review rounds | Beyond 4 rounds, returns diminish | Check if rounds 3-4 are improving scores |
| Structured handoff.json | Models lose context across sessions | Check if native memory improves this |
| Hard per-criterion floors | Weighted average hides weak dimensions | Revisit thresholds annually |

---

## Recovery from Context Overflow

If context overflows mid-session:
1. Read `handoff.json` for current stage and next step (fastest recovery)
2. Read `outputs/REVIEW_STATE.json` for review loop per-criterion state
3. Read `memory/MEMORY.md` for pipeline overview
4. Read `findings.md` (COMPACT_MODE) or `EXPERIMENT_LOG.md` (full)
5. Resume from last incomplete stage — never re-run completed stages

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
├── launch.py                        ← START HERE (choose backend)
├── program.md                       ← EDIT: full research brief (12 sections)
├── research_contract.md             ← Active idea context (condensed)
├── findings.md                      ← Compact one-line discovery log (append-only)
├── EXPERIMENT_LOG.md                ← Complete experiment record (append-only)
├── handoff.json                     ← Context-reset handoff (written by stop hook)
├── CLAUDE.md                        ← This file (dashboard)
├── AGENT_STRUCTURE.md               ← Full architecture map
├── README.md                        ← Usage guide and quick-start
├── settings.json                    ← Claude Code hooks, permissions, env vars
├── pyproject.toml / requirements.txt
│
├── .claude/
│   ├── commands/                    ← Slash commands (8 total)
│   │   ├── launcher.md              ← /launcher       — interactive entry point
│   │   ├── orchestrate.md           ← /orchestrate    — launch orchestrator sub-agent
│   │   ├── full-pipeline.md         ← /full-pipeline  — 4-stage autonomous run
│   │   ├── find-gaps.md             ← /find-gaps      — idea discovery from gaps
│   │   ├── lit-review.md            ← /lit-review     — full literature review
│   │   ├── geo-search.md            ← /geo-search     — targeted paper search
│   │   ├── write-section.md         ← /write-section  — write one paper section
│   │   └── review-draft.md          ← /review-draft   — adversarial review loop
│   │
│   └── agents/                      ← Specialist sub-agent definitions (9 total)
│       ├── orchestrator.md          ← Pipeline manager (sequences all stages)
│       ├── literature-scout.md      ← ArXiv + Semantic Scholar search
│       ├── synthesis-analyst.md     ← Synthesises papers into narrative
│       ├── gap-finder.md            ← Identifies and ranks research gaps
│       ├── hypothesis-generator.md  ← Proposes and scores research ideas
│       ├── geo-specialist.md        ← Injects GIS/RS domain knowledge
│       ├── paper-writer.md          ← Writes paper sections (generator)
│       ├── peer-reviewer.md         ← Scores sections independently (evaluator)
│       └── citation-manager.md      ← APA 7th edition citation formatting
│
├── skills/                          ← Skill logic: Markdown workflow files (19 skills)
│   ├── full-pipeline/SKILL.md       ← 5-stage master pipeline (idea → experiment → review → report)
│   ├── lit-review/SKILL.md          ← Literature search + synthesis (ArXiv, S2, Zotero, Obsidian)
│   ├── idea-discovery/SKILL.md      ← Full idea pipeline (lit-review → generate → novelty → review)
│   ├── generate-idea/SKILL.md       ← Brainstorm + filter + pilot-test research ideas
│   ├── novelty-check/SKILL.md       ← Verify idea novelty via multi-source search
│   ├── idea-review/SKILL.md         ← External critical review via Codex MCP
│   ├── refine-research/SKILL.md     ← Iterative method refinement (GPT-5.4, up to 5 rounds)
│   ├── experiment-design/SKILL.md   ← Claim-driven experiment roadmap
│   ├── experiment-design-pipeline/SKILL.md ← One-shot: refine-research → experiment-design
│   ├── deploy-experiment/SKILL.md   ← Deploy to local/remote/Modal GPU
│   ├── data-download/SKILL.md       ← Discover, evaluate, download datasets with provenance
│   ├── spatial-analysis/SKILL.md    ← Research-question-driven spatial analysis workflows
│   ├── result-to-claim/SKILL.md     ← Validate claims vs results (safety gate)
│   ├── auto-review-loop/SKILL.md    ← Adversarial review (4 rounds, per-criterion floors)
│   ├── paper-plan/SKILL.md          ← Section outline + figure plan
│   ├── paper-write/SKILL.md         ← Section writing with iterative scoring
│   ├── paper-figure/SKILL.md        ← Spatial figures + captions
│   ├── submit-check/SKILL.md        ← Validate manuscript vs journal requirements
│   ├── training-check/SKILL.md      ← Monitor running experiments
│   └── knowledge/                   ← Domain reference files (read by skills)
│       ├── academic-writing.md
│       ├── apa-citations.md
│       ├── spatial-methods.md
│       ├── geoai-domain.md
│       ├── disaster-resilience.md
│       ├── environmental-health.md
│       ├── literature-mining.md
│       └── research-iteration.md
│
├── tools/                           ← Python CLI utilities (called by skills)
│   ├── arxiv_fetch.py               ← ArXiv Atom API search
│   └── semantic_scholar_fetch.py    ← Semantic Scholar API search
│
├── geo_benchmark/                   ← Spatial regression benchmark suite
│   ├── run_benchmark.py             ← Full OLS/GWR/MGWR comparison
│   ├── download_data.py             ← Download open datasets
│   ├── baselines/
│   │   ├── ols_baseline.py          ← OLS (statsmodels)
│   │   ├── gwr_baseline.py          ← GWR (mgwr, max 5,000 obs)
│   │   └── mgwr_baseline.py         ← Multiscale GWR (mgwr, max 3,000 obs)
│   ├── datasets/                    ← Downloaded open-source spatial datasets
│   ├── evaluation/
│   │   ├── metrics.py               ← R², RMSE, MAE, Moran's I residuals
│   │   └── visualize.py             ← Choropleth, coefficient, residual maps
│   └── notebooks/
│
├── core/                            ← Core engine (API backend)
│   ├── orchestrator.py              ← Main entry point
│   ├── research_loop.py             ← Iterative research cycle
│   ├── paper_generator.py           ← Paper assembly
│   ├── code_executor.py             ← Sandboxed execution
│   ├── literature_manager.py        ← Literature search + cache
│   ├── memory_manager.py            ← Three-layer memory system
│   ├── token_optimizer.py           ← 8-technique token cost reduction
│   └── config.py                    ← Pydantic settings + YAML loader
│
├── agents/                          ← Python agent implementations (API backend)
│   ├── literature_agent.py
│   ├── experiment_agent.py
│   ├── writing_agent.py
│   ├── review_agent.py
│   ├── geo_specialist.py
│   └── codex_worker.py              ← Optional Codex/GPT coding workers
│
├── harness/
│   ├── hooks/                       ← Claude Code lifecycle hooks
│   │   ├── pre_tool_use.sh          ← Block dangerous ops; log intent
│   │   ├── post_tool_use.sh         ← Log tool calls; update state
│   │   ├── stop_hook.sh             ← Update MEMORY.md; write handoff.json
│   │   └── notification.sh          ← Desktop/Slack alerts
│   └── prompts/                     ← System prompt templates
│       ├── system_geo.md
│       ├── codex_task.md
│       └── ...
│
├── configs/                         ← YAML run-mode configurations
│   ├── default.yaml                 ← Scoring weights, priority venues, keywords
│   ├── full_auto.yaml               ← Overnight autonomous run
│   ├── codex_hybrid.yaml            ← Claude + Codex coding workers
│   └── benchmark_only.yaml          ← Benchmark without paper writing
│
├── templates/                       ← File format templates + journal templates
│   ├── RESEARCH_CONTRACT_TEMPLATE.md
│   ├── EXPERIMENT_PLAN_TEMPLATE.md
│   ├── EXPERIMENT_LOG_TEMPLATE.md
│   ├── FINDINGS_TEMPLATE.md
│   ├── IDEA_CANDIDATES_TEMPLATE.md
│   ├── PAPER_PLAN_TEMPLATE.md
│   ├── REVIEW_STATE_TEMPLATE.json
│   ├── HANDOFF_TEMPLATE.json
│   ├── geoscience/                  ← Nature Geoscience, JGR, GRL, ESSD
│   ├── remote_sensing/              ← RSE, IEEE TGRS, ISPRS, RS-MDPI
│   └── giscience/                   ← IJGIS, TGIS, AAG, CAGIS
│
├── memory/                          ← Persistent session memory
│   ├── MEMORY.md                    ← Session dashboard (updated by stop hook)
│   ├── paper-cache/                 ← Retrieved paper JSONs (git-ignored)
│   └── [generated files]            ← synthesis-*.md, gap-analysis.md, etc. (git-ignored)
│
├── outputs/                         ← All generated outputs
│   ├── AUTO_REVIEW.md               ← Review loop history
│   ├── REVIEW_STATE.json            ← Review loop state (per-criterion scores)
│   ├── papers/                      ← Written sections per paper slug
│   ├── figures/                     ← Spatial maps, plots, captions.md
│   └── reports/                     ← Literature reviews, submit-check reports
│
├── mcp/                             ← MCP server implementations
│   └── geo_mcp_server.py            ← GADM, OSM, GEE, Census, CRS utilities
│
├── tests/                           ← Unit and integration tests
└── research_architect/              ← Collaborative workspace (add custom work here)
```
