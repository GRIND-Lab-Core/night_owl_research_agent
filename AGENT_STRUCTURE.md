# GeoResearchAgent-247: Architecture & Structure

## Overview

GeoResearchAgent-247 is a fully autonomous AI-powered research agent designed specifically for **Geoscientists**, **Remote Sensing researchers**, and **GIScientists**. It combines large-language-model orchestration with domain-specific tools, journal templates, spatial benchmarks, and harness engineering to accelerate the full research lifecycle — from literature review through experiment, paper writing, and peer-review simulation.

---

## Directory Structure

```
geo_research_agent_247/
│
├── AGENT_STRUCTURE.md          ← You are here: visual map of the entire system
├── README.md                   ← Full usage guide and quick-start
├── CLAUDE.md                   ← Harness engineering: hooks, permissions, MCP bindings
├── settings.json               ← Claude Code settings (hooks, models, permissions)
├── .mcp.json                   ← MCP server manifest (filesystem, web, arxiv, github)
├── pyproject.toml              ← Python package & dependency declaration
├── requirements.txt            ← Python dependencies
│
├── core/                       ← Core orchestration engine
│   ├── orchestrator.py         ← Main entry point: runs the full research loop
│   ├── research_loop.py        ← Iterative idea → experiment → write → review cycle
│   ├── paper_generator.py      ← LaTeX/Markdown paper assembly and section writing
│   ├── code_executor.py        ← Sandboxed code execution manager
│   ├── literature_manager.py   ← ArXiv/Semantic Scholar search & cache
│   └── config.py               ← Pydantic settings & YAML config loader
│
├── agents/                     ← Specialized sub-agents (Claude-based)
│   ├── literature_agent.py     ← Literature search, summarization, gap analysis
│   ├── experiment_agent.py     ← Hypothesis → design → run → analyze
│   ├── writing_agent.py        ← Section-by-section academic writing
│   ├── review_agent.py         ← Self-critique and simulated peer review
│   ├── codex_worker.py         ← Codex/GPT-4o coding worker integration
│   ├── geo_specialist.py       ← Geo-domain knowledge injection agent
│   └── coordinator.py          ← Multi-agent task distribution and state tracking
│
├── harness/                    ← Harness Engineering (Claude Code hooks + skills)
│   ├── hooks/
│   │   ├── pre_tool_use.sh     ← Validates dangerous tool calls before execution
│   │   ├── post_tool_use.sh    ← Logs tool calls, updates experiment state
│   │   ├── stop_hook.sh        ← On agent stop: save state, generate summary
│   │   └── notification.sh     ← Sends desktop/Slack/email notifications
│   ├── skills/
│   │   ├── geo_search.md       ← /geo-search: domain-aware literature search
│   │   ├── run_experiment.md   ← /run-experiment: execute benchmarks
│   │   ├── write_section.md    ← /write-section: generate paper section
│   │   ├── review_paper.md     ← /review-paper: simulated peer review
│   │   ├── geo_plot.md         ← /geo-plot: generate spatial maps/charts
│   │   └── submit_check.md     ← /submit-check: journal-specific validation
│   └── prompts/
│       ├── system_geo.md       ← System prompt: geo-domain expert persona
│       ├── literature_review.md
│       ├── experiment_design.md
│       ├── paper_writing.md
│       ├── peer_review.md
│       └── codex_task.md       ← Prompt template for delegating to Codex workers
│
├── templates/                  ← Journal-specific paper templates
│   ├── geoscience/
│   │   ├── nature_geoscience.md
│   │   ├── jgr_solid_earth.md
│   │   ├── grl_template.md     ← Geophysical Research Letters
│   │   └── earth_system_sci.md
│   ├── remote_sensing/
│   │   ├── remote_sensing_env.md    ← Remote Sensing of Environment
│   │   ├── ieee_tgrs.md             ← IEEE Trans. on Geoscience & Remote Sensing
│   │   ├── isprs_jprs.md            ← ISPRS Journal
│   │   └── rs_mdpi.md               ← Remote Sensing (MDPI open-access)
│   └── giscience/
│       ├── ijgis.md                 ← Int'l Journal of GIS
│       ├── transactions_gis.md
│       ├── annals_aag.md
│       ├── cagis.md                 ← Cartography & GIS
│       └── epb_template.md          ← Environment & Planning B
│
├── mcp/                        ← MCP server configurations and custom servers
│   ├── mcp_config.json         ← Master MCP manifest
│   ├── geo_mcp_server.py       ← Custom MCP: spatial data, GEE, GADM, OSM
│   ├── arxiv_mcp.py            ← Custom MCP: ArXiv paper fetch & search
│   └── README_MCP.md           ← How to add/use MCP servers
│
├── tools/                      ← Standalone Python utilities
│   ├── arxiv_search.py
│   ├── semantic_scholar.py
│   ├── geo_data_downloader.py  ← Downloads open geo datasets
│   ├── latex_compiler.py
│   └── pdf_parser.py
│
├── configs/                    ← YAML configuration files
│   ├── default.yaml            ← Default agent configuration
│   ├── quick_mode.yaml         ← Fast single-agent mode
│   ├── full_auto.yaml          ← Fully autonomous overnight mode
│   ├── codex_hybrid.yaml       ← Claude orchestrator + Codex workers
│   └── benchmark_only.yaml     ← Run GeoBenchmark without writing paper
│
├── GeoBenchmark/               ← Geospatial regression benchmark suite
│   ├── README.md               ← Benchmark documentation
│   ├── download_data.py        ← Auto-download all open datasets
│   ├── run_benchmark.py        ← Run all baselines and generate report
│   ├── datasets/               ← Downloaded open-source spatial datasets
│   │   ├── california_housing/
│   │   ├── boston_housing/
│   │   ├── london_house_prices/
│   │   ├── beijing_pm25/
│   │   ├── us_county_health/
│   │   └── README_DATASETS.md
│   ├── baselines/
│   │   ├── ols_baseline.py     ← Ordinary Least Squares (statsmodels)
│   │   ├── gwr_baseline.py     ← Geographically Weighted Regression (mgwr)
│   │   ├── mgwr_baseline.py    ← Multiscale GWR (mgwr)
│   │   ├── kriging_baseline.py ← Spatial interpolation baseline
│   │   └── rf_spatial.py       ← Random Forest with spatial features
│   ├── evaluation/
│   │   ├── metrics.py          ← R², RMSE, MAE, Moran's I residuals
│   │   └── visualize.py        ← Maps, scatter plots, residual plots
│   └── notebooks/
│       └── benchmark_demo.ipynb
│
├── ResearchArchitect/          ← Collaborative content — add your own work here
│   └── (empty — for collaborators to populate)
│
└── tests/                      ← Unit and integration tests
    ├── test_orchestrator.py
    ├── test_geo_tools.py
    └── test_benchmark.py
```

