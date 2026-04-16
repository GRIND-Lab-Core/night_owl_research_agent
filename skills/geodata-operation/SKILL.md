---
name: geodata-operation
description: 'Geodata manipulation and spatial data operations. Performs spatial joins, overlays (clip/intersect/union/difference), buffering, dissolve, reprojection, format conversion, raster calculations (NDVI/NDWI/NBR/zonal stats/reclassify/mosaic/clip), geocoding, and network analysis. This is the data wrangling complement to the analytical spatial-analysis skill — it transforms data, not analyzes it. Use when user says "reproject", "clip", "spatial join", "buffer", "convert format", "calculate NDVI", "zonal statistics", "dissolve", "geocode", "mosaic rasters", "overlay", "intersect layers", "fix geometries", or needs any geodata transformation before analysis.'
argument-hint: [operation-and-data-description]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
---

# Geodata Operation: Spatial Data Manipulation

Execute: **$ARGUMENTS**

## Purpose

This skill performs geodata manipulation — the "hands-on data wrangling" that prepares data for analysis or publication. It transforms, combines, clips, reprojects, and converts spatial data. **It does not perform statistical analysis** — that is `spatial-analysis`.

Read `skills/knowledge/spatial-methods.md` for CRS reference and raster processing snippets. If `metadata-inspect` has been run on the input data, read `output/metadata-inspect/<dataset>_metadata.json` to skip redundant checks.

---

## Constants

- **OUTPUT_DIR = `output/geodata-operation`** — Destination for reports, logs, scripts.
- **DATA_DIR = `data/processed/`** — Destination for processed data files.
- **MAX_RASTER_MEMORY_GB = 4** — Use windowed processing above this threshold.
- **PRESERVE_ORIGINALS = true** — Never overwrite source files; always write to new paths.
- **LOG_OPERATIONS = true** — Log every operation with inputs, outputs, and parameters.
- **MAX_AUTO_RETRY = 2** — Attempt auto-recovery on error up to this many times, then report and stop.

> Override via argument, e.g., `/geodata-operation "buffer 500m" — output dir: results/`.

---

## Section 1: Operation Classification

Map the user's request to an operation category before writing any code.

| Operation | Signal Phrases | Primary Library | Key Guardrail |
|---|---|---|---|
| **Spatial Join** | "join by location", "spatial join", "attach attributes from", "points in polygons" | geopandas `sjoin`, `sjoin_nearest` | CRS must match; check for many-to-many duplicates |
| **Overlay** | "clip", "intersect", "union", "difference", "erase", "symmetric difference" | geopandas `overlay`, `clip` | CRS must match; fix invalid geometries first |
| **Buffer** | "buffer", "within X meters", "create buffer zone", "proximity" | geopandas `.buffer()` | **Must be in projected CRS (meters)** |
| **Dissolve** | "dissolve", "aggregate by", "merge polygons by field" | geopandas `.dissolve()` | Specify `aggfunc` for numeric columns |
| **Reprojection** | "reproject", "change CRS", "convert to UTM", "to EPSG:XXXX" | geopandas `.to_crs()`, rasterio `reproject` | Validate source CRS exists first |
| **Format Conversion** | "convert to GeoPackage", "save as GeoJSON", "export shapefile" | geopandas `.to_file()` | Preserve CRS; handle encoding |
| **Spectral Index** | "NDVI", "NDWI", "NBR", "NDBI", "BSI", "band math" | rasterio + numpy | Always mask nodata; add epsilon for division |
| **Zonal Statistics** | "zonal stats", "mean per zone", "summarize raster by polygon" | rasterstats, rioxarray | CRS must match raster and zones |
| **Raster Clip** | "clip raster", "mask raster", "extract by polygon" | rioxarray `.clip()` | CRS must match |
| **Raster Mosaic** | "mosaic", "merge rasters", "combine tiles" | rasterio.merge | All inputs must share CRS, resolution, band count |
| **Reclassify** | "reclassify", "remap values", "bin raster" | rasterio + numpy | Preserve nodata; document mapping table |
| **Geocoding** | "geocode", "address to coordinates", "lat/lon from address" | geopy, Census geocoder | Rate limiting required; batch > 100 → pause |
| **Network Analysis** | "shortest path", "isochrone", "service area", "routing" | osmnx + networkx | Requires OSM download; use projected CRS for distances |
| **Merge/Concat** | "combine datasets", "append features", "merge tables" | geopandas `pd.concat`, `.merge()` | Check CRS consistency; handle duplicate IDs |
| **Fix Geometries** | "fix invalid geometries", "repair geometry" | shapely `make_valid`, `buffer(0)` | Verify result with `is_valid` |
| **Areal Interpolation** | "interpolate between zones", "crosswalk", "population-weight" | tobler (PySAL) | Area-weighted; document assumptions |

