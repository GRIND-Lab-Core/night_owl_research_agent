---
name: spatial-analysis
description: 'Research-question-driven spatial analysis workflow designer and executor. Given a research question, infers analytical objective, selects appropriate spatial methods, constructs a coherent analysis pipeline, implements it in Python, runs diagnostics, and writes interpretation. Use when user says "spatial analysis", "analyze spatial data", "run spatial regression", "check for clustering", "map this", or needs to go from a research question to a complete spatial analysis workflow.'
argument-hint: [research-question-or-analysis-goal]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
---

# Spatial Analysis: Research-Question-Driven Workflow

Design and execute a spatial analysis workflow for: **$ARGUMENTS**

## Overview

This skill turns a research question into a complete, justified spatial analysis workflow. It does NOT apply every available method. It reasons from the question to the minimum set of methods that answer it rigorously.

The workflow is always: **research question → analytical objective → data assessment → method selection → implementation → diagnostics → interpretation → output**.

Read `skills/knowledge/spatial-methods.md` for reference implementations before starting. That file has code snippets and parameter details; this skill decides *when* and *why* to use them.

## Constants

- **OUTPUT_DIR = `spatial-analysis-outputs/`** — Default destination for all analysis artifacts (scripts, figures, tables, reports).
- **MAX_FEATURES = 15** — Soft cap on predictor variables before recommending dimensionality reduction or domain-driven selection.
- **MGWR_MAX_N = 3000** — Subsample threshold for MGWR. Above this, spatially stratified subsample.
- **GWR_MAX_N = 5000** — Subsample threshold for GWR.
- **SIGNIFICANCE_LEVEL = 0.05** — Default alpha for statistical tests unless user specifies otherwise.
- **SPATIAL_CV_FOLDS = 5** — Default number of spatial cross-validation folds for predictive workflows.

> Override via argument, e.g., `/spatial-analysis "question" — significance: 0.01, max features: 8`.

---

## Phase 0: Understand the Research Question

Before touching data or methods, classify the research question along these dimensions:

### Step 0.1: Infer the Analytical Objective

Map the user's question to one or more of these objective types:

| Objective | Signal phrases | Primary methods |
|---|---|---|
| **Description** | "what is the spatial pattern of...", "how is X distributed" | Choropleth, KDE, summary statistics, ESDA |
| **Explanation** | "what factors explain...", "why does X vary across..." | Regression (OLS → spatial lag/error → GWR/MGWR) |
| **Comparison** | "does X differ between regions...", "is the pattern different in..." | Stratified analysis, interaction terms, regional subsetting |
| **Prediction** | "can we predict...", "where will X occur next..." | ML + spatial CV, feature engineering, residual autocorrelation check |
| **Clustering / hot spots** | "are events clustered...", "where are hot spots..." | Moran's I, LISA, Getis-Ord Gi*, nearest neighbor, DBSCAN |
| **Association** | "is X related to Y spatially...", "do areas with more X have more Y..." | Bivariate Moran's I, correlation with spatial adjustment, regression |
| **Accessibility** | "who has access to...", "what areas are underserved..." | Network analysis, service areas, 2SFCA, isochrones |
| **Temporal-spatial change** | "how has X changed over time across space..." | Panel methods, temporal faceting, spatiotemporal aggregation |
| **Causal inference** | "does X cause Y...", "what is the effect of..." | Spatial DiD, IV, RDD with spatial dimension — flag limitations |
| **Interpolation** | "what is the value at unsampled locations..." | Kriging, IDW, cross-validation comparison |

If the question maps to multiple objectives, identify the **primary** objective and treat others as supporting.

If the question is too vague (e.g., "analyze this spatial data"), STOP and ask the user to specify:
- What outcome or pattern are you trying to understand?
- What is your spatial unit of analysis?
- What is the study area and time period?

### Step 0.2: Identify Key Analysis Components

Extract from the question and any provided data:

- **Outcome variable** (dependent variable, if applicable)
- **Explanatory variables** (predictors, if applicable)
- **Spatial unit** (point, polygon, raster cell, network edge)
- **Temporal unit** (cross-sectional, panel, time series)
- **Study extent** (local, regional, national, global)
- **Sample size** (affects method feasibility — GWR/MGWR have hard limits)
- **Data type** (vector points, vector polygons, raster, network)

### Step 0.3: Decide if Spatial Methods are Necessary

Not every question about geographic data requires spatial statistics. Ask:

1. **Is spatial dependence theoretically plausible?** If observations are independent conditional on covariates, OLS may suffice.
2. **Is the spatial structure the research question itself?** If yes, spatial methods are mandatory.
3. **Would ignoring spatial structure bias the results?** If residuals are spatially autocorrelated, OLS standard errors are wrong.

If the answer to all three is "no," recommend a non-spatial analysis and explain why. Do not force spatial methods.

Write the question classification to `spatial-analysis-outputs/question_classification.md`:

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

## Preliminary Method Candidates
1. [method — why it fits]
2. [method — why it fits]
3. [method — may be needed if condition X holds]
```

---

## Phase 1: Inspect and Prepare Data

### Step 1.1: Load and Inspect

```python
import geopandas as gpd
import pandas as pd
import numpy as np

gdf = gpd.read_file('path/to/data')  # or gpd.GeoDataFrame from CSV with geometry
print(f"Shape: {gdf.shape}")
print(f"CRS: {gdf.crs}")
print(f"Geometry types: {gdf.geom_type.value_counts().to_dict()}")
print(f"Bounds: {gdf.total_bounds}")
print(gdf.describe())
print(f"Missing values:\n{gdf.isnull().sum()}")
```

Check for:
- **CRS defined?** If `gdf.crs is None`, ask the user or infer from coordinates.
- **Geometry validity?** Run `gdf.geometry.is_valid.all()`. Fix with `gdf.geometry = gdf.geometry.buffer(0)` if needed.
- **Duplicated geometries?** `gdf.geometry.duplicated().sum()` — investigate before dropping.
- **Multipart features?** `gdf[gdf.geom_type.str.startswith('Multi')]` — explode if analysis requires single-part.
- **Empty geometries?** `gdf[gdf.is_empty]` — drop or investigate.

### Step 1.2: CRS Assessment

**This step is non-negotiable.** Wrong CRS invalidates distance, area, and density calculations.

| Analysis type | Required CRS property | Recommended |
|---|---|---|
| Distance calculations | Projected (meters) | Local UTM or national grid |
| Area calculations | Equal-area | Albers, Mollweide, or national equal-area |
| Density / KDE | Projected (meters) | Local UTM |
| Web mapping / display only | Any (geographic OK) | WGS84 (EPSG:4326) |
| Spatial joins / overlays | Both layers must match | Reproject to analysis CRS first |

```python
# Determine appropriate CRS
import pyproj

if gdf.crs is None or gdf.crs.to_epsg() == 4326:
    # Need to project — estimate UTM zone from centroid
    centroid = gdf.geometry.unary_union.centroid
    utm_zone = int((centroid.x + 180) / 6) + 1
    hemisphere = 'north' if centroid.y >= 0 else 'south'
    epsg = 32600 + utm_zone if hemisphere == 'north' else 32700 + utm_zone
    gdf_proj = gdf.to_crs(epsg=epsg)
    print(f"Projected to EPSG:{epsg} (UTM Zone {utm_zone}{hemisphere[0].upper()})")
else:
    gdf_proj = gdf
