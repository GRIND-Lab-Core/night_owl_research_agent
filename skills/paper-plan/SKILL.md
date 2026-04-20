---
name: paper-plan
description: Produces a detailed, venue-aware paper outline from all available upstream artifacts (RESEARCH_PLAN, lit review, idea report, refined proposal, experiment plan/results, narrative report). Creates section-by-section plan with word budgets, claim-evidence matrix, figure/table plan, and citation scaffolding. Uses journal templates from templates/ for venue-specific formatting.
argument-hint: [topic-or-narrative-doc]
tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Skill: paper-plan

You produce a concrete, actionable paper outline before any writing begins from: **$ARGUMENTS**

---

## Constants

- **REVIEWER_MODEL = `gpt-5.4`** — Model used via Codex MCP for outline review. Must be an OpenAI model.
- **TARGET_VENUE = `IJGIS`** — Default venue. User can override (e.g., `/paper-plan "topic" — venue: AAAG`). Supported: `TGIS`, `RSE`, `ISPRS_JPRS`, `AAG_ANNALS`, `IEEE_TGRS`, `ICML`, `ICLR`, `NeurIPS`, `CVPR`, `ACL`, `AAAI`, `ACM`, `IEEE_JOURNAL` (IEEE Transactions / Letters), `IEEE_CONF` (IEEE conferences).
- **MAX_PAGES = 40** — Adjust based on paper template selected. ML conferences typically 8–10 pages (excluding refs/appendix). IEEE venues include references in page count.
- **MAX_PRIMARY_CLAIMS = 2** — One dominant contribution + one supporting. Prevents scope creep.
- **MAX_FIGURES = 8** — Soft cap; hero figure + up to 7 supporting figures/tables.
- **OUTPUT_PATH = `output/PAPER_PLAN.md`**

---

## Orchestra-Guided Writing Overlay

Keep the existing workflow and outputs, but use the shared references below to improve the quality of the story and outline.

- Read `skills/knowledge/academic-writing.md` when framing the one-sentence contribution, Abstract, Introduction, Related Work, or hero figure.
- Read `skills/knowledge/geoai-domain.md` for GIScience/GeoAI framing conventions.
- Read `skills/knowledge/spatial-methods.md` when planning methodology sections for spatial analysis papers.
- Only load these references when needed; do not paste their full contents into the working draft.

---

## Phase 0: Load Checkpoint (Resume Support)

Check for existing state:

1. Read `output/PAPER_PLAN.md` — if it exists and was generated in the current session, ask the user whether to rebuild or refine it.
2. Read `handoff.json` — if `pipeline.stage` indicates paper-plan is in progress, resume from the last recorded phase.

If no checkpoint exists, proceed to Phase 1.

---

## Phase 1: Gather Context

Read all available upstream artifacts. Each file is **optional** — missing files are soft failures. Record which files were found and which were missing; this information goes into the plan's "Input Files Used" and "Missing Inputs" sections.

### Primary Inputs (read in this order)

| Priority | File | What to extract | Required? |
|---|---|---|---|
| 1 | `RESEARCH_PLAN.md` | Problem statement, method overview, success criteria, target venue, research questions | No — fall back to FINAL_PROPOSAL or NARRATIVE_REPORT |
| 2 | `output/LIT_REVIEW_REPORT.md` | Gap Analysis (gaps this paper closes), Synthesis (related work themes), key citations | No — reduces related work quality |
| 3 | `output/IDEA_REPORT.md` | Chosen idea rationale, pilot scores, competing ideas considered | No — reduces novelty framing |
| 4 | `output/refine-logs/FINAL_PROPOSAL.md` | Refined problem, method, contributions, feasibility assessment | No — fall back to RESEARCH_PLAN |
| 5 | `output/EXPERIMENT_PLAN.md` | Experiment design, run order, success criteria, claim-to-experiment mapping | No — reduces experiment planning quality |
| 6 | `output/EXPERIMENT_RESULT.md` | Actual quantitative results, metrics, pass/fail status | No — plan will flag results as [PENDING] |
| 7 | `output/NARRATIVE_REPORT.md` | Consolidated narrative with claims-evidence matrix, figure plan, limitations | No — if present, this is the richest single source |


### Context Synthesis Rules

