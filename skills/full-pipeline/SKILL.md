---
name: full-pipeline
description: Complete 5-stage research pipeline. Runs: idea discovery → experiment design → autonomous experiments → review loop → report generation. Call this to run the full workflow from program.md to a polished geo/RS/GIScience paper.
tools: all
argument-hint: [coarse-research-idea]
flags:
  COMPACT_MODE: false       # If true, read findings.md instead of full logs to save context
---

# Skill: full-pipeline

End-to-end research pipeline for $ARGUMENTS. You are the pipeline conductor — you sequence sub-skills, check gates, and persist state across sessions.

---

## Constants

- **AUTO_PROCEED = true** — When `true`, Gate 1 auto-selects the top-ranked idea (highest pilot signal + novelty confirmed) and continues to implementation. When `false`, always waits for explicit user confirmation before proceeding.
- **ARXIV_DOWNLOAD = false** — When `true`, `/research-lit` downloads the top relevant arXiv PDFs during literature survey. When `false` (default), only fetches metadata via arXiv API. Passed through to `/idea-discovery` → `/research-lit`.
- **HUMAN_CHECKPOINT = false** — When `true`, the auto-review loops (Stage 4) pause after each round's review to let you see the score and provide custom modification instructions before fixes are implemented. When `false` (default), loops run fully autonomously. Passed through to `/auto-review-loop`.
- **REVIEWER_DIFFICULTY = medium** — How adversarial the reviewer is. `medium` (default): standard MCP review. `hard`: adds reviewer memory + debate protocol. `nightmare`: GPT reads repo directly via `codex exec` + memory + debate. Passed through to `/auto-review-loop`.

> Override via argument, e.g., `/full-pipeline "topic" — AUTO_PROCEED: false, human checkpoint: true, difficulty: nightmare`.


## Startup: Check & Resume

1. Read `memory/MEMORY.md` for current pipeline stage.
2. Read `outputs/REVIEW_STATE.json` if it exists — resume from saved round.
3. Read `research_plan.md` if it exists; otherwise read `program.md`.
4. Read `findings.md` (compact) if COMPACT_MODE is true; read full `EXPERIMENT_LOG.md` otherwise.
5. Display current pipeline position and confirm with user before proceeding.

---

## Stage 1: Idea Discovery

**Goal**: Identify a tractable, novel research direction from the literature.

**Steps**:
If `research_plan.md` exists in the project root, it will be automatically loaded as detailed context (replaces one-line prompt). See `templates/RESEARCH_PLAN_TEMPLATE.md`.

Invoke the idea discovery pipeline:

```
/idea-discovery "$ARGUMENTS"
```

This internally runs: `/lit-review` → `/generate-idea` → `/novelty-check` → `/research-review`

**Output:** `idea_report.md` with ranked, validated, pilot-tested ideas. (see template at `templates/IDEA_CANDIDATES_TEMPLATE.md`).

**Gate 1**: If AUTO_PROCEED is false, stop here and present the top ideas to the user.

```
📋 Idea Discovery Pipeline completed! Top ideas:

1. [Idea 1 title] — Pilot Exp: POSITIVE (+X%), Novelty: 9/10
2. [Idea 2 title] — Pilot Exp: WEAK POSITIVE (+Y%), Novelty: 8.3/10
3. [Idea 3 title] — Pilot Exp: NEGATIVE, eliminated

Recommended: Idea 1. Shall I proceed with implementation?
```

**If AUTO_PROCEED=false:** Wait for user confirmation before continuing. The user may:
- **Approve an idea** → proceed to Stage 2.
- **Pick a different idea** → proceed with their choice.
- **Request changes** (e.g., "combine Idea 1 and 3", "focus more on X") → update the idea prompt with user feedback, re-run `/idea-discovery` with refined constraints, and present again.
- **Reject all ideas** → collect feedback on what's missing, re-run Stage 1 with adjusted research direction. Repeat until the user commits to an idea.
- **Stop here** → save current state to `idea_report.md` for future reference.

**If AUTO_PROCEED=true:** Present the top ideas, wait 10 seconds for user input. If no response, auto-select the #1 ranked idea (highest pilot signal + novelty confirmed) and proceed to Stage 2. Log: `"AUTO_PROCEED: selected Idea 1 — [title]"`.

> ⚠️ **This gate waits for user confirmation when AUTO_PROCEED=false.** When `true`, it auto-selects the top idea after presenting results. The rest of the pipeline (Stages 2-4) is expensive, so set `AUTO_PROCEED=false` if you want to manually choose which idea to pursue.

