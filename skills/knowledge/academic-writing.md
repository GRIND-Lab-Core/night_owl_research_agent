# Academic Writing Skill — GeoAI and Geography Papers

**Last Updated:** 2026-03-13
**Maintainer:** Research Agent — GeoAI Lab

---

## 1. IMRAD Structure

**IMRAD** = Introduction, Methods, Results, And Discussion.

The standard structure for empirical research papers in natural sciences, engineering, and quantitative social science. GeoAI and geography papers overwhelmingly follow IMRAD.

**When IMRAD applies:**
- Empirical studies with new data collection, processing, or modeling
- Methodological papers proposing a new algorithm or framework
- Applied studies testing a GeoAI method on a real-world problem

**When to deviate:**
- Conceptual/theoretical papers (may not have Results/Discussion in the traditional sense)
- Review papers (Literature Review replaces Methods; Synthesis replaces Results)
- Short communications / letters (compressed structure; Methods may be in SI)
- Data papers (Data Descriptor format: data sources, quality, reuse potential)

**Typical word counts by journal type:**
- Full research article: 6,000-10,000 words (body text, excluding references)
- Letter / short communication: 2,500-4,000 words
- Review article: 8,000-15,000 words
- Data descriptor: 3,000-5,000 words

---

## 2. Section-Specific Guidance

### 2.1 Abstract

**Length:** 150-250 words for most journals; some allow 300. Always check journal guidelines. Structured abstracts (Background / Objective / Methods / Results / Conclusions) are required by some journals (EHP, GeoHealth) and recommended everywhere.

**Self-containment rule:** the abstract must be interpretable without reading the paper. Do not use abbreviations not defined within the abstract, do not cite specific figures or tables, do not use footnotes.

**What each sentence must accomplish:**
- Sentence 1-2: Frame the broad problem. Why does this topic matter to someone outside your subfield?
- Sentence 3-4: The specific gap. What does existing work fail to do that this paper addresses?
- Sentence 5: The objective. What does this paper do? Use action verbs: "We develop," "We propose," "We evaluate."
- Sentence 6-8: Methods summary. What data? What method? Where applied? Keep this concrete.
- Sentence 9-11: Key quantitative results. Include at least one specific number (accuracy, improvement %, error metric).
- Sentence 12-13: Conclusion. What does this mean for the field? What is the practical or scientific contribution?

**Common abstract errors:**
- Vague objectives: "We investigate the potential of AI for disaster response" — never say what you specifically did
- Missing numbers: "Our method achieves high accuracy" — meaningless without the value
- Contradiction with paper: the abstract says F1=0.91 but the paper reports F1=0.89 in Table 2 — always reconcile
- Over-claiming: "Our model is the best" — say "outperforms [specific baseline] by X% on [specific benchmark]"

### 2.2 Introduction

**Target length:** 800-1,200 words (3-5 paragraphs for most journals; up to 7 for reviews).

**Funnel structure:** broad → specific → contribution.

**Paragraph 1 — The broad problem:** Why is this topic important to society or science? A reader who is not a specialist in your subfield should understand why this matters. Use active framing: "Floods cause X deaths and $Y billion in damages annually..." not "There has been increasing interest in flood modeling."

**Paragraph 2 — Scale and significance:** Quantify the problem. Numbers build urgency and anchor reviewers in the real-world stakes. Reference authoritative sources (UN, WHO, IPCC, USGS reports).

**Paragraph 3 — Current approaches and their shortcomings:** Brief synthesis of the state of the field. This is NOT a literature review — it is a strategic summary that builds toward the gap. Use themes, not chronology. End this paragraph by setting up what is missing.

**Paragraph 4 — The gap:** "Despite these advances, [specific limitation] remains unaddressed because [reason]." Be precise: "no prior work has simultaneously used SAR and optical imagery with a unified encoder for multi-hazard damage assessment in low-income regions" is a defensible gap. "More research is needed" is not.

**Paragraph 5 — Your contribution:** "To address this gap, we propose [method name]..." Use clear, direct language. Do not be modest here — reviewers and readers need to understand immediately what you did.

**Contributions list:** Number your contributions explicitly. 3-5 contributions is typical. Each contribution should be:
- Specific (what exactly did you contribute)
- Novel (why is this new)
- Verifiable (how will the reader know you achieved it)

Good example: "(1) We propose XYZ-Net, a Siamese transformer architecture that jointly processes pre- and post-event Sentinel-1 SAR pairs for building damage classification without requiring optical imagery."

Bad example: "(1) We make a contribution to disaster mapping."

**Final paragraph — Paper organization:** "The remainder of this paper is organized as follows. Section 2 reviews related work. Section 3 describes [study area, data, and methods]. Section 4 presents experimental results. Section 5 discusses implications and limitations. Section 6 concludes." This sentence is formulaic and that is fine — readers expect it.

