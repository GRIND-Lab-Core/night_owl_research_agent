---
name: paper-write
description: Writes individual paper sections using the autoresearch iterative scoring loop (write → score → revise → accept at ≥7.5). Reads from memory/outline.md and memory/approved_claims.md. Only uses verified claims. Follows IMRAD conventions from skills/knowledge/academic-writing.md.
tools: Read, Write
---

# Skill: paper-write

You write one paper section at a time using the autoresearch loop. You only use claims from `memory/approved_claims.md`.

---

## Pre-Writing Checklist

Before writing any section:
1. Read `memory/outline.md` for section plan, word budget, and required claims
2. Read `memory/approved_claims.md` — **only use claims listed here**
3. Read `skills/knowledge/academic-writing.md` for section-specific guidance
4. Read `skills/knowledge/apa-citations.md` for citation formatting
5. Read relevant section from `memory/synthesis-YYYY-MM-DD.md` for literature content
6. Read `skills/knowledge/spatial-methods.md` for spatial conventions (CRS, Moran's I reporting)

---

## Writing Loop (Autoresearch Pattern)

For each section:

**Attempt 1**: Write full section draft following outline plan exactly.

**Self-scoring**: Score on 5 dimensions (from `configs/default.yaml` scoring.weights):
- Novelty (30%): Is the contribution clearly and defensibly stated?
- Rigor (25%): Methods reproducible? Spatial validity addressed? Baselines compared?
- Literature coverage (20%): ≥ 15 citations? Current? Priority geo venues?
- Clarity (15%): Active voice? Numbers reported? No vague claims?
- Impact (10%): Practical significance stated?

Report: `Score: X.X (N:X.X, R:X.X, L:X.X, C:X.X, I:X.X)`

**If score ≥ 7.5**: accept and save.
**If score 7.0–7.4**: minor revision — sharpen specific claims, increase citation density
**If score 5.0–6.9**: moderate revision — restructure argument, add evidence
**If score < 5.0**: major revision — rewrite from outline plan scratch
**Maximum 3 attempts.** If still < 7.5 after 3: flag `NEEDS_HUMAN_REVIEW`, save best draft, continue.

---

## Section-Specific Rules

**Abstract**: Self-contained, ≤ 250 words, ≥ 1 specific number from approved_claims.md, no citations.
**Introduction**: Funnel structure. Contributions list MUST match approved_claims.md. No fabricated contributions.
**Literature Review**: Thematic, not chronological. Synthesis table optional. Gap paragraph mandatory.
**Methodology**: CRS must be stated for all datasets. Spatial CV specified. All hyperparameters listed.
**Results**: Lead with best approved claim + its specific number. Moran's I residuals reported. No interpretation.
**Discussion**: Interpret results vs. prior work with specific metric comparisons. Limitations subsection.
**Conclusion**: Not an abstract copy. Numbered contributions. Future work ≥ 3 items.

---

## Output

Save each accepted section to: `outputs/papers/<title-slug>/<section>.md`
Git commit: `git commit -m "feat: accept <section> — score <X.X>"`
Update `memory/MEMORY.md` Section Quality Scores table.
Update `memory/outline.md` status: `- [x] <section> (score: X.X)`
