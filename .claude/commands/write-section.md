---
name: write-section
description: "Invoke skills result-to-claim then paper-write for a specific section. Verifies claims vs results first, then runs autoresearch loop (write → score → revise until ≥ 7.5). Reads memory/outline.md and memory/approved_claims.md. Git commits accepted section. Usage: /write-section <section-name>"
---

# Command: /write-section

Write and iteratively improve a single paper section using the autoresearch loop.

Supported sections: abstract, introduction, literature_review, methodology, results, discussion, conclusion

## Protocol

1. Read program.md for topic, venue, constraints.
2. Read any existing context files: synthesis, gap analysis, hypotheses, outline.
3. Read previous sections if they exist (for consistency).
4. For **methodology** and **results**: first delegate to **geo-specialist** for spatial analysis context.
5. Delegate to **paper-writer** with section name, all context, and template path.
6. Evaluate score. Loop with targeted revision directives until score ≥ 7.5 or 3 attempts reached.
7. If ≥ 7.5: quick peer-reviewer pass.
8. Accept → save to outputs/papers/<title-slug>/<section>.md
9. Git commit: `git commit -m "feat: accept <section-name> — score <X.X>"`
10. Update MEMORY.md.

Progress report:
```
Writing: <section>
Attempt 1: Score X.X — [Revision directive if < 7.5]
Attempt 2: Score X.X — [Accepted / next directive]
✓ <section> accepted — Score: X.X
Saved: outputs/papers/<title-slug>/<section>.md
```