**If the operation is unclear**, ask the user to specify: (1) what layer(s) are the inputs, (2) what the desired output represents, and (3) whether a specific method is required.

---

## Section 2: Pre-Operation Checks

**These checks are mandatory before any spatial operation. Do not skip them.**

If `metadata-inspect` output exists for the input file(s), read the JSON to obtain these checks pre-computed — skip re-inspection for those fields.

| Check | When Required | Test | On Failure |
|---|---|---|---|
| Input file exists | Always | `Path(path).exists()` | STOP — report path and suggest checking `data/raw/` |
| CRS is defined | All spatial ops | `gdf.crs is not None` | Attempt recovery or STOP |
| CRS match (multi-input) | Spatial join, overlay, zonal stats, raster clip | `gdf1.crs == gdf2.crs` | Reproject minority layer to match majority |
| CRS is projected | Buffer, distance-based ops | `gdf.crs.is_projected` | Reproject to local UTM first (see UTM estimation below) |
| Valid geometries | Overlay, spatial join | `gdf.geometry.is_valid.all()` | Fix with `gdf.geometry = gdf.geometry.buffer(0)` |
| No empty geometries | All spatial ops | `~gdf.geometry.is_empty.any()` | `gdf = gdf[~gdf.geometry.is_empty]` |
| Memory estimate (raster) | Raster load | bands × width × height × bytes_per_pixel | Use windowed processing if > MAX_RASTER_MEMORY_GB |

**UTM zone estimation** (when no local CRS is specified):

```python
centroid = gdf.geometry.unary_union.centroid
zone = int((centroid.x + 180) / 6) + 1
hem = 32600 if centroid.y >= 0 else 32700
epsg_utm = hem + zone
gdf_proj = gdf.to_crs(epsg=epsg_utm)
```

---

## Section 3: Vector Operations

### 3.1 Spatial Join

**Predicate selection (critical — choose wrong predicate and results silently break):**

| Situation | Predicate |
|---|---|
| Points in polygons | `'within'` or `'intersects'` |
| Polygons sharing area | `'intersects'` |
| Polygon A entirely inside polygon B | `'within'` |
| Polygon A fully contains polygon B | `'contains'` |
| Shared edges only | `'touches'` |
| Nearest feature (no overlap required) | `sjoin_nearest` with `max_distance` |

**The sjoin signature (LLM-Geo verified):**
```python
# Default 'inner' join: keeps only left_gdf geometry
result = gpd.sjoin(left_gdf, right_gdf, how='left', predicate='intersects',
                   lsuffix='left', rsuffix='right')
```

**Critical: sjoin returns one-to-many.** If a left feature intersects multiple right features, it appears multiple times in the output. Always handle this explicitly:

```python
# Check for duplicates
n_before = len(left_gdf)
n_after = len(result)
if n_after > n_before:
    # Decide: keep first match, aggregate, or keep all
    result_dedup = result.drop_duplicates(subset=[left_gdf.index.name or 'index'])
```

**Do NOT use `GeoSeries.intersects()` when you need attribute transfer** — it returns a boolean mask, not a joined DataFrame. Use `sjoin` for attribute transfer; `intersects()` for boolean filtering only.

### 3.2 Overlay Operations

| Operation | GeoPandas Call | Result Geometry |
|---|---|---|
| Clip (mask input to boundary) | `gpd.clip(gdf, mask)` | Features within mask extent |
| Intersection (shared area + both attributes) | `gpd.overlay(gdf1, gdf2, how='intersection')` | Overlapping areas |
| Union (all areas + attributes where present) | `gpd.overlay(gdf1, gdf2, how='union')` | Full combined extent |
| Difference (gdf1 minus gdf2) | `gpd.overlay(gdf1, gdf2, how='difference')` | gdf1 area outside gdf2 |
| Symmetric difference | `gpd.overlay(gdf1, gdf2, how='symmetric_difference')` | Non-overlapping areas |

