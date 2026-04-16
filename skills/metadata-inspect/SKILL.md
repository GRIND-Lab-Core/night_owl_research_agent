---
name: metadata-inspect
description: 'Full geodata inspection and understanding. Given a dataset (file path, URL, or directory), produces a comprehensive metadata report covering format, CRS, schema, spatial extent, quality flags, and suitability assessment for downstream NORA skills. Handles vector (Shapefile, GeoPackage, GeoJSON, KML, GeoParquet), raster (GeoTIFF, COG, NetCDF, HDF5), and tabular (CSV, Parquet, Excel) formats. Automatically detects geographic columns in non-spatial tables, identifies FIPS/GEOID join keys, and flags data quality issues. Use when user says "inspect data", "describe this file", "what is in this dataset", "check data quality", "metadata report", "examine CRS", "what fields does this have", or needs to understand a dataset before running analysis or operations.'
argument-hint: [file-path-url-or-directory]
allowed-tools: Bash(*), Read, Write, Grep, Glob, Agent
---

# Metadata Inspect: Comprehensive Geodata Understanding

Inspect: **$ARGUMENTS**

## Purpose

This skill inspects a dataset and produces a structured metadata report that both humans and downstream NORA skills can consume. It answers: what format is this, what does it contain, what is its spatial reference, what quality issues are present, and is it ready for analysis?

**This skill never modifies the source data.** It is read-only.

Read `skills/knowledge/spatial-methods.md` for CRS reference. Use the geo MCP server (`get_epsg_info`, `suggest_crs`) for CRS interpretation when EPSG codes are unclear.

---

## Constants

- **OUTPUT_DIR = `output/metadata-inspect`** — Default destination for inspection reports.
- **SAMPLE_ROWS = 10** — Number of sample rows to include in previews.
- **MAX_UNIQUE_DISPLAY = 20** — Max unique values to enumerate for categorical fields.
- **NULL_THRESHOLD = 0.10** — Fraction of nulls above which a field is flagged.
- **INVALID_GEOM_THRESHOLD = 0.01** — Fraction of invalid geometries above which a quality warning is raised.
- **LARGE_VECTOR_THRESHOLD = 1_000_000** — Feature count above which metadata-only mode is used.
- **LARGE_RASTER_THRESHOLD_PX = 100_000_000** — Pixel count above which statistics are computed from overviews only.

> Override via argument, e.g., `/metadata-inspect "data/file.gpkg" — sample rows: 20`.

---

## Phase 0: Format Detection and Routing

Before inspecting, determine the data type. Route to the correct inspection track.

### Format Detection Table

| Extension / Pattern | Format Family | Track |
|---|---|---|
| `.shp` (+ `.dbf`, `.shx`, `.prj`) | ESRI Shapefile | Vector |
| `.gpkg` | GeoPackage | Vector (check for raster tiles) |
| `.geojson`, `.json` with geometry key | GeoJSON | Vector |
| `.kml`, `.kmz` | KML/KMZ | Vector |
| `.geoparquet` or `.parquet` with geo metadata | GeoParquet | Vector |
| `.fgb` | FlatGeobuf | Vector |
| `.tif`, `.tiff` | GeoTIFF / COG | Raster |
| `.nc`, `.nc4` | NetCDF | Raster/MultiDim |
| `.hdf`, `.hdf5`, `.h5`, `.he5` | HDF5 | Raster/MultiDim |
| `.img` | ERDAS Imagine | Raster |
| `.jp2` | JPEG 2000 | Raster |
| `.csv`, `.tsv` | Tabular | Tabular |
| `.xlsx`, `.xls` | Excel | Tabular |
| `.parquet` (without geo metadata) | Parquet | Tabular |
| `.txt` | Text (maybe tabular) | Tabular |
| directory | Multiple files | Multi-file scan |
| URL | Remote resource | Fetch → re-route |

**Auto-detection for ambiguous `.parquet`:** Try `geopandas.read_parquet()` first — if it raises (no geometry column), fall back to `pandas.read_parquet()`.

