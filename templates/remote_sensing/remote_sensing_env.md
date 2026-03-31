# Remote Sensing of Environment (RSE)
## Paper Template & Formatting Guide

**Publisher**: Elsevier
**Impact Factor**: ~14
**Scope**: Remote sensing of land, ocean, atmosphere; algorithms, validation, applications

---

## Submission Requirements

| Requirement | Specification |
|-------------|--------------|
| Article types | Research Article, Letter to Editor, Review |
| Word limit | 10,000 words (Research Article) |
| Abstract | 300 words maximum, structured preferred |
| Keywords | 6 keywords |
| Highlights | 3–5 bullet points (85 chars each max) |
| References | Numbered (Vancouver style) |
| Figures | 300 DPI, TIFF/EPS/PDF |
| Graphical abstract | Required (400×300 px) |

---

## Required Paper Structure

### Highlights (3–5 bullets, ≤85 chars each)
```
• Novel MGWR framework for urban LST mapping across 100 cities
• Spatial non-stationarity revealed in all climate zones
• MGWR outperforms GWR by 23% RMSE reduction
• Open-source Python implementation provided
• Validated against independent Landsat-8 scenes
```

### Title
Descriptive and specific. Include sensor/data type, geographic scope, and method.

### Abstract (≤300 words)
**Background**: Why this topic matters.
**Objectives**: Specific aims of the study.
**Methods**: Data sources (sensor, resolution, dates), algorithm, validation approach.
**Results**: Key quantitative findings.
**Conclusions**: Significance and recommendations.

### Keywords (6)
Include: sensor/data type, method, application, geographic region.

### 1. Introduction
- Remote sensing context and significance
- State-of-the-art methods and their limitations
- Data gaps (missing sensors, temporal gaps, spatial resolution trade-offs)
- Explicit research objectives

### 2. Study Area and Data
#### 2.1 Study Area
- Geographic extent, coordinates, climate zone
- Why this area for this study
- Ground truth/validation data sources

#### 2.2 Satellite/Remote Sensing Data
For each dataset:
- Sensor name and platform
- Band(s) used with wavelength range
- Spatial resolution (ground sampling distance)
- Temporal coverage and revisit time
- Atmospheric correction method applied
- Cloud masking approach

#### 2.3 Ancillary Data
In-situ measurements, DEM, land cover, etc.

### 3. Methods
#### 3.1 Preprocessing
- Geometric registration and orthorectification
- Radiometric calibration (DN → reflectance/radiance)
- Atmospheric correction (algorithm, inputs, parameters)

#### 3.2 Feature Extraction / Index Calculation
Include equations for all indices (NDVI, LST, etc.)

#### 3.3 Model Development
Full mathematical description. State all tuning parameters.

#### 3.4 Accuracy Assessment
- Reference data collection method
- Train/test split or cross-validation strategy
- Metrics: RMSE, MAE, R², bias, OA, Kappa (as appropriate)
- Uncertainty quantification

### 4. Results
#### 4.1 Preprocessing Validation
#### 4.2 Model Performance
- Quantitative metrics table (required)
- Comparison with baseline/existing methods
- Spatial distribution maps

#### 4.3 Spatial Patterns
- Describe geographic patterns in results
- Temporal patterns if multi-date

### 5. Discussion
- Physical interpretation of results (not just statistics)
- Comparison with published benchmarks
- Sensitivity analysis if applicable
- Error sources: atmospheric, geometric, algorithm
- Transferability and generalizability

### 6. Conclusions

### CRediT Author Contribution Statement
(Required by Elsevier)

### Data Availability
Repository link with DOI (Zenodo, GitHub release, etc.)

---

## RSE-Specific Requirements

- **Validation is mandatory**: All algorithms must be validated against independent reference data
- **Uncertainty**: Quantify uncertainty in all derived products
- **Reproducibility**: Code must be available (GitHub + Zenodo DOI)
- **Graphical abstract**: Required for all submissions
- **Color figures**: Free in online version; check print requirements

## Pre-submission Checklist

- [ ] Graphical abstract prepared (400×300 px)
- [ ] Highlights provided (3–5, ≤85 chars)
- [ ] Sensor metadata complete (resolution, dates, preprocessing)
- [ ] Independent validation dataset described
- [ ] Accuracy metrics table included
- [ ] Code/data deposited with DOI
- [ ] Abstract ≤300 words
- [ ] CRediT statement included