After user response, or auto proceed. write the selected idea and relevant information to `research_plan.md` (template: `templates/RESEARCH_PLAN_TEMPLATE.md`).

Update `memory/MEMORY.md`

---

## Stage 2: Experiment Design

**Goal**: Turn approved idea into a concrete, runnable experiment plan.

**Steps**:
1. Read `research_plan.md` for problem, method, experiment design, pilot code, success criteria.
2. Design the full experiment: 
   - Dataset(s) and preprocessing steps
   - Extend pilot code to full scale (multi-seed, full dataset, proper baselines)
   - Add proper evaluation metrics and logging (wandb if configured)
   - Write clean, reproducible experiment scripts
   - Follow existing codebase conventions
   - Select proper baseline models
   - Proposed method with parameter choices
   - Ablation variants
   - Success criteria 
3. Before deploying, do a self-review:
   - Are all hyperparameters configurable via argparse?
   - Is the random seed fixed and controllable?
   - Are results saved to JSON/CSV for later analysis?
   - Is there proper logging for debugging?
4. Run a sanity-check experiment: smallest dataset, fastest model. Auto-debug up to 3 times if it errors.
5. Produce `experiment_plan.md` (template: `templates/EXPERIMENT_PLAN_TEMPLATE.md`).

**Gate 2** (if HUMAN_CHECKPOINT is true): Show experiment plan to user before deploying full suite.

Update `memory/MEMORY.md`

---

## Stage 3: Autonomous Experiment Execution

**Goal**: Run all experiments and collect results.

**Steps**:
1. Run skill `deploy-experiment` in EXECUTE mode — dispatch all experiments from `experiment_plan.md`.
2. Periodically (every 15 min) run skill `monitor-progress` to monitor progress.
3. Wait for experiments to complete and collect results.
5. Update `experiment_log.md` (append results). Write discoveries to `findings.md`.

Update `memory/MEMORY.md`

---


## Stage 4: Autonomous Review Loop

**Goal**: Iteratively improve work quality through adversarial review until score ≥ 6/10 or 4 rounds.

**Steps**:
1. Invoke skill:
```
/auto-review-loop "$ARGUMENTS — [chosen idea title], difficulty: $REVIEWER_DIFFICULTY"
```
This handles all review rounds internally. What it does:
1. Subagent or external MCP server reviews the work (score, weaknesses, minimum fixes)
2. Claude Code implements fixes (code changes, new experiments, reframing)
3. Deploy fixes, collect new results
4. Re-review → repeat until score ≥ 6/10 or 4 rounds reached

After review loop completes, read final score from `outputs/review_states.json`.

**If score ≥ 7.5**: Proceed to paper writing.
**If score 6–7.4**: Proceed to paper writing with noted limitations.
**If score < 6**: Ask user whether to continue with major revision or pivot.

Update `memory/MEMORY.md`

---

## Stage 5: Report Writing

After the auto-review loop completes, write a final status report:

```markdown
# Research Pipeline Report

**Direction**: $ARGUMENTS
**Chosen Idea**: [title]
**Date**: [start] → [end]
**Pipeline**: idea-discovery → implement → run-experiment → auto-review-loop

## Journey Summary
- Ideas generated: X → filtered to Y → piloted Z → chose 1
- Implementation: [brief description of what was built]
- Experiments: [number of GPU experiments, total compute time]
- Review rounds: N/4, final score: X/10

## Final Status
- [ ] Ready for submission / [ ] Needs manual follow-up

## Remaining TODOs (if any)
- [items flagged by reviewer that weren't addressed]

## Files Changed
- [list of key files created/modified]
```

Update `memory/MEMORY.md`

---

## Recovery Instructions

If context overflows mid-pipeline:
1. Read `outputs/review_states.json` to find current stage/round.
2. Read `memory/MEMORY.md` for pipeline state flags.
3. Read `findings.md` for compact discovery summary (COMPACT_MODE).
4. Resume from the interrupted stage — do NOT re-run completed stages.


## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- **Human checkpoint after Stage 1 is controlled by AUTO_PROCEED.** When `false`, do not proceed without user confirmation. When `true`, auto-select the top idea after presenting results.
- **Stages 2-4 can run autonomously** once the user confirms the idea. This is the "sleep and wake up to results" part.
- **If Stage 4 ends at round 4 without positive assessment**, stop and report remaining issues. Do not loop forever.
- **Budget awareness**: Track total GPU-hours across the pipeline. Flag if approaching user-defined limits.
- **Documentation**: Every stage updates its own output file. The full history should be self-contained.
- **Fail gracefully**: If any stage fails (no good ideas, experiments crash, review loop stuck), report clearly and suggest alternatives rather than forcing forward.