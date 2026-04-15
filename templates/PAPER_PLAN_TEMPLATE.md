# PAPER_PLAN.md

> Purpose: This file consolidates all information needed for a manuscript-writing agent to draft a full, high-quality paper for the target journal.  
> Rule: Be explicit, concrete, and evidence-based. Do not leave important claims unsupported.  
> Writing agent instruction: Use this file as the primary planning document and consult the referenced source files for supporting details, exact numbers, and evidence.

---

## 0. Document Status

- **Plan version**: [v0.1]
- **Last updated**: [YYYY-MM-DD]
- **Project codename**: [PROJECT_NAME]
- **Plan owner / generating agent**: [AGENT_NAME]
- **Target journal**: [JOURNAL_NAME]
- **Manuscript type**: [Research Article / Review / Methods Paper / Short Communication / Perspective]
- **Readiness level**: [Idea stage / Experiment complete / Ready for draft / Needs validation]
- **Overall confidence**: [High / Medium / Low]

### Input Files Used
List all upstream files that informed this plan.

- `literature_review/...`
- `idea_discovery/...`
- `experiment_plan/...`
- `experiment_results/...`
- `figures/...`
- `tables/...`
- `notes/...`

### Missing or Unread Inputs
- [ ]
- [ ]
- [ ]

---

## 1. One-Paragraph Paper Summary

### Working Title
[Proposed manuscript title]

### One-Sentence Paper Claim
[State the central claim in one sentence. This should be specific, defensible, and evidence-based.]

### Short Abstract-Style Summary
[Provide a 150–250 word summary covering: problem, gap, method, data, main findings, and significance.]

### Keywords
- [keyword 1]
- [keyword 2]
- [keyword 3]
- [keyword 4]
- [keyword 5]

---

## 2. Target Journal Strategy

### Journal Fit
- **Why this journal is appropriate**:
  - [Reason 1]
  - [Reason 2]
  - [Reason 3]

### Audience
[Describe the expected readership and how the paper should be framed for them.]

### Journal Expectations
Summarize the likely expectations for this journal.

- **Theoretical depth needed**: [Low / Moderate / High]
- **Methodological rigor needed**: [Low / Moderate / High]
- **Application emphasis**: [Low / Moderate / High]
- **Interpretability / explainability expectations**: [ ]
- **Reproducibility expectations**: [ ]
- **Societal implications expected**: [ ]
- **Typical article tone/style**: [ ]

### Alignment Notes for Writing Agent
[Explain how the paper should be positioned to match the journal’s style, scope, and editorial preferences.]

---

## 3. Research Context and Motivation

### Broad Problem
[What larger scientific or practical problem does this paper address?]

### GIScience / GeoAI Context
[Explain the problem specifically in GIScience, GeoAI, remote sensing, spatial data science, or related fields.]

### Why This Matters
Cover scientific, methodological, and societal relevance.

- **Scientific importance**:
- **Methodological importance**:
- **Practical importance**:
- **Societal importance**:

### Motivation Narrative
[Provide the motivating story for the paper. Why should readers care now?]

---

## 4. Research Gap

### Existing State of the Literature
[Summarize the current state of the field based on literature review files.]

### Specific Gaps
List the exact unresolved gaps this paper addresses.

1. [Gap 1]
2. [Gap 2]
3. [Gap 3]

### Why Existing Work Is Insufficient
For each gap, explain why prior work does not fully solve it.

- **Gap 1 insufficiency**:
- **Gap 2 insufficiency**:
- **Gap 3 insufficiency**:

### Gap Evidence
Reference the literature or notes supporting the gap.

- [Citation / source file / note]
- [Citation / source file / note]
- [Citation / source file / note]

---

## 5. Novelty and Contributions

### Core Novelty Statement
[State clearly what is new in this paper.]

### Contribution List
Use strong, precise, publication-ready language.

1. [Contribution 1]
2. [Contribution 2]
3. [Contribution 3]
4. [Contribution 4]

### Contribution Types
Mark the nature of the contribution.

