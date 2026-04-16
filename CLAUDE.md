# NORA — Dashboard

> Read this file at the start of every session. Then read `memory/MEMORY.md`.

---

## Pipeline Status

```
Active idea:     [not set — fill in RESEARCH_PLAN.md]
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
COMPACT_MODE: false       # true = use output/PROJ_NOTES.md instead of full logs (saves context in long runs)
EXTERNAL_REVIEW: false    # true = use claude subagent or external reviewer LLM for adversarial review
```

## Constants
**PAPER_LIBRARY**: `papers/`

---

## Session Start Checklist

1. Read `handoff.json` — fastest way to recover current stage, last action, and what to do next
2. Read `memory/MEMORY.md` for pipeline stage and token usage
3. Read `RESEARCH_PLAN.md` for active idea (or `BRIEF.md` if not yet committed)
4. If COMPACT_MODE: read `output/EXPERIMENT_RESULT.md` instead of full experiment logs
5. If resuming review loop: read `output/REVIEW_STATE.json` for current round and per-criterion scores
6. Confirm stage with user before taking any action

**`handoff.json` fields to act on immediately:**
- `pipeline.next_step` — the one thing to do first
- `recovery.human_checkpoint_needed` — if true, pause and show user before proceeding
- `review_state.pending_fixes` — implement these before resuming the review loop
- `recovery.resume_skill` — the skill to invoke to resume

---

## Key Files

| File | Purpose | Updated by |
|---|---|---|
| `RESEARCH_PLAN.md` | Active idea: problem, method, success criteria | You (after idea-discovery-pipeline) |
| `BRIEF.md` | Full research brief (12 sections), override skill arguments | Researcher |
| `output/PROJ_NOTES.md` | Compact one-line discoveries log | All skills (append) |
| `output/EXPERIMENT_LOG.md` | Complete experiment record | skill `deploy-experiment` |
| `output/AUTO_REVIEW._REPORT.md` | All review rounds with scores | skill `auto-review-loop` / `paper-review-loop` |
| `output/REVIEW_STATE.json` | Review loop state (per-criterion scores) | skill `auto-review-loop` / `paper-review-loop` |
| `handoff.json` | Structured context-reset handoff (written on Stop) | stop hook |
| `memory/MEMORY.md` | Session state, scores, token usage | Stop hook |
| `output/paper-cache/` | Retrieved paper JSON files | skill `lit-review` |
| `output/LIT_REVIEW_REPORT.md` | Consolidated literature review: findings, thematic synthesis, ranked gaps | skill `lit-review` |
| `output/IDEA_REPORT.md` | Ranked idea candidates with pilot scores | skill `idea-discovery-pipeline` |
| `output/EXPERIMENT_PLAN.md` | Experiment design with commands | skill `experiment-design` |
| `output/NARRATIVE_REPORT.md` | Consolidated narrative driving paper pipeline | skill `generate-report` |
| `output/PAPER_PLAN.md` | Section outline + figure plan | skill `paper-plan` |
| `data/DATA_MANIFEST.md` | Downloaded dataset provenance log | skill `data-download` |
| `data/raw/` | Raw downloaded datasets (never modified) | skill `data-download` |
| `data/processed/` | Transformed/cleaned datasets | skill `geodata-operation` |
| `output/metadata-inspect/` | Metadata reports (Markdown + JSON) per inspected dataset | skill `metadata-inspect` |
| `output/geodata-operation/` | Operation logs, scripts, preview maps | skill `geodata-operation` |
| `output/spatial-analysis/` | Spatial analysis reports, figures, scripts | skill `spatial-analysis` |
| `output/manuscript/` | Draft + reviewed manuscript files | skills `paper-draft`, `paper-review-loop` |
| `output/papers/` | Final/submission-ready paper files | skill `paper-covert` |
| `output/figures/` | All generated figures | skill `paper-figure-generate` |
| `output/reports/` | Auxiliary reports | multiple skills |
| `output/ARCHITECTURE_DIAGRAM_PROMPTS.md` | Prompts for generating architecture diagrams | manual / figure tooling |
| `res/nora_architecture.png` | NORA architecture diagram | static asset |

---

## How Skills Work

**Skills describe workflow logic in Markdown. Claude reads a skill, understands the guidelines, and decides the optimal workflow based on context.**

- Claude reads a skill (`skills/<name>/SKILL.md`) to understand the workflow
- The skill provides guidelines, decision frameworks, and guardrails
- Claude decides the exact sequence of actions based on the research question and available data
- CLI utilities in `tools/` are available for literature search tasks

