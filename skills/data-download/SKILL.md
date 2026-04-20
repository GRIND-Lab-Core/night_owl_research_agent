---
name: data-download
description: 'Discover, evaluate, and download publicly available datasets from the internet. Infers data needs from a research question or task, selects authoritative sources, downloads reproducibly, validates file integrity, and documents provenance. Pauses for user input when authentication, API keys, or major tradeoffs require a decision. Use when user says "download data", "get data", "find a dataset", "I need boundary files", "download census data", or needs any external dataset for analysis.'
argument-hint: [data-need-or-research-question]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
---

# Data Download: Discover, Evaluate, and Acquire Research Data

Find and download data for: **$ARGUMENTS**

## Overview

This skill turns a data need into a validated, documented, locally available dataset. It does NOT blindly download from the first URL found. It reasons from the research question to the right data, evaluates candidate sources, downloads reproducibly, validates the result, and records provenance.

The workflow is always: **data need → source discovery → source evaluation → download → validation → provenance documentation**.

## Constants

- **DATA_DIR = `data/`** — Top-level data directory. Raw downloads go to `data/raw/`, processed outputs to `data/processed/`.
- **MANIFEST_FILE = `data/DATA_MANIFEST.md`** — Provenance log for all downloaded datasets.
- **MAX_UNATTENDED_SIZE_MB = 500** — If a single file exceeds this size, pause and confirm with the user before downloading.
- **VERIFY_AFTER_DOWNLOAD = true** — Always validate downloaded files (existence, size, format, openability).
- **PREFER_PUBLIC = true** — When both public and authenticated sources exist, prefer the public source unless the authenticated source is materially better.

> Override via argument, e.g., `/data-download "US census tracts" — data dir: datasets/, max size: 2000`.

---

## Phase 0: Understand the Data Need

Before searching for data, classify what is actually needed.

### Step 0.1: Infer Data Requirements

Extract from the user's request, the research question, or existing project files (`research_contract.md`, `output/EXPERIMENT_PLAN.md`, `RESEARCH_PLAN.md`):

| Dimension | Question to answer |
|---|---|
| **Geography** | What study area? Country, state, city, bounding box, global? |
| **Time range** | What period? Single year, multi-year, historical, real-time? |
| **Spatial resolution** | Point, tract, county, grid cell, pixel? What resolution? |
| **Temporal resolution** | Daily, monthly, annual, static snapshot? |
| **Variables / bands** | What specific attributes, indicators, or spectral bands? |
| **Data type** | Vector (points, lines, polygons), raster, tabular, network? |
| **File format** | GeoJSON, Shapefile, GeoPackage, GeoParquet, GeoTIFF, COG, NetCDF, CSV? |
| **Licensing** | Must it be open? CC-BY? Public domain? Commercial use? |
| **Quality** | Research-grade? Official statistics? Authoritative boundaries? |
| **Size** | How many features/pixels/rows? Will it fit in memory? |

If the request is too vague (e.g., "get me some data"), STOP and ask the user to specify at least:
- What geographic area?
- What variables or themes?
- What time period?

### Step 0.2: Categorize the Data Need

Map the need to one or more data categories:

