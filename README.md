# NORA (Night Owl Research Agent)

> A fully automatic, domain-aware AI research agent for Geoscientists, Remote Sensing researchers, and GIScientists — powered entirely by Claude Code skills.

![NORA Banner](res/NORA_Banner.png)

---

## Quick Start

NORA runs inside **Claude Code**. There is no Python entry point, no server to spin up, and no build step — you just drop the skills into Claude Code's skill directory and invoke the launcher.

### Step 1 — Install Claude Code

Install Claude Code first. Any of the official distributions works:

- **CLI** (recommended):
  ```bash
  npm install -g @anthropic-ai/claude-code
  claude --version
  ```
- **Desktop app** (macOS / Windows): download from <https://claude.com/claude-code>
- **VS Code extension**: install "Claude Code" from the Marketplace
- **Web**: <https://claude.ai/code>

Sign in once with your Anthropic account so Claude Code can reach the API.

### Step 2 — Get NORA onto your machine

```bash
git clone https://github.com/GRIND-Lab-Core/night_owl_research_agent.git
cd night_owl_research_agent
```

### Step 3 — Install the skills into Claude Code

Claude Code looks for skills under `~/.claude/skills/` (user-level, available in every project) or `<project>/.claude/skills/` (project-local). **Copy the entire `skills/` folder from this repo into one of those locations.**

**macOS / Linux (user-level — recommended):**
```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

**Windows PowerShell (user-level):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force .\skills\* "$env:USERPROFILE\.claude\skills\"
```

**Windows bash / Git Bash:**
```bash
mkdir -p "$USERPROFILE/.claude/skills"
cp -R skills/* "$USERPROFILE/.claude/skills/"
```

**Project-local alternative** (skills only visible when Claude Code is opened in this folder):
```bash
mkdir -p .claude/skills
cp -R skills/* .claude/skills/
```

Also copy the launcher slash command so `/launcher` is available:

```bash
# macOS / Linux
mkdir -p ~/.claude/commands
cp .claude/commands/launcher.md ~/.claude/commands/
```
```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\commands" | Out-Null
Copy-Item -Force .\.claude\commands\launcher.md "$env:USERPROFILE\.claude\commands\"
```

Verify the install — open Claude Code and run:

```
/skills
```

You should see the NORA skills (`full-pipeline`, `lit-review`, `idea-discovery-pipeline`, `deploy-experiment`, `paper-draft`, …) listed.

### Step 4 — Start a research session

Open the `night_owl_research_agent` folder in Claude Code (this gives NORA access to `CLAUDE.md`, `RESEARCH_PLAN.md`, `output/`, `memory/`, and `tools/`), then pick one of the two entry points:

**Option A — interactive launcher** (best for first-time users):
```
/launcher
```
The launcher walks you through a short questionnaire — research topic, stage to start from, control flags (`AUTO_PROCEED`, `HUMAN_CHECKPOINT`, `COMPACT_MODE`, `REVIEWER_DIFFICULTY`) — and routes to the correct skill.

**Option B — end-to-end pipeline** (best when you already know what you want to run):
```
Skill: full-pipeline
"Your research direction here, e.g. 'urban soundscape inequality via street-view + audio foundation models'"
```
or, if you prefer a slash-style invocation:
```
/full-pipeline "your research direction"
```
`full-pipeline` chains all four stages:
`idea-discovery-pipeline → deploy-experiment → auto-review-loop → generate-report`
and then hands off to `paper-writing-pipeline` for the manuscript.

**Tip:** for reproducibility, fill in `RESEARCH_PLAN.md` (or `BRIEF.md`) in the project root before launching. When either file is present, skills read it as the authoritative brief and ignore conflicting `$ARGUMENTS`.

### Step 5 — (Optional) Enable extras

