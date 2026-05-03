---
name: spatial-analysis
description: 'Guideline-driven spatial analysis skill. Given a research question and data context, provides decision frameworks for selecting appropriate spatial methods, diagnostics, and interpretation strategies. Adapts to available data, spatial units, and analytical objectives — Claude Code determines the optimal workflow. Use when user says "spatial analysis", "analyze spatial data", "run spatial regression", "check for clustering", "map this", or needs to go from a research question to a complete spatial analysis.'
argument-hint: [research-question-or-analysis-goal]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
---

# Spatial Analysis: Guideline-Driven Decision Framework

Analyze: **$ARGUMENTS**

## Purpose

This skill provides **guidelines, decision tables, and guardrails** for spatial analysis — not a fixed procedure. The sequence and combination of methods should be determined by Claude Code based on:

1. The research question and its analytical objective
2. The available data (type, size, quality, spatial unit)
3. The study context (domain, audience, publication target)

Read `skills/knowledge/spatial-methods.md` for reference implementations. This skill decides *when*, *why*, and *under what conditions* to use them.

## Constants

- **OUTPUT_DIR = `output/spatial-analysis`** — Default destination for all analysis artifacts.
- **MAX_FEATURES = 15** — Soft cap on predictors before recommending dimensionality reduction.
- **MGWR_MAX_N = 3000** — Subsample threshold for MGWR.
- **GWR_MAX_N = 5000** — Subsample threshold for GWR.
- **SIGNIFICANCE_LEVEL = 0.05** — Default alpha unless user specifies otherwise.
- **SPATIAL_CV_FOLDS = 5** — Default spatial cross-validation folds.

> Override via argument, e.g., `/spatial-analysis "question" — significance: 0.01, max features: 8`.

---

## 1. Research Question Classification

Before selecting any method, classify the research question. This classification drives every downstream decision.

### 1.1 Analytical Objective Mapping

| Objective | Signal phrases | Typical method families |
|---|---|---|
| **Description** | "what is the spatial pattern of...", "how is X distributed" | Choropleth, KDE, summary statistics, ESDA |
| **Explanation** | "what factors explain...", "why does X vary across..." | Regression ladder (OLS → spatial → local) |
| **Comparison** | "does X differ between regions..." | Stratified analysis, interaction terms, regional subsetting |
| **Prediction** | "can we predict...", "where will X occur..." | ML + spatial CV, feature engineering |
| **Clustering / hot spots** | "are events clustered...", "where are hot spots..." | Moran's I, LISA, Getis-Ord Gi*, DBSCAN |
| **Association** | "is X related to Y spatially..." | Bivariate Moran's I, spatial regression |
| **Accessibility** | "who has access to...", "what areas are underserved..." | Network analysis, 2SFCA, isochrones |
| **Temporal-spatial change** | "how has X changed over time across space..." | Panel methods, spatiotemporal aggregation |
| **Causal inference** | "does X cause Y..." | Spatial DiD, IV, RDD — flag limitations explicitly |
| **Interpolation** | "what is the value at unsampled locations..." | Kriging, IDW, cross-validation |

**If the question maps to multiple objectives**, identify the primary one and treat others as supporting. If the question is too vague, ask the user to clarify the outcome, spatial unit, and study area.

### 1.2 Should Spatial Methods Be Used at All?

Not every geographic dataset requires spatial statistics. Evaluate:

| Question | If "no" | If "yes" |
|---|---|---|
| Is spatial dependence theoretically plausible? | Standard methods may suffice | Spatial structure likely matters |
| Is the spatial structure itself the research question? | Spatial methods are optional | Spatial methods are mandatory |
| Would ignoring spatial structure bias results? | OLS may be adequate | Spatial adjustment needed |

**Guideline:** If all three are "no", recommend non-spatial analysis and explain why. Do not force spatial methods where they add no value.

### 1.3 Write Question Classification

Save classification to `output/spatial-analysis/question_classification.md`:

```markdown
# Research Question Classification

**Question**: [user's question]
**Date**: [today]

## Analytical Objective
- Primary: [objective type]
- Supporting: [if any]

## Key Components
- Outcome variable: [or N/A]
- Explanatory variables: [list or TBD]
- Spatial unit: [point / polygon / raster / network]
- Temporal structure: [cross-sectional / panel / time series]
- Study extent: [description]
- Estimated N: [if known]

## Spatial Methods Needed?
- [Yes / No / Conditional on diagnostics]
- Reasoning: [why]

## Method Candidates
1. [method — why it fits this question]
2. [method — why it fits this question]
3. [method — conditional on X]
```

