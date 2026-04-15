---
name: auto-review-loop
description: Adversarial iterative review loop with generator-evaluator separation. Up to 4 rounds of independent review, improvement, and re-evaluation. Persists state to output/REVIEW_STATE.json for recovery. Stop: score ≥ 7.5/10 on all dimensions, or 4 rounds. Writes full history to output/AUTO_REVIEW_REPORT.md.
argument-hint: [topic-or-scope]
tools: all
flags:
  HUMAN_CHECKPOINT: true    # If true, pause after each round for user approval of fixes
  COMPACT_MODE: false       # If true, use output/EXPERIMENT_RESULT.md instead of full experiment logs
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
- REVIEW_DOC: `output/AUTO_REVIEW_REPORT.md` in project root (cumulative log)
- REVIEWER_MODEL = `gpt-5.4` — Preferred external reviewer via Codex MCP (OpenAI models: `gpt-5.4`, `o3`, `gpt-4o`, etc.). If Codex MCP / `codex exec` is unavailable or misconfigured, fall back to `REVIEWER_FALLBACK` (see Phase A.0).
- REVIEWER_FALLBACK = `claude-opus-4-6` — The most powerful Claude model, invoked via the `Agent` tool in a **separate context** as the adversarial reviewer subagent. Used automatically when the external LLM cannot be reached.
- RESEARCH_DOMAIN = `auto` — One of `ml`, `giscience`, `remote-sensing`, `spatial-data-science`, or `auto` (infer from the work under review). Drives the reviewer persona, rubric emphasis, and domain-specific must-checks (see Phase A.5).
- **HUMAN_CHECKPOINT = false** — When `true`, pause after each round's review (Phase B) and present the score + weaknesses to the user. Wait for user input before proceeding to Phase C. The user can: approve the suggested fixes, provide custom modification instructions, skip specific fixes, or stop the loop early. When `false` (default), the loop runs fully autonomously.
- **COMPACT = false** — When `true`, (1) read `output/EXPERIMENT_LOG.md` and `output/PROJ_NOTES.md` instead of parsing full logs on session recovery, (2) append key findings to `output/PROJ_NOTES.md` after each round.
- **REVIEWER_DIFFICULTY = medium** — Controls how adversarial the reviewer is. Three levels:
  - `medium` (default): Current behavior — MCP-based review, Claude controls what context GPT sees.
  - `hard`: Adds **Reviewer Memory** (GPT tracks its own suspicions across rounds) + **Debate Protocol** (Claude can rebut, GPT rules).
  - `nightmare`: Everything in `hard` + **GPT reads the repo directly** via `codex exec` (Claude cannot filter what GPT sees) + **Adversarial Verification** (GPT independently checks if code matches claims).

> 💡 Override: `/auto-review-loop "topic" — compact: true, human checkpoint: true, difficulty: hard`

## State Persistence (Compact Recovery)

Long-running loops may hit the context window limit, triggering automatic compaction, or crash mid-round. To survive both, persist state to `output/REVIEW_STATE.json` **at every phase boundary** (not only end-of-round):

```json
{
  "round": 2,
  "phase": "C_implementing_fixes",
  "threadId": "019cd392-...",
  "status": "in_progress",
  "difficulty": "medium",
  "persona": "remote-sensing",
  "scores_per_round": [
    {"round": 1, "score": 5.0, "verdict": "not ready"}
  ],
  "last_score": 5.0,
  "last_verdict": "not ready",
  "open_weaknesses": [
    {"id": "W1", "title": "no spatial CV", "first_seen_round": 1, "status": "open"}
  ],
  "pending_experiments": ["screen_name_1"],
  "round_started_at": "2026-03-13T21:00:00",
  "loop_started_at": "2026-03-13T18:00:00",
  "timestamp": "2026-03-13T21:14:03"
}
```

