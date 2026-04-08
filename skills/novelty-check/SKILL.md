---
name: novelty-check
description: Validates that a research idea is genuinely novel vs. existing literature. Searches ArXiv and Semantic Scholar for near-duplicate work. Produces a novelty verdict and evidence. Run on each idea from idea-discovery before investing in experiments.
tools: Bash, WebFetch, WebSearch, Read, Write
---

# Skill: novelty-check

You verify that a research idea has not already been published in substantially equivalent form.

---

## Phase 1: Formulate Search Queries

Given an idea description, extract:
- Core method + core application
- Key dataset name
- Geographic scope

Build 3-5 specific queries that would find this exact paper if it existed:
- `"<method> <application> <geography>"`
- `"<method> <dataset>"`
- `"<application> spatial non-stationarity <region>"` (example pattern)

---

## Phase 2: Search

**ArXiv:**
```bash
python tools/arxiv_fetch.py --query "<query>" --max-results 20 --output memory/paper-cache/novelty_<slug>.json
```

**Semantic Scholar:**
```bash
python tools/semantic_scholar_fetch.py --query "<query>" --max-results 30 --output memory/paper-cache/novelty_s2_<slug>.json
```

Also directly fetch relevant abstracts from `memory/paper-cache/` if they already exist.

---

## Phase 3: Evaluate

For each retrieved paper, assess: is this paper doing **substantially the same thing** as the idea?

Criteria for "near-duplicate":
- Same method + same application domain + overlapping geography
- Same data sources + same analytical framework
- Published within last 3 years (older near-duplicates may be OK if a clear advance is made)

---

## Phase 4: Verdict

**NOVEL** — no near-duplicate found. Proceed.
**INCREMENTAL** — similar work exists but a meaningful advance is still possible. Describe what advance is needed. Mark idea as needing stronger differentiation.
**ALREADY DONE** — substantially equivalent paper exists. Reject idea, cite the paper.

Write verdict to `memory/novelty_<idea-slug>.md`:
```
Idea: [title]
Verdict: NOVEL / INCREMENTAL / ALREADY DONE
Closest paper: [citation]
Distinguishing factors: [what makes this idea different, if NOVEL or INCREMENTAL]
```

Update `IDEA_REPORT.md` with verdict.
