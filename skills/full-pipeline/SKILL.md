---
name: full-pipeline
description: Complete 4-stage end-to-end research pipeline. Orchestrates idea-discovery-pipeline → deploy-experiment → auto-review-loop → generate-report. Reads RESEARCH_PLAN.md (or BRIEF.md as fallback) for context that overrides $ARGUMENTS.
tools: all
argument-hint: [research-idea-description]
flags:
  COMPACT_MODE: false       # If true, read output/PROJ_NOTES.md instead of full logs to save context
---

# Skill: full-pipeline

End-to-end research pipeline. You are the pipeline conductor — you sequence the four sub-skills, check gates, and persist state across sessions.

The pipeline orchestrates exactly **four subskills**, in order:

```
idea-discovery-pipeline → deploy-experiment → auto-review-loop → generate-report
```

---

## Constants

- **AUTO_PROCEED = true** — When `true`, Gate 1 auto-selects the top-ranked idea (highest pilot signal + novelty confirmed) and continues to implementation. When `false`, always waits for explicit user confirmation before proceeding. Passed through to `/idea-discovery-pipeline`.
- **ARXIV_DOWNLOAD = false** — When `true`, `/lit-review` (inside `/idea-discovery-pipeline`) downloads the top relevant arXiv PDFs. When `false` (default), only fetches metadata via arXiv API. Passed through to `/idea-discovery-pipeline`.
- **HUMAN_CHECKPOINT = false** — When `true`, the auto-review loop (Stage 3) pauses after each round's review to let you see the score and provide custom modification instructions before fixes are implemented. When `false` (default), the loop runs fully autonomously. Passed through to `/auto-review-loop`.
- **REVIEWER_DIFFICULTY = medium** — How adversarial the reviewer is. `medium` (default): standard MCP review. `hard`: adds reviewer memory + debate protocol. `nightmare`: GPT reads the repo directly via `codex exec` + memory + debate. Passed through to `/auto-review-loop`.
- **COMPACT_MODE = false** — When `true`, prefer compact summaries (`output/PROJ_NOTES.md`, `output/experiment/EXPERIMENT_RESULT.md`) over full logs (`output/experiment/EXPERIMENT_LOG.md`, `output/AUTO_REVIEW_REPORT.md`) on session recovery. Passed through to `/auto-review-loop` and `/generate-report`.

> Override via argument, e.g., `/full-pipeline "topic" — AUTO_PROCEED: false, human checkpoint: true, difficulty: nightmare`.

---

## Startup: Load Context, Check & Resume

Before any subskill is invoked, load the project context. **All discovered files override `$ARGUMENTS`**; `$ARGUMENTS` is only the primary driver when none of the context files exist or carry usable information.

1. Read `CLAUDE.md` — project dashboard, control flags, canonical output paths.
2. Read `handoff.json` if it exists — `pipeline.stage`, `recovery.resume_skill`, `recovery.read_first`.
3. Read `memory/MEMORY.md` for the current pipeline stage and prior token usage.
4. **Load research context (priority order):**
   1. **`RESEARCH_PLAN.md`** in the project root — if present and non-empty, this is the authoritative research brief (problem, method, constraints, success criteria, prior attempts). Treat it as ground truth.
   2. **`BRIEF.md`** in the project root — if `RESEARCH_PLAN.md` is missing, read `BRIEF.md` (the 12-section research brief — see `CLAUDE.md` Key Files). Treat it as the authoritative brief.
   3. **`$ARGUMENTS`** — if neither file exists, or both are empty / contain only template placeholders, fall back to `$ARGUMENTS` as the research direction.
   4. **Both file and `$ARGUMENTS` present**: the file's details (problem, constraints, success criteria) override; `$ARGUMENTS` may sharpen scope but cannot contradict the brief. If they conflict materially, surface the conflict to the user and ask which one to follow before proceeding.
5. Read `output/REVIEW_STATE.json` if it exists — resume from saved round (see `/auto-review-loop` resume rules).
6. Read the experiment status file appropriate for `COMPACT_MODE`:
   - `COMPACT_MODE = true` → `output/PROJ_NOTES.md` and `output/experiment/EXPERIMENT_RESULT.md`
   - `COMPACT_MODE = false` → `output/experiment/EXPERIMENT_LOG.md` and `output/experiment/EXPERIMENT_RESULT.md`