**Write rules:**
- Overwrite `output/REVIEW_STATE.json` at each phase transition (A → B → B.5 → B.6 → C → D → E). `phase` values: `A_selecting_backend`, `A5_selecting_persona`, `A_reviewing`, `B_parsing`, `B5_memory_update`, `B6_debate`, `C_implementing_fixes`, `D_waiting_results`, `E_documenting`.
- `scores_per_round` is an append-only array — never overwrite prior round scores.
- `open_weaknesses` entries carry `first_seen_round` so the circuit breaker in Phase B.7 can detect repeats.

**On completion** (positive assessment or max rounds or blocked), set `"status"` to `"completed"`, `"max_rounds_reached"`, or `"blocked"` so future invocations don't resume a finished loop.

## Budget Caps (safety valves)

Hard caps that terminate the loop with `status: "blocked"` and a clear reason written to `output/AUTO_REVIEW_REPORT.md`:

- **MAX_ROUNDS = 4** (as before)
- **MAX_WALL_CLOCK_HOURS = 6** — total elapsed from `loop_started_at` to current time. Prevents runaway overnight loops. Override via argument (`max-hours: N`).
- **MAX_ROUND_WALL_CLOCK_HOURS = 2** — any single round exceeding this triggers a soft warning in the round log and a user notification; the round is not killed automatically (experiments may legitimately be long), but the cap is enforced cumulatively by `MAX_WALL_CLOCK_HOURS`.
- **MAX_STALLED_ROUNDS = 2** — see Phase B.7.

Log `round_started_at` at the top of Phase A and compute elapsed at Phase E.


## Workflow

### Initialization

1. **Check for `output/REVIEW_STATE.json`** in project root:
   - If it does not exist: **fresh start** (normal case, identical to behavior before this feature existed)
   - If it exists AND `status` is `"completed"`: **fresh start** (previous loop finished normally)
   - If it exists AND `status` is `"in_progress"` AND `timestamp` is older than 24 hours: **fresh start** (stale state from a killed/abandoned run — delete the file and start over)
   - If it exists AND `status` is `"in_progress"` AND `timestamp` is within 24 hours: **resume**
     - Read the state file to recover `round`, `threadId`, `last_score`, `pending_experiments`
     - Read `output/AUTO_REVIEW_REPORT.md` to restore full context of prior rounds
     - If `pending_experiments` is non-empty, check if they have completed (e.g., check screen sessions)
     - Resume from the next round (round = saved round + 1)
     - Log: "Recovered from context compaction. Resuming at Round N."
2. Read project narrative documents, memory files, and any prior review documents. **When `COMPACT = true` and compact files exist**: read `output/PROJ_NOTES.md` + `output/EXPERIMENT_LOG.md` instead of full `output/AUTO_REVIEW_REPORT.md` and raw logs — saves context window.
3. Read recent experiment results (check output directories, logs)
4. Identify current weaknesses and open TODOs from prior reviews
5. Initialize round counter = 1 (unless recovered from state file)
6. Create/update `output/AUTO_REVIEW_REPORT.md` with header and timestamp

### Loop (repeat up to MAX_ROUNDS)

#### Phase A.0: Select Reviewer Backend

Before sending any review prompt, decide which backend will act as the reviewer. Probe in this order and stop at the first one that works:

1. **Codex MCP (`mcp__codex__codex`)** — preferred. Check that the MCP server is registered (e.g., entry in `.mcp.json`) and that a cheap ping call returns without an auth/config error.
2. **`codex exec` CLI** — required for `nightmare` difficulty. Check with `command -v codex` and a `--version` probe. If missing on `nightmare`, **downgrade to `hard`** and note this in `EXPERIMENT_LOG.md`.
3. **Reviewer subagent fallback** — if neither of the above is usable, fall back to **`REVIEWER_FALLBACK`** (Claude Opus 4.6) invoked through the `Agent` tool in a fresh context. This preserves generator-evaluator separation because the subagent starts cold and sees only the review package we hand it — not this session's writer context.

**How to invoke the subagent fallback:**

```
Agent({
  description: "Adversarial reviewer — round N",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: "<persona from Phase A.5> + <context package> + <scoring rubric> + <difficulty-specific instructions: memory, debate, verification>"
})
```

