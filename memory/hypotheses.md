# Research Hypotheses
Date: 2026-04-02
Topic: Soundscape-conditioned street-level image generation via latent diffusion (GeoAI framework)
Source gaps: memory/gap-analysis.md (11 gaps, composite scores 3.30–4.80)
Source synthesis: memory/synthesis-2026-04-01.md (52 papers, 2016–2026)
Source program: program.md (RQ1–RQ3, objectives 1–5, NYC/London/Singapore scope)
Agent: hypothesis-generator

---

## H1: ISO 12913-Conditioned Latent Diffusion Outperforms Raw-Embedding Baselines for Urban Street-Level Image Synthesis

**Statement:** A Stable Diffusion v2.1 + ControlNet model conditioned on a structured acoustic
vector combining CLAP/ImageBind audio embeddings with ISO 12913 perceptual descriptors
(pleasantness, eventfulness) and A-weighted SPL will achieve FID ≤ 30 on held-out Mapillary
test images and will show a statistically significant FID reduction ≥ 10% compared to a
CLAP-only baseline and ≥ 15% compared to a text-only baseline, across all three study cities
(NYC, London, Singapore). The hypothesis is that structured perceptual priors provide
semantically richer conditioning than raw spectral embeddings alone, because ISO 12913
dimensions are validated cross-modal signals that co-vary with visual scene semantics.

**Rationale:** Gap M1 (composite 4.80) documents the complete absence of ISO 12913 descriptors
as generative conditioning signals across all reviewed audio-to-image generation papers
(Sound2Scene FID 28.3, Sound2Vision FID ~24, SonicDiffusion). Kang et al. (2018) and
Qin et al. (2019) established cross-modal coupling between soundscape pleasantness/eventfulness
and visual scene perception. The ARAUS dataset (Ooi et al. 2022; 25,440 ISO 12913 responses)
enables training a lightweight acoustic-to-perception head. Gap T2 (composite 4.35) separately
identifies that ISO 12913 scores have never been inverted as generative priors: the entire
T2 literature treats them as endpoints, not inputs. This hypothesis inverts that direction,
directly answering RQ1: can urban soundscape features serve as effective conditioning signals
for realistic street-level image synthesis?

**Test:**
Three-arm ablation on a held-out spatially stratified test set (500 locations per city):
- Arm A — text-prompt-only ControlNet baseline
- Arm B — CLAP 512-dim embedding only (no ISO 12913 descriptors)
- Arm C — CLAP 512-dim + ISO 12913 [pleasantness, eventfulness, LAeq] concatenated vector (full proposed model)
Primary metrics: FID (Fréchet Inception Distance, Inception v3 activations, ≥ 500 generated vs. real images per city).
Secondary: SSIM, LPIPS, semantic segmentation class overlap (DeepLab v3+ on generated images).
Statistical test: Paired Wilcoxon signed-rank test on per-image LPIPS scores (Arm C vs. Arm B);
Bonferroni correction for 3-city × 2-comparison multiple testing (α = 0.05/6).
Rejection criterion: if Arm C FID improvement over Arm B < 5% and Wilcoxon p > 0.05 in ≥ 2 cities,
the ISO 12913 conditioning adds no statistically significant benefit.

**Datasets:**
- Mapillary open dataset (CC-BY-SA): ground-truth street-level imagery, NYC/London/Singapore;
  target ≥ 5,000 images per city, spatially stratified by OSM land use class and road hierarchy
- SoundingEarth (~50,000 geotagged audio clips): matched to Mapillary images by geographic
  proximity ≤ 50 m (UTM per city); primary audio source for CLAP encoding
- Noise-Planet NoiseCapture: crowdsourced LAeq measurements; kriged to 500 m grid (ordinary
  kriging, UTM CRS) as the A-weighted SPL conditioning channel
- ARAUS (Ooi et al. 2022): 25,440 ISO 12913 pleasantness/eventfulness annotations used to
  train the acoustic-to-perception prediction head (MLP applied at inference to SoundingEarth audio)
- OSM via Overpass API: land use class labels for spatial stratification of train/test split

**Model configuration:**
- Backbone: Stable Diffusion v2.1 (CompVis open weights, 512×512 resolution)
- Conditioning adapter: ControlNet zero-conv architecture (lllyasviel open weights)
- Audio encoder: CLAP (LAION-AI, laion/larger_clap_music_and_speech, HuggingFace, 512-dim)
- ISO 12913 head: 3-layer MLP (hidden 256) trained on ARAUS to predict pleasantness,
  eventfulness, LAeq from CLAP embeddings; outputs concatenated with CLAP embedding
  (total conditioning vector: 515 dim), projected via linear layer to SD hidden dim 1024,
  injected via cross-attention into all 12 UNet transformer blocks
- Training: LoRA fine-tune (r=16) on cross-attention layers only; SD backbone frozen;
  AdamW lr=1e-4, 50K steps, batch 16, cosine LR decay, 1K warmup steps
- CRS: all spatial matching in local UTM (NYC EPSG:32618, London EPSG:32630, Singapore EPSG:32648)

**Expected result:** Arm C FID ≤ 30 pooled; FID improvement ≥ 10% over Arm B and ≥ 15%
over Arm A. SSIM improvement ≥ 0.05 absolute for Arm C vs. B. Semantic segmentation class
overlap (road, vegetation, building, sky) ≥ 5 percentage points higher in Arm C vs. B.
NYC and London expected to show stronger ISO 12913 gains than Singapore due to denser ARAUS-
compatible acoustic annotation coverage.

**geo_benchmark task:** Partial — FID/SSIM/LPIPS are computed outside geo_benchmark via the
generation evaluation pipeline; OLS/GWR/MGWR spatial analysis of per-location FID scores
(as dependent variable) is directly runnable via geo_benchmark/run_benchmark.py after metrics
are aggregated to the spatial grid.

