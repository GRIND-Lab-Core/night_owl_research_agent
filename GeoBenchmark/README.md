# GeoBenchmark — Geospatial Regression Benchmark Suite

A reproducible benchmark for comparing spatial regression models on open-source datasets.
Includes OLS, GWR, MGWR, Kriging, and spatial machine learning baselines.

---

## Quick Start

```bash
# 1. Download all datasets (first run only, ~200MB total)
python GeoBenchmark/download_data.py

# 2. Run all baselines on all datasets
python GeoBenchmark/run_benchmark.py --all

# 3. Run specific combination
python GeoBenchmark/run_benchmark.py --dataset california_housing --models ols,gwr,mgwr

# 4. Open interactive notebook
jupyter notebook GeoBenchmark/notebooks/benchmark_demo.ipynb
```

---

## Included Datasets

| Dataset | N | Features | Spatial Unit | Task | Source |
|---------|---|---------|--------------|------|--------|
| California Housing (1990) | 20,640 | 8 + lon/lat | Census blocks | Median home value | scikit-learn |
| Boston Housing (Harrison 1978) | 506 | 13 + lon/lat | Census tracts | Median home value | UCI/scikit-learn |
| London House Prices | 1,000+ | 12 + lon/lat | Transactions | Sale price (log) | UK Land Registry (open) |
| Beijing PM2.5 | 8,760 | 11 + lon/lat | Hourly station | PM2.5 concentration | UCI |
| US County Health Rankings | 3,142 | 40+ + lon/lat | County | Health outcome index | RWJF (open) |

### Dataset Details

#### California Housing
- **Source**: 1990 US Census, distributed via `sklearn.datasets`
- **CRS**: WGS84 (lon/lat in degrees)
- **Target**: `MedHouseVal` (median house value, $100k units)
- **Features**: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
- **Notes**: Classic benchmark for spatial heterogeneity studies

#### US County Health Rankings
- **Source**: Robert Wood Johnson Foundation (open access)
- **URL**: https://www.countyhealthrankings.org/explore-health-rankings/rankings-data-documentation
- **CRS**: WGS84 county centroids
- **Target**: Premature death rate, various health outcomes
- **Features**: social determinants, clinical care, health behaviors
- **Notes**: Strong spatial structure due to regional health disparities

---

## Baseline Models

### OLS — Ordinary Least Squares
- **Library**: `statsmodels`
- **Assumptions**: linearity, homoskedasticity, no spatial autocorrelation
- **Evaluation**: R², RMSE, AIC, Moran's I on residuals
- **File**: `baselines/ols_baseline.py`

### GWR — Geographically Weighted Regression
- **Library**: `mgwr` (Multiscale GWR library)
- **Kernel**: Adaptive bi-square
- **Bandwidth selection**: AICc minimization
- **Assumptions**: Local stationarity, normally distributed errors
- **File**: `baselines/gwr_baseline.py`

### MGWR — Multiscale Geographically Weighted Regression
- **Library**: `mgwr`
- **Key advantage over GWR**: Each predictor has its own bandwidth (captures different scales of spatial non-stationarity)
- **Bandwidth selection**: AICc minimization per variable
- **File**: `baselines/mgwr_baseline.py`

### Ordinary Kriging
- **Library**: `pykrige`
- **Variogram**: Exponential, Spherical, or Gaussian (auto-selected by CV)
- **File**: `baselines/kriging_baseline.py`

### Spatial Random Forest
- **Library**: `scikit-learn`
- **Enhancement**: + spatial lag features + XY coordinates as features
- **File**: `baselines/rf_spatial.py`

---

## Evaluation Metrics

| Metric | Description | Better |
|--------|-------------|--------|
| R² | Coefficient of determination | Higher |
| RMSE | Root Mean Square Error | Lower |
| MAE | Mean Absolute Error | Lower |
| AIC/AICc | Information criterion (model parsimony) | Lower |
| Moran's I (residuals) | Spatial autocorrelation in residuals | Closer to 0 |
| Local R² | Spatial variation in fit (GWR/MGWR) | Reported as map |

---

## Results Format

All results are saved to `GeoBenchmark/results/` in JSON format:

```json
{
  "dataset": "california_housing",
  "model": "MGWR",
  "timestamp": "2026-03-31T14:30:00",
  "global_metrics": {
    "r2": 0.74,
    "rmse": 0.52,
    "mae": 0.38,
    "aic": 25432.1,
    "morans_i_residuals": 0.03,
    "morans_i_p_value": 0.21
  },
  "local_metrics": {
    "local_r2_mean": 0.79,
    "local_r2_std": 0.12
  },
  "bandwidths": {
    "MedInc": 45,
    "HouseAge": 320,
    "AveRooms": 180
  }
}
```

---

## Adding New Datasets

1. Add a download function to `download_data.py`
2. Create a `datasets/{name}/` folder with `README.md` describing the data
3. Add the dataset to the registry in `run_benchmark.py`
4. Verify CRS and coordinate columns are correctly specified

## Adding New Baselines

1. Create `baselines/{model_name}_baseline.py` following the existing template
2. Implement the `run(dataset_path, config)` function returning a metrics dict
3. Register in `run_benchmark.py`
