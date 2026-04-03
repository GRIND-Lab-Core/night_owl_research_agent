---
name: research-pipeline
description: Master 4-stage geo research pipeline. Runs: idea discovery → experiment design → autonomous spatial experiments → review loop. Call this to run the full workflow from program.md to a polished geo/RS/GIScience paper.
tools: all
flags:
  AUTO_PROCEED: false       # If true, auto-selects top idea after Stage 1 without user confirmation
  HUMAN_CHECKPOINT: true    # If true, pause after each review round in Stage 4
  COMPACT_MODE: false       # If true, read findings.md instead of full logs to save context
---

# Skill: research-pipeline

End-to-end geo research pipeline (Karpathy autoresearch + ARIS patterns). You are the pipeline conductor — you sequence sub-skills, check gates, and persist state across sessions.

---

## Startup: Check & Resume

1. Read `memory/MEMORY.md` for current pipeline stage.
2. Read `outputs/REVIEW_STATE.json` if it exists — resume from saved round.
3. Read `research_contract.md` if it exists; otherwise read `program.md`.
4. Read `findings.md` (compact) if COMPACT_MODE is true; read full `EXPERIMENT_LOG.md` otherwise.
5. Display current pipeline position and confirm with user before proceeding.

---

## Stage 1: Idea Discovery (Evening — Interactive)

**Goal**: Identify a tractable, novel research direction from the literature.

**Steps**:
1. Run skill `geo-lit-review` — retrieve ≥ 30 papers, build synthesis.
2. Run skill `idea-discovery` — generate 6-10 candidate research ideas from literature gaps.
3. Run skill `novelty-check` on each idea — eliminate incremental or already-solved ideas.
4. Select top 2-3 ideas by novelty + feasibility score.
5. For each surviving idea, run a brief pilot: call `python geo_benchmark/run_benchmark.py` with a small sample dataset to estimate signal. Budget: ≤ 3 GPU/CPU hours total.
6. Write results to `IDEA_REPORT.md` (see template at `templates/IDEA_CANDIDATES_TEMPLATE.md`).

**Gate 1**: If AUTO_PROCEED is false, stop here and ask user: "Approve top idea? (y/n/edit)".
If approved, write the selected idea to `research_contract.md` (template: `templates/RESEARCH_CONTRACT_TEMPLATE.md`).

---

## Stage 2: Experiment Design (Evening — Interactive or Autonomous)

**Goal**: Turn approved idea into a concrete, runnable experiment plan.

**Steps**:
1. Read `research_contract.md` for problem, method, success criteria.
2. Run skill `geo-experiment` in DESIGN mode — produce `EXPERIMENT_PLAN.md` (template: `templates/EXPERIMENT_PLAN_TEMPLATE.md`). Include:
   - Dataset(s) and preprocessing steps
   - Baseline models (always OLS + GWR + MGWR minimum)
   - Proposed method with parameter choices
   - Ablation variants
   - Success criteria (R² improvement, Moran's I residuals, etc.)
3. Write experiment scripts as needed, reusing existing code in `geo_benchmark/` and `agents/`.
4. Run a sanity-check experiment: smallest dataset, fastest model. Auto-debug up to 3 times if it errors.

**Gate 2** (if HUMAN_CHECKPOINT is true): Show experiment plan to user before deploying full suite.

---

## Stage 3: Autonomous Experiment Execution (Overnight — No User Needed)

**Goal**: Run all experiments and collect results.

**Steps**:
1. Run skill `geo-experiment` in EXECUTE mode — dispatch all experiments from `EXPERIMENT_PLAN.md`.
2. Periodically (every 15 min) run skill `training-check` to monitor progress.
3. On completion, run skill `spatial-analysis` to interpret results and compute all geo metrics (R², AICc, Moran's I residuals, coefficient maps).
4. Run skill `result-to-claim` — validate that result numbers support each claim in `EXPERIMENT_PLAN.md`. Remove or qualify unsupported claims.
5. Update `EXPERIMENT_LOG.md` (append results). Write one-line discoveries to `findings.md`.

---

## Stage 4: Autonomous Review Loop (Overnight → Morning)

**Goal**: Iteratively improve work quality through adversarial review until score ≥ 6/10 or 4 rounds.

**Steps**:
1. Run skill `auto-review-loop` — this handles all review rounds internally.
2. After review loop completes, read final score from `outputs/REVIEW_STATE.json`.

**If score ≥ 7.5**: Proceed to paper writing.
**If score 6–7.4**: Proceed to paper writing with noted limitations.
**If score < 6**: Ask user whether to continue with major revision or pivot.

---

## Morning: Polish & Write

1. Run skill `paper-plan` — build section outline from research_contract + findings + review feedback.
2. Run skill `paper-write` — write each section using autoresearch scoring loop (score ≥ 7.5 to accept).
3. Run skill `paper-figure` — generate spatial visualizations (maps, coefficient plots, comparison tables).
4. Run `.claude/commands/review-draft.md` for final peer review.
5. Run `.claude/commands/find-gaps.md` on your own paper to pre-empt reviewer concerns.

---

## Recovery Instructions

If context overflows mid-pipeline:
1. Read `outputs/REVIEW_STATE.json` to find current stage/round.
2. Read `memory/MEMORY.md` for pipeline state flags.
3. Read `findings.md` for compact discovery summary (COMPACT_MODE).
4. Resume from the interrupted stage — do NOT re-run completed stages.