| Category | Examples | Typical sources |
|---|---|---|
| **Administrative boundaries** | Country, state, county, tract, district | Census/TIGER, GADM, Natural Earth, OSM |
| **Transportation / infrastructure** | Roads, railways, airports, utilities | OSM, DOT, OpenStreetMap Overpass |
| **Elevation / terrain** | DEM, slope, aspect, hillshade | USGS 3DEP, SRTM, Copernicus DEM, ALOS |
| **Land cover / land use** | NLCD, ESA WorldCover, MODIS LC | MRLC, ESA, USGS, Google Dynamic World |
| **Environmental / climate** | Temperature, precipitation, drought, soil | PRISM, ERA5, NOAA, WorldClim, SoilGrids |
| **Weather** | Observations, forecasts, station data | NOAA ISD/GHCN, Open-Meteo, ERA5 |
| **Air quality** | PM2.5, ozone, AQI | EPA AQS, OpenAQ, Copernicus CAMS |
| **Hydrology** | Rivers, watersheds, streamflow, flood zones | NHD, USGS NWIS, HydroSHEDS, FEMA NFHL |
| **Disaster / hazard** | Hurricane tracks, wildfire, earthquake, flood | NOAA IBTrACS, NIFC, USGS Earthquake, FEMA |
| **Census / socioeconomic** | Population, income, housing, education | US Census/ACS, WorldPop, IPUMS, Eurostat |
| **Public health** | Disease rates, hospital locations, SVI | CDC, HHS, EPA EJScreen, County Health Rankings |
| **Remote sensing imagery** | Landsat, Sentinel, MODIS, VIIRS | USGS EarthExplorer, Copernicus Open Access, NASA LAADS |
| **Points of interest** | Schools, hospitals, parks, businesses | OSM, HIFLD, local open data portals |
| **Vegetation / agriculture** | NDVI, crop type, cropland extent | MODIS, Sentinel-2, USDA CDL |
| **Ocean / coastal** | Bathymetry, sea surface temp, shorelines | NOAA NCEI, GEBCO, Copernicus Marine |

Write the data requirement summary to `data/DOWNLOAD_PLAN.md`:

```markdown
# Data Download Plan

**Task**: [user's request or research question]
**Date**: [today]

## Required Datasets

### Dataset 1: [descriptive name]
- Category: [from table above]
- Geography: [study area]
- Time range: [period]
- Spatial resolution: [resolution]
- Variables: [list]
- Format preference: [format]
- Priority: REQUIRED / NICE-TO-HAVE

### Dataset 2: [descriptive name]
...

## Constraints
- Licensing: [requirement]
- Size budget: [limit]
- Authentication: [any known requirements]
```

---

## Phase 1: Discover Data Sources

### Step 1.1: Source Search Strategy

For each required dataset, search for sources in this priority order:

1. **Official government portals** — Census.gov, data.gov, USGS, NOAA, EPA, Eurostat, national mapping agencies
2. **Intergovernmental organizations** — UN, World Bank, WHO, FAO, OECD
3. **Well-known research repositories** — NASA Earthdata, Copernicus, PANGAEA, Zenodo, Figshare, Dryad
4. **Established open data projects** — OpenStreetMap, Natural Earth, GADM, WorldPop, WorldClim
5. **Cloud-hosted public data** — AWS Open Data, Google Earth Engine, Microsoft Planetary Computer, Source Cooperative
6. **Official APIs** — Census API, NOAA API, EPA API, Open-Meteo, Overpass API
7. **Academic project pages** — with clear documentation, DOI, and citation

**NEVER use as primary source:**
- Random blog posts or personal websites
- Undocumented file-sharing links
- Preview/visualization tiles meant for display only (e.g., map tile servers are NOT data downloads)
- Scraped HTML tables when a documented API or download endpoint exists
- Sources without clear provenance or licensing

### Step 1.2: Source Catalog

For each candidate source, record:

```markdown
### Source: [name]
- URL: [download page or API endpoint]
- Provider: [organization]
- Format: [file format(s) available]
- Coverage: [geographic and temporal]
- Resolution: [spatial and temporal]
- License: [license type]
- Access: PUBLIC / API_KEY / LOGIN / INSTITUTIONAL / PAID
- Documentation: [link to docs/metadata]
- Last updated: [date or frequency]
- Stability: HIGH (government/institution) / MEDIUM (research project) / LOW (personal)
- Citation: [how to cite]
```

---

## Phase 2: Evaluate and Select Sources

### Step 2.1: Evaluation Criteria

Score each candidate source:

| Criterion | Weight | What to check |
|---|---|---|
| **Authority** | HIGH | Is the provider an official or recognized institution? |
| **Coverage match** | HIGH | Does it cover the needed geography, time range, and variables? |
| **Accessibility** | HIGH | Is it publicly downloadable without login? |
| **Format usability** | MEDIUM | Is the format machine-readable and standard? |
| **Documentation quality** | MEDIUM | Are metadata, schema, and methodology documented? |
| **Freshness** | MEDIUM | Is the data current enough for the research need? |
| **Resolution match** | MEDIUM | Does the spatial/temporal resolution match the need? |
| **Stability** | LOW | Will the URL still work in 6 months? |
| **Citability** | LOW | Does it have a DOI, recommended citation, or clear provenance? |