**Before any overlay:** Fix invalid geometries:
```python
gdf1.geometry = gdf1.geometry.buffer(0)
gdf2.geometry = gdf2.geometry.buffer(0)
```

**After overlay:** Check for empty result. An empty overlay usually means CRS mismatch (check that extents actually overlap) or all invalid geometries.

### 3.3 Buffer

**Non-negotiable: buffer requires a projected CRS.** Geographic CRS (degrees) produces meaningless elliptical buffers and incorrect distances.

```python
# Always check before buffering
assert gdf.crs.is_projected, \
    f"Buffer requires projected CRS — current CRS is {gdf.crs} (units: degrees). Reproject first."

# Buffer in meters (assuming meters CRS)
buffered = gdf.copy()
buffered['geometry'] = gdf.geometry.buffer(distance_meters)
```

**Buffer distance units decision:**

| CRS Units | Buffer Input | Reminder |
|---|---|---|
| meters | distance in meters | Direct — most common after UTM reproject |
| feet | distance in feet | Divide by 3.28084 to convert to meters |
| degrees | **Never buffer in degrees** | Reproject first, always |

### 3.4 Dissolve

```python
# Dissolve by field, specifying aggregation for numeric columns
dissolved = gdf.dissolve(
    by='field_name',
    aggfunc={
        'population': 'sum',
        'area_km2': 'sum',
        'name': 'first',
        'value': 'mean'
    }
)
```

**If no aggregation field:** `gdf.dissolve()` merges all features into one.

**Shapefile field name limit (10 chars):** If writing dissolved output to Shapefile, truncate field names to ≤ 10 characters. Use GeoPackage instead to avoid this constraint.

### 3.5 Reprojection (Vector)

```python
# Reproject to known EPSG
gdf_reprojected = gdf.to_crs(epsg=32618)  # UTM Zone 18N

# Reproject to match another layer
gdf_reprojected = gdf.to_crs(other_gdf.crs)
```

**Only reproject when needed.** Do not reproject a single layer that is already in a suitable CRS. Reproject when: (1) multiple layers have different CRS, (2) distance/area/buffer operations require projected CRS.

**Do NOT reproject DataFrames from CSV.** CSV files have no CRS — the rule applies only to GeoDataFrames.

### 3.6 Format Conversion (Vector)

```python
# To GeoPackage (recommended — no field length limit, supports all geometry types)
gdf.to_file('output.gpkg', driver='GPKG')

# To GeoJSON (WGS84 only by convention — reproject to EPSG:4326 first)
gdf.to_crs(epsg=4326).to_file('output.geojson', driver='GeoJSON')

# To Shapefile (legacy — 10-char field name limit, no mixed geometry types)
gdf.to_file('output.shp', encoding='utf-8')

# Load zipped Shapefile from URL (do NOT download and unzip manually)
gdf = gpd.read_file('https://example.com/data.zip')
```

---

## Section 4: Raster Operations

### 4.1 Spectral Index Calculation

**Band mapping reference** — always verify band order from raster metadata before calculating:

| Index | Formula | Sentinel-2 Bands | Landsat 8/9 Bands | Use Case |
|---|---|---|---|---|
| NDVI | (NIR − Red) / (NIR + Red) | B8 (NIR), B4 (Red) | B5 (NIR), B4 (Red) | Vegetation health |
| NDWI | (Green − NIR) / (Green + NIR) | B3 (Green), B8 (NIR) | B3 (Green), B5 (NIR) | Water detection |
| NBR | (NIR − SWIR2) / (NIR + SWIR2) | B8 (NIR), B12 (SWIR2) | B5 (NIR), B7 (SWIR2) | Burn severity |
| NDBI | (SWIR1 − NIR) / (SWIR1 + NIR) | B11 (SWIR1), B8 (NIR) | B6 (SWIR1), B5 (NIR) | Built-up areas |
| BSI | ((SWIR1+Red)−(NIR+Blue)) / ((SWIR1+Red)+(NIR+Blue)) | B11, B4, B8, B2 | B6, B4, B5, B2 | Bare soil |
| MNDWI | (Green − SWIR1) / (Green + SWIR1) | B3, B11 | B3, B6 | Open water (better than NDWI) |

