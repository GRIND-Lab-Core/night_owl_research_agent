# International Journal of Geographical Information Science (IJGIS)
## Paper Template & Formatting Guide

**Publisher**: Taylor & Francis
**Impact Factor**: ~4.5
**Scope**: Algorithms, data structures, spatial analysis, geocomputation, cartography, spatial databases

---

## Submission Requirements

| Requirement | Specification |
|-------------|--------------|
| Word limit | 8,000 words (excl. references, tables, figures) |
| Abstract | 200 words maximum |
| Keywords | 6–8 keywords |
| References | APA style (Taylor & Francis) |
| Figures | 300 DPI minimum, TIFF/EPS preferred |
| Supplemental | Encouraged for code and data |

---

## Required Paper Structure

### Title
Clear, specific, ≤15 words. Avoid abbreviations. Include spatial/geographic scope.

Example: *Multiscale geographically weighted regression for analyzing urban heat island effects across 50 US cities*

### Authors & Affiliations
Full name, institution, city, country, ORCID.

### Abstract (≤200 words)
Structure: Background (1–2 sentences) → Gap (1 sentence) → Objective (1 sentence) → Methods (2 sentences) → Key findings (2 sentences) → Implications (1 sentence).

### Keywords (6–8)
Include: geographic/spatial term, method, application domain, geographic region (if applicable).

### 1. Introduction
- 4–5 paragraphs
- Background → specific problem → gap in literature → study objective
- End with: *"The specific objectives of this study are: (1)..., (2)..., (3)..."*
- Cite recent IJGIS papers where relevant

### 2. Related Work / Background
- Review of relevant methods
- Position your contribution relative to existing work
- Identify specific limitations your study addresses

### 3. Study Area (if applicable)
- Geographic extent with coordinates (WGS84)
- Key spatial characteristics justifying study area choice
- Include a study area map (Figure 1)

### 4. Data
For each dataset:
- Source and access URL/DOI
- Temporal coverage
- Spatial resolution / scale
- Coordinate Reference System (EPSG code)
- Preprocessing steps

### 5. Methods
- Provide equations for all mathematical models
- Specify all hyperparameters/tuning choices
- Name all software libraries and versions
- Describe spatial validation strategy (how you avoid spatial autocorrelation leakage in train/test)

#### 5.x Model Formulation
```
Y_i = β_0(u_i, v_i) + Σ β_k(u_i, v_i) X_ik + ε_i
where (u_i, v_i) denotes coordinates of observation i
```

### 6. Results
- Report quantitative metrics with confidence intervals
- Reference all figures and tables
- Test for spatial autocorrelation in residuals (Moran's I)
- Note geographic patterns in results

### 7. Discussion
- Interpret spatial patterns (the *why*, not just the *what*)
- Compare with benchmark/baseline results and explain differences
- Discuss scale dependency if relevant
- Limitations: data quality, method assumptions, geographic scope

### 8. Conclusions
- Summarize key contributions (numbered)
- Practical/policy implications
- Future research directions

### Acknowledgements
Funding sources, data providers, computing resources.

### Data Availability Statement
"All data and code used in this study are openly available at [DOI]."

### References
APA 7th Edition. Include DOIs for all references.

---

## Figures and Maps

- All maps must specify the CRS/projection
- Include scale bar and north arrow on all maps
- Use color-blind-accessible palettes (ColorBrewer recommended)
- Figure captions must be self-contained

## Checklist Before Submission

- [ ] Abstract ≤200 words
- [ ] Total ≤8,000 words
- [ ] CRS stated for all spatial datasets
- [ ] Moran's I reported for residuals
- [ ] All figures at 300 DPI
- [ ] Code/data deposited in repository with DOI
- [ ] Spatial autocorrelation in model evaluation addressed
- [ ] Author contributions statement included
