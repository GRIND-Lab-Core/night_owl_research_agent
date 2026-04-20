---
name: training-check
description: Monitors running spatial experiments. Checks output files, log files, and process status. Categorizes results as OK, STALLED, FAILED, or COMPLETE. Fires alerts by appending to output/PROJ_NOTES.md. Run every 15 minutes during Stage 3 of research-pipeline.
tools: Bash, Read, Write
---

# Skill: training-check

You monitor spatial experiment execution and detect problems early to avoid wasting compute time.

---

## Phase 1: Check Active Experiments

Read `output/EXPERIMENT_LOG.md` for experiments with status RUNNING or PENDING.

For each running experiment:
1. Check if output file was recently modified:
```bash
python -c "import os, time; f='[output_path]'; age=(time.time()-os.path.getmtime(f))/60; print(f'Modified {age:.1f} min ago')"
```
2. Check last few lines of log file for errors:
```bash
tail -20 [log_path]
```
3. Check for error keywords: `Error`, `Traceback`, `NaN`, `inf`, `MemoryError`, `Killed`
4. Check for stall: no file modification in > 30 min despite RUNNING status

---

## Phase 2: Classify Status

| Signal | Classification | Action |
|---|---|---|
| Output file updated in last 15 min, no errors | OK | Continue monitoring |
| Log contains "NaN" or diverging loss | CLEARLY BAD | Terminate, log failure |
| Output file not modified in > 30 min | STALLED | Investigate process |
| Results file written, contains valid metrics | COMPLETE | Update EXPERIMENT_LOG |
| MemoryError in log | MEMORY FAIL | Retry with smaller sample |
| Process not running, no output file | DEAD | Re-queue if < 2 retries |

---

## Phase 3: Actions

**COMPLETE**: Update output/EXPERIMENT_LOG.md status to SUCCESS. Append finding to `output/PROJ_NOTES.md`.
**CLEARLY BAD**: Kill job if possible. Mark as FAILED in log. Try to fix the issue and retry once.
**STALLED**: Check if process is still alive. If dead: re-queue. If alive: wait 15 more min.

---

## Phase 3.5: Human Checkpoint — Data Synthesis

Honor the `HUMAN_CHECKPOINT` flag in `CLAUDE.md` (default: `true`). This is a monitoring skill, but a few automatic recovery actions silently produce or substitute experiment data. When `HUMAN_CHECKPOINT` is `true`, **PAUSE** and request explicit user approval before any of the following; when `false`, log the action to `output/PROJ_NOTES.md` with rationale and proceed.

| Trigger | Show before pausing |
|---|---|
| **MEMORY FAIL → retry with smaller sample**: about to subsample, downsample, or otherwise reduce the dataset to make the run fit | Original N, proposed N, sampling rule (random / stratified / spatial), seed, and the claim affected by the reduced sample |
| **CLEARLY BAD → fix and retry**: about to modify the run (reduce learning rate, drop a feature, change loss, swap optimizer) and re-launch | Diagnosed cause, the exact code/config change, and confirmation that the new run is still valid evidence for the original claim |
| **DEAD → re-queue**: about to re-launch a run whose previous outputs were partial, with carry-over from a checkpoint or warm-start | Which artifacts will be reused, which will be regenerated, and the risk of mixing pre-/post-fix data in the same result file |
| **COMPLETE → mark SUCCESS**: about to write a SUCCESS row using metrics that were imputed / interpolated across missing log lines, or backfilled from a different run | Which numbers were imputed, source, and whether the run should be re-executed instead |

Do not mark a run SUCCESS in `EXPERIMENT_LOG.md` based on synthesized metrics. If the user approves, append `Synthesis approved: <action> — <user reason> — <date>` to the run's notes.

---

## Phase 4: Progress Report

Output to stdout:
```
Training Check — <timestamp>
Active experiments: N
  COMPLETE: N
  OK (running): N
  STALLED: N
  FAILED: N

[List any failures or alerts]
```

Append alerts to `output/PROJ_NOTES.md`: `[ALERT] Experiment <name> failed: <reason>`
