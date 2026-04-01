# GeoResearchAgent-247

> A fully automatic, domain-aware AI research agent for Geoscientists, Remote Sensing researchers, and GIScientists.

---

## What It Does

GeoResearchAgent-247 automates the complete academic research lifecycle:

1. **Literature review** — searches ArXiv, Semantic Scholar, and Google Scholar for relevant papers, summarizes findings, and identifies research gaps
2. **Hypothesis generation** — proposes novel research questions informed by current literature and domain context
3. **Experiment design & execution** — writes and runs Python code for spatial analysis, remote sensing workflows, and GIS operations
4. **Paper writing** — drafts full academic papers using journal-specific templates (IJGIS, IEEE TGRS, GRL, RSE, and more)
5. **Self-review** — simulates peer review feedback and iteratively revises the paper
6. **Spatial benchmarking** — provides a ready-to-run benchmark suite (GeoBenchmark) with OLS, GWR, and MGWR baselines
7. **Memory management** — three-layer memory (working / session / long-term) persists research knowledge across agents and sessions, with token-aware retrieval and automatic pruning
8. **Token optimization** — eight complementary techniques (prompt compression, response caching, tiered model routing, context windowing, dynamic max_tokens, abstract truncation, context budgeting, session ledger) reduce API costs by 40–70%

---

## Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

Required:
- Python ≥ 3.11
- Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
- Anthropic API key (`export ANTHROPIC_API_KEY=your_key`)
- Optional: OpenAI API key for Codex workers (`export OPENAI_API_KEY=your_key`)

### Run Full Automatic Research

```bash
# Full overnight research loop (literature → experiments → paper)
python core/orchestrator.py --config configs/full_auto.yaml --topic "Spatial non-stationarity in urban heat island effects"

# Quick single-pass draft (~10 minutes)
python core/orchestrator.py --config configs/quick_mode.yaml --topic "GWR vs MGWR for house price prediction"

# Claude as orchestrator, Codex as coding workers
python core/orchestrator.py --config configs/codex_hybrid.yaml --topic "Deep learning for SAR flood mapping"
```

### Run Individual Agent Functions

```bash
# Literature review only
python agents/literature_agent.py --topic "Geographically Weighted Regression" --output lit_review.md

# Run GeoBenchmark only
python GeoBenchmark/run_benchmark.py --dataset california_housing --models ols,gwr,mgwr

# Generate paper from existing results
python agents/writing_agent.py --results results/experiment.json --template templates/giscience/ijgis.md

# Simulated peer review
python agents/review_agent.py --paper draft.md --journal IJGIS
```

### Use Claude Code Skills (Slash Commands)

Inside any Claude Code session in this directory:

```
/geo-search "spatial heterogeneity urban temperature"
/run-experiment configs/benchmark_only.yaml
/write-section methods
/review-paper draft.md
/geo-plot results/coefficients.gpkg
/submit-check IJGIS
```

---

## Modes of Operation

### Mode 1: Full Auto (Overnight Research)

The agent runs autonomously from topic to paper. Recommended for new research directions.

```bash
python core/orchestrator.py --config configs/full_auto.yaml \
  --topic "Multiscale spatial analysis of PM2.5 and respiratory health" \
  --journal RSE \
  --output-dir output/pm25_study/
```

This will:
1. Search literature (ArXiv + Semantic Scholar, top 30 papers)
2. Identify 3 novel hypotheses
3. Design experiments for each
4. Download relevant open datasets via GeoBenchmark
5. Execute Python code (sandboxed)
6. Write the paper using the RSE template
7. Run simulated peer review
8. Revise and produce final PDF

**Estimated runtime:** 2–6 hours depending on complexity.

---

### Mode 2: Claude Code Only

All coding tasks handled by Claude Code directly.

```bash
python core/orchestrator.py --backend claude-only --topic "..."
```

---

### Mode 3: Claude as Orchestrator + Codex Workers

