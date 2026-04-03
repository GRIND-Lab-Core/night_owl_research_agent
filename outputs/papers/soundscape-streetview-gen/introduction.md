---
section: introduction
score: 8.1
attempt: 1
status: ACCEPTED
---

# 1. Introduction

The auditory and visual experiences of urban space are deeply coupled: a pedestrian who hears
the rumble of traffic expects a different scene from one who hears birdsong, yet no
computational framework has exploited this coupling to synthesize street-level imagery directly
from soundscape descriptions. This gap has practical consequences. Urban noise exposure affects
more than one billion people worldwide, and WHO Europe (2018) estimates that at least one million
disability-adjusted life years are lost annually in Western Europe alone to traffic-related noise
— yet urban planners still lack tools that translate acoustic intervention proposals into
visualizable street-level scenes. Street-level imagery, meanwhile, has become the backbone of
urban analytics (Biljecki & Ito, 2021), but geographic coverage remains uneven: Mapillary's
1.5-billion-image corpus is dense in North American and European city centers yet sparse across
large portions of the Global South, creating systematic data gaps precisely where acoustic
surrogate data could substitute most usefully.

## 1.1 The Acoustic-Visual Gap in Urban Digital Twins

Two parallel research traditions address parts of this problem without converging. The urban
soundscape literature, anchored in ISO 12913-1 (2014), has produced validated perceptual
frameworks and large annotated datasets — most notably ARAUS (Ooi et al., 2022), which provides
25,440 human responses mapping audio features to pleasantness, eventfulness, and A-weighted SPL
— and has established that soundscape perception co-varies systematically with the visual
environment (Kang et al., 2018; Qin et al., 2019). Separately, the generative AI literature has
demonstrated that audio embeddings can condition realistic image synthesis: Sound2Scene (Sung-Bin
et al., 2023) achieved FID 28.3 on VEGAS environmental sounds, and latent diffusion models
(Rombach et al., 2022) with ControlNet spatial adapters (Zhang & Agrawala, 2023) now support
rich multimodal conditioning. Open cross-modal encoders such as CLAP (Wu et al., 2023) and
ImageBind (Girdhar et al., 2023) provide shared audio-visual representation spaces suitable for
conditioning diffusion decoders.

Despite this convergence of enabling components, no published system combines ISO 12913
perceptual descriptors with generative image synthesis, nor does any GeoAI synthesis framework
incorporate acoustic conditioning. Two editorial assessments in the target community make this
gap explicit. Biljecki & Ito (2021), reviewing 600+ street-view analytics papers, identified
acoustic-visual fusion as an unexplored direction in urban visual intelligence. Biljecki et al.
(2024), surveying GeoAI more broadly in the Annals of the American Association of Geographers,
repeated the call, naming acoustic-visual generation as a key unaddressed opportunity. The gap
persists: the closest existing GeoAI synthesis paper (Mai et al., 2023) conditions a diffusion
model on OSM metadata for multi-city street-view generation but includes no acoustic channel.
Existing audio-to-image systems (Sung-Bin et al., 2023; Wu et al., 2023) train on general
sound benchmarks with no geographic framework, no ISO 12913 conditioning, and no spatial
regression analysis.

## 1.2 Limitations of Existing Work

Three methodological limitations characterize the current state of the art. First, every
audio-to-image generation system that has been benchmarked — including Sound2Scene, Sound2Vision,
and SonicDiffusion — treats audio as an abstract embedding with no geographic context. Second,
GeoAI synthesis systems such as Mai et al. (2023) demonstrate cross-city generalization via
spatial metadata but have not incorporated acoustic modality. Third, when spatially varying
relationships between urban form and acoustic environment have been studied with appropriate
methods — for instance, Fan et al. (2020) applied geographically weighted regression (GWR) to
London soundscape data and found GWR R² = 0.71 versus OLS R² = 0.54, with residual Moran's I
reduced to 0.08 after spatial adjustment — these spatial regression tools have never been
applied to generation quality metrics. No paper reports Fréchet Inception Distance, LPIPS, or
SSIM as spatially varying dependent variables explainable by urban form covariates (Wei et al.,
2025 is the sole precedent using GWR on diffusion quality, but on satellite imagery with no
acoustic conditioning). Multiscale geographically weighted regression (MGWR; Fotheringham et al.,
2017), which allows each predictor to operate at its own spatial scale, is also absent from the
generative GeoAI literature.

## 1.3 Contributions

This paper makes three principal contributions:

1. **SoundScape-ControlNet**: the first latent diffusion framework conditioned on ISO 12913
   acoustic descriptors (pleasantness, eventfulness, A-weighted SPL) combined with OSM auxiliary
   spatial covariates (land use, building density, road hierarchy). The architecture implements a
   dual-path ControlNet — a local spatial path via zero-conv adapters and a global acoustic
   path via cross-attention injection of CLAP embeddings augmented with ISO 12913 predictions —
   trained and evaluated on Mapillary street-level imagery across three cities.

2. **Spatially varying generation quality analysis**: the first application of OLS, GWR, and
   MGWR to explain geographic variation in per-cell median LPIPS as a spatially varying
   dependent variable, with Moran's I reported for residuals of all three models, revealing the
   multi-scale acoustic and morphological drivers of generation fidelity.

3. **Multi-city GeoAI evaluation with zero-shot transfer**: a rigorous cross-city benchmark
   across New York City (UTM Zone 18N, EPSG:32618), London (UTM Zone 30N, EPSG:32630), and
   Singapore (UTM Zone 48N, EPSG:32648), including a zero-shot transfer experiment from
   NYC + London to Singapore that quantifies the contribution of OSM spatial conditioning to
   cross-city robustness.

## 1.4 Research Questions

The study addresses three research questions drawn directly from the gap structure:

- **RQ1**: Can urban soundscape features — audio embeddings, A-weighted SPL, and ISO 12913
  perceptual descriptors — serve as effective conditioning signals for generating realistic
  street-level imagery via latent diffusion, and does structured ISO 12913 conditioning
  improve FID by ≥ 10% over raw audio embeddings?
- **RQ2**: Which auxiliary spatial inputs (OSM land use, GHS-BUILT-S building density, road
  hierarchy, sky view factor, green view index) most improve generation fidelity when fused
  with soundscape conditioning in the dual-path architecture?
- **RQ3**: How does geographic context (urban morphology, city type, regional acoustic
  character) spatially modulate generation quality, and can OLS/GWR/MGWR capture these
  spatially varying relationships, with MGWR reducing residual Moran's I to ≤ 0.08?

## 1.5 Paper Organization

Section 2 reviews the three relevant literature clusters — cross-modal audio-visual generation,
GeoAI street-level synthesis, and urban soundscape perception — and positions SoundScape-ControlNet
against the closest prior work. Section 3 details the study areas, datasets, dual-path
architecture, and OLS/GWR/MGWR spatial analysis design. Section 4 reports generation fidelity
results, ablation experiments, and the MGWR spatial decomposition of per-cell LPIPS. Section 5
interprets findings against prior benchmarks, addresses limitations, and identifies practical
applications for urban planning and acoustic gap-filling. Section 6 concludes with numbered
contributions and five actionable directions for future work.