- **MCP servers** — edit `.mcp.json` and register with Claude Code (`/mcp` inside the chat) to enable `filesystem`, `fetch`, `arxiv_mcp`, `geo_mcp`, `github`, and `brave_search`. See `mcp/README_MCP.md`.
- **Hooks** — `settings.json` wires `harness/hooks/*.sh` into Claude Code's lifecycle (writes `handoff.json` on session end, validates tool use, sends desktop notifications). On Windows, run the hook scripts via Git Bash or WSL.
- **W&B** — if your experiments use Weights & Biases, run `wandb login` once on the host where `deploy-experiment` will launch training.
- **API keys** — set `ANTHROPIC_API_KEY` (for Claude Code), plus any optional keys you want to use (`SEMANTIC_SCHOLAR_API_KEY`, `GITHUB_TOKEN`, `BRAVE_API_KEY`).

### Prerequisites summary

| Requirement | Why |
|---|---|
| Claude Code (CLI / desktop / web / VS Code) | Runtime for skills |
| Anthropic account + API credit | Powers the agent |
| Python 3.10+ with `pip install arxiv requests` | `tools/arxiv_fetch.py`, `tools/semantic_scholar_fetch.py` |
| Conda env with `geopandas, pysal, libpysal, esda, spreg, mgwr, rasterio, xarray` | Track B (spatial) experiments |
| CUDA GPU (local / remote SSH / Modal) | Track A (deep-learning) experiments — optional |

---

## What It Does

NORA automates the complete academic research lifecycle using **Claude Code skills** — Markdown-defined workflows that Claude reads and executes, selecting appropriate tools and methods based on context.

1. **Literature review** — searches ArXiv, Semantic Scholar, local papers, Zotero, and Obsidian; synthesizes findings and identifies ranked research gaps.
2. **Idea discovery** — generates 8–12 research ideas from literature gaps, validates novelty via multi-source search + external reviewer, and pilot-tests the top candidates. **Pilots run a mandatory local-GPU presence check first** (`nvidia-smi` → CUDA, then MPS, then `none`); when a local GPU is detected, every pilot launches on it instead of silently falling back to CPU or remote.
3. **Method refinement** — iteratively refines vague research directions into problem-anchored, implementation-ready proposals via adversarial review (up to 5 rounds, score ≥ 9 target).
4. **Experiment design & execution** — produces claim-driven experiment roadmaps and deploys to local, remote SSH, or Modal serverless GPU (Track A), or runs spatial/GIScience methods on CPU (Track B), or both for mixed GeoAI. The same mandatory local-GPU check runs at Step 0 of `deploy-experiment` so any ML/DL workload (pilot or full) executes on the local GPU when present.
5. **Data acquisition** — discovers, evaluates, downloads, validates, and documents datasets from government portals, APIs, cloud archives, and open repositories with full provenance.
6. **Spatial analysis** — guideline-driven: classifies the analytical objective, runs ESDA, and **applies geospatial diagnostics conditionally on the research question**. MAUP discussion, GWR/MGWR, residual Moran's I, alternative spatial weights, and spatial CV are triggered only when the claim depends on them; when in doubt the skill pauses for a human checkpoint instead of running heavyweight checks (or skipping reviewer-expected ones) by reflex.
7. **Adversarial review** — up to 4 rounds of generator–evaluator-separated review with per-criterion hard floors; `medium` / `hard` / `nightmare` reviewer modes via Codex MCP, `codex exec`, or a Claude subagent. Domain personas (`giscience`, `remote-sensing`, `spatial-data-science`) apply geo-specific must-checks **only where the paper's claims actually depend on them** instead of penalizing every paper for missing MAUP / GWR discussion.
8. **Report + paper writing** — consolidates every pipeline artifact into `output/NARRATIVE_REPORT.md`, then runs `paper-writing-pipeline` to produce a journal-ready manuscript (Markdown → LaTeX → PDF/DOCX) with journal-specific profiles for IJGIS, IEEE TGRS, ISPRS JPRS, RSE, AAG, TGIS, and more.

---

## Architecture

NORA is a **skills-first** system. All research logic lives in Markdown skill files that Claude reads and executes.

![NORA Architecture](res/nora_architecture.png)