Claude handles planning, writing, and review. Codex (GPT-4o-mini or o1) handles parallel coding tasks. Useful for experiment-heavy work.

```bash
python core/orchestrator.py --config configs/codex_hybrid.yaml --topic "..."
```

Configuration in `configs/codex_hybrid.yaml`:
```yaml
backend:
  orchestrator: claude-sonnet-4-6
  coding_workers:
    provider: openai
    model: gpt-4o-mini
    max_workers: 4
    task_types: [code_generation, data_analysis, plotting]
```

This mode spawns up to 4 parallel Codex workers for coding subtasks while Claude maintains research coherence.

---

### Mode 4: Partial Agent Functions

Use individual components without running the full loop:

```bash
# Flags to include/exclude specific agents
python core/orchestrator.py --agents literature,writing --skip experiment,review

# Available agent flags:
# literature, experiment, writing, review, geo_specialist, codex_worker
```

Or call agents directly (see scripts above).

---

## Harness Engineering

The agent uses **Claude Code's hook system** for automated lifecycle management. Hooks are configured in `settings.json`.

### Active Hooks

| Hook | When | What It Does |
|------|------|--------------|
| `PreToolUse` | Before Bash/Write | Validates paths, blocks dangerous commands, logs intent |
| `PostToolUse` | After tool execution | Updates `experiment_state.json`, caches results |
| `Stop` | Agent session ends | Saves checkpoint, generates summary, sends notification |
| `Notification` | Long tasks finish | Desktop alert via `notify-send` or macOS `osascript` |

### Configuring Hooks

Edit `settings.json` to customize hook behavior:

```json
{
  "hooks": {
    "PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "bash harness/hooks/pre_tool_use.sh"}]}],
    "PostToolUse": [{"matcher": "Write", "hooks": [{"type": "command", "command": "bash harness/hooks/post_tool_use.sh"}]}],
    "Stop": [{"hooks": [{"type": "command", "command": "bash harness/hooks/stop_hook.sh"}]}]
  }
}
```

### Custom Skills

Skills are slash commands you invoke inside a Claude Code session. Located in `harness/skills/`:

```
/geo-search       → domain-aware literature search with geo-specific query expansion
/run-experiment   → execute configured benchmark or custom experiment
/write-section    → draft a specific section using journal template
/review-paper     → simulated multi-reviewer peer review
/geo-plot         → spatial visualization with auto-chosen map projection
/submit-check     → validate manuscript against journal requirements
```

---

## Memory Management

GeoResearchAgent-247 includes a three-layer memory system (`core/memory_manager.py`) that persists research knowledge across agent stages and sessions.

### Memory Layers

| Layer | Scope | Storage | Purpose |
|-------|-------|---------|---------|
| **Working memory** | Current process | In-process dict | Fast inter-agent data sharing within one run |
| **Session memory** | Current run | `.checkpoints/{run_id}_memory.json` | Resume interrupted runs; carry stage outputs forward |
| **Long-term memory** | All runs | `.memory/long_term.json` | Reuse literature summaries, remember failed hypotheses, track review decisions across topics |

### Key Capabilities

- **Token-aware retrieval** — `build_context(keys, token_budget=3000)` ranks entries by priority and recency, dropping lowest-priority items when the budget is exhausted
- **Keyword search** — `search_long_term(query)` finds relevant past entries without a vector database
- **Automatic pruning** — when the long-term store exceeds `lt_max_entries` (default 200) or `lt_token_budget` (default 32,000 tokens), lowest-priority entries are evicted
- **Priority system** — agents assign priorities (e.g., `literature=1.8`, `draft=1.5`); review decisions and failed hypotheses are stored with lower priority so they persist without crowding working context

### Usage in Code