```
You (or /launcher)
    ↓ invokes
Skill SKILL.md  ←─── reads domain knowledge from skills/knowledge/
    ↓ Claude decides what to do
CLI tools (tools/arxiv_fetch.py, etc.) + inline Python as needed
    ↓ produce
Output files (reports, paper-cache, figures)
    ↓ read by
Next skill in pipeline
```

---

## Workflow Skills

Slash commands: the only installed slash command is **`/launcher`** (see `.claude/commands/launcher.md`) — it is the interactive entry point. All other skills are invoked by name via the Skill tool (e.g. `Skill: full-pipeline`) or by being called internally by another skill.

| Skill | What it does |
|---|---|
| `full-pipeline` | Master pipeline: idea discovery → experiment design → execution → review → report → paper |
| `lit-review` | Search + synthesize + gap analysis (ArXiv, Semantic Scholar, local papers, Zotero, Obsidian) |
| `idea-discovery-pipeline` | Full idea pipeline: lit-review → generate-idea → novelty-check → idea-review → experiment-design-pipeline |
| `generate-idea` | Brainstorm 8–12 ideas, filter, pilot-test top 3, rank (called by idea-discovery-pipeline) |
| `novelty-check` | Verify idea is genuinely new via multi-source search + external reviewer (called by idea-discovery-pipeline) |
| `idea-review` | External critical review of research ideas via Codex MCP (called by idea-discovery-pipeline) |
| `refine-research` | Iterative method refinement via external review (up to 5 rounds, score ≥ 9 target) |
| `experiment-design` | Claim-driven experiment roadmap with run order, budget, decision gates |
| `experiment-design-pipeline` | One-shot wrapper: refine-research → experiment-design |
| `deploy-experiment` | Deploy experiments to local / remote / Modal GPU and record results |
| `data-download` | Discover, evaluate, download datasets from the internet with provenance tracking |
| `metadata-inspect` | Full geodata inspection: format detection, CRS assessment, schema, quality flags, suitability report for vector/raster/tabular data |
| `geodata-operation` | Geodata manipulation: spatial join, overlay, buffer, dissolve, reproject, format conversion, raster indices (NDVI/NDWI), zonal stats, mosaic, geocoding |
| `spatial-analysis` | Research-question-driven spatial analysis: question classification → ESDA → method selection → diagnostics → interpretation |
| `auto-review-loop` | Up to 4 adversarial review rounds with per-criterion floors (generic drafts) |
| `generate-report` | Consolidate lit-review + idea + experiment + review artifacts into `output/NARRATIVE_REPORT.md` |
| `paper-writing-pipeline` | Orchestrates paper-plan → paper-figure-generate → paper-draft → paper-review-loop → paper-covert |
| `paper-plan` | Build section outline + figure plan (`output/PAPER_PLAN.md`) |
| `paper-figure-generate` | Generate publication-quality figures, maps, diagrams, and captions from `output/PAPER_PLAN.md` |
| `paper-draft` | Turn `output/PAPER_PLAN.md` into a journal-quality Markdown manuscript (full / partial / skeleton) |
| `paper-review-loop` | Reviewer-editor review of the draft manuscript and iterative revision |
| `paper-covert` | Convert final manuscript into venue submission package (modular LaTeX, PDF, DOCX) |
| `submit-check` | Validate manuscript against target journal requirements |
| `training-check` | Monitor running experiments for stalls/failures |

Skills live in `skills/<name>/SKILL.md`. Domain knowledge lives in `skills/knowledge/`.

---

## CLI Tools (called by skills)

| Tool | Path | When skills call it |
|---|---|---|
| ArXiv search | `tools/arxiv_fetch.py` | lit-review, novelty-check |
| Semantic Scholar search | `tools/semantic_scholar_fetch.py` | lit-review, novelty-check |
| Skill converter | `tools/convert_skills_to_llm_chat.py` | Converting skills to chat format |

---

## Autoresearch Scoring Loop

Every paper section uses this loop. Never skip it.

```
paper-draft writes draft
    ↓
paper-review-loop / peer-reviewer scores it (separate context — generator-evaluator separation)
    ↓
All 5 dimension floors met AND weighted avg ≥ 7.5? → ACCEPT
    ↓ (else)
paper-draft revises (max 3 attempts total)
    ↓
If still not accepted after 3 attempts → flag for human review
```

**The writer does NOT score its own work.** Always use `peer-reviewer` / `paper-review-loop` as evaluator.

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