**Shapefile sidecar check:** If `.shp` is given, verify `.dbf`, `.shx`, and `.prj` exist alongside. Flag `MISSING_SIDECAR` if `.prj` is absent (CRS will be unknown).

```python
from pathlib import Path

def detect_format(path_str: str) -> str:
    p = Path(path_str)
    ext = p.suffix.lower()
    VECTOR = {'.shp', '.gpkg', '.geojson', '.json', '.kml', '.kmz', '.geoparquet', '.fgb'}
    RASTER = {'.tif', '.tiff', '.nc', '.nc4', '.hdf', '.hdf5', '.h5', '.he5', '.img', '.jp2'}
    TABULAR = {'.csv', '.tsv', '.xlsx', '.xls', '.txt'}
    if ext in VECTOR: return 'vector'
    elif ext in RASTER: return 'raster'
    elif ext in TABULAR: return 'tabular'
    elif ext == '.parquet': return 'parquet_ambiguous'
    elif p.is_dir(): return 'directory'
    else: return 'unknown'
```

---

## Phase 1: Vector Inspection

Use this track for Shapefile, GeoPackage, GeoJSON, KML, GeoParquet, FlatGeobuf.

**For very large files (> `LARGE_VECTOR_THRESHOLD` features):** Use `fiona` for metadata-only extraction — read CRS, schema, driver, and bounds from the file header without loading all features. Only load `SAMPLE_ROWS` rows for the preview.

```python
import geopandas as gpd
import fiona
import numpy as np

# Large-file-safe metadata extraction
with fiona.open(path) as src:
    driver = src.driver
    crs_wkt = src.crs_wkt
    schema = src.schema
    bounds = src.bounds
    n_features = len(src)

# For preview — sample only
gdf_sample = gpd.read_file(path, rows=SAMPLE_ROWS)

# For small files — full load
gdf = gpd.read_file(path)
```

### 1.1 Properties to Extract

| Property | How to Extract | Notes |
|---|---|---|
| Format / Driver | `fiona.open().driver` or `gdf.attrs` | e.g., "ESRI Shapefile", "GPKG" |
| CRS | `gdf.crs` or `fiona.open().crs_wkt` | See CRS Assessment below |
| Geometry type(s) | `gdf.geom_type.unique()` | May be mixed — flag this |
| Feature count | `len(gdf)` or `len(src)` | |
| Bounding box | `gdf.total_bounds` → [minx, miny, maxx, maxy] | In CRS units |
| Field names & types | `gdf.dtypes` | Pandas dtype per column |
| Null counts per field | `gdf.isnull().sum()` | Compute null fraction |
| Sample values | `gdf.head(SAMPLE_ROWS)` | Display key columns |
| Invalid geometries | `~gdf.geometry.is_valid` | Count + fraction |
| Empty geometries | `gdf.geometry.is_empty` | Count |
| Multipart features | `gdf.geom_type.str.startswith('Multi')` | Count |
| Duplicate geometries | `gdf.geometry.duplicated().sum()` | Count |
| File size | `Path(path).stat().st_size` | In MB |
| Encoding | Try UTF-8, fallback to latin-1 / cp1252 | Flag if non-UTF-8 needed |

### 1.2 CRS Assessment

**CRS is always assessed — no spatial file leaves inspection without a CRS verdict.**

| CRS State | Implication | Action |
|---|---|---|
| Defined, projected (meters) | Analysis-ready for distance/area operations | Report EPSG + name + units |
| Defined, geographic (degrees) | Cannot use for distance/buffer — must reproject | Flag `GEOGRAPHIC_CRS` warning |
| Defined, feet | Unusual — potential for unit confusion | Flag `CRS_UNITS_FEET` info |
| Not defined / None | All spatial operations unreliable | Flag `NO_CRS` critical error |

**CRS recovery attempts when CRS is None:**
1. Check for a `.prj` sidecar file — read its WKT
2. Inspect coordinate range: if all x in [-180, 180] and y in [-90, 90] → likely EPSG:4326
3. Report uncertainty if recovery fails; suggest the user provide the CRS