### Step 2.2: Access Classification and Pause Logic

Classify each source by access type and act accordingly:

| Access type | Action |
|---|---|
| **PUBLIC** — direct HTTP download, no auth | Proceed to download |
| **PUBLIC API** — free API, no key required | Proceed to download via API |
| **API_KEY** — free but requires registration for key | **PAUSE**: Tell user they need to register for an API key. Provide the registration URL. Ask if they have a key or want to use an alternative source. |
| **LOGIN** — requires account creation | **PAUSE**: Explain that login is required. Provide registration URL. Ask user how to proceed. |
| **INSTITUTIONAL** — requires university/org credentials | **PAUSE**: Explain institutional access requirement. Suggest public alternatives if available. |
| **PAID** — subscription or per-download cost | **PAUSE**: Explain cost. Strongly recommend free alternatives. Only proceed if user explicitly confirms. |
| **CLICK-THROUGH** — requires manual license agreement | **PAUSE**: Explain that a manual license agreement must be accepted in a browser. Provide the URL for the user to accept and download manually. |
| **CAPTCHA** — automated access blocked | **PAUSE**: Explain that automated download is not possible. Provide the URL for manual download. |

**GUARDRAIL**: Never fabricate, guess, or hardcode API keys, passwords, or tokens. Never attempt to bypass authentication, CAPTCHAs, or access controls. Never assume the user has credentials unless they explicitly provide them.

### Step 2.3: Present Options When Tradeoffs Exist

If multiple sources exist with material tradeoffs, **PAUSE** and present the options:

```
I found multiple sources for [data need]:

1. [Source A] — PUBLIC, 30m resolution, 2021, GeoTIFF
   + No login required, direct download
   - Slightly older, coarser resolution

2. [Source B] — API_KEY required, 10m resolution, 2023, COG
   + Higher resolution, more recent
   - Requires free API key registration at [URL]

3. [Source C] — INSTITUTIONAL, 1m resolution, 2024
   + Best resolution and most current
   - Requires university login

Which source should I use? Or should I proceed with Source A (public, no login)?
```

Let the user decide. If no response and the public source is adequate, default to the public source.

### Step 2.4: Size Check

Before downloading, estimate the file size if possible (from documentation, HTTP HEAD request, or API metadata).

If estimated size > MAX_UNATTENDED_SIZE_MB:
```
The download for [dataset] is approximately [X] MB.
This exceeds the [MAX_UNATTENDED_SIZE_MB] MB threshold.

Should I proceed? Options:
1. Download the full file ([X] MB)
2. Download a spatial subset (specify bounding box or region)
3. Skip this dataset for now
```

---

## Phase 3: Download

### Step 3.1: Directory Setup

```python
from pathlib import Path

data_dir = Path('data')
raw_dir = data_dir / 'raw'
processed_dir = data_dir / 'processed'
raw_dir.mkdir(parents=True, exist_ok=True)
processed_dir.mkdir(parents=True, exist_ok=True)
```

Organize raw downloads into subdirectories by dataset name:
```
data/
├── raw/
│   ├── census_tracts_2020/
│   │   ├── tl_2020_us_tract.shp
│   │   ├── tl_2020_us_tract.dbf
│   │   └── ...
│   ├── nlcd_2021/
│   │   └── nlcd_2021_land_cover.tif
│   └── noaa_hurricanes/
│       └── ibtracs_NA.csv
├── processed/
│   └── [user creates these later]
└── DATA_MANIFEST.md
```

### Step 3.2: Download Methods

Choose the download method based on the source type:

#### Method A: Direct HTTP Download (preferred for single files)

```python
import requests
from pathlib import Path

def download_file(url, dest_path, chunk_size=8192):
    """Download a file with progress tracking and integrity check."""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    total = int(response.headers.get('content-length', 0))
    downloaded = 0

    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            downloaded += len(chunk)

    file_size = dest_path.stat().st_size
    if total > 0 and file_size != total:
        raise ValueError(f"Size mismatch: expected {total}, got {file_size}")

    print(f"Downloaded {dest_path.name} ({file_size / 1e6:.1f} MB)")
    return dest_path
```

