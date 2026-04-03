---
name: full-pipeline
description: "Full end-to-end geo research pipeline (4 stages). Reads CLAUDE.md control flags then invokes skill research-pipeline: idea discovery → experiment design → autonomous spatial experiments (OLS/GWR/MGWR) → adversarial review loop → paper writing. State persists to outputs/REVIEW_STATE.json, findings.md, EXPERIMENT_LOG.md, and memory/MEMORY.md for overnight/recovery runs."
---

# Command: /full-pipeline

Full end-to-end research pipeline for GeoResearchAgent-247. Delegates all stages to specialist agents with iterative scoring (propose → write → score → revise → commit).

---

## Step 1: Program Validation

Read `program.md`. Validate required fields:

**Required (halt if missing):**
- Research Topic (Section 1)
- Target Venue (Section 2)
- At least 1 Research Question (Section 4)

**Recommended (warn, do not halt):**
- Domain Focus checkboxes (Section 5)
- Geographic Scope (Section 7)
- Datasets (Section 8)
- Constraints (Section 6)

If required fields missing:
```
ERROR: program.md validation failed. Missing:
  - [list missing fields]
Fill in program.md before running /full-pipeline.
```

Display pipeline preview on success:
```
GeoResearchAgent-247 Full Pipeline
Topic: <topic>
Target Venue: <venue>
Domain: <checked domains>
Stages: 12
Estimated runtime: 30-90 min (quick) / 2-6 hrs (full-auto)

Starting. Progress saved to memory/MEMORY.md.
```

---

## Step 2: Initialize State

Create/update memory/MEMORY.md with full pipeline state. If partially complete, display resume status:
```
Resuming pipeline:
  ✓ Stage 1: Literature Search (N papers)
  ✓ Stage 2: Synthesis
  ○ Stage 3: Gap Analysis (pending)
```

Create output directories:
- memory/paper-cache/
- memory/synthesis-<date>.md (placeholder)
- outputs/papers/<title-slug>/
- outputs/reports/

Initialize git if needed.

---

## Step 3: Literature Search (delegate to literature-scout)
Skip if MEMORY.md shows Stage 1 complete with ≥ 20 papers.

Requirements: ≥ 20 papers, 60% from ≥ 2020, 30% from priority geo venues.
Retry with broader terms if < 20.

Log: `✓ Stage 1: Literature Search — N papers — <datetime>`

---

## Step 4: Synthesis (delegate to synthesis-analyst)
Skip if Stage 2 complete. Output: memory/synthesis-<date>.md

Log: `✓ Stage 2: Synthesis — N papers analyzed — <datetime>`

---

## Step 5: Gap Analysis (delegate to gap-finder)
Skip if Stage 3 complete. Output: memory/gap-analysis.md with ≥ 3 gaps.

Log: `✓ Stage 3: Gap Analysis — N gaps — <datetime>`

---

## Step 6: Hypothesis Generation (delegate to hypothesis-generator)
Skip if Stage 4 complete. Output: memory/hypotheses.md with ≥ 2 hypotheses scored ≥ 5.0.

Also delegate to **geo-specialist** for feasibility review of top hypothesis.

Log: `✓ Stage 4: Hypothesis Generation — N hypotheses — top: "<H1>" score X.X`

---

## Step 7: Outline Construction
Skip if Stage 5 complete. Write memory/outline.md.

---

## Step 8: Section Writing Loop

For each section (abstract → introduction → literature_review → methodology → results → discussion → conclusion):

Skip if already marked COMPLETE in MEMORY.md.

For methodology and results sections: first delegate to **geo-specialist** for spatial analysis context injection.

**8a.** Invoke **paper-writer** with all context + template.
**8b.** Evaluate score:
- ≥ 7.5: proceed to peer review pass
- 7.0–7.4: minor revision ("sharpen claims and citation density")
- 5.0–6.9: moderate revision ("improve evidence and clarity")
- < 5.0: major revision ("revisit structure and core argument")
- Maximum 3 attempts. If still < 7.5: flag NEEDS_HUMAN_REVIEW, continue.

**8c.** Quick peer review: invoke **peer-reviewer** with just this section.
- Major issues found: one targeted revision pass
- Minor/no issues: accept

**8d.** Save and commit:
```bash
git add "outputs/papers/<title-slug>/<section>.md"
git commit -m "feat: accept <section> — score <X.X>"
```
Update MEMORY.md. Report: `✓ <Section> — Score: X.X — Progress: N/7`

---

## Step 9: Full Paper Peer Review

Invoke **peer-reviewer** for complete paper review.
- Accept/Minor Revision: proceed
- Major Revision: targeted revision loop (max 2 full-paper review cycles)
- Reject: halt with full review and path to acceptance

---

## Step 10: Reference Validation (delegate to citation-manager)
Output: outputs/papers/<title-slug>/references.txt (APA 7th)

---

## Step 11: Assemble Final Paper

Concatenate sections → outputs/papers/<title-slug>/full_paper.md

Add YAML frontmatter:
```yaml
---
title: "<paper title>"
generated: "<ISO datetime>"
agent: "GeoResearchAgent-247"
target_venue: "<venue>"
total_word_count: ~N
sections_accepted: 7/7
peer_review_decision: "<decision>"
---
```

Final git commit.

---

## Step 12: Completion Report

```
/full-pipeline complete.
============================================================
Paper: <title>
Target Venue: <venue>

Pipeline Summary:
  ✓ Literature Search: N papers
  ✓ Synthesis: N papers analyzed
  ✓ Gap Analysis: N gaps
  ✓ Hypotheses: N evaluated
  ✓ Sections: 7/7 accepted
  ✓ Peer Review: <decision>
  ✓ References: N citations validated

Section Scores:
  Abstract:          X.X
  Introduction:      X.X
  Literature Review: X.X
  Methodology:       X.X
  Results:           X.X
  Discussion:        X.X
  Conclusion:        X.X
  Mean:              X.X

Output: outputs/papers/<title-slug>/full_paper.md

[If flags]: Human Review Needed: ...

Next steps:
  1. Review peer review report for remaining minor issues
  2. Add figures/tables referenced in text
  3. Format for <venue> submission
  4. Final proofread
```
