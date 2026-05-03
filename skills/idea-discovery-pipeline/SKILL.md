---
name: idea-discovery-pipeline
description: The full pipeline for idea generation. It generates 8-12 novel research ideas from literature gaps and evaluates each on novelty, feasibility, and domain fit. Orchestrates lit-review → generate-idea → novelty-check → idea-review → experiment-design-pipeline to go from a broad research direction to a validated, pilot-tested idea with a refined proposal and experiment plan. Produces output/IDEA_REPORT.md plus refinement and experiment artifacts.
argument-hint: [research-direction]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill
---

# Skill: idea-discovery-pipeline

You are the orchestrator for a complete idea discovery workflow for: **$ARGUMENTS**

---

## Overview

This skill chains sub-skills into a single automated pipeline:

```
/lit-review → /generate-idea → /novelty-check → /idea-review → /experiment-design-pipeline
```

Each phase builds on the previous one's output. The final deliverables are:

- `output/LIT_REVIEW_REPORT.md` — literature landscape and ranked gaps
- `output/IDEA_REPORT.md` — ranked, validated, pilot-tested ideas (the top-level report)
- `output/NOVELTY_REPORT.md` — deep novelty verdicts for top ideas
- `output/IDEA_REVIEW_REPORT.md` — external critical review of the top idea
- `output/refine-logs/FINAL_PROPOSAL.md` + `output/refine-logs/REFINE_REPORT.md` — refined proposal
- `output/EXPERIMENT_PLAN.md` + `output/EXPERIMENT_TRACKER.md` — experiment roadmap
- `output/EXP_PIPELINE_SUMMARY.md` — pipeline summary from experiment-design-pipeline

## Constants

- **PILOT_MAX_HOURS = 2** — Skip any pilot experiment estimated to take > 2 hours per GPU. Flag as "needs manual pilot" in the report.
- **PILOT_TIMEOUT_HOURS = 3** — Hard timeout: kill any running pilot that exceeds 3 hours. Collect partial results if available.
- **MAX_PILOT_IDEAS = 3** — Run pilots for at most 3 top ideas in parallel. Additional ideas are validated on paper only.
- **MAX_TOTAL_GPU_HOURS = 8** — Total GPU budget across all pilots. If exceeded, skip remaining pilots and note in report.
- **AUTO_PROCEED = true** — If user doesn't respond at a checkpoint, automatically proceed with the best option after presenting results. Set to `false` to always wait for explicit user confirmation.
- **REVIEWER_MODEL = `gpt-5.4`** — Model used via Codex MCP. Must be an OpenAI model (e.g., `gpt-5.4`, `o3`, `gpt-4o`). Passed to sub-skills. If not configured properly, use Claude Code subagent.
- **ARXIV_DOWNLOAD = false** — When `true`, `/lit-review` downloads the top relevant arXiv PDFs during Phase 1. When `false` (default), only fetches metadata. Passed through to `/lit-review`.
- **COMPACT = false** — When `true`, generate compact summary files for short-context models and session recovery. Writes `output/IDEA_CANDIDATES.md` (top 3-5 ideas only) at the end of this workflow. Downstream skills read this instead of the full `output/IDEA_REPORT.md`.
- **REF_PAPER = false** — Reference paper to base ideas on. Accepts: local PDF path, arXiv URL, or any paper URL. When set, the paper is summarized first (`output/REF_PAPER_SUMMARY.md`), then idea generation uses it as context. Combine with `base repo` for "improve this paper with this codebase" workflows.

> 💡 These are defaults. Override by telling the skill, e.g., `/idea-discovery-pipeline "topic" — ref paper: https://arxiv.org/abs/2406.04329` or `/idea-discovery-pipeline "topic" — compact: true`.

## Pipeline

### Phase 0: Load Context and Research Plan

At the very start, read the most relevant existing files if they exist (use `Read`; skip silently if missing). This mirrors the Phase 0 pattern used by each subskill and ensures the pipeline never re-does stable work:

- `CLAUDE.md` — project dashboard, control flags, canonical output paths
- `handoff.json` — if present, check `pipeline.stage` and `recovery.resume_skill`
- `RESEARCH_PLAN.md` in the project root (or path passed as `$ARGUMENTS`) — detailed research brief
- `output/LIT_REVIEW_REPORT.md` — prior literature review, if any
- `output/IDEA_REPORT.md` — prior idea candidates, if any
- `output/NOVELTY_REPORT.md` — prior novelty verdicts, if any
- `output/IDEA_REVIEW_REPORT.md` — prior external review, if any
- `output/REF_PAPER_SUMMARY.md` — prior reference paper summary, if any
- `output/refine-logs/FINAL_PROPOSAL.md` — prior refined proposal, if any

