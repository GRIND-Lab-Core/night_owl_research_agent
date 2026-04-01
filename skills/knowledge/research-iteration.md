# Research Iteration Skill — Autoresearch-Inspired Iterative Loop

**Last Updated:** 2026-03-13
**Maintainer:** Research Agent — GeoAI Lab

---

## 1. Philosophy

The iterative research loop is founded on three principles:

**Principle 1 — Testability.** Every hypothesis and every written section must be evaluated against an objective, pre-specified metric before it is accepted. Subjective impressions ("this looks good") are insufficient. The metric defines progress.

**Principle 2 — Quality over quantity.** It is better to produce one excellent, fully reasoned, well-cited section at score 9 than three mediocre sections at score 5. Reviewers reward depth and precision. Incomplete coverage is a correctible gap; weak reasoning is a fundamental problem.

**Principle 3 — Transparent state.** At all times, the system (human + agent) should know: what has been completed, at what score, in how many iterations, and what remains. This is tracked in MEMORY.md and surfaced at the start of every session.

---

## 2. The Iterative Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCH ITERATION LOOP                  │
│                                                             │
│  [1] PROPOSE       Define the section/hypothesis to work on │
│         ↓                                                   │
│  [2] WRITE         Draft the section or execute hypothesis  │
│         ↓                                                   │
│  [3] SCORE         Apply the scoring rubric (0-10, 5 dim.)  │
│         ↓                                                   │
│  [4] ACCEPT?       Score ≥ 7? → Accept and commit          │
│       / \          Score < 7? → Diagnose and revise        │
│     YES   NO                                               │
│      ↓     ↓                                               │
│  [5] COMMIT  [REVISE] → return to [2]                      │
│         ↓                                                   │
│  [6] NEXT SECTION                                           │
└─────────────────────────────────────────────────────────────┘
```

### Step 1 — PROPOSE
Select the next section or hypothesis to work on based on:
- Current paper outline (what section is next in sequence?)
- Dependency: can this section be written before dependencies are completed? (e.g., Results requires Methods to be complete)
- Priority: which gap in the current draft is most critical to address?

Output of PROPOSE step: a one-paragraph description of the section goal, target length, key claims it must make, and the primary literature it must engage.

### Step 2 — WRITE
Produce the draft. For writing tasks: use academic-writing.md templates as scaffolding. For research tasks (literature synthesis, gap analysis, hypothesis generation): use domain knowledge base and literature-mining.md protocols.

The first draft is not expected to be perfect. It must: (a) address the stated goal, (b) be the correct length, (c) contain all required structural elements (claims, evidence, transitions), even if imperfectly.

### Step 3 — SCORE
Apply the full scoring rubric (see Section 3 below). Score each of the 5 dimensions; calculate composite score. Document the score in MEMORY.md.

### Step 4 — ACCEPT or REVISE
- If composite score ≥ 7.0: accept the section. Proceed to COMMIT.
- If composite score 5.0–6.9: identify the weakest dimensions (score < 6), diagnose the specific issue, revise only the identified weaknesses, re-score.
- If composite score < 5.0: do NOT attempt minor edits. Diagnose root cause (wrong framing? insufficient literature? missing data?). Rewrite from the PROPOSE step.

### Step 5 — COMMIT
After acceptance:
1. Finalize text (proofread, fix formatting, confirm citations are correct APA format)
2. Append to the paper document
3. Run: `git add [paper_file]`
4. Run: `git commit -m "section: [section_name] score:[X.X] iter:[n]"`
5. Update MEMORY.md with section completion record

### Step 6 — NEXT SECTION
Load the next unfinished section from the paper outline. If all sections complete, proceed to integration review (check cross-section consistency, internal citations, figure/table references).

---

## 3. Section Scoring Rubric (0-10)

### 3.1 Overall Score Interpretation

| Score | Interpretation | Action |
|---|---|---|
| 9-10 | Publishable as-is; exceptional clarity, contribution, and rigor | Accept immediately; commit |
| 7-8 | Solid; minor polish needed (typos, small citation gaps, minor clarity) | Accept with light editing; commit |
| 5-6 | Core content present; major gaps OR significant clarity issues | Revise targeted weaknesses |
| 3-4 | Incomplete; missing key structural elements or critical evidence | Major revision; likely rewrite |
| 1-2 | Needs complete rewrite; wrong framing, wrong content, or wrong approach | Stop; re-PROPOSE from scratch |

### 3.2 Dimension-Specific Scoring

#### Dimension 1 — NOVELTY (0-10)

| Score | Description |
|---|---|
| 9-10 | Paradigm-shifting contribution; opens a new subfield or fundamentally changes how a problem is solved |
| 7-8 | Meaningfully novel; clearly extends state-of-the-art in a way that is not incremental |
| 5-6 | Novel combination of existing ideas; some new element but the core insight is not surprising |
| 3-4 | Largely incremental; applies existing methods to a slightly different dataset or context |
| 1-2 | Essentially a reproduction or replication of prior work without new insight |

**Assessment protocol:** compare the stated contribution against the gap analysis from the literature review. If the gap was explicitly identified in a prior survey paper, novelty is limited. If the gap was not identified in the literature, score higher.

#### Dimension 2 — RIGOR (0-10)

| Score | Description |
|---|---|
| 9-10 | Fully reproducible; code and data available; statistical tests with p-values and CIs; spatial CV; ablation study; multiple datasets |
| 7-8 | Strong methodology; most reproducibility elements present; minor gaps (e.g., no code release) |
| 5-6 | Core methodology described; missing some elements (random seeds, hardware specs, or significance tests) |
| 3-4 | Methodology unclear in key areas; cannot fully reproduce; missing baselines |
| 1-2 | No methodological detail; impossible to evaluate or reproduce |

**Assessment protocol:** run the reproducibility checklist from academic-writing.md (methodology section). Count missing elements; each missing critical element reduces by 0.5-1.0 points.

#### Dimension 3 — LITERATURE (0-10)

| Score | Description |
|---|---|
| 9-10 | Comprehensive; recent (2020+); thematically organized; critical synthesis (not just listing); ≥30 papers for full article |
| 7-8 | Solid coverage; organized by theme; minor gaps in coverage or recency |
| 5-6 | Adequate coverage; organized but partially chronological; some important papers missing |
| 3-4 | Thin coverage; <15 papers; many foundational papers missing; organized as annotation not synthesis |
| 1-2 | Essentially uncited; or citations are irrelevant/incorrect |

**Assessment protocol:** check against domain-knowledge.md landmark papers list. Missing any landmark paper in the relevant subfield: -0.5 per paper. No synthesis table: -0.5. Exclusively chronological organization: -1.0.

#### Dimension 4 — CLARITY (0-10)

| Score | Description |
|---|---|
| 9-10 | Every sentence is unambiguous; textbook-clear; technical terms defined; logical flow throughout |
| 7-8 | Clear to a knowledgeable reader; minor ambiguous phrases or jargon issues |
| 5-6 | Generally understandable but several confusing passages; some undefined terms |
| 3-4 | Significant comprehension barriers; reader must guess at meaning of key claims |
| 1-2 | Incomprehensible; major structural or linguistic issues |

**Assessment protocol:** read each paragraph aloud. Mark any sentence requiring re-reading. More than 2 re-readings in one paragraph: score drops below 7. More than 5 across the section: score drops below 5.

#### Dimension 5 — IMPACT (0-10)

| Score | Description |
|---|---|
| 9-10 | Field-changing; will be widely cited; addresses a problem that many researchers face; strong practical implications |
| 7-8 | Significant contribution; will be cited by those in the subfield; clear practical or scientific value |
| 5-6 | Modest impact; niche relevance; unclear why the broader field should care |
| 3-4 | Limited impact; addresses a very minor problem; practical value is unclear |
| 1-2 | Negligible impact; trivial problem or solution |

**Assessment protocol:** ask "Who is waiting for this paper?" If the answer is fewer than 50 researchers globally, the impact score is likely ≤ 4. If this could influence regulatory practice, policy, or widely-used tools, score higher.

### 3.3 Composite Score Calculation

```
Composite = (Novelty × 0.25) + (Rigor × 0.25) + (Literature × 0.20) + (Clarity × 0.20) + (Impact × 0.10)
```

Weight rationale: Novelty and Rigor are the two dimensions reviewers weight most heavily. Literature and Clarity are table stakes for publication. Impact is important but partially outside the author's control.

**Dimensional floor rule:** if ANY single dimension scores ≤ 3, the section cannot be accepted regardless of composite score. Each dimension must meet a minimum of 4.0 for an acceptance.

---

## 4. Improvement Strategies by Dimension

### 4.1 Improving Novelty

- Re-read the gap analysis and ensure the introduction explicitly states why this gap exists (not just that it exists)
- Compare your method with the 3 most recent papers doing the most similar thing: be specific about what is different
- If incrementally novel: expand scope (add a new modality, a new region, a new evaluation task) to strengthen novelty claim
- If novelty is genuine but not communicated: rewrite the contribution statement to be more specific and direct

### 4.2 Improving Rigor

- Run the reproducibility checklist: add missing hyperparameters, seeds, hardware specs
- Add spatial cross-validation if standard CV was used
- Add ablation table removing each component of your method
- Add statistical significance tests (permutation test, bootstrap CI)
- Add a second dataset or geographic region for generalizability assessment

### 4.3 Improving Literature

- Run a fresh Semantic Scholar search for the 3 core themes; add any papers from last 18 months
- Check literature against landmark papers in domain-knowledge.md; add any missing
- Reorganize from chronological to thematic if needed
- Add synthesis table comparing all reviewed methods
- Write explicit gap paragraph summarizing what prior work cannot do

### 4.4 Improving Clarity

- Restructure any paragraph that makes more than one main claim
- Define all acronyms and domain-specific terms at first use
- Break sentences longer than 40 words into multiple sentences
- Add signposting sentences at the start of each paragraph ("In this section, we address...")
- Use parallel grammatical structure in all lists

### 4.5 Improving Impact

- Quantify the downstream application ("This enables real-time flood mapping for X million people at risk")
- Add a practical implications paragraph in the Discussion
- Connect findings to policy-relevant frameworks (Sendai, EPA NAAQS, WHO guidelines)
- Consider adding a worked example or case study to demonstrate real-world utility
- If impact is genuinely limited, consider combining with another manuscript component where the findings contribute more substantively

---

## 5. Iteration Budget

**Maximum 5 iterations per section.** This prevents indefinite cycling on a problematic section.

**Stopping rule:** if a section has been revised 3 times and the composite score has not improved by at least 0.3 per iteration, stop and flag for human review. Do not continue revising in the same direction.

**Score trajectory tracking:**

```
Section: Introduction
Iter 1: Novelty=5, Rigor=4, Lit=6, Clarity=6, Impact=5 → Composite=5.2
Iter 2: Novelty=6, Rigor=5, Lit=7, Clarity=7, Impact=6 → Composite=6.2 (+1.0 ✓)
Iter 3: Novelty=7, Rigor=6, Lit=8, Clarity=8, Impact=7 → Composite=7.2 (+1.0 ✓)
→ ACCEPT at Iter 3
```

If Iter 3 = 6.0, Iter 4 = 6.1, Iter 5 = 6.2 → score is not improving meaningfully → FLAG FOR HUMAN.

---

## 6. Git Workflow

After each accepted section:

```bash
# Stage the paper file
git add [paper_filename].md

