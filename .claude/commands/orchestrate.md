---
name: orchestrate
description: "Launch the orchestrator sub-agent to run the full research pipeline end-to-end. The orchestrator reads program.md, manages state across all 7 stages (literature → synthesis → gaps → hypotheses → outline → writing → references), delegates to specialist sub-agents, and produces a final paper. Usage: /orchestrate [resume|status]"
---

# Command: /orchestrate

Launches the `orchestrator` sub-agent as a delegated agent with full tool access. The orchestrator reads program.md, manages pipeline state, sequences all specialist sub-agents, and produces a publication-ready paper.

---

## Usage

```
/orchestrate           — start or resume the pipeline from current state
/orchestrate resume    — explicitly resume from saved state in memory/MEMORY.md
/orchestrate status    — report current stage and progress without running
```

---

## Pre-flight Checks

Before launching the sub-agent, verify:

1. **`program.md` exists and has required fields** — read it and check:
   - `topic` (or equivalent heading) is filled in
   - Target venue/journal is specified
   - If either is missing: print what is needed and stop. Do not launch the agent.

2. **Check `handoff.json`** — if it exists, show the user:
   ```
   Resuming from: <handoff.pipeline.stage>
   Next step:     <handoff.pipeline.next_step>
   Resume skill:  <handoff.recovery.resume_skill>
   Human checkpoint needed: <true/false>
   ```
   Ask: "Resume from this point? (y/n)"

3. **Check `outputs/REVIEW_STATE.json`** — if it exists and `status != "complete"`, warn:
   ```
   Active review loop detected: round <N>, score <X.X>/10
   Resuming orchestrator will continue from the review loop.
   ```

---

## Launch

Use the Claude Code sub-agent system to invoke `.claude/agents/orchestrator.md` with full context:

```
<agent: orchestrator>
Task: Run the full GeoResearchAgent-247 research pipeline.

Context files to read first (in order):
1. handoff.json (if exists) — current stage and recovery hints
2. memory/MEMORY.md — pipeline state and scores
3. program.md — research topic, questions, venue, datasets
4. research_contract.md (if exists) — active committed idea

Arguments: $ARGUMENTS

Proceed from the current stage. Do not re-run stages already marked COMPLETE
in memory/MEMORY.md. Delegate each stage to the appropriate specialist agent
as specified in your startup protocol.
</agent>
```

---

## Stage Map (for reference)

| Stage | Delegates to | Output |
|---|---|---|
| 1. Literature Search | `literature-scout` | `memory/paper-cache/` |
| 2. Synthesis | `synthesis-analyst` | `memory/synthesis-*.md` |
| 3. Gap Analysis | `gap-finder` | `memory/gap-analysis.md` |
| 4. Hypothesis Generation | `hypothesis-generator` + `geo-specialist` | `memory/hypotheses.md` |
| 5. Outline | orchestrator (direct) | `memory/outline.md` |
| 6. Section Writing | `paper-writer` (write) + `peer-reviewer` (score) | `outputs/papers/<slug>/*.md` |
| 7. Reference Validation | `citation-manager` | `outputs/papers/<slug>/references.txt` |

---

## After Completion

When the orchestrator finishes, it will output a completion summary. At that point:
- Final paper is assembled at `outputs/papers/<slug>/full_paper.md`
- Run `/review-draft outputs/papers/<slug>/full_paper.md` for the adversarial review loop
- Run `/orchestrate status` to confirm all sections are COMPLETE