1. **NARRATIVE_REPORT.md is king** — if it exists, it is the primary planning source. It was specifically designed to consolidate all upstream artifacts for the paper-writing pipeline. Use other files only to fill gaps or verify claims.
2. **RESEARCH_PLAN.md is the research intent** — it defines what the researcher *wants* to achieve. FINAL_PROPOSAL.md is the *refined* version. EXPERIMENT_RESULT.md is what *actually happened*. The outline must reconcile all three.
3. **Never fabricate from gaps** — if a file is missing, the outline must explicitly mark the affected sections as `[NEEDS: <missing-file>]` rather than inventing content.
4. **Numbers are sacred** — copy metrics verbatim from EXPERIMENT_RESULT.md and APPROVED_CLAIMS.md. Never round, paraphrase, or extrapolate.

---

## Phase 2: Determine Venue and Paper Type

### Step 2.1: Resolve TARGET_VENUE

Check in this order (first match wins):
1. Explicit user argument (e.g., `— venue: ISPRS_JPRS`)
2. `RESEARCH_PLAN.md` target venue field
3. `NARRATIVE_REPORT.md` venue target section
4. `output/PAPER_PLAN.md` existing venue (if refining)
5. Default: `IJGIS`

### Step 2.2: Load Venue Template

Based on **TARGET_VENUE**, choose the appropriate template from `templates/`:

| Venue Category | Template Directory | Venues |
|---|---|---|
| GIScience | `templates/giscience/` | IJGIS, TGIS, AAG Annals |
| Remote Sensing | `templates/remote_sensing/` | RSE, IEEE TGRS, ISPRS JPRS |
| Geoscience | `templates/geoscience/` | GRL, Nature Geoscience |
| ML Conference | (use WebSearch) | ICLR, NeurIPS, ICML, CVPR, ACL, AAAI |
| IEEE | (use WebSearch) | IEEE_JOURNAL, IEEE_CONF |

If the template does not exist locally, use WebSearch to retrieve the venue's author guidelines and page limits.

### Step 2.3: Determine Paper Type

Infer from the contributions and method:

| Paper Type | Signal | Section Emphasis |
|---|---|---|
| Methodological innovation | New algorithm/model, ablation studies | Heavy Methods + Experiments |
| Applied case study | Domain problem, study area, practical results | Heavy Study Area + Results + Discussion |
| Benchmark/evaluation | Comparison across methods/datasets | Heavy Experiments + Analysis |
| System/platform | Architecture, pipeline, deployment | Heavy System Description + Evaluation |
| Conceptual/framework | Theory, taxonomy, conceptual model | Heavy Framework + Case Study |
| Review/survey | Synthesis, taxonomy, gap analysis | Heavy Literature + Synthesis |

### Step 2.4: Set Page Budget

Derive from venue:

| Venue Type | MAX_PAGES | References in page count? | Appendix allowed? |
|---|---|---|---|
| IJGIS / TGIS / AAG Annals | 25–30 | No | Yes (supplementary) |
| RSE / ISPRS JPRS | 20–30 | Varies | Yes |
| IEEE TGRS | 13–15 | Yes | Brief online supplement |
| IEEE_CONF | 6–8 | Yes | No |
| ICLR / NeurIPS / ICML | 8–10 | No | Yes (appendix) |
| CVPR | 8 | No | Yes (supplementary) |

---

## Phase 3: Build the Outline

Write `output/PAPER_PLAN.md` following the structure in `templates/PAPER_PLAN_TEMPLATE.md` (Sections §0–§26). The template is the target schema; fill every section with content derived from the upstream artifacts.

### Section-by-Section Generation Rules

**§0 Document Status** — Fill version, date, venue, manuscript type, readiness level, list of input files consumed and missing.

**§1 One-Paragraph Summary** — Synthesize from NARRATIVE_REPORT.md §1 or FINAL_PROPOSAL.md contributions. The one-sentence claim must be specific, defensible, and evidence-based. Draft a 150–250 word abstract-style summary.

**§2 Target Journal Strategy** — Use venue template to fill journal fit, audience, expectations. Read `skills/knowledge/academic-writing.md` for framing advice.

**§3 Research Context and Motivation** — Draw from LIT_REVIEW_REPORT.md synthesis + RESEARCH_PLAN.md problem statement. Quantify the problem scale.

**§4 Research Gap** — Extract directly from LIT_REVIEW_REPORT.md Gap Analysis section. List specific gaps with boundary citations. Explain why existing work is insufficient.

**§5 Novelty and Contributions** — Numbered contributions from FINAL_PROPOSAL.md or NARRATIVE_REPORT.md. Each contribution tied to a specific experiment/claim. Include "What This Paper Is *Not* Claiming" to set expectations.

**§6 Research Questions and Hypotheses** — From RESEARCH_PLAN.md or FINAL_PROPOSAL.md. Align RQs with experiment design from EXPERIMENT_PLAN.md.

