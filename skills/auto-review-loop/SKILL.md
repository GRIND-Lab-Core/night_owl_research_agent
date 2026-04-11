---
name: auto-review-loop
description: Adversarial iterative review loop with generator-evaluator separation. Up to 4 rounds of independent review, improvement, and re-evaluation. Persists state to outputs/review_state.json for recovery. Stop: score ≥ 7.5/10 on all dimensions, or 4 rounds. Writes full history to outputs/AUTO_REVIEW.md.
argument-hint: [topic-or-scope]
tools: all
flags:
  HUMAN_CHECKPOINT: true    # If true, pause after each round for user approval of fixes
  COMPACT_MODE: false       # If true, use findings.md instead of full experiment logs
  EXTERNAL_REVIEW: false    # If true, use MCP claude-review or gemini-review server
---

# Skill: auto-review-loop

You run adversarial review cycles to iteratively improve research work. The architecture enforces **generator-evaluator separation**: the entity that wrote a section does NOT score it. Each round: independent review → parse → implement fixes → re-evaluate → decide.

---

## Context: $ARGUMENTS

## Core Principle: Generator-Evaluator Separation

**Never let the same agent that wrote a section score it.**

## Constants
- MAX_ROUNDS = 4
- POSITIVE_THRESHOLD: score >= 6/10, or verdict contains "accept", "sufficient", "ready for submission"
- REVIEW_DOC: `auto_review.md` in project root (cumulative log)
- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP. Must be an OpenAI model (e.g., `gpt-5.4`, `o3`, `gpt-4o`)
- **HUMAN_CHECKPOINT = false** — When `true`, pause after each round's review (Phase B) and present the score + weaknesses to the user. Wait for user input before proceeding to Phase C. The user can: approve the suggested fixes, provide custom modification instructions, skip specific fixes, or stop the loop early. When `false` (default), the loop runs fully autonomously.
- **COMPACT = false** — When `true`, (1) read `experiment_log.md` and `findings.md` instead of parsing full logs on session recovery, (2) append key findings to `findings.md` after each round.
- **REVIEWER_DIFFICULTY = medium** — Controls how adversarial the reviewer is. Three levels:
  - `medium` (default): Current behavior — MCP-based review, Claude controls what context GPT sees.
  - `hard`: Adds **Reviewer Memory** (GPT tracks its own suspicions across rounds) + **Debate Protocol** (Claude can rebut, GPT rules).
  - `nightmare`: Everything in `hard` + **GPT reads the repo directly** via `codex exec` (Claude cannot filter what GPT sees) + **Adversarial Verification** (GPT independently checks if code matches claims).

> 💡 Override: `/auto-review-loop "topic" — compact: true, human checkpoint: true, difficulty: hard`

## State Persistence (Compact Recovery)

Long-running loops may hit the context window limit, triggering automatic compaction. To survive this, persist state to `review_state.json` after each round:

```json
{
  "round": 2,
  "threadId": "019cd392-...",
  "status": "in_progress",
  "difficulty": "medium",
  "last_score": 5.0,
  "last_verdict": "not ready",
  "pending_experiments": ["screen_name_1"],
  "timestamp": "2026-03-13T21:00:00"
}
```
**Write this file at the end of every Phase E** (after documenting the round). Overwrite each time — only the latest state matters.

**On completion** (positive assessment or max rounds), set `"status": "completed"` so future invocations don't accidentally resume a finished loop.


## Workflow

### Initialization

1. **Check for `review_state.json`** in project root:
   - If it does not exist: **fresh start** (normal case, identical to behavior before this feature existed)
   - If it exists AND `status` is `"completed"`: **fresh start** (previous loop finished normally)
   - If it exists AND `status` is `"in_progress"` AND `timestamp` is older than 24 hours: **fresh start** (stale state from a killed/abandoned run — delete the file and start over)
   - If it exists AND `status` is `"in_progress"` AND `timestamp` is within 24 hours: **resume**
     - Read the state file to recover `round`, `threadId`, `last_score`, `pending_experiments`
     - Read `auto_review.md` to restore full context of prior rounds
     - If `pending_experiments` is non-empty, check if they have completed (e.g., check screen sessions)
     - Resume from the next round (round = saved round + 1)
     - Log: "Recovered from context compaction. Resuming at Round N."