**Novelty:** 5/5 — ISO 12913 descriptors as generative conditioning are entirely absent from
all 52 reviewed papers; this combination is unambiguously new.
**Feasibility:** 4/5 — All components are open-access and open-weight; main technical
challenge is geographic co-registration of SoundingEarth audio with Mapillary images at ≤ 50 m.
**Alignment:** 5/5 — Directly and precisely answers RQ1; constitutes the paper's core methodological contribution.
**Measurability:** 5/5 — FID, SSIM, LPIPS are fully specified with concrete thresholds;
Wilcoxon test with Bonferroni correction provides a well-defined falsification procedure.
**Impact:** 5/5 — Establishes the first ISO 12913-conditioned generative model; enables
"design by soundscape" for urban planners; privacy-preserving mapping alternative;
publishable as primary ISPRS contribution.

**Composite: 4.80**
**Decision: RECOMMENDED**

---

## H2: Dual-Path ControlNet Combining Local OSM Spatial Controls and Global Soundscape Embedding Achieves Lower FID Than Single-Path Baselines

**Statement:** A dual-path ControlNet architecture that injects (i) OSM-derived local spatial
features — land use rasters, GHS-BUILT-S building density, road hierarchy — via a spatial
zero-conv adapter, and (ii) CLAP + ISO 12913 soundscape embedding via a global cross-attention
pathway, will achieve FID ≥ 8% lower than either path in isolation and ≥ 12% lower than a
text-only baseline, across the three-city test set. The dual-path design captures complementary
information: local OSM controls constrain scene geometry, while the acoustic global path
constrains semantic scene content (activity density, vegetation character, building type).

**Rationale:** Gap M2 (composite 4.50) identifies that no ControlNet architecture combines
local OSM spatial conditioning with a global acoustic embedding pathway. Uni-ControlNet
(Zhao et al. NeurIPS 2023) demonstrated that separating local and global conditioning
pathways improves generation coherence (FID 19.4), but tests only visual conditions with no
audio channel. Mai et al. (ISPRS 2023) showed OSM metadata conditioning alone enables
plausible urban street generation with zero-shot cross-city transfer — but without acoustic
signals. The proposed dual-path architecture bridges these two partial solutions.
The architectural motivation is spatial-scale divergence: OSM features change at street-segment
scale (~100 m), while soundscape character is neighborhood-scale (~500 m); a dual-path design
allows each signal to condition at its natural scale. This directly answers RQ2: which
auxiliary spatial inputs most improve generation fidelity when combined with soundscape conditioning?

**Test:**
Four-arm ablation, same Mapillary held-out test sets as H1:
- Arm A — text-only baseline
- Arm B — local OSM spatial path only (no acoustic global path)
- Arm C — global CLAP + ISO 12913 path only (no OSM local path) — same as H1 Arm C
- Arm D — dual-path: OSM local + acoustic global combined (proposed)
Primary metric: FID per city and pooled.
Secondary: SSIM, LPIPS, semantic segmentation class overlap (DeepLab v3+).
Hypothesis confirmed if Arm D FID is ≥ 8% lower than the better single-path arm (B or C)
in ≥ 2 of 3 cities and improvement is statistically significant (bootstrap 95% CI on FID
does not overlap with best single-path FID CI).
Additional test: MGWR fitted to per-location FID scores for all four arms separately to
determine whether the dual-path advantage is spatially uniform or concentrated in
specific morphological zones.

**Datasets:**
- Mapillary: same ground-truth imagery as H1
- OpenStreetMap (Overpass API): land use polygons (7 classes), building footprints, road
  hierarchy; rasterized to 256×256 at ~5 m/pixel in local UTM per city
- GHS-BUILT-S (100 m, ESA/JRC open): building density surface, resampled to 256×256 control
  images; projected to UTM Zone 18N (NYC EPSG:32618), 30N (London EPSG:32630), 48N (Singapore EPSG:32648)
- SoundingEarth + Noise-Planet: same acoustic pipeline as H1

**Model configuration:**
- Backbone: SD v2.1 frozen
- Local path: ControlNet zero-conv adapter; input is a 12-channel control raster encoding
  OSM land-use one-hot (7 classes) + road hierarchy (4-level ordinal) + GHS-BUILT-S density (continuous)
- Global path: cross-attention adapter from H1 (CLAP + ISO 12913 + LAeq, 515-dim vector)
- Fusion: Uni-ControlNet-style learned gating; per-resolution-level weighted sum
  at 4 UNet resolution levels (64×64, 32×32, 16×16, 8×8)
- Only adapter and gate weights trained; backbone frozen

**Expected result:** Arm D FID ≤ 23 pooled; ≥ 8% below Arm C (best expected single-path ~25).
Semantic segmentation class overlap ≥ 0.75 for primary scene classes (building, road, vegetation, sky).
Dual-path advantage expected to be largest in mixed-use zones where OSM spatial control
and acoustic environment are jointly informative; smallest in residential zones where either
path alone constrains the scene adequately.

**geo_benchmark task:** Yes — per-grid-cell FID from all four arms can be analyzed with
OLS/GWR/MGWR in geo_benchmark/run_benchmark.py to test whether dual-path advantage is
spatially uniform or heterogeneous. Results saved to geo_benchmark/results/.

**Novelty:** 5/5 — Dual-path acoustic-spatial ControlNet does not exist in any reviewed paper.
**Feasibility:** 4/5 — All code and data available; multi-path fusion engineering is non-trivial
but manageable with Uni-ControlNet as reference implementation.
**Alignment:** 5/5 — Directly and specifically answers RQ2 (which auxiliary inputs most improve fidelity).
**Measurability:** 4/5 — FID threshold and bootstrap CI test are well-defined; semantic
segmentation overlap adds a pipeline step (DeepLab v3+ inference on generated images).
**Impact:** 4/5 — Produces a reusable dual-path architecture for urban sensing tasks beyond
soundscape; architectural contribution relevant to GeoAI community.