**Implementation pattern (memory-safe, nodata-aware):**

```python
import rasterio
import numpy as np

def calculate_spectral_index(nir_path, red_path, output_path, nodata_val=-9999):
    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype('float32')
        nodata = nir_src.nodata
        profile = nir_src.profile.copy()

    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype('float32')

    # Mask nodata pixels
    nodata_mask = (nir == nodata) | (red == nodata) if nodata is not None else np.zeros_like(nir, dtype=bool)

    # Calculate with epsilon to prevent division by zero
    denominator = nir + red
    index = np.where(
        nodata_mask | (denominator == 0),
        nodata_val,
        (nir - red) / (denominator + 1e-10)
    )

    # Write output
    profile.update(dtype='float32', count=1, nodata=nodata_val, compress='lzw')
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(index.astype('float32'), 1)
```

**Always check output value range:** NDVI, NDWI, NBR should fall in [-1, 1]. Values outside this range indicate nodata masking or dtype issues.

### 4.2 Zonal Statistics

```python
from rasterstats import zonal_stats
import geopandas as gpd
import pandas as pd

# CRS MUST match between raster and zones
zones = gpd.read_file(zones_path)
# Reproject zones to raster CRS if needed:
# with rasterio.open(raster_path) as src: zones = zones.to_crs(src.crs)

stats = zonal_stats(
    zones,
    raster_path,
    stats=['min', 'max', 'mean', 'median', 'std', 'count', 'sum'],
    nodata=-9999,
    geojson_out=False
)
zones = zones.join(pd.DataFrame(stats))
```

**Common statistics:** `min`, `max`, `mean`, `median`, `std`, `count`, `sum`, `percentile_25`, `percentile_75`.

### 4.3 Raster Reprojection

```python
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Resampling method — critical choice:
# Continuous data (DEM, temperature, NDVI): Resampling.bilinear or .cubic
# Categorical data (land cover, land use classes): Resampling.nearest
# Count/sum data: Resampling.sum

dst_crs = 'EPSG:32618'

# CRITICAL: Choose resampling method based on data type — wrong choice corrupts categorical data
# Continuous data (DEM, temperature, NDVI, spectral indices): Resampling.bilinear or .cubic
# Categorical data (land cover, NLCD, land use classes): Resampling.nearest  ← ALWAYS
# Count/aggregate data: Resampling.nearest or .sum
resampling_method = Resampling.bilinear     # <--- CHANGE to Resampling.nearest for categorical rasters

with rasterio.open(src_path) as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({'crs': dst_crs, 'transform': transform, 'width': width, 'height': height})
    with rasterio.open(dst_path, 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(source=rasterio.band(src, i), destination=rasterio.band(dst, i),
                      src_transform=src.transform, src_crs=src.crs,
                      dst_transform=transform, dst_crs=dst_crs,
                      resampling=resampling_method)
```

### 4.4 Raster Clip by Polygon

```python
import rioxarray

rds = rioxarray.open_rasterio(raster_path)
# Reproject zones to match raster CRS if needed
zones_proj = zones.to_crs(rds.rio.crs)
clipped = rds.rio.clip(zones_proj.geometry, zones_proj.crs, drop=True, invert=False)
clipped.rio.to_raster(output_path, compress='lzw')
```

### 4.5 Raster Mosaic

```python
from rasterio.merge import merge
import rasterio

src_files = [rasterio.open(f) for f in raster_paths]
# ALL inputs must share CRS, band count, and preferably resolution
mosaic, out_transform = merge(src_files, method='first')  # 'first', 'last', 'min', 'max', 'mean'

out_meta = src_files[0].meta.copy()
out_meta.update({'height': mosaic.shape[1], 'width': mosaic.shape[2],
                 'transform': out_transform, 'compress': 'lzw'})
with rasterio.open(output_path, 'w', **out_meta) as dst:
    dst.write(mosaic)
for src in src_files:
    src.close()
```

**Before mosaic:** Verify all inputs have the same CRS (`src.crs`), band count (`src.count`), and dtype. Reproject mismatched inputs before merging.

### 4.6 Reclassify