Skills describe workflow logic in Markdown. Claude reads a skill to understand the workflow, then decides the exact sequence of actions based on context — the skill provides guidelines and decision frameworks, not rigid procedures.

```
You (or /launcher)
    ↓ invokes
Skill SKILL.md  ←─── reads domain knowledge from skills/knowledge/
    ↓ Claude decides what to do
CLI tools (tools/arxiv_fetch.py, etc.) + inline Python + MCP servers as needed
    ↓ produce
Output files (reports, paper-cache, figures, manuscript)
    ↓ read by
Next skill in pipeline
```

The single installed slash command is **`/launcher`**. Every other skill is invoked by name (Claude Code's native Skill tool) or by being called internally from another skill.

---

## Skills

**23 workflow skills** in `skills/` plus domain knowledge in `skills/knowledge/`. Each skill is a self-contained Markdown workflow file.

### Workflow Skills

| Skill | What it does |
|---|---|
| `full-pipeline` | Master pipeline: idea discovery → experiment → review → report → paper |
| `lit-review` | Search + synthesize + gap analysis (ArXiv, Semantic Scholar, local papers, Zotero, Obsidian) |
| `idea-discovery-pipeline` | Full idea pipeline: lit-review → generate-idea → novelty-check → idea-review → experiment-design-pipeline |
| `generate-idea` | Brainstorm 8–12 ideas, filter, pilot-test top 3, rank (called by idea-discovery-pipeline) |
| `novelty-check` | Verify idea novelty via multi-source search + external reviewer |
| `idea-review` | External critical review of research ideas (Codex MCP) |
| `refine-research` | Iterative method refinement via external review (up to 5 rounds, score ≥ 9) |
| `experiment-design` | Claim-driven experiment roadmap with run order, budget, decision gates |
| `experiment-design-pipeline` | One-shot wrapper: refine-research → experiment-design |
| `deploy-experiment` | Deploy experiments — mandatory local-GPU check at Step 0, then Track A (GPU ML) and/or Track B (CPU spatial) |
| `data-download` | Discover, evaluate, download datasets with provenance tracking |
| `spatial-analysis` | Research-question-driven spatial analysis: classification → ESDA → method → conditional diagnostics → interpretation, with a human checkpoint before adding or skipping heavyweight spatial checks |
| `auto-review-loop` | Up to 4 adversarial review rounds with per-criterion floors |
| `generate-report` | Consolidate lit-review + idea + experiment + review artifacts into `output/NARRATIVE_REPORT.md` |
| `paper-writing-pipeline` | Orchestrates paper-plan → paper-figure-generate → paper-draft → paper-review-loop → paper-covert |
| `paper-plan` | Build section outline + figure plan (`output/PAPER_PLAN.md`) |
| `paper-figure-generate` | Generate publication-quality figures, maps, diagrams, and captions |
| `paper-draft` | Turn `output/PAPER_PLAN.md` into a journal-quality Markdown manuscript |
| `paper-review-loop` | Reviewer-editor review of the draft manuscript and iterative revision |
| `paper-covert` | Convert final manuscript into venue submission package (modular LaTeX, PDF, DOCX) |
| `submit-check` | Validate manuscript against target-journal requirements |
| `training-check` | Monitor running experiments for stalls/failures |

### Domain Knowledge

| File | Domain |
|---|---|
| `spatial-methods.md` | Spatial statistics, regression, autocorrelation |
| `geoai-domain.md` | GeoAI, spatial deep learning, foundation models |
| `academic-writing.md` | Academic writing conventions |
| `apa-citations.md` | APA 7th edition citation formatting |
| `disaster-resilience.md` | Disaster management, community resilience |
| `environmental-health.md` | Environmental epidemiology, exposure assessment |
| `literature-mining.md` | Literature search and synthesis strategies |
| `research-iteration.md` | Iterative research refinement patterns |

---

## Control Flags

Edit `CLAUDE.md` before starting a long run:

```yaml
AUTO_PROCEED: false       # true = auto-select top idea after discovery; false = wait for approval
HUMAN_CHECKPOINT: true    # true = pause after each review round; false = run autonomously
COMPACT_MODE: false       # true = use output/PROJ_NOTES.md instead of full logs (saves context)
EXTERNAL_REVIEW: false    # true = use Claude subagent / external reviewer LLM
```

`full-pipeline` also accepts `REVIEWER_DIFFICULTY = medium | hard | nightmare` and `ARXIV_DOWNLOAD = true | false`. Overrides can be passed inline, e.g.:

```
/full-pipeline "topic — AUTO_PROCEED: false, difficulty: nightmare"
```

---

## Harness Engineering

Claude Code's hook system automates lifecycle management (configured in `settings.json`):

| Hook | When | What it does |
|---|---|---|
| `PreToolUse` | Before Bash/Write | Validates paths, blocks dangerous commands, logs intent |
| `PostToolUse` | After tool execution | Updates state, caches results |
| `SkillUse` | Before/after each Skill tool call | `harness/hooks/skill_marker.sh` writes per-stage markers feeding `tools/telemetry_stage_marker.py` |
| `Stop` | Agent session ends | Writes `handoff.json`, updates `memory/MEMORY.md`, runs `tools/telemetry_aggregate.py` to emit `output/TELEMETRY.jsonl` and `output/TELEMETRY_STAGES.jsonl`, sends notification |
| `Notification` | Long tasks finish | Desktop alert via `notify-send` / `osascript` |

---

## Autoresearch Scoring Loop

```
paper-draft writes draft
    ↓
paper-review-loop scores it (separate context — generator–evaluator separation)
    ↓
All 5 dimension floors met AND weighted avg ≥ 7.5? → ACCEPT
    ↓ (else)
paper-draft revises (max 3 attempts total)
    ↓
If still not accepted → flag for human review
```

| Dimension | Weight | Hard floor |
|---|---|---|
| Novelty | 30% | ≥ 6.5 |
| Rigor | 25% | ≥ 7.0 |
| Literature coverage | 20% | ≥ 6.5 |
| Clarity | 15% | ≥ 6.0 |
| Impact | 10% | ≥ 6.0 |

Accept requires weighted avg ≥ 7.5 **and** all five floors met.

---

## Journal Templates & Profiles

Templates enforce correct structure, section ordering, word limits, and formatting. `paper-covert` additionally loads a YAML **profile** that drives LaTeX conversion.

### Markdown templates (`templates/`)

| Category | Journals |
|---|---|
| `geoscience/` | Nature Geoscience, Geophysical Research Letters |
| `remote_sensing/` | Remote Sensing of Environment, IEEE TGRS, ISPRS JPRS |
| `giscience/` | IJGIS, Transactions in GIS, Annals of AAG |

### Submission profiles (`skills/paper-covert/profiles/`)

`aag_annals.yaml`, `generic.yaml`, `ieee_tgrs.yaml`, `ijgis.yaml`, `isprs_jprs.yaml`, `rse.yaml`, `tgis.yaml`.

---

## MCP Servers

Declared in `.mcp.json`. Setup notes in `mcp/README_MCP.md`.

| Server | Purpose |
|---|---|
| `filesystem` | Read/write local files and datasets |
| `fetch` | Fetch web content (papers, data portals, journal pages) |
| `geo_mcp` | Spatial data: GADM, OSM Overpass, Census ACS, GEE (`mcp/geo_mcp_server.py`) |
| `arxiv_mcp` | ArXiv search, paper fetch, abstract parsing |
| `github` | GitHub repo reading and code management |
| `brave_search` | Web search for literature, datasets, documentation |

---

## Key Output Files

| File | Written by |
|---|---|
| `output/LIT_REVIEW_REPORT.md` | `lit-review` |
| `output/IDEA_REPORT.md` / `NOVELTY_REPORT.md` / `IDEA_REVIEW_REPORT.md` | `idea-discovery-pipeline` |
| `output/refine-logs/FINAL_PROPOSAL.md` / `REFINE_REPORT.md` | `refine-research` |
| `output/refine-logs/EXPERIMENT_PLAN.md` / `output/EXPERIMENT_TRACKER.md` | `experiment-design` |
| `output/experiment/EXPERIMENT_RESULT.md` / `EXPERIMENT_LOG.md` | `deploy-experiment` |
| `output/experiment/data/` / `figures/` / `scripts/` | `deploy-experiment`, `spatial-analysis` |
| `output/AUTO_REVIEW_REPORT.md` / `REVIEW_STATE.json` / `review-rounds/` | `auto-review-loop` |
| `output/METHOD_DESCRIPTION.md` | `auto-review-loop` |
| `output/NARRATIVE_REPORT.md` | `generate-report` |
| `output/PAPER_PLAN.md` | `paper-plan` |
| `output/figures/` | `paper-figure-generate` |
| `output/manuscript/` | `paper-draft`, `paper-review-loop` |
| `output/papers/` | `paper-covert` |
| `output/reports/submit_check_*.md` | `submit-check` |
| `data/DATA_MANIFEST.md`, `data/raw/` | `data-download` |
| `output/PROJ_NOTES.md` | all skills (append-only, compact log) |
| `output/TELEMETRY.jsonl` (per-session) and `output/TELEMETRY_STAGES.jsonl` (per-skill) | `tools/telemetry_aggregate.py` (run by Stop hook) |
| `output/CONTRACT_VIOLATION.md` | any skill that detects a downgraded success criterion or other contract violation |
| `memory/MEMORY.md`, `handoff.json` | Stop hook |

---

## Project Structure

```
night_owl_research_agent/
├── CLAUDE.md                        ← Dashboard and project conventions
├── README.md                        ← This file
├── design_principle.md              ← Skill-level design principles (export → Excel via tools/)
├── design_principle_agents.md       ← Sub-agent design principles
├── settings.json                    ← Claude Code hooks, permissions, env vars
├── .mcp.json                        ← MCP server declarations
│
├── .claude/
│   ├── commands/
│   │   └── launcher.md              ← /launcher (only installed slash command)
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
├── skills/                          ← 22 workflow skills + knowledge/
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
│   ├── spatial-analysis/SKILL.md
│   ├── auto-review-loop/SKILL.md
│   ├── generate-report/{SKILL.md, templates/}
│   ├── paper-writing-pipeline/SKILL.md
│   ├── paper-plan/SKILL.md
│   ├── paper-figure-generate/{SKILL.md, templates/}
│   ├── paper-draft/{SKILL.md, templates/}
│   ├── paper-review-loop/{SKILL.md, templates/}
│   ├── paper-covert/{SKILL.md, profiles/, templates/}
│   ├── submit-check/SKILL.md
│   ├── training-check/SKILL.md
│   └── knowledge/                   ← Domain reference files
│
├── tools/                           ← CLI utilities (called by skills + harness)
│   ├── arxiv_fetch.py
│   ├── semantic_scholar_fetch.py
│   ├── convert_skills_to_llm_chat.py
│   ├── export_design_principle_table.py        ← exports design_principle.md tables to Excel
│   ├── export_agent_design_principle_table.py  ← exports design_principle_agents.md tables
│   ├── telemetry_stage_marker.py               ← called by skill_marker hook (per-skill timing)
│   └── telemetry_aggregate.py                  ← called by Stop hook (session/stage telemetry)
│
├── configs/
│   └── default.yaml                 ← Scoring weights, domain keywords
│
├── templates/                       ← Project + paper templates
│   ├── EXPERIMENT_LOG_TEMPLATE.md
│   ├── EXPERIMENT_PLAN_TEMPLATE.md
│   ├── FINDINGS_TEMPLATE.md
│   ├── HANDOFF_TEMPLATE.json
│   ├── IDEA_CANDIDATES_TEMPLATE.md
│   ├── PAPER_PLAN_TEMPLATE.md
│   ├── RESEARCH_CONTRACT_TEMPLATE.md
│   ├── RESEARCH_PLAN_TEMPLATE.md
│   ├── REVIEW_STATE_TEMPLATE.json
│   ├── geoscience/ (nature_geoscience, grl_template)
│   ├── remote_sensing/ (ieee_tgrs, isprs_jprs, remote_sensing_env)
│   └── giscience/ (ijgis, transactions_gis, annals_aag)
│
├── harness/
│   ├── hooks/ (pre_tool_use, post_tool_use, skill_marker, stop_hook, notification)
│   └── prompts/system_geo.md
│
├── mcp/                             ← MCP server implementations
│   ├── geo_mcp_server.py
│   └── README_MCP.md
│
├── memory/MEMORY.md                 ← Persistent session memory
│
├── output/                          ← All generated outputs
│   ├── AUTO_REVIEW.md
│   ├── REVIEW_STATE.json
│   ├── ARCHITECTURE_DIAGRAM_PROMPTS.md
│   ├── papers/
│   ├── figures/
│   └── reports/
│
├── res/nora_architecture.png        ← Architecture diagram
│
└── archived/                        ← Retired skills and pre-skill Python modules
```

---

## Contributing

1. Fork this repository.
2. Add skills in `skills/<name>/SKILL.md`.
3. Add journal templates in `templates/` (plus a YAML profile in `skills/paper-covert/profiles/` if needed).
4. Add domain knowledge in `skills/knowledge/`.

---

## License

MIT License. See `LICENSE` for details.

---

## Design Principles

Two living documents describe the rules NORA's skills and sub-agents follow. Treat them as the source of truth when you write or change a skill.

| File | Scope |
|---|---|
| `design_principle.md` | Skill-level principles: anchored problem, smallest adequate mechanism, generator–evaluator separation, conditional geospatial checks, mandatory local-GPU check before any pilot or full experiment, human-checkpoint pattern for synthesis decisions. |
| `design_principle_agents.md` | Sub-agent principles for the 9 specialists in `.claude/agents/` (orchestrator, literature-scout, gap-finder, hypothesis-generator, geo-specialist, paper-writer, peer-reviewer, citation-manager, synthesis-analyst). |

Both files can be exported to Excel for review or workshop use:

```bash
python tools/export_design_principle_table.py
python tools/export_agent_design_principle_table.py
```

---

## Inspired By

NORA's design borrows ideas from several open-source projects. Credit and gratitude to their authors:

- [BZBarrett/superpowers](https://github.com/BZBarrett/superpowers) — skill-pack patterns for extending Claude Code with composable Markdown workflows.
- [BZBarrett/get-shit-done](https://github.com/BZBarrett/get-shit-done) — pragmatic harness patterns for getting long-running agentic work to actually finish.
- [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) — "research while you sleep" autonomous-loop concept that motivated NORA's overnight pipelines, handoff.json recovery, and adversarial review loop.
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — generator–evaluator separation and the per-criterion floors + weighted-average scoring loop adapted into `auto-review-loop` and `paper-review-loop`.

If your project influenced NORA and is missing here, please open an issue and we will add it.

---

## Citation

If you use NORA in your research, please cite the arXiv preprint:

> Zhou, B., Wu, Q., Huang, X., Ning, H., Li, D., & Zhang, Z. (2026). *NORA: Night Owl Research Agent — Autonomous AI Research for Geoscience, Remote Sensing, and GIScience*. arXiv:2605.02092. <https://arxiv.org/abs/2605.02092>

```bibtex
@misc{zhou2026nora,
  title         = {NORA: Night Owl Research Agent --- Autonomous AI Research for Geoscience, Remote Sensing, and GIScience},
  author        = {Zhou, Bing and Wu, Qiusheng and Huang, Xiao and Ning, Huan and Li, Diya and Zhang, Ziyi},
  year          = {2026},
  eprint        = {2605.02092},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2605.02092},
  howpublished  = {\url{https://github.com/GRIND-Lab-Core/night_owl_research_agent}}
}
```
