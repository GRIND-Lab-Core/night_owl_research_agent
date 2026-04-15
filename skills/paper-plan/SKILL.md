---
name: paper-plan
description: Produces a detailed paper outline from research plan, review results, and experiment results. Creates section-by-section plan with word budgets, key claims per section, and figures list. Uses journal templates from templates/ for venue-specific formatting.
argument-hint: [topic-or-narrative-doc]
tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Skill: paper-plan

You produce a concrete, actionable paper outline before any writing begins from: **$ARGUMENTS**

---

## Constants

- **REVIEWER_MODEL = `gpt-5.4`** — Model used via Codex MCP for outline review. Must be an OpenAI model.
- **TARGET_VENUE = `IJGIS`** — Default venue. User can override (e.g., `/paper-plan "topic" — venue: AAAG`). Supported: `TGIS`, `RSE`, `ICML`, `CVPR`, `ACL`, `AAAI`, `ACM`, `IEEE_JOURNAL` (IEEE Transactions / Letters), `IEEE_CONF` (IEEE conferences).
- **MAX_PAGES** = 30. Adjust based on paper tempalte selected.

---


## Orchestra-Guided Writing Overlay

Keep the existing `insleep` workflow and outputs, but use the shared references below to improve the quality of the story and outline.

- Read `../shared-references/writing-principles.md` when framing the one-sentence contribution, Abstract, Introduction, Related Work, or hero figure.
- Read `../shared-references/venue-checklists.md` before freezing the outline for a specific venue.
- Only load these references when needed; do not paste their full contents into the working draft.



## Phase 1: Gather Context

Read:
- `research_contract.md` — problem, method, contributions
- `memory/APPROVED_CLAIMS.md` — verified results to highlight
- `output/LIT_REVIEW_REPORT.md` — Gap Analysis section (gaps addressed) and Synthesis section (related work context)
- `output/AUTO_REVIEW.md` — if review has run, incorporate reviewer feedback into outline
- Target venue from `program.md` Section 2

---

## Phase 2: Select Template

Based on **TARGET_VENUE**, choose the appropriate template from `templates/`:
- Geoscience: `templates/geoscience/` — GRL, Nature Geoscience, JGR
- Remote Sensing: `templates/remote_sensing/` — RSE, IEEE TGRS, ISPRS
- GIScience: `templates/giscience/` — IJGIS, Transactions in GIS, AAG Annals
If template does not exist, use Websearch to grab journal or paper templates.

**IMPORTANT**: The section count is FLEXIBLE (5-8 sections). Choose what fits the content best. The templates below are starting points, not rigid constraints.

---

## Phase 3: Build Outline

Write `output/PAPER_PLAN.md` with:
- For each section: title, word budget, key claims to make, evidence to cite, figures/tables needed
- Especially for Methods: list every tool/dataset/parameter to document
- For Results: reference specific table/figure numbers (pre-assign them)

Example structure:
```markdown
# Paper Outline: [Title]
Target: [venue] | Word limit: N | Type: empirical

## Section 1: Abstract (250 words)
Claims: [top 2-3 approved claims]
Required: problem / gap / method / 1+ specific number / contribution

## Section 2: Introduction (800 words)
Para 1: Broad problem (cite 2-3 authoritative sources)
Para 2: Scale/significance (quantified)
Para 3: Current approaches + shortcomings
Para 4: The specific gap (cite boundary papers from the Gap Analysis section of output/LIT_REVIEW_REPORT.md)
Para 5: Your contribution (numbered, match memory/APPROVED_CLAIMS.md)
Para 6: Paper organization

## Section 3: Literature Review (1500 words, 3 subsections)
Theme 1: [GWR/spatial methods — 8 papers]
Theme 2: [domain application — 10 papers]
Theme 3: [datasets and evaluation — 7 papers]
Gap paragraph: bridge to contribution

## Section 4: Methodology (1200 words)
4.1 Study Area (coords, CRS, area in km², why chosen)
4.2 Data (each dataset: source, resolution, temporal, preprocessing)
4.3 Methods (OLS → GWR → MGWR pipeline; proposed method)
4.4 Evaluation (metrics: R², AICc, Moran's I, RMSE; spatial CV protocol)

## Section 5: Results (1000 words)
Table 1: Model comparison (OLS/GWR/MGWR + proposed)
Figure 1: Local R² map
Figure 2: Key coefficient map
5.1 Main results — lead with best approved claim
5.2 Spatial patterns — coefficient variation
5.3 Moran's I residuals — spatial autocorrelation diagnostic

## Section 6: Discussion (700 words)
6.1 Confirm/refute hypothesis from research_contract.md
6.2 Compare to cited papers (specific numbers)
6.3 Limitations (specific, not generic)
6.4 Implications

## Section 7: Conclusion (400 words)
Numbered contributions (mirror Introduction)
Broader implications
Future work (3-5 specific directions from claim audit)
```