```

**GUARDRAIL**: If the user's data is in EPSG:4326 and the analysis involves distances, areas, or density — project first. Never compute Euclidean distance on lat/lon.

### Step 1.3: Data Harmonization

If multiple datasets are involved:

1. **CRS alignment**: `assert gdf1.crs == gdf2.crs` before any spatial operation.
2. **Spatial join**: Use `gpd.sjoin(gdf1, gdf2, how='left', predicate='intersects')` — choose predicate carefully (`intersects`, `within`, `contains`).
3. **Temporal alignment**: Verify that datasets cover the same time period. Flag mismatches.
4. **Resolution mismatch**: If combining data at different spatial resolutions, document the aggregation/disaggregation method and warn about MAUP.
5. **Missing data**: Document missingness spatially — is it random or clustered? Clustered missingness biases spatial statistics.

### Step 1.4: Variable Preparation

- **Outlier inspection**: Box plots, z-scores. Do NOT auto-remove — investigate spatial context first (an "outlier" may be a real local phenomenon).
- **Skewness**: Check distributions. Log-transform only if theoretically justified and skewness > |2|.
- **Multicollinearity**: Compute VIF for regression predictors. VIF > 10 → drop or combine.
- **Standardization**: For GWR/MGWR, standardize predictors (mean=0, std=1) so bandwidths are comparable.

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

X = gdf_proj[feature_cols].dropna()
vif = pd.DataFrame({
    'Variable': X.columns,
    'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
print(vif.sort_values('VIF', ascending=False))
```

---

## Phase 2: Exploratory Spatial Data Analysis (ESDA)

**Always do ESDA before modeling.** It reveals patterns that inform method choice and catches data problems early.

### Step 2.1: Non-Spatial Summaries

- Descriptive statistics for outcome and predictors
- Histograms and distribution plots
- Correlation matrix (Pearson or Spearman depending on distributions)

### Step 2.2: Spatial Visualization

Choose map type based on data:

| Data type | Default map | When to use alternatives |
|---|---|---|
| Polygon counts/rates | Choropleth | Cartogram if area distortion matters |
| Point events | Point map | KDE if too many points overlap |
| Point values | Graduated symbols | Interpolated surface if continuous field |
| Raster | Continuous color map | Classified if discrete categories |

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf_proj.plot(column='outcome_var', cmap='viridis', legend=True,
              scheme='quantiles', k=5, ax=ax,
              edgecolor='0.8', linewidth=0.3)
ax.set_title('Outcome Variable Distribution')
ax.set_axis_off()
plt.tight_layout()
plt.savefig('spatial-analysis-outputs/fig_eda_choropleth.png', dpi=300, bbox_inches='tight')
```

**Classification choice matters.** Different schemes tell different stories:

| Scheme | Use when | Avoid when |
|---|---|---|
| `quantiles` | Want equal-count bins; good default | Distribution is multimodal |
| `natural_breaks` (Jenks) | Want to minimize within-class variance | Need reproducibility (algorithm is non-deterministic in some implementations) |
| `equal_interval` | Distribution is roughly uniform | Skewed data (most observations in one bin) |
| `std_mean` | Want to highlight deviation from mean | Non-normal distributions |
| `fisher_jenks` | Stable alternative to natural breaks | — |

**GUARDRAIL**: Never use a sequential colormap (e.g., `viridis`) for diverging data (e.g., residuals, change). Use a diverging colormap (`RdBu_r`, `coolwarm`) centered on zero or the mean.

### Step 2.3: Spatial Autocorrelation Screening

Run global Moran's I on the outcome variable to decide whether spatial modeling is needed:

```python
import libpysal
import esda

# Construct spatial weights — choose based on data type
# Polygons: Queen contiguity
W = libpysal.weights.Queen.from_dataframe(gdf_proj)
# Points: KNN (default k=8, adjust based on density)
# W = libpysal.weights.KNN.from_dataframe(gdf_proj, k=8)
# Distance band: use when irregular spacing
# W = libpysal.weights.DistanceBand.from_dataframe(gdf_proj, threshold=d)

W.transform = 'R'  # Row-standardize