Rules for the fallback:

- The subagent must receive the **same instructions** the external reviewer would have received (persona, rubric, output format). Only the transport changes.
- For `hard` and `nightmare`: include the full contents of `memory/REVIEWER_MEMORY.md` in the prompt; the subagent returns an updated memory block we then persist.
- For `nightmare`: grant the subagent read access to the repo (it already has file tools) and explicitly tell it to verify claims against code/results/logs itself, without trusting the author.
- There is **no persistent `threadId`** across rounds. Simulate memory by re-pasting `memory/REVIEWER_MEMORY.md` + the last round's raw response on each invocation.
- Record which backend was used (`mcp` / `codex_exec` / `subagent`) in the round entry of `output/AUTO_REVIEW_REPORT.md` so the audit trail is explicit.

If **all three** backends fail, stop the loop and write a clear error to `output/AUTO_REVIEW_REPORT.md` + `output/REVIEW_STATE.json` (`status: "blocked"`, reason: "no reviewer backend available"). Do NOT silently self-review — that breaks generator-evaluator separation.

#### Phase A.5: Select Domain Persona and Rubric Emphasis

Pick the reviewer persona based on `RESEARCH_DOMAIN` (when `auto`, infer from the work: presence of spatial data, remote-sensing imagery, spatial statistics, GIScience theory, etc.). The persona string is injected into every Phase A prompt, whether MCP, `codex exec`, or subagent.

**Persist the selected persona** in `REVIEW_STATE.json` (`persona` field) so a resumed loop does not reclassify the domain mid-run and flip personas between rounds. On resume, read `persona` from state rather than re-inferring.

| Domain | Persona string | Target venues | Domain-specific must-checks |
|---|---|---|---|
| `ml` | "a senior ML reviewer (NeurIPS / ICML / ICLR level)" | NeurIPS, ICML, ICLR, CVPR | ablations, baselines, statistical significance, compute disclosure, seed variance |
| `giscience` | "a senior GIScience reviewer (IJGIS / TGIS / AAG level)" | IJGIS, TGIS, Annals of the AAG, CaGIS | MAUP, spatial unit justification, CRS + projection, conceptualization of space, reproducibility of spatial workflow |
| `remote-sensing` | "a senior remote-sensing reviewer (RSE / IEEE-TGRS / ISPRS level)" | RSE, IEEE TGRS, ISPRS J. of P&RS, Remote Sensing | sensor & preprocessing chain, radiometric/atmospheric correction, cloud masking, train/test geographic split, transferability across scenes, per-class metrics |
| `spatial-data-science` | "a senior spatial data science reviewer" | EPB, CEUS, Geographical Analysis, IJGIS | spatial autocorrelation reported (Moran's I / Geary's C), spatial cross-validation (not random), OLS vs spatial lag / error / GWR / MGWR comparison, residual diagnostics, effect-size maps |

**Mixed GeoAI (deep learning + spatial/RS data)**: combine the ML persona with the relevant geo persona; require BOTH sets of must-checks. Example preamble: "You are both a senior ML reviewer and a senior remote-sensing reviewer — hold this work to both bars."

When constructing Phase A prompts below, replace the placeholder `<PERSONA>` with the persona string, and append the domain-specific must-checks as an explicit checklist the reviewer must address.

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

    Please act as <PERSONA> (see Phase A.5). Apply the domain-specific
    must-checks listed there in addition to the general criteria below.

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
    [Paste full contents of memory/REVIEWER_MEMORY.md here]

    IMPORTANT: You have memory from prior rounds. Check whether your
    previous suspicions were genuinely addressed or merely sidestepped.
    The author (Claude) controls what context you see — be skeptical
    of convenient omissions.

    [Full research context, changes since last round...]

    Please act as <PERSONA> (see Phase A.5). Apply the domain-specific
    must-checks listed there in addition to the general criteria below.
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
You are <PERSONA> acting as an adversarial senior reviewer.
This is Round N/MAX_ROUNDS of an autonomous review loop.
Apply the domain-specific must-checks from Phase A.5 of the skill.