7. Display the resolved context (which brief was loaded, current stage, last action) and confirm with the user before proceeding.

> 💡 If neither `RESEARCH_PLAN.md` nor `BRIEF.md` exists and `$ARGUMENTS` is also empty, stop and ask the user for a research direction or to create one of these files (templates: `templates/RESEARCH_PLAN_TEMPLATE.md`).

---

## Stage 1 — Idea Discovery (`/idea-discovery-pipeline`)

**Goal**: Identify a tractable, novel research direction and produce an experiment plan.

Invoke the subskill, passing through control flags:

```
/idea-discovery-pipeline "$ARGUMENTS"
```

The subskill internally chains: `/lit-review` → `/generate-idea` → `/novelty-check` → `/idea-review` → `/experiment-design-pipeline` (which itself runs `/refine-research` → `/experiment-design`). It will read `RESEARCH_PLAN.md` directly in its Phase 0 — do not re-paste its contents into the prompt.

**Outputs (canonical paths produced by `/idea-discovery-pipeline`):**

- `output/LIT_REVIEW_REPORT.md` — literature landscape and ranked gaps
- `output/IDEA_REPORT.md` — ranked, novelty-checked, pilot-tested ideas (top-level report)
- `output/NOVELTY_REPORT.md` — deep novelty verdicts
- `output/IDEA_REVIEW_REPORT.md` — external critical review
- `output/refine-logs/FINAL_PROPOSAL.md` + `output/refine-logs/REFINE_REPORT.md` — refined proposal
- `output/EXPERIMENT_PLAN.md` + `output/EXPERIMENT_TRACKER.md` — experiment roadmap
- `output/EXP_PIPELINE_SUMMARY.md` — pipeline summary

**Gate 1**: If `AUTO_PROCEED = false`, stop here and present the top ideas to the user:

```
📋 Idea Discovery Pipeline completed! Top ideas:

1. [Idea 1 title] — Pilot: POSITIVE (+X%), Novelty: 9/10
2. [Idea 2 title] — Pilot: WEAK POSITIVE (+Y%), Novelty: 8.3/10
3. [Idea 3 title] — Pilot: NEGATIVE, eliminated

Recommended: Idea 1. Shall I proceed with deployment?
```

The user may approve, pick a different idea, request changes (re-run the subskill with refined constraints), reject all (collect feedback, re-run), or stop and save state.

If `AUTO_PROCEED = true`, the subskill auto-selects the top idea after presenting results.

After selection, ensure the chosen idea and supporting context are recorded in `RESEARCH_PLAN.md` (template: `templates/RESEARCH_PLAN_TEMPLATE.md`) so downstream stages and future sessions inherit it.

**Path bridge before Stage 2**: `/deploy-experiment` reads `output/refine-logs/EXPERIMENT_PLAN.md` and `output/refine-logs/FINAL_PROPOSAL.md`. `/idea-discovery-pipeline` writes the plan to `output/EXPERIMENT_PLAN.md`. Before Stage 2, verify `output/refine-logs/EXPERIMENT_PLAN.md` exists; if it does not, copy `output/EXPERIMENT_PLAN.md` to that location so the deploy skill finds it. Do not relocate the original.

Update `memory/MEMORY.md`.

---

## Stage 2 — Autonomous Experiment Execution (`/deploy-experiment`)

**Goal**: Run all experiments described in the plan and collect results.

Invoke the subskill:

```
/deploy-experiment
```

The subskill will:

1. Read `output/refine-logs/EXPERIMENT_PLAN.md` (authoritative plan) and `output/refine-logs/FINAL_PROPOSAL.md` (context).
2. **Run the mandatory local GPU availability check (Step 0 of `/deploy-experiment`)** before any classification. This applies to every pilot or full experiment in this pipeline. If a local GPU (CUDA or MPS) is detected, all ML/DL runs MUST execute on it; only when `LOCAL_GPU=none` may runs route to remote/Modal/CPU.
3. Classify the experiment into Track A (ML/DL on GPU) or Track B (spatial/GIScience on CPU) — or both for mixed GeoAI.
4. Acquire data via `/data-download` if any required dataset is missing from `data/raw/`.
5. Pre-flight environment checks (GPU re-confirmed from Step 0 for Track A, package availability for Track B).
6. Launch runs (long-running jobs go to background or remote screen sessions).
6. For Track B, route execution through `/spatial-analysis` per claim.
7. Periodically invoke `/training-check` (Track A with W&B) to monitor for stalls/failures.