moran = esda.Moran(gdf_proj['outcome_var'].values, W)
print(f"Moran's I: {moran.I:.4f}")
print(f"Expected I: {moran.EI:.4f}")
print(f"p-value: {moran.p_sim:.4f}")
print(f"z-score: {moran.z_sim:.4f}")
```

**Interpretation guide:**

| Moran's I p-value | Interpretation | Implication |
|---|---|---|
| p < 0.01 | Strong evidence of spatial autocorrelation | Spatial methods likely needed |
| 0.01 ≤ p < 0.05 | Moderate evidence | Spatial methods recommended; compare with OLS |
| p ≥ 0.05 | No significant spatial autocorrelation | OLS may be sufficient; still check residuals after modeling |

**Weights matrix choice is consequential.** Document your choice and reasoning:

| Weights type | Best for | Watch out for |
|---|---|---|
| Queen contiguity | Regular polygon tessellations (counties, census tracts) | Islands with no neighbors (add manual connections) |
| Rook contiguity | Grid-like polygons where corner adjacency is not meaningful | — |
| KNN (k=5-8) | Point data; irregular polygon sizes | k too small → disconnected components; k too large → smooths real variation |
| Distance band | When interaction decays with distance | Choice of threshold is arbitrary; try multiple |

**GUARDRAIL**: Always check for islands (observations with no neighbors): `W.islands`. If islands exist, they break spatial statistics. Either add manual neighbor connections or use KNN instead.

### Step 2.4: Local Pattern Detection (if global Moran's I is significant)

```python
# Local Moran's I (LISA)
lisa = esda.Moran_Local(gdf_proj['outcome_var'].values, W)
gdf_proj['lisa_cluster'] = lisa.q  # 1=HH, 2=LH, 3=LL, 4=HL
gdf_proj['lisa_sig'] = lisa.p_sim < SIGNIFICANCE_LEVEL

# Getis-Ord Gi* (hot/cold spots)
gstar = esda.G_Local(gdf_proj['outcome_var'].values, W, star=True)
gdf_proj['gstar_z'] = gstar.Zs
gdf_proj['gstar_sig'] = gstar.p_sim < SIGNIFICANCE_LEVEL
```

**When to use LISA vs Getis-Ord Gi*:**

| Method | Detects | Better when |
|---|---|---|
| LISA (Local Moran's I) | Clusters (HH, LL) AND outliers (HL, LH) | You care about both types of spatial association |
| Getis-Ord Gi* | Hot spots (high values) and cold spots (low values) only | You only care about concentration of high/low values |

**GUARDRAIL**: Multiple testing. With N spatial units, you run N local tests. Report the number of significant clusters at your chosen alpha AND note that some may be false positives. Consider using Bonferroni or FDR correction for conservative inference, or report both corrected and uncorrected results.

---

## Phase 3: Method Selection and Execution

Route to the appropriate analysis based on the objective from Phase 0.

### Route A: Explanation (Regression)

**Decision tree:**

```
Research question is explanatory
    │
    ├── Run OLS first (always)
    │   ├── Check residual Moran's I
    │   │   ├── p ≥ 0.05 → OLS is adequate. Report and stop.
    │   │   └── p < 0.05 → Spatial dependence in residuals. Continue.
    │   │
    │   ├── Is the spatial dependence substantive (spillover)?
    │   │   ├── Yes → Spatial Lag Model (ML_Lag)
    │   │   └── No / Nuisance → Spatial Error Model (ML_Error)
    │   │
    │   ├── Do relationships plausibly vary across space?
    │   │   ├── Yes, all at same scale → GWR
    │   │   └── Yes, at different scales → MGWR (preferred)
    │   │   └── No theoretical reason → Do NOT run GWR/MGWR
    │   │
    │   └── Compare models: AICc, R², residual Moran's I
    │       └── Report the best-fitting model with full diagnostics
```

#### Step 3A.1: OLS Baseline

```python
import statsmodels.api as sm

y = gdf_proj['outcome_var'].values.reshape(-1, 1)
X = gdf_proj[feature_cols].values
X = sm.add_constant(X)

ols = sm.OLS(y, X).fit(cov_type='HC3')
print(ols.summary())