For very large files or when `requests` is slow, use `curl` or `wget`:

```bash
curl -L -o data/raw/dataset/file.zip "https://example.gov/data/file.zip"
# or
wget -O data/raw/dataset/file.zip "https://example.gov/data/file.zip"
```

#### Method B: API Download (when structured query is needed)

```python
import requests
import json

# Example: Census API
params = {
    'get': 'B01001_001E,NAME',
    'for': 'tract:*',
    'in': 'state:06',
    'key': API_KEY  # only if user provided it
}
response = requests.get('https://api.census.gov/data/2021/acs/acs5', params=params)
data = response.json()
```

```python
# Example: Open-Meteo (free, no key)
params = {
    'latitude': 40.7128,
    'longitude': -74.0060,
    'daily': 'temperature_2m_max,precipitation_sum',
    'start_date': '2020-01-01',
    'end_date': '2023-12-31',
    'timezone': 'America/New_York'
}
response = requests.get('https://api.open-meteo.com/v1/forecast', params=params)
weather = response.json()
```

#### Method C: Direct Read (when library handles download internally)

```python
import geopandas as gpd

# GeoJSON from URL
gdf = gpd.read_file('https://raw.githubusercontent.com/.../boundaries.geojson')

# Shapefile from zip URL
gdf = gpd.read_file('https://example.gov/data/tracts.zip')
```

```python
import pandas as pd

# CSV from URL
df = pd.read_csv('https://example.gov/data/indicators.csv')
```

```python
import xarray as xr

# NetCDF / Zarr from cloud
ds = xr.open_dataset('https://example.org/data/climate.nc')
# or from Zarr store
ds = xr.open_zarr('s3://bucket/dataset.zarr')
```

#### Method D: Archive Extraction

```python
import zipfile
import tarfile
from pathlib import Path

def extract_archive(archive_path, dest_dir):
    """Extract zip or tar archive."""
    archive_path = Path(archive_path)
    dest_dir = Path(dest_dir)

    if archive_path.suffix == '.zip':
        with zipfile.ZipFile(archive_path, 'r') as z:
            z.extractall(dest_dir)
    elif archive_path.suffix in ('.tar', '.gz', '.tgz', '.bz2'):
        with tarfile.open(archive_path, 'r:*') as t:
            t.extractall(dest_dir)
    else:
        raise ValueError(f"Unknown archive format: {archive_path.suffix}")

    print(f"Extracted to {dest_dir}")
    # Optionally remove the archive after extraction
    # archive_path.unlink()
```

#### Method E: STAC / Cloud-Optimized Access (for remote sensing)

```python
from pystac_client import Client

# Search a STAC catalog
catalog = Client.open('https://planetarycomputer.microsoft.com/api/stac/v1')
search = catalog.search(
    collections=['sentinel-2-l2a'],
    bbox=[-122.5, 37.5, -122.0, 38.0],
    datetime='2023-01-01/2023-12-31',
    query={'eo:cloud_cover': {'lt': 20}}
)
items = list(search.items())
print(f"Found {len(items)} scenes")
```

```python
import rioxarray

# Read a Cloud-Optimized GeoTIFF with spatial subset
ds = rioxarray.open_rasterio(
    'https://example.org/data/dem.tif',
    overview_level=2  # use overview for quick preview
)
# Clip to area of interest
ds_clipped = ds.rio.clip_box(minx=-122.5, miny=37.5, maxx=-122.0, maxy=38.0)
```

#### Method F: OpenStreetMap via Overpass API

```python
import requests

# Query Overpass API for specific features
overpass_query = """
[out:json][timeout:60];
area["ISO3166-1"="US"]["admin_level"="2"]->.searchArea;
(
  node["amenity"="hospital"](area.searchArea);
  way["amenity"="hospital"](area.searchArea);
);
out center;
"""
response = requests.get(
    'https://overpass-api.de/api/interpreter',
    params={'data': overpass_query}
)
data = response.json()
```