**Composite: 4.40**
**Decision: RECOMMENDED**

---

## H3: MGWR Outperforms OLS and GWR in Explaining Spatial Variation in Generation Fidelity, with Significant AICc Improvement and Residual Moran's I Below 0.10

**Statement:** Multiscale Geographically Weighted Regression (MGWR) with adaptive bisquare
kernel applied to per-grid-cell generation FID scores (dependent variable) against acoustic
and urban morphology covariates (LAeq, CLAP embedding PCA components, GHS-BUILT-S building
density, OSM road hierarchy index, NDVI proxy, ISO 12913 pleasantness estimate) will
outperform both OLS (AICc improvement ≥ 10 units) and standard GWR (AICc improvement ≥ 5
units) across the three-city dataset. Residual Moran's I will fall from ≥ 0.20 (OLS residuals)
to ≤ 0.08 (MGWR residuals). Building density and road hierarchy will show significantly
different optimal MGWR bandwidths, reflecting multi-scale spatial structure in the
acoustic-generation quality relationship.

**Rationale:** Gap M3 (composite 4.45) documents that GWR/MGWR has never been applied to
generative model quality metrics as a dependent variable — the entire T5 literature uses GWR
on perception scores or physical measurements, never on FID or SSIM. Wei et al. (2025) is the
sole paper combining diffusion synthesis with GWR evaluation, but uses satellite imagery with
no acoustic conditioning. Fan et al. (2020) provides the key precedent: GWR R² = 0.71 vs.
OLS R² = 0.54 for soundscape-land-use in London, with residual Moran's I = 0.08 after GWR
adjustment. Gap M4 (composite 4.10) separately notes that Moran's I has never been reported
for generative quality metrics. Together these gaps motivate treating per-location FID as a
spatially varying quantity that reflects local acoustic-morphological context. This directly
answers RQ3: how does geographic context spatially modulate generation quality, and can
GWR/MGWR capture these spatially varying relationships?

**Test:**
Three-model OLS/GWR/MGWR comparison via geo_benchmark/run_benchmark.py:
- Dependent variable: per-grid-cell FID aggregated at 250 m grid (≥ 20 Mapillary images per cell required)
- Covariates: LAeq (Noise-Planet, kriged to 250 m grid), CLAP embedding PC1–PC3 (PCA to ≥ 80% variance),
  GHS-BUILT-S building density (100 m aggregated to 250 m), OSM road hierarchy index
  (weighted mean road order per cell), NDVI proxy (Sentinel-2 or Landsat green view fraction),
  ISO 12913 pleasantness estimate (from ISO 12913 prediction head applied to SoundingEarth clips)
- ~800 grid cells per city × 3 cities = ~2,400 observations total (within MGWR ≤ 3,000 limit)
- All projections to local UTM per city; distances computed in meters, never in WGS84 degrees
- GWR: adaptive bisquare kernel, golden-section bandwidth cross-validation
- MGWR: adaptive bisquare per covariate, back-fitting convergence criterion ε < 1e-5
- Reported: AICc, adjusted R², spatial CV RMSE (leave-one-city-out), Moran's I on residuals
  (PySAL libpysal, queen contiguity weights, 999 permutations pseudo-p)
- Coefficient maps: spatially varying GWR/MGWR coefficients for building density and road
  hierarchy plotted per city via geo_benchmark/evaluation/visualize.py

Confirmation criteria: MGWR AICc < GWR AICc by ≥ 5; GWR AICc < OLS AICc by ≥ 10;
OLS residual Moran's I ≥ 0.15; MGWR residual Moran's I ≤ 0.10;
MGWR adjusted R² ≥ OLS adjusted R² + 0.15; MGWR bandwidth(building density) ≠ bandwidth(road hierarchy)
at statistical significance (MGWR bootstrap CI on bandwidth values, p < 0.05).

**Datasets:**
- Per-grid-cell FID/SSIM/LPIPS scores: output of H1/H2 generation evaluation pipeline
- GHS-BUILT-S (100 m ESA/JRC): building density, aggregated to 250 m grid
- OpenStreetMap: road network (Overpass API), building footprints; road hierarchy index
  per 250 m cell = weighted mean road classification (motorway=5, primary=4, secondary=3,
  residential=2, path=1)
- Noise-Planet NoiseCapture: LAeq point measurements; ordinary kriging to 250 m grid (UTM)
- SoundingEarth: CLAP 512-dim embeddings per clip; PCA to 3 components; kriged to 250 m grid
- GADM v4.1: city boundary masks for spatial subsetting

**Model configuration:**
- mgwr Python package (Oshan et al. 2019, open-source, PyPI)
- Adaptive bisquare kernel for both GWR and MGWR
- Subsampling: NYC ~1,200 cells, London ~1,000 cells, Singapore ~600 cells — all within
  GWR ≤ 5,000 and MGWR ≤ 3,000 limits stated in CLAUDE.md
- geo_benchmark pipeline: run_benchmark.py with --model ols gwr mgwr --kernel adaptive_bisquare
  --dependent fid_per_cell --output geo_benchmark/results/soundscape_fidelity_[city].json

**Expected result:** MGWR adjusted R² ≈ 0.65–0.72; GWR adjusted R² ≈ 0.52–0.62;
OLS adjusted R² ≈ 0.35–0.45 (consistent with Fan et al. 2020 precedent of GWR vs. OLS gap
of ~0.17 for soundscape-land-use). OLS residual Moran's I ≈ 0.25–0.35 (moderate clustering
of unexplained generation quality); MGWR residual Moran's I ≤ 0.08 (near spatial
independence). Building density bandwidth ≈ 400–800 m (local canyon effects); road hierarchy
bandwidth ≈ 2,000–5,000 m (network-level acoustic character). Interpretable spatial narrative:
high-FID zones (poor generation) cluster in high-density mixed-use areas where acoustic
environment complexity exceeds CLAP embedding capacity; low-FID zones cluster in residential
areas with coherent acoustic signatures.