# Residual spatial autocorrelation
residuals = ols.resid
moran_resid = esda.Moran(residuals, W)
print(f"Residual Moran's I: {moran_resid.I:.4f}, p={moran_resid.p_sim:.4f}")
```

**OLS diagnostics checklist:**
- [ ] R², Adjusted R²
- [ ] RMSE, MAE
- [ ] AIC, BIC
- [ ] Residual Moran's I (p-value)
- [ ] Breusch-Pagan test (heteroskedasticity)
- [ ] Jarque-Bera test (normality of residuals)
- [ ] VIF for all predictors (multicollinearity)
- [ ] Condition number (< 30 preferred)

#### Step 3A.2: Spatial Regression (if residual Moran's I is significant)

```python
from spreg import ML_Lag, ML_Error

# Spatial Lag Model
lag_model = ML_Lag(y, X, w=W, name_y='outcome', name_x=feature_cols)

# Spatial Error Model
error_model = ML_Error(y, X, w=W, name_y='outcome', name_x=feature_cols)
```

**Choose between lag and error:**

| Criterion | Spatial Lag | Spatial Error |
|---|---|---|
| Theory | Outcome in area i depends on outcome in neighbors | Unobserved factors with spatial structure affect the outcome |
| Example | Crime in one area spills to neighbors | Soil quality (unmeasured) varies smoothly across space |
| Diagnostic | Lagrange Multiplier (lag) significant | Lagrange Multiplier (error) significant |
| If both significant | Use Robust LM tests; pick the one that remains significant | If both remain significant, consider Spatial Durbin |

#### Step 3A.3: GWR / MGWR (only if theoretically justified)

**GUARDRAIL**: Do NOT run GWR/MGWR as a default. Run them only when:
1. There is a theoretical reason to expect spatially varying relationships (e.g., the effect of greenspace on health plausibly differs between urban and rural areas).
2. OLS or spatial lag/error models leave substantial residual spatial structure.
3. The research question asks about *where* relationships differ, not just *whether* they exist.

```python
from mgwr.gwr import GWR, MGWR
from mgwr.sel_bw import Sel_BW

# Prepare coordinates — MUST be in projected CRS
coords = np.column_stack((gdf_proj.geometry.x, gdf_proj.geometry.y))

# Standardize predictors for GWR/MGWR
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_std = scaler.fit_transform(gdf_proj[feature_cols].values)
X_std = np.column_stack((np.ones(X_std.shape[0]), X_std))  # add intercept
y_arr = gdf_proj['outcome_var'].values.reshape(-1, 1)

# Subsample if needed
n = len(gdf_proj)
if n > GWR_MAX_N:
    print(f"WARNING: n={n} exceeds GWR limit ({GWR_MAX_N}). Spatially stratified subsample recommended.")

# GWR
bw_sel = Sel_BW(coords, y_arr, X_std, kernel='bisquare', fixed=False)
bw = bw_sel.search()
gwr_model = GWR(coords, y_arr, X_std, bw=bw, kernel='bisquare', fixed=False).fit()

# MGWR (preferred — allows per-variable bandwidth)
if n <= MGWR_MAX_N:
    bw_sel_multi = Sel_BW(coords, y_arr, X_std, multi=True, kernel='bisquare', fixed=False)
    bws = bw_sel_multi.search(multi_bw_min=[2])
    mgwr_model = MGWR(coords, y_arr, X_std, selector=bw_sel_multi,
                       kernel='bisquare', fixed=False).fit()