**Look up CRS details via MCP:** Call `get_epsg_info(epsg_code)` to retrieve the full CRS name, axis units, and geographic scope.

### 1.3 FIPS/GEOID Detection

**Critical rule (from LLM-Geo):** FIPS and GEOID columns may be stored as string with leading zeros **or** as integer without. NEVER read them as float (float destroys leading zeros and adds `.0`).

Detect these patterns automatically:

| Column Name Pattern | Expected Type | Expected Format |
|---|---|---|
| `STATEFP`, `STATE_FIPS`, `state` | str or int | 2-digit (e.g., "06", 6) |
| `COUNTYFP`, `COUNTY_FIPS`, `GEOID` (5-char) | str or int | 5-digit (e.g., "06037") |
| `TRACTCE`, `GEOID` (11-char) | str or int | 11-digit |
| `BLKGRPCE`, `GEOID` (12-char) | str or int | 12-digit |

**Flag `FIPS_AS_FLOAT`** if any of these columns has dtype `float64` — this is a critical data quality issue that will break spatial joins with Census data.

**Flag `FIPS_AS_INT`** (info-level) if stored as int — joining with another table that has them as str with leading zeros will silently fail unless the types are reconciled.

---

## Phase 2: Raster Inspection

Use this track for GeoTIFF, COG, NetCDF, HDF5, JPEG 2000, ERDAS Imagine.

**For large rasters (> `LARGE_RASTER_THRESHOLD_PX` pixels):** Compute statistics from overviews if available (`src.overviews(1)`), not from the full array. Never load the entire raster into memory for metadata.

```python
import rasterio
import numpy as np

with rasterio.open(path) as src:
    meta = src.meta
    profile = src.profile
    bounds = src.bounds
    crs = src.crs
    transform = src.transform
    n_bands = src.count
    dtypes = src.dtypes
    nodata = src.nodata
    overviews = {i: src.overviews(i) for i in src.indexes}
    block_shapes = src.block_shapes
    
    # Sample statistics from first 1000x1000 window (memory-safe)
    window = rasterio.windows.Window(0, 0, min(src.width, 1000), min(src.height, 1000))
    sample = src.read(window=window)
```

### 2.1 Properties to Extract

| Property | Source | Report As |
|---|---|---|
| Format / Driver | `src.driver` | e.g., "GTiff", "netCDF" |
| Band count | `src.count` | Integer |
| Dimensions (W × H) | `src.width`, `src.height` | pixels |
| Pixel resolution | `src.res` | (x_res, y_res) in CRS units — include units |
| CRS | `src.crs` | EPSG + name + type |
| Bounding box | `src.bounds` | BoundingBox in CRS units |
| Nodata value | `src.nodata` | Per band, or "not set" |
| Data type | `src.dtypes` | Per band (e.g., float32, uint16) |
| Color interpretation | `src.colorinterp` | Per band |
| Compression | `profile.get('compress')` | e.g., LZW, DEFLATE, or "none" |
| Tiling | `profile.get('tiled')` | Boolean |
| Overview levels | `src.overviews(1)` | List of zoom levels |
| File size | `Path(path).stat().st_size` | In MB |
| COG validity | Check if tiled + overviews present | Boolean + note |
| Per-band statistics | min, max, mean, std, p5, p95 | From sample window |

### 2.2 NetCDF / HDF5 Variant

For multi-dimensional datasets, use `xarray`:

```python
import xarray as xr

ds = xr.open_dataset(path)
```

Extract: variable names, dimensions, coordinate names, time range (`ds.time.values[[0, -1]]` if time dimension exists), global attributes, spatial resolution from coordinate spacing, CRS (check `crs` attribute, `spatial_ref` variable, or CF conventions `grid_mapping`).

---

## Phase 3: Tabular Inspection

Use this track for CSV, Excel, Parquet, TXT.

**Key insight:** Tabular files may contain geographic information in various forms — coordinates, WKT geometries, FIPS codes, or address strings. Detecting these enables the downstream skills to convert the table to a GeoDataFrame.