**geo_benchmark task:** Yes — this hypothesis is directly and fully testable with
geo_benchmark/run_benchmark.py. Input is a CSV with grid-cell lat/lon, FID, and covariate
columns. OLS/GWR/MGWR results saved to geo_benchmark/results/ as JSON.
Moran's I computed via geo_benchmark/evaluation/metrics.py.

**Novelty:** 4/5 — Applying GWR/MGWR to generative model quality (FID/SSIM) as dependent
variable is genuinely novel; the methods themselves are established.
**Feasibility:** 5/5 — mgwr package is open-source and well-documented; FID per grid cell
is computable with ≥ 20 images; all spatial covariates are open-access; geo_benchmark
pipeline is already configured.
**Alignment:** 5/5 — Directly answers RQ3; satisfies the program.md geo_benchmark threshold
(OLS + GWR + MGWR comparison with Moran's I residuals required).
**Measurability:** 5/5 — AICc, adjusted R², and Moran's I thresholds are fully quantified;
MGWR bandwidth bootstrap CI provides a well-defined statistical test for multi-scale structure.
**Impact:** 4/5 — Produces interpretable spatial maps of where acoustic conditioning works
and fails; actionable for urban planners; introduces spatial validation standard for GeoAI
generation papers; strongly aligned with ISPRS venue expectations.

**Composite: 4.60**
**Decision: RECOMMENDED**

---

## H4: Spatial Moran's I of Per-Location Generation FID Exceeds 0.25 Before Covariate Adjustment and Falls Below 0.10 After MGWR

**Statement:** Per-location FID scores from the ISO 12913-conditioned generation model will
exhibit significant positive spatial autocorrelation before covariate adjustment
(global Moran's I > 0.25, pseudo-p < 0.01) in all three cities, reflecting the spatial
clustering of urban acoustic environment types and urban morphologies. After MGWR adjustment
using acoustic and morphology covariates, residual Moran's I will fall below 0.10 in all
three cities. LISA cluster maps will identify distinct high-FID clusters (poor generation
quality) spatially coinciding with high-density commercial or industrial zones, and low-FID
clusters (high generation quality) coinciding with residential or park-adjacent zones.

**Rationale:** Gap M4 (composite 4.10) documents that no paper in the audio-visual or
generative GeoAI literature applies Moran's I to generation quality outputs. The T5 literature
routinely reports Moran's I of regression residuals (Fan et al. 2020 achieved Moran's I = 0.08
after GWR for London soundscape data), but this convention has not crossed into the T4
(generative AI) literature. Program.md explicitly requires Moran's I of residuals for all
regression models as a geo_benchmark threshold condition. Demonstrating that FID scores are
spatially clustered and that MGWR removes this clustering provides spatial validation for the
entire framework and introduces a reproducible spatial quality diagnostic for future GeoAI
generation papers.

**Test:**
Phase 1 — Pre-adjustment Moran's I:
Global Moran's I computed on raw per-grid-cell FID (250 m cells, same grid as H3) using
queen contiguity spatial weights matrix; computed via PySAL libpysal for each city
independently and for the pooled three-city dataset.
Report: Moran's I statistic, z-score, pseudo-p value (999 permutations); also k-NN (k=8)
weights as robustness check.

Phase 2 — Post-adjustment Moran's I:
Global Moran's I on OLS, GWR, and MGWR residuals from H3 models.
Primary target: MGWR residual Moran's I < 0.10 in all three cities.

Phase 3 — LISA analysis:
Local Indicators of Spatial Association (LISA) on raw FID scores per city.
Identify HH clusters (high FID, poor generation), LL clusters (low FID, good generation),
HL and LH outliers.
Produce LISA cluster maps via geo_benchmark/evaluation/visualize.py.
Overlay with OSM land use categories to test whether HH clusters concentrate in commercial/
industrial zones (hypothesis: yes) and LL clusters in residential/park zones (hypothesis: yes).

Confirmation criteria: Moran's I(FID_raw) > 0.25 and pseudo-p < 0.01 in ≥ 2 of 3 cities;
MGWR residual Moran's I < 0.10 in ≥ 2 of 3 cities; OLS residual Moran's I > MGWR residual
Moran's I in all 3 cities.

**Datasets:**
- Per-grid-cell FID: output of H1/H2 generation evaluation pipeline aggregated to 250 m grid
- Spatial weights: queen contiguity for grid cells; k-NN (k=8) as robustness check
- OSM land use polygons: for LISA cluster overlay interpretation
- All analysis projected to local UTM per city; distances in meters

**Model configuration:**
- PySAL libpysal for spatial weights construction
- esda.Moran for global Moran's I
- esda.Moran_Local for LISA
- geo_benchmark/evaluation/metrics.py already implements Moran's I
- OLS/GWR/MGWR residuals output directly by geo_benchmark/run_benchmark.py

**Expected result:** Pre-adjustment pooled Moran's I ≈ 0.28–0.40 (strong positive
spatial autocorrelation driven by clustering of urban morphology types). Post-MGWR
Moran's I ≈ 0.05–0.10 (near spatial independence, consistent with Fan et al. 2020 target
of 0.08). LISA maps expected to show HH clusters in NYC Midtown/Downtown, London City/
Canary Wharf, Singapore CBD (all high-density commercial zones with complex multi-source
acoustic environments that challenge CLAP embedding capacity); LL clusters in residential
neighborhoods and parks.

**geo_benchmark task:** Yes — geo_benchmark/evaluation/metrics.py implements Moran's I;
OLS/GWR/MGWR residuals from geo_benchmark/run_benchmark.py feed directly into Moran's I
computation. LISA maps produced via geo_benchmark/evaluation/visualize.py.

