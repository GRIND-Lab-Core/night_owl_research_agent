---
name: training-check
description: Monitors running spatial experiments. Checks output files, log files, and process status. Categorizes results as OK, STALLED, FAILED, or COMPLETE. Fires alerts by appending to output/FINDINGS.md. Run every 15 minutes during Stage 3 of research-pipeline.
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

**COMPLETE**: Update output/EXPERIMENT_LOG.md status to SUCCESS. Append finding to `output/FINDINGS.md`.
**CLEARLY BAD**: Kill job if possible. Mark as FAILED in log. Try to fix the issue and retry once.
**STALLED**: Check if process is still alive. If dead: re-queue. If alive: wait 15 more min.

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

Append alerts to `output/FINDINGS.md`: `[ALERT] Experiment <name> failed: <reason>`
