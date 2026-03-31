# GeoBenchmark Datasets

All datasets are automatically downloaded by `download_data.py`.
Run: `python GeoBenchmark/download_data.py`

---

## Dataset Index

### `california_housing/`
- **Source**: 1990 US Census (scikit-learn built-in)
- **N**: 20,640 census blocks
- **Target**: Median house value (`target`, in $100k units)
- **Features**: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
- **CRS**: WGS84 (EPSG:4326)
- **License**: Public domain
- **Citation**: Pace, R. K., & Barry, R. (1997). Sparse spatial autoregressions. Statistics & Probability Letters, 33(3), 291-297.

### `boston_housing/`
- **Source**: Harrison & Rubinfeld (1978), via statsmodels
- **N**: 506 census tracts
- **Target**: Median home value (`target`)
- **Features**: 13 socioeconomic/environmental variables
- **CRS**: WGS84 (approximate coordinates)
- **License**: Public domain
- **Note**: Coordinates are approximations — use for method demonstration only
- **Citation**: Harrison, D., & Rubinfeld, D. L. (1978). Hedonic housing prices and the demand for clean air. Journal of Environmental Economics and Management, 5(1), 81-102.

### `beijing_pm25/`
- **Source**: UCI Machine Learning Repository / synthetic
- **N**: 500–8,760 records
- **Target**: PM2.5 concentration (`target`, μg/m³)
- **Features**: temperature, humidity, wind_speed, pressure, month
- **CRS**: WGS84 (Beijing area)
- **License**: Open (UCI ML Repository)
- **Note**: Spatial coordinates are approximations for demonstration

### `us_county_health/`
- **Source**: County Health Rankings (RWJF) + US Census TIGER centroids
- **N**: 3,142 counties
- **Target**: Composite health outcome index (`target`)
- **Features**: poverty_rate, uninsured_rate, median_income, education, unemployment, air_pollution, etc.
- **CRS**: WGS84 county centroids (US Census 2020)
- **License**: Open (CC BY 4.0)
- **Real data**: https://www.countyhealthrankings.org/explore-health-rankings/rankings-data-documentation
- **Note**: Synthetic values used by default. Replace with real CHR data for research.

---

## Adding New Datasets

1. Create a folder: `GeoBenchmark/datasets/your_dataset/`
2. Add a CSV with `lat`, `lon`, `target` columns and feature columns
3. Add a `metadata.json`:
```json
{
  "name": "your_dataset",
  "n": 1000,
  "target": "target",
  "features": ["feature1", "feature2"],
  "lat_col": "lat",
  "lon_col": "lon",
  "crs": "EPSG:4326",
  "source": "Description of data source",
  "citation": "Full citation"
}
```
4. Add a download function to `download_data.py`

---

## Recommended External Datasets for GWR/MGWR Research

| Dataset | N | Variables | Source | Use Case |
|---------|---|-----------|--------|----------|
| Lucas County (OH) housing | ~25K | Price + socioeconomic | Various | Classic GWR demo |
| Georgia counties | 159 | Education, income, voting | GWmodel R package | MGWR tutorial |
| Dublin voter turnout | 322 | Socioeconomic | mgwr Python examples | GWR validation |
| Tokyo commuter flows | 49 | OD + attributes | Published GWR papers | Transport GWR |
