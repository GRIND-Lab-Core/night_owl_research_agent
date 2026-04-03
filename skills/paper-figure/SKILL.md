---
name: paper-figure
description: Generates spatial figures and tables for paper sections. Calls geo_benchmark/evaluation/visualize.py for standard geo plots (choropleth maps, coefficient maps, model comparison tables). Enforces geo cartographic conventions (scale bar, north arrow, legend, inset map).
tools: Bash, Read, Write
---

# Skill: paper-figure

You generate all figures and tables for a geo/RS/GIScience paper. You call Python visualization tools — you decide what type of figure is needed and what data to use.

---

## Phase 1: Build Figure Plan

Read `memory/figure_plan.md` (from skill `paper-plan`). If not yet written, infer from `memory/outline.md` Results and Methods sections.

Standard figures for a spatial regression paper:
| Figure | Type | Source |
|---|---|---|
| Study area map | Choropleth/point map | Study area shapefile + data |
| Model comparison | Bar chart or table | geo_benchmark/results/ |
| Local R² map | Choropleth | GWR/MGWR results JSON |
| Coefficient map | Choropleth | MGWR per-variable coefficients |
| Residual map + LISA | Bivariate map | OLS/GWR residuals + spatial weights |

---

## Phase 2: Generate Each Figure

Call the visualization tool for each figure. Decide which arguments to pass based on the figure type and available data.

**Study area map:**
```bash
python geo_benchmark/evaluation/visualize.py \
  --type study_area \
  --shapefile [path/to/boundary.geojson] \
  --data [path/to/data.csv] \
  --lat-col [lat] --lon-col [lon] \
  --output outputs/figures/fig1_study_area.png
```

**Model comparison (bar chart + table):**
```bash
python geo_benchmark/evaluation/visualize.py \
  --type comparison_table \
  --results geo_benchmark/results/ \
  --metrics r2 aicc rmse morans_i \
  --output outputs/figures/fig2_model_comparison.png
```

**Local R² choropleth (GWR or MGWR):**
```bash
python geo_benchmark/evaluation/visualize.py \
  --type local_r2_map \
  --results geo_benchmark/results/gwr_results.json \
  --shapefile [path] \
  --output outputs/figures/fig3_local_r2.png
```

**Coefficient map (specify variable name):**
```bash
python geo_benchmark/evaluation/visualize.py \
  --type coefficient_map \
  --results geo_benchmark/results/mgwr_results.json \
  --variable [predictor_col] \
  --shapefile [path] \
  --output outputs/figures/fig4_coef_[var].png
```

**Residual map:**
```bash
python geo_benchmark/evaluation/visualize.py \
  --type residual_map \
  --results geo_benchmark/results/ols_results.json \
  --shapefile [path] \
  --output outputs/figures/fig5_residuals.png
```

If `visualize.py` does not support a required plot type, write a short Python script to `outputs/figures/scripts/fig[N]_plot.py` and run it with `python outputs/figures/scripts/fig[N]_plot.py`. Keep scripts focused (< 50 lines each).

---

## Phase 3: Validate Cartographic Conventions

For every map figure, verify (or note as missing for manual addition):
- [ ] Scale bar present
- [ ] North arrow present
- [ ] Legend with units
- [ ] Inset map showing study area location in regional context
- [ ] CRS labeled in caption (e.g., "UTM Zone 10N / EPSG:32610")

Call `visualize.py` with `--add-cartographic-elements` if the flag is supported; otherwise document missing elements in `outputs/figures/captions.md` for manual addition before submission.

---

## Phase 4: Write Figure Captions

For each figure, write a self-contained caption to `outputs/figures/captions.md`:

```markdown
**Figure N.** [What is shown]. [Data source]. [CRS if a map].
[Key finding or pattern visible in the figure.]
```

Good example:
> **Figure 3.** Local R² values from MGWR applied to county-level PM2.5 exposure in CONUS (n=3,109). Projected to Albers Equal Area (EPSG:5070). Local R² is highest in the southeastern US (median=0.74) and lowest in the Great Plains (median=0.41), indicating that the model explains more variance in areas with stronger spatial covariate structure.

Bad example (too vague):
> **Figure 3.** Local R² values from MGWR.

---

## Outputs

- `outputs/figures/fig[N]_[name].png` — all figure files
- `outputs/figures/captions.md` — self-contained captions for all figures
- `outputs/figures/scripts/` — any custom plot scripts written
- Update `memory/outline.md` Figures section with paths and caption status