If `RESEARCH_PLAN.md` is found, extract:

- Problem statement and context
- Constraints (compute, data, timeline, venue)
- What the user already tried / what didn't work
- Domain knowledge and non-goals
- Existing results (if any)

Use this as the primary context for all subsequent phases — it replaces the one-line prompt. If both `RESEARCH_PLAN.md` and a one-line `$ARGUMENTS` exist, merge them (the plan takes priority for details; the argument sets the direction). If no plan exists, proceed with `$ARGUMENTS` as the research direction.

Decide whether to resume from a prior stage or re-run:

- If a prior artifact is stale or materially different from the current request, re-run that phase.
- If it is strong and aligned, reuse it and jump to the next phase.
- When in doubt, prefer re-running over planning on top of the wrong idea.

> 💡 Create a plan from the template: `cp templates/RESEARCH_PLAN_TEMPLATE.md RESEARCH_PLAN.md`

### Phase 0.5: Reference Paper Summary (when REF_PAPER is set)

**Skip entirely if `REF_PAPER` is `false`.**

Summarize the reference paper before searching the literature:

1. **If arXiv URL** (e.g., `https://arxiv.org/abs/2406.04329`):
   - Invoke `/arxiv "ARXIV_ID" — download` to fetch the PDF
   - Read the first 5 pages (title, abstract, intro, method overview)

2. **If local PDF path** (e.g., `papers/reference.pdf`):
   - Read the PDF directly (first 5 pages)

3. **If other URL**:
   - Fetch and extract content via WebFetch

4. **Generate `output/REF_PAPER_SUMMARY.md`** (canonical path — use this everywhere):

```markdown
# Reference Paper Summary

**Title**: [paper title]
**Authors**: [authors]
**Venue**: [venue, year]

## What They Did
[2-3 sentences: core method and contribution]

## Key Results
[Main quantitative findings]

## Limitations & Open Questions
[What the paper didn't solve, acknowledged weaknesses, future work suggestions]

## Potential Improvement Directions
[Based on the limitations, what could be improved or extended?]

## Codebase
[If `base repo` is also set: link to the repo and note which parts correspond to the paper]
```

**🚦 Checkpoint:** Present the summary to the user:

```
📄 Reference paper summarized:
- Title: [title]
- Key limitation: [main gap]
- Improvement directions: [2-3 bullets]

Proceeding to literature survey with this as context.
```

Phase 1 and Phase 2 will use `output/REF_PAPER_SUMMARY.md` as additional context — `/lit-review` searches for related and competing work, `/generate-idea` generates ideas that build on or improve the reference paper.

### Phase 1: Literature Review

Invoke skill `/lit-review` to map the research landscape:

```
/lit-review "$ARGUMENTS"
```

**What this does** (per the `lit-review` subskill):

- Searches local sources first (`papers/`, Zotero, Obsidian) when configured, then arXiv via `tools/arxiv_fetch.py`, Semantic Scholar via `tools/semantic_scholar_fetch.py`, and WebSearch (arXiv, Google Scholar, Semantic Scholar)
- Builds a synthesis matrix and gap analysis
- Writes paper metadata to `output/paper-cache/`
- Writes the consolidated report to `output/LIT_REVIEW_REPORT.md` (Findings, Synthesis, Gap Analysis sections)

Pass `ARXIV_DOWNLOAD` through if the user overrode it.

**🚦 Checkpoint:** Present the landscape summary from `output/LIT_REVIEW_REPORT.md` to the user:

```
📚 Literature survey complete. Here's what I found:
- [key findings, gaps, open problems]

Does this match your understanding? Should I adjust the scope before generating ideas?
(If no response, I'll proceed with the top-ranked direction.)
```

- **User approves** (or no response + AUTO_PROCEED=true) → proceed to Phase 2 with best direction.
- **User requests changes** (e.g., "focus more on X", "ignore Y", "too broad") → refine the search with updated queries, re-run `/lit-review` with adjusted scope, and present again. Repeat until the user is satisfied.

### Phase 2: Idea Generation + Filtering + Pilots

Invoke `/generate-idea` with the landscape context (and `output/REF_PAPER_SUMMARY.md` if available):

```
/generate-idea "$ARGUMENTS"
```

**What this does** (per the `generate-idea` subskill):