**§7 Study Scope and Boundaries** — Spatial, temporal, data, and method scope. Explicit limitations of scope.

**§8 Data and Materials** — From DATA_MANIFEST.md and EXPERIMENT_PLAN.md. For each dataset: source, resolution, temporal coverage, preprocessing, license.

**§9 Methodological Plan** — From FINAL_PROPOSAL.md method description and EXPERIMENT_PLAN.md design. Include baselines, evaluation protocol, spatial analysis components. Read `skills/knowledge/spatial-methods.md` for GIScience method framing.

**§10 Experiments** — From EXPERIMENT_PLAN.md (design) and EXPERIMENT_RESULT.md (outcomes). Mark incomplete experiments as `[PENDING]`.

**§11 Results Summary** — From EXPERIMENT_RESULT.md and APPROVED_CLAIMS.md. Headline findings in priority order. Quantitative results with exact values. Flag missing results as `[NEEDS: experiment completion]`.

**§12 Claim-to-Evidence Map** — The backbone of the plan. Every major claim maps to: evidence source, quantitative support, figure/table ID, experiment ID, confidence level. Unsupported claims go into "Unsupported or Weak Claims" subsection.

**§13 Figures Plan** — From NARRATIVE_REPORT.md figure plan or EXPERIMENT_RESULT.md outputs. For each figure: ID, type, description, data source, status, priority.

> **CRITICAL: Hero Figure (Fig. 1)** — Describe in detail:
> - What methods/concepts are being compared
> - What the visual difference should demonstrate
> - Caption draft that clearly states the comparison
> - Why a skim reader understands the paper from this figure alone

**§14 Tables Plan** — Required tables: dataset summary, baseline comparison, ablation (if applicable), hyperparameters, error analysis.

**§15 Related Work Synthesis** — From LIT_REVIEW_REPORT.md thematic synthesis. Group into 3–4 clusters that map to the paper's related work section. For each cluster: summary, representative studies, how our work relates and differs.

**§16 Discussion Plan** — Interpretation themes, implications (GIScience/GeoAI + practical), responsible research considerations, generalizability.

**§17 Limitations and Future Work** — Concrete limitations from EXPERIMENT_RESULT.md and AUTO_REVIEW_REPORT.md. Severity assessment. 3–5 specific future work directions.

**§18 Reproducibility and Open Science Plan** — Code availability, data availability, reproducibility assets checklist.

**§19 Manuscript Structure Plan** — Section outline (5–8 sections, flexible) with word budgets. Per-section: goal, key points, gap statement, contributions paragraph.

**§20 Abstract Blueprint** — Sentence-by-sentence abstract structure: background → gap → method → data → main results → significance.

**§21 Title and Framing Options** — 3 candidate titles. Dominant framing (methodological / applied / benchmark / conceptual).

**§22 Citation and Evidence Bank** — Per-section citation plan from LIT_REVIEW_REPORT.md verified citations. Flag unverified citations with `[VERIFY]`.

**§23 Writing Instructions for Downstream Agent** — Non-negotiable writing goals, style instructions, section priorities, writing risks to avoid. Venue-specific tone guidance.

**§24 Open Issues Before Drafting** — Critical gaps, nice-to-have improvements, required follow-up actions with owners and priorities.

**§25 Final Readiness Assessment** — Ready for full/partial/skeleton draft? Minimum conditions for drafting. Recommended drafting strategy.

**§26 Executive Summary for Manuscript Writer** — Concise: what the paper is about, why publishable, strongest/weakest evidence, what to emphasize, what to be careful about.

### Section Count and Word Budget

**IMPORTANT**: The section count is FLEXIBLE (5–8 sections). Choose what fits the content and paper type best. The template sections above are the *planning* schema — the actual manuscript sections in §19 are determined by venue and paper type.

Example word budgets for a 25-page IJGIS paper (~8000 words):

| Section | Words | Notes |
|---|---|---|
| Abstract | 200–250 | Structured: problem, gap, method, data, results, significance |
| Introduction | 800–1000 | 5–6 paragraphs, end with numbered contributions |
| Literature Review | 1500–2000 | 3–4 themed subsections + gap paragraph |
| Study Area & Data | 500–800 | Maps, data tables, preprocessing |
| Methodology | 1200–1500 | Architecture, baselines, evaluation protocol |
| Results | 1000–1200 | Lead with strongest claim |
| Discussion | 700–1000 | Interpretation, comparison, limitations, implications |
| Conclusion | 300–500 | Mirror contributions, future work |