**Outputs (canonical paths produced by `/deploy-experiment`):**

- `output/experiment/EXPERIMENT_RESULT.md` — final per-claim results, tables, key numbers
- `output/experiment/EXPERIMENT_LOG.md` — chronological run log (commands, timings, failures)
- `output/experiment/data/` — visualization-ready artifacts (CSV, GeoPackage, predictions, metrics, sidecar metadata)
- `output/experiment/figures/` — quick-look figures
- `output/experiment/scripts/` — runner scripts created during execution

Wait for runs to finish, then confirm `EXPERIMENT_RESULT.md` and `EXPERIMENT_LOG.md` are populated before advancing.

Update `memory/MEMORY.md`.

---

## Stage 3 — Autonomous Review Loop (`/auto-review-loop`)

**Goal**: Iteratively improve work quality through adversarial review until all per-criterion floors are met and the weighted score is acceptable, or `MAX_ROUNDS = 4` is reached.

Invoke the subskill, passing the chosen idea and difficulty:

```
/auto-review-loop "[chosen idea title] — difficulty: $REVIEWER_DIFFICULTY"
```

The subskill reads `output/experiment/EXPERIMENT_RESULT.md`, `output/experiment/EXPERIMENT_LOG.md`, `output/refine-logs/FINAL_PROPOSAL.md`, and prior review state. Each round runs: independent reviewer (Codex MCP / `codex exec` / Claude subagent fallback) → parse → (optional debate in `hard`/`nightmare`) → fix verification → re-evaluate. State is persisted to `output/REVIEW_STATE.json` at every phase boundary.

**Outputs (canonical paths produced by `/auto-review-loop`):**

- `output/AUTO_REVIEW_REPORT.md` — cumulative review log (one entry per round)
- `output/review-rounds/round_<N>_raw.md` — verbatim raw reviewer responses
- `output/REVIEW_STATE.json` — per-round scores, open weaknesses, threadId, status
- `output/METHOD_DESCRIPTION.md` — concise final method description (consumed by `/paper-figure-generate` and `/paper-draft`)
- `memory/REVIEWER_MEMORY.md` (`hard` and `nightmare` only) — persistent reviewer memory across rounds
- `output/PROJ_NOTES.md` (when `COMPACT_MODE = true`) — appended one-line discoveries per round

After the loop completes, read the terminal `status` and final score from `output/REVIEW_STATE.json`:

- `status = "completed"` (POSITIVE_THRESHOLD met) → proceed to Stage 4.
- `status = "max_rounds_reached"` → proceed to Stage 4 with the remaining `open_weaknesses` flagged as limitations in the narrative.
- `status = "blocked"` (Phase B.7 circuit breaker, contract violation, or no reviewer backend) → STOP. Surface `output/CONTRACT_VIOLATION.md` (if any) and the blocker reason. Do **not** proceed to `/generate-report` until a human resolves it.

Update `memory/MEMORY.md`.

---

## Stage 4 — Report Writing (`/generate-report`)

**Goal**: Consolidate all pipeline artifacts into a single narrative rich enough to drive the downstream `paper-writing-pipeline` (paper-plan → paper-figure-generate → paper-draft → paper-review-loop → paper-convert).

Invoke the subskill (optionally with a focus hint):

```
/generate-report
```

The subskill reads, at minimum:

- `output/LIT_REVIEW_REPORT.md`
- `output/IDEA_REPORT.md` and `RESEARCH_PLAN.md` (or `BRIEF.md` if that was the active brief)
- `output/refine-logs/FINAL_PROPOSAL.md`
- `output/refine-logs/EXPERIMENT_PLAN.md`
- `output/experiment/EXPERIMENT_RESULT.md` and `output/experiment/EXPERIMENT_LOG.md`
- `output/AUTO_REVIEW_REPORT.md` and `output/REVIEW_STATE.json`
- `output/METHOD_DESCRIPTION.md`
- `output/PROJ_NOTES.md` (when `COMPACT_MODE = true`)
- `data/DATA_MANIFEST.md`, `output/spatial-analysis/`, `output/figures/` (as needed)

