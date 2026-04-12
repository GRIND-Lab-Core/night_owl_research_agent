# NORA (Night Owl Research Agent)

> A fully automatic, domain-aware AI research agent for Geoscientists, Remote Sensing researchers, and GIScientists.

---

## What It Does

NORA automates the complete academic research lifecycle using **Claude Code skills** — Markdown-defined workflows that Claude reads and executes, selecting appropriate tools and methods based on context.

1. **Literature review** — searches ArXiv, Semantic Scholar, Google Scholar, Zotero, and Obsidian for relevant papers; synthesizes findings and identifies research gaps
2. **Idea discovery** — generates 8-12 research ideas from literature gaps, validates novelty via multi-source search, and pilot-tests top candidates
3. **Method refinement** — iteratively refines vague research directions into problem-anchored, implementation-ready proposals via adversarial review
4. **Experiment design & execution** — produces claim-driven experiment roadmaps and deploys to local, remote SSH, or Modal serverless GPU
5. **Data acquisition** — discovers, evaluates, downloads, validates, and documents datasets from government portals, APIs, cloud archives, and open repositories
6. **Spatial analysis** — guideline-driven spatial analysis: classifies analytical objectives, provides decision frameworks for method selection, and adapts to available data
7. **Paper writing** — drafts full academic papers using journal-specific templates (IJGIS, IEEE TGRS, GRL, RSE, and more) with iterative scoring loops
8. **Adversarial review** — up to 4 rounds of generator-evaluator-separated review with per-criterion hard floors

---

## Quick Start

### Prerequisites

- Claude Code CLI (`npm install -g @anthropic-ai/claude-code`) or Claude Code desktop/web app
- Anthropic API key (for API-based tools like ArXiv/Semantic Scholar search)

### Getting Started

Open this folder in Claude Code and use the interactive launcher:

```
/launcher
```

The launcher walks you through choosing a task and routes to the correct skill automatically.

Or invoke skills directly:

```
/full-pipeline "topic"                      — end-to-end: idea discovery → experiments → review → paper
/find-gaps "soundscape urban imagery"       — discover and score research ideas
/lit-review "GWR urban heat island"         — full literature review pipeline
/geo-search "spatial heterogeneity"         — targeted literature search
/refine-research "problem | approach"       — iterative method refinement
/data-download "US census tracts 2020"      — discover, download, validate, and document datasets
/spatial-analysis "research question"       — guideline-driven spatial analysis
/deploy-experiment                          — deploy experiments to local/remote/Modal GPU
/review-draft output/papers/methodology.md — adversarial peer-review loop
/write-section results                      — write one paper section
/submit-check IJGIS                         — validate manuscript against journal requirements
```

---

## Architecture

NORA is a **skills-first** system. All research logic lives in Markdown skill files that Claude reads and executes.

```
User (or /slash command)
    ↓ invokes
Skill (skills/<name>/SKILL.md)  ←── reads domain knowledge from skills/knowledge/
    ↓ Claude decides what to do
CLI tools (tools/arxiv_fetch.py, etc.)  ←── lightweight utilities
    ↓ produce
Output files (reports, figures, paper sections)
    ↓ read by
Next skill in pipeline
```

Skills describe workflow logic in Markdown. Claude reads a skill to understand the workflow, then decides the exact sequence of actions based on context — the skill provides guidelines and decision frameworks, not rigid procedures.

---

## Skills

**19 skills** in `skills/`. Each skill is a self-contained Markdown workflow file.

### Workflow Skills

