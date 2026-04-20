---
name: experiment-design
description: 'Turn a refined GIScience / remote sensing / spatial data science proposal into a detailed, claim-driven experiment roadmap. Use after `refine-research`, or when the user asks for a detailed experiment plan, ablation matrix, spatial evaluation protocol, run order, compute budget, or paper-ready validation that supports the core problem, novelty, simplicity, and contribution.'
argument-hint: [topic-or-scope]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
---

# Experiment Design: Claim-Driven, Paper-Oriented Validation

Refine and concretize: **$ARGUMENTS**

## Overview

Use this skill after the method is stable enough that the next question becomes: **what exact experiments should we run, in what order, to defend the paper?** If the user wants the full chain in one request, prefer `/experiment-design-pipeline`.

The skill is domain-general (AI / deep learning / ML research is fully supported) **and** must handle GIScience, remote sensing, and spatial data science research as a first-class case. When the proposal is spatial, add the spatial-specific validation layer described in *Spatial Research Addendum* below; otherwise skip it.

The goal is not to generate a giant benchmark wishlist. The goal is to turn a proposal into a **claim -> evidence -> run order** roadmap that supports four things:

1. the method actually solves the anchored problem
2. the dominant contribution is real and focused (not a confound of scale, data source, or setup choice)
3. the method is elegant enough that extra complexity is unnecessary
4. any frontier-model-era component (foundation model, VLM, diffusion, RL, geo/graph transformer, etc.) is genuinely useful, not decorative

## Constants

- **OUTPUT_DIR = `output/`** — Default destination for experiment planning artifacts.
- **MAX_PRIMARY_CLAIMS = 2** — Prefer one dominant claim plus one supporting claim.
- **MAX_CORE_BLOCKS = 5** — Keep the must-run experimental story compact.
- **MAX_BASELINE_FAMILIES = 3** — Prefer a few strong baselines over many weak ones.
- **DEFAULT_SEEDS = 3** — Use 3 seeds when stochastic variance matters and budget allows.

## Workflow

### Phase 0: Load the Proposal Context

Read the most relevant existing files first if they exist (use `Read`; skip silently if missing):

- `output/LIT_REVIEW_REPORT.md` — consolidated literature review, thematic synthesis, ranked gaps
- `output/IDEA_REPORT.md` — ranked idea candidates with pilot scores
- `output/refine-logs/FINAL_PROPOSAL.md` — refined proposal the experiments must defend
- `output/refine-logs/REFINE_REPORT.md` — round-by-round resolution log and drift record

Extract:

- **Problem Anchor** (and, if spatial, the geographic / sensor / scale scope)
- **Dominant contribution**
- **Optional supporting contribution**
- **Critical reviewer concerns** (including any spatial-validity concerns: autocorrelation, MAUP, transferability, geographic bias)
- **Data / compute / timeline constraints** (including geospatial data licensing, AOI coverage, revisit cadence, compute for large rasters / graphs)
- **Which frontier primitive is central, if any** (e.g., geo-foundation model, SAM-style segmenter, VLM, diffusion, GNN, transformer)

**If none of these files exist, focus on `$ARGUMENTS`** and derive the same information directly from the user's prompt. Do not block on missing files; do not fabricate content from files that are not present.

### Phase 1: Freeze the Paper Claims

Before proposing experiments, write down the claims that must be defended.

Use this structure:

- **Primary claim**: the main mechanism-level contribution
- **Supporting claim**: optional, only if it directly strengthens the main paper story
- **Anti-claim to rule out**: e.g. "the gain only comes from more parameters," "the gain only comes from a larger search space," or "the modern component is just decoration"
- **Minimum convincing evidence**: what would make each claim believable to a strong reviewer?

Do not exceed `MAX_PRIMARY_CLAIMS` unless the paper truly has multiple inseparable claims.

### Phase 2: Build the Experimental Storyline

Design the paper around a compact set of experiment blocks. Default to the following blocks and delete any that are not needed:

1. **Main anchor result** — does the method solve the actual bottleneck?
2. **Novelty isolation** — does the dominant contribution itself matter?
3. **Simplicity / elegance check** — can a bigger or more fragmented version be avoided?
4. **Frontier necessity check** — if an LLM / VLM / Diffusion / RL-era component is central, is it actually the right tool?
5. **Failure analysis or qualitative diagnosis** — what does the method still miss?

For each block, decide whether it belongs in:

- **Main paper** — essential to defend the core claims
- **Appendix** — useful but non-blocking
- **Cut** — interesting, but not worth the paper budget

Prefer one strong baseline family over many weak baselines. If a stronger modern baseline exists, use it instead of padding the list.

### Phase 3: Specify Each Experiment Block

For every kept block, fully specify:

- **Claim tested**
- **Why this block exists**
- **Dataset / split / task**
- **Compared systems**: strongest baselines, ablations, and variants only
- **Metrics**: decisive metrics first, secondary metrics second
- **Setup details**: backbone, frozen vs trainable parts, key hyperparameters, training budget, seeds
- **Success criterion**: what outcome would count as convincing evidence?
- **Failure interpretation**: if the result is negative, what does it mean?
- **Table / figure target**: where this result should appear in the paper

Special rules:

- A **simplicity check** should usually compare the final method against either an overbuilt variant or a tempting extra component that the paper intentionally rejects.
- A **frontier necessity check** should usually compare the chosen modern primitive against the strongest plausible simpler or older alternative.
- If the proposal is intentionally non-frontier, say so explicitly and skip the frontier block instead of forcing one.

### Phase 4: Turn the Plan Into an Execution Order

Build a realistic run order so the user knows what to do first.

Use this milestone structure:

1. **Sanity stage** — data pipeline, metric correctness, one quick overfit or toy split
2. **Baseline stage** — reproduce the strongest baseline(s)
3. **Main method stage** — run the final method on the primary setting
4. **Decision stage** — run the decisive ablations for novelty, simplicity, and frontier necessity
5. **Polish stage** — robustness, qualitative figures, appendix extras

For each milestone, estimate:

- compute cost
- expected turnaround time
- stop / go decision gate
- risk and mitigation

Separate **must-run** from **nice-to-have** experiments.

### Phase 4.5: Human Checkpoint — Data Synthesis

Honor the `HUMAN_CHECKPOINT` flag in `CLAUDE.md` (default: `true`). This skill is a planning skill, but the plan it writes commits the executor (`/deploy-experiment`) to specific data — and a few choices in this phase silently authorize *generation* of that data. When `HUMAN_CHECKPOINT` is `true`, **PAUSE** and request explicit user approval before writing any of the following into `EXPERIMENT_PLAN.md`; when `false`, log the choice to `output/PROJ_NOTES.md` and proceed.

| Trigger | Show before pausing |
|---|---|
| A block's **Dataset / split / task** entry would commit the executor to *generate* synthetic data (simulated points, bootstrapped resamples treated as new observations, GAN/LLM-generated samples, synthetic minorities) | Generator recipe, intended N, what claim it supports, and the alternative of using a real dataset |
| A block requires data that is not in `data/DATA_MANIFEST.md` and not on a public source you can name | Proposed acquisition path, fallback if acquisition fails, and whether the plan should be rewritten around available data instead |
| A claim's **Minimum convincing evidence** would be satisfied by *imputed* values (filling missing labels, pseudo-labels from a teacher model, weak supervision) | Imputation source, expected coverage, and the leakage / circularity risk if the same model produces both pseudo-labels and predictions |
| A **Spatial split** is being defined by the planner (block boundaries, buffer radius, k-means folds) rather than taken from the proposal | Why this split, sensitivity expected if it changes, and confirmation that it is not chosen to favor a particular system |
| A **Success criterion** is a number you set yourself (threshold, p-value cutoff, effect-size floor) that is not in `FINAL_PROPOSAL.md` | The number, where it came from (literature norm, defensible default, guess), and whether the user wants to fix it before runs start |

Record approved synthesis decisions in the **Risks and Mitigations** section of `EXPERIMENT_PLAN.md` so the executor inherits the rationale.

---

### Phase 5: Write the Outputs

#### Step 5.1: Write `output/EXPERIMENT_PLAN.md`

Use this structure:

```markdown
# Experiment Plan

**Problem**: [problem]
**Method Thesis**: [one-sentence thesis]
**Date**: [today]

## Claim Map
| Claim | Why It Matters | Minimum Convincing Evidence | Linked Blocks |
|-------|-----------------|-----------------------------|---------------|
| C1    | ...             | ...                         | B1, B2        |

## Paper Storyline
- Main paper must prove:
- Appendix can support:
- Experiments intentionally cut:

## Experiment Blocks

### Block 1: [Name]
- Claim tested:
- Why this block exists:
- Dataset / split / task:
- Compared systems:
- Metrics:
- Setup details:
- Success criterion:
- Failure interpretation:
- Table / figure target:
- Priority: MUST-RUN / NICE-TO-HAVE

### Block 2: [Name]
...

## Run Order and Milestones
| Milestone | Goal | Runs | Decision Gate | Cost | Risk |
|-----------|------|------|---------------|------|------|
| M0        | ...  | ...  | ...           | ...  | ...  |

## Compute and Data Budget
- Total estimated GPU-hours:
- Data preparation needs:
- Human evaluation needs:
- Biggest bottleneck:

## Risks and Mitigations
- [Risk]:
- [Mitigation]:

## Final Checklist
- [ ] Main paper tables are covered
- [ ] Novelty is isolated
- [ ] Simplicity is defended
- [ ] Frontier contribution is justified or explicitly not claimed
- [ ] Nice-to-have runs are separated from must-run runs
```

#### Step 5.2: Write `output/EXPERIMENT_TRACKER.md`

Use this structure:

```markdown
# Experiment Tracker

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics | Priority | Status | Notes |
|--------|-----------|---------|------------------|-------|---------|----------|--------|-------|
| R001   | M0        | sanity  | ...              | ...   | ...     | MUST     | TODO   | ...   |
```

Keep the tracker compact and execution-oriented.

#### Step 5.3: Present a Brief Summary to the User

```
Experiment plan ready.

Must-run blocks:
- [Block 1]
- [Block 2]

Highest-risk assumption:
- [risk]

First three runs to launch:
1. [run]
2. [run]
3. [run]

Plan file: output/EXPERIMENT_PLAN.md
Tracker file: output/EXPERIMENT_TRACKER.md
```

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- **Every experiment must defend a claim.** If it does not change a reviewer belief, cut it.
- **Prefer a compact paper story.** Design the main table first, then add only the ablations that defend it.
- **Defend simplicity explicitly.** If complexity is a concern, include a deletion study or a stronger-but-bloated variant comparison.
- **Defend frontier choices explicitly.** If a modern primitive is central, prove why it is better than the strongest simpler alternative.
- **Prefer strong baselines over long baseline lists.** A short, credible comparison set is better than a padded one.
- **Separate must-run from nice-to-have.** Do not let appendix ideas delay the core paper evidence.
- **Reuse proposal constraints.** Do not invent unrealistic budgets or data assumptions.
- **Do not fabricate results.** Plan evidence; do not claim evidence.

## Composing with Other Skills

```
/experiment-design-pipeline -> one-shot method + experiment planning
/refine-research   -> method and claim refinement
/experiment-design   -> detailed experiment roadmap
/deploy-experiment    -> execute the runs
/auto-review-loop  -> react to results and iterate on the paper
```
