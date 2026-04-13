---
name: novelty-check
description: Validates that a research idea is genuinely novel vs. existing literature. Searches ArXiv, Semantic Scholar, and WebSearch for near-duplicate work. Produces a novelty verdict and evidence. Run on each idea from idea-discovery before investing in experiments.
argument-hint: [method-or-idea-description]
tools: Bash, WebFetch, WebSearch, Read, Write, Grep, Glob
---

# Skill: novelty-check

You verify that a research idea,**$ARGUMENTS** , has not already been published in substantially equivalent form.

---

## Constants

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP. Must be an OpenAI model (e.g., `gpt-5.4`, `o3`, `gpt-4o`)

## Phase 1: Identify Key Claims

1. Read the user's method description
2. Identify 3-5 core claims that would need to be novel:
   - What is the method?
   - What problem does it solve?
   - What is the mechanism?
   - What makes it different from obvious baselines?
   - What dataset does it use?
   - What is the spatial and temporal granularity of the research?

---

## Phase 2: Search

For EACH core claim, search using ALL available sources:

1. **Web Search** (via `WebSearch`):
   - Search arXiv, Google Scholar, Semantic Scholar
   - Use specific technical terms from the claim
   - Try at least 3 different query formulations per claim
   - Include year filters for 2024-2026

2. **Known paper databases**: Check against:
   - ICLR 2025/2026, NeurIPS 2025, ICML 2025/2026
   - Recent arXiv preprints (2025-2026)

3. **Local Papers**
   - Also directly fetch relevant abstracts from `output/paper-cache/` or `paper/` if they already exist.

4. **Read abstracts**: For each potentially overlapping paper, WebFetch its abstract and related work section


---

## Phase 3: Evaluate

Call REVIEWER_MODEL via Codex MCP (`mcp__codex__codex`) with xhigh reasoning:
```
config: {"model_reasoning_effort": "xhigh"}
```
Prompt should include:
- The proposed method description
- All papers found in Phase 2
- Ask: "Is this method novel? What is the closest prior work? What is the delta?"

**If the external reviewer model is not configured correctly, use Claude Code subagent instead.**

---

## Phase 4: Novelty Report

Output a structured novelty report:

```markdown
## Novelty Check Report

### Proposed Method
[1-2 sentence description]

### Core Claims
1. [Claim 1] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
2. [Claim 2] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
...

### Closest Prior Work
| Paper | Year | Venue | Overlap | Key Difference |
|-------|------|-------|---------|----------------|

### Overall Novelty Assessment
- Score: X/10
- Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON
- Key differentiator: [what makes this unique, if anything]
- Risk: [what a reviewer would cite as prior work]

### Suggested Positioning
[How to frame the contribution to maximize novelty perception]
```

**Write report to `output/NOVELTY_REPORT.md`**

**Update `output/IDEA_REPORT.md` with verdict and score.**

### Important Rules
- Be BRUTALLY honest — false novelty claims waste months of research time
- "Applying X to Y" is NOT novel unless the application reveals surprising insights
- Check both the method AND the experimental setting for novelty
- If the method is not novel but the FINDING would be, say so explicitly
- Always check the most recent 6 months of arXiv — the field moves fast



