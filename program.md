# Research Program Brief — GeoResearchAgent-247

> **Instructions**: Fill in this file to direct the research agent.
>
> For API mode: run `python launch.py --backend api`
> For Claude Code mode: open this folder in Claude Code and run `/full-pipeline`

---

## 1. Research Topic

```
A GeoAI framework for generating realistic street-level imagery conditioned on
urban soundscapes and auxiliary spatial data. Using acoustic features (soundscape
descriptors, audio embeddings from geotagged audio) together with auxiliary
inputs (OpenStreetMap land use, building density, road type, time-of-day) as
conditioning signals for a latent diffusion model to synthesize plausible
street-level views. The study evaluates generation fidelity across diverse
urban environments and uses GWR/MGWR to characterize spatially varying
relationships between acoustic-spatial inputs and visual scene realism.
```

**Current Topic:**
> Soundscape-conditioned street-level image generation: a GeoAI framework using
> urban acoustic features and auxiliary spatial data to synthesize realistic
> street-level imagery via latent diffusion models.

---

## 2. Target Venue

```
Primary: ISPRS Journal of Photogrammetry and Remote Sensing — IF 12.7
Backup:  Computers, Environment and Urban Systems (CEUS) — IF 6.0
Alt:     IEEE Transactions on Geoscience and Remote Sensing — IF 8.2
```

**Current Target:** ISPRS Journal of Photogrammetry and Remote Sensing — IF 12.7

---

## 3. Research Objectives

1. Design a cross-modal conditional generation framework that synthesizes street-level imagery from urban soundscape embeddings + auxiliary spatial inputs.
2. Identify which combinations of acoustic features and spatial covariates (land use, morphology, time-of-day) maximize generation fidelity (FID, SSIM, LPIPS).
3. Quantify spatially varying generation quality using GWR/MGWR, revealing geographic factors that strengthen or weaken sound-vision correspondence.
4. Evaluate framework across ≥ 3 cities with contrasting urban morphologies (dense grid, organic medieval, tropical high-density) to test generalizability.
5. Demonstrate downstream application: filling gaps in street-level image coverage using acoustic + OSM data as surrogates.

---

## 4. Key Research Questions

1. Can urban soundscape features (audio embeddings, A-weighted SPL, soundscape descriptors) serve as effective conditioning signals for generating realistic street-level imagery via latent diffusion?
2. Which auxiliary spatial inputs (OSM land use, building footprint density, road hierarchy, sky view factor, green view index) most improve generation fidelity when combined with soundscape conditioning?
3. How does geographic context (urban morphology, city type, regional acoustic character) spatially modulate generation quality, and can GWR/MGWR capture these spatially varying relationships?

---

## 5. Domain Focus

- [✓] **GeoAI** — spatial deep learning, foundation models, place embeddings, geo-CV
- [ ] **Geophysics / Earth Systems**
- [ ] **Remote Sensing** — scene synthesis, image generation
- [✓] **GIScience / Spatial Statistics** — GWR, MGWR, spatial econometrics
- [ ] **Disaster Resilience**
- [✓] **Environmental Health** — urban noise, acoustic environment quality
- [✓] **Urban Analytics** — city-scale spatial analysis, urban morphology
- [ ] **Social Sensing**

---

## 6. Constraints and Scope

```
- Maximum 10,000 words (ISPRS)
- Open-access data only (no proprietary datasets)
- Street-level imagery ground truth: Mapillary open dataset (CC-BY-SA)
  (avoid Google Street View API for reproducibility; use Mapillary instead)
- Acoustic data: SoundingEarth (geotagged audio), Noise-Planet (crowdsourced),
  OpenSoundscape or FreeSound geotagged clips
- Generative model: Stable Diffusion (Runway/CompVis, open weights) with
  ControlNet-style conditioning, or similar open diffusion model
- Audio encoder: ImageBind (Meta, open weights) or CLAP (LAION, open weights)
- Spatial analysis: OLS + GWR + MGWR comparison required (geo_benchmark baseline)
- Geographic scope: ≥ 3 cities
- All spatial analysis projected to local UTM before distance computation
- Moran's I of residuals required for all regression models
- Reproducible without proprietary API access
- Literature: 2019-2026 preferred
```

**Constraints:**
> Open data only; Mapillary for imagery ground truth; Stable Diffusion + ControlNet;
> OLS/GWR/MGWR spatial analysis; ≥ 3 cities; max 10,000 words.

---

## 7. Geographic Scope