Or use `osmnx` for network data:
```python
import osmnx as ox
G = ox.graph_from_place("Manhattan, New York", network_type='drive')
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
```

### Step 3.3: Rate Limiting and Courtesy

- **APIs**: Respect rate limits. Add `time.sleep(1)` between sequential API calls unless documentation allows faster.
- **Bulk downloads**: Use a 1-second delay between sequential file downloads from the same server.
- **Large files**: Use chunked download (Method A) instead of loading the entire response into memory.
- **Retries**: Retry failed downloads up to 2 times with exponential backoff. If still failing, report the error and stop.

```python
import time

def download_with_retry(url, dest_path, max_retries=2):
    for attempt in range(max_retries + 1):
        try:
            return download_file(url, dest_path)
        except Exception as e:
            if attempt < max_retries:
                wait = 2 ** attempt
                print(f"Retry {attempt + 1}/{max_retries} in {wait}s: {e}")
                time.sleep(wait)
            else:
                raise RuntimeError(f"Download failed after {max_retries + 1} attempts: {e}")
```

---

## Phase 3.5: Human Checkpoint — Data Synthesis

Honor the `HUMAN_CHECKPOINT` flag in `CLAUDE.md` (default: `true`). This skill *downloads* — it does not generate data — but a few code paths still create derived or synthetic artifacts. When `HUMAN_CHECKPOINT` is `true`, **PAUSE** and request explicit user approval before any of the following; when `false`, log the decision to `output/PROJ_NOTES.md` and proceed.