```python
import numpy as np
import rasterio

# Define reclassification mapping: {old_value: new_value}
reclass_map = {1: 10, 2: 10, 3: 20, 4: 20, 5: 30, 11: 0}  # e.g., NLCD → simplified classes

with rasterio.open(src_path) as src:
    data = src.read(1)
    nodata = src.nodata
    profile = src.profile.copy()

reclassed = np.full_like(data, nodata if nodata is not None else 0)
for old_val, new_val in reclass_map.items():
    reclassed[data == old_val] = new_val

with rasterio.open(output_path, 'w', **profile) as dst:
    dst.write(reclassed, 1)
```

**Always document the reclassification table** in the operation log.

---

## Section 5: Geocoding

**Geocoding converts addresses or place names to coordinates.** Use it only when coordinate data is unavailable. For US data, the Census Geocoder is preferred (public, high accuracy, no API key).

| Provider | API Key | Rate Limit | Best For |
|---|---|---|---|
| Census Geocoder (batch) | None | 10,000/batch | US addresses — most accurate |
| Nominatim (OSM) | None | 1 req/sec | Global addresses, non-commercial |
| Google Maps API | Required | Usage-based | High-accuracy global (PAUSE — confirm key with user) |

```python
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

geolocator = Nominatim(user_agent='nora_research_agent')
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)  # 1 req/sec for Nominatim

df['location'] = df['address'].apply(geocode)
df['latitude'] = df['location'].apply(lambda loc: loc.latitude if loc else None)
df['longitude'] = df['location'].apply(lambda loc: loc.longitude if loc else None)
```

**Guardrails:**
- **> 100 addresses:** Confirm with user before starting — geocoding takes time.
- **> 1000 addresses:** Recommend Census batch geocoder instead of row-by-row.
- **Failed geocodes:** If Nominatim returns None, try simplifying the place name (remove apt numbers, zip codes). Do not silently drop — flag failed rows.

---

## Section 6: Network Analysis

Use only when the research question specifically requires routing, accessibility, or reachability. Do not add network analysis to a workflow just because spatial data is involved.

**OSM data downloads belong in `data-download`, not here.** If the task involves downloading OSM POIs, boundaries, or features (rather than routing on an existing network), use `/data-download` instead. The critical Overpass rule (`relation({osm_id}); map_to_area->.rel;`) is documented there — do not write Overpass queries in this skill.

```python
import osmnx as ox
import networkx as nx

# Download street network for a place
G = ox.graph_from_place("Atlanta, Georgia", network_type='drive')
# Or from bounding box: G = ox.graph_from_bbox(north, south, east, west, network_type='walk')

# Add travel time (requires projected CRS for speed calculation)
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

# Nearest network nodes to origin/destination points
orig_node = ox.nearest_nodes(G, orig_lon, orig_lat)
dest_node = ox.nearest_nodes(G, dest_lon, dest_lat)

# Shortest path (by distance or travel time)
route = nx.shortest_path(G, orig_node, dest_node, weight='travel_time')
route_length = nx.shortest_path_length(G, orig_node, dest_node, weight='length')
```

**Network type selection:**

| Use Case | `network_type` | Weight |
|---|---|---|
| Driving distance | `'drive'` | `'length'` (m) or `'travel_time'` (s) |
| Walking accessibility | `'walk'` | `'length'` |
| Cycling | `'bike'` | `'length'` |
| All roads | `'all'` | `'length'` |

---

## Section 7: Error Handling and Recovery

When an operation fails, follow this structured recovery approach. Maximum **`MAX_AUTO_RETRY` = 2** auto-recovery attempts. After that, report the error clearly with diagnosis and stop.

**Error recovery table:**

| Error Category | Common Cause | Recovery Strategy | Fallback |
|---|---|---|---|
| CRS mismatch | Different CRS between inputs | Reproject minority to majority CRS | Check if extents actually overlap |
| Invalid geometry | Self-intersection, unclosed rings | `gdf.geometry = gdf.geometry.buffer(0)` | `shapely.make_valid(geom)` for persistent cases |
| Empty overlay result | CRS mismatch or no spatial overlap | Verify CRS equality and extent overlap | Check if geometries are in same hemisphere |
| Memory error (raster) | Full raster load | Switch to windowed/chunked processing | Subsample or mosaic tiles |
| Topology error | Invalid overlay inputs | Fix all input geometries → retry | Use `gpd.clip()` instead of `overlay()` |
| Encoding error (Shapefile) | Non-UTF-8 field values | Try `encoding='latin-1'` or `'cp1252'` | Re-encode with `iconv` in Bash |
| File not found | Wrong path | Check `data/raw/` and `data/processed/` | List `data/` directory |
| Field not found | Wrong column name | Print `gdf.columns.tolist()` | Use `str.lower()` comparison |
| sjoin empty result | Predicate too restrictive | Try `'intersects'` instead of `'within'` | Verify CRS match and check spatial overlap |
| FIPS join failure | Type mismatch (str vs int) | Convert to str with `.str.zfill(N)` | Check unique values from both sides |

