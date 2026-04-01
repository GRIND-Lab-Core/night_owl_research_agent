# Spatial Methods Knowledge Base — GeoResearchAgent-247

**Domain:** GIScience / Spatial Statistics / Remote Sensing Analysis
**Maintainer:** GeoResearchAgent-247

---

## 1. Spatial Autocorrelation Fundamentals

**Tobler's First Law:** "Everything is related to everything else, but near things are more related than distant things."

Spatial autocorrelation (SA) means observations are not independent — nearby values are more similar than random chance predicts. Ignoring SA in regression models violates OLS assumptions and produces unreliable coefficient estimates and standard errors.

**Global Moran's I:**
- Range: -1 (perfect dispersion) to +1 (perfect clustering); 0 = random
- Compute: `esda.Moran(y, W)` in PySAL
- Report with p-value and z-score
- **Rule:** always report Moran's I for regression residuals in any spatial model paper

**Local Moran's I (LISA):**
- Identifies local clusters (High-High, Low-Low) and outliers (High-Low, Low-High)
- Use `esda.Moran_Local(y, W)` in PySAL
- Visualize with significance map (α = 0.05)

**Geary's C:**
- Alternative to Moran's; more sensitive to local SA
- Range: 0 (perfect clustering) to 2 (perfect dispersion); 1 = random

**Spatial weights matrix construction:**
- Queen contiguity: shares any boundary point → `libpysal.weights.Queen.from_dataframe(gdf)`
- Rook contiguity: shares an edge → `libpysal.weights.Rook.from_dataframe(gdf)`
- K-nearest neighbors (KNN): `libpysal.weights.KNN.from_dataframe(gdf, k=5)` — use for point data
- Distance band: `libpysal.weights.DistanceBand.from_dataframe(gdf, threshold=d)`
- Row-standardize always: `W.transform = 'R'`

---

## 2. Spatial Regression Models

### 2.1 OLS (Baseline — Always Run First)

```python
import statsmodels.api as sm
X = sm.add_constant(X_df)
model = sm.OLS(y, X).fit(cov_type='HC3')  # HC3 = heteroskedasticity-robust SE
print(model.summary())
```

**Diagnostics to run after OLS:**
- Moran's I on residuals: if p < 0.05, spatial model needed
- Breusch-Pagan: heteroskedasticity test
- Jarque-Bera: normality of residuals
- VIF: multicollinearity (threshold: VIF > 10 is problematic)

**Report:** R², Adj-R², RMSE, MAE, AIC, BIC, Moran's I residuals (I, p-value)

### 2.2 Spatial Lag Model

```python
from spreg import ML_Lag
model = ML_Lag(y, X, w=W)
```

Use when: Moran's I significant + theoretical reason for spatial spillover (outcome in one area influenced by outcomes in neighboring areas).

### 2.3 Spatial Error Model

```python
from spreg import ML_Error
model = ML_Error(y, X, w=W)
```

Use when: Moran's I significant + spatial autocorrelation is due to unmeasured confounders with spatial structure (not spillover).

### 2.4 GWR (Geographically Weighted Regression)

```python
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW

coords = list(zip(gdf.geometry.x, gdf.geometry.y))  # must be projected CRS
bw_sel = Sel_BW(coords, y, X, kernel='bisquare', fixed=False)  # adaptive bandwidth
bw = bw_sel.search()
gwr_model = GWR(coords, y, X, bw=bw, kernel='bisquare', fixed=False).fit()
```

**Key outputs:**
- `gwr_model.localR2`: local R² per observation — map this
- `gwr_model.params`: N × (k+1) local coefficient matrix — map each predictor
- `gwr_model.bw`: bandwidth (number of neighbors for adaptive)
- `gwr_model.aicc`: AICc for model comparison

**Computational limits:** O(n²) complexity. Subsample to ≤ 5,000 obs for memory.

**Report:** global R², AICc, bandwidth, % of local R² > 0.5, Moran's I residuals, coefficient maps for key predictors.

### 2.5 MGWR (Multiscale GWR) — Preferred Over GWR