| Skill | Invoke | What it does |
|---|---|---|
| `full-pipeline` | `/full-pipeline` | 5-stage master pipeline: idea discovery → experiment design → execution → review → report |
| `lit-review` | `/lit-review <topic>` | Search + synthesize + gap analysis (ArXiv, Semantic Scholar, Zotero, Obsidian) |
| `idea-discovery` | `/find-gaps <topic>` | Full idea pipeline: lit-review → generate-idea → novelty-check → research-review → experiment-design |
| `generate-idea` | (called by idea-discovery) | Brainstorm 8-12 ideas, filter, pilot-test top 3, rank |
| `novelty-check` | (called by idea-discovery) | Verify idea is genuinely new via multi-source search |
| `idea-review` | (called by idea-discovery) | External critical review of research ideas |
| `refine-research` | `/refine-research` | Iterative method refinement (up to 5 rounds, score ≥ 9 target) |
| `experiment-design` | `/experiment-design` | Claim-driven experiment roadmap with run order, budget, decision gates |
| `experiment-design-pipeline` | (called by idea-discovery) | One-shot wrapper: refine-research → experiment-design |
| `deploy-experiment` | `/deploy-experiment` | Deploy experiments to local/remote/Modal GPU |
| `data-download` | `/data-download` | Discover, evaluate, download datasets with provenance tracking |
| `spatial-analysis` | `/spatial-analysis` | Guideline-driven spatial analysis: question classification → method selection → diagnostics → interpretation |
| `result-to-claim` | (called before paper-write) | Verify claims against actual results (safety gate) |
| `auto-review-loop` | `/review-draft <file>` | Up to 4 adversarial review rounds with per-criterion floors |
| `paper-plan` | (called before paper-write) | Build section outline + figure plan |
| `paper-write` | `/write-section <name>` | Write section with iterative scoring loop |
| `paper-figure` | `/geo-plot` | Generate spatial figures and captions with cartographic conventions |
| `submit-check` | `/submit-check` | Validate manuscript against journal requirements |
| `training-check` | (called by full-pipeline Stage 3) | Monitor running experiments for stalls/failures |

### Domain Knowledge

Skills read from `skills/knowledge/` for reference material:

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

## Harness Engineering

The agent uses **Claude Code's hook system** for automated lifecycle management. Hooks are configured in `settings.json`.

### Active Hooks

| Hook | When | What It Does |
|------|------|--------------|
| `PreToolUse` | Before Bash/Write | Validates paths, blocks dangerous commands, logs intent |
| `PostToolUse` | After tool execution | Updates state, caches results |
| `Stop` | Agent session ends | Saves checkpoint, generates summary, sends notification |
| `Notification` | Long tasks finish | Desktop alert via `notify-send` or macOS `osascript` |

---

## Autoresearch Scoring Loop

Every paper section uses this loop:

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

**The writer does NOT score its own work.** Always uses `peer-reviewer` as evaluator.

| Dimension | Weight | Hard floor |
|---|---|---|
| Novelty | 30% | ≥ 6.5 |
| Rigor | 25% | ≥ 7.0 |
| Literature coverage | 20% | ≥ 6.5 |
| Clarity | 15% | ≥ 6.0 |
| Impact | 10% | ≥ 6.0 |

Accept requires: weighted avg ≥ 7.5 AND all five floors met.

---

## Journal Templates

Templates enforce correct structure, section ordering, word limits, and formatting for each target journal.

### Geoscience

| Journal | Template |
|---------|----------|
| Nature Geoscience | `templates/geoscience/nature_geoscience.md` |
| JGR: Solid Earth | `templates/geoscience/jgr_solid_earth.md` |
| Geophysical Research Letters | `templates/geoscience/grl_template.md` |
| Earth System Science Data | `templates/geoscience/earth_system_sci.md` |

### Remote Sensing

| Journal | Template |
|---------|----------|
| Remote Sensing of Environment | `templates/remote_sensing/remote_sensing_env.md` |
| IEEE TGRS | `templates/remote_sensing/ieee_tgrs.md` |
| ISPRS JPRS | `templates/remote_sensing/isprs_jprs.md` |
| Remote Sensing (MDPI) | `templates/remote_sensing/rs_mdpi.md` |

### GIScience

| Journal | Template |
|---------|----------|
| IJGIS | `templates/giscience/ijgis.md` |
| Transactions in GIS | `templates/giscience/transactions_gis.md` |
| Annals of AAG | `templates/giscience/annals_aag.md` |
| Cartography & GIS | `templates/giscience/cagis.md` |
| Environment & Planning B | `templates/giscience/epb_template.md` |

---

## MCP Servers

MCP (Model Context Protocol) servers extend the agent's capabilities. Configured in `.mcp.json`.

| Server | Purpose |
|--------|---------|
| `filesystem` | Read/write local files and datasets |
| `fetch` | Fetch web content (papers, data portals) |
| `geo_mcp_server` | Spatial data access: GADM, OSM, Census |
| `arxiv_mcp` | ArXiv search, paper fetch, abstract parsing |

---

## Key Output Files