### 2.3 Literature Review

**Organization principle:** NEVER organize chronologically. Organize thematically. The literature review demonstrates mastery of the field and positions your contribution relative to prior work.

**Typical thematic structure for GeoAI papers:**
1. Remote sensing / geospatial data for [topic]
2. AI/ML methods for [application type]
3. Domain-specific prior work (disaster/env health/urban)
4. Evaluation approaches and benchmarks
5. [Optional] Limitations of prior work → synthesis paragraph bridging to your contribution

**Each subsection template:**
- Opening sentence: characterizes the theme and its importance ("Convolutional neural networks have become the dominant approach for building damage detection in high-resolution optical imagery.")
- Synthesis of 3-5 key papers: compare, contrast, build. Do NOT just annotate sequentially.
- Critical evaluation: what works well, what limitations exist across this body of work.
- Transition: how this theme connects to the next, or to your paper's approach.

**How to cite without summarizing:**
- Compare: "While [A] used U-Net at 0.5m resolution, [B] demonstrated that semi-supervised approaches reduce annotation burden at coarser 10m scale."
- Contrast: "Unlike [C], which assumed single-hazard events, [D] and [E] both attempt multi-hazard generalizations but with limited geographic scope."
- Build: "Building on the spatial attention mechanism of [F], our method additionally incorporates temporal context via..."

**Synthesis table:** in longer papers, include a summary table in the Related Work section (paper, year, method, dataset, key metric, limitation). This signals systematic knowledge of the field.

**Gap paragraph:** close the literature review with a clear synthesis: "Despite these advances, three key challenges remain: (1) geographic generalizability beyond training regions, (2) fusion of SAR and optical modalities in a unified framework, and (3) equitable performance across socioeconomically diverse neighborhoods. This paper addresses all three challenges."

**Target:** 25-40 references in a typical empirical paper; 50-100+ in a review paper.

### 2.4 Methodology

**Reproducibility is the primary obligation.** A reader with access to your data should be able to exactly replicate your results following your methods section.

**Structure:**
1. Study area (or "Experimental Setup" for non-geographic methods papers)
2. Data sources and preprocessing
3. Model architecture
4. Training details and hyperparameters
5. Evaluation metrics
6. Baselines

**Study area description:** geographic bounding box (coordinate bounds in WGS84), population, why chosen, potential limitations of this specific area for generalizability.

**Data section:** for each dataset, specify: name, source with URL, spatial resolution, temporal coverage, number of samples, preprocessing steps applied (cloud masking, normalization, reprojection to which CRS).

**Model description:** if proposing a new architecture, describe it precisely: layer types, activation functions, attention mechanisms, input/output dimensions. Include a figure. Reference open-source implementations if adapted.

**Training details:** optimizer, learning rate, scheduler, batch size, number of epochs, hardware (GPU model, VRAM), training time, number of parameters, random seeds for reproducibility.

**Statistical tests:** report which statistical tests were used for significance, with justification for choice. For spatial data, account for spatial autocorrelation in error estimates.

### 2.5 Results

**Lead with the best result.** Your first sentence in Results should deliver the key finding: "XYZ-Net achieves an F1 score of 0.87 for damaged building detection, outperforming the previous state-of-the-art by 4.2 percentage points."

**Structure:**
1. Main results table/figure (compare all methods on main benchmark)
2. Ablation study (what each component contributes)
3. Qualitative results (example maps, failure cases)
4. Additional experiments (robustness, temporal analysis, geographic generalization)

**Tables:** bold the best result in each column. Report mean and standard deviation across multiple runs. Use consistent significant figures throughout (do NOT report 0.8732 in one row and 0.87 in another).

**Figures:** maps must include scale bar, north arrow, legend, and study area inset. All figures need self-contained captions.

**Do NOT interpret in Results.** Results section states what happened. Discussion section explains why and what it means. Mixing these is a common reviewer complaint.