```

**Interpret MGWR bandwidths:**

| Bandwidth range | Interpretation | Example |
|---|---|---|
| < 50 neighbors | Local process | Land use effects on temperature |
| 50–200 neighbors | Regional process | Socioeconomic gradients |
| > n/3 | Effectively global | Elevation effect on precipitation |

### Route B: Clustering / Hot Spot Detection

If the objective is clustering detection, the workflow is:

1. **Global test** (Moran's I or Getis-Ord General G) — is there spatial clustering at all?
2. **Local test** (LISA or Gi*) — where are the clusters?
3. **Visualize** — map significant clusters with appropriate symbology.
4. **Interpret** — what do the clusters mean substantively?

**GUARDRAIL**: If analyzing event counts (e.g., disease cases), always normalize by population at risk. Raw counts cluster where people live, not where rates are elevated. Use rates or standardized incidence ratios.

### Route C: Prediction

If the objective is prediction:

1. **Feature engineering** — include spatial features (coordinates, distance to landmarks, spatial lag of predictors, neighborhood summaries).
2. **Spatial cross-validation** — NEVER use random CV. Use spatial block CV to prevent data leakage from spatial autocorrelation.
3. **Model selection** — compare models by spatial CV performance, not in-sample fit.
4. **Residual check** — even for predictive models, check residual Moran's I. Remaining spatial structure means the model is missing a spatial predictor or process.

```python
from sklearn.model_selection import KFold
import mapclassify

# Create spatial folds using geographic blocks
# Option 1: Grid-based blocks
gdf_proj['block'] = pd.cut(gdf_proj.geometry.x, bins=SPATIAL_CV_FOLDS, labels=False)

# Option 2: K-means clustering on coordinates (more balanced)
from sklearn.cluster import KMeans
coords_for_cv = np.column_stack((gdf_proj.geometry.x, gdf_proj.geometry.y))
gdf_proj['spatial_fold'] = KMeans(n_clusters=SPATIAL_CV_FOLDS, random_state=42).fit_predict(coords_for_cv)
```

### Route D: Accessibility / Network Analysis

```python
import osmnx as ox
import networkx as nx

# Download street network
G = ox.graph_from_place("City Name", network_type='drive')

# Compute shortest paths / isochrones
# Service area analysis, 2SFCA, etc.
```

Only invoke network analysis when the research question specifically concerns accessibility, reachability, or service coverage. Do not add network analysis to a regression workflow just because it exists.

### Route E: Interpolation

Use interpolation only when the goal is estimating values at unsampled locations from point observations.

```python
from pykrige.ok import OrdinaryKriging

# Always fit and inspect the variogram first
OK = OrdinaryKriging(x, y, z, variogram_model='spherical')
z_pred, z_var = OK.execute('grid', gridx, gridy)
```

**GUARDRAIL**: Interpolation is not prediction in the regression sense. It assumes spatial continuity. If the variable is not spatially continuous (e.g., categorical land use), interpolation is inappropriate.

---

## Phase 4: Diagnostics and Validation

### Step 4.1: Model Diagnostics (for regression workflows)

| Diagnostic | What it checks | Tool |
|---|---|---|
| Residual Moran's I | Remaining spatial autocorrelation | `esda.Moran(residuals, W)` |
| Breusch-Pagan | Heteroskedasticity | `statsmodels.stats.diagnostic.het_breuschpagan()` |
| Jarque-Bera | Normality of residuals | `statsmodels.stats.stattools.jarque_bera()` |
| VIF | Multicollinearity | `statsmodels.stats.outliers_influence.variance_inflation_factor()` |
| Cook's distance | Influential observations | `ols.get_influence().cooks_distance` |
| AICc comparison | Model selection | Lower is better; prefer simpler model if AICc difference < 2 |

### Step 4.2: Model Comparison Table

Always produce a comparison table when multiple models are run:

```markdown
| Model | R² | Adj. R² | AICc | RMSE | Residual Moran's I | p(Moran) |
|-------|-----|---------|------|------|--------------------|----------|
| OLS   |     |         |      |      |                    |          |
| Spatial Lag |  |      |      |      |                    |          |
| Spatial Error | |     |      |      |                    |          |
| GWR   |     |         |      |      |                    |          |
| MGWR  |     |         |      |      |                    |          |
```

**Model selection logic:**
1. Best AICc among candidates (with > 2 difference being meaningful).
2. Residual Moran's I closest to 0 (spatial autocorrelation resolved).
3. If AICc and Moran's I disagree, prefer the model that resolves spatial autocorrelation — biased standard errors are worse than slightly lower fit.
4. Prefer the simpler model when differences are marginal.

### Step 4.3: Robustness Checks

Depending on the analysis, consider:

- **Sensitivity to spatial weights**: Re-run key statistics with a different weights matrix (e.g., KNN instead of Queen). If results change substantially, report this.
- **Sensitivity to spatial scale (MAUP)**: If data can be aggregated to a different level, test whether conclusions hold. If not feasible, acknowledge the limitation.
- **Boundary effects**: Observations at study area edges have fewer neighbors. Note potential bias.
- **Temporal mismatch**: If combining datasets from different years, explicitly acknowledge the assumption that spatial patterns are stable over that period.

---

## Phase 5: Visualization and Communication

### Step 5.1: Publication-Quality Maps

Every map must include:
- [ ] Clear title
- [ ] Legend with units and classification scheme named
- [ ] Scale bar
- [ ] North arrow (if convention for the venue requires it)
- [ ] CRS stated in caption
- [ ] Source attribution for basemap (if used)
- [ ] Consistent color scheme across related maps

```python
import matplotlib.pyplot as plt
import contextily as cx

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf_proj.plot(column='outcome_var', cmap='viridis', legend=True,
              scheme='fisher_jenks', k=5, ax=ax,
              edgecolor='0.8', linewidth=0.3,
              legend_kwds={'title': 'Outcome (units)', 'loc': 'lower right'})

