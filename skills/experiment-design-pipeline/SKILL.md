---
name: experiment-design-pipeline
description: 'Run an end-to-end workflow that chains the skills `refine-research` and `experiment-design`. Use when the user wants a one-shot pipeline from vague research direction to focused final proposal plus detailed experiment roadmap, or asks to build a pipeline, do it end-to-end, or generate both the method and experiment plan together.'
argument-hint: [topic-or-scope]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
---

# Experiment Design Pipeline: End-to-End Method and Experiment Planning

Refine and concretize: **$ARGUMENTS**

## Overview

Use this skill when the user does not want to stop at a refined method. The goal is to produce a coherent package that includes:

- a problem-anchored, elegant final proposal
- the review history explaining why the method is focused
- a detailed experiment roadmap tied to the paper's claims
- a compact pipeline summary that says what to run next

This skill composes two existing workflows:

1. `refine-research` for method refinement
2. `experiment-design` for claim-driven validation planning

For stage-specific detail, read these sibling skills only when needed:

- `../refine-research/SKILL.md`
- `../experiment-design/SKILL.md`

## Core Rule

Do not plan a large experiment suite on top of an unstable method. First stabilize the thesis. Then turn the stable thesis into experiments.

## Default Outputs

Refinement stage (written by `refine-research`, under `output/refine-logs/`):

- `output/refine-logs/FINAL_PROPOSAL.md`
- `output/refine-logs/REFINE_REPORT.md`
- `output/refine-logs/SCORE_HISTORY.md`
- `output/refine-logs/REFINE_STATE.json` and per-round files

Experiment stage (written by `experiment-design`, under `output/`):

- `output/EXPERIMENT_PLAN.md`
- `output/EXPERIMENT_TRACKER.md`

Pipeline integration (written by this skill):

- `output/EXP_PIPELINE_SUMMARY.md`

Do not move the subskill outputs into a different directory; downstream skills (`deploy-experiment`, `result-to-claim`, etc.) expect these canonical paths.

## Workflow

### Phase 0: Triage the Starting Point

At the very start, read the most relevant existing files if they exist (use `Read`; skip silently if missing). This mirrors the file-reading step at the start of each subskill so the pipeline never re-does stable work:

- `CLAUDE.md` — project dashboard, control flags, canonical output paths
- `handoff.json` — if present, check `pipeline.stage` and `recovery.resume_skill`
- `output/LIT_REVIEW_REPORT.md` — consolidated literature review
- `output/IDEA_REPORT.md` — ranked idea candidates
- `output/refine-logs/FINAL_PROPOSAL.md` — prior refined proposal, if any
- `output/refine-logs/REFINE_REPORT.md` — prior refinement history
- `output/refine-logs/REFINE_STATE.json` — checkpoint for an in-progress refinement
- `output/EXPERIMENT_PLAN.md` — prior experiment plan, if any

From these plus `$ARGUMENTS`, extract the problem, rough approach, constraints, resources, and target venue.

Then decide:

- If `FINAL_PROPOSAL.md` is missing, stale, or materially different from the current request, run the full `refine-research` stage.
- If a `REFINE_STATE.json` exists with `status: in_progress`, resume `refine-research` from that checkpoint rather than restarting.
- If the proposal is already strong and aligned, reuse it and jump to experiment planning.
- If in doubt, prefer re-running `refine-research` rather than planning experiments for the wrong method.

### Phase 1: Method Refinement Stage

Run the `refine-research` workflow and keep its four guiding principles intact:

- do not lose the original problem — freeze the Problem Anchor
- prefer the smallest adequate mechanism
- one paper, one dominant contribution (plus at most one supporting contribution)
- modern leverage (LLM / VLM / Diffusion / RL / distillation / inference-time scaling) is a prior, not a decoration

Respect the subskill's constants: `MAX_ROUNDS = 5`, `SCORE_THRESHOLD = 9`, `MAX_PRIMARY_CLAIMS = 2`, `MAX_CORE_EXPERIMENTS = 3`, `MAX_NEW_TRAINABLE_COMPONENTS = 2`. Do not override these from the pipeline unless the user asks.

Exit this stage only when these are explicit in `FINAL_PROPOSAL.md`:

