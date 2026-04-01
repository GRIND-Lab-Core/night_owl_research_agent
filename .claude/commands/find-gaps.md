---
name: find-gaps
description: "Identify research gaps in a geo/RS/GIScience topic from existing literature. Outputs a ranked gap list and top 3 actionable hypotheses. Usage: /find-gaps <topic>"
---

# Command: /find-gaps

Identify and rank research gaps for a geo/RS/GIScience topic.

## Protocol

1. Check if paper cache exists for `<topic>`. If not, run /geo-search first.
2. Check if synthesis exists. If not, delegate to **synthesis-analyst**.
3. Delegate to **gap-finder** with synthesis and program.md context.
4. Display ranked gap list:
```
Research Gaps: <topic>
N gaps identified, ranked by: 0.4×Novelty + 0.35×Feasibility + 0.25×Impact

1. [Gap name] — Score: X.X
   Type: Methodological/Geographic/Data/Equity
   [2-sentence description]
   Suggested approach: ...

2. ...
```
5. Also generate top 3 hypotheses from top-ranked gaps (delegate to **hypothesis-generator**).
6. Save: memory/gap-analysis.md and memory/hypotheses.md