2. Read project narrative documents, memory files, and any prior review documents. **When `COMPACT = true` and compact files exist**: read `findings.md` + `experiment_log.md` instead of full `auto_review.md` and raw logs — saves context window.
3. Read recent experiment results (check output directories, logs)
4. Identify current weaknesses and open TODOs from prior reviews
5. Initialize round counter = 1 (unless recovered from state file)
6. Create/update `auto_review.md` with header and timestamp

### Loop (repeat up to MAX_ROUNDS)

#### Phase A: Review

**Route by REVIEWER_DIFFICULTY:**

##### Medium (default) — MCP Review

Send comprehensive context to the external reviewer:

```
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    [Round N/MAX_ROUNDS of autonomous review loop]

    [Full research context: claims, methods, results, known weaknesses]
    [Changes since last round, if any]

    Please act as a senior ML reviewer (NeurIPS/ICML level).

    1. Score this work 1-10 for a top venue
    2. List remaining critical weaknesses (ranked by severity)
    3. For each weakness, specify the MINIMUM fix (experiment, analysis, or reframing)
    4. State clearly: is this READY for submission? Yes/No/Almost

    Be brutally honest. If the work is ready, say so clearly.
```

If this is round 2+, use `mcp__codex__codex-reply` with the saved threadId to maintain conversation context.

##### Hard — MCP Review + Reviewer Memory

Same as medium, but **prepend Reviewer Memory** to the prompt:

```
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    [Round N/MAX_ROUNDS of autonomous review loop]

    ## Your Reviewer Memory (persistent across rounds)
    [Paste full contents of REVIEWER_MEMORY.md here]

    IMPORTANT: You have memory from prior rounds. Check whether your
    previous suspicions were genuinely addressed or merely sidestepped.
    The author (Claude) controls what context you see — be skeptical
    of convenient omissions.

    [Full research context, changes since last round...]

    Please act as a senior ML reviewer (NeurIPS/ICML level).
    1. Score this work 1-10 for a top venue
    2. List remaining critical weaknesses (ranked by severity)
    3. For each weakness, specify the MINIMUM fix
    4. State clearly: is this READY for submission? Yes/No/Almost
    5. **Memory update**: List any new suspicions, unresolved concerns,
       or patterns you want to track in future rounds.

    Be brutally honest. Actively look for things the author might be hiding.
```

##### Nightmare — Codex Exec (GPT reads repo directly)

**Do NOT use MCP.** Instead, let GPT access the repo autonomously via `codex exec`:

```bash
codex exec "$(cat <<'PROMPT'
You are an adversarial senior reviewer.
This is Round N/MAX_ROUNDS of an autonomous review loop.

## Your Reviewer Memory (persistent across rounds)
[Paste full contents of REVIEWER_MEMORY.md]

## Instructions
You have FULL READ ACCESS to this repository. The author (Claude) does NOT
control what you see — explore freely. Your job is to find problems the
author might hide or downplay.

DO THE FOLLOWING:
1. Read the experiment code, results files (JSON/CSV), and logs YOURSELF
2. Verify that reported numbers match what's actually in the output files
3. Check if evaluation metrics are computed correctly (ground truth, not model output)
4. Look for cherry-picked results, missing ablations, or suspicious hyperparameter choices
5. Read NARRATIVE_REPORT.md or AUTO_REVIEW.md for the author's claims — then verify each against code

OUTPUT FORMAT:
- Score: X/10
- Verdict: ready / almost / not ready
- Verified claims: [which claims you independently confirmed]
- Unverified/false claims: [which claims don't match the code or results]
- Weaknesses (ranked): [with MINIMUM fix for each]
- Memory update: [new suspicions and patterns to track next round]

Be adversarial. Trust nothing the author tells you — verify everything yourself.
PROMPT
)" --skip-git-repo-check 2>&1
```

**Key difference**: In nightmare mode, GPT independently reads code, result files, and logs. Claude cannot filter or curate what GPT sees. This is the closest analog to a real hostile reviewer who reads your actual paper + supplementary materials.

