---
name: geo-plot
description: Generate publication-quality spatial visualizations from geospatial data files. Auto-selects appropriate map projection, color scheme, and layout.
---

Create spatial visualization for: $ARGUMENTS

Follow these steps:

1. **Parse arguments**: Accept a file path (GeoPackage, Shapefile, CSV with coordinates, or GeoTIFF).

2. **Detect data type and auto-select visualization**:
   - Point data with continuous value → choropleth or proportional symbols
   - Polygon data → choropleth with appropriate classification (Natural Breaks, Quantile, or Equal Interval)
   - Raster data → pseudocolor map with appropriate colormap
   - Regression coefficients → diverging colormap centered at 0
   - Residuals → diverging or sequential with significance markers

3. **Select projection**:
   - Global → Robinson or Mollweide
   - Continental US → Albers Equal Area (EPSG:5070)
   - Europe → ETRS89 Lambert (EPSG:3035)
   - Local/city → UTM zone for the area
   - Web display → EPSG:3857

4. **Generate the plot** using this Python code pattern:
```python
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import contextily as ctx
from pathlib import Path

# Load data
gdf = gpd.read_file("{FILE_PATH}")
# Project
gdf = gdf.to_crs("EPSG:4326")  # or appropriate CRS

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column="{COLUMN}", cmap="RdYlBu_r", legend=True,
         legend_kwds={"label": "{COLUMN}", "orientation": "horizontal"},
         ax=ax, missing_kwds={"color": "lightgray"})

# Add basemap if appropriate
try:
    ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron)
except:
    pass

ax.set_title("{TITLE}", fontsize=14, fontweight="bold")
ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("{OUTPUT_PATH}", dpi=300, bbox_inches="tight")
```

5. **Save output**: Save to `output/figures/{filename}_{timestamp}.png` at 300 DPI.

6. **Report**: Show the file path to the saved figure and describe key spatial patterns visible in the map.
