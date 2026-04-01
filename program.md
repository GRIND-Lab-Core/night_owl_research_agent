# Research Program Brief — GeoResearchAgent-247

> **Instructions**: Fill in this file to direct the research agent. It mirrors
> the role of `program.md` in Karpathy's autoresearch — the agent reads this
> at the start of every session to understand what to work on and how to
> evaluate success.
>
> For API mode: run `python launch.py --backend api`
> For Claude Code mode: open this folder in Claude Code and run `/full-pipeline`

---

## 1. Research Topic

```
[FILL IN: Describe the research topic in 1-3 sentences]

Examples:
  Investigating multi-scale geographically weighted regression (MGWR) for
  identifying spatial drivers of urban heat island intensity across 50 US
  cities, using Landsat LST, impervious surface fraction, and NDVI (2015-2024).

  A GeoAI framework for real-time wildfire damage assessment integrating
  Sentinel-1 SAR change detection with foundation model embeddings, evaluated
  across the 2020-2023 California fire seasons.

  Spatial econometric analysis of environmental health disparities in PM2.5
  exposure across census tracts in the US Southeast, incorporating
  socioeconomic vulnerability indices and green space accessibility.
```

**Current Topic:**
> _Not yet specified. Edit this field._

---

## 2. Target Venue

```
[FILL IN: Journal or conference name, impact factor if known]

Geoscience:
  - Geophysical Research Letters (GRL) — IF 4.0
  - Journal of Geophysical Research: Atmospheres — IF 3.8
  - Earth and Planetary Science Letters — IF 4.4
  - Nature Geoscience — IF 18.3

Remote Sensing:
  - Remote Sensing of Environment (RSE) — IF 13.5
  - ISPRS Journal of Photogrammetry and Remote Sensing — IF 12.7
  - IEEE Transactions on Geoscience and Remote Sensing — IF 8.2
  - International Journal of Applied Earth Observation and Geoinformation — IF 7.5

GIScience:
  - International Journal of Geographical Information Science (IJGIS) — IF 4.3
  - Annals of the American Association of Geographers — IF 4.0
  - Transactions in GIS — IF 2.8
  - Computers, Environment and Urban Systems — IF 6.0

Interdisciplinary:
  - Nature Communications — IF 16.6
  - Environmental Health Perspectives (EHP) — IF 10.1
  - Science of the Total Environment — IF 8.2
  - ACM SIGSPATIAL (conference)
```

**Current Target:** _Not yet specified._

---

## 3. Research Objectives

List 3-5 specific, measurable objectives:

1. _[Objective 1]_
2. _[Objective 2]_
3. _[Objective 3]_

---

## 4. Key Research Questions

1. _[RQ1]_
2. _[RQ2]_
3. _[RQ3]_

---

## 5. Domain Focus

Select all that apply (mark with ✓):

- [ ] **GeoAI** — spatial deep learning, foundation models, place embeddings, geo-CV
- [ ] **Geophysics / Earth Systems** — geodynamics, seismology, atmospheric, hydrology
- [ ] **Remote Sensing** — SAR, optical, hyperspectral, LiDAR, change detection
- [ ] **GIScience / Spatial Statistics** — GWR, MGWR, spatial econometrics, geostatistics
- [ ] **Disaster Resilience** — early warning, damage assessment, recovery monitoring, equity
- [ ] **Environmental Health** — air quality, flood risk, heat islands, environmental justice
- [ ] **Urban Analytics** — city-scale spatial analysis, urban growth, accessibility
- [ ] **Social Sensing** — social media, crowdsourced data, VGI

---

## 6. Constraints and Scope

```
[FILL IN: Any constraints the paper must satisfy]

Examples:
  - Maximum 8,000 words for the target journal
  - Must use only open-access datasets (no proprietary data)
  - Must include a case study in [specific region or bounding box]
  - Methodology must be reproducible without GPU cluster
  - Literature review: 2019-2026 papers only
  - All spatial analysis must use EPSG:4326 / local UTM
  - GeoBenchmark baseline comparison required (OLS / GWR / MGWR)
```

**Constraints:**
> _Not yet specified._

---

## 7. Geographic Scope

```
[FILL IN: Study area — region, country, bounding box, or "global"]

Examples:
  - Contiguous United States (CONUS), EPSG:5070
  - Pearl River Delta, China (bbox: 112°E–115°E, 21°N–24°N)
  - Sub-Saharan Africa (30 countries)
  - Global (all continents)
```

**Study Area:** _Not yet specified._

---

## 8. Datasets

List any pre-identified datasets (open-source preferred):

```
[FILL IN: dataset name, source, spatial resolution, temporal coverage]

Examples:
  - Sentinel-2 L2A (ESA Copernicus), 10 m, 2017-present
  - MODIS Land Surface Temperature (MOD11A1), 1 km, 2000-present
  - US Census ACS 5-year estimates (2019-2023), county/tract level
  - GADM administrative boundaries (gadm.org), v4.1
  - OpenStreetMap (Overpass API), various features
  - EPA AQS air quality data, monitoring station level
```

- _[Dataset 1]_
- _[Dataset 2]_
- _[Dataset 3]_

---

## 9. Preliminary References (Seed Papers)

List key papers the agent should start with:

```
[FILL IN: arXiv IDs, DOIs, or titles of seed papers]
```

- _[Seed paper 1]_
- _[Seed paper 2]_
- _[Seed paper 3]_

---

## 10. Success Metric (Autoresearch-Style)

The agent scores each paper section 0–10 on five dimensions:

| Dimension | Weight | Description |
|---|---|---|
| Novelty | 30% | How original is the contribution? Is the problem formulation, method, or finding genuinely new? |
| Rigor | 25% | Is the methodology sound, reproducible, and spatially valid? Are baselines included? |
| Literature coverage | 20% | Are key papers in the domain cited? Is the synthesis accurate and current (≥2020)? |
| Clarity | 15% | Is the writing clear, well-structured, and free of vague claims? |
| Impact | 10% | Does this matter to the field? Does it have practical or policy implications? |

**Acceptance threshold:** ≥ 7.5 / 10 overall before finalizing

**GeoBenchmark threshold (for quantitative papers):** MGWR must be compared against OLS and GWR baselines; Moran's I of residuals must be reported.

---

## 11. Paper Type

Select one:

- [ ] Full research article (empirical, original data + methods + results)
- [ ] Review / survey paper (systematic literature synthesis)
- [ ] Methods paper (proposing a new algorithm or framework)
- [ ] Data paper (describing a new dataset)
- [ ] Commentary / perspective (short opinion or synthesis)
- [ ] Short communication / letter

---

## 12. Current Status

```
Stage:                   [not started | lit-review | gap-analysis | outlining |
                          writing | reviewing | final]
Last updated:            [YYYY-MM-DD]
Current section:         [section name or "—"]
Overall score so far:    [X/10 or "—"]
Sections accepted:       [0 / 7]
```

**Stage:** _Not started_
**Last updated:** _—_
