# Geo-Specialist Review
**Study:** Soundscape-Conditioned Street-Level Image Generation — Spatial Analysis Component
**Reviewer:** Geo-Specialist Agent (GeoResearchAgent-247)
**Date:** 2026-04-01
**Input files reviewed:** `memory/gap-analysis.md`, `memory/synthesis-2026-04-01.md`, `program.md`

---

## 1. CRS Validation

All three city projections stated in `program.md` Section 7 are correct and appropriate for metric-unit distance computation and area calculation. Confirmed EPSG codes:

| City | UTM Zone | EPSG | Notes |
|------|----------|------|-------|
| New York City | UTM Zone 18N | EPSG:32618 | Covers Manhattan through outer boroughs; correct |
| London | UTM Zone 30N | EPSG:32630 | Correct for central London; entire Greater London authority fits within this zone |
| Singapore | UTM Zone 48N | EPSG:32648 | Correct; Singapore spans 103.6–104.0°E, fully within Zone 48N (102°–108°E) |

**No CRS issues flagged.** All three are WGS84-based UTM projections providing metric units without significant distortion at these city extents.

**Required practice:** Store all raw data in WGS84 (EPSG:4326), reproject to city-specific UTM for all distance, area, and spatial weight computations, and reproject to EPSG:3857 only if web map tiles are needed for figure display. Do not mix UTM zones within a single spatial weights matrix. Per-city models must use per-city UTM. If any pooled cross-city analysis is conducted, reproject to a common equal-area reference (EPSG:6933, WGS84 / NSIDC EASE-Grid 2.0 Global, or individually to each city UTM with documented coordinate transformation) — do not pool coordinates in decimal degrees.

---

## 2. Sample Size Review — GWR and MGWR Limits

Expected spatial unit counts per city: ~2,000–5,000 (500 m grid cells or street segments).

**GWR (limit: 5,000 obs)**

| City | Expected n | GWR feasibility |
|------|-----------|-----------------|
| NYC | ~4,000–5,000 | Borderline; enforce hard cap at 5,000 |
| London | ~3,000–4,500 | Acceptable |
| Singapore | ~1,500–2,500 | Well within limit |

If NYC approaches 5,000, apply systematic spatial subsampling before GWR: use a regular hexagonal grid subsample (H3 resolution 8 ~460 m) to select the spatially most representative subset. Do not use random subsampling — it disrupts spatial autocorrelation structure.

**MGWR (limit: 3,000 obs)**

All three cities likely exceed 3,000 at 500 m grid resolution, particularly NYC and London. Required subsampling strategy:

- Aggregate to 700–800 m grid cells (instead of 500 m) to reduce n toward 2,000–2,500 per city while preserving spatial resolution adequate for neighborhood-scale acoustic variation.
- Alternatively, retain 500 m cells but apply H3-based spatial stratified sampling to draw 2,500 representative cells per city, stratifying by land use class (residential, commercial, mixed, industrial, green) to preserve composition.
- Document the subsampling method fully; report both the full-n GWR result and the subsampled MGWR result side by side so reviewers can assess sensitivity.

**Recommended per-city target sample sizes:**

| Model | NYC | London | Singapore |
|-------|-----|--------|-----------|
| OLS | All cells, up to ~5,000 | All cells, up to ~4,500 | All cells, ~2,000 |
| GWR | Max 5,000 (subsample if needed) | Max 5,000 | All cells |
| MGWR | 2,500 (stratified spatial subsample) | 2,500 (stratified spatial subsample) | All cells (~2,000) |

---

## 3. Spatial Autocorrelation and Bandwidth Selection

**Moran's I — run before regression, not only after.**

Compute Moran's I on the raw dependent variable (per-cell LPIPS or FID) before model fitting. This establishes the baseline spatial autocorrelation and justifies the use of spatial regression over OLS. Expected outcome based on analogous literature (Fan et al., IJGIS 2020; Shen et al., TGRS 2022): Moran's I of generation quality metrics will likely fall in the range 0.15–0.35 for 500 m urban grid cells, given that visual scene quality co-varies with land use clustering and morphological regularity, both of which are strongly spatially autocorrelated.

**Bandwidth selection — use AICc-based golden section search.**