```python
import pandas as pd

# Encoding-safe read
for enc in ['utf-8', 'latin-1', 'cp1252']:
    try:
        df = pd.read_csv(path, encoding=enc, nrows=SAMPLE_ROWS * 10)
        break
    except UnicodeDecodeError:
        continue
```

### 3.1 Properties to Extract

| Property | How to Extract |
|---|---|
| Row count | `len(df)` (or estimate from file size) |
| Column count | `len(df.columns)` |
| Column names and types | `df.dtypes` |
| Null counts per column | `df.isnull().sum()` |
| Sample rows | `df.head(SAMPLE_ROWS)` |
| Unique value counts | `df.nunique()` per column |
| Date/time columns | Columns parseable as datetime |
| Geographic columns | See detection heuristics below |
| Potential join keys | See FIPS/GEOID detection above |

### 3.2 Geographic Column Detection Heuristics

Apply these checks in order. Report confidence level for each detected geographic column.

| Pattern | Confidence | Detected As |
|---|---|---|
| Column pair: `lat`/`latitude`/`y`/`lat_dd` AND `lon`/`longitude`/`lng`/`x`/`lon_dd` (name match) AND values in valid lat/lon ranges | **HIGH** | Point coordinates → use `gpd.points_from_xy()` |
| Column named `geometry`/`geom`/`the_geom`/`wkt` with values starting `POINT`/`POLYGON`/`LINESTRING` | **HIGH** | WKT geometry → use `gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df[col]))` |
| Column named `GEOID`/`FIPS`/`TRACTCE`/`STATEFP`/`COUNTYFP`/`BLKGRPCE` | **HIGH** | Census join key → join to Census boundary shapefile |
| Column values match `^[0-9]{5}$` (5 digits) or `^[0-9]{2}[0-9]{3}$` | **HIGH** | Likely county FIPS code |
| Column named `zip`/`zipcode`/`ZIP`/`postal_code` | **MEDIUM** | ZIP code → geocodable or join to ZIP shapefile |
| Column named `address`/`street`/`city_name` + `state`/`state_fips` | **MEDIUM** | Address string → geocodable via Census or Nominatim |
| Column named `iso_a3`/`iso_a2`/`country_code`/`ADM0_A3` | **MEDIUM** | Country join key |
| Numeric column pair with values in [-90, 90] AND [-180, 180] (name does not match lat/lon) | **LOW** | Possible coordinates — verify column names |

**FIPS/GEOID dtype warning:** Flag `FIPS_AS_FLOAT` if detected FIPS/GEOID columns are float dtype. This means leading zeros were dropped when reading.

**Suggested conversion code:** For HIGH-confidence detections, include a ready-to-use code snippet in the report.

---

## Phase 4: Quality Flags

After inspection, classify quality issues using this flag system. Every flag has a severity and a recommended remediation.