…and produces `output/NARRATIVE_REPORT.md` — the single source-of-truth narrative for the paper-writing pipeline.

After `/generate-report` returns, append a short pipeline summary block to `output/NARRATIVE_REPORT.md` (or write it alongside as `output/PIPELINE_SUMMARY.md`):

```markdown
# Research Pipeline Report

**Direction**: $ARGUMENTS (and/or RESEARCH_PLAN.md / BRIEF.md)
**Chosen Idea**: [title]
**Date**: [start] → [end]
**Pipeline**: idea-discovery-pipeline → deploy-experiment → auto-review-loop → generate-report

## Journey Summary
- Ideas generated: X → filtered to Y → piloted Z → chose 1
- Implementation: [brief description of what was built]
- Experiments: [number of runs, total compute time, GPU-hours]
- Review rounds: N/4, final score: X/10, status: [completed|max_rounds_reached|blocked]

## Final Status
- [ ] Ready for paper-writing-pipeline / [ ] Needs manual follow-up

## Remaining TODOs (if any)
- [items from output/REVIEW_STATE.json open_weaknesses]

## Files Changed
- [list of key files created/modified]
```

**Gate 4** (if `HUMAN_CHECKPOINT = true`): Present `output/NARRATIVE_REPORT.md` to the user for approval before handing off.

**Handoff**: Once approved, the next call in the workflow is `/paper-writing-pipeline` using `output/NARRATIVE_REPORT.md` as input.

Update `memory/MEMORY.md`.

---

## Recovery Instructions

If context overflows mid-pipeline:

1. Read `handoff.json` for `pipeline.stage`, `recovery.resume_skill`, `recovery.read_first` (fastest recovery).
2. Read `output/REVIEW_STATE.json` to find current review round and per-criterion scores (Stage 3 only).
3. Read `memory/MEMORY.md` for pipeline state flags.
4. Read `output/PROJ_NOTES.md` (when `COMPACT_MODE = true`) or `output/experiment/EXPERIMENT_LOG.md` (full).
5. Resume from the interrupted stage — do **NOT** re-run completed stages or experiments marked SUCCESS in `output/experiment/EXPERIMENT_LOG.md`.

---

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.
- **Brief precedence**: `RESEARCH_PLAN.md` > `BRIEF.md` > `$ARGUMENTS`. The first one with usable content wins; the others provide supplementary scope only.
- **Mandatory local GPU check before any pilot or full experiment.** Stage 1 (`/idea-discovery-pipeline` → `/generate-idea` Phase 5.0) and Stage 2 (`/deploy-experiment` Step 0) MUST each run the local GPU presence check (`nvidia-smi`, then MPS) before launching. If a local GPU is detected, all ML/DL runs MUST execute on it; remote/Modal/CPU is only allowed when `LOCAL_GPU=none`.
- **Gate 1 is controlled by `AUTO_PROCEED`.** When `false`, do not proceed past Stage 1 without user confirmation. When `true`, the subskill auto-selects the top idea after presenting results.
- **Stages 2–4 can run autonomously** once the user confirms the idea. This is the "sleep and wake up to results" part.
- **Respect the canonical output paths** above — do NOT relocate subskill outputs. Downstream skills (and the paper-writing pipeline) read them at fixed locations.
- **If Stage 3 ends `blocked`**, stop and surface the blocker. Do not proceed to `/generate-report` or paper writing.
- **If Stage 3 ends `max_rounds_reached`**, proceed to Stage 4 but flag remaining `open_weaknesses` as limitations.
- **Budget awareness**: Track total GPU-hours across the pipeline. Flag if approaching user-defined limits.
- **Documentation**: Every stage updates its own canonical output files. The full history must be self-contained for the next session to recover.
- **Generator-evaluator separation** (CLAUDE.md): never let the entity that wrote a section score it. `/auto-review-loop` enforces this — do not bypass it.
- **Fail gracefully**: If any stage fails (no good ideas, experiments crash, review loop blocked), report clearly and suggest alternatives rather than forcing forward.