- [ ] New theory or conceptual framing
- [ ] New dataset
- [ ] New method / model / algorithm
- [ ] New benchmark or evaluation protocol
- [ ] New system / platform / agent
- [ ] New empirical findings
- [ ] New application to an important domain
- [ ] New insight into GIScience / GeoAI practice
- [ ] New reproducibility / interpretability / ethics framework

### What This Paper Is *Not* Claiming
[Clarify boundaries to avoid overstating novelty.]

### Differentiation from Prior Work
Summarize the nearest competing or related approaches and how this work differs.

| Prior Work | Similarity | Key Difference | Why Our Work Matters More |
|---|---|---|---|
| [Paper / system] | [ ] | [ ] | [ ] |
| [Paper / system] | [ ] | [ ] | [ ] |
| [Paper / system] | [ ] | [ ] | [ ] |

---

## 6. Research Questions and Hypotheses

### Main Research Question
[RQ1]

### Secondary Research Questions
- [RQ2]
- [RQ3]
- [RQ4]

### Hypotheses (if applicable)
- **H1**: [ ]
- **H2**: [ ]
- **H3**: [ ]

### Expected Answers
[Summarize what the paper is expected to show.]

---

## 7. Study Scope and Boundaries

### Spatial Scope
[Study area, geographic extent, spatial units, projection assumptions if relevant]

### Temporal Scope
[Time range, temporal resolution, period of analysis]

### Data Scope
[What data types are included and excluded?]

### Method Scope
[What method families are in scope?]

### Boundary Conditions
[Under what conditions do the claims hold?]

### Explicit Limitations of Scope
- [ ]
- [ ]
- [ ]

---

## 8. Data and Materials

### Datasets Used
For each dataset, fill in as much detail as possible.

#### Dataset 1
- **Name**:
- **Source**:
- **Access method**:
- **Spatial coverage**:
- **Temporal coverage**:
- **Resolution / granularity**:
- **Variables used**:
- **Preprocessing applied**:
- **Known limitations**:
- **License / usage constraints**:

#### Dataset 2
- **Name**:
- **Source**:
- **Access method**:
- **Spatial coverage**:
- **Temporal coverage**:
- **Resolution / granularity**:
- **Variables used**:
- **Preprocessing applied**:
- **Known limitations**:
- **License / usage constraints**:

### Data Integration Strategy
[Explain how datasets are aligned, joined, cleaned, harmonized, georeferenced, or transformed.]

### Data Quality Notes
[Missingness, bias, uncertainty, class imbalance, geospatial inconsistencies, temporal mismatch, etc.]

### Ethics / Privacy / Responsible Use
[Discuss any privacy, fairness, representativeness, or ethical issues.]

---

## 9. Methodological Plan

### Overall Method Summary
[Give a concise but complete overview of the workflow.]

### Workflow Stages
1. [Stage 1]
2. [Stage 2]
3. [Stage 3]
4. [Stage 4]

### Method Details
Describe each component precisely enough for manuscript drafting.

#### 9.1 Problem Formulation
- **Task definition**:
- **Input**:
- **Output**:
- **Prediction / inference target**:
- **Unit of analysis**:

#### 9.2 Preprocessing
- **Cleaning**:
- **Transformation**:
- **Normalization / scaling**:
- **Feature engineering**:
- **Spatial processing**:
- **Temporal processing**:
- **Text / image / multimodal preprocessing**:

#### 9.3 Model / Analytical Method
- **Method name**:
- **Architecture / algorithm**:
- **Why chosen**:
- **Key parameters**:
- **Training strategy**:
- **Inference strategy**:

#### 9.4 Baselines / Comparators
| Baseline | Type | Why Included | Expected Role |
|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] |
| [ ] | [ ] | [ ] | [ ] |

#### 9.5 Experimental Design
- **Train/validation/test split**:
- **Cross-validation**:
- **Ablation settings**:
- **Sensitivity analysis**:
- **Robustness checks**:
- **Statistical tests**:

#### 9.6 GIScience / Spatial Analysis Components
- **Spatial unit**:
- **Spatial relationships modeled**:
- **Spatial dependency considerations**:
- **Projection / CRS handling**:
- **Spatial autocorrelation handling**:
- **MAUP / scale effects considered?**:
- **Spatial uncertainty considered?**:

#### 9.7 Implementation Details
- **Programming language(s)**:
- **Packages / frameworks**:
- **Hardware / compute environment**:
- **Runtime considerations**:
- **Reproducibility notes**:

---

## 10. Experiments

### Experiment Inventory
List every experiment that matters for the paper.

| Experiment ID | Purpose | Input / Setting | Output / Metric | Status | Include in paper? |
|---|---|---|---|---|---|
| EXP-1 | [ ] | [ ] | [ ] | [Complete / Partial / Missing] | [Yes/No] |
| EXP-2 | [ ] | [ ] | [ ] | [Complete / Partial / Missing] | [Yes/No] |
| EXP-3 | [ ] | [ ] | [ ] | [Complete / Partial / Missing] | [Yes/No] |

### Main Experiments
Describe the flagship experiments that support the core claims.

#### Experiment [ID]
- **Purpose**:
- **Setup**:
- **Key variables**:
- **Metrics**:
- **Expected interpretation**:
- **Result file(s)**:

### Ablation Studies
[Summarize which components are removed or varied and why.]

### Sensitivity / Robustness Studies
[Describe tests for stability across parameters, locations, time windows, seeds, or datasets.]

### Error Analysis
[Summarize how errors are analyzed and what categories matter.]

---

## 11. Results Summary

### Main Findings
List the headline findings in priority order.

1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

### Quantitative Results
Fill in exact values when available.

| Result ID | Finding | Metric | Value | Comparison | Interpretation |
|---|---|---|---|---|---|
| R1 | [ ] | [ ] | [ ] | [ ] | [ ] |
| R2 | [ ] | [ ] | [ ] | [ ] | [ ] |
| R3 | [ ] | [ ] | [ ] | [ ] | [ ] |

### Spatial / Visual Findings
[Describe any spatial patterns, maps, clusters, or geospatial insights.]

### Qualitative Findings
[Summarize qualitative, interpretive, or case-based findings if applicable.]

### Negative or Mixed Findings
[Document results that did not work, including why they still matter.]

### Statistical Strength
- **Significance tested?** [Yes/No]
- **Effect sizes available?** [Yes/No]
- **Confidence intervals available?** [Yes/No]
- **Uncertainty quantified?** [Yes/No]

---

## 12. Claim-to-Evidence Map

Every major paper claim should be tied to direct evidence.

| Claim ID | Claim | Supporting Evidence | Figure/Table | Experiment | Confidence |
|---|---|---|---|---|---|
| C1 | [ ] | [ ] | [ ] | [ ] | [High/Medium/Low] |
| C2 | [ ] | [ ] | [ ] | [ ] | [High/Medium/Low] |
| C3 | [ ] | [ ] | [ ] | [ ] | [High/Medium/Low] |

### Unsupported or Weak Claims
- [Claim needing stronger support]
- [Claim needing validation]
- [Claim that should be softened]

---

## 13. Figures Plan

### Figure Inventory
| Figure No. | Tentative Title | Purpose | Data Source | Status | Priority |
|---|---|---|---|---|---|
| Fig. 1 | [ ] | [ ] | [ ] | [Ready / Needs revision / Missing] | [High/Med/Low] |
| Fig. 2 | [ ] | [ ] | [ ] | [Ready / Needs revision / Missing] | [High/Med/Low] |
| Fig. 3 | [ ] | [ ] | [ ] | [Ready / Needs revision / Missing] | [High/Med/Low] |

### Figure Draft Notes
For each figure, explain what it should show and why it matters.

#### Figure 1
- **Purpose**:
- **Visual type**:
- **Key message**:
- **Required annotations**:
- **Source file**:

#### Figure 2
- **Purpose**:
- **Visual type**:
- **Key message**:
- **Required annotations**:
- **Source file**:

---

## 14. Tables Plan