| Flag | Severity | Condition | Recommended Remediation |
|---|---|---|---|
| `NO_CRS` | **CRITICAL** | Spatial file has no CRS defined | Set CRS explicitly: `gdf = gdf.set_crs(epsg=XXXX)` |
| `MISSING_SIDECAR` | **CRITICAL** | `.prj` absent from Shapefile | Regenerate from known CRS: `gdf.to_file()` exports `.prj` automatically |
| `FIPS_AS_FLOAT` | **CRITICAL** | FIPS/GEOID column is float dtype | Re-read with `dtype={'GEOID': str}` |
| `GEOGRAPHIC_CRS` | **WARNING** | CRS is geographic (degrees) and analysis involves distance/area | Reproject: `gdf.to_crs(epsg=XXXX)` via `geodata-operation` skill |
| `INVALID_GEOMETRIES` | **WARNING** | > `INVALID_GEOM_THRESHOLD` invalid geometries | Fix with `gdf.geometry = gdf.geometry.buffer(0)`, or `shapely.make_valid()` |
| `HIGH_NULL_RATE` | **WARNING** | Any field exceeds `NULL_THRESHOLD` nulls | Investigate before joins — `df.dropna(subset=[col])` before calculations |
| `MIXED_GEOMETRY_TYPES` | **WARNING** | Multiple geometry types in one layer | Separate by type or use `gdf.explode()` |
| `FIPS_AS_INT` | **WARNING** | FIPS/GEOID stored as int — leading zeros absent | Re-read with `dtype=str` or convert: `gdf['GEOID'].astype(str).str.zfill(N)` |
| `EMPTY_GEOMETRIES` | **INFO** | Any empty geometries | `gdf = gdf[~gdf.geometry.is_empty]` |
| `DUPLICATE_GEOMETRIES` | **INFO** | Duplicate geometries present | Investigate — may be intentional (e.g., multi-record features) |
| `CRS_UNITS_FEET` | **INFO** | CRS uses feet not meters | Distances/areas computed in feet — divide by 3.28084 for meters |
| `NO_NODATA` | **INFO** | Raster has no nodata value defined | Nodata pixels will be treated as data — specify: `src.nodata = value` |
| `LARGE_FILE` | **INFO** | > `LARGE_VECTOR_THRESHOLD` features or > `LARGE_RASTER_THRESHOLD_PX` pixels | Use windowed/chunked processing in downstream operations |
| `NO_GEO_COLUMNS` | **INFO** | Tabular file has no detected geographic columns | Manual inspection needed before spatial use |
| `LONG_FIELD_NAMES` | **WARNING** | Any field name exceeds 10 characters (Shapefile only) | Shapefile driver will silently truncate on export; use GeoPackage instead |
| `NAN_IN_JOIN_KEY` | **CRITICAL** | A detected FIPS/GEOID or join key column contains any null values | Even one null silently drops a row in joins; `df.dropna(subset=[join_key])` before joining |

---

## Phase 5: Suitability Assessment

Report readiness for each downstream NORA skill. List any blockers with specific remediation.

| Downstream Skill | Required Conditions | Assessment Logic |
|---|---|---|
| `spatial-analysis` | Valid CRS, clean geometries, sufficient N (>30 recommended for regression), numeric outcome variable | Check CRS, geometry validity, row count, numeric column presence |
| `geodata-operation` | File exists, valid CRS for spatial ops, geometry type compatible with intended operation | Check basic spatial validity, file accessibility |
| `paper-figure-generate` | Spatial data with valid CRS and reasonable extent, geometry type plottable | Check CRS, extent reasonableness |
| `data-download` | N/A — metadata-inspect validates post-download | Compare file size to expected, verify format matches manifest |

Output format per skill:
```
✓ spatial-analysis: READY
  └─ N=3142 features, CRS=EPSG:4269 (geographic — reproject before distance ops), 0 invalid geometries
✗ geodata-operation (buffer): BLOCKED
  └─ GEOGRAPHIC_CRS: reproject to projected CRS before buffering
```

---

## Phase 6: Outputs

Write to `output/metadata-inspect/` using the dataset filename as the base name (without extension).

### Markdown Report (`<dataset_name>_metadata.md`)

```markdown
# Metadata Report: [filename]

**Inspected**: [ISO date]
**Path**: [absolute path]
**Format**: [format name]
**File size**: [MB]

## Schema
[field name | dtype | null_count | null_pct | sample values — table]

## Spatial Properties
[CRS: EPSG code, name, type, units]
[Extent: minx, miny, maxx, maxy]
[Geometry type(s), feature count]
[For rasters: bands, resolution, nodata, dimensions]

## Quality Flags
[flag | severity | detail | remediation — table, sorted by severity]

## Suitability Assessment
[per-skill readiness with blockers]

## Sample Data
[first SAMPLE_ROWS rows as markdown table, or raster band statistics]

## Suggested Next Steps
[ranked list: fix critical issues first, then warnings, then proceed to operation/analysis]
```

### JSON Metadata (`<dataset_name>_metadata.json`)

Machine-readable output consumed by `geodata-operation` and `spatial-analysis`:

```json
{
  "file_path": "...",
  "format": "vector|raster|tabular",
  "inspected_at": "ISO-8601",
  "schema": {"field_name": {"dtype": "...", "null_count": 0, "null_pct": 0.0, "sample": [...]}},
  "spatial": {
    "crs": {"epsg": 4326, "name": "WGS 84", "type": "geographic", "units": "degrees"},
    "bounds": [minx, miny, maxx, maxy],
    "geometry_type": "MultiPolygon",
    "feature_count": 3142
  },
  "quality_flags": [{"flag": "GEOGRAPHIC_CRS", "severity": "WARNING", "detail": "..."}],
  "suitability": {
    "spatial-analysis": {"ready": true, "blockers": []},
    "geodata-operation": {"ready": false, "blockers": ["GEOGRAPHIC_CRS for distance ops"]}
  },
  "fips_columns": ["GEOID", "STATEFP", "COUNTYFP"],
  "geo_columns_detected": [{"column": "lat", "confidence": "HIGH", "type": "latitude"}]
}
```

---

## Guardrails

| Mistake | Prevention |
|---|---|
| Loading a 10 GB raster into memory | Use `rasterio.open()` for metadata only; compute stats from sample window or overviews |
| Treating FIPS/GEOID as float | Flag `FIPS_AS_FLOAT` with critical severity; provide re-read code |
| Assuming lat/lon columns without checking value ranges | Geographic column detection requires both name pattern AND value range validation |
| Reporting CRS as "unknown" without recovery attempts | Attempt recovery: `.prj` sidecar → coordinate range heuristic |
| Missing encoding issues in Shapefiles | Try UTF-8 first, then latin-1, cp1252 — report which worked |
| Treating `.parquet` as tabular without checking geo metadata | Attempt `geopandas.read_parquet()` first |
| Loading every feature for count on a shapefile with 10M features | Use `fiona.open()` for count + schema without loading |
| Modifying source data during inspection | This skill is read-only — write only to `output/metadata-inspect/` |
| Ignoring the `.prj` absence for Shapefiles | Always check sidecar presence; flag `MISSING_SIDECAR` |

---

## Key Principles

- **Read-only.** Never write to or modify source files.
- **CRS first.** Every spatial file gets a CRS verdict — defined/geographic/projected/unknown — before anything else.
- **Proportional depth.** A 10-row CSV gets a quick scan; a 100-band satellite image gets full band statistics.
- **Machine-readable output.** The JSON metadata enables downstream automation — always write it.
- **Fail gracefully.** If one property cannot be extracted, report it as unavailable and continue with the rest.
- **Explicit about FIPS/GEOID.** These columns are a common source of silent join failures — always flag type issues.
- **Data-side bugs are real.** Map projection inconsistency, FIPS leading zeros, NaN cells, and type mismatches are data issues that masquerade as code bugs (LLM-Geo insight). Surface them clearly.

---

## Composing with Other Skills

```
/data-download "dataset"           → acquires raw data
/metadata-inspect "data/file.gpkg" ← you are here
/geodata-operation "reproject"     → fix GEOGRAPHIC_CRS flag
/geodata-operation "fix geometries" → fix INVALID_GEOMETRIES flag
/spatial-analysis "question"       → analysis (reads metadata JSON for pre-computed readiness)
/paper-figure-generate             → uses CRS and extent metadata for map configuration
```

**Integration points:**
- **From `data-download`**: Invoke automatically after every download to validate the result. Feed `output/metadata-inspect/<name>_metadata.json` path into the data manifest.
- **To `geodata-operation`**: Quality flags directly drive operation selection. `GEOGRAPHIC_CRS` → reproject first. `INVALID_GEOMETRIES` → fix geometries. `FIPS_AS_FLOAT` → re-read with correct dtype.
- **To `spatial-analysis`**: The suitability assessment and JSON metadata replace the manual data readiness check in `spatial-analysis` Section 2. Read the JSON at analysis start to skip redundant inspection.
- **Knowledge base**: See `skills/knowledge/spatial-methods.md` for CRS projection code and spatial weights setup.
- **MCP tools**: `get_epsg_info(epsg)` for CRS details; `suggest_crs(country, analysis_type, lat, lon)` for CRS recommendations.