**IMPORTANT**: The section count is FLEXIBLE (5-8 sections). Choose what fits the content best. The example structure are starting points, not rigid constraints.

---

## Phase 4: Figure List

List every figure and table:

```markdown
## Figure Plan

| ID | Type | Description | Data Source | Priority |
|----|------|-------------|-------------|----------|
| Fig 1 | Hero/Architecture | System overview + comparison | manual | HIGH |
| Fig 2 | Line plot | Training curves comparison | figures/exp_A.json | HIGH |
| Fig 3 | Bar chart | Ablation results | figures/ablation.json | MEDIUM |
| Table 1 | Comparison table | Main results vs. baselines | figures/main_results.json | HIGH |
| Table 2 | Theory comparison | Prior bounds vs. ours | manual | HIGH (theory papers) |
```

**CRITICAL for Figure 1 / Hero Figure**: Describe in detail what the figure should contain, including:
- Which methods are being compared
- What the visual difference should demonstrate
- Caption draft that clearly states the comparison
- Why the figure helps a skim reader understand the paper before reading the full method


## Phase 5: Citation Scaffolding

For each section, list required citations:

```markdown
## Citation Plan
- §1 Intro: [paper1], [paper2], [paper3] (problem motivation)
- §2 Related: [paper4]-[paper10] (categorized by subtopic)
- §3 Method: [paper11] (baseline), [paper12] (technique we build on)
```

**Citation rules**
1. NEVER generate BibTeX from memory — always verify via search or existing .bib files
2. Every citation must be verified: correct authors, year, venue
3. Flag any citation you're unsure about with `[VERIFY]`
4. Prefer published versions over arXiv preprints when available

## Phase 6: Cross-Review with REVIEWER_MODEL

Send the complete outline to GPT-5.4 xhigh for feedback:

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Review this paper outline for a [VENUE] submission.
    [full outline including Claims-Evidence Matrix]

    Score 1-10 on:
    1. Logical flow — does the story build naturally?
    2. Claim-evidence alignment — every claim backed?
    3. Missing experiments or analysis
    4. Positioning relative to prior work
    5. Page budget feasibility (MAX_PAGES = main body to Conclusion end, excluding refs/appendix)
    6. Front-matter strength — are the abstract, introduction, and hero figure plan strong enough for skim-reading reviewers?

    For each weakness, suggest the MINIMUM fix.
    Be specific and actionable — "add X" not "consider more experiments".
```
If external LLM is not configured correctly, use subagent instead.

Apply feedback before finalizing.

### Step 7: Output

Save the final outline to `output/PAPER_PLAN.md`. Refer to `template/PAPER_PLAN_TEMPLATE` for example structure.


## Key Rules
- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.
- **Do NOT generate author information** — leave author block as placeholder or anonymous
- **Be honest about evidence gaps** — mark claims as "needs experiment" rather than overclaiming
- **Page budget is hard** — if content exceeds MAX_PAGES, suggest what to move to appendix
- **MAX_PAGES counting differs by venue** — ML conferences: main body to Conclusion end, references/appendix NOT counted. **IEEE venues: references ARE counted toward the page limit.**
- **Venue-specific norms** — ML conferences (ICLR/NeurIPS/ICML) use `natbib` (`\citep`/`\citet`); **IEEE venues use `cite` package (`\cite{}`, numeric style)**
- **Claims-Evidence Matrix is the backbone** — every claim must map to evidence, every experiment must support a claim
- **Front-load the story** — the outline should make the contribution clear in the title, abstract, introduction, and hero figure before the reader reaches the full method
- **Figures need detailed descriptions** — especially the hero figure, which must clearly specify comparisons and visual expectations
- **Section count is flexible** — 5-8 sections depending on paper type. Don't force content into a rigid 5-section template.



## Acknowledgements
Outline methodology inspired by [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) (claim-evidence mapping), [claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) (citation verification), and [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) (claim verification protocol). The writing-framing overlay in this hybrid pack is adapted from Orchestra Research's paper-writing guidance.