**5-tier fallback strategy (SpatialAnalysisAgent pattern):**
1. Retry with fixed inputs (geometry fix, CRS reproject)
2. Try alternative function (e.g., `gpd.clip()` instead of `overlay()`, `rioxarray` instead of `rasterio.mask`)
3. Break into simpler sub-steps
4. Use native Python/numpy alternative
5. Manual implementation — report approach to user

---

## Section 8: FIPS/GEOID Join Handling

Joining spatial data to Census tables is a frequent operation with common failure modes. Apply these rules every time FIPS/GEOID columns are involved.

**The joining problem:** Census FIPS codes may be stored as:
- `str` with leading zeros: `"06"`, `"06037"`, `"06037970100"` — correct
- `int` without leading zeros: `6`, `6037`, `6037970100` — common after Excel or float read
- `float` with decimals: `6.0`, `6037.0` — worst case (destroys leading zeros)

**Always convert to zero-padded string before joining.** The safe pattern handles all three storage forms (already-str, int, and float-string like `"6.0"` from Excel):

```python
def to_fips_str(col, width):
    """Convert FIPS/GEOID column to zero-padded string, regardless of storage type.
    Handles: str "06" → "06", int 6 → "06", float-str "6.0" → "06"
    DO NOT use .astype(int) — it fails on already-correct string FIPS like "06".
    """
    s = col.astype(str).str.strip()
    s = s.str.replace(r'\.0+$', '', regex=True)  # strip "6.0" → "6"
    return s.str.zfill(width)

# State: 2 digits
gdf['STATEFP'] = to_fips_str(gdf['STATEFP'], 2)

# County: 5 digits (state + county concatenated)
gdf['GEOID'] = to_fips_str(gdf['GEOID'], 5)

# Census tract: 11 digits
gdf['GEOID'] = to_fips_str(gdf['GEOID'], 11)

# Block group: 12 digits
gdf['GEOID'] = to_fips_str(gdf['GEOID'], 12)
```

**Never read FIPS/GEOID as float.** When loading CSV: `pd.read_csv(path, dtype={'GEOID': str, 'FIPS': str})`.

**Before joining, remove NaN rows from join key columns:**
```python
df = df.dropna(subset=['GEOID'])
gdf = gdf.dropna(subset=['GEOID'])
```

---

## Section 9: NaN and Data Quality Handling

**Always remove NaN from join key and calculation columns before operations.** NaN propagation is one of the most common causes of silent analysis failures (LLM-Geo insight).

```python
# Before any join
df = df.dropna(subset=['join_key_column'])

# Before calculations
df = df.dropna(subset=['value_col_1', 'value_col_2'])

# Check for NaN in results
n_null = result['output_col'].isnull().sum()
if n_null > 0:
    print(f"Warning: {n_null} null values in output column")
```

**Do NOT auto-drop all NaN rows.** Inspect the spatial pattern of missing values — clustered missingness may be meaningful (e.g., hospitals with no reported cases). Only drop when the missing value would corrupt the operation.

---

## Section 10: Operation Provenance Log

Every operation is logged to `output/geodata-operation/operation_log.md`. Append each entry:

```markdown
## [Operation Type] — [ISO date]

| Field | Value |
|---|---|
| Input(s) | [file paths] |
| Output | [file path] |
| Operation | [description] |
| Parameters | [key params: CRS, distance, predicate, method, etc.] |
| Input CRS | [EPSG] |
| Output CRS | [EPSG] |
| Input features/pixels | [count] |
| Output features/pixels | [count] |
| Warnings | [any issues encountered] |
| Script | [path to saved script] |
```