```python
from mgwr.gwr import MGWR
from mgwr.sel_bw import Sel_BW

bw_sel = Sel_BW(coords, y, X, multi=True, kernel='bisquare', fixed=False)
bws = bw_sel.search(multi_bw_min=[2])  # array of per-variable bandwidths
mgwr_model = MGWR(coords, y, X, selector=bw_sel, kernel='bisquare', fixed=False).fit()
```

**Key outputs:**
- `mgwr_model.bws`: array of per-variable bandwidths
- Interpret bandwidth scale: small bw = local (few neighbors), large bw = regional/global
- `mgwr_model.params`: local coefficients (same as GWR but each variable has its own bandwidth)

**Computational limits:** even more intensive than GWR; subsample to ≤ 3,000 obs; limit to ≤ 8 predictors.

**When MGWR > GWR:** when different predictors operate at different spatial scales (e.g., elevation is regional, land use is local).

**Standard phrasing:** "MGWR allows each covariate to have its own bandwidth, capturing multi-scale spatial non-stationarity."

### 2.6 Geographically Weighted Random Forest (GWRF)

```python
# Use spgwr package or manual geographic stratification
# Not yet in mgwr; typically implemented as spatially-weighted bootstrapped RF
```

Emerging method; cite Georganos et al. (2021) for benchmarking.

---

## 3. Interpolation Methods

### 3.1 Kriging (Optimal Spatial Interpolation)

```python
from pykrige.ok import OrdinaryKriging

OK = OrdinaryKriging(x, y, z, variogram_model='spherical', verbose=False, enable_plotting=False)
z_pred, z_var = OK.execute('grid', gridx, gridy)
```

**Variogram models:** spherical (default for most geo data), exponential, gaussian, power, linear
**Always show:** empirical variogram + fitted model before reporting kriging results

**Types:**
- Ordinary Kriging (OK): unknown constant mean — most common
- Universal Kriging (UK): trend + spatial autocorrelation
- Indicator Kriging: for categorical variables
- Co-Kriging: incorporate correlated secondary variable

### 3.2 IDW (Inverse Distance Weighting)

Non-optimal deterministic interpolation; use only when kriging assumptions cannot be met. Always compare with kriging by cross-validation RMSE.

---

## 4. Remote Sensing Analysis

### 4.1 Raster Processing with rasterio

```python
import rasterio
import numpy as np

with rasterio.open('image.tif') as src:
    data = src.read()          # (bands, rows, cols) array
    profile = src.profile      # metadata dict
    transform = src.transform  # affine transform
    crs = src.crs

# Reproject
from rasterio.warp import calculate_default_transform, reproject, Resampling
dst_crs = 'EPSG:32610'  # UTM Zone 10N
transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)
```

### 4.2 Spectral Indices

```python
# NDVI (Normalized Difference Vegetation Index)
ndvi = (nir - red) / (nir + red + 1e-10)

# NDWI (Normalized Difference Water Index — McFeeters)
ndwi = (green - nir) / (green + nir + 1e-10)

# NBR (Normalized Burn Ratio — for fire severity)
nbr = (nir - swir2) / (nir + swir2 + 1e-10)

# BSI (Bare Soil Index)
bsi = ((swir1 + red) - (nir + blue)) / ((swir1 + red) + (nir + blue) + 1e-10)

# NDBI (Normalized Difference Built-up Index)
ndbi = (swir1 - nir) / (swir1 + nir + 1e-10)
```

### 4.3 Change Detection

**Bitemporal differencing:**
```python
change = image_t2 - image_t1  # or index difference
```

**CVA (Change Vector Analysis):**
```python
magnitude = np.sqrt(np.sum((img2 - img1)**2, axis=0))
direction = np.arctan2(img2[0] - img1[0], img2[1] - img1[1])
```

**Deep learning change detection:**
- Siamese network (two encoders sharing weights, difference in latent space)
- Transformer-based: BIT, ChangeFormer
- Foundation model fine-tuning: Prithvi-100M, Clay