### Table Inventory
| Table No. | Tentative Title | Purpose | Status | Priority |
|---|---|---|---|---|
| Table 1 | [ ] | [ ] | [ ] | [ ] |
| Table 2 | [ ] | [ ] | [ ] | [ ] |
| Table 3 | [ ] | [ ] | [ ] | [ ] |

### Required Tables
- **Dataset summary table**: [Yes/No]
- **Baseline comparison table**: [Yes/No]
- **Ablation table**: [Yes/No]
- **Hyperparameter/configuration table**: [Yes/No]
- **Error analysis table**: [Yes/No]

---

## 15. Related Work Synthesis

### Related Work Clusters
Group the literature in a way suitable for manuscript writing.

#### Cluster 1: [Name]
- **Summary**:
- **Representative studies**:
- **How our work relates**:
- **How our work differs**:

#### Cluster 2: [Name]
- **Summary**:
- **Representative studies**:
- **How our work relates**:
- **How our work differs**:

#### Cluster 3: [Name]
- **Summary**:
- **Representative studies**:
- **How our work relates**:
- **How our work differs**:

### Literature Positioning Strategy
[Explain how the introduction and related work should frame this paper against existing studies.]

### Papers That Must Be Cited
- [ ]
- [ ]
- [ ]
- [ ]

---

## 16. Discussion Plan

### Interpretation of Main Findings
[Explain what the results mean, not just what they are.]

### Why the Method Works
[Mechanistic, conceptual, or empirical explanation.]

### GIScience / GeoAI Implications
[What does this change for the field?]

### Practical Implications
[Operational, policy, disaster management, geospatial workflow, education, etc.]

### Responsible Research Considerations
Address any relevant issues.

- **Bias / fairness**:
- **Privacy / geoprivacy**:
- **Transparency / interpretability**:
- **Reproducibility / replicability**:
- **Limitations of foundation models / LLMs / generative AI**:
- **Societal risks**:

### Generalizability
[Discuss what settings the findings may transfer to.]

---

## 17. Limitations and Future Work

### Known Limitations
1. [Limitation 1]
2. [Limitation 2]
3. [Limitation 3]

### Severity of Limitations
| Limitation | Severity | Impact on Claims | How to Phrase in Paper |
|---|---|---|---|
| [ ] | [Low/Med/High] | [ ] | [ ] |
| [ ] | [Low/Med/High] | [ ] | [ ] |

### Future Work Directions
- [ ]
- [ ]
- [ ]

---

## 18. Reproducibility and Open Science Plan

### Code Availability
- **Repository path / URL placeholder**:
- **Public or private**:
- **Planned release timing**:

### Data Availability
- **Public datasets**:
- **Restricted datasets**:
- **Derived data to release**:

### Reproducibility Assets
- [ ] Environment file
- [ ] Data processing scripts
- [ ] Training / inference scripts
- [ ] Evaluation scripts
- [ ] Figure generation scripts
- [ ] README
- [ ] Model weights
- [ ] Prompt / agent workflow files

### Replication Risks
[Document dependencies, unstable APIs, costly compute, licensing issues, etc.]

---

## 19. Manuscript Structure Plan

### Recommended Section Outline
1. Introduction
2. Related Work
3. Study Area / Data
4. Methodology
5. Experiments
6. Results
7. Discussion
8. Limitations
9. Conclusion

### Section-by-Section Content Plan

#### 19.1 Introduction
- **Goal of section**:
- **Key points to include**:
- **Gap statement to end with**:
- **Contributions paragraph content**:

#### 19.2 Related Work
- **Main clusters**:
- **What to emphasize**:
- **What to avoid**:

#### 19.3 Data / Study Area
- **Datasets to describe**:
- **Spatial/temporal setting**:
- **Data quality caveats**:

#### 19.4 Methodology
- **Core method components**:
- **Baselines**:
- **Implementation details to include**:

#### 19.5 Experiments / Results
- **Ordering of experiments**:
- **Headline result first?** [Yes/No]
- **Ablation placement**:
- **Robustness placement**:

#### 19.6 Discussion
- **Interpretive themes**:
- **Broader implications**:
- **Responsible GIScience / GeoAI implications**:

#### 19.7 Conclusion
- **Take-home message**:
- **Final significance statement**:

---

## 20. Abstract Blueprint

### Abstract Structure
- **Background / problem**:
- **Gap**:
- **Method**:
- **Data / case study**:
- **Main results**:
- **Significance**:

### Draft Abstract Sentences
1. [Sentence 1]
2. [Sentence 2]
3. [Sentence 3]
4. [Sentence 4]
5. [Sentence 5]

---

## 21. Title and Framing Options

### Candidate Titles
1. [Title option 1]
2. [Title option 2]
3. [Title option 3]

### Preferred Framing
Choose the dominant framing.

- [ ] Methodological innovation
- [ ] System / agent innovation
- [ ] GIScience conceptual contribution
- [ ] Applied GeoAI case study
- [ ] Benchmark / evaluation contribution
- [ ] Responsible AI / responsible GIScience contribution

### Recommended Final Framing
[Explain which framing is strongest for publication.]

---

## 22. Citation and Evidence Bank

### Core Citations by Section

#### Introduction
- [Citation 1] — [why it matters]
- [Citation 2] — [why it matters]

#### Related Work
- [Citation 1] — [why it matters]
- [Citation 2] — [why it matters]

#### Methods
- [Citation 1] — [why it matters]
- [Citation 2] — [why it matters]

#### Discussion
- [Citation 1] — [why it matters]
- [Citation 2] — [why it matters]

### Citations Requiring Careful Verification
- [ ]
- [ ]
- [ ]

### Claims That Need Supporting Citations
- [ ]
- [ ]
- [ ]

---

## 23. Writing Instructions for Downstream Manuscript Agent

### Non-Negotiable Writing Goals
- Maintain a formal academic tone suitable for [TARGET JOURNAL].
- Be precise and evidence-based.
- Do not overclaim novelty.
- Tie each major claim to explicit evidence.
- Highlight GIScience / GeoAI significance throughout.
- Preserve methodological clarity and reproducibility.
- Explicitly acknowledge limitations.

### Style Instructions
- Prefer [concise / detailed / theory-driven / application-driven] writing.
- Use terminology consistently.
- Avoid vague adjectives unless supported.
- Use exact metric values whenever available.
- Prioritize logical flow over decorative language.

### Section Priorities
- **Most important section to get right**:
- **Section requiring strongest persuasion**:
- **Section needing the most technical detail**:
- **Section most sensitive to reviewer criticism**:

### Writing Risks to Avoid
- [ ] Overstating novelty
- [ ] Weak gap articulation
- [ ] Insufficient baseline comparison
- [ ] Missing spatial reasoning
- [ ] Inadequate limitation discussion
- [ ] Unsupported claims
- [ ] Poor journal fit in tone or framing

---

## 24. Open Issues Before Drafting

### Critical Gaps
List issues that may prevent a strong manuscript draft.

1. [ ]
2. [ ]
3. [ ]

### Nice-to-Have Improvements
- [ ]
- [ ]
- [ ]

### Required Follow-Up Actions
| Action | Owner | Priority | Status |
|---|---|---|---|
| [ ] | [ ] | [High/Med/Low] | [ ] |
| [ ] | [ ] | [High/Med/Low] | [ ] |

---

## 25. Final Readiness Assessment

### Ready for Full Draft?
- [ ] Yes
- [ ] No
- [ ] Partially

### If Not Ready, Why Not?
[Explain what is missing.]

### Minimum Conditions for Drafting
- [ ]
- [ ]
- [ ]

### Recommended Drafting Strategy
- [ ] Draft full manuscript now
- [ ] Draft introduction + related work first
- [ ] Draft methods/results first
- [ ] Wait for missing experiments
- [ ] Wait for figures/tables cleanup

---

## 26. Executive Summary for Manuscript Writer

Provide a concise summary that the writing agent can immediately act on.

### What the paper is about
[ ]

### Why it is publishable
[ ]

### What evidence is strongest
[ ]

### What evidence is weakest
[ ]

### What the writer should emphasize most
[ ]

### What the writer should be careful about
[ ]

---