Also update `data/DATA_MANIFEST.md` with each new processed dataset.

---

## Section 11: Guardrails Summary

| Mistake | Prevention |
|---|---|
| Buffering in geographic CRS (degrees) | Pre-operation check enforces projected CRS; auto-reproject to UTM |
| Spatial join with CRS mismatch | Pre-operation check; reproject before sjoin |
| sjoin one-to-many silently inflates rows | Always check `len(result) > len(left_gdf)` after join |
| Using `GeoSeries.intersects()` for attribute transfer | Decision table: `intersects()` = boolean filter; `sjoin()` = attribute transfer |
| Division by zero in band math | Epsilon (`1e-10`) in denominator; always set |
| Nodata pixels treated as data in raster ops | Explicit nodata masking before every calculation |
| Bilinear resampling on categorical raster | Resampling decision table: categorical → `nearest` always |
| Overwriting source data | `PRESERVE_ORIGINALS = true`; always write to new path |
| Float FIPS/GEOID breaking Census joins | FIPS handling section; convert to zero-padded str |
| NaN in join key causing row loss | Always `dropna(subset=[join_key])` before joining |
| Overlay on invalid geometries | Pre-operation check: fix with `buffer(0)` first |
| Shapefile field names > 10 chars | Use GeoPackage instead; truncate to 10 chars if shapefile required |
| No log of what operations were applied | LOG_OPERATIONS constant; every operation gets a log entry |
| Zonal stats CRS mismatch (raster vs zones) | Pre-operation check; reproject zones to raster CRS |

---

## Section 12: Outputs

- `data/processed/<descriptive_name>.<format>` — Primary processed data output
- `output/geodata-operation/operation_log.md` — Provenance log of all operations
- `output/geodata-operation/scripts/` — Python scripts for reproducibility
- `output/geodata-operation/previews/` — Quick-look maps of operation results (optional)
- `data/DATA_MANIFEST.md` — Updated with new processed dataset entries

**Naming convention for output files:** Use descriptive names that encode the operation and source, e.g., `counties_buffered_50km.gpkg`, `ndvi_sentinel2_atlanta_2023.tif`, `census_tracts_joined_income.gpkg`.

---

## Key Principles

- **CRS first.** Every spatial operation starts with CRS validation. Wrong CRS = wrong analysis.
- **Never modify source data.** `PRESERVE_ORIGINALS = true`. All outputs go to `data/processed/`.
- **NaN is not your friend.** Remove NaN from join keys and calculation columns before operations.
- **sjoin multiplies rows.** Always check output row count and handle one-to-many explicitly.
- **FIPS/GEOID typing is critical.** Read as str; convert int to zero-padded str before joins.
- **Proportional implementation.** A simple reproject is 3 lines. A complex multi-step pipeline may need error handling and intermediate validation.
- **Log everything.** Every operation gets a provenance entry. Reproducibility requires traceability.
- **Data-side bugs exist.** CRS mismatch, FIPS type issues, NaN cells, and ESRI encoding — these are data problems that look like code bugs. Check the data first.

---

## Composing with Other Skills

```
/data-download "dataset"           → acquires raw data
/metadata-inspect "path"           → understand data, surface quality flags
/geodata-operation "transform"     ← you are here
/spatial-analysis "question"       → statistical analysis of prepared data
/deploy-experiment                 → orchestrated experiment execution
/paper-figure-generate             → publication figures from outputs
```

**Integration points:**
- **From `metadata-inspect`**: Quality flags drive operation selection. `GEOGRAPHIC_CRS` → reproject. `INVALID_GEOMETRIES` → fix geometries. `FIPS_AS_FLOAT` → re-read. Read `output/metadata-inspect/<name>_metadata.json` to skip pre-operation checks.
- **From `data-download`**: Raw files in `data/raw/` → processed outputs in `data/processed/`.
- **To `spatial-analysis`**: Prepared data (clean geometries, projected CRS, joined attributes) feeds directly into `spatial-analysis` Section 2 prerequisites.
- **Knowledge base**: `skills/knowledge/spatial-methods.md` — CRS reference (Section 1), raster processing (Section 4), spectral indices.
- **MCP tools**: `suggest_crs` for CRS recommendations; `get_gadm_boundaries` for boundary retrieval for clipping; `get_osm_data` for network or POI data.