Adjust proportions for ML conferences (heavier methods/experiments, lighter lit review) or applied papers (heavier study area/discussion).

---

## Phase 4: Figure and Table Plan

Consolidate the figure and table plan from §13 and §14 into a single reference table:

```markdown
## Figure & Table Plan

| ID | Type | Description | Data Source | Priority | Status |
|----|------|-------------|-------------|----------|--------|
| Fig 1 | Hero/Architecture | System overview or key comparison | manual/code | HIGH | [Ready/Needed] |
| Fig 2 | Map | Study area with spatial units | GIS data | HIGH | [Ready/Needed] |
| Fig 3 | Line/Bar plot | Main quantitative comparison | output/EXPERIMENT_RESULT.md | HIGH | [Ready/Needed] |
| Fig 4 | Heatmap/Map | Spatial pattern visualization | spatial-analysis/ | MEDIUM | [Ready/Needed] |
| Table 1 | Data summary | Dataset characteristics | DATA_MANIFEST.md | HIGH | [Ready/Needed] |
| Table 2 | Comparison | Main results vs. baselines | EXPERIMENT_RESULT.md | HIGH | [Ready/Needed] |
| Table 3 | Ablation | Component contribution analysis | EXPERIMENT_RESULT.md | MEDIUM | [Ready/Needed] |
```

**For each HIGH-priority figure**, provide:
- Detailed visual specification (axes, colors, annotations)
- Caption draft
- Data source path
- Generation method (Python script / manual / architecture diagram prompt)

Check `output/figures/FIGURE_MANIFEST.md` — if figures already exist from a prior `paper-figure-generate` run, reference them rather than re-planning.

---

## Phase 5: Citation Scaffolding

For each section, list required citations drawn from verified sources:

```markdown
## Citation Plan
- §Intro: [paper1], [paper2], [paper3] (problem motivation)
- §Related: [paper4]-[paper10] (categorized by cluster from §15)
- §Method: [paper11] (baseline), [paper12] (technique we build on)
- §Discussion: [paper13] (comparison point), [paper14] (implication support)
```

**Citation rules**:
1. **NEVER generate BibTeX from memory** — always verify via search or existing .bib files
2. Every citation must be verified: correct authors, year, venue
3. Flag any citation you are unsure about with `[VERIFY]`
4. Prefer published versions over arXiv preprints when available
5. Draw primarily from `output/LIT_REVIEW_REPORT.md` which has already-verified citations
6. For missing citations, use WebSearch to find the correct reference — do not guess

---

## Phase 6: Cross-Review with REVIEWER_MODEL

Send the complete outline to REVIEWER_MODEL for feedback:

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
    5. Page budget feasibility (MAX_PAGES = main body to Conclusion end, excluding refs/appendix for most venues; IEEE venues include refs)
    6. Front-matter strength — are the abstract, introduction, and hero figure plan strong enough for skim-reading reviewers?
    7. Input coverage — does the plan utilize all available upstream artifacts?
    8. Venue fit — does the framing, depth, and emphasis match the target journal's expectations?

    For each weakness, suggest the MINIMUM fix.
    Be specific and actionable — "add X" not "consider more experiments".
```

If Codex MCP is not available, spawn a subagent with fresh context to review the outline instead.

Apply feedback before finalizing. If any score is below 6, address the specific weakness before proceeding.

---

## Phase 7: Self-Check

Before saving, verify all of the following:

- [ ] Every numbered contribution maps to ≥1 row in the Claims-Evidence Matrix (§12)
- [ ] Every claim in the matrix has a source file path (e.g., `EXPERIMENT_RESULT.md §3.2`)
- [ ] Every HIGH-priority figure has a detailed visual specification and caption draft
- [ ] Hero figure description is detailed enough for `paper-figure-generate` to produce it
- [ ] Missing upstream files are documented in §0 "Missing Inputs" and affected sections are marked `[NEEDS: <file>]`
- [ ] Word budgets sum to within ±10% of venue word limit
- [ ] Venue-specific formatting norms are noted (citation style, page counting, appendix rules)
- [ ] No fabricated claims, numbers, or citations exist in the plan
- [ ] §25 readiness assessment accurately reflects the state of available evidence
- [ ] §26 executive summary is actionable for `paper-draft`

If any check fails, fix the plan before writing the final output.

---

## Phase 8: Output

Save the final outline to `output/PAPER_PLAN.md`.

Append a one-line entry to `output/PROJ_NOTES.md`:

```
[YYYY-MM-DD] paper-plan: PAPER_PLAN.md built from [list of consumed input files] — [N] sections, [M] figures, [K] claims, venue=[VENUE]
```

Report back to the user:

```
Paper plan complete:
- Title: [proposed title]
- Venue: [TARGET_VENUE] | Page limit: [MAX_PAGES]
- Sections: [N] ([list names])
- Contributions: [N]
- Claims in evidence matrix: [M] (supported: X, pending: Y)
- Figures planned: [total] (hero: 1, auto: X, manual: Y)
- Tables planned: [Z]
- Input files consumed: [list]
- Missing inputs: [list or "none"]
- Readiness: [full draft / partial draft / skeleton — from §25]

