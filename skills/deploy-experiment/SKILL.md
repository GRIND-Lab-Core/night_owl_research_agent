---
name: deploy-experiment
description: Deploy and run experiments for ML/DL training (local, remote, or Modal GPU) AND spatial data science / GIScience experiments (local, data-driven). Reads from output/refine-logs/EXPERIMENT_PLAN.md and output/refine-logs/FINAL_PROPOSAL.md, writes to output/experiment/. Use when user says "run experiment", "deploy experiment", "execute experiment plan", or needs to launch training / spatial analysis jobs.
argument-hint: [experiment-description-or-scope]
allowed-tools: Bash(*), Read, Grep, Glob, Edit, Write, Agent
---

# Deploy Experiment

Execute the experiment described in **output/refine-logs/EXPERIMENT_PLAN.md** (with context from **output/refine-logs/FINAL_PROPOSAL.md**) and write all results to **output/experiment/**.

Scope override (optional): $ARGUMENTS

---

## Inputs

| File | Purpose |
|---|---|
| `output/refine-logs/EXPERIMENT_PLAN.md` | Authoritative experiment plan: objectives, claims, run order, commands, success criteria, data needs |
| `output/refine-logs/FINAL_PROPOSAL.md` | Final refined proposal: problem anchor, method, expected contribution, constraints |
| `CLAUDE.md` | Environment config (gpu location, conda env, SSH, wandb, code_sync) |

If either required input is missing, stop and tell the user which file to produce first (likely via `/refine-research` and `/experiment-design`).

## Outputs (all under `output/experiment/`)

| File | Content |
|---|---|
| `EXPERIMENT_RESULT.md` | Final results report: per-claim outcomes, tables, key numbers, figures referenced |
| `EXPERIMENT_LOG.md` | Chronological run log: commands executed, environment, timings, stdout/stderr pointers, failures, retries |
| `data/` | Intermediate data artifacts ready for visualization (CSV, Parquet, GeoJSON, GeoPackage, NetCDF, .npz, model predictions, metrics.json) |
| `figures/` *(optional)* | Quick-look figures produced during the run (final paper figures come from `paper-figure`) |
| `scripts/` *(optional)* | Any inline runner scripts created to execute the plan |

Create the `output/experiment/`, `output/experiment/data/`, `output/experiment/figures/`, and `output/experiment/scripts/` directories at the start if they do not exist.

---

## Step 0: Mandatory Local GPU Availability Check (pilot AND full experiments)

**This check is REQUIRED before classification, regardless of whether the run is a pilot, a full experiment, Track A, Track B, or mixed.** The goal is to guarantee that when a local GPU is present, every ML / DL component runs on it — never silently on CPU.

Run the local GPU presence check first:

**Local CUDA:**
```bash
nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader
```

**Local Mac MPS (only if `nvidia-smi` is missing or returns zero rows):**
```bash
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```

Decision rules (apply in order):

1. If `nvidia-smi` exits 0 and returns at least one GPU row → record `LOCAL_GPU=cuda`, capture the `<gpu_id>` and the chosen device for use in Step A5 and any pilot launch. Do **NOT** gate on idle memory; a desktop GPU with a display attached normally reports 0.7–1.5 GiB used.
2. Else if `torch.backends.mps.is_available()` returns `True` → record `LOCAL_GPU=mps`.
3. Else → record `LOCAL_GPU=none`. Only in this case may an ML / DL component fall back to CPU or to remote / Modal as defined in `CLAUDE.md`.

Write the result as the first lines of `output/experiment/EXPERIMENT_LOG.md`:

```markdown
- LOCAL_GPU: cuda | mps | none
- Device chosen: <e.g. CUDA:0 / mps / cpu / remote-A100>
- GPU check command + output: <verbatim>
```

**Hard rule:** if `LOCAL_GPU` is `cuda` or `mps`, every ML / DL pilot AND every ML / DL full-experiment run launched by this skill MUST use that local GPU. Do not switch to remote / Modal / CPU just because the plan's default is set elsewhere — local GPU takes precedence whenever it is present. Record any deviation as a `CONTRACT_VIOLATION.md` with the user's explicit override.

If `LOCAL_GPU=none` and `CLAUDE.md` lists `gpu: remote` or `gpu: modal`, route ML / DL work there as documented in Step A1; otherwise stop and report to the user before proceeding.

This check applies equally to:
- Pilot experiments invoked from `/generate-idea` (Phase 5)
- Full experiments invoked from `/full-pipeline` Stage 2
- Any mixed GeoAI experiment whose Track A leg requires GPU

---

## Step 0.1: Classify the Experiment

Read `EXPERIMENT_PLAN.md` and `FINAL_PROPOSAL.md`, then classify into ONE of the two tracks below. Record the choice at the top of `EXPERIMENT_LOG.md`.

| Track | Signals | Route |
|---|---|---|
| **A. ML / Deep Learning** | Model training, fine-tuning, gradient descent, epochs, GPU/TPU required, checkpoints, benchmarks on splits, wandb-style tracking | → Step A1 |
| **B. Spatial / GIScience** | Spatial regression, ESDA (Moran's I, LISA, Getis-Ord), GWR/MGWR, spatial clustering, accessibility (2SFCA, isochrones), cartographic description, spatiotemporal analysis, network analysis, choropleth-driven claims, no GPU needed (mostly CPU + geospatial libs) | → Step B1 |

Mixed experiments (e.g., GeoAI: deep learning applied to spatial data) run **both** tracks in sequence — Track A for model training/inference, Track B for downstream spatial evaluation.

Invoke supporting skills when needed:

- If the plan requires datasets not yet in `data/raw/` → call **`data-download`** skill with the data requirements from the plan.
- For Track B (spatial analysis execution and diagnostics) → call **`spatial-analysis`** skill to run the analysis under guideline-driven decisions. This skill (deploy-experiment) orchestrates and records results; `spatial-analysis` is the executor for spatial methods.

---

## Track A — ML / Deep Learning Experiments

### A1. Detect Environment

From `CLAUDE.md`:

- **Local GPU** (`gpu: local`): local CUDA or Apple MPS
- **Remote server** (`gpu: remote`): SSH alias, conda env, code directory
- **Modal** (`gpu: modal`): use Modal serverless GPU app

### A2. Pre-flight GPU Check

The local presence check from **Step 0** has already determined `LOCAL_GPU`. Re-use that result — do not re-decide here. Only run remote / multi-GPU contention checks below.

**Remote (SSH), only when `LOCAL_GPU=none` and `CLAUDE.md` says `gpu: remote`:**
```bash
ssh <server> nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader
```

**Contention check (optional, only when sharing a multi-GPU box):** pick a GPU where `memory.free / memory.total > 0.7` to avoid colliding with another running job. On a single-GPU workstation, skip this and proceed once presence is confirmed in Step 0.

### A3. Sync Code (Remote Only)

Read `code_sync` in `CLAUDE.md` (default `rsync`).

**rsync:**
```bash
rsync -avz --include='*.py' --exclude='*' <local_src>/ <server>:<remote_dst>/
```

**git:**
```bash
git add -A && git commit -m "sync: experiment deployment" && git push
ssh <server> "cd <remote_dst> && git pull"
```

### A4. W&B Integration (only when `wandb: true`)

Skip entirely if not enabled. Otherwise, ensure scripts contain:

```python
import wandb
wandb.init(project=WANDB_PROJECT, name=EXP_NAME, config={...})
wandb.log({"train/loss": loss, "train/lr": lr, "step": step})
wandb.log({"eval/loss": eval_loss, "eval/accuracy": acc})
wandb.finish()
```

Verify login: `ssh <server> "wandb status"`.

### A5. Launch

**Remote (SSH + screen):**
```bash
ssh <server> "screen -dmS <exp_name> bash -c '\
  eval \"\$(<conda_path>/conda shell.bash hook)\" && \
  conda activate <env> && \
  CUDA_VISIBLE_DEVICES=<gpu_id> python <script> <args> 2>&1 | tee <log_file>'"
```

**Local:**
```bash
CUDA_VISIBLE_DEVICES=<gpu_id> python <script> <args> 2>&1 | tee output/experiment/<exp_name>.log
# Mac MPS: omit CUDA_VISIBLE_DEVICES
```

Use `run_in_background: true` for long local jobs. Each experiment gets its own screen/process and one GPU.

### A6. Collect Artifacts

After completion (detected via `/monitor-experiment` or screen ending):

```bash
rsync -avz -e "ssh -p <PORT>" root@<HOST>:/workspace/project/results/ output/experiment/data/
scp -P <PORT> root@<HOST>:/workspace/*.log output/experiment/
```

Place tabular metrics as `metrics.csv` / `metrics.json`, learned checkpoints' evaluation predictions as `predictions.parquet` (or `.npz`), and any training curves as `curves.csv` — all under `output/experiment/data/` so they are visualization-ready.

---

## Track B — Spatial / GIScience Experiments

These experiments are typically CPU-bound, run locally, and rely on PyGeoAI / GeoPandas / PySAL / libpysal / esda / spreg / mgwr / rasterio / xarray / networkx / scikit-mobility. GPU is irrelevant unless the plan specifies a deep-learning component (then also run Track A).

### B1. Verify / Acquire Data

1. Read the **Data** section of `EXPERIMENT_PLAN.md`.
2. Check `data/DATA_MANIFEST.md` and `data/raw/` for each required dataset.
3. For any missing dataset → invoke the **`data-download`** skill with the precise data need (geography, time range, spatial resolution, variables, format). Do NOT ad-hoc download; rely on the skill so provenance is recorded in `DATA_MANIFEST.md`.
4. After download, re-check presence and basic integrity (file exists, non-zero size, opens with the expected library).

### B2. Pre-flight Environment Check

```bash
python - <<'PY'
import importlib, sys
required = ["geopandas","pysal","libpysal","esda","spreg","mgwr","rasterio","xarray","shapely","pyproj","numpy","pandas","matplotlib"]
missing = [p for p in required if importlib.util.find_spec(p) is None]
print("MISSING:", missing)
PY
```

If anything is missing, report to the user and stop — do NOT silently `pip install` into a shared env. Suggest the conda env from `CLAUDE.md`.

### B3. Plan-to-Run Mapping

For every claim listed in `EXPERIMENT_PLAN.md`, identify:

| Plan field | Concrete execution artifact |
|---|---|
| Claim / hypothesis | Section heading in `EXPERIMENT_RESULT.md` |
| Spatial unit | CRS, geometry file in `output/experiment/data/` |
| Method | Call into `spatial-analysis` skill (ESDA / regression / GWR / accessibility / etc.) |
| Diagnostics required | **Only the diagnostics the claim actually needs** (see `spatial-analysis/SKILL.md` §5.1 / §5.3). Do NOT run Moran's I residuals, MAUP sweeps, GWR, alternative-W sensitivity, or spatial CV by default — they apply only when the claim depends on them. When the plan is silent, follow `spatial-analysis` §5.3 and ask the user before adding heavyweight checks (and before omitting one that a strict GIScience reviewer would expect). Capture whatever diagnostics are run in `data/diagnostics.json`. |
| Success criterion | Pass/fail row in the results table |

### B4. Execute via the `spatial-analysis` Skill

Invoke the `spatial-analysis` skill per claim (or per grouped set of claims). Pass the research question verbatim from `EXPERIMENT_PLAN.md` and the resolved data paths. The skill will write analysis artifacts to `output/spatial-analysis/` — this skill (`deploy-experiment`) is then responsible for:

1. Copying / linking the resulting tables and figures into `output/experiment/data/` and `output/experiment/figures/` with stable filenames.
2. Writing a short per-claim summary row (numbers, CI, p-values, effect sizes, diagnostics) to `EXPERIMENT_RESULT.md`.

**Intermediate data files to persist** — decide which artifacts are actually needed based on the claims, methods, and visualizations the plan implies. The list below is **illustrative, not mandatory**; produce only what is genuinely useful for downstream visualization, paper figures, or reproducibility, and skip the rest.

Examples (pick, rename, or add as appropriate):

- `data/features.gpkg` or `.parquet` — joined analytical table with geometries
- `data/moran_results.csv` — global + local indicators
- `data/lisa_clusters.gpkg` — LISA cluster/outlier labels
- `data/regression_coefficients.csv` — OLS / spatial lag / error / GWR coefficients
- `data/gwr_local_estimates.gpkg` — per-location coefficients, t-values, local R²
- `data/predictions.parquet` — out-of-sample predictions with geometry keys
- `data/diagnostics.json` — VIF, condition number, Moran's I on residuals, CV scores
- `data/metrics.json` — aggregate pass/fail per claim (machine-readable)

**Always accompany data with metadata** so the next step (figure generation, paper writing, review) can interpret it without re-reading code:

- `data/README.md` — index of every file under `data/`, one line each: filename → what it is, which claim it supports, which run produced it.
- Per-file sidecar: for each non-trivial artifact `X.ext`, write `X.meta.json` (or `X.meta.yaml`) containing at minimum:
  - `description` — one sentence on what the file holds
  - `produced_by` — script / skill invocation / run id in `EXPERIMENT_LOG.md`
  - `source_inputs` — upstream files used
  - `schema` — columns (name, dtype, unit, description) for tabular/vector files; variables + dims for raster/NetCDF
  - `crs` — EPSG code or WKT (for any geospatial file)
  - `spatial_unit` / `temporal_range` — when applicable
  - `notes` — caveats, filters applied, known issues

For simple CSVs, documenting columns in a header comment plus a one-line entry in `data/README.md` is sufficient; reserve full sidecar JSON for geospatial or multi-dimensional artifacts.

### B5. For Mixed GeoAI Experiments

If the plan couples deep learning with spatial evaluation:

1. Run Track A to train/infer.
2. Export model predictions to `output/experiment/data/predictions.parquet` joined to spatial IDs.
3. Run Track B on those predictions (e.g., residual spatial autocorrelation, fairness across regions, spatially-stratified CV, LISA on error maps).

---

## Human Checkpoint: Data Synthesis

Honor the `HUMAN_CHECKPOINT` flag in `CLAUDE.md` (default: `true`). When set, **PAUSE** and request explicit user approval before performing any of the synthesis actions below; resume only after the user replies. When `false`, append a one-line rationale to `output/PROJ_NOTES.md` and proceed. **Never** silently fabricate or substitute experiment data.

| Trigger | Show before pausing |
|---|---|
| A required dataset is missing and the plan would be satisfied by simulated, imputed, or synthetically generated input data | Source(s) considered, exact synthesis recipe (sampler / generator / random seed), and which claims would rely on it |
| A run FAILED but the plan needs a value for that claim | The failure mode, the proposed substitute (e.g., last-checkpoint metric, k-fold mean, prior run, hand-set placeholder), and the impact on downstream claims |
| Metrics, predictions, or diagnostics need to be aggregated / re-weighted / re-scaled before being written to `data/` | Aggregation function, weights, denominator choice, and which raw artifacts are being collapsed |
| A Track B sidecar (`*.meta.json`) is being authored from inferred (not directly observed) schema, CRS, or units | Per-field provenance: observed vs inferred, source of inference |
| Mixed GeoAI Step B5 will join model predictions to spatial IDs via a key the plan does not specify | The join key proposed, fallback if matches < 100%, and risk of silent label leakage |
| `EXPERIMENT_RESULT.md` would mark a claim **Pass** using values that were not produced by an executed run in `EXPERIMENT_LOG.md` | The exact source of each number and why it is acceptable evidence |

If the user declines a synthesis action, record the decision in `EXPERIMENT_LOG.md` under the affected run as `Synthesis declined: <action> — <user reason>` and either re-plan, mark the claim **Blocked**, or stop.

---

## Step 5 (Both Tracks): Verify & Record

**Remote verify:**
```bash
ssh <server> "screen -ls"
```
**Local verify:** check process and, for Track A, GPU allocation.

Update `output/experiment/EXPERIMENT_LOG.md` continuously during the run. Use this structure:

```markdown
# Experiment Log

- Started: <ISO timestamp>
- Track: A | B | A+B
- Plan: output/refine-logs/EXPERIMENT_PLAN.md
- Proposal: output/refine-logs/FINAL_PROPOSAL.md
- Environment: <conda env / python version / host>

## Run <N>: <short name>
- Command: `...`
- GPU / CPU: ...
- Start → End: ...
- Exit status: SUCCESS | FAILED | PARTIAL
- Stdout/stderr: <path>
- Artifacts produced: <paths under output/experiment/data or figures>
- Notes: <anything surprising>
```

---

## Step 6 (Both Tracks): Write `EXPERIMENT_RESULT.md`

After all runs complete (or if `EXPERIMENT_PLAN.md` marks the run as terminal), compose `output/experiment/EXPERIMENT_RESULT.md` with this structure:

```markdown
# Experiment Result

> Plan: output/refine-logs/EXPERIMENT_PLAN.md
> Proposal: output/refine-logs/FINAL_PROPOSAL.md
> Track: A | B | A+B
> Date: <ISO>

## 1. Summary
<3–6 sentences: what was run, what was found, whether the headline claim holds>

## 2. Per-Claim Outcomes
| Claim | Success criterion | Observed | Pass/Fail |
|---|---|---|---|
| C1 ... | ... | ... | ✅ / ❌ |

## 3. Key Numbers and Tables
<inline the most important metrics; reference files under output/experiment/data/>

## 4. Diagnostics
<Track A: loss curves, generalization gap, ablations>
<Track B: **only the diagnostics the claim required** — pick from Moran's I on residuals, VIF, spatial CV, GWR local R², LISA significance, etc. Explicitly list any geospatial check that was considered but skipped, with the one-line reason (e.g., "MAUP sensitivity skipped: unit of analysis is fixed sensor location, not aggregated"). See `spatial-analysis/SKILL.md` §5 for the trigger conditions.>

## 5. Intermediate Artifacts (for visualization)
<list files under output/experiment/data/ with one-line descriptions so paper-figure can pick them up>

## 6. Known Limitations / Failures
<anything marked FAILED or PARTIAL in EXPERIMENT_LOG.md>
```

Append a one-line entry to `output/EXPERIMENT_LOG.md` (the repo-level log listed in `CLAUDE.md`) pointing to the new `output/experiment/EXPERIMENT_RESULT.md`.

---

## Key Rules

- ALWAYS read `EXPERIMENT_PLAN.md` and `FINAL_PROPOSAL.md` before any execution; never improvise the experiment.
- ALWAYS run the **Step 0** local GPU presence check before any pilot or full experiment. If `LOCAL_GPU` is `cuda` or `mps`, every ML/DL run MUST execute on the local GPU; fall back to remote / Modal / CPU only when `LOCAL_GPU=none`.
- Route data acquisition through the `data-download` skill — preserves provenance.
- Route spatial execution through the `spatial-analysis` skill — preserves generator-evaluator separation.
- For Track A: GPU is already verified in Step 0; one experiment = one screen/process = one GPU.
- Use `tee` or explicit log files so `EXPERIMENT_LOG.md` can reference them.
- Persist intermediate data under `output/experiment/data/` with documented schemas so figures are reproducible.
- Never fabricate numbers. If a run fails, record FAILED and do NOT invent a plausible result.
- Run deployment commands with `run_in_background: true` when long-running to keep the conversation responsive.
- Report back: track chosen, runs launched, where logs/artifacts are, estimated time, next step.

---

## CLAUDE.md Example

```markdown
## Remote Server
- gpu: remote
- SSH: `ssh my-gpu-server`
- GPU: 4x A100 (80GB each)
- Conda: `eval "$(/opt/conda/bin/conda shell.bash hook)" && conda activate research`
- Code dir: `/home/user/experiments/`
- code_sync: rsync          # or "git"
- wandb: false
- wandb_project: my-project
- wandb_entity: my-team

## Local Environment
- gpu: local
- Mac MPS / Linux CUDA
- Conda env: `ml` (Python 3.10 + PyTorch)

## Spatial Environment
- conda env: `geo` (geopandas, pysal, mgwr, rasterio, xarray)
- CRS default: EPSG:5070 (CONUS) / EPSG:4326 (global)
```

> **W&B**: run `wandb login` on the server once (or set `WANDB_API_KEY`). Dashboard: `https://wandb.ai/<entity>/<project>`.