- Read/write in `output/`, `memory/`, `data/`, `tools/`, `skills/`, `papers/`
- Call CLI tools listed above when skills require them
- Git commit accepted sections: `feat: accept <section> — score <X.X>`
- Append to `output/EXPERIMENT_RESULT.md`, `output/EXPERIMENT_LOG.md`, `output/AUTO_REVIEW._REPORT.md`

## Prohibited Behaviors

- Do NOT execute Python files directly without a skill invoking them
- Do NOT delete `output/EXPERIMENT_RESULT.md`, `output/EXPERIMENT_LOG.md`, or `output/AUTO_REVIEW._REPORT.md` entries
- Do NOT push to remote without explicit user instruction
- Do NOT run `rm -rf` or destructive shell commands
- Do NOT self-score your own written sections — always use `peer-reviewer` / `paper-review-loop` as evaluator
- Do NOT proceed to paper writing if any experiment result is FAILED in `output/EXPERIMENT_LOG.md` and that result is claimed in the paper
- Do NOT silently lower experiment pass/fail criteria mid-execution — write `output/CONTRACT_VIOLATION.md` instead

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
1. Write current state to `output/PROJ_NOTES.md` (one-line summary of what was just learned)
2. Append current experiment results to `output/EXPERIMENT_LOG.md`
3. Update `output/REVIEW_STATE.json` with current scores and pending fixes
4. Tell the user: "Context is getting large — I recommend starting a new session. `handoff.json` will be updated on stop."
5. Do NOT continue trying to squeeze more work into an overfull context

### What to Resume vs Re-run
- **Never re-run** experiments marked SUCCESS in `output/EXPERIMENT_LOG.md`
- **Never re-run** sections marked ACCEPTED in `output/REVIEW_STATE.json` or `memory/MEMORY.md`
- **Always resume** from the stage listed in `handoff.pipeline.stage`
- If in doubt, check `output/PROJ_NOTES.md` — it is the authoritative compact log of all discoveries

---

## Generator-Evaluator Separation

The entity that writes content does NOT score it. This is enforced everywhere:

| Stage | Generator | Evaluator |
|---|---|---|
| Paper sections | `paper-draft` | `paper-review-loop` / `peer-reviewer` (separate context) |
| Experiment results | `deploy-experiment` | `spatial-analysis` |
| Claims validation | `deploy-experiment` + `paper-draft` | 
| Review rounds | previous writer context | `auto-review-loop` / `paper-review-loop` (no writer context) |

If you find yourself both writing and scoring in the same context window, stop and re-invoke the evaluator skill in a fresh invocation.

---

## Harness Stress-Test Checklist

Re-examine these assumptions periodically — as models improve, some harness scaffolding becomes unnecessary overhead:

| Component | Assumption it encodes | Still needed? |
|---|---|---|
| 3-attempt write loop | Models rarely hit 7.5 on first draft | Check if first-draft scores are rising |
| Generator-evaluator split | Models can't evaluate their own work objectively | Check if self-scores correlate with external review |
| Max 4 review rounds | Beyond 4 rounds, returns diminish | Check if rounds 3-4 are improving scores |
| Structured handoff.json | Models lose context across sessions | Check if native memory improves this |
| Hard per-criterion floors | Weighted average hides weak dimensions | Revisit thresholds annually |

---

## Recovery from Context Overflow

If context overflows mid-session:
1. Read `handoff.json` for current stage and next step (fastest recovery)
2. Read `output/REVIEW_STATE.json` for review loop per-criterion state
3. Read `memory/MEMORY.md` for pipeline overview
4. Read `output/PROJ_NOTES.md` (COMPACT_MODE) or `output/EXPERIMENT_LOG.md` (full)
5. Resume from last incomplete stage — never re-run completed stages

---

## MCP Servers (`.mcp.json`)

- `filesystem` — local file system access for the project directory
- `fetch` — web content retrieval (ArXiv, data portals, journal pages)
- `geo_mcp` — spatial data: GADM boundaries, OSM Overpass, Census ACS, GEE access (`mcp/geo_mcp_server.py`)
- `arxiv_mcp` — ArXiv paper search, abstract fetch, citation parsing
- `github` — GitHub repo reading and code management
- `brave_search` — web search for literature, datasets, documentation

See `mcp/README_MCP.md` for setup notes.

---

## Project Layout

