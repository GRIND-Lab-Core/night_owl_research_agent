---
name: review-draft
description: "Simulated peer review of a paper section or full draft. Three reviewer perspectives (methods expert, domain specialist, applications reviewer). Outputs formal review with decision and path to acceptance. Usage: /review-draft <file-path>"
---

# Command: /review-draft

Run a structured peer review of the specified paper or section.

## Protocol

1. Read `<file-path>` — may be a section file or full_paper.md.
2. Read program.md for target venue and domain focus.
3. Delegate to **peer-reviewer** agent.
4. Display formal review:
```
Peer Review: <file>
Target Venue: <venue>
============================================================
Reviewer 1 (Methods Expert)
  Major Issues: N
  Minor Issues: N
  Recommendation: [decision]

Reviewer 2 (Domain Specialist)
  ...

Reviewer 3 (Applications Reviewer)
  ...

Editor Summary
  Decision: [Accept | Minor Revision | Major Revision | Reject]
  Must-address: N items
  Overall Score: X.X / 10

Path to Acceptance: [if Major/Reject]
```
5. Save review to outputs/reports/review-<slug>-<YYYY-MM-DD>.md
6. If Major Revision or Reject: offer to invoke **paper-writer** for targeted revisions.