## Your Reviewer Memory (persistent across rounds)
[Paste full contents of memory/REVIEWER_MEMORY.md]

## Instructions
You have FULL READ ACCESS to this repository. The author (Claude) does NOT
control what you see — explore freely. Your job is to find problems the
author might hide or downplay.

DO THE FOLLOWING:
1. Read the experiment code, results files (JSON/CSV), and logs YOURSELF
2. Verify that reported numbers match what's actually in the output files
3. Check if evaluation metrics are computed correctly (ground truth, not model output)
4. Look for cherry-picked results, missing ablations, or suspicious hyperparameter choices
5. Read output/AUTO_REVIEW_REPORT.md for the author's claims — then verify each against code

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

**CRITICAL: Save the FULL raw response** from the external reviewer verbatim. Write it immediately to a **per-round raw file** `output/review-rounds/round_<N>_raw.md` (create the directory on first use). Do NOT paste the entire raw response into `output/AUTO_REVIEW_REPORT.md` — that file keeps a lean index + summary only (per Phase E). The per-round files are the authoritative record; the report is the navigable summary.

Then extract structured fields:
- **Score** (numeric 1-10)
- **Verdict** ("ready" / "almost" / "not ready")
- **Action items** (ranked list of fixes), each tagged with a stable `id` (W1, W2, …) so repeats across rounds can be detected by the Phase B.7 circuit breaker.

**STOP CONDITION**: If score ≥ 6 AND verdict contains "ready" or "almost" → stop loop, document final state.

#### Phase B.5: Reviewer Memory Update (hard + nightmare only)

**Skip entirely if `REVIEWER_DIFFICULTY = medium`.**

After parsing the assessment, update `memory/REVIEWER_MEMORY.md` in the project root:

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

Append the full debate transcript to `output/AUTO_REVIEW_REPORT.md` under the round's entry.

#### Phase B.7: Circuit Breakers (regression + stall detection)

Before deciding to continue, check the `scores_per_round` and `open_weaknesses` arrays in `REVIEW_STATE.json`:

1. **Score regression** — if `last_score` is **more than 0.5 points lower** than the previous round's score, write a `### Regression Warning` block to the current round's entry in `AUTO_REVIEW_REPORT.md` listing what changed since the previous round. Do NOT auto-terminate — a temporary dip is normal when addressing a real weakness — but if regression persists for two consecutive rounds, escalate: set `status: "blocked"`, reason: `"score regressed two rounds in a row"`, and stop the loop.

2. **Stalled weakness** — a weakness whose `id` appears `open` in `open_weaknesses` for **two rounds in a row** (i.e., the fix attempted in round N did not close it by round N+1) counts as stalled. If `MAX_STALLED_ROUNDS` (= 2) stalled weaknesses accumulate, escalate: set `status: "blocked"`, reason: `"recurring unresolved weaknesses: [ids]"`, and stop the loop. A stalled weakness closed in a later round resets its counter.

3. **Wall-clock cap** — if `now - loop_started_at > MAX_WALL_CLOCK_HOURS`, set `status: "blocked"`, reason: `"wall-clock budget exhausted"`, and stop.

In every `blocked` case, the termination block in `AUTO_REVIEW_REPORT.md` must list: the trigger, the offending weaknesses / score history, and a recommended next step (user review, pivot, extend budget). Do NOT silently relax thresholds — see Key Rules on contract integrity.

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

#### Phase C.5: Fix Verification (before re-review)

Before moving on to Phase D / re-review, **verify each fix actually landed** — reviewers have caught "promised but not implemented" fixes in prior projects. For every action item marked as addressed this round:

1. **File-level evidence** — record the file path + a 1-line diff summary (what changed) or the commit hash if committed. A fix with no file change is suspect: mark its weakness `status: "claimed_but_unverified"` in `open_weaknesses` rather than `closed`.
2. **Executable evidence where applicable** —
   - Code changes: ensure the file parses (`python -m py_compile <file>`) or the relevant test runs.
   - Experiment fixes: confirm a new entry exists in `output/EXPERIMENT_LOG.md` **for this round** (not an old entry being re-cited).
   - Analysis/metric additions: confirm the new metric appears in the results file the reviewer will see.
3. **Claim-to-fix map** — append to the current round's entry in `AUTO_REVIEW_REPORT.md`:

   ```markdown
   ### Fix Verification (Round N)
   | Weakness | Fix claimed | Evidence | Verified |
   |---|---|---|---|
   | W1 | Added spatial CV | spatial_cv.py (new, 42 lines) + run log round_N_spatial_cv.log | ✅ |
   | W2 | Reframed scope | paper-plan.md §1.2 rewritten | ✅ |
   | W3 | Added ablation | — no new experiment log entry found | ❌ claimed_but_unverified |
   ```

4. **Unverified fixes are NOT re-presented as "done"** in the next round's Phase A prompt — they are sent back as still-open weaknesses. This prevents the loop from gaming its own score by claiming phantom fixes.

Update `REVIEW_STATE.json` with `phase: "C5_verifying_fixes"` before this step and `phase: "D_waiting_results"` after.

#### Phase D: Wait for Results

If experiments were launched:
- Monitor remote sessions for completion
- Collect results from output files and logs
- **Training quality check** — if W&B is configured, invoke skill `training-check` to verify training was healthy (no NaN, no divergence, no plateau). If W&B not available, skip silently. Flag any quality issues in the next review round.

#### Phase E: Document Round

Append to `output/AUTO_REVIEW_REPORT.md`:

```markdown
## Round N (timestamp)

### Assessment (Summary)
- Score: X/10
- Verdict: [ready/almost/not ready]
- Key criticisms: [bullet list]

### Reviewer Raw Response

Full raw response stored at `output/review-rounds/round_<N>_raw.md` (authoritative record — verbatim, unedited). Do NOT paste it here; this report stays navigable even after many rounds. Link, don't duplicate.

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

**Write `output/REVIEW_STATE.json`** with current round, `phase: "E_documenting"`, threadId, score history (append this round's entry to `scores_per_round`), verdict, `open_weaknesses` (updated — close fixed ones, add new ones), and any pending experiments. Log `round_elapsed_hours = now - round_started_at` and surface a warning if it exceeds `MAX_ROUND_WALL_CLOCK_HOURS`.

**Append to `output/PROJ_NOTES.md`** (when `COMPACT = true`): one-line entry per key finding this round:

```markdown
- [Round N] [positive/negative/unexpected]: [one-sentence finding] (metric: X.XX → Y.YY)
```

Increment round counter → back to Phase A.

### Termination

When loop ends (positive assessment, max rounds, or `blocked` from Phase B.7 / contract violation):

1. Update `output/REVIEW_STATE.json` with terminal `status`:
   - `"completed"` — POSITIVE_THRESHOLD met
   - `"max_rounds_reached"` — hit MAX_ROUNDS without passing
   - `"blocked"` — Phase B.7 circuit breaker or contract violation
2. Write final summary to `output/AUTO_REVIEW_REPORT.md` including the score history table (from `scores_per_round`) and the final `open_weaknesses` list.
3. Update project notes (`output/PROJ_NOTES.md` when `COMPACT = true`) with conclusions.
4. **Write method/pipeline description** to a standalone file `output/METHOD_DESCRIPTION.md` — a concise 1–2 paragraph description of the final method, its architecture, and data flow. Cross-link it from `AUTO_REVIEW_REPORT.md` under a `## Method Description` section. Standalone form is required so skill `paper-figure-generate` (architecture diagrams) and skill `paper-draft` (methods section) can read it cleanly without parsing the review report.
5. **Update `handoff.json`** so the next session / next pipeline stage knows what to do:
   - `pipeline.stage` = `"review_complete"` / `"review_blocked"` / `"review_maxed"` (match terminal status)
   - `pipeline.next_step` = on success: `"invoke generate-report to consolidate into NARRATIVE_REPORT.md"`; on blocked: `"resolve blockers listed in AUTO_REVIEW_REPORT.md before resuming"`; on max rounds: `"user decides: manual revision or pivot"`
   - `recovery.resume_skill` = `"generate-report"` on success, else `"auto-review-loop"`
   - `recovery.human_checkpoint_needed` = `true` on `blocked` / `max_rounds_reached`
   - `recovery.read_first` = `["output/AUTO_REVIEW_REPORT.md", "output/METHOD_DESCRIPTION.md", "output/REVIEW_STATE.json"]`