Ready to invoke /paper-figure-generate or /paper-draft.
```

---

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.
- **Do NOT generate author information** — leave author block as placeholder or anonymous.
- **Be honest about evidence gaps** — mark claims as `[NEEDS: evidence]` rather than overclaiming. The downstream `paper-draft` skill will handle these appropriately.
- **Page budget is hard** — if content exceeds MAX_PAGES, suggest what to move to appendix.
- **MAX_PAGES counting differs by venue** — ML conferences: main body to Conclusion end, references/appendix NOT counted. **IEEE venues: references ARE counted toward the page limit.**
- **Venue-specific norms** — ML conferences (ICLR/NeurIPS/ICML) use `natbib` (`\citep`/`\citet`); **IEEE venues use `cite` package (`\cite{}`, numeric style)**; GIScience journals typically use author-year (APA or similar).
- **Claims-Evidence Matrix is the backbone** — every claim must map to evidence, every experiment must support a claim. This matrix is the primary contract between `paper-plan` and `paper-draft`.
- **Front-load the story** — the outline should make the contribution clear in the title, abstract blueprint, introduction plan, and hero figure before the reader reaches the full method.
- **Figures need detailed descriptions** — especially the hero figure, which must clearly specify comparisons and visual expectations.
- **Section count is flexible** — 5–8 sections depending on paper type. Don't force content into a rigid template.
- **NARRATIVE_REPORT.md is the richest source** — if it exists, use it as the primary input and cross-reference other files for verification.
- **Template is the target schema** — follow `templates/PAPER_PLAN_TEMPLATE.md` (§0–§26) as the output structure. Every section should be filled or explicitly marked N/A with a reason.
- **Do NOT generate BibTeX** — citation scaffolding provides keys and context, but actual BibTeX generation belongs to downstream skills.

---

## Composability

### Upstream Skills (produce inputs for this skill)

| Skill | Artifact | How paper-plan uses it |
|---|---|---|
| `lit-review` | `output/LIT_REVIEW_REPORT.md` | Gap analysis, related work themes, verified citations |
| `generate-idea` | `output/IDEA_REPORT.md` | Idea rationale, novelty framing |
| `refine-research` | `output/refine-logs/FINAL_PROPOSAL.md` | Refined method, contributions |
| `experiment-design` | `output/EXPERIMENT_PLAN.md` | Experiment design, success criteria |
| `deploy-experiment` | `output/EXPERIMENT_RESULT.md` | Actual results, metrics |
| `auto-review-loop` | `output/AUTO_REVIEW_REPORT.md` | Reviewer feedback |
| `generate-report` | `output/NARRATIVE_REPORT.md` | Consolidated narrative (preferred primary source) |
| `data-download` | `data/DATA_MANIFEST.md` | Dataset provenance |

### Downstream Skills (consume this skill's output)

| Skill | What it reads | What it does |
|---|---|---|
| `paper-figure-generate` | `output/PAPER_PLAN.md` §13 Figure Plan | Generates publication-quality figures |
| `paper-draft` | `output/PAPER_PLAN.md` (full) | Writes journal-quality manuscript |
| `paper-review-loop` | `output/PAPER_PLAN.md` (claims matrix) | Reviews draft against planned claims |

### Pipeline Context

When invoked as part of `paper-writing-pipeline`, this skill is Phase 1. The pipeline expects `output/PAPER_PLAN.md` to exist after this skill completes.

When invoked standalone, ensure at least one of `RESEARCH_PLAN.md`, `FINAL_PROPOSAL.md`, or `NARRATIVE_REPORT.md` exists — otherwise the skill has insufficient context to build a meaningful plan.

---

## Acknowledgements

Outline methodology inspired by [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) (claim-evidence mapping), [claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) (citation verification), and [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) (claim verification protocol). Template structure follows the §0–§26 schema from `templates/PAPER_PLAN_TEMPLATE.md`.
