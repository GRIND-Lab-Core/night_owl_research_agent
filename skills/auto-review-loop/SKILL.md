---
name: auto-review-loop
description: Adversarial iterative review loop. Up to 4 rounds of review (external or self), improvement, and re-evaluation. Persists state to REVIEW_STATE.json for recovery. Stop condition: score ≥ 6/10 or 4 rounds. Writes full history to AUTO_REVIEW.md.
tools: all
flags:
  HUMAN_CHECKPOINT: true    # If true, pause after each round for user approval of fixes
  COMPACT_MODE: false       # If true, use findings.md instead of full logs
  EXTERNAL_REVIEW: false    # If true, use MCP claude-review or gemini-review server
---

# Skill: auto-review-loop

You run adversarial review cycles to iteratively improve research work. Each round: review → parse → implement fixes → re-evaluate → decide.

---

## Startup: Initialize or Resume

1. Check if `REVIEW_STATE.json` exists:
   - If yes: read current round number, score, and pending_fixes. Resume from next phase.
   - If no: initialize `REVIEW_STATE.json` with round=0, score=0.
2. Check if `AUTO_REVIEW.md` exists; if not, create it with header.
3. Identify what to review: read `outputs/papers/` for sections, or `EXPERIMENT_LOG.md` for experiment results.

---

## Loop: Up to 4 Rounds

For each round (while round < 4 AND score < 6.0):

### Round Step 1: Prepare Review Context

Build the review context (use COMPACT_MODE if flag is set):
- Current work: paper sections, experiment results, claims
- Previous rounds: last entry from `AUTO_REVIEW.md`
- Research contract: `research_contract.md`

Compact context (COMPACT_MODE): use `findings.md` + latest section files only.
Full context: read all section files + `EXPERIMENT_LOG.md`.

### Round Step 2: Review

**If EXTERNAL_REVIEW is true** and MCP server is available:
- Call `claude-review` or `gemini-review` MCP tool with prepared context
- Receive structured review: score (1-10), verdict, action items

**Otherwise** (self-review using the peer-reviewer agent):
- Invoke the `.claude/agents/peer-reviewer.md` agent
- Ask for: score (1-10), top 3 must-fix items, verdict (accept/needs-work/reject)

Parse the response to extract:
- Numeric score (1-10)
- Verdict string (contains "accept", "ready", "sufficient", "needs work", "major revision", "reject")
- Action items (numbered list)

### Round Step 3: Evaluate Stop Condition

If score ≥ 6.0 AND verdict contains "accept" or "ready" or "sufficient":
- Write to AUTO_REVIEW.md: STOP — criteria met at round N with score X
- Update REVIEW_STATE.json: {"status": "complete", "final_score": score}
- Exit loop

If round == 4:
- Write to AUTO_REVIEW.md: STOP — max rounds reached
- Exit loop

### Round Step 4: Implement Fixes

For each action item, determine the fix type:
- **Write more content**: call `.claude/agents/paper-writer.md` with specific section + reviewer feedback
- **Run new experiment**: add to EXPERIMENT_PLAN.md and run skill `geo-experiment` EXECUTE mode
- **Fix spatial analysis error**: run skill `spatial-analysis` for re-interpretation
- **Add citations**: call `.claude/agents/citation-manager.md`
- **Restructure section**: call `.claude/agents/paper-writer.md` with revision directive

If HUMAN_CHECKPOINT is true: show action plan and await user confirmation before executing.

After implementing fixes, re-run affected experiments or re-score affected sections.

### Round Step 5: Persist State

Write to `REVIEW_STATE.json`:
```json
{
  "round": <N>,
  "score": <score>,
  "verdict": "<verdict>",
  "completed_fixes": ["<fix1>", "<fix2>"],
  "pending_fixes": [],
  "timestamp": "<ISO datetime>"
}
```

Append to `AUTO_REVIEW.md`:
```markdown
## Round N — Score: X/10 — <timestamp>

### Review
[Full review text]

### Action Items Implemented
1. [fix 1]
2. [fix 2]

### Score After Fixes: [re-score if applicable]
```

Increment round counter. Continue to next round.

---

## Exit Report

When loop exits, output:
```
Auto-review loop complete.
Rounds run: N/4
Final score: X/10
Verdict: <verdict>
Key improvements made: [list]

Full history: AUTO_REVIEW.md
State file: REVIEW_STATE.json

[If score < 6.0]: Recommend human review of remaining issues before proceeding.
[If score ≥ 7.5]: Ready for paper writing. Run /full-pipeline or /write-section.
```
