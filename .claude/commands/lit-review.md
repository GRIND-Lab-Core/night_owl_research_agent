---
name: lit-review
description: "Automated literature review for a geo/RS/GIScience topic. Runs: search → synthesis → gap analysis → formatted review section. Output: outputs/reports/lit-review-<topic>-<date>.md. Usage: /lit-review <topic>"
---

# Command: /lit-review

Run a complete literature review pipeline (search, synthesis, gap analysis, write review section).

## Protocol

1. Run **/geo-search** to retrieve papers for `<topic>`
2. Delegate to **synthesis-analyst** to analyze paper cache
3. Delegate to **gap-finder** to identify research gaps
4. Delegate to **paper-writer** to draft a formal Literature Review section
   - Template: templates/giscience/lit_review_template.md or appropriate subdomain template
   - Self-score target: ≥ 7.5
5. Save to outputs/reports/lit-review-<topic-slug>-<YYYY-MM-DD>.md

Output summary:
```
Literature Review: <topic>
Papers analyzed: N
Gaps identified: N
Review sections: Introduction to field, Theme 1, Theme 2, Theme 3, Synthesis, Gaps
Score: X.X / 10
Saved: outputs/reports/lit-review-<topic-slug>-<date>.md
```