Do not use cross-validation (CV) bandwidth selection for this study design. Use AICc minimization for all GWR and MGWR bandwidth calibration:

- GWR bandwidth: AICc golden section search over the range [10, min(n, 500)] neighbors (adaptive bisquare kernel). Recommended initial search range: k = 30–300 neighbors. For 500 m urban cells in NYC, expected optimal bandwidth is likely in the range of 40–120 neighbors (approximately 2–6 km effective spatial scale at 500 m cell spacing), consistent with neighborhood-level acoustic variation.
- MGWR per-variable bandwidth: each predictor gets its own bandwidth via backfitting algorithm with AICc stopping criterion. Expected bandwidth variation by covariate type:
  - A-weighted SPL and road hierarchy: local bandwidth (k ~ 30–80 neighbors; sub-kilometer to 1–2 km) — these vary sharply at street level.
  - Land use entropy and building density: regional bandwidth (k ~ 80–200 neighbors; 2–5 km) — these reflect neighborhood-scale zones.
  - Time-of-day and city-level acoustic character: potentially global bandwidth (k ~ n; effectively a global coefficient) — these may not exhibit meaningful spatial variation.

Report per-variable bandwidths in the paper as "local / regional / global" following Fotheringham et al. (2017) terminology, converting neighbor counts to approximate metric distances (multiply k by mean inter-cell spacing).

**Spatial lag range:** At 500 m cell spacing in a dense urban grid, spatial effects in soundscape-visual correspondence are expected to be meaningful at 1–5 km. Moran's I correlogram (compute I at lag distances 500 m, 1 km, 2 km, 3 km, 5 km, 10 km) should be reported to document the effective range of spatial dependence before selecting bandwidth bounds.

---

## 4. Spatial Cross-Validation Recommendation

**Use spatial block cross-validation. Do not use random k-fold CV.**

The dependent variable (per-location generation quality) will exhibit spatial autocorrelation. Random CV artificially inflates predictive performance because test observations are spatially adjacent to training observations and share local autocorrelation structure. This produces optimistic R² and RMSE estimates that do not reflect true out-of-sample generalization.

**Recommended approach: spatial block CV with 5 folds per city.**

- Divide each city into 5 spatially contiguous blocks using either (a) regular rectangular blocks aligned with the UTM grid, or (b) k-means spatial clustering on centroids (using libpysal `skater` or `spopt` regionalization).
- Minimum block size: at least 3× the expected GWR bandwidth radius to ensure adequate spatial separation between train and test blocks. At k ~ 60 neighbors and 500 m spacing, this corresponds to blocks of at least 3 km radius.
- For the spatial regression models (OLS/GWR/MGWR), report leave-one-block-out RMSE and R² alongside in-sample fit statistics.

**Buffered leave-one-out (LOBO)** is appropriate only if the sample is very small (n < 200 per city). At the expected n of 2,000–5,000, block CV is computationally feasible and statistically more informative.

**For the generative model evaluation** (training the diffusion model itself, separate from spatial regression), use a city-level train/test split: train on NYC + London, test on Singapore, and report cross-city FID/SSIM as the zero-shot generalization result. This is consistent with gap T3 and with the multi-city design in `program.md` Section 7.

---

## 5. Dependent Variable Construction — Per-Image LPIPS as Spatial Variable

**Per-image LPIPS is a valid foundation but requires careful spatial aggregation before use as a spatial regression dependent variable.**

Issues with using raw per-image scores:
- A single 500 m cell may contain 5–50 Mapillary images depending on street density. Each image will have its own LPIPS score relative to the generated output. These raw scores have high within-cell variance driven by viewing direction, occlusion, and image quality, not by soundscape conditioning quality.
- Using a single image per cell risks selection bias (which image represents the cell?).
- Per-image scores violate spatial stationarity assumptions if camera-level confounders (direction, time of capture, image resolution) are not controlled.

**Recommended aggregation procedure:**