```python
from core.memory_manager import MemoryManager

mm = MemoryManager(run_id="run_20260331_143000")

# Store a result with auto-generated summary
mm.store("literature", result, priority=1.8, tags=["giscience"])

# Build a token-bounded context string for a prompt
context = mm.build_context(["literature", "geo_context"], token_budget=2000)

# Save a plain-text fact to long-term memory
mm.remember("mgwr_diverged_small_n", "MGWR failed to converge on n<100 datasets", priority=1.0)

# Search long-term memory by keyword
relevant = mm.search_long_term("GWR bandwidth selection", token_budget=800)

# Flush to disk
mm.persist()

# Token usage report
print(mm.token_usage_report())
# → {"working_tokens": 412, "session_tokens": 1840, "long_term_tokens": 5200, "long_term_entries": 47}
```

### Memory Files

```
.checkpoints/
└── run_20260331_143000_memory.json   ← per-run session memory
.memory/
└── long_term.json                    ← shared across all runs
output/run_20260331_143000/
└── memory_report.json                ← end-of-run stats
```

---

## Token Optimization

GeoResearchAgent-247 applies eight complementary techniques to minimize Anthropic API token usage without sacrificing output quality. All techniques are configurable in `configs/*.yaml` under the `token_optimizer` key.

### Techniques

#### 1. Token Counting Before Dispatch
Every prompt is estimated (1 token ≈ 4 chars) before the API call. Prompts that would exceed the context window are rejected early with a clear error, preventing wasted spend on truncated responses.

#### 2. Prompt Compression
`compress_prompt()` in `core/token_optimizer.py` runs before every API call:
- Collapses 3+ consecutive blank lines → 2
- Strips trailing whitespace per line
- Removes HTML comments (`<!-- ... -->`)
- Collapses repeated inline spaces

Typical savings: **5–15%** of input tokens with no semantic loss.

#### 3. Tiered Model Routing
`select_model()` routes each call to the cheapest model that can handle it, based on estimated input token count and declared task complexity:

| Input size | Complexity flag | Model selected |
|-----------|-----------------|----------------|
| < 800 tokens | `simple` | `claude-haiku-4-5` (~20× cheaper than Opus) |
| 800–6,000 tokens | `default` | `claude-sonnet-4-6` (configured default) |
| > 6,000 tokens | `complex` | `claude-opus-4-6` |

Query generation, JSON extraction, and result analysis are automatically routed to Haiku. Literature synthesis and paper revision use Sonnet/Opus.

#### 4. Response Caching
`ResponseCache` stores API responses on disk, keyed by SHA-256 hash of `(model, system_prompt, user_prompt)`. On repeated runs (e.g., re-running after a crash, or re-reviewing the same draft), identical prompts return instantly at zero cost.

```yaml
token_optimizer:
  response_caching: true
  cache_dir: .cache/responses
```

Cache hit/miss statistics are written to `output/{run_id}/memory_report.json`.

#### 5. Abstract & Field Truncation
Literature abstracts are hard-truncated to `abstract_token_budget` (default 80 tokens / ~320 chars) at fetch time — before they are assembled into synthesis prompts. This prevents a single long abstract from crowding out other papers in the context window.

```yaml
token_optimizer:
  abstract_token_budget: 80   # tokens per paper abstract
```

#### 6. Context Windowing
`build_windowed_prompt(sections, token_budget)` assembles multi-section prompts within a strict token ceiling. Sections are ranked by a relevance score; lower-ranked sections are dropped (not truncated mid-sentence) when the budget is exhausted.

```python
# Example: writing agent section generation
build_windowed_prompt(
    sections=[
        ("Topic", topic, 2.0),           # highest priority — always included
        ("Results Summary", results, 1.2), # dropped first if budget is tight
        ("Section Guidance", guide, 1.8),
    ],
    token_budget=3000,
)
```

#### 7. Dynamic `max_tokens` per Task
Rather than using a single blanket `max_tokens=4096` ceiling, each task type has a calibrated output budget:

| Task type | `max_tokens` |
|-----------|-------------|
| `query_generation` | 512 |
| `json` (hypothesis extraction) | 1,024 |
| `section_short` (abstract, conclusion) | 1,024 |
| `section_long` (methods, results) | 2,048 |
| `code` | 4,096 |
| `revision` | 8,192 |