**Spatial results:** when showing geographic distribution of errors, use choropleth maps with appropriate classification (equal interval vs. quantile vs. natural breaks — justify choice). Show spatial autocorrelation of residuals (Moran's I of residuals) as a diagnostic for spatial model misspecification.

### 2.6 Discussion

**Interpret results in light of theory and prior work.** For each major finding, ask: Does this confirm, refute, or extend existing theory? How does it compare with specific prior papers (cite by metric value, not vague "outperforms prior work")?

**Structure:**
1. Confirm/refute the main hypothesis stated in the introduction
2. Explain unexpected findings (lower performance in region X — what geographic or data factors explain this?)
3. Compare with prior work (specific numbers, not vague claims)
4. Generalizability statement: where would these findings hold? Where might they not?
5. Limitations subsection (see below)
6. Practical implications: who can use this? Under what conditions?

**Limitations:** Be specific and honest. Generic limitations ("our method may not generalize to other regions") are not useful. Specific limitations: "Our model was trained exclusively on Sentinel-1 C-band SAR data; performance on ALOS-2 L-band SAR used in some national monitoring systems is unknown" is a useful limitation statement.

**Do NOT:** introduce major new results in Discussion. If you found something unexpected, mention in Results; interpret in Discussion.

### 2.7 Conclusion

**Target:** 400-600 words.

**Do NOT copy-paste the abstract.** The conclusion synthesizes contributions at a higher level than the abstract does.

**Structure:**
1. Brief summary (2-3 sentences: what was the problem, what did you do)
2. Restate contributions (numbered, matching Introduction contributions list)
3. Broader implications (what does this mean for the field, for practice, for policy?)
4. Limitations (1-3 sentences, referring back to Discussion)
5. Future work (3-5 specific, actionable directions, connected to identified limitations)
6. Closing sentence: inspiring but grounded — do not overstate impact

---

## 3. Writing Style

**Active voice preferred:** "We trained the model on..." not "The model was trained on..."

**Precise, not verbose:** "We use Sentinel-2 imagery" not "We utilize the imagery provided by the Sentinel-2 satellite system."

**Avoid weasel words:** "very," "quite," "seems," "appears to," "somewhat," "relatively" — cut them or replace with specific values.

**Consistent tense:**
- Methods: past tense ("we used," "we trained")
- Results: past tense ("the model achieved," "accuracy decreased")
- Discussion/interpretation: present tense ("this suggests," "the results indicate")
- Contributions/general truths: present tense ("our method enables," "GeoAI addresses")

**Parallel structure in lists:** all items in a list should be grammatically parallel:
- Good: "The method (1) improves accuracy, (2) reduces inference time, and (3) requires fewer labels."
- Bad: "The method (1) improves accuracy, (2) the inference time was reduced, (3) fewer labels."

**Define acronyms on first use.** Do this in abstract (if used there) AND again in body text.

---

## 4. Geography/GeoAI Specific Conventions

- Always spell out the coordinate reference system: "WGS84 (EPSG:4326)" or "UTM Zone 10N (EPSG:32610)"
- State spatial resolution of all raster data
- Describe study area with coordinates and area in km² or ha
- Justify spatial scale selection: why 30m? why county level? what are the scale implications?
- When comparing across sensors, acknowledge spectral/spatial resolution differences
- Report spatial autocorrelation metrics (Moran's I) for spatial prediction residuals
- Specify whether cross-validation is spatial or random; prefer spatial

---

## 5. Common Errors to Avoid

- **Overclaiming:** "Our method is the best / state-of-the-art / significantly better" — only say this if you have tested against ALL relevant recent methods on the SAME benchmark
- **Underclaiming / missing contribution statement:** do not bury your contribution in vague language
- **Missing reproducibility info:** no random seed, no hardware specs, no hyperparameters = reproducibility failure
- **Citation without analysis:** listing papers without comparing or synthesizing them
- **Table without narrative:** never present a table without at least 2-3 sentences explaining what it shows
- **Inconsistent numbers:** methods says 10,000 training samples, Table 1 says 9,847 — always reconcile
- **Passive + jargon stack:** "The proposed framework was utilized to perform geospatial analysis" — use active voice and plain terms
- **Conclusions that just summarize:** a conclusion that only reiterates the abstract adds no value; include implications and future directions

---

## 6. Word Count Management

**Sections that can be shortened:**
- Study area description (can be compressed to 1-2 paragraphs)
- Data preprocessing details (move to supplementary materials)
- Baseline method descriptions (cite instead of describe)

**Sections that must be complete:**
- Experimental setup (reproducibility is non-negotiable)
- Ablation study (reviewers specifically look for this)
- Limitations (reviewers penalize omission)
- Statistical reporting (significant figures, confidence intervals, p-values)

---

## 7. Response to Reviewers

**RADAR Method:**
- **R — Restate:** briefly restate what the reviewer said
- **A — Acknowledge:** acknowledge the validity of the concern (even if you disagree)
- **D — Defend:** if you disagree, explain why with evidence or literature
- **A — Amend:** describe what change you made to the paper
- **R — Reply:** point reviewer to where the change appears in the revised manuscript

**Golden rules:**
- Never argue without evidence
- Thank every reviewer in the opening of your response (sincere, not sycophantic)
- For every change: specify the page, paragraph, line where the change appears
- Track all changes in the manuscript itself (bold or track-changes mode)
- If you cannot address a limitation: explain why and acknowledge it explicitly in the paper