- the final method thesis
- the dominant contribution
- the complexity intentionally rejected
- the key claims and must-run ablations
- the remaining risks, if any
- a fully populated **Experiment Design Handoff** section (hard gate inherited from `refine-research`)

If the verdict is still `REVISE`, continue into experiment planning only if the remaining weaknesses are clearly documented in `REFINE_REPORT.md`.

### Phase 2: Planning Gate

Before the experiment stage, write a short gate check:

- What is the final method thesis?
- What is the dominant contribution?
- What complexity was intentionally rejected?
- Which reviewer concerns still matter for validation?
- Is a frontier primitive central, optional, or absent?

If these answers are not crisp, tighten the final proposal first.

### Phase 3: Experiment Planning Stage

Run the `experiment-design` workflow grounded in the refinement outputs (which that skill also reads in its own Phase 0):

- `output/refine-logs/FINAL_PROPOSAL.md`
- `output/refine-logs/REFINE_REPORT.md`
- `output/LIT_REVIEW_REPORT.md` and `output/IDEA_REPORT.md` if present

Respect the subskill's constants: `MAX_PRIMARY_CLAIMS = 2`, `MAX_CORE_BLOCKS = 5`, `MAX_BASELINE_FAMILIES = 3`, `DEFAULT_SEEDS = 3`.

Ensure the experiment plan covers:

- the main anchor result
- novelty isolation
- a simplicity / elegance (deletion) check
- a frontier necessity check if a modern primitive is central (skip explicitly otherwise)
- a failure analysis or qualitative diagnosis block
- run order, compute / data budget, and decision gates
- separation of must-run vs nice-to-have

The subskill writes `output/EXPERIMENT_PLAN.md` and `output/EXPERIMENT_TRACKER.md`. Do not rewrite those files from this pipeline — only read them to build the summary.

### Phase 4: Integration Summary

Write `output/EXP_PIPELINE_SUMMARY.md`:

```markdown
# Pipeline Summary

**Problem**: [problem]
**Final Method Thesis**: [one sentence]
**Final Verdict**: [READY / REVISE / RETHINK]
**Date**: [today]

## Final Deliverables
- Proposal: `output/refine-logs/FINAL_PROPOSAL.md`
- Refinement report: `output/refine-logs/REFINE_REPORT.md`
- Score history: `output/refine-logs/SCORE_HISTORY.md`
- Experiment plan: `output/EXPERIMENT_PLAN.md`
- Experiment tracker: `output/EXPERIMENT_TRACKER.md`

## Contribution Snapshot
- Dominant contribution:
- Optional supporting contribution:
- Explicitly rejected complexity:

## Must-Prove Claims
- [Claim 1]
- [Claim 2]

## First Runs to Launch
1. [Run]
2. [Run]
3. [Run]

## Main Risks
- [Risk]:
- [Mitigation]:

## Next Action
- Proceed to `/deploy-experiment`
```

### Phase 5: Present a Brief Summary to the User

```
Pipeline complete.

Method output:
- output/refine-logs/FINAL_PROPOSAL.md
- output/refine-logs/REFINE_REPORT.md

Experiment output:
- output/EXPERIMENT_PLAN.md
- output/EXPERIMENT_TRACKER.md

Pipeline summary:
- output/EXP_PIPELINE_SUMMARY.md

Best next step:
- /deploy-experiment
```

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- Do not let the experiment plan override the Problem Anchor.
- Do not widen the paper story after method refinement unless a missing validation block is truly necessary.
- Reuse the same claims across `FINAL_PROPOSAL.md`, `EXPERIMENT_PLAN.md`, and `EXP_PIPELINE_SUMMARY.md`.
- Keep the main paper story compact.
- If the method is intentionally simple, defend that simplicity in the experiment plan rather than adding new components.
- If the method uses a modern LLM / VLM / Diffusion / RL primitive, make its necessity test explicit.
- If the method does not need a frontier primitive, say that clearly and avoid forcing one.
- Do not relocate subskill outputs. Refinement artifacts belong under `output/refine-logs/`; experiment artifacts belong directly under `output/`.
- Prefer the staged skills when the user only needs one stage; use this skill for the integrated flow.

## Composing with Other Skills

```
/experiment-design-pipeline -> one-shot method + experiment planning
/refine-research   -> method refinement only
/experiment-design   -> experiment planning only
/deploy-experiment    -> execution
```