```
night_owl_research_agent/
├── CLAUDE.md                        ← This file (dashboard)
├── README.md                        ← Usage guide and quick-start
├── settings.json                    ← Claude Code hooks, permissions, env vars
├── .mcp.json                        ← MCP server declarations
│
├── .claude/
│   ├── commands/                    ← Slash commands
│   │   └── launcher.md              ← /launcher — interactive entry point (only installed slash command)
│   │
│   └── agents/                      ← Specialist sub-agent definitions (9 total)
│       ├── orchestrator.md
│       ├── literature-scout.md
│       ├── synthesis-analyst.md
│       ├── gap-finder.md
│       ├── hypothesis-generator.md
│       ├── geo-specialist.md
│       ├── paper-writer.md
│       ├── peer-reviewer.md
│       └── citation-manager.md
│
├── skills/                          ← Skill logic: Markdown workflow files (24 skills)
│   ├── full-pipeline/SKILL.md
│   ├── lit-review/SKILL.md
│   ├── idea-discovery-pipeline/SKILL.md
│   ├── generate-idea/SKILL.md
│   ├── novelty-check/SKILL.md
│   ├── idea-review/SKILL.md
│   ├── refine-research/SKILL.md
│   ├── experiment-design/SKILL.md
│   ├── experiment-design-pipeline/SKILL.md
│   ├── deploy-experiment/SKILL.md
│   ├── data-download/SKILL.md
│   ├── metadata-inspect/SKILL.md
│   ├── geodata-operation/SKILL.md
│   ├── spatial-analysis/SKILL.md
│   ├── auto-review-loop/SKILL.md
│   ├── generate-report/SKILL.md
│   ├── paper-writing-pipeline/SKILL.md
│   ├── paper-plan/SKILL.md
│   ├── paper-figure-generate/SKILL.md
│   ├── paper-draft/SKILL.md
│   ├── paper-review-loop/SKILL.md
│   ├── paper-covert/SKILL.md
│   ├── submit-check/SKILL.md
│   ├── training-check/SKILL.md
│   └── knowledge/                   ← Domain reference files
│       ├── academic-writing.md
│       ├── apa-citations.md
│       ├── spatial-methods.md
│       ├── geoai-domain.md
│       ├── disaster-resilience.md
│       ├── environmental-health.md
│       ├── literature-mining.md
│       └── research-iteration.md
│
├── tools/                           ← CLI utilities (called by skills)
│   ├── arxiv_fetch.py               ← ArXiv Atom API search
│   ├── semantic_scholar_fetch.py    ← Semantic Scholar API search
│   └── convert_skills_to_llm_chat.py ← Skill-to-chat format converter
│
├── configs/
│   └── default.yaml                 ← Scoring weights, domain keywords, literature settings
│
├── templates/                       ← Project and paper templates
│   ├── EXPERIMENT_LOG_TEMPLATE.md
│   ├── EXPERIMENT_PLAN_TEMPLATE.md
│   ├── FINDINGS_TEMPLATE.md
│   ├── HANDOFF_TEMPLATE.json
│   ├── IDEA_CANDIDATES_TEMPLATE.md
│   ├── PAPER_PLAN_TEMPLATE.md
│   ├── RESEARCH_CONTRACT_TEMPLATE.md
│   ├── RESEARCH_PLAN_TEMPLATE.md
│   ├── REVIEW_STATE_TEMPLATE.json
│   ├── geoscience/                  ← Nature Geoscience, GRL
│   │   ├── nature_geoscience.md
│   │   └── grl_template.md
│   ├── remote_sensing/              ← RSE, IEEE TGRS, ISPRS JPRS
│   │   ├── ieee_tgrs.md
│   │   ├── isprs_jprs.md
│   │   └── remote_sensing_env.md
│   └── giscience/                   ← IJGIS, TGIS, AAG Annals
│       ├── ijgis.md
│       ├── transactions_gis.md
│       └── annals_aag.md
│
├── harness/
│   ├── hooks/                       ← Claude Code lifecycle hooks
│   │   ├── pre_tool_use.sh
│   │   ├── post_tool_use.sh
│   │   ├── stop_hook.sh
│   │   └── notification.sh
│   └── prompts/
│       └── system_geo.md
│
├── mcp/                             ← MCP server implementations
│   ├── geo_mcp_server.py
│   └── README_MCP.md
│
├── memory/                          ← Persistent session memory
│   └── MEMORY.md
│
├── output/                          ← All generated outputs
│   ├── AUTO_REVIEW.md
│   ├── REVIEW_STATE.json
│   ├── ARCHITECTURE_DIAGRAM_PROMPTS.md
│   ├── papers/
│   ├── figures/
│   └── reports/
│
├── res/                             ← Static project assets
│   └── nora_architecture.png
│
└── archived/                        ← Archived earlier versions
    ├── core/                        ← Pre-skill Python orchestrator modules
    ├── skills/                      ← Retired skills (geo-experiment, spatial-analysis)
    ├── paper-draft/
    └── paper-figure/
```