**Novelty:** 4/5 — Moran's I applied to generative quality metrics is novel; method itself
is standard spatial statistics.
**Feasibility:** 5/5 — Moran's I is fully implemented in PySAL and geo_benchmark; no
additional data beyond H3; computationally trivial.
**Alignment:** 4/5 — Required by program.md geo_benchmark threshold; directly supports RQ3
spatial characterization; provides mandatory validation layer.
**Measurability:** 5/5 — Moran's I thresholds (> 0.25 pre, < 0.10 post) are precisely
specified; pseudo-p criterion < 0.01 is unambiguous.
**Impact:** 3/5 — Primarily methodological/validation contribution; strengthens paper rigor
at ISPRS venue; introduces a reproducible spatial quality diagnostic for the GeoAI
generation community.

**Composite: 4.20**
**Decision: CANDIDATE**

---

## H5: CLAP Audio Encoder Provides Superior Soundscape Conditioning Over ImageBind for Urban Street-Level Generation

**Statement:** CLAP (LAION-AI, trained on LAION-Audio-630K) will produce lower FID scores
than ImageBind (Meta, audio branch of 6-modality joint embedding space) when used as the
primary audio encoder in the ISO 12913-conditioned generation model, with a FID difference
≥ 5% in favor of CLAP across the three-city test set. The advantage is expected to be most
pronounced for urban sound categories (traffic, construction, crowd noise) that are more
prominent in CLAP's urban-relevant training distribution than in ImageBind's unconstrained
video-derived audio training distribution.

**Rationale:** Program.md Section 6 lists both CLAP and ImageBind as permitted audio encoders
without specifying a preference. Wu et al. (2023) established CLAP as state-of-the-art for
audio-text retrieval and zero-shot audio classification; its training corpus (LAION-Audio-630K,
633K audio-text pairs) explicitly includes urban sound categories. ImageBind (Girdhar et al.
CVPR 2023) achieves zero-shot audio-to-image retrieval top-1 ~42% but optimizes for
audio-visual correspondence across six modalities without urban soundscape specificity.
For the purpose of conditioning urban street-level image synthesis, CLAP's domain-specific
training is theoretically advantageous; however, ImageBind's direct visual embedding
alignment might compensate. This is a tractable model selection experiment that produces
an evidence-based encoder recommendation for the community and answers a component of
RQ1 and RQ2 (which encoder provides more effective acoustic conditioning).

**Test:**
Two-arm encoder comparison within the full conditioning framework (H1 Arm C configuration):
- Arm A — full model with CLAP encoder (laion/larger_clap_music_and_speech, 512-dim)
- Arm B — full model with ImageBind audio encoder (facebookresearch/imagebind, 1024-dim
  projected to 512-dim via learned linear layer before cross-attention injection)
Same Mapillary held-out test set as H1–H4; same ISO 12913 conditioning pipeline for both arms.
Metrics: FID, SSIM, LPIPS per city; CLAP cosine similarity between generated image CLAP
description and ground-truth audio (cross-modal alignment proxy).
Hypothesis confirmed if CLAP FID is ≥ 5% lower than ImageBind FID in ≥ 2 of 3 cities
at bootstrap 95% CI.
Also report per-land-use-category breakdown: does the CLAP advantage vary by land use zone?

**Datasets:**
- Mapillary, SoundingEarth, Noise-Planet: same pipeline as H1
- CLAP weights: laion/larger_clap_music_and_speech (HuggingFace, open)
- ImageBind weights: facebookresearch/imagebind (GitHub, open)
- For ImageBind: audio branch takes 2-second mel-spectrogram patches (128 mel bins,
  25 fps hop); projected from 1024-dim to 512-dim before cross-attention

**Model configuration:**
- All other model components identical to H1 Arm C (dual-path ControlNet from H2
  if H2 is confirmed; otherwise single acoustic path from H1)
- Training runs independently for each encoder; same hyperparameters

**Expected result:** CLAP achieves FID ≤ 28 vs. ImageBind FID ~30–32; 5–8% advantage for
CLAP pooled. Largest CLAP advantage expected in high-traffic urban cores (commercial and
transport zones) where urban-specific audio semantics are richest. ImageBind may approach
CLAP performance in park/residential zones where audio-visual co-occurrence in video training
data is more representative.

**geo_benchmark task:** Partial — FID/SSIM comparison is a generation pipeline task; per-land-
use-category breakdown can be produced with OLS/GWR analysis if FID scores are stratified
by OSM land use class.

**Novelty:** 3/5 — Encoder comparison is pragmatic and reusable but not a primary theoretical
contribution; both encoders are published.
**Feasibility:** 5/5 — Both CLAP and ImageBind weights are open; the experiment adds only
one additional training run to the H1 pipeline.
**Alignment:** 4/5 — Directly supports RQ1 and RQ2 (which audio encoder produces more
effective conditioning); provides mandatory model selection rationale.
**Measurability:** 5/5 — FID percentage threshold and bootstrap CI test are fully specified;
per-land-use breakdown is a concrete additional output.
**Impact:** 3/5 — Community-useful model selection benchmark; reusable result; moderate
scientific novelty but high practical value for practitioners adopting the framework.

**Composite: 4.00**
**Decision: CANDIDATE**

---

## H6: Cross-City Zero-Shot Transfer Preserves FID Within 15% Degradation for Dual-Path Architecture but Exceeds 25% Degradation for Acoustic-Only Conditioning in Singapore

**Statement:** A dual-path ControlNet model (OSM spatial + acoustic conditioning) trained on
NYC + London will achieve FID degradation of ≤ 15% when evaluated zero-shot on Singapore,
compared to ≥ 25% FID degradation for an acoustic-only model on the same Singapore test set.
The OSM spatial conditioning pathway is the key generalizability enabler: it provides a
city-agnostic structural prior (building density, land use, road hierarchy) that anchors
generation across morphologically contrasting cities, while pure acoustic conditioning is
insufficiently constrained by city-specific morphological factors not seen during training.
Fine-tuning the acoustic pathway on ≥ 500 Singapore audio-image pairs will recover FID to ≤ 30.