6. If stopped at max rounds without positive assessment:
   - List remaining blockers (from `open_weaknesses`)
   - Estimate effort needed for each
   - Suggest whether to continue manually or pivot
7. If stopped `blocked`: ensure `output/CONTRACT_VIOLATION.md` (if any) is referenced in the termination block, and do NOT proceed to downstream skills (`generate-report`, `paper-writing-pipeline`) until a human resolves the blocker.


## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- ALWAYS use `config: {"model_reasoning_effort": "xhigh"}` for maximum reasoning depth
- Save threadId from first call, use `mcp__codex__codex-reply` for subsequent rounds
- **Anti-hallucination citations**: When adding references during fixes, NEVER fabricate BibTeX. Use the same DBLP → CrossRef → `[VERIFY]` chain as skill `paper-draft`: (1) `curl -s "https://dblp.org/search/publ/api?q=TITLE&format=json"` → get key → `curl -s "https://dblp.org/rec/{key}.bib"`, (2) if not found, `curl -sLH "Accept: application/x-bibtex" "https://doi.org/{doi}"`, (3) if both fail, mark with `% [VERIFY]`. Do NOT generate BibTeX from memory.
- Be honest — include negative results and failed experiments
- Do NOT hide weaknesses to game a positive score
- Implement fixes BEFORE re-reviewing (don't just promise to fix)
- **Exhaust before surrendering** — before marking any reviewer concern as "cannot address": (1) try at least 2 different solution paths, (2) for experiment issues, adjust hyperparameters or try an alternative baseline, (3) for theory issues, provide a weaker version of the result or an alternative argument, (4) only then concede narrowly and bound the damage. Never give up on the first attempt.
- **Contract integrity — never silently relax thresholds.** `POSITIVE_THRESHOLD`, `MAX_ROUNDS`, and all budget caps are fixed once the loop has started. If mid-loop you find yourself tempted to lower the passing score, redefine the verdict, mark a stalled weakness as "out of scope" to unblock the circuit breaker, or otherwise weaken the acceptance criteria to force a positive outcome — **stop and write `output/CONTRACT_VIOLATION.md`** instead. The file must record: (1) the original constraint, (2) the proposed relaxation, (3) why the loop is stuck, (4) what would legitimately resolve it. Then set `REVIEW_STATE.json` `status: "blocked"`, surface to the user, and wait for explicit approval before any threshold changes. Per CLAUDE.md Prohibited Behaviors, silently lowering experiment pass/fail criteria is forbidden; the same rule applies to review thresholds here.
- **No phantom fixes** — a weakness may only be closed in `open_weaknesses` when Phase C.5 verification succeeds. Claimed-but-unverified fixes stay open and are re-surfaced to the reviewer next round. Never mark a fix "done" based on intent alone.
- If an experiment takes > 30 minutes, launch it and continue with other fixes while waiting
- Document EVERYTHING — the review log should be self-contained
- Update project notes after each round, not just at the end

For Round 2+ prompts, use `mcp__codex__codex-reply` with the saved `threadId` (medium/hard) or re-invoke `codex exec` with reviewer memory pasted in (nightmare) — see Phase A. The prompt includes: actions taken since last round, updated results, and a request to re-score using the same format. A standalone template block is intentionally omitted to keep Phase A as the single source of truth.