# Add basemap (requires Web Mercator or auto-reproject)
# cx.add_basemap(ax, crs=gdf_proj.crs, source=cx.providers.CartoDB.Positron)

ax.set_title('Title', fontsize=14, fontweight='bold')
ax.set_axis_off()
plt.tight_layout()
plt.savefig('spatial-analysis-outputs/fig_main_map.png', dpi=300, bbox_inches='tight')
```

### Step 5.2: Diagnostic Plots

| Plot | When to include | Purpose |
|---|---|---|
| Residual map | Any regression | Visual check for spatial patterns in residuals |
| LISA cluster map | When clustering is detected | Show HH, HL, LH, LL significant clusters |
| Coefficient map (GWR/MGWR) | When local coefficients vary | Show where each predictor is strong/weak |
| Local R² map | GWR/MGWR | Show where the model fits well vs poorly |
| Moran scatter plot | When reporting Moran's I | Visual complement to the statistic |
| QQ plot of residuals | Regression diagnostics | Check normality assumption |

### Step 5.3: Color Scheme Rules

| Variable type | Colormap | Example |
|---|---|---|
| Sequential (counts, rates) | `viridis`, `YlOrRd`, `Blues` | Population density |
| Diverging (residuals, change, coefficients) | `RdBu_r`, `coolwarm`, `PiYG` | Regression residuals |
| Categorical (clusters, land use) | `Set2`, `tab10`, custom | LISA clusters |

**GUARDRAIL**: Never use rainbow/jet colormaps. They are perceptually non-uniform and misleading.

---

## Phase 6: Write Interpretation

### Step 6.1: Analysis Narrative

Write a 3-6 paragraph interpretation to `spatial-analysis-outputs/analysis_report.md`:

```markdown
# Spatial Analysis Report

**Research Question**: [question]
**Date**: [today]
**Data**: [description — N, spatial extent, time period]

## Data and Study Area
[Para 1: Data sources, spatial units, sample size, key variables, CRS used]