| Trigger | Show before pausing |
|---|---|
| The requested dataset does not exist in any authoritative source and you are about to construct a substitute by combining other sources (e.g., synthesizing a "population × land cover" raster from two unaligned products) | Component sources, alignment / resampling / reprojection recipe, target schema, and the analytical risk if the synthesis is later treated as primary data |
| You are about to generate a *simulated* dataset (random points, synthetic boundaries, climate scenario realizations, demonstration data) for an experiment | Generator (function + parameters + seed), N, spatial extent, intended use, and explicit confirmation that it will be tagged `synthetic: true` in the manifest |
| You are about to call a parametric API (Open-Meteo, Census ACS, Overpass) with parameters you inferred — not parameters the user gave — that materially shape the result (bbox larger than asked, time range padded, variable list expanded) | Inferred vs requested parameters side-by-side and how they change the resulting dataset |
| You are about to spatially subset, temporally aggregate, or otherwise transform a raw download before placing it in `data/raw/` | The transform, why it is being done before raw storage (default: it shouldn't be — raw must stay raw) |
| A download failed and you are about to substitute an alternative source whose schema differs (different variable names, units, resolution) | Original vs substitute schema diff, unit / projection conversions implied, and downstream claims that depend on field equivalence |

Synthetic and substitute datasets must be recorded in `data/DATA_MANIFEST.md` with `Source: SYNTHESIZED` (or `SUBSTITUTED`), the recipe, and a `Synthesis approved by user: YYYY-MM-DD` line. Do not list a synthesized dataset under the same heading as authoritative downloads.

---

## Phase 4: Validate Downloads

**Every download must be validated.** Never assume a download succeeded just because no exception was raised.

### Step 4.1: Basic File Checks

```python
from pathlib import Path

def validate_download(file_path, min_size_bytes=100):
    """Basic validation: file exists and is not empty/corrupt."""
    p = Path(file_path)
    assert p.exists(), f"File not found: {p}"
    size = p.stat().st_size
    assert size > min_size_bytes, f"File too small ({size} bytes): {p}"
    print(f"OK: {p.name} ({size / 1e6:.2f} MB)")
    return True
```

### Step 4.2: Format-Specific Validation

| Format | Validation | Tool |
|---|---|---|
| **CSV / TSV** | Read header, check row count, check expected columns | `pd.read_csv(path, nrows=5)` |
| **GeoJSON / Shapefile / GeoPackage** | Read, check CRS, check feature count, check geometry types | `gpd.read_file(path, rows=5)` |
| **GeoTIFF / COG** | Check bands, CRS, bounds, nodata | `rasterio.open(path)` |
| **NetCDF / HDF** | Check variables, dimensions, time range | `xr.open_dataset(path)` |
| **ZIP archive** | Test archive integrity, list contents | `zipfile.ZipFile(path).testzip()` |
| **Parquet / GeoParquet** | Read schema, check row count | `gpd.read_parquet(path)` or `pd.read_parquet(path, nrows=5)` |

```python
import geopandas as gpd

def validate_vector(file_path):
    """Validate a vector geospatial file."""
    gdf = gpd.read_file(file_path, rows=10)
    print(f"  Features: {len(gpd.read_file(file_path))}")
    print(f"  CRS: {gdf.crs}")
    print(f"  Geometry types: {gdf.geom_type.unique()}")
    print(f"  Columns: {list(gdf.columns)}")
    print(f"  Bounds: {gdf.total_bounds}")
    return gdf
```

```python
import rasterio

def validate_raster(file_path):
    """Validate a raster file."""
    with rasterio.open(file_path) as src:
        print(f"  Bands: {src.count}")
        print(f"  Size: {src.width} x {src.height}")
        print(f"  CRS: {src.crs}")
        print(f"  Bounds: {src.bounds}")
        print(f"  Nodata: {src.nodata}")
        print(f"  Dtype: {src.dtypes}")
    return True
```

### Step 4.3: Content Sanity Checks

After format validation, check content against the download plan:

- [ ] **Geographic coverage**: Does the bounding box roughly match the requested study area?
- [ ] **Temporal coverage**: Does the time range match what was requested?
- [ ] **Expected variables**: Are the expected columns, bands, or layers present?
- [ ] **Row / feature count**: Is the count in a plausible range?
- [ ] **CRS present**: Is a coordinate reference system defined (for spatial data)?
- [ ] **No obvious corruption**: No all-null columns, no zero-byte layers, no garbled text.

If any check fails, report the problem and suggest whether to re-download, try an alternative source, or ask the user.

---

## Phase 5: Document Provenance

### Step 5.1: Update the Data Manifest

Append an entry to `data/DATA_MANIFEST.md` for every downloaded dataset:

```markdown
## [Dataset Name]

| Field | Value |
|---|---|
| **Source** | [organization / portal name] |
| **URL** | [exact download URL or API endpoint] |
| **Access date** | [YYYY-MM-DD] |
| **License** | [license name or "see URL"] |
| **Citation** | [recommended citation, if available] |
| **Geographic coverage** | [description or bounding box] |
| **Temporal coverage** | [time range or "static"] |
| **Spatial resolution** | [resolution] |
| **Format** | [file format] |
| **Local path** | `data/raw/[folder]/[filename]` |
| **File size** | [size in MB] |
| **Variables** | [key columns / bands / layers] |
| **CRS** | [EPSG code] |
| **Notes** | [any caveats, processing notes, or known issues] |
```

### Step 5.2: Create/Update Manifest Header

If `data/DATA_MANIFEST.md` does not exist, create it with:

```markdown
# Data Manifest

All datasets used in this project. Each entry records provenance, access date, and local path.

**Raw data**: `data/raw/` — original downloaded files, never modified.
**Processed data**: `data/processed/` — cleaned, reprojected, or subsetted versions.

---
```

### Step 5.3: Per-Dataset Metadata (optional)

For datasets downloaded via API or with complex provenance, write a `metadata.json` in the dataset subdirectory:

```json
{
  "name": "us_census_tracts_2020",
  "source": "US Census Bureau TIGER/Line",
  "url": "https://www2.census.gov/geo/tiger/TIGER2020/TRACT/",
  "access_date": "2026-04-10",
  "license": "Public Domain",
  "geographic_coverage": "United States",
  "temporal_coverage": "2020",
  "crs": "EPSG:4269",
  "format": "Shapefile",
  "files": ["tl_2020_06_tract.shp", "tl_2020_06_tract.dbf", "tl_2020_06_tract.shx", "tl_2020_06_tract.prj"],
  "notes": "California tracts only (FIPS 06)"
}
```

---

## Source Reference: Common Data Sources by Category

This section provides starting points. Always verify URLs are current before downloading — government portals reorganize periodically.

### Administrative Boundaries

| Source | Coverage | Format | Access |
|---|---|---|---|
| US Census TIGER/Line | US (all levels) | Shapefile, GeoJSON | PUBLIC |
| GADM | Global (admin 0-5) | GeoPackage, Shapefile, GeoJSON | PUBLIC |
| Natural Earth | Global (simplified) | Shapefile, GeoJSON | PUBLIC |
| Eurostat GISCO | Europe | GeoJSON, Shapefile, TopoJSON | PUBLIC |
| OSM (via Overpass or Geofabrik) | Global | PBF, Shapefile, GeoJSON | PUBLIC |

### Elevation / Terrain

| Source | Resolution | Coverage | Access |
|---|---|---|---|
| USGS 3DEP | 1m–10m | US | PUBLIC |
| SRTM (NASA) | 30m, 90m | 60°N–56°S | PUBLIC (Earthdata login for 30m) |
| Copernicus DEM (GLO-30) | 30m | Global | PUBLIC |
| ALOS World 3D | 30m | Global | PUBLIC (JAXA registration) |

### Land Cover

| Source | Resolution | Coverage | Access |
|---|---|---|---|
| NLCD (MRLC) | 30m | US | PUBLIC |
| ESA WorldCover | 10m | Global | PUBLIC |
| MODIS MCD12Q1 | 500m | Global | PUBLIC |
| Google Dynamic World | 10m | Global | PUBLIC (Earth Engine) |
| USDA Cropland Data Layer | 30m | US | PUBLIC |

### Environmental / Climate

| Source | Type | Resolution | Access |
|---|---|---|---|
| PRISM Climate Group | Temp, precip, etc. | 4km | PUBLIC |
| WorldClim | Climate normals | ~1km | PUBLIC |
| ERA5 (Copernicus CDS) | Reanalysis | 0.25° | API_KEY (free registration) |
| NOAA Climate Normals | Station observations | Point | PUBLIC |
| MODIS LST | Land surface temperature | 1km | PUBLIC |
| SoilGrids (ISRIC) | Soil properties | 250m | PUBLIC |
| Open-Meteo | Weather/climate | ~1-11km | PUBLIC API (no key) |

### Disaster / Hazard

| Source | Type | Access |
|---|---|---|
| NOAA IBTrACS | Hurricane/cyclone tracks | PUBLIC |
| USGS Earthquake Catalog | Earthquake events | PUBLIC API |
| NIFC / GeoMAC / MTBS | Wildfire perimeters | PUBLIC |
| FEMA NFHL | Flood hazard zones | PUBLIC |
| FEMA Disaster Declarations | Disaster events | PUBLIC API |
| NOAA Storm Events | Severe weather reports | PUBLIC |
| NASA FIRMS | Active fire detections | PUBLIC |
| Copernicus EMS | Emergency mapping products | PUBLIC |

### Census / Socioeconomic

| Source | Coverage | Access |
|---|---|---|
| US Census / ACS (API) | US (tract, county, state) | PUBLIC API (key recommended) |
| US Census TIGER (geometry) | US boundaries | PUBLIC |
| IPUMS | US + international microdata | LOGIN (free registration) |
| WorldPop | Global population grids | PUBLIC |
| County Health Rankings | US counties | PUBLIC |
| CDC PLACES | US health indicators | PUBLIC |
| EPA EJScreen | Environmental justice indicators | PUBLIC |

### Remote Sensing

| Source | Platform | Access |
|---|---|---|
| USGS EarthExplorer | Landsat, NAIP, DEMs | LOGIN (free) |
| Copernicus Open Access Hub | Sentinel-1/2/3/5P | LOGIN (free) → migrating to Copernicus Data Space |
| NASA Earthdata | MODIS, VIIRS, ICESat, etc. | LOGIN (free) |
| Microsoft Planetary Computer | Sentinel, Landsat, DEM, more | PUBLIC (STAC API) |
| Google Earth Engine | Multi-source archive | LOGIN (free for research) |
| AWS Open Data (USGS/Sentinel) | Landsat, Sentinel COGs | PUBLIC (S3) |

---

## Guardrails: Common Mistakes This Skill Prevents

| Mistake | How this skill prevents it |
|---|---|
| Downloading from untrusted random sites | Phase 1 Step 1.1 enforces source priority order |
| Attempting to bypass login/authentication | Phase 2 Step 2.2 forces a PAUSE for any non-public source |
| Hardcoding API keys into scripts | Phase 2 guardrail: never embed credentials in code |
| Downloading a 50 GB global file when 200 MB regional subset suffices | Phase 2 Step 2.4 enforces size check and subset suggestion |
| Mixing raw and processed data | Phase 3 Step 3.1 enforces `raw/` vs `processed/` separation |
| Failing to record where data came from | Phase 5 requires manifest entry for every download |
| Not checking if downloaded files are valid | Phase 4 validates every download |
| Confusing map tiles with downloadable data | Phase 1 Step 1.1 explicitly warns against this |
| Downloading outdated versions when newer exist | Phase 2 Step 2.1 checks freshness |
| Scraping fragile HTML when a documented API exists | Phase 1 Step 1.1 prefers documented endpoints |
| Proceeding when user must choose among tradeoffs | Phase 2 Step 2.3 forces a PAUSE with options |
| Ignoring licensing | Phase 2 evaluation records license for every source |
| Downloading without checking CRS | Phase 4 Step 4.2 validates CRS for spatial data |

---

## Outputs

- `data/raw/[dataset_name]/` — Raw downloaded files, never modified
- `data/processed/` — User-created processed versions (this skill does not write here)
- `data/DATA_MANIFEST.md` — Provenance log for all downloaded datasets
- `data/DOWNLOAD_PLAN.md` — Requirements and source evaluation (if complex multi-dataset download)
- `data/raw/[dataset_name]/metadata.json` — Per-dataset metadata (for API or complex downloads)

---

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- **Data need first.** Never download before understanding what is needed and why.
- **Authoritative sources first.** Government and institutional sources beat random websites.
- **PAUSE for authentication.** If login, API key, payment, CAPTCHA, or click-through is required, stop and ask the user. Never fabricate credentials or bypass access controls.
- **PAUSE for major tradeoffs.** If multiple sources exist with material differences in resolution, coverage, access, or size, present options and let the user decide.
- **PAUSE for large files.** If a single file exceeds MAX_UNATTENDED_SIZE_MB, confirm before downloading.
- **Validate every download.** Check existence, size, format readability, CRS, and content plausibility.
- **Document everything.** Every downloaded dataset gets a manifest entry with source URL, access date, license, and local path.
- **Preserve raw data.** Never overwrite raw downloads. Keep originals in `data/raw/`, create processed versions in `data/processed/`.
- **Prefer subsets over full archives.** If only California is needed, do not download all 50 states.
- **Respect rate limits.** Add delays between sequential API calls and bulk downloads.
- **Do not fabricate data.** If a download fails, report the failure — do not create synthetic substitutes without telling the user.
- **Do not scrape when APIs exist.** Prefer structured download endpoints over HTML parsing.
- **No secrets in code.** Never write API keys, tokens, or passwords into scripts, notebooks, or committed files. Use environment variables or prompt the user.

## Composing with Other Skills

This skill provides data for the rest of the research pipeline:

```
/data-download "what data is needed"   ← you are here
/spatial-analysis "research question"  → analyze the downloaded data
/lit-review                            → literature context (separate concern)
/paper-write                           → document data sources in Methodology
/paper-figure                          → visualize the downloaded data
/submit-check                          → verify data citations and DOIs
```

**Integration points:**
- **To spatial-analysis**: Downloaded data lands in `data/raw/`. The `spatial-analysis` skill reads from there (or from paths the user specifies).
- **To deploy-experiment**: This skill handles all external data — custom study area data, external covariates, boundary files, remote sensing imagery.
- **To paper-write / submit-check**: The `DATA_MANIFEST.md` provides source URLs, citations, and access dates for the Methodology section and submission checklist.
- **Knowledge base**: Read `skills/knowledge/spatial-methods.md` for CRS guidance when downloading spatial data.