```
Multi-city study across ≥ 3 cities with contrasting urban morphologies:
  - New York City, USA (dense grid, high acoustic diversity, EPSG:32618)
  - London, UK (irregular organic + modern, EPSG:32630)
  - Singapore (tropical high-density compact city, EPSG:32648)
  Optional: Paris, Amsterdam, or Tokyo for extended analysis
```

**Study Area:** Multi-city (NYC · London · Singapore) — local UTM per city

---

## 8. Datasets

```
Street-level imagery (ground truth / training):
  - Mapillary open dataset (CC-BY-SA), global coverage, 1.5B+ images
  - Amsterdam OpenStreetView (high-res, Netherlands, open license)

Acoustic / soundscape data:
  - SoundingEarth dataset — geotagged field recordings, global
    (Heittola et al.; ~50K georeferenced audio clips)
  - Noise-Planet / NoiseCapture — crowdsourced urban noise, global
  - DCASE 2023/2024 soundscape challenge datasets (annotated urban audio)
  - FreeSound geotagged clips (via FreeSound API, open license)

Audio encoders (open weights):
  - CLAP (LAION-AI, open weights, HuggingFace) — audio-text embeddings
  - ImageBind (Meta, open weights) — audio-visual-text joint embedding

Generative model backbone:
  - Stable Diffusion v2.1 or SDXL (CompVis/Runway, open weights)
  - ControlNet (lllyasviel, open weights) — spatial conditioning adapter

Urban morphology / spatial covariates:
  - OpenStreetMap (Overpass API) — land use, buildings, roads, POIs
  - GADM administrative boundaries v4.1
  - GHS-BUILT-S (100 m building density, ESA/JRC, open)
  - Global Surface Water / NDVI (Landsat/Sentinel via GEE or open portals)

Evaluation metrics:
  - FID (Frechet Inception Distance) — generation fidelity
  - SSIM / LPIPS — structural + perceptual similarity
  - Semantic segmentation overlap (DeepLab v3+) — scene class accuracy
```

- Mapillary open dataset (CC-BY-SA street-level imagery ground truth)
- SoundingEarth + Noise-Planet (geotagged acoustic data)
- CLAP / ImageBind audio encoders (open weights)
- Stable Diffusion + ControlNet (open weights generative backbone)
- OpenStreetMap + GADM + GHS-BUILT-S (auxiliary spatial covariates)

---

## 9. Preliminary References (Seed Papers)

```
Key seed topics:
  - Conditional image generation / ControlNet (Zhang & Agrawala, 2023)
  - Cross-modal audio-visual learning (Owens et al.; Girdhar et al. ImageBind)
  - Urban soundscape mapping and perception (ISO 12913; Kang et al.)
  - Street-level imagery for urban analytics (Place Pulse; Dubey et al.)
  - GeoAI for scene synthesis / image generation
  - GWR/MGWR for urban spatial analysis (Fotheringham et al.)
  - Audio-conditioned image generation (sound2sight, audio-driven diffusion)
```

- ControlNet: Adding Conditional Control to Text-to-Image Diffusion Models (Zhang & Agrawala, ICCV 2023)
- ImageBind: One Embedding Space to Bind Them All (Girdhar et al., CVPR 2023)
- CLAP: Learning Audio Concepts From Natural Language Supervision (LAION, 2022)
- Soundscape ecology and urban sound mapping (Kang et al., 2018 + recent)
- StreetScore / Place Pulse: large-scale street-level urban perception

---

## 10. Success Metric (Autoresearch-Style)

| Dimension | Weight | Description |
|---|---|---|
| Novelty | 30% | Cross-modal soundscape→image generation is a genuinely new direction |
| Rigor | 25% | Quantitative FID/SSIM + spatial GWR/MGWR analysis, open reproducible pipeline |
| Literature coverage | 20% | Key generative AI, soundscape, and GeoAI papers cited (≥15, majority ≥2020) |
| Clarity | 15% | Active voice, specific numbers, clear problem formulation |
| Impact | 10% | Urban planning visualization, acoustic gap-filling, privacy-preserving mapping |

**Acceptance threshold:** ≥ 7.5 / 10 overall before finalizing

**geo_benchmark threshold:** MGWR vs OLS vs GWR; Moran's I of residuals reported.

---

## 11. Paper Type

- [✓] Full research article (empirical, original data + methods + results)

---

## 12. Current Status

```
Stage:                   not started
Last updated:            2026-04-01
Current section:         —
Overall score so far:    —
Sections accepted:       0 / 7
```

**Stage:** _Not started_
**Last updated:** _2026-04-01_