## Exploratory Findings
[Para 2: Distribution of outcome, initial spatial patterns, global Moran's I result]

## Model Results
[Para 3: Model comparison table, best model selection rationale]

## Key Spatial Patterns
[Para 4: For GWR/MGWR — which variables vary locally, where are effects strongest/weakest]
[For clustering — where are hot/cold spots, what characterizes them]

## Diagnostics and Robustness
[Para 5: Residual spatial autocorrelation status, sensitivity checks, caveats]

## Implications
[Para 6: What the results mean for the research question, limitations, next steps]
```

### Step 6.2: Update Project Files

- Append key findings to `findings.md` (one line each).
- Update `memory/MEMORY.md` if results feed into the broader research pipeline.
- If this analysis feeds into `geo-experiment`, write results to `geo_benchmark/results/` in the expected JSON format.

---

## Guardrails: Common Mistakes This Skill Prevents

| Mistake | How this skill prevents it |
|---|---|
| Using lat/lon for distance calculations | Phase 1 Step 1.2 forces CRS check and projection |
| Applying Moran's I without thoughtful weights choice | Phase 2 Step 2.3 requires explicit weights justification |
| Interpreting raw count clusters as rate clusters | Route B guardrail: normalize by population at risk |
| Running GWR/MGWR by default | Route A Step 3A.3 guardrail: require theoretical justification |
| Ignoring MAUP | Phase 4 Step 4.3 includes scale sensitivity check |
| Random CV on spatial data | Route C forces spatial block CV |
| Reporting OLS when residuals are spatially autocorrelated | Route A decision tree forces spatial model if Moran's I significant |
| Misleading map classification | Phase 2 Step 2.2 table guides classification choice |
| Rainbow colormaps | Phase 5 Step 5.3 explicitly bans rainbow/jet |
| Overclaiming causality from observational spatial data | Phase 0 Step 0.1 distinguishes explanation from causal inference |
| Mixing incompatible spatial resolutions silently | Phase 1 Step 1.3 requires documenting resolution mismatch |
| Treating significance as substantive importance | Phase 6 narrative requires effect size interpretation, not just p-values |
| Overcomplicating when simple methods suffice | Phase 0 Step 0.3 checks whether spatial methods are even needed |

---

## Outputs

- `spatial-analysis-outputs/question_classification.md` — Research question classification and method candidates
- `spatial-analysis-outputs/analysis_report.md` — Full analysis narrative
- `spatial-analysis-outputs/model_comparison.md` — Model comparison table (if regression)
- `spatial-analysis-outputs/scripts/` — All Python scripts used (for reproducibility)
- `spatial-analysis-outputs/figures/` — All maps and diagnostic plots
- `findings.md` — One-line findings appended
- `geo_benchmark/results/` — JSON results (if feeding into geo-experiment pipeline)

---

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- **Research question first.** Never start with a method. Start by classifying the question.
- **Justify every method choice.** If you cannot explain why a method is needed for this question, do not use it.
- **OLS before spatial models.** Always establish the non-spatial baseline.
- **Document CRS decisions.** Every analysis must state which CRS was used and why.
- **Parsimonious workflows.** If a choropleth and summary statistics answer the question, do not run MGWR.
- **Honest interpretation.** Report effect sizes, not just significance. Acknowledge limitations. Never claim causality from cross-sectional observational data without explicit justification.
- **Reproducibility.** Save all scripts to `spatial-analysis-outputs/scripts/`. Log all parameter choices.
- **Do not fabricate results.** Only report numbers that came from executed code.
- **Respect computational limits.** GWR maxes at ~5,000 observations; MGWR at ~3,000. Subsample with spatial stratification if needed.

## Composing with Other Skills

This skill connects to the broader research pipeline:

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
- **From geo-experiment**: If `geo-experiment` runs OLS/GWR/MGWR via `geo_benchmark/run_benchmark.py`, this skill interprets those results. Read from `geo_benchmark/results/`.
- **To paper-figure**: This skill produces draft figures in `spatial-analysis-outputs/figures/`. The `paper-figure` skill can polish them with cartographic conventions.
- **To result-to-claim**: This skill's model comparison table feeds directly into claim validation.
- **Knowledge base**: Read `skills/knowledge/spatial-methods.md` for code snippets, CRS reference table, and detailed method parameters.