---

## 2. Data Readiness Guidelines

These guidelines apply regardless of analytical objective. Evaluate data readiness before proceeding to any analysis. The depth of preparation depends on the situation.

### 2.1 CRS Decision Framework

**This is non-negotiable.** Wrong CRS invalidates distance, area, and density calculations.

| If the analysis involves... | CRS requirement | Recommendation |
|---|---|---|
| Distance or density calculations | Projected (meters) | Local UTM or national grid |
| Area calculations | Equal-area projection | Albers, Mollweide, or national equal-area |
| Only display / web mapping | Any (geographic OK) | WGS84 (EPSG:4326) |
| Spatial joins / overlays | Both layers must match | Reproject to analysis CRS first |
| Mixed (distance + display) | Analyze in projected, display in geographic | Two CRS in workflow |

**Guardrail:** If data is in EPSG:4326 and the analysis involves distances, areas, or density — project first. Never compute Euclidean distance on lat/lon.

**UTM zone estimation** (when no local CRS is obvious):
```python
centroid = gdf.geometry.unary_union.centroid
utm_zone = int((centroid.x + 180) / 6) + 1
hemisphere = 'north' if centroid.y >= 0 else 'south'
epsg = 32600 + utm_zone if hemisphere == 'north' else 32700 + utm_zone
```

### 2.2 Data Quality Checklist

Evaluate these as needed — not all checks apply to every dataset:

| Issue | When to check | How to handle |
|---|---|---|
| Missing CRS | Always | Ask user or infer from coordinate range |
| Invalid geometries | Before spatial operations | `gdf.geometry.buffer(0)` to fix |
| Duplicated geometries | Before spatial statistics | Investigate context before dropping |
| Multipart features | When analysis requires single-part | `gdf.explode()` |
| Empty geometries | Always | Drop or investigate |
| Missing values | Always | Document spatial pattern of missingness — clustered missingness biases spatial statistics |

### 2.3 Multi-Dataset Integration

When combining datasets, address these issues in the order they arise:

| Issue | Guideline |
|---|---|
| CRS mismatch | Reproject all layers to a common analysis CRS before any spatial operation |
| Temporal mismatch | Document the assumption that spatial patterns are stable over the time gap; flag if gap > 2 years |
| Resolution mismatch (MAUP) | Document aggregation/disaggregation method; warn about ecological fallacy; consider sensitivity analysis at different scales |
| Boundary mismatch | Use areal interpolation if administrative boundaries don't align |

### 2.4 Variable Preparation Guidelines

| Situation | Guideline |
|---|---|
| Suspected outliers | Inspect in spatial context — an "outlier" may be a real local phenomenon. Do NOT auto-remove |
| Skewed distributions | Log-transform only if theoretically justified AND skewness > \|2\| |
| Many predictors (> MAX_FEATURES) | Apply domain-driven selection or dimensionality reduction before modeling |
| Multicollinearity (VIF > 10) | Drop or combine correlated predictors |
| Preparing for GWR/MGWR | Standardize predictors (mean=0, std=1) so bandwidths are comparable |

---

## 3. Spatial Weights Selection Guide

Spatial weights underpin most spatial statistics. The choice is consequential and must be justified.

| Data type | Recommended weights | Rationale |
|---|---|---|
| Regular polygon tessellation (counties, tracts) | Queen contiguity | Captures all adjacency relationships |
| Grid-like polygons | Rook contiguity | Corner adjacency often not meaningful |
| Point data | KNN (k=5–8) | Adapts to varying point density |
| Irregular polygon sizes | KNN or distance band | Contiguity unreliable with very different sizes |
| Interaction decays with distance | Distance band | Captures distance-decay process |

**Guardrails:**
- Always check for islands: `W.islands`. Islands break spatial statistics — add manual connections or switch to KNN.
- Always row-standardize: `W.transform = 'R'`.
- Document your choice and reasoning. If results are sensitive to weights choice, report this.

---

## 4. Analytical Approach Guidelines