**Rationale:** Gap T3 (composite 3.70) identifies the complete absence of cross-city acoustic
conditioning transfer experiments. Mai et al. (ISPRS 2023) demonstrated that OSM-conditioned
diffusion transfers zero-shot from NYC to London and Tokyo, establishing that OSM spatial
metadata enables geographic generalization. The open question is whether acoustic conditioning
transfers similarly or requires city-specific adaptation. Liang et al. (2020) found that a
CNN acoustic-visual fusion model trained on Singapore transferred only partially to Hong Kong
(R² drop from 0.67 to 0.54), suggesting acoustic-visual correspondence is partially but not
fully city-generalizable. Singapore is the most demanding transfer target due to tropical
compact-city morphology (dense tree canopy, uniform high-rise typology, distinct soundscape
character) absent from NYC/London training distributions. This tests program.md Objective 4
(generalizability across ≥ 3 cities with contrasting morphologies) and anchors the multi-city
scientific claim required for ISPRS impact.

**Test:**
Three transfer experiments (same held-out Mapillary test sets per city):
- Exp 1: Train NYC+London (60% each), test London held-out (40%) — within-distribution reference
- Exp 2: Train NYC+London (full), zero-shot test Singapore (100% withheld) — dual-path model
- Exp 3: Train NYC+London (full), zero-shot test Singapore — acoustic-only model (no OSM path)
- Exp 4: Train NYC+London (full), fine-tune on 500 Singapore pairs, test Singapore — few-shot adaptation

FID degradation = (test_FID − train_held-out_FID) / train_held-out_FID × 100%.
Statistical test: Bootstrap 95% CI on FID (1,000 resamples of 100 generation samples) per experiment.
Secondary: SSIM and CLIP alignment per city as cross-validation metrics.
GWR spatial analysis: fit MGWR per city on per-grid FID from Exp 2 and Exp 4 separately;
compare coefficient maps to test whether fine-tuning changes the spatial structure of
generation quality (i.e., does fine-tuning reduce the high-FID clusters in Singapore CBD?).

Confirmation criteria: Exp 2 FID degradation ≤ 15%; Exp 3 FID degradation ≥ 25%;
Exp 4 FID ≤ 30 (recovery to within-range); difference between Exp 2 and Exp 3 degradation
is statistically significant (bootstrap CI non-overlapping).

**Datasets:**
- Mapillary: separate spatially stratified held-out test sets per city
- SoundingEarth: global coverage; Singapore subset filtered within GADM city boundary (UTM 48N)
- Noise-Planet: available for NYC and London; Singapore supplemented with DCASE 2023/2024
  urban audio challenge data (Singapore-annotated soundscape clips)
- OpenStreetMap: full coverage for all three cities; consistent rasterization pipeline applied
- GHS-BUILT-S: global 100 m raster; all three cities available at consistent resolution
- GADM v4.1: city boundary masks for spatial train/test separation

**Model configuration:**
- Same dual-path ControlNet architecture from H2
- Zero-shot inference: no adaptation for Singapore; OSM rasterized consistently using
  identical encoding procedure as training cities
- CLAP encoder applied without retraining; ISO 12913 prediction head applied as in H1
- Few-shot fine-tuning (Exp 4): LoRA re-fine on Singapore acoustic path only (acoustic
  cross-attention adapters); spatial path frozen; 5K fine-tuning steps on 500 Singapore pairs

**Expected result:** Exp 2 (dual-path zero-shot Singapore) FID ≤ 35; degradation ≤ 15%.
Exp 3 (acoustic-only zero-shot Singapore) FID ≥ 40; degradation ≥ 25%.
Exp 4 (few-shot adaptation) FID ≤ 30; near-full recovery.
Result confirms OSM spatial conditioning as the geographic anchor for zero-shot transfer,
consistent with Mai et al. (2023) finding, and establishes the few-shot adaptation requirement
for acoustic conditioning in novel city morphologies.

**geo_benchmark task:** Partial — per-city FID comparison is a generation pipeline task;
per-city MGWR spatial analysis of generation quality is fully testable via
geo_benchmark/run_benchmark.py for each transfer experiment independently.

**Novelty:** 4/5 — Cross-city acoustic conditioning transfer with morphology-control ablation
(dual-path vs. acoustic-only) is a new generalization test; no prior art for acoustic transfer.
**Feasibility:** 3/5 — Singapore SoundingEarth and Noise-Planet coverage is sparser than
NYC/London; supplementary DCASE data required; zero-shot evaluation protocol is well-defined
but Singapore data pipeline adds engineering overhead.
**Alignment:** 4/5 — Directly supports program.md Objective 4 (multi-city generalizability);
partially answers RQ3 through cross-city transfer analysis; key for ISPRS multi-city framing.
**Measurability:** 4/5 — FID degradation percentage thresholds (15%/25%) are operationally
specific; bootstrap CI provides statistical test; few-shot recovery FID target (≤ 30) is clear.
**Impact:** 4/5 — Generalizability is the central scientific claim for a multi-city GeoAI
paper; ISPRS explicitly values cross-city validation; enables deployment beyond training cities;
few-shot adaptation result is practically actionable.

**Composite: 3.80**
**Decision: CANDIDATE**

---

## Ranked Summary Table