---

## Key Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Domain-aware orchestration** | `geo_specialist.py` injects GIS/RS domain knowledge into every agent call |
| **Modular participation** | Use individual agents standalone or chain them into a full loop |
| **Harness Engineering** | Pre/post hooks enforce safety, logging, and state persistence |
| **Dual coding backend** | Choose Claude Code only OR Claude as orchestrator + Codex workers |
| **Reproducible benchmarks** | GeoBenchmark provides fixed datasets, baselines, and metrics |
| **Journal-aligned output** | Templates match exact formatting of target journals |
| **MCP extensibility** | Drop in new MCP servers to add capabilities without touching core code |

---

## Data Flow

```
User Input (research topic / hypothesis)
        │
        ▼
  [Orchestrator] ─── reads config.yaml, loads agent chain
        │
   ┌────┴────┐
   │         │
   ▼         ▼
[Literature  [Geo Specialist]
  Agent]     │ ← injects domain context
   │         │
   └────┬────┘
        │
        ▼
[Experiment Agent] ─── may spawn Codex workers for coding tasks
        │
        ▼
[Writing Agent] ─── uses journal template
        │
        ▼
[Review Agent] ─── simulated peer review + revision
        │
        ▼
   Final Paper Output (LaTeX / Markdown / PDF)
```

---

## Agent Modes

| Mode | Description | Config File |
|------|-------------|-------------|
| `quick` | Single-pass: idea → draft in ~10 min | `configs/quick_mode.yaml` |
| `full-auto` | Complete loop overnight: lit review → experiments → paper → review | `configs/full_auto.yaml` |
| `codex-hybrid` | Claude orchestrates, Codex runs coding tasks in parallel | `configs/codex_hybrid.yaml` |
| `benchmark-only` | Run GeoBenchmark baselines only | `configs/benchmark_only.yaml` |
| `partial` | Call individual agents via CLI flags or skills | `--agents literature,writing` |

---

## Harness Engineering Summary

Hooks are configured in `settings.json` and executed by the Claude Code harness:

| Hook | Trigger | Action |
|------|---------|--------|
| `PreToolUse` | Before any Bash or Write call | Validate path safety, log intent |
| `PostToolUse` | After file write or code execution | Update experiment state JSON |
| `Stop` | Agent session ends | Save checkpoint, send notification |
| `Notification` | Long-running task completes | Desktop/Slack/email alert |

Skills (invocable via `/skill-name`):

| Skill | Command | Purpose |
|-------|---------|---------|
| Geo Literature Search | `/geo-search "topic"` | Domain-aware ArXiv + Scholar search |
| Run Experiment | `/run-experiment config.yaml` | Execute benchmark or custom experiment |
| Write Section | `/write-section methods` | Draft a specific paper section |
| Peer Review | `/review-paper paper.md` | Get simulated reviewer feedback |
| Geo Plot | `/geo-plot data.gpkg` | Generate spatial visualization |
| Submit Check | `/submit-check IJGIS` | Validate formatting for target journal |