| File | Location | Written by |
|---|---|---|
| Review loop history | `output/AUTO_REVIEW.md` | `auto-review-loop` skill |
| Review loop state | `output/REVIEW_STATE.json` | `auto-review-loop` skill |
| Paper sections | `output/papers/<slug>/` | `paper-write` skill |
| Figures | `output/figures/` | `paper-figure` skill |
| Session handoff | `handoff.json` | Stop hook (on session end) |
| Experiment record | `output/EXPERIMENT_LOG.md` | `deploy-experiment` skill |
| Discovery log | `output/FINDINGS.md` | All skills (append-only) |
| Approved claims | `memory/APPROVED_CLAIMS.md` | `result-to-claim` skill |
| Ranked idea candidates | `output/IDEA_REPORT.md` | `idea-discovery` skill |
| Experiment plan | `output/EXPERIMENT_PLAN.md` | `experiment-design` skill |
| Data provenance log | `data/DATA_MANIFEST.md` | `data-download` skill |
| Spatial analysis report | `output/spatial-analysis/analysis_report.md` | `spatial-analysis` skill |
| Submission check report | `output/reports/submit_check_*.md` | `submit-check` skill |

---

## Project Structure

```
night_owl_research_agent/
├── CLAUDE.md                        ← Dashboard and project conventions
├── README.md                        ← This file
├── settings.json                    ← Claude Code hooks and permissions
│
├── .claude/
│   ├── commands/                    ← Slash commands
│   │   ├── launcher.md              ← /launcher (interactive entry point)
│   │   ├── orchestrate.md           ← /orchestrate
│   │   ├── full-pipeline.md         ← /full-pipeline
│   │   ├── find-gaps.md             ← /find-gaps
│   │   ├── lit-review.md            ← /lit-review
│   │   ├── geo-search.md            ← /geo-search
│   │   ├── write-section.md         ← /write-section
│   │   └── review-draft.md          ← /review-draft
│   │
│   └── agents/                      ← Specialist sub-agent definitions
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
├── skills/                          ← Skill logic: Markdown workflow files (19 skills)
│   ├── full-pipeline/SKILL.md
│   ├── lit-review/SKILL.md
│   ├── idea-discovery/SKILL.md
│   ├── generate-idea/SKILL.md
│   ├── novelty-check/SKILL.md
│   ├── idea-review/SKILL.md
│   ├── refine-research/SKILL.md
│   ├── experiment-design/SKILL.md
│   ├── experiment-design-pipeline/SKILL.md
│   ├── deploy-experiment/SKILL.md
│   ├── data-download/SKILL.md
│   ├── spatial-analysis/SKILL.md
│   ├── result-to-claim/SKILL.md
│   ├── auto-review-loop/SKILL.md
│   ├── paper-plan/SKILL.md
│   ├── paper-write/SKILL.md
│   ├── paper-figure/SKILL.md
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
├── templates/                       ← Journal-specific paper templates
│   ├── geoscience/                  ← Nature Geoscience, JGR, GRL, ESSD
│   ├── remote_sensing/              ← RSE, IEEE TGRS, ISPRS, RS-MDPI
│   └── giscience/                   ← IJGIS, TGIS, AAG, CAGIS
│
├── harness/
│   ├── hooks/                       ← Claude Code lifecycle hooks (shell scripts)
│   │   ├── pre_tool_use.sh
│   │   ├── post_tool_use.sh
│   │   ├── stop_hook.sh
│   │   └── notification.sh
│   └── prompts/
│       └── system_geo.md            ← System prompt template
│
├── mcp/                             ← MCP server implementations
│   └── geo_mcp_server.py
│
├── memory/                          ← Persistent session memory
│   └── MEMORY.md
│
├── output/                          ← All generated outputs
│   ├── AUTO_REVIEW.md
│   ├── REVIEW_STATE.json
│   ├── papers/
│   ├── figures/
│   ├── reports/
│   ├── refine-logs/
│   └── spatial-analysis/
│
├── archived/                        ← Archived earlier versions
└── res/                             ← Resources
```

---

## Contributing

1. Fork this repository
2. Add skills in `skills/<name>/SKILL.md`
3. Add journal templates in `templates/`
4. Add domain knowledge in `skills/knowledge/`

---

## License

MIT License. See `LICENSE` for details.

---

## Citation

If you use NORA in your research, please cite:

```bibtex
@software{nora,
  title  = {NORA: Autonomous AI Research Agent for Geoscientists},
  year   = {2026},
  url    = {https://github.com/your-org/nora}
}
```