### 4.4 SAR Processing

- Sentinel-1 C-band: VV/VH polarization; GRD (ground range detected) product most common
- Coherence: temporal coherence between two SAR acquisitions detects change
- Backscatter change: detect flooding, damage
- Tool: ESA SNAP (desktop) or `pyroSAR` (Python wrapper)

```python
import pyroSAR  # for batch Sentinel-1 preprocessing
# Or use Google Earth Engine / Planetary Computer for cloud-based processing
```

---

## 5. Spatial Cross-Validation

**CRITICAL:** never use random CV for spatial data. Spatial autocorrelation causes data leakage between train/test splits when they are geographically proximate.

**Spatial k-fold CV:**
```python
from sklearn.model_selection import KFold
import geopandas as gpd
# Use geographic blocks (H3 hexagons, admin units, or lat/lon grid cells) as folds

# Using spatial blocks:
from sklearn.model_selection import cross_val_score
# Block CV: assign each sample to a block, use blocks as fold units
```

**Leave-One-Block-Out (LOBO):** use when geographic units (counties, watersheds) exist naturally

**Buffered LOBO:** exclude samples within distance d of test block from training (removes spatial proximity leakage). Recommended by Valavi et al. (2019) `blockCV` (R) / `spatial-blocks` pattern in Python.

**Standard phrasing:** "We used spatial k-fold cross-validation with H3 resolution-5 hexagonal blocks as fold units to prevent data leakage from spatial autocorrelation."

---

## 6. CRS and Projection Reference

| Use case | CRS | EPSG |
|---|---|---|
| Storage, global data | WGS84 geographic | 4326 |
| Web maps | Web Mercator | 3857 |
| CONUS analysis (equal-area) | Albers Equal Area CONUS | 5070 |
| Australia | GDA2020 / Australian Albers | 3577 |
| Global equal-area | Mollweide | 54009 |
| UTM zones (analysis) | UTM (zone-specific) | 32601–32660 (N), 32701–32760 (S) |
| UK | OSGB36 | 27700 |

**Rules:**
1. Never compute distances or areas in WGS84 (degrees are not uniform distance units)
2. Always use equal-area projection for area calculations
3. Always project to local UTM for point-level accuracy
4. Validate CRS before every spatial join: `assert gdf1.crs == gdf2.crs`

```python
import geopandas as gpd
gdf = gpd.read_file('data.geojson')
gdf_proj = gdf.to_crs(epsg=32610)       # reproject
gdf.crs.to_epsg()                        # get EPSG code
```

---

## 7. GeoBenchmark Integration

When a paper involves spatial regression, **always compare OLS / GWR / MGWR** using the GeoBenchmark suite:

```bash
python GeoBenchmark/run_benchmark.py \
    --dataset your_data.csv \
    --target y_column \
    --lat lat_col --lon lon_col \
    --features col1 col2 col3 \
    --models ols gwr mgwr
```

Report in paper:
| Model | R² | AICc | RMSE | Moran's I (residuals) |
|---|---|---|---|---|
| OLS | | | | |
| GWR | | | | |
| MGWR | | | | |

**Standard phrasing:** "We benchmark against OLS and GWR baselines using the GeoBenchmark suite. MGWR provides per-variable bandwidth estimation, allowing detection of multi-scale spatial non-stationarity in predictor effects."

---

## 8. Common Errors and How to Avoid Them

| Error | Correct Practice |
|---|---|
| Distances computed in WGS84 | Always project to metric CRS first |
| Random CV on spatial data | Use spatial block CV |
| Not reporting Moran's I residuals | Always report for any regression model |
| Using Web Mercator (3857) for analysis | Only for web tiles; use UTM or equal-area for analysis |
| MGWR on n > 3000 | Subsample with spatial stratification |
| CRS mismatch in spatial join | Assert equal CRS before join |
| Ignoring MAUP | Discuss scale sensitivity; try multiple resolutions if feasible |
| Reporting OLS only for spatial data | Always include at least one spatial model (spatial lag, GWR, or MGWR) |