Over-allocating `max_tokens` does not cost tokens directly, but it increases latency and can encourage verbose responses that consume more output tokens.

#### 8. Session Token Ledger
`TokenLedger` accumulates input tokens, output tokens, and Anthropic prompt-cache reads across every API call in a session. At the end of each run it writes `output/{run_id}/token_usage.json`:

```json
{
  "input_tokens": 48320,
  "output_tokens": 19840,
  "cache_read_tokens": 12100,
  "total_tokens": 68160,
  "api_calls": 31,
  "estimated_cost_usd": 0.4421
}
```

A configurable `hard_limit_tokens` raises `RuntimeError` before the limit is breached, preventing runaway overnight spend.

```yaml
token_optimizer:
  hard_limit_tokens: 2000000   # ~$10 at Sonnet pricing; null = unlimited
```

### Configuration Reference

```yaml
token_optimizer:
  prompt_compression: true        # strip whitespace / collapse blank lines
  response_caching: true          # disk cache keyed on SHA-256(model+prompts)
  tiered_model_routing: true      # haiku → sonnet → opus based on input size
  context_windowing: true         # rank + drop sections to fit token budget
  abstract_token_budget: 80       # tokens per fetched paper abstract
  context_token_budget: 3000      # max tokens for assembled context per call
  hard_limit_tokens: null         # set an integer to cap total session spend
  cache_dir: .cache/responses     # where to store cached responses
```

### Estimated Savings

When all techniques are enabled on a full-auto run (literature + experiments + writing + review):

| Technique | Typical reduction |
|-----------|-------------------|
| Prompt compression | 5–15% input tokens |
| Abstract truncation | 30–50% literature-stage input |
| Context windowing | 20–40% writing-stage input |
| Response caching | 0–100% on repeated/resumed runs |
| Tiered routing | 40–80% cost reduction on simple calls |
| Dynamic max_tokens | 10–20% output token reduction |

**Combined: 40–70% reduction in total token cost vs. naive implementation.**

---

## GeoBenchmark

A reproducible spatial regression benchmark for comparing models across multiple datasets.

### Included Datasets (all open-source)

| Dataset | N | Features | Task |
|---------|---|---------|------|
| California Housing (1990 Census) | 20,640 | 8 + coordinates | House value prediction |
| Boston Housing | 506 | 13 + coordinates | Median home value |
| London House Prices | ~1.5M | 20+ + coordinates | Transaction price |
| Beijing PM2.5 | 8,760 | 11 + coordinates | Air quality prediction |
| US County Health Rankings | 3,142 | 40+ + coordinates | Health outcome prediction |

### Included Baselines

| Model | Library | Key Parameters |
|-------|---------|---------------|
| OLS | `statsmodels` | Heteroskedasticity-robust standard errors |
| GWR | `mgwr` | Adaptive bi-square kernel, AICc bandwidth selection |
| MGWR | `mgwr` | Adaptive kernels per variable, AICc selection |
| Ordinary Kriging | `pykrige` | Variogram fitting, CV-optimized range |
| Spatial RF | `scikit-learn` | + spatial lag features + XY coordinates |

### Running the Benchmark

```bash
# Download all datasets (first run)
python GeoBenchmark/download_data.py

# Run all models on all datasets
python GeoBenchmark/run_benchmark.py --all

# Run specific dataset + models
python GeoBenchmark/run_benchmark.py \
  --dataset california_housing \
  --models ols,gwr,mgwr \
  --output-dir GeoBenchmark/results/

# Open interactive notebook
jupyter notebook GeoBenchmark/notebooks/benchmark_demo.ipynb
```

---

## Journal Templates

Templates enforce correct structure, section ordering, word limits, and formatting for each target journal.

### Geoscience