Select your approach based on the analytical objective from Section 1. These are **not sequential steps** — choose the relevant section(s) and adapt.

### 4.1 Exploratory Spatial Data Analysis (ESDA)

**When to use:** Almost always — ESDA should precede formal modeling in most situations. Skip only if the question is purely about accessibility/network analysis with no distributional component.

**What to include depends on the question:**

| If the question is about... | ESDA should include |
|---|---|
| Spatial patterns or distribution | Choropleth/KDE maps, global Moran's I, LISA or Gi* |
| Regression / explanation | Distribution of outcome + predictors, correlation matrix, global Moran's I to determine if spatial modeling is needed |
| Prediction | Feature distributions, spatial autocorrelation of target variable, visual inspection for spatial structure |
| Clustering | Global clustering test first (Moran's I or General G), then local tests |

**Map classification guidance:**

| Data distribution | Best classification scheme |
|---|---|
| Roughly uniform | `equal_interval` |
| Skewed (common) | `quantiles` (equal-count bins) |
| Multimodal or natural groupings | `natural_breaks` or `fisher_jenks` |
| Need to highlight deviation from mean | `std_mean` (only if roughly normal) |

**Color scheme rules:**

| Variable type | Use | Never use |
|---|---|---|
| Sequential (counts, rates) | `viridis`, `YlOrRd`, `Blues` | rainbow/jet |
| Diverging (residuals, change) | `RdBu_r`, `coolwarm`, `PiYG` | sequential colormap |
| Categorical (clusters) | `Set2`, `tab10` | continuous colormap |

**Global Moran's I interpretation:**

| Result | Implication |
|---|---|
| p < 0.01 | Strong spatial autocorrelation — spatial methods likely needed |
| 0.01 ≤ p < 0.05 | Moderate — spatial methods recommended; compare with non-spatial |
| p ≥ 0.05 | Not significant — non-spatial methods may suffice; still check residuals after modeling |

**Local pattern detection — LISA vs Getis-Ord Gi*:**

| Use LISA when | Use Gi* when |
|---|---|
| You care about both clusters AND spatial outliers (HH, LL, HL, LH) | You only care about hot spots and cold spots |
| You want to identify areas that deviate from neighbors | You want to identify concentration of extreme values |

**Guardrail:** Multiple testing — with N spatial units, you run N local tests. Report the number of significant clusters and note potential false positives. Consider Bonferroni or FDR correction.

### 4.2 Explanatory Analysis (Regression)

**When to use:** The research question asks *why* a spatial pattern exists or *what factors explain* spatial variation.

**Decision framework — choose the model based on diagnostics, not assumption:**

```
Start with OLS baseline (always)
    │
    ├── Check residual Moran's I
    │   ├── p ≥ 0.05 → OLS is adequate. Report and stop.
    │   └── p < 0.05 → Spatial dependence in residuals. Continue below.
    │
    ├── Determine the nature of spatial dependence:
    │   ├── Substantive (spillover: outcome in i depends on neighbors)
    │   │   → Spatial Lag Model
    │   │   Example: crime spillover, housing price contagion
    │   │
    │   ├── Nuisance (unobserved spatially-structured factors)
    │   │   → Spatial Error Model
    │   │   Example: unmeasured soil quality, regional culture
    │   │
    │   └── Both LM tests significant → Use Robust LM tests
    │       ├── Only Robust LM-Lag remains significant → Spatial Lag
    │       ├── Only Robust LM-Error remains significant → Spatial Error
    │       └── Both remain significant → Spatial Durbin Model
    │
    ├── Do relationships plausibly vary across space?
    │   ├── Yes AND theoretical justification exists
    │   │   ├── N ≤ MGWR_MAX_N → MGWR (preferred — per-variable bandwidth)
    │   │   ├── N ≤ GWR_MAX_N → GWR
    │   │   └── N > GWR_MAX_N → Spatially stratified subsample, or regional submodels
    │   │
    │   └── No theoretical reason → Do NOT run GWR/MGWR
    │
    └── Compare all fitted models: AICc, R², residual Moran's I
        └── Report best model with full diagnostics
```

**OLS diagnostics to check:**
- R², Adjusted R², RMSE, MAE, AIC/BIC
- Residual Moran's I (spatial autocorrelation)
- Breusch-Pagan (heteroskedasticity)
- Jarque-Bera (residual normality)
- VIF (multicollinearity), Condition number (< 30 preferred)

**GWR/MGWR guardrails:**
- Only run when there is a **theoretical reason** to expect spatially varying relationships
- Always standardize predictors first
- Coordinates must be in projected CRS
- Interpret bandwidths: < 50 neighbors = local process; 50–200 = regional; > n/3 = effectively global

**Model comparison table** (always produce when multiple models are run):

```markdown
| Model | R² | Adj. R² | AICc | RMSE | Residual Moran's I | p(Moran) |
|-------|-----|---------|------|------|--------------------|----------|
```

**Selection logic:** (1) Best AICc with > 2 difference being meaningful. (2) Residual Moran's I closest to 0. (3) If AICc and Moran's I disagree, prefer the model that resolves spatial autocorrelation. (4) Prefer simpler model when differences are marginal.

### 4.3 Clustering and Hot Spot Detection

**When to use:** The question asks *whether* or *where* spatial clustering exists.

**Decision framework:**

| Situation | Approach |
|---|---|
| Testing for global clustering | Global Moran's I (spatial autocorrelation) or Getis-Ord General G (concentration of high/low values) |
| Locating specific clusters | LISA (clusters + outliers) or Gi* (hot/cold spots only) |
| Detecting clusters without predefined weights | DBSCAN or other density-based methods |
| Analyzing event/count data | **Normalize by population at risk first** — raw counts cluster where people live |

**Guardrail:** If analyzing event counts (disease cases, crime incidents), always normalize by population at risk or use standardized rates. Raw count clusters reflect population density, not elevated risk.

### 4.4 Prediction

**When to use:** The goal is to estimate values at locations where the outcome is unknown.

**Key guidelines:**

| Guideline | Rationale |
|---|---|
| Include spatial features | Coordinates, distance to landmarks, spatial lag of predictors, neighborhood summaries — these capture spatial structure |
| Use spatial cross-validation, NEVER random CV | Random CV leaks spatial autocorrelation and overestimates predictive accuracy |
| Compare models by spatial CV performance | Not in-sample fit |
| Check residual Moran's I even for ML models | Remaining spatial structure means the model misses a spatial predictor or process |

**Spatial CV approaches:**
- Grid-based blocks (simple, may be imbalanced)
- K-means clustering on coordinates (more balanced folds)
- Buffer-based exclusion (strongest protection against leakage)

Choose based on the spatial structure of the data and the prediction task.

### 4.5 Accessibility and Network Analysis

**When to use:** The question concerns reachability, service coverage, or spatial access to facilities.

**Guideline:** Only invoke network analysis when the research question specifically requires it. Do not add network analysis to a regression workflow just because spatial data is involved.

**Common approaches:** Street network analysis (OSMnx + NetworkX), isochrone construction, 2-step floating catchment area (2SFCA), service area delineation.

### 4.6 Interpolation

**When to use:** Estimating values at unsampled locations from point observations, assuming spatial continuity.

**Key guidelines:**

| Guideline | Rationale |
|---|---|
| Always inspect the variogram first | The variogram reveals the spatial structure; fitting without inspection is reckless |
| Cross-validate to choose method | Compare Kriging variants, IDW, etc. by leave-one-out or k-fold spatial CV |
| Do NOT interpolate categorical variables | Interpolation assumes spatial continuity — categorical data is not continuous |
| Distinguish from regression-based prediction | Interpolation leverages spatial proximity, not covariates |

### 4.7 Temporal-Spatial Analysis

**When to use:** The question involves change over time across space.

**Guideline:** Choose approach based on data structure:

| Data structure | Approach |
|---|---|
| Repeated cross-sections (same areas, multiple time points) | Panel methods, fixed/random effects with spatial terms |
| Two time points | Change analysis, spatial pattern of change |
| Continuous time series at fixed locations | Spatiotemporal modeling, temporal faceting |
| Irregular temporal observations | Aggregate to consistent time windows first; document the choice |

---

## 5. Diagnostics and Robustness Guidelines

Apply diagnostics proportional to the complexity of the analysis and the stakes of the conclusions. **Diagnostics are a menu, not a checklist.** Pick only the ones that are relevant to the research question, the chosen method, and the data — running every spatial diagnostic on every project is wasteful and frequently misleading.

### 5.1 Core Diagnostics (apply only when the trigger is met)

| Diagnostic | Apply ONLY when | Skip when |
|---|---|---|
| Residual Moran's I | A regression / ML model is fit AND spatial dependence is theoretically plausible AND inference depends on residual independence | Question is purely descriptive, predictive on i.i.d. data, or non-spatial; or the unit of analysis has no plausible neighborhood structure |
| Breusch-Pagan | Regression with formal inference on coefficients | Predictive-only modeling, ML pipelines reported by CV error |
| Jarque-Bera | Regression where you rely on parametric inference | Robust / nonparametric / large-N CLT cases |
| VIF | Multiple regression with multiple plausibly-correlated predictors | Single predictor; orthogonal-by-design features |
| Cook's distance | Regression where leverage of individual observations could flip a substantive conclusion | Large N where single points cannot dominate |
| AICc comparison | Multiple competing **nested or comparable** models are fit | Single chosen model justified a priori |
| Spatial CV metrics | Prediction task on spatially structured data where leakage is plausible | Non-spatial prediction; spatial structure already removed by design (e.g., independent draws) |

If unsure whether a diagnostic is necessary, default to **asking the user** rather than running it. See Section 5.3.

### 5.2 Robustness Checks — Apply When Conclusions Are Sensitive

| Check | Apply ONLY when | Skip when |
|---|---|---|
| Alternative spatial weights | The headline claim is a clustering result or spatial regression coefficient that could plausibly flip under a different W | Pure description, prediction by CV error, or W has no causal role in the claim |
| Alternative spatial scale (MAUP) | The unit of aggregation was a researcher choice **and** the conclusion is about magnitude, ranking, or causation across units | Unit is fixed by the data-generating process; question is at a single scale by design; result is about presence/absence rather than magnitude |
| Boundary effects | Study area has hard administrative or natural boundaries AND inference relies on neighborhood-based statistics near those edges | Question is interior-only or edge units are excluded a priori |
| Temporal mismatch sensitivity | Combining datasets from different years AND the spatial pattern is plausibly non-stationary over that gap | Single time slice; gap < 1 year; pattern known to be stable |
| Subset analysis | Study area is heterogeneous AND a regional effect is plausible | Homogeneous area or N too small to subset reliably |

**Guideline:** Report robustness checks that you performed AND **explicitly list checks you considered but skipped, with the reason** (e.g., "MAUP not assessed — unit of analysis is the individual sensor reading, not aggregated"). It is acceptable — and often correct — to skip MAUP, GWR, alternative weights, or spatial CV when the research question does not depend on them.

### 5.3 Human Checkpoint — Adding or Skipping Spatial Checks

Geospatial diagnostics (Moran's I on residuals, MAUP sensitivity, GWR/MGWR, alternative spatial weights, spatial CV, LISA / Gi*) are powerful but **not universally required**. Apply them only when the research question genuinely depends on them. When in doubt, **PAUSE and ask the user** rather than running them by reflex.

Honor the `HUMAN_CHECKPOINT` flag in `CLAUDE.md` (default: `true`). When `true`, request explicit user approval before either of the following; when `false`, log the decision (and reasoning) to `output/PROJ_NOTES.md` and the **Diagnostics and Robustness** section of the report and proceed.

| Trigger | Show before pausing |
|---|---|
| About to **add** a heavyweight spatial check that the question may not need (GWR/MGWR, MAUP sensitivity sweep, alternative-W sweep, spatial CV when the task is not predictive on spatially structured data) | Which check, why it might be relevant, the cost (time / compute / interpretive load), the simpler alternative, and a one-line recommendation |
| About to **skip** a spatial check that a strict GIScience reviewer would expect (e.g., regression on aggregated areal data with no MAUP discussion, spatial regression with no residual Moran's I) | Which check, why this question / dataset arguably does not need it, and the explicit caveat that will go into the report |

Default rule: **prefer the lightest analysis that answers the question.** If a choropleth and summary statistics answer it, do not run MGWR; if the question is non-spatial in substance even though the data have coordinates, do not force spatial methods.

---

## 6. Visualization Guidelines

### 6.1 Map Requirements

Every map must include: title, legend with units and classification scheme, scale bar, CRS in caption, consistent color scheme across related maps. Add north arrow and source attribution if publication conventions require them.

### 6.2 Which Plots to Include

Choose based on what was analyzed — do not produce plots that add no information:

| Plot type | Include when |
|---|---|
| Choropleth / KDE map | Describing spatial distribution (almost always) |
| Residual map | Any regression model was fit |
| LISA cluster map | Local clustering was detected |
| Gi* hot/cold spot map | Hot spot analysis was performed |
| Coefficient surface map | GWR/MGWR was run and coefficients vary meaningfully |
| Local R² map | GWR/MGWR and local fit varies |
| Moran scatter plot | Reporting Moran's I (visual complement) |
| QQ plot of residuals | Regression diagnostics, normality in question |
| Model comparison bar chart | Multiple models compared |

---

## 7. Interpretation and Reporting

### 7.1 Report Structure

Write to `output/spatial-analysis/analysis_report.md`:

```markdown
# Spatial Analysis Report

**Research Question**: [question]
**Date**: [today]
**Data**: [description — N, spatial extent, time period]

## Data and Study Area
[Data sources, spatial units, sample size, key variables, CRS used]

## Exploratory Findings
[Distribution of outcome, initial spatial patterns, global Moran's I result if computed]

## Analytical Results
[Method(s) used and why, model comparison if applicable, key findings]

## Diagnostics and Robustness
[Residual checks, sensitivity analysis, caveats]

## Implications
[What the results mean for the research question, limitations, next steps]
```

**Adapt the depth to the complexity of the analysis.** A descriptive analysis needs 2–3 paragraphs. A full regression comparison may need 5–6. Do not pad simple analyses with unnecessary sections.

### 7.2 Interpretation Guardrails

| Guardrail | Rationale |
|---|---|
| Report effect sizes, not just significance | p-values alone are uninformative about practical importance |
| Never claim causality from cross-sectional observational data without explicit justification | Spatial association ≠ causation |
| Acknowledge MAUP **when** results could plausibly depend on the unit of aggregation | Results at county level may not hold at census tract level — but a fixed-unit study (e.g., per-sensor measurements) does not need a MAUP statement |
| Note boundary effects **when** the analysis relies on neighborhood statistics near hard edges | Fewer neighbors = less reliable local statistics; skip if interior-only |
| Distinguish statistical significance from substantive importance | A Moran's I of 0.02 with p < 0.01 is significant but trivially small |

---

## 7.5 Human Checkpoint — Data Synthesis

Honor the `HUMAN_CHECKPOINT` flag in `CLAUDE.md` (default: `true`). Spatial analysis frequently *creates* derived layers (interpolated surfaces, predicted maps, simulated permutations, areal-interpolated reaggregations) that downstream skills may treat as observations. When `HUMAN_CHECKPOINT` is `true`, **PAUSE** and request explicit user approval before any of the following; when `false`, log the decision to `output/PROJ_NOTES.md` and the analysis report's **Diagnostics and Robustness** section, and proceed.

| Trigger | Show before pausing |
|---|---|
| Producing an **interpolated surface** (Kriging, IDW, regression-Kriging) that will be saved to `output/spatial-analysis/` and may be reused as input by another skill | Method, variogram model, search neighborhood, CV error, and whether downstream skills should treat outputs as observations or as model predictions |
| Producing **GWR/MGWR coefficient surfaces or local R² maps** that will be exported as data (not just figures) | Bandwidth choice, standardization, and a warning that local estimates are not independent observations |
| **Areal interpolation** between non-aligned boundaries (e.g., reallocating block-group counts to a custom grid) | Source / target geometries, the weighting variable (population, area, dasymetric), and the MAUP risk introduced |
| **Imputing missing values** for any variable that enters a regression or clustering result reported in `analysis_report.md` | Imputation method, share of values imputed, and a sensitivity analysis plan (or explicit decision to skip it) |
| **Permutation / Monte Carlo** runs whose realizations will be persisted (not just summarized) | N permutations, seed, what each realization represents, and how it will be cited in downstream artifacts |
| **Pseudo-absences / random-background points** generated for a presence-only model | Sampling region, density, exclusion rules, seed, and circularity risk if presence and pseudo-absence share predictors |
| Any number entering the report that was not produced by an executed code cell logged in `output/spatial-analysis/scripts/` | The exact source and why it is acceptable evidence |

Synthesized layers must be saved with a `.meta.json` sidecar marking `synthetic_or_derived: true`, recording the recipe, and noting `Synthesis approved by user: YYYY-MM-DD`.

---

## 8. Guardrails Summary

These are mistakes this skill is designed to prevent. Claude Code should internalize these as hard constraints:

| Mistake | Prevention |
|---|---|
| Using lat/lon for distance calculations | CRS guidelines require projection for any distance/area/density analysis |
| Applying Moran's I without thoughtful weights choice | Weights selection guide requires explicit justification |
| Interpreting raw count clusters as rate clusters | Clustering guidelines mandate normalizing by population at risk |
| Running GWR/MGWR by default | Regression guidelines require theoretical justification — and Section 5.3 requires user approval before adding it |
| Forcing MAUP / GWR / spatial CV on questions that do not need them | Section 1.2, Section 5, and Section 5.3 make these conditional, not mandatory; skipping with documented reasoning is a valid outcome |
| Random CV on spatial data **when** the prediction task is spatial | Prediction guidelines mandate spatial CV in that case; non-spatial prediction tasks remain free to use standard CV |
| Reporting OLS when residuals are spatially autocorrelated **and** inference depends on residual independence | Regression decision framework escalates to a spatial model in that specific case |
| Misleading map classification | ESDA guidelines match classification scheme to data distribution |
| Rainbow/jet colormaps | Color scheme rules explicitly ban them |
| Overclaiming causality | Objective mapping distinguishes explanation from causal inference |
| Mixing incompatible spatial resolutions silently | Data integration guidelines require documenting resolution mismatch |
| Overcomplicating when simple methods suffice | Question classification checks whether spatial methods are even needed |

---

## 9. Outputs

- `output/spatial-analysis/question_classification.md` — Research question classification and method candidates
- `output/spatial-analysis/analysis_report.md` — Analysis narrative (depth proportional to complexity)
- `output/spatial-analysis/model_comparison.md` — Model comparison table (if regression)
- `output/spatial-analysis/scripts/` — Python scripts used (for reproducibility)
- `output/spatial-analysis/figures/` — Maps and diagnostic plots
- `output/PROJ_NOTES.md` — One-line findings appended
- `output/results/` — JSON results (if feeding into geo-experiment pipeline)

---

## 10. Key Principles

- **Research question first.** Never start with a method. The question determines everything.
- **Justify every method choice.** If you cannot explain why a method is needed for this question, do not use it.
- **Parsimonious workflows.** If a choropleth and summary statistics answer the question, do not run MGWR.
- **Geospatial checks are conditional, not mandatory.** MAUP, GWR/MGWR, alternative-W sweeps, spatial CV, residual Moran's I all require a triggering reason from Section 5. When unclear, ask the user (Section 5.3) instead of running them by default.
- **Adapt to the data.** The guidelines above are decision frameworks, not checklists. Skip what doesn't apply; go deeper where the data demands it.
- **Honest interpretation.** Report what the analysis actually shows, including null results and limitations.
- **Reproducibility.** Save scripts, log parameter choices, document CRS decisions.
- **Do not fabricate results.** Only report numbers from executed code.
- **Respect computational limits.** GWR ≤ 5,000 obs; MGWR ≤ 3,000. Subsample spatially if needed.
- **Large file handling**: If the Write tool fails due to file size, retry using Bash (`cat << 'EOF' > file`). Do not ask permission — just do it.

---

## 11. Composing with Other Skills

```
/lit-review "spatial topic"       → literature context
/generate-idea "spatial direction" → research ideas
/refine-research "spatial problem" → method refinement
/spatial-analysis "research question" ← you are here
/geo-experiment                    → formal experiment execution with sprint contracts
/result-to-claim                   → validate claims against actual results
/auto-review-loop                  → adversarial review of the analysis
/paper-figure                      → publication-quality figures
/paper-write                       → write the paper sections
```

**Integration points:**
- **From geo-experiment**: If `geo-experiment` runs OLS/GWR/MGWR, this skill interprets those results. Read from `output/results/`.
- **To paper-figure**: Draft figures in `output/spatial-analysis/figures/`. The `paper-figure` skill polishes them.
- **To result-to-claim**: Model comparison table feeds directly into claim validation.
- **Knowledge base**: Read `skills/knowledge/spatial-methods.md` for code snippets, CRS reference, and detailed method parameters.
