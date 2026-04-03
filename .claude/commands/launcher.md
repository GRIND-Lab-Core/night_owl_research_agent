---
name: launcher
description: "Interactive launcher — choose backend (API or Claude Code subscription) and task (full pipeline / discover ideas / review article), then invoke the matching skill."
---

# Command: /launcher

Interactive entry point for GeoResearchAgent-247. Walks the user through two choices then routes to the appropriate skill.

---

## Step 1 — Choose Backend

Present this menu and wait for the user's response:

```
GeoResearchAgent-247 — Launcher
================================

Backend:
  [1] Anthropic API          — autonomous overnight runs; requires ANTHROPIC_API_KEY
  [2] Claude Code subscription — interactive session; no API key needed (you are already here)

Enter 1 or 2:
```

**If user chooses 1 (API):**
- Check that `ANTHROPIC_API_KEY` is set: `python -c "import os; print('OK' if os.getenv('ANTHROPIC_API_KEY') else 'MISSING')"`
- If MISSING: print `ANTHROPIC_API_KEY is not set. Export it and restart.` then stop.
- If OK: note `backend = api`. Inform user: "API backend selected. Tasks will run via core/orchestrator.py."

**If user chooses 2 (Claude Code subscription):**
- Note `backend = claude-code`. Inform user: "Claude Code backend selected. Tasks run as skills in this session."

---

## Step 2 — Choose Task

Present this menu and wait for the user's response:

```
Task:
  [1] Full pipeline       — literature → experiments → paper writing → review (end-to-end)
  [2] Discover ideas      — search literature, find gaps, generate and score research ideas
  [3] Review article      — adversarial review loop on an existing draft or set of sections

Enter 1, 2, or 3:
```

---

## Step 3 — Route to Skill

Based on the combination of backend and task, take the following action:

### Task 1: Full Pipeline

**Claude Code backend:**
Invoke skill `skills/research-pipeline/SKILL.md`.
Before invoking, confirm AUTO_PROCEED flag with user:
```
AUTO_PROCEED controls whether the agent selects the top idea automatically.
Current value: [read from CLAUDE.md control flags block]
Change it? (y/n):
```
If y: ask "Set AUTO_PROCEED to true (autonomous) or false (pause for approval)?" and update CLAUDE.md accordingly.

Then say: "Starting full pipeline. Reading memory/MEMORY.md to check current stage..." and invoke the skill.

**API backend:**
Run: `python core/orchestrator.py --config configs/full_auto.yaml --topic "[read from program.md Current Topic field]"`
First confirm the topic is set: read `program.md` and display the Current Topic line. Ask "Proceed with this topic? (y/n)".

---

### Task 2: Discover Ideas

**Claude Code backend:**
Ask: "Enter your research topic or press Enter to use the topic from program.md:"
- If user enters a topic: invoke skill `skills/idea-discovery/SKILL.md` with that topic
- If Enter: read `program.md` Current Topic field; invoke skill `skills/idea-discovery/SKILL.md` with that topic

The idea-discovery skill will:
1. Run `skills/geo-lit-review/SKILL.md` to search literature
2. Run gap analysis
3. Generate and score 6–10 ideas
4. Write results to `IDEA_REPORT.md`

**API backend:**
Run: `python core/orchestrator.py --config configs/quick_mode.yaml --agents literature,idea_discovery --topic "[topic]"`

---

### Task 3: Review Article

**Claude Code backend:**
Ask: "Enter the path to the file or folder to review (or press Enter to review outputs/papers/):"
- If path given: invoke skill `skills/auto-review-loop/SKILL.md` with that path
- If Enter: check `outputs/REVIEW_STATE.json`
  - If exists and status ≠ "complete": say "Resuming review loop from round [N]..." and invoke skill `skills/auto-review-loop/SKILL.md`
  - If not exists or complete: invoke skill `skills/auto-review-loop/SKILL.md` on `outputs/papers/`

Before starting, show current HUMAN_CHECKPOINT flag value and ask if user wants to change it.

**API backend:**
Run: `python core/orchestrator.py --config configs/default.yaml --agents review --paper "[path]"`

---

## Notes

- After task completes, offer to return to Step 2 to run another task in the same session.
- All state is persisted automatically (findings.md, outputs/REVIEW_STATE.json, memory/MEMORY.md, handoff.json).
- To run without the launcher, use slash commands directly: `/full-pipeline`, `/find-gaps`, `/review-draft`.