# Commit with structured message
git commit -m "section: [section_name] score:[X.X] iter:[n]

[one-line description of key improvement made in final iteration]"
```

**Commit message examples:**
- `section: introduction score:7.4 iter:3 — added spatial equity framing and explicit gap statement`
- `section: methodology score:8.1 iter:2 — added spatial cross-validation protocol and hardware specs`
- `section: results score:7.8 iter:1 — first draft accepted; strong quantitative results table`

**Branch strategy:**
- `main`: stable, accepted sections only
- `draft/[section_name]`: working branch for each section
- Merge to main after acceptance and git commit

---

## 7. State Tracking

**MEMORY.md sections to update after every session:**
1. Current Research State: update paper stage and timestamp
2. Section Scores: append new row with (section, iter, composite score, dimension scores)
3. Patterns Learned: note any recurring issue (e.g., "literature section consistently under-scores on recency — check 2024-2026 papers more aggressively")
4. API Notes: log any useful Semantic Scholar queries that yielded high-relevance results

**State summary format (update at session end):**

```markdown
## Session Summary — [DATE]
- Completed: [section] at score [X.X] in [n] iterations
- Next: [next section]
- Blockers: [any issues requiring human input]
- PRISMA update: [n papers added to corpus]
```

---

## 8. When to Escalate to Human

Escalation is required (do not continue autonomously) when:

1. **Score stuck below 5.0 after 3 iterations** — fundamental issue with framing, data, or method that requires researcher judgment
2. **Contradictory reviewer feedback** — two reviewers make incompatible requests (expand Section X vs. shorten Section X) — researcher must decide priority
3. **Missing data that cannot be retrieved** — a key baseline result is not reported in the original paper and the paper is behind paywall — researcher must obtain through institutional access or contact author
4. **Novel finding that may change the paper's contribution** — literature search reveals a very recent paper (post-search) that closely overlaps with the proposed contribution — researcher must reassess novelty and scope
5. **Ethical or EJ concerns** — analysis reveals potential disparate impact; researcher must decide whether to add equity analysis, modify scope, or acknowledge limitation
6. **Authorship and collaboration decisions** — which collaborators should be listed, what order, what contributions — always human decision