- Reads `output/LIT_REVIEW_REPORT.md` (if present) and skips its own Phase 1 silently
- Reads `output/REF_PAPER_SUMMARY.md` if present — ideas should build on, improve, or extend the reference paper
- Brainstorms 8-12 concrete ideas
- Filters by feasibility, compute cost, quick novelty search
- Deep-validates top ideas (quick novelty pass + devil's advocate)
- Runs pilot experiments on available GPUs (top `MAX_PILOT_IDEAS`, respecting `MAX_TOTAL_GPU_HOURS` and `PILOT_TIMEOUT_HOURS`)
- Ranks by empirical signal
- Writes `output/IDEA_REPORT.md`

**🚦 Checkpoint:** Present the ranked ideas from `output/IDEA_REPORT.md`:

```
💡 Generated X ideas, filtered to Y, piloted Z. Top results:

1. [Idea 1] — Pilot: POSITIVE (+X%)
2. [Idea 2] — Pilot: WEAK POSITIVE (+Y%)
3. [Idea 3] — Pilot: NEGATIVE, eliminated

Which ideas should I validate further? Or should I regenerate with different constraints?
(If no response, I'll proceed with the top-ranked ideas.)
```

- **User picks ideas** (or no response + AUTO_PROCEED=true) → proceed to Phase 3 with top-ranked ideas.
- **User unhappy with all ideas** → collect feedback ("what's missing?", "what direction do you prefer?"), update the prompt with user's constraints, re-run Phase 2. Repeat until the user selects at least 1 idea.
- **User wants to adjust scope** → go back to Phase 1 with refined direction.

### Phase 3: Deep Novelty Verification

Invoke `/novelty-check` to run a thorough novelty check on the top candidates:

```
/novelty-check "$ARGUMENTS"
```

**What this does** (per the `novelty-check` subskill):

- Reads `output/IDEA_REPORT.md` (preferred) and runs the remaining phases **per idea** for the top-ranked candidates; treats `$ARGUMENTS` as a topic filter
- Reuses abstracts from `output/paper-cache/` and `papers/` where available
- Runs multi-source literature search (arXiv, Semantic Scholar, WebSearch) and cross-verifies with `REVIEWER_MODEL`
- Checks for concurrent work in the last 3-6 months and identifies closest existing work plus differentiation points
- Writes `output/NOVELTY_REPORT.md`
- **Updates `output/IDEA_REPORT.md`** in place with each idea's novelty verdict and score

Eliminate any idea that turns out to be already published.

### Phase 4: External Critical Review

For the surviving top idea(s), get brutal feedback. The underlying skill is `idea-review/`

```
/idea-review "[top idea with hypothesis + pilot results]"
```

**What this does** (per the `idea-review` subskill):

- `REVIEWER_MODEL` (xhigh reasoning via Codex MCP) acts as a senior reviewer
- Runs a multi-round critical dialogue, scores the idea, identifies weaknesses, suggests minimum viable improvements
- Provides concrete feedback on experimental design
- Writes `output/IDEA_REVIEW_REPORT.md`

**Update `output/IDEA_REPORT.md`** with the reviewer feedback and revised plan.

### Phase 4.5: Method Refinement + Experiment Planning

After review, refine the top idea into a concrete proposal and plan experiments by invoking the wrapper pipeline:

```
/experiment-design-pipeline "[top idea description + pilot results + reviewer feedback]"
```

**What this does** (per the `experiment-design-pipeline` skill, which chains `refine-research` then `experiment-design`):

- Freezes a **Problem Anchor** and preserves it across rounds
- Iteratively refines the method via `REVIEWER_MODEL` review (up to 5 rounds, target score ≥ 9), respecting the subskill's constants (`MAX_PRIMARY_CLAIMS = 2`, `MAX_NEW_TRAINABLE_COMPONENTS = 2`, etc.)
- Generates a claim-driven experiment roadmap with ablations, budgets, and run order
- Outputs:
  - Refinement: `output/refine-logs/FINAL_PROPOSAL.md`, `output/refine-logs/REFINE_REPORT.md`, `output/refine-logs/SCORE_HISTORY.md`
  - Experiments: `output/EXPERIMENT_PLAN.md`, `output/EXPERIMENT_TRACKER.md`
  - Pipeline summary: `output/EXP_PIPELINE_SUMMARY.md`

Do not relocate these artifacts — downstream skills (`deploy-experiment`, `result-to-claim`, etc.) expect these canonical paths.

**🚦 Checkpoint:** Present the refined proposal summary:

```
🔬 Method refined and experiment plan ready:
- Problem anchor: [anchored problem]
- Method thesis: [one sentence]
- Dominant contribution: [what's new]
- Must-run experiments: [N blocks]
- First 3 runs to launch: [list]

Proceed to implementation? Or adjust the proposal?
```

- **User approves** (or AUTO_PROCEED=true) → proceed to Final Report.
- **User requests changes** → pass feedback to `/refine-research` for another round, then re-run `/experiment-design` if needed.
- **Lite mode:** If reviewer score < 6 or the pilot was weak, run `/refine-research` only (skip `/experiment-design`) and note remaining risks in the report.

### Phase 5: Final Report

Finalize `output/IDEA_REPORT.md` with all accumulated information:

```markdown
# Idea Discovery Report

**Direction**: $ARGUMENTS
**Date**: [today]
**Pipeline**: lit-review → generate-idea → novelty-check → idea-review → experiment-design-pipeline

## Executive Summary
[2-3 sentences: best idea, key evidence, recommended next step]

## Literature Landscape
[from Phase 1 — see output/LIT_REVIEW_REPORT.md]

## Ranked Ideas
[from Phase 2, updated with Phase 3-4 results]

### 🏆 Idea 1: [title] — RECOMMENDED
- Pilot: POSITIVE (+X%)
- Novelty: CONFIRMED (closest: [paper], differentiation: [what's different])
- Reviewer score: X/10
- Next step: implement full experiment → /deploy-experiment

### Idea 2: [title] — BACKUP
...

## Eliminated Ideas
[ideas killed at each phase, with reasons]

## Refined Proposal
- Proposal: `output/refine-logs/FINAL_PROPOSAL.md`
- Refinement report: `output/refine-logs/REFINE_REPORT.md`
- Experiment plan: `output/EXPERIMENT_PLAN.md`
- Experiment tracker: `output/EXPERIMENT_TRACKER.md`
- Pipeline summary: `output/EXP_PIPELINE_SUMMARY.md`

## Supporting Reports
- Literature: `output/LIT_REVIEW_REPORT.md`
- Novelty: `output/NOVELTY_REPORT.md`
- External review: `output/IDEA_REVIEW_REPORT.md`

## Next Steps
- [ ] /deploy-experiment to deploy experiments from the plan
- [ ] /auto-review-loop to iterate until submission-ready
- [ ] Or invoke /full-pipeline for the complete end-to-end flow
```

### Phase 5.5: Write Compact Files (when COMPACT = true)

**Skip entirely if `COMPACT` is `false`.**

Write `output/IDEA_CANDIDATES.md` — a lean summary of the top 3-5 surviving ideas:

```markdown
# Idea Candidates

| # | Idea | Pilot Signal | Novelty | Reviewer Score | Status |
|---|------|-------------|---------|---------------|--------|
| 1 | [title] | +X% | Confirmed | X/10 | RECOMMENDED |
| 2 | [title] | +Y% | Confirmed | X/10 | BACKUP |
| 3 | [title] | Negative | — | — | ELIMINATED |

## Active Idea: #1 — [title]
- Hypothesis: [one sentence]
- Key evidence: [pilot result]
- Next step: /experiment-design-pipeline or /deploy-experiment
```

This file is intentionally small (~30 lines) so downstream skills and session recovery can read it without loading the full `output/IDEA_REPORT.md` (~200+ lines).

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- **Don't skip phases.** Each phase filters and validates — skipping leads to wasted effort later.
- **Checkpoint between phases.** Briefly summarize what was found before moving on.
- **Mandatory local GPU check before pilots.** Phase 2 delegates pilot launch to `/generate-idea`, which MUST run its Phase 5.0 local GPU presence check (`nvidia-smi` → CUDA, else MPS, else `LOCAL_GPU=none`). When a local GPU is detected, every pilot in this pipeline MUST run on it — never fall back to CPU and never silently re-route to remote/Modal while a local GPU is available.
- **Kill ideas early.** It's better to kill 10 bad ideas in Phase 3 than to implement one and fail.
- **Empirical signal > theoretical appeal.** An idea with a positive pilot outranks a "sounds great" idea without evidence.
- **Document everything.** Dead ends are just as valuable as successes for future reference.
- **Be honest with the reviewer.** Include negative results and failed pilots in the review prompt.
- **Do not relocate subskill outputs.** Literature, idea, novelty, and review reports live directly under `output/`. Refinement artifacts live under `output/refine-logs/`. Experiment artifacts live directly under `output/`.
- **Reuse, don't duplicate.** If a subskill already reads a canonical file (e.g., `generate-idea` reads `output/LIT_REVIEW_REPORT.md`, `novelty-check` reads `output/IDEA_REPORT.md`), do not re-inject that content as a large prompt — let the subskill read it.

## Composing with Workflow 2

After this pipeline produces a validated top idea:

```
/idea-discovery-pipeline "direction"   ← you are here (Workflow 1, includes method refinement + experiment planning)
/deploy-experiment                      ← deploy experiments from the plan
/auto-review-loop "top idea"            ← Workflow 2: iterate until submission-ready

Or use /full-pipeline for the full end-to-end flow.
```