| Rank | ID | Hypothesis (short) | Novelty | Feasibility | Alignment | Measurability | Impact | Composite | Decision |
|------|----|-------------------|---------|-------------|-----------|---------------|--------|-----------|----------|
| 1 | H1 | ISO 12913 conditioning lowers FID vs. raw-audio baseline (FID ≤ 30) | 5 | 4 | 5 | 5 | 5 | **4.80** | Recommended |
| 2 | H3 | MGWR outperforms OLS + GWR on spatial FID variation (AICc + Moran's I) | 4 | 5 | 5 | 5 | 4 | **4.60** | Recommended |
| 3 | H2 | Dual-path ControlNet (OSM local + acoustic global) beats single-path (FID ≥ 8%) | 5 | 4 | 5 | 4 | 4 | **4.40** | Recommended |
| 4 | H4 | Spatial Moran's I of FID > 0.25 pre-MGWR; drops to < 0.10 post-MGWR | 4 | 5 | 4 | 5 | 3 | **4.20** | Candidate |
| 5 | H5 | CLAP outperforms ImageBind as soundscape conditioning encoder (FID ≥ 5%) | 3 | 5 | 4 | 5 | 3 | **4.00** | Candidate |
| 6 | H6 | Zero-shot cross-city transfer: dual-path ≤ 15% FID degradation; acoustic-only ≥ 25% | 4 | 3 | 4 | 4 | 4 | **3.80** | Candidate |

**Minimum threshold check (composite ≥ 3.33 required to proceed):**
H1 (4.80), H3 (4.60), H2 (4.40), H4 (4.20), H5 (4.00), H6 (3.80) — all six hypotheses
exceed the threshold. Three hypotheses score ≥ 4.40 (comfortably above minimum). Proceed.

**Score scale:** All dimensions scored 1–5; composite = unweighted mean of 5 dimensions.
Minimum threshold for "proceed" = composite ≥ 3.33 (equivalent to ≥ 5.0 on rescaled 10-point basis).

**Logical dependency chain:** H1 → H2 (architecture extension) → H3 (spatial analysis of
H1/H2 outputs) → H4 (Moran's I validation of H3 residuals) → H6 (transfer using H2 model).
H5 is a parallel sensitivity analysis within H1. H3 and H4 can be run in parallel with
H1/H2 evaluation once per-location FID scores are available.

---

## Top Hypothesis: Recommended for Research Contract

### H1 — ISO 12913-Conditioned Latent Diffusion for Urban Street-Level Image Synthesis

**Full narrative and experimental design sketch**

**The scientific claim.**
A Stable Diffusion v2.1 + ControlNet model conditioned on structured ISO 12913 perceptual
descriptors (pleasantness, eventfulness, A-weighted SPL) combined with CLAP audio embeddings
constitutes the first generative framework that treats urban soundscape as a geographically
situated, perceptually grounded conditioning signal. It achieves FID ≤ 30 on held-out
Mapillary images across NYC, London, and Singapore — matching or exceeding the prior
state-of-the-art audio-to-image generation result (Sound2Scene FID 28.3) while introducing
geographic specificity, ISO 12913 perceptual grounding, and spatial regression analysis
entirely absent from prior work.

**Why this is the right primary hypothesis.**
It sits at the exact intersection of the two highest-scoring gaps: M1 (composite 4.80,
absence of ISO 12913 conditioning in any generative model) and T2 (composite 4.35,
ISO 12913 scores never used as generative priors). It is falsifiable by a concrete
three-arm ablation experiment with specified FID thresholds. It constitutes the paper's
primary methodological novelty. H2 and H3 are additive: H2 tests whether the dual-path
OSM+acoustic architecture further improves on H1, and H3 uses H1's per-location FID scores
as dependent variable for GWR/MGWR spatial analysis. All three Recommended hypotheses
should be pursued together as an integrated study, with H1 as the main result.

**Why now.**
Two ISPRS/AAG review papers (Biljecki & Ito 2021; Biljecki et al. 2024) explicitly name
acoustic-visual fusion as "a key unexplored direction" in Urban Visual Intelligence — providing
direct editorial community endorsement of the gap. The ARAUS dataset (2022), CLAP weights
(2022), and Stable Diffusion + ControlNet (2022–2023) all became publicly available within
the last four years. The enabling infrastructure now exists; the gap has been explicitly
flagged by the target venue's community; no competing paper has yet appeared.

**Experimental design sketch (four-phase, 6-week timeline).**

Phase 1 — Data pipeline (weeks 1–2):
1. Download Mapillary images for NYC (EPSG:32618), London (EPSG:32630), Singapore (EPSG:32648)
   via Mapillary API (open access). Target: ≥ 5,000 images per city; stratified random
   sample by OSM land use class (7 classes) and road hierarchy (4 levels).
2. Match each Mapillary image location to the nearest SoundingEarth audio clip within 50 m
   (UTM proximity; temporal window ≤ 6 months). Supplement with Noise-Planet SPL
   measurements interpolated via IDW (k=5 neighbors, 500 m search radius) where audio clips
   are absent.
3. Compute CLAP 512-dim embeddings for all matched audio (laion/larger_clap_music_and_speech,
   HuggingFace).
4. Run acoustic-to-ISO 12913 prediction head (MLP trained on ARAUS) on CLAP embeddings to
   generate pleasantness, eventfulness, LAeq estimates. Compile per-image conditioning vector:
   [CLAP_512 || pleasantness || eventfulness || LAeq] (515-dim total).
5. Rasterize OSM land use (7-class), road hierarchy (4-level ordinal), and GHS-BUILT-S
   building density to 256×256 control images at ~5 m/pixel (local UTM per city).

Phase 2 — Model training (weeks 2–3):
6. Three parallel training runs (Arm A: text-only; Arm B: CLAP-only; Arm C: CLAP + ISO 12913):
   - Initialize SD v2.1 backbone (frozen); initialize ControlNet adapter weights from scratch
   - For Arms B and C: add cross-attention conditioning pathway with 515-dim vector
   - LoRA adapters (r=16) on all UNet cross-attention layers; AdamW lr=1e-4, 50K steps,
     batch 16, cosine LR decay, 1K warmup steps
   - Training data: 80% of matched pairs per city (city-stratified split)

Phase 3 — Evaluation (week 4):
7. Generate 500 images per city per arm on held-out test set (20% per city).
   FID: torchmetrics.FrechetInceptionDistance, ≥ 500 generated vs. real images.
   SSIM: skimage.metrics.structural_similarity.
   LPIPS: lpips package (Alex net perceptual similarity).
   Semantic segmentation overlap: DeepLab v3+ (torchvision pretrained ImageNet),
   4 primary classes (building, road, vegetation, sky).
8. Statistical tests: paired Wilcoxon signed-rank on per-image LPIPS (Arm C vs. B per city);
   Bonferroni correction for 3-city × 2-comparison multiple testing (α = 0.05/6 = 0.0083).
   Bootstrap 95% CI on FID (1,000 resamples per arm per city).

Phase 4 — Spatial analysis (week 5):
9. Aggregate FID to 250 m grid (≥ 20 images per cell required; ~800 cells per city).
   Compute Moran's I on raw FID grid (PySAL libpysal, queen contiguity, 999 permutations).
   Run OLS/GWR/MGWR via geo_benchmark/run_benchmark.py (adaptive bisquare kernel; covariates:
   LAeq, CLAP PC1–PC3, GHS-BUILT-S density, road hierarchy index, NDVI proxy).
   Report AICc, adjusted R², residual Moran's I (OLS/GWR/MGWR).
   Generate coefficient maps via geo_benchmark/evaluation/visualize.py.
   Save all results to geo_benchmark/results/soundscape_fidelity_[city].json.

**Success criteria.**

| Metric | Target | Source of evidence |
|--------|--------|--------------------|
| FID (Arm C) | ≤ 30 pooled | Generation evaluation pipeline |
| FID improvement C vs. B | ≥ 10% | Bootstrap CI comparison |
| FID improvement C vs. A | ≥ 15% | Bootstrap CI comparison |
| SSIM improvement (C vs. B) | ≥ 0.05 absolute | Paired SSIM on test set |
| Wilcoxon p-value (LPIPS, C vs. B) | < 0.0083 (Bonferroni) | Per-city signed-rank test |
| MGWR adjusted R² | ≥ 0.65 | geo_benchmark/run_benchmark.py |
| OLS residual Moran's I | ≥ 0.15 | geo_benchmark/evaluation/metrics.py |
| MGWR residual Moran's I | ≤ 0.10 in all 3 cities | geo_benchmark/evaluation/metrics.py |
| MGWR AICc improvement over OLS | ≥ 10 units | geo_benchmark results JSON |
| Semantic class overlap (C vs. B) | ≥ 5 pp | DeepLab v3+ segmentation |

**Expected paper contributions.**
1. First latent diffusion model conditioned on ISO 12913 urban soundscape descriptors —
   establishes acoustic-to-image generation as a GeoAI sub-domain with ISO 12913 grounding.
2. Dual-path ControlNet architecture for joint acoustic-semantic and spatial-morphological
   conditioning — reusable beyond soundscape for any multi-scale urban conditioning task.
3. First OLS/GWR/MGWR spatial analysis of generative model quality as a function of
   acoustic-morphological covariates — introduces spatial validation standard for GeoAI
   generation papers at ISPRS/CEUS venue level.
4. Multi-city analysis (NYC, London, Singapore) with quantified FID degradation bounds
   for zero-shot cross-city transfer — validates geographic generalizability.
5. Interpretable MGWR coefficient maps showing where soundscape conditioning is most and
   least effective — directly actionable for urban planners and acoustic environment designers.

**Risks and mitigations.**

| Risk | Mitigation |
|------|-----------|
| Sparse SoundingEarth coverage in Singapore | Supplement with FreeSound geotagged clips and DCASE 2023/2024 Singapore audio; use Noise-Planet SPL as primary acoustic signal where full audio is unavailable |
| ARAUS pleasantness/eventfulness annotations do not generalize to SoundingEarth audio style | Apply ARAUS-trained MLP only to CLAP embeddings (not raw audio), so that CLAP's urban-domain pretraining bridges the domain gap |
| FID estimation noise at small sample sizes | Use ≥ 500 generated images per arm; report bootstrap 95% CI; use torchmetrics FID implementation with consistent preprocessing |
| MGWR computational cost at 2,400 observations | Within CLAUDE.md MGWR ≤ 3,000 limit; use mgwr package (Oshan et al. 2019); city-by-city runs if needed |
| OSM rasterization inconsistencies across cities | Standardize encoding pipeline (land use class mapping, pixel resolution, UTM projection) with a single shared preprocessing script |
| Mapillary API rate limits | Download in advance; use open CC-BY-SA data portal; cache locally |

**Venue fit.**
All five contributions align with ISPRS Journal of Photogrammetry and Remote Sensing:
cross-modal GeoAI, spatial regression analysis (OLS/GWR/MGWR), multi-city open-data
reproducible framework, urban analytics application. The paper architecture is:
Introduction (1,000 w) → Related Work T1/T2/T3/T5 (1,800 w) → Method: dual-path ControlNet
+ ISO 12913 conditioning (2,200 w) → Experiments: ablation + FID/SSIM + GWR/MGWR analysis
(2,500 w) → Discussion: multi-city generalization + bandwidth interpretation + limitations
(1,500 w) → Conclusion (500 w). Target total: ~9,500 words (within ISPRS 10,000-word limit).

---

*Hypotheses produced by hypothesis-generator agent.*
*Sources: memory/gap-analysis.md, memory/synthesis-2026-04-01.md, program.md.*
*Next step: commit top hypothesis (H1 + H2 + H3 as integrated study) to research_contract.md;*
*invoke /run-experiment to execute geo_benchmark OLS/GWR/MGWR pipeline on pilot data.*