| Journal | Template | Impact Factor |
|---------|----------|--------------|
| Nature Geoscience | `templates/geoscience/nature_geoscience.md` | ~19 |
| JGR: Solid Earth | `templates/geoscience/jgr_solid_earth.md` | ~4 |
| Geophysical Research Letters | `templates/geoscience/grl_template.md` | ~5 |
| Earth System Science Data | `templates/geoscience/earth_system_sci.md` | ~12 |

### Remote Sensing

| Journal | Template | Impact Factor |
|---------|----------|--------------|
| Remote Sensing of Environment | `templates/remote_sensing/remote_sensing_env.md` | ~14 |
| IEEE TGRS | `templates/remote_sensing/ieee_tgrs.md` | ~8 |
| ISPRS JPRS | `templates/remote_sensing/isprs_jprs.md` | ~12 |
| Remote Sensing (MDPI) | `templates/remote_sensing/rs_mdpi.md` | ~5 |

### GIScience

| Journal | Template | Impact Factor |
|---------|----------|--------------|
| IJGIS | `templates/giscience/ijgis.md` | ~4 |
| Transactions in GIS | `templates/giscience/transactions_gis.md` | ~3 |
| Annals of AAG | `templates/giscience/annals_aag.md` | ~4 |
| Cartography & GIS | `templates/giscience/cagis.md` | ~3 |
| Environment & Planning B | `templates/giscience/epb_template.md` | ~4 |

---

## MCP Servers

MCP (Model Context Protocol) servers extend the agent's capabilities. Configured in `.mcp.json`.

### Bundled MCP Servers

| Server | Purpose |
|--------|---------|
| `filesystem` | Read/write local files and datasets |
| `fetch` | Fetch web content (papers, data portals) |
| `geo_mcp_server` | Spatial data access: GADM, OSM, GEE, Census |
| `arxiv_mcp` | ArXiv search, paper fetch, abstract parsing |

### Adding New MCP Servers

```json
// .mcp.json
{
  "mcpServers": {
    "my_custom_server": {
      "command": "python",
      "args": ["mcp/my_server.py"],
      "env": {"API_KEY": "${MY_API_KEY}"}
    }
  }
}
```

---

## Configuration Reference

### `configs/default.yaml`

```yaml
agent:
  max_literature_papers: 30
  max_experiment_iterations: 3
  writing_temperature: 0.7
  review_rounds: 2

backend:
  orchestrator: claude-sonnet-4-6
  coding_workers:
    provider: claude          # or "openai" for Codex
    model: claude-sonnet-4-6
    max_workers: 1

output:
  format: markdown            # markdown | latex | pdf
  save_intermediate: true
  checkpoint_dir: .checkpoints/
```

---

## File Outputs

All outputs are saved to `output/<run_id>/`:

```
output/
└── run_20260331_143000/
    ├── literature_review.md
    ├── hypotheses.json
    ├── experiment_log.json
    ├── results/
    │   ├── figures/
    │   └── tables/
    ├── draft_v1.md
    ├── review_feedback.md
    ├── draft_v2.md        ← revised after review
    └── paper_final.pdf
```

---

## ResearchArchitect

The `ResearchArchitect/` folder is a shared space for collaborators to contribute:
- Custom experiment scripts
- Additional journal templates
- Domain-specific prompts
- Pilot datasets
- Research notes

No files are committed here by default. Add your own content and document it with a `README.md` inside.

---

## Contributing

1. Fork this repository
2. Add your content to `ResearchArchitect/` or submit PRs for `templates/`, `agents/`, or `GeoBenchmark/`
3. Follow the coding standards in `pyproject.toml`
4. Write tests in `tests/`

---

## License

MIT License. See `LICENSE` for details.

---

## Citation

If you use GeoResearchAgent-247 in your research, please cite:

```bibtex
@software{geo_research_agent_247,
  title  = {GeoResearchAgent-247: Autonomous AI Research Agent for Geoscientists},
  year   = {2026},
  url    = {https://github.com/your-org/geo_research_agent_247}
}
```