#### Phase B: Parse Assessment

**CRITICAL: Save the FULL raw response** from the external reviewer verbatim (store in a variable for Phase E). Do NOT discard or summarize — the raw text is the primary record.

Then extract structured fields:
- **Score** (numeric 1-10)
- **Verdict** ("ready" / "almost" / "not ready")
- **Action items** (ranked list of fixes)

**STOP CONDITION**: If score >= 6 AND verdict contains "ready" or "almost" → stop loop, document final state.

#### Phase B.5: Reviewer Memory Update (hard + nightmare only)

**Skip entirely if `REVIEWER_DIFFICULTY = medium`.**

After parsing the assessment, update `REVIEWER_MEMORY.md` in the project root:

```markdown
# Reviewer Memory

## Round 1 — Score: X/10
- **Suspicion**: [what the reviewer flagged]
- **Unresolved**: [concerns not yet addressed]
- **Patterns**: [recurring issues the reviewer noticed]

## Round 2 — Score: X/10
- **Previous suspicions addressed?**: [yes/no for each, with reviewer's judgment]
- **New suspicions**: [...]
- **Unresolved**: [carried forward + new]
```

**Rules**:
- Append each round, never delete prior rounds (audit trail)
- If the reviewer's response includes a "Memory update" section, copy it verbatim
- This file is passed back to GPT in the next round's Phase A — it is GPT's persistent brain

#### Phase B.6: Debate Protocol (hard + nightmare only)

**Skip entirely if `REVIEWER_DIFFICULTY = medium`.**

After parsing the review, Claude (the author) gets a chance to **rebut**:

**Step 1 — Claude's Rebuttal:**

For each weakness the reviewer identified, Claude writes a structured response:

```markdown
### Rebuttal to Weakness #1: [title]
- **Accept / Partially Accept / Reject**
- **Argument**: [why this criticism is invalid, already addressed, or based on a misunderstanding]
- **Evidence**: [point to specific code, results, or prior round fixes]
```

Rules for Claude's rebuttal:
- Must be honest — do NOT fabricate evidence or misrepresent results
- Can point out factual errors in the review (reviewer misread code, wrong metric, etc.)
- Can argue a weakness is out of scope or would require unreasonable effort
- Maximum 3 rebuttals per round (pick the most impactful to contest)

**Step 2 — GPT Rules on Rebuttal:**

Send Claude's rebuttal back to GPT for a ruling:

*Hard mode (MCP):*
```
mcp__codex__codex-reply:
  threadId: [saved]
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    The author rebuts your review:

    [paste Claude's rebuttal]

    For each rebuttal, rule:
    - SUSTAINED (author's argument is valid, withdraw this weakness)
    - OVERRULED (your original criticism stands, explain why)
    - PARTIALLY SUSTAINED (revise the weakness to a narrower scope)

    Then update your score if any weaknesses were withdrawn.
```

*Nightmare mode (codex exec):*
```bash
codex exec "$(cat <<'PROMPT'
You are the same adversarial reviewer. The author rebuts your review:

[paste Claude's rebuttal]

VERIFY the author's evidence claims yourself — read the files they reference.
Do NOT take their word for it.

For each rebuttal, rule:
- SUSTAINED (verified and valid)
- OVERRULED (evidence doesn't check out or argument is weak)
- PARTIALLY SUSTAINED (partially valid, narrow the weakness)

Update your score. Update your memory.
PROMPT
)" --skip-git-repo-check 2>&1
```

**Step 3 — Update score and action items** based on the ruling:
- SUSTAINED weaknesses: remove from action items
- OVERRULED: keep as-is
- PARTIALLY SUSTAINED: revise scope

Append the full debate transcript to `AUTO_REVIEW.md` under the round's entry.

#### Human Checkpoint (if enabled)

**Skip this step entirely if `HUMAN_CHECKPOINT = false`.**

When `HUMAN_CHECKPOINT = true`, present the review results and wait for user input:

```
📋 Round N/MAX_ROUNDS review complete.

Score: X/10 — [verdict]
Top weaknesses:
1. [weakness 1]
2. [weakness 2]
3. [weakness 3]

Suggested fixes:
1. [fix 1]
2. [fix 2]
3. [fix 3]

Options:
- Reply "go" or "continue" → implement all suggested fixes
- Reply with custom instructions → implement your modifications instead
- Reply "skip 2" → skip fix #2, implement the rest
- Reply "stop" → end the loop, document current state
```

Wait for the user's response. Parse their input:
- **Approval** ("go", "continue", "ok", "proceed"): proceed to Phase C with all suggested fixes
- **Custom instructions** (any other text): treat as additional/replacement guidance for Phase C. Merge with reviewer suggestions where appropriate
- **Skip specific fixes** ("skip 1,3"): remove those fixes from the action list
- **Stop** ("stop", "enough", "done"): terminate the loop, jump to Termination


#### Phase C: Implement Fixes (if not stopping)

For each action item (highest priority first):

1. **Code changes**: Write/modify experiment scripts, model code, analysis scripts
2. **Run experiments**: Deploy to GPU server via SSH + screen/tmux
3. **Analysis**: Run evaluation, collect results, update figures/tables
4. **Documentation**: Update project notes and review document

Prioritization rules:
- Skip fixes requiring excessive compute (flag for manual follow-up)
- Skip fixes requiring external data/models not available
- Prefer reframing/analysis over new experiments when both address the concern
- Always implement metric additions (cheap, high impact)

#### Phase D: Wait for Results

If experiments were launched:
- Monitor remote sessions for completion
- Collect results from output files and logs
- **Training quality check** — if W&B is configured, invoke `/training-check` to verify training was healthy (no NaN, no divergence, no plateau). If W&B not available, skip silently. Flag any quality issues in the next review round.

#### Phase E: Document Round

Append to `AUTO_REVIEW.md`:

```markdown
## Round N (timestamp)

### Assessment (Summary)
- Score: X/10
- Verdict: [ready/almost/not ready]
- Key criticisms: [bullet list]

### Reviewer Raw Response

<details>
<summary>Click to expand full reviewer response</summary>

[Paste the COMPLETE raw response from the external reviewer here — verbatim, unedited.
This is the authoritative record. Do NOT truncate or paraphrase.]

</details>

### Debate Transcript (hard + nightmare only)

<details>
<summary>Click to expand debate</summary>

**Claude's Rebuttal:**
[paste rebuttal]

**GPT's Ruling:**
[paste ruling — SUSTAINED / OVERRULED / PARTIALLY SUSTAINED for each]

**Score adjustment**: X/10 → Y/10

</details>

### Actions Taken
- [what was implemented/changed]

### Results
- [experiment outcomes, if any]

### Status
- [continuing to round N+1 / stopping]
- Difficulty: [medium/hard/nightmare]
```

**Write `REVIEW_STATE.json`** with current round, threadId, score, verdict, and any pending experiments.

**Append to `findings.md`** (when `COMPACT = true`): one-line entry per key finding this round:

```markdown
- [Round N] [positive/negative/unexpected]: [one-sentence finding] (metric: X.XX → Y.YY)
```

Increment round counter → back to Phase A.

### Termination

When loop ends (positive assessment or max rounds):

1. Update `REVIEW_STATE.json` with `"status": "completed"`
2. Write final summary to `AUTO_REVIEW.md`
3. Update project notes with conclusions
4. **Write method/pipeline description** to `AUTO_REVIEW.md` under a `## Method Description` section — a concise 1-2 paragraph description of the final method, its architecture, and data flow. This serves as input for `/paper-illustration` in Workflow 3 (so it can generate architecture diagrams automatically).
5. **Generate claims from results** — invoke `/result-to-claim` to convert experiment results from `AUTO_REVIEW.md` into structured paper claims. Output: `claims_from_results.md`. This bridges Workflow 2 → Workflow 3 so `/paper-plan` can directly use validated claims instead of extracting them from scratch. If `/result-to-claim` is not available, skip silently.
6. If stopped at max rounds without positive assessment:
   - List remaining blockers
   - Estimate effort needed for each
   - Suggest whether to continue manually or pivot


## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- ALWAYS use `config: {"model_reasoning_effort": "xhigh"}` for maximum reasoning depth
- Save threadId from first call, use `mcp__codex__codex-reply` for subsequent rounds
- **Anti-hallucination citations**: When adding references during fixes, NEVER fabricate BibTeX. Use the same DBLP → CrossRef → `[VERIFY]` chain as `/paper-write`: (1) `curl -s "https://dblp.org/search/publ/api?q=TITLE&format=json"` → get key → `curl -s "https://dblp.org/rec/{key}.bib"`, (2) if not found, `curl -sLH "Accept: application/x-bibtex" "https://doi.org/{doi}"`, (3) if both fail, mark with `% [VERIFY]`. Do NOT generate BibTeX from memory.
- Be honest — include negative results and failed experiments
- Do NOT hide weaknesses to game a positive score
- Implement fixes BEFORE re-reviewing (don't just promise to fix)
- **Exhaust before surrendering** — before marking any reviewer concern as "cannot address": (1) try at least 2 different solution paths, (2) for experiment issues, adjust hyperparameters or try an alternative baseline, (3) for theory issues, provide a weaker version of the result or an alternative argument, (4) only then concede narrowly and bound the damage. Never give up on the first attempt.
- If an experiment takes > 30 minutes, launch it and continue with other fixes while waiting
- Document EVERYTHING — the review log should be self-contained
- Update project notes after each round, not just at the end

## Prompt Template for Round 2+

```
mcp__codex__codex-reply:
  threadId: [saved from round 1]
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    [Round N update]

    Since your last review, we have:
    1. [Action 1]: [result]
    2. [Action 2]: [result]
    3. [Action 3]: [result]

    Updated results table:
    [paste metrics]

    Please re-score and re-assess. Are the remaining concerns addressed?
    Same format: Score, Verdict, Remaining Weaknesses, Minimum Fixes.
```




















- Generator: `paper-writer` agent writes content
- Evaluator: `peer-reviewer` agent scores it — invoked independently with **no shared context** with the writer
- This is enforced in Step 2 below: always route evaluation to `peer-reviewer`, never ask `paper-writer` to self-assess

If you are currently acting as a writer and are asked to evaluate, refuse and re-invoke the skill as evaluator mode.

---

## Startup: Initialize or Resume

1. Check if `handoff.json` exists — read it first for pipeline state (fast context recovery)
2. Check if `outputs/REVIEW_STATE.json` exists:
   - If yes: read current round number, score, per-criterion scores, and pending_fixes. Resume from next phase.
   - If no: initialize `outputs/REVIEW_STATE.json` with round=0, per_criterion={}, status="in_progress"
3. Check if `outputs/AUTO_REVIEW.md` exists; if not, create it with header
4. Identify what to review: read `outputs/papers/` for sections, or `EXPERIMENT_LOG.md` for experiment results

---

## Hard Per-Criterion Thresholds

**Accept only if ALL dimensions meet their floor.** A 9.5 in novelty does not compensate for a 4.0 in rigor.

| Dimension | Weight | Floor (hard threshold) | What "floor" means |
|---|---|---|---|
| Novelty | 30% | ≥ 6.5 | Contribution clearly distinguished from prior work |
| Rigor | 25% | ≥ 7.0 | OLS+GWR+MGWR compared; Moran's I reported; reproducible |
| Literature coverage | 20% | ≥ 6.5 | ≥ 15 citations, majority ≥ 2020, key GeoAI/soundscape papers cited |
| Clarity | 15% | ≥ 6.0 | Active voice; specific numbers; no "may", "could", "might" claims |
| Impact | 10% | ≥ 6.0 | Practical application or scientific significance stated |

**Weighted average threshold:** ≥ 7.5 overall AND all floors met.

If any single floor is missed, the verdict is **not acceptable** regardless of weighted average.

---

## Few-Shot Score Calibration

Use these anchors to calibrate scores consistently. Read them before scoring.

### Score 6.0 / 10 (Needs Work)
> Methodology section describes GWR but does not report MGWR or compare the two. Moran's I of residuals is mentioned but the value is not given. Seven of 12 citations are older than 2019. The problem statement uses passive voice throughout and does not specify which cities are studied. Generation fidelity metrics (FID, SSIM) are mentioned but their values are not reported numerically.
- Rigor floor MISSED (no MGWR, no Moran's I value)
- Literature floor MISSED (too many old citations)
- Would score: Novelty 7.0, Rigor 4.5, Literature 5.5, Clarity 5.0, Impact 6.5 → average ~5.7

### Score 7.5 / 10 (Acceptable — Minimum Bar)
> Methodology section runs OLS, GWR, and MGWR on NYC, London, Singapore data. Reports R² (OLS 0.43, GWR 0.61, MGWR 0.67) and Moran's I of MGWR residuals (0.08, p=0.12, not significant — spatial autocorrelation removed). Cites 16 papers, 13 from 2020–2025 including ControlNet (Zhang 2023), ImageBind (Girdhar 2023), CLAP (LAION 2022). Uses active voice. FID = 42.3 reported. One limitation: GWI (Green View Index) is described but its contribution to FID is not ablated.
- All floors met (barely)
- Weighted average ≈ 7.5

### Score 9.0 / 10 (Strong — Target Quality)
> Methodology clearly positions contribution against three prior systems (sound2sight, UrbanCLIP, GeoGen) with head-to-head FID/SSIM/LPIPS table. OLS R²=0.43, GWR R²=0.61, MGWR R²=0.67 across all three cities; Moran's I = 0.08 (p=0.12). MGWR local coefficient maps reveal that sky-view factor matters more in Singapore (β̄=0.41) than London (β̄=0.19). All 22 citations ≥ 2019; 7 from ISPRS/IEEE-TGRS/CEUS venues. Ablation: removing soundscape conditioning drops FID by 18.3 points. Each figure has scale bar, north arrow, CRS label, inset locator.
- All floors exceeded
- Novelty 9.5, Rigor 9.0, Literature 9.0, Clarity 8.5, Impact 8.5 → average ~9.0

---

## Loop: Up to 4 Rounds

For each round (while round < 4 AND NOT all_floors_met AND weighted_avg < 7.5):

### Round Step 1: Prepare Review Context

Build the review context (**evaluator does NOT read generator's working notes**):
- Current work: the specific section file(s) being reviewed
- Previous round scores: last entry from `outputs/AUTO_REVIEW.md` (scores only, not writer's reasoning)
- Research contract: `research_contract.md` (ground truth for what was promised)
- Approved claims: `memory/approved_claims.md` (to check if claims are grounded)

COMPACT_MODE: use `findings.md` + latest section files only (not full EXPERIMENT_LOG).
Full context: read section files + `memory/approved_claims.md`.

**Do NOT include**: writer's draft notes, prior writer context, or any information that blurs generator/evaluator separation.

### Round Step 2: Evaluate (Independent Evaluator)

**Always use peer-reviewer agent as evaluator — never self-review.**

Invoke `.claude/agents/peer-reviewer.md` with this exact instruction:
```
Score each dimension independently using the calibration anchors in auto-review-loop/SKILL.md.
For each dimension, state: score (0–10), floor (from skill), pass/fail, and one specific improvement required.
Report: weighted average, whether all floors are met, and verdict (accept/revise/reject).
```

The peer-reviewer MUST return a structured response:
```
Novelty:             X.X / 10 (floor 6.5) — PASS/FAIL — [specific improvement]
Rigor:               X.X / 10 (floor 7.0) — PASS/FAIL — [specific improvement]
Literature coverage: X.X / 10 (floor 6.5) — PASS/FAIL — [specific improvement]
Clarity:             X.X / 10 (floor 6.0) — PASS/FAIL — [specific improvement]
Impact:              X.X / 10 (floor 6.0) — PASS/FAIL — [specific improvement]
Weighted average:    X.X / 10
All floors met:      YES / NO
Verdict:             ACCEPT / NEEDS REVISION / REJECT
Top 3 must-fix items:
1. [specific, actionable fix with target dimension]
2. [specific, actionable fix with target dimension]
3. [specific, actionable fix with target dimension]
```

If EXTERNAL_REVIEW is true and MCP server is available: call `claude-review` or `gemini-review` with the same instruction; parse the structured response.

### Round Step 3: Evaluate Stop Condition

Parse the reviewer response to extract per-criterion scores and floors.

**ACCEPT if:**
- Weighted average ≥ 7.5 AND
- All five dimension floors are met

**CONTINUE if:**
- Any floor is missed OR weighted average < 7.5
- AND round < 4

**FORCE STOP if:**
- round == 4 (max rounds reached, even if not accepted)

On ACCEPT: write to `outputs/AUTO_REVIEW.md`: `STOP — accepted at round N, score X.X/10, all floors met`
Update `outputs/REVIEW_STATE.json`: `{"status": "complete", "final_score": X.X, "all_floors_met": true}`

On FORCE STOP: write to `outputs/AUTO_REVIEW.md`: `STOP — max rounds reached, score X.X/10 — human review required`
Update `outputs/REVIEW_STATE.json`: `{"status": "max_rounds", "final_score": X.X}`

### Round Step 4: Implement Fixes (Generator)

Focus only on dimensions that failed their floor or are below 7.5.

For each must-fix item, route to the appropriate generator:
- **Write more content / restructure**: call `.claude/agents/paper-writer.md` with section + specific reviewer feedback + calibration target
- **Run new experiment or ablation**: add to `EXPERIMENT_PLAN.md` and run skill `geo-experiment` EXECUTE mode
- **Fix spatial analysis**: run skill `spatial-analysis` for re-interpretation and Moran's I
- **Add or fix citations**: call `.claude/agents/citation-manager.md` with APA 7th edition format
- **Fix figures**: run skill `paper-figure` with corrected cartographic conventions

If HUMAN_CHECKPOINT is true: show action plan (what will be fixed, by which agent) and await user confirmation before executing.

After implementing fixes, re-evaluate only the fixed dimensions (not all five) to verify improvement.

### Round Step 5: Persist State

Write to `outputs/REVIEW_STATE.json`:
```json
{
  "round": <N>,
  "score": <weighted_average>,
  "per_criterion": {
    "novelty": {"score": X.X, "floor": 6.5, "pass": true|false},
    "rigor": {"score": X.X, "floor": 7.0, "pass": true|false},
    "literature": {"score": X.X, "floor": 6.5, "pass": true|false},
    "clarity": {"score": X.X, "floor": 6.0, "pass": true|false},
    "impact": {"score": X.X, "floor": 6.0, "pass": true|false}
  },
  "all_floors_met": true|false,
  "verdict": "<verdict>",
  "completed_fixes": ["<fix1>", "<fix2>"],
  "pending_fixes": [],
  "timestamp": "<ISO datetime>",
  "status": "in_progress"
}
```

Append to `outputs/AUTO_REVIEW.md`:
```markdown
## Round N — Weighted avg: X.X/10 — <timestamp>

### Per-Criterion Scores
| Dimension | Score | Floor | Status |
|---|---|---|---|
| Novelty | X.X | 6.5 | PASS/FAIL |
| Rigor | X.X | 7.0 | PASS/FAIL |
| Literature | X.X | 6.5 | PASS/FAIL |
| Clarity | X.X | 6.0 | PASS/FAIL |
| Impact | X.X | 6.0 | PASS/FAIL |

### Must-Fix Items
1. [fix 1]
2. [fix 2]

### Fixes Implemented
1. [what was done]
2. [what was done]

### Post-fix Re-score (dimensions that changed)
- Rigor: 5.5 → 7.2 (PASS)
```

Increment round counter. Continue to next round.

---

## Exit Report

When loop exits, output:
```
Auto-review loop complete.
Rounds run: N/4
Weighted average: X.X/10
Floors met: [list which passed/failed]
All floors met: YES/NO
Verdict: ACCEPTED / NOT ACCEPTED — human review required

Key improvements made:
- [improvement 1]
- [improvement 2]

Full history: outputs/AUTO_REVIEW.md
State file: outputs/REVIEW_STATE.json

[If not accepted]: The following dimensions are below floor — do not proceed to final submission:
  - [Dimension]: X.X (floor Y.Y) — [specific remaining issue]

[If accepted]: Ready for references compilation. Run /write-section references.
```