1. For each spatial unit (grid cell or street segment), collect all Mapillary images with centroids falling within the cell boundary.
2. Compute LPIPS score for each image relative to the generated counterpart (generated from the cell's acoustic and spatial covariates).
3. Aggregate to cell level using the median LPIPS score (not mean — LPIPS is bounded [0,1] but distributions are right-skewed; median is more robust to outlier images).
4. Require a minimum of 3 images per cell. Cells with fewer than 3 images should be excluded from the spatial regression sample.
5. Compute cell-level interquartile range (IQR) of LPIPS as an auxiliary variable capturing within-cell generation consistency. Report the spatial distribution of this IQR in supplementary figures — high IQR cells identify locations where acoustic conditioning is unreliable.

**For FID:** FID cannot be computed per-image; it is a distribution-level metric requiring a minimum of ~50 images. If using FID as the spatial dependent variable, aggregate to neighborhood (GADM level 4 or OSM postal district) or use tiles with sufficient image count. At 500 m cell spacing this will likely require 750 m–1 km cells in lower-density areas of London and Singapore. SSIM and LPIPS are more appropriate for 500 m cell-level analysis.

**Recommended primary dependent variable:** Median per-cell LPIPS score (lower = better generation quality), supplemented by mean SSIM. Report per-city distribution statistics (mean, SD, spatial Moran's I) before regression.

---

## 6. Moran's I — Spatial Weights Matrix Recommendation

**Use a distance-based k-nearest-neighbor (k-NN) spatial weights matrix, not queen contiguity.**

Rationale:
- Queen contiguity is appropriate for regular lattice data (e.g., census tracts with shared boundaries). The proposed spatial units are either 500 m grid cells (regular lattice, where queen contiguity is acceptable) or street segments (irregular network topology, where queen contiguity is poorly defined and produces unequal neighbor counts).
- For street segments, k-NN distance-based weights are essential because segment lengths vary and contiguity-based neighbors would produce spatial weights matrices with highly variable row lengths.
- Even for regular grid cells, distance-based k-NN weights (with k chosen to reflect the expected spatial interaction range) will be more informative for this study because acoustic propagation follows continuous distance decay, not hard cell-boundary adjacency.

**Recommended specifications:**

| Analysis | Weights type | k / distance threshold | Row standardization |
|----------|-------------|----------------------|---------------------|
| Moran's I on raw LPIPS | k-NN, k=8 | 8 nearest centroids | Row-standardized (W) |
| Moran's I on OLS residuals | k-NN, k=8 | 8 nearest centroids | Row-standardized (W) |
| Moran's I on GWR residuals | k-NN, k=8 | 8 nearest centroids | Row-standardized (W) |
| Moran's I on MGWR residuals | k-NN, k=8 | 8 nearest centroids | Row-standardized (W) |
| Sensitivity check | Queen contiguity | — | Row-standardized (W) |

Use k=8 for all primary Moran's I calculations (consistent with 8 surrounding cells in a regular grid, and with the urban acoustic interaction range at 500 m cell spacing). Run a sensitivity check with k=4 and k=12 and report in a supplementary table.

Build spatial weights using `libpysal.weights.KNN` with `k=8`, computed on projected UTM coordinates (not WGS84 decimal degrees). Report the resulting weights summary (mean neighbors, min neighbors, max neighbors) in the methods section.

**Expected Moran's I benchmarks from analogous literature:**

| Stage | Expected Moran's I | Threshold for action |
|-------|-------------------|---------------------|
| Raw LPIPS (pre-regression) | 0.15–0.35 | I > 0.1: spatial regression required |
| OLS residuals | 0.10–0.25 | I > 0.1: adopt GWR/spatial lag model |
| GWR residuals | 0.05–0.12 | I > 0.1: consider MGWR or spatial error |
| MGWR residuals | < 0.08 | Target; Fan et al. (2020) achieved I=0.08 |

If MGWR residual Moran's I exceeds 0.10, run a spatial error model (PySAL `spreg.ML_Error`) as an additional baseline.

---

## 7. Multi-City Pooling Strategy

**Run per-city models first. Pool only with appropriate fixed effects and after confirming cross-city coefficient stability.**

Pooling NYC, London, and Singapore into a single OLS/GWR/MGWR model without controls is methodologically unsound because:
- Acoustic environments differ fundamentally across cities (different baseline SPL, traffic density, building typology, green space patterns).
- LPIPS distributions will differ across cities if models are not equally trained on each city's imagery.
- The three UTM coordinate systems are incompatible — pooling requires a common projected CRS that may introduce distortion.
- The primary scientific question is whether spatial effects are consistent across cities, which requires per-city models to be compared, not a single pooled estimate.

**Recommended analysis sequence:**

1. **Per-city OLS:** Run OLS separately for NYC (EPSG:32618), London (EPSG:32630), Singapore (EPSG:32648). Report R², coefficient estimates, and Moran's I of residuals for each.
2. **Per-city GWR:** Run GWR per city using AICc bandwidth. Report local R² maps and coefficient maps per city.
3. **Per-city MGWR:** Run MGWR per city on subsampled n ≤ 3,000. Report per-variable bandwidths, spatially varying coefficient maps, and global-local classification.
4. **Cross-city comparison:** Compare OLS coefficients across cities using a meta-analytic approach (test whether coefficients are statistically indistinguishable across cities using Chow test or coefficient confidence interval overlap). Report this as a cross-city generalizability result.
5. **Pooled model with fixed effects (optional, for supplementary):** If a pooled model is desired for a single summary table, project all cities to WGS84 (EPSG:4326) with city dummy variables (London = 0, NYC = 1, Singapore = 2) and include city-level fixed effects. Do not run GWR or MGWR on a pooled dataset with mixed UTM coordinates.

**Required fixed effects in any pooled OLS:**
- City dummy variables (2 dummies for 3 cities, London as reference)
- Season/month of acoustic measurement (acoustic environments vary seasonally)
- Time-of-day category (morning peak / off-peak / evening peak) if not already an independent variable
- Image capture year (Mapillary imagery spans multiple years; visual scene may differ from acoustic measurement year)

---

## 8. Additional Dataset Recommendations

The following open datasets are not listed in `program.md` Section 8 but strengthen the spatial analysis component:

**Acoustic covariates:**
- **Noise-Planet / NoiseCapture mobile app database** (https://noise-planet.org/noiseplanet.html): Crowdsourced A-weighted SPL measurements with GPS timestamps. Provides point-level LAeq observations for NYC, London, and Singapore; can be spatially aggregated to 500 m cells. Note: coverage is sparser in Singapore than NYC/London — check record counts before committing to this source for Singapore.
- **BN-LOUD (British Noise database)** (https://environment.data.gov.uk/noise/): UK government statutory noise mapping data (LAden and Lnight) at 10 m resolution for London, derived from EU Environmental Noise Directive reporting. Provides authoritative road traffic and rail noise contours that can be spatially joined to your 500 m cells. Higher quality than Noise-Planet for London street-segment noise levels.
- **NYC DEP Noise Complaint Data** (NYC Open Data, https://data.cityofnewyork.us/): Geotagged noise complaints as a proxy for high-event soundscape locations. Useful as a binary covariate (high-complaint cell vs. low-complaint cell) to stratify the spatial analysis.

**Urban morphology:**
- **Global Human Settlement Layer — Building Height (GHS-BUILT-H)** (https://ghsl.jrc.ec.europa.eu/ghs_builtH2023.php): 100 m resolution mean building height raster (2023 release). Not listed in `program.md` but building height is a primary determinant of acoustic canyon effects and sky view factor. Include as a covariate alongside GHS-BUILT-S (density). EPSG:4326 native; reproject to city UTM before extraction.
- **Sky View Factor (SVF) from Global Urban Morphology dataset** (Biljecki et al., 2021 supplementary; or compute from GHS-BUILT-H via PyUFSA or urbanformviz): SVF is listed in the prompt as an independent variable but is not in `program.md` datasets. For NYC, the NYC 3D buildings dataset (DOITT, NYC Open Data) provides building footprints + heights at parcel level, enabling SVF computation via raytracing.
- **OpenStreetMap Green View Index proxy**: NDVI from Sentinel-2 Level-2A (10 m, ESA Copernicus Open Access Hub) composited over the study period provides a consistent green view proxy across all three cities. Use summer composites (June–August) for NYC and London; use dry-season composites (February–April) for Singapore.

**Acoustic reference — ISO 12913 validation:**
- **ARAUS dataset** (Ooi et al., 2022; https://github.com/ntudsp/araus-dataset): Already cited in the synthesis. This dataset provides ISO 12913 pleasantness and eventfulness annotations for 600 augmented urban soundscapes. Relevant for validating the acoustic feature extraction pipeline (mapping raw audio embeddings to pleasantness/eventfulness scores before conditioning). Not a spatial dataset, but directly relevant for conditioning signal construction.

**Street segment network:**
- **OSMnx** (Boeing, 2017; https://osmnx.readthedocs.io): Not a dataset but the standard Python tool for extracting routable street networks from OSM for NYC, London, and Singapore. Use `ox.graph_from_place()` to extract the primal graph, then `ox.geocode_to_gdf()` for administrative boundaries. Provides street-segment spatial units directly if street segments are preferred over grid cells. Segment-level acoustic data can then be joined via spatial proximity (nearest-neighbor join within 50 m tolerance in UTM).

---

## 9. Red Flags — Spatial Analysis Pitfalls

### Red Flag 1: Temporal mismatch between acoustic measurements and Mapillary imagery
The acoustic data (SoundingEarth, Noise-Planet) and Mapillary imagery will likely not share the same collection dates, and in many cases will differ by 2–5 years. Mapillary imagery in NYC was densely collected 2015–2020; Noise-Planet crowdsourced measurements are ongoing but temporally sparse. A 500 m cell might have acoustic data from 2022 and Mapillary imagery from 2017, before a major development project changed the visual scene. This temporal mismatch is a direct confound for the LPIPS-based dependent variable: the generated image is conditioned on acoustic inputs from one year, but the reference image against which LPIPS is computed shows the scene from a different year.

**Required mitigation:** For each spatial unit, document the date range of Mapillary images and the date of acoustic measurements. Flag and exclude cells where the temporal gap exceeds 3 years. Report the distribution of temporal gaps in the supplementary material. If temporal gap is large for a significant fraction of cells (>20%), conduct a sensitivity analysis excluding high-gap cells.

### Red Flag 2: Acoustic measurement spatial support mismatch
Point-level acoustic measurements (Noise-Planet, SoundingEarth) are punctual observations, but the spatial regression unit is a 500 m grid cell. Aggregating 1–5 point measurements to a 500 m cell assumes spatial stationarity of sound levels within the cell, which is violated near major roads, parks, or construction sites. A single point near a highway will produce a high-SPL cell estimate that is not representative of the entire 500 m area.

**Required mitigation:** Use the UK BN-LOUD raster (for London) and EPA traffic noise model (for NYC, if available) as spatially continuous noise surfaces, then extract zonal statistics (mean, SD) for each cell. For Singapore and where continuous surfaces are unavailable, weight point observations by inverse distance to the cell centroid. Report cell-level standard deviation of SPL as a quality control variable; exclude or flag cells where SPL SD > 10 dB(A) within the cell.

### Red Flag 3: Multicollinearity among OSM covariates
The proposed independent variables — land use entropy, building density, road hierarchy, green view index, A-weighted SPL, soundscape pleasantness, soundscape eventfulness — are likely to be substantially collinear in urban environments. Dense commercial areas will simultaneously have high SPL, low green view index, high building density, and low pleasantness. Multicollinearity inflates GWR local coefficient variance, producing unstable and uninterpretable coefficient maps.

**Required mitigation:** Before GWR, compute a variance inflation factor (VIF) matrix for all covariates using OLS. Remove or combine any variable with VIF > 10. For the acoustic variables specifically, pleasantness and eventfulness are derived from the same acoustic signal and may be collinear with A-weighted SPL — test their pairwise Pearson correlations and consider using only one ISO 12913 dimension (pleasantness) plus SPL if correlation exceeds |r| = 0.7. For MGWR, follow the collinearity diagnostic guidance in Fotheringham et al. (2020): report the local condition number distribution and flag cells where the local condition number exceeds 30.

### Red Flag 4: FID is not a per-cell metric
FID requires a distribution of images (recommended minimum 50, typically 1,000+) to produce a stable estimate. At 500 m cell resolution, most cells will have fewer than 50 Mapillary images in any of the three cities. Using FID as the spatial dependent variable at cell level will produce noisy, unstable estimates.

**Required mitigation:** Use SSIM and LPIPS as primary per-cell metrics (both are per-image and can be aggregated reliably from small samples). Reserve FID for city-level and land-use-zone-level analysis (larger spatial aggregations with sufficient image counts). Report FID only at city level (3 values per model configuration) and per land use zone (commercial, residential, industrial, green) within each city.

### Red Flag 5: Edge effects in GWR near city boundaries
GWR uses a spatial kernel that borrows strength from neighboring observations. Near city boundaries, observations at the urban periphery have fewer neighbors on one side, causing the adaptive bandwidth to stretch spatially to reach the required k neighbors, potentially incorporating rural or periurban observations with different acoustic-visual relationships into the local regression.

**Required mitigation:** Define a 1 km inward buffer from the administrative boundary of each city study area. Cells within this buffer zone are retained in the dataset for neighbor calculations but flagged; their GWR coefficient estimates should be treated with caution and marked in the coefficient maps with a hatching pattern. Report the fraction of edge-affected cells and confirm that primary conclusions are not driven by boundary cells.

### Red Flag 6: MGWR convergence on small n
For Singapore (expected n ~ 1,500–2,000), MGWR backfitting may converge slowly or to degenerate solutions where all per-variable bandwidths collapse to the global limit, effectively producing OLS coefficients for all predictors. This occurs when spatial variation is weak relative to model complexity.

**Required mitigation:** Limit the MGWR covariate set for Singapore to the 4–5 most spatially variable predictors (identified by GWR coefficient CV prior to MGWR). Set a minimum bandwidth floor of k = 20 neighbors for all MGWR bandwidths. If MGWR convergence fails or all bandwidths collapse to global, report GWR as the spatially varying model for Singapore and note the limitation explicitly.

---

## geo_benchmark Applicability

**Applicable: Yes**

Recommended geo_benchmark configuration:

```yaml
models:
  - OLS
  - GWR
  - MGWR
dependent_variable: median_lpips_per_cell  # or mean_ssim_per_cell
spatial_weights: KNN_k8_UTM
bandwidth_method: AICc
kernel: adaptive_bisquare
mgwr_max_n: 3000
subsampling: stratified_spatial_hexbin
cities:
  - name: NYC
    epsg: 32618
    max_n_gwr: 5000
    max_n_mgwr: 2500
  - name: London
    epsg: 32630
    max_n_gwr: 5000
    max_n_mgwr: 2500
  - name: Singapore
    epsg: 32648
    max_n_gwr: null   # use all
    max_n_mgwr: null  # use all (expected < 3000)
moran_i_k: 8
report_local_r2_maps: true
report_coefficient_maps: true
report_bandwidth_per_variable: true  # MGWR only
```

Additional baseline to include: `spreg.ML_Error` (PySAL spatial error model) as a fourth comparison if OLS residual Moran's I > 0.15, per geo_benchmark extension protocol.

---

## Summary: Required Actions Before Spatial Analysis Begins

| Priority | Action | Why |
|----------|--------|-----|
| P1 | Confirm per-city cell counts at 500 m resolution | Determines GWR/MGWR feasibility without subsampling |
| P1 | Audit temporal gap between Mapillary imagery and acoustic data per cell | Addresses Red Flag 1 — this is the most serious validity threat |
| P1 | Compute VIF for all covariates in OLS before GWR | Addresses Red Flag 3 multicollinearity |
| P2 | Switch primary DV from FID to median LPIPS per cell | Addresses Red Flag 4 — FID is not a per-cell metric |
| P2 | Replace random CV with spatial block CV (5 folds per city) | Required for valid out-of-sample evaluation |
| P2 | Add GHS-BUILT-H (building height) as covariate | Not in program.md; addresses acoustic canyon modeling |
| P3 | Add 1 km boundary buffer mask | Addresses Red Flag 5 GWR edge effects |
| P3 | Run Moran's I correlogram at 500m–10km lags before regression | Documents spatial dependence range for bandwidth selection |

---

*Geo-Specialist Review produced by geo-specialist agent. References: Fan et al. (IJGIS 2020), Fotheringham et al. (2017, 2020), Shen et al. (TGRS 2022), Oshan et al. (2019), Wei et al. (2025), program.md Section 6–8, memory/gap-analysis.md M3/M4.*
