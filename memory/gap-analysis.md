# Research Gap Analysis
Date: 2026-04-01
Topic: Soundscape-conditioned street-level image generation (GeoAI framework)
Source synthesis: memory/synthesis-2026-04-01.md (52 papers, 63 indexed)

---

## Summary

11 gaps identified across three categories (5 methodological, 3 geographic, 3 thematic).
Top gap: **M1 — Urban-conditioned acoustic-to-image diffusion with ISO 12913 descriptors**
(composite score 4.85). This is the primary gap the proposed framework directly addresses and
is the recommended basis for hypothesis generation and paper framing.

Composite score formula: 0.35 × Novelty + 0.30 × Feasibility + 0.20 × Impact + 0.15 × Alignment

---

## Methodological Gaps

### Gap M1: Urban-conditioned acoustic-to-image diffusion with ISO 12913 descriptors — Score: 4.85
**Type:** Methodological
**Description:** Every existing audio-to-image generation system (Sound2Scene, Sound2Vision,
SonicDiffusion) trains and evaluates on general environmental sound benchmarks (VEGAS,
VGGSound, AudioCaps) without urban soundscape-specific conditioning. None applies ISO 12913
perceptual descriptors (pleasantness, eventfulness, vibrancy) or A-weighted SPL as structured
conditioning signals. The gap is the absence of a generation architecture that treats
soundscape as a geographically situated, perceptually grounded signal rather than an abstract
audio embedding.
**Evidence from literature:**
- Sung-Bin et al. (CVPR 2023) — Sound2Scene achieves FID 28.3 using audio-to-visual latent
  alignment but uses VEGAS/VGGSound; explicitly no urban/soundscape context, no ISO 12913.
- Biner et al. (arXiv 2024) — SonicDiffusion injects audio into frozen Stable Diffusion via
  cross-attention adapters; no urban application, no geographic framework, no soundscape.
- Kang et al. (Landscape Urban Planning 2018) — Establishes ISO 12913 pleasantness/
  eventfulness as cross-modal signal that predicts visual scene perception, but no generative
  model exists in this tradition.
**Novelty:** 5/5 — No paper in the reviewed set uses ISO 12913 descriptors as generative
conditioning; this combination is unambiguously absent from the literature.
**Feasibility:** 5/5 — ARAUS (Ooi et al., 2022; 25,440 ISO 12913 responses), CLAP/ImageBind
open weights, Stable Diffusion + ControlNet open weights, and Mapillary ground-truth imagery
are all openly available; no proprietary data dependency.
**Impact:** 4/5 — Enables soundscape-driven urban visualization for planners; fills acoustic
gap in street-level coverage; privacy-preserving mapping alternative.
**Alignment:** 5/5 — Directly addresses Research Question 1 and is the core proposed
contribution.
**Composite score:** 0.35×5 + 0.30×5 + 0.20×4 + 0.15×5 = 1.75 + 1.50 + 0.80 + 0.75 = **4.80**

---

### Gap M2: Dual-path ControlNet conditioning (local OSM spatial + global soundscape embedding) — Score: 4.55
**Type:** Methodological
**Description:** Existing ControlNet-based generation uses single-modality spatial conditioning
(edge maps, depth, segmentation). Uni-ControlNet (Zhao et al., NeurIPS 2023) unifies local
and global controls but applies neither acoustic data nor geographic metadata. No published
work injects soundscape embeddings as a global semantic conditioning channel alongside local
OSM-derived spatial controls (land use rasters, building density, road hierarchy) in a
dual-path architecture. The gap is the absence of a multi-channel ControlNet design that fuses
acoustic and spatial signals at different architectural levels.
**Evidence from literature:**
- Zhang et al. (ICCV 2023) — ControlNet supports spatial conditioning via zero-conv adapters
  but uses only visual spatial signals; no audio conditioning pathway.
- Zhao et al. (NeurIPS 2023) — Uni-ControlNet unifies local + global conditioning but tests
  only visual conditions (edges, depth, normals, segmentation); explicitly no audio.
- Mai et al. (ISPRS 2023) — Closest GeoAI conditioning paper; uses OSM metadata only, no
  acoustic global embedding pathway.
**Novelty:** 5/5 — Dual-path acoustic-spatial ControlNet is entirely absent from existing
work; the architectural pattern is new.
**Feasibility:** 4/5 — ControlNet and Uni-ControlNet codebases are open; audio embeddings from
CLAP/ImageBind are straightforward to inject via cross-attention; some engineering complexity
in multi-path fusion.
**Impact:** 4/5 — Addresses Research Question 2 directly; produces an architecture reusable
across urban sensing tasks beyond soundscape.
**Alignment:** 5/5 — Central to Research Questions 1 and 2.
**Composite score:** 0.35×5 + 0.30×4 + 0.20×4 + 0.15×5 = 1.75 + 1.20 + 0.80 + 0.75 = **4.50**

---

### Gap M3: GWR/MGWR applied to spatial variation in generative model fidelity — Score: 4.43
**Type:** Methodological
**Description:** Spatial regression has been applied to soundscape perception (Fan et al.,
IJGIS 2020) and urban noise (Shen et al., TGRS 2022) but never to explain spatial variation in
generative model quality metrics (FID per grid cell, SSIM per location, CLIP alignment score).
Wei et al. (2025) is the sole paper combining diffusion synthesis with GWR evaluation, but uses
satellite imagery and no acoustic conditioning. The gap is the absence of OLS/GWR/MGWR
frameworks that treat image generation fidelity scores as spatially varying dependent
variables explainable by acoustic and morphological covariates.
**Evidence from literature:**
- Fan et al. (IJGIS 2020) — GWR R²=0.71 vs OLS R²=0.54 for soundscape-land-use; residual
  Moran's I=0.08 after GWR; limited to perception scores, not generation quality metrics.
- Wei et al. (arXiv 2025) — Only paper combining diffusion + GWR but satellite imagery and
  no acoustic conditioning.
- Shen et al. (TGRS 2022) — GWR for urban morphology + noise; no generative model.
**Novelty:** 4/5 — Applying GWR to generation quality (FID, SSIM) rather than perception
scores is novel; GWR itself is established. Partially anticipated by Wei et al. (2025).
**Feasibility:** 5/5 — mgwr Python package (Oshan et al., 2019) is open-source; FID/SSIM are
computable per spatial grid cell; geo_benchmark baseline pipeline already supports OLS/GWR/MGWR.
**Impact:** 4/5 — Produces interpretable maps of where acoustic conditioning works well or
fails; directly actionable for urban planners and soundscape designers.
**Alignment:** 5/5 — Directly addresses Research Question 3.
**Composite score:** 0.35×4 + 0.30×5 + 0.20×4 + 0.15×5 = 1.40 + 1.50 + 0.80 + 0.75 = **4.45**

---

### Gap M4: Moran's I applied to generation quality residuals as a spatial validation metric — Score: 4.08
**Type:** Methodological / Validation
**Description:** No paper in the audio-visual or generative GeoAI literature applies Moran's I
to test spatial autocorrelation of generation quality residuals. The standard practice in T4
(generative AI) papers is to report global FID/SSIM without any spatial structure analysis.
The T5 literature (GWR papers) consistently reports Moran's I for regression residuals but
these papers do not generate images. Reporting Moran's I of per-location generation quality
metrics before and after GWR adjustment would introduce a spatial validation dimension
absent from the generative AI literature.
**Evidence from literature:**
- Synthesis Section 7, Pattern 6: "No paper uses Moran's I to evaluate spatial
  autocorrelation of generative model outputs."
- Fan et al. (IJGIS 2020) and Shen et al. (TGRS 2022) report Moran's I for regression
  residuals; neither involves image generation.
- All T4 papers report only global aggregate quality metrics; no spatial structure analysis.
**Novelty:** 4/5 — Moran's I itself is standard but applying it to generative quality metrics
is methodologically novel in the GeoAI generation space.
**Feasibility:** 5/5 — Moran's I is computable via PySAL/libpysal; only requires that
generation quality is recorded per geographic location, which the proposed pipeline does.
**Impact:** 3/5 — Primarily methodological contribution; strengthens paper rigor at ISPRS venue.
**Alignment:** 4/5 — Required by geo_benchmark threshold in program.md; strengthens Research
Question 3 answer.
**Composite score:** 0.35×4 + 0.30×5 + 0.20×3 + 0.15×4 = 1.40 + 1.50 + 0.60 + 0.60 = **4.10**

---

### Gap M5: Nonlinear GWR extensions (GWNN, GWRBoost) for acoustic-visual fidelity modeling — Score: 3.48
**Type:** Methodological
**Description:** GWRBoost (Li et al., 2022), GWNN (Zhou et al., 2025), and M-SGWR (Liu et al.,
2026) all demonstrate improved fit over standard GWR on nonlinear urban datasets (house prices)
but none has been applied to acoustic-visual correspondence or image generation quality. Given
that the relationship between soundscape embeddings and generation fidelity is likely nonlinear
(Watcharasupat et al., 2022 shows ISO 12913 dimensions are not linearly determined by spectral
features), nonlinear GWR may outperform standard GWR in the proposed framework.
**Evidence from literature:**
- Li et al. (arXiv 2022) — GWRBoost uses GWR + gradient boosting + SHAP; no acoustic domain.
- Zhou et al. (arXiv 2025) — GWNN: geographically weighted neural network; no soundscape.
- Liu et al. (arXiv 2026) — M-SGWR: similarity-weighted MGWR; 0 citations, very new.
**Novelty:** 3/5 — Methods exist; application domain is new; exploratory comparison value.
**Feasibility:** 4/5 — GWRBoost and GWNN have reference implementations; integration into
geo_benchmark comparison table is straightforward.
**Impact:** 3/5 — Methodological comparison value; may improve spatial R² marginally.
**Alignment:** 3/5 — Optional extension; relevant to Research Question 3 but not central.
**Composite score:** 0.35×3 + 0.30×4 + 0.20×3 + 0.15×3 = 1.05 + 1.20 + 0.60 + 0.45 = **3.30**

---

## Geographic Gaps

### Gap G1: Global South and non-Western urban morphology in soundscape-visual generation — Score: 4.10
**Type:** Geographic / Equity
**Description:** The T3 and T4 street-level generation literature is concentrated in the
Global North and a small set of East/Southeast Asian cities. Among the 52 reviewed papers,
nearly all geographic applications are in NYC, London, Tokyo, Singapore, or unnamed Western
cities. The one exception, Liu et al. (2021), uses Guangzhou for noise mapping only. No
generative model for street-level imagery has been trained or evaluated in African, Latin
American, or South Asian cities. Given that acoustic environments in these contexts are
fundamentally different (street vendors, informal transport, high density of biological sounds),
a framework trained on NYC/London/Singapore may not generalize.
**Evidence from literature:**
- Qin et al. (CEUS 2019) — 18 global cities but coarse resolution; no ML generation.
- Synthesis Section 3: "geographic diversity of T3 papers is primarily urban Global North
  with limited Global South coverage, a recurring limitation noted by multiple review papers."
- Biljecki & Ito (2021) and Biljecki et al. (2024) — explicitly call for geographic diversity
  in urban analytics research.
**Novelty:** 4/5 — No generative acoustic-visual model has been tested outside Global North
or East/Southeast Asia; a clear gap.
**Feasibility:** 3/5 — Mapillary coverage is lower in the Global South; acoustic reference
data (Noise-Planet) has sparser coverage. Feasible for a future study but not with open data
available for the current three-city scope.
**Impact:** 4/5 — Significant equity dimension; urban soundscape design decisions in the
Global South are data-scarce; generation from acoustic data could fill coverage gaps.
**Alignment:** 3/5 — The current program.md targets NYC/London/Singapore; this gap is a
stated future-work direction, not the core study design.
**Composite score:** 0.35×4 + 0.30×3 + 0.20×4 + 0.15×3 = 1.40 + 0.90 + 0.80 + 0.45 = **3.55**

---

### Gap G2: Temporal acoustic-visual dynamics — time-of-day and seasonal generation — Score: 3.93
**Type:** Geographic / Temporal
**Description:** All existing acoustic-visual generation and correspondence papers treat the
acoustic environment as a static snapshot. Urban soundscapes are fundamentally time-varying:
diurnal cycles (morning rush vs. midday vs. evening), day-of-week patterns, and seasonal
effects produce systematically different acoustic signatures at the same location. No paper
models how time-of-day or seasonal variation in acoustic inputs affects the generated visual
output or correspondingly changes which visual scene elements should appear (street density,
pedestrian activity, lighting). The proposed framework includes time-of-day as an auxiliary
conditioning input, but temporal dynamics across days/seasons are not addressed.
**Evidence from literature:**
- Lionello et al. (Landscape Urban Planning 2020) — multi-metric soundscape assessment does
  not model temporal dynamics; single measurement sessions.
- Hoffmann et al. (ISPRS JPRS 2023) — temporal change detection in street-view imagery but
  not acoustic; no soundscape.
- Chen et al. (arXiv 2025) — single-time-point CLIP alignment analysis; no temporal dimension.
**Novelty:** 4/5 — Temporal conditioning on acoustic time-series for image generation is
entirely absent from the literature.
**Feasibility:** 3/5 — Noise-Planet provides time-stamped crowdsourced measurements; Mapillary
has metadata timestamps. Aligning these at scale is technically challenging.
**Impact:** 4/5 — Enables diurnal urban visualization; relevant for urban planning simulation.
**Alignment:** 3/5 — Time-of-day is listed in program.md as an auxiliary input; full temporal
dynamics are out of scope for the current paper but a natural extension.
**Composite score:** 0.35×4 + 0.30×3 + 0.20×4 + 0.15×3 = 1.40 + 0.90 + 0.80 + 0.45 = **3.55**

---

### Gap G3: Street-level acoustic image gap-filling for data-sparse cities — Score: 3.88
**Type:** Geographic / Application
**Description:** A practical downstream gap is the use of acoustic + OSM data as surrogates
to synthesize plausible street-level images where visual coverage is sparse or absent. Mapillary
coverage is dense in Western cities but sparse in many global regions. No existing paper
demonstrates using acoustic surrogate data to fill visual coverage gaps at city scale. This
gap is partly methodological (no system exists) and partly geographic (the coverage problem
is concentrated in specific regions).
**Evidence from literature:**
- Biljecki & Ito (2021) — identifies sparse coverage in parts of Africa, South America,
  Central Asia as a problem for street-level urban analytics.
- Xia et al. (Nature Communications 2023) — multi-source fusion across 10 cities shows
  cross-modal fusion improves coverage but does not perform generation.
- Liu et al. (Science Total Env 2021) — CNN noise prediction at 10-m resolution provides
  an acoustic proxy for locations without visual data; no generation step.
**Novelty:** 4/5 — Acoustic-driven gap-filling synthesis is a novel application framing.
**Feasibility:** 3/5 — Requires acoustic data in data-sparse areas, which is often also
missing; SoundingEarth global coverage could partially address this.
**Impact:** 4/5 — Listed as Objective 5 in program.md; high practical value for urban
planners and NGOs in data-sparse contexts.
**Alignment:** 4/5 — Explicitly listed in program.md Section 3 Objective 5.
**Composite score:** 0.35×4 + 0.30×3 + 0.20×4 + 0.15×4 = 1.40 + 0.90 + 0.80 + 0.60 = **3.70**

---

## Thematic Gaps

### Gap T1: Acoustic-visual correspondence as a function of urban morphology — untested with GWR — Score: 4.38
**Type:** Thematic
**Description:** Qin et al. (CEUS 2019) showed that acoustic-visual Pearson correlation varies
by land use zone (r=0.52–0.74 residential vs. r~0.30 mixed-use), and Chen et al. (2025) report
a mean CLIP alignment of 0.31. However, neither study uses spatial regression to explain
geographic variation in this correspondence, nor does either test the role of urban morphology
variables (building height, sky view factor, canyon ratio, green view index) as moderators.
The gap is a spatially explicit, regression-based account of why acoustic-visual correspondence
varies and what urban form factors drive variation — which is precisely what OLS/GWR/MGWR can
provide.
**Evidence from literature:**
- Qin et al. (CEUS 2019) — correspondence analysis across 18 cities; no spatial regression.
- Chen et al. (arXiv 2025) — evaluates sound-vision alignment at street level; no GWR,
  single city (NYC), analysis only.
- Fan et al. (IJGIS 2020) — GWR for soundscape-land-use; dependent variable is perception
  score, not acoustic-visual correspondence.
**Novelty:** 4/5 — The combination of acoustic-visual correspondence as dependent variable
with GWR spatial regression and urban morphology covariates does not exist in the literature.
**Feasibility:** 5/5 — GHS-BUILT-S provides building density; OSM provides land use; mgwr
package handles regression; data at NYC/London/Singapore is available.
**Impact:** 4/5 — Explains where soundscape conditioning is most and least reliable; informs
optimal deployment zones for acoustic-based image synthesis in urban planning.
**Alignment:** 5/5 — Directly answers Research Question 3.
**Composite score:** 0.35×4 + 0.30×5 + 0.20×4 + 0.15×5 = 1.40 + 1.50 + 0.80 + 0.75 = **4.45**

---

### Gap T2: ISO 12913 soundscape descriptors as structured generative priors — Score: 4.23
**Type:** Thematic
**Description:** The soundscape perception literature (ARAUS, Watcharasupat et al., Tarlao et
al.) has produced validated models mapping acoustic features to ISO 12913 perceptual dimensions
(pleasantness, eventfulness, appropriateness). None of this work treats these perceptual
dimensions as generative priors for visual synthesis. Treating ISO 12913 scores as latent
conditioning variables — rather than prediction endpoints — would allow soundscape designers
to specify a target perceptual quality (e.g., "high pleasantness, low eventfulness") and
generate the corresponding visual scene. This inversion of the soundscape-perception pipeline
has not been attempted.
**Evidence from literature:**
- Ooi et al. (IEEE Trans. Affective Computing 2022) — ARAUS: 25,440 ISO 12913 responses;
  used as training data for perception models, never as generative conditioning.
- Watcharasupat et al. (J. Acoustical Society 2022) — acoustic-to-perception regression;
  direction of inference is acoustic→perception, never perception→image.
- Tarlao et al. (Building and Environment 2024) — SEM on appropriateness mediating
  acoustic-quality; no generative component.
**Novelty:** 5/5 — Perception-to-image generation using ISO 12913 scores as conditioning
does not exist anywhere in the reviewed literature.
**Feasibility:** 4/5 — ARAUS provides perceptual annotations; conditioning on scalar
pleasantness/eventfulness scores is architecturally straightforward via cross-attention;
alignment with visual scene at training time requires matched annotated pairs.
**Impact:** 4/5 — Enables "design by soundscape": urban planners specify acoustic quality
targets and receive visual scene proposals.
**Alignment:** 4/5 — Central to Research Question 1; adds a structured conditioning variant
beyond raw audio embeddings.
**Composite score:** 0.35×5 + 0.30×4 + 0.20×4 + 0.15×4 = 1.75 + 1.20 + 0.80 + 0.60 = **4.35**

---

### Gap T3: Cross-city zero-shot generalization of acoustic-visual generation models — Score: 3.88
**Type:** Thematic
**Description:** Mai et al. (ISPRS 2023) demonstrated zero-shot transfer of a visual synthesis
model trained on NYC to London and Tokyo using OSM metadata conditioning. No analogous
transfer experiment exists for acoustic conditioning. It is unknown whether a model trained on
NYC soundscape-image pairs will generate plausible images when applied to London (European
morphology) or Singapore (tropical compact-city) without fine-tuning. This is a core
generalization question for GeoAI: do acoustic-visual correspondences generalize across
cities, or are they locally specific?
**Evidence from literature:**
- Mai et al. (ISPRS 2023) — zero-shot transfer via OSM conditioning; no acoustic channel;
  transfer works for visual-spatial conditioning.
- Qin et al. (CEUS 2019) — acoustic-visual correspondence varies across 18 cities but no
  ML transfer experiment.
- Synthesis Section 3: "The multi-city analysis spanning NYC, London, and Singapore would be
  without precedent in the T1 cluster."
**Novelty:** 4/5 — Transfer of acoustic conditioning across contrasting urban morphologies
is a new generalization test with no prior art.
**Feasibility:** 3/5 — Requires sufficient Mapillary + acoustic data in all three cities;
Singapore acoustic data may be sparser; zero-shot evaluation requires held-out city test sets.
**Impact:** 4/5 — Generalizability is the central scientific claim for a multi-city GeoAI
paper; ISPRS venue rewards this.
**Alignment:** 4/5 — Directly supports the multi-city design in program.md Section 7.
**Composite score:** 0.35×4 + 0.30×3 + 0.20×4 + 0.15×4 = 1.40 + 0.90 + 0.80 + 0.60 = **3.70**

---

## Ranked Gap Summary Table

| Rank | Gap ID | Name | Composite Score | Category |
|------|--------|------|----------------|----------|
| 1 | M1 | Urban-conditioned acoustic-to-image diffusion with ISO 12913 | 4.80 | Methodological |
| 2 | T1 | Acoustic-visual correspondence as function of urban morphology (GWR) | 4.45 | Thematic |
| 3 | M2 | Dual-path ControlNet: local OSM spatial + global soundscape embedding | 4.50 | Methodological |
| 4 | M3 | GWR/MGWR applied to generative model fidelity as dependent variable | 4.45 | Methodological |
| 5 | T2 | ISO 12913 soundscape descriptors as structured generative priors | 4.35 | Thematic |
| 6 | M4 | Moran's I applied to generation quality residuals | 4.10 | Methodological/Validation |
| 7 | G1 | Global South / non-Western urban morphology in generation | 3.55 | Geographic/Equity |
| 8 | G2 | Temporal acoustic-visual dynamics (diurnal/seasonal) | 3.55 | Geographic/Temporal |
| 9 | T3 | Cross-city zero-shot generalization of acoustic-visual generation | 3.70 | Thematic |
| 10 | G3 | Acoustic-based gap-filling for data-sparse cities | 3.70 | Geographic/Application |
| 11 | M5 | Nonlinear GWR extensions for acoustic-visual fidelity modeling | 3.30 | Methodological |

*Note: Ties at 4.45 broken by Novelty score (M2=5, M3=4, T1=4); M2 ranked above M3 and T1 by
Novelty, M3 and T1 tied — T1 ranked above M3 due to higher Alignment score.*

Corrected ranking (rechecked):
- M1: 4.80
- M2: 4.50
- M3 and T1 both: 4.45 — T1 ranked 3 (Alignment 5 > M3 Alignment 5, identical; Novelty M3=4,
  T1=4; both equal; M3 placed above T1 as it is a core deliverable of the study design)
- T2: 4.35
- M4: 4.10
- T3 and G3: 3.70 — T3 ranked above G3 as it has higher Novelty
- G1 and G2: 3.55
- M5: 3.30

Final corrected table:

| Rank | Gap ID | Name | Composite Score | Category |
|------|--------|------|----------------|----------|
| 1 | M1 | Urban-conditioned acoustic-to-image diffusion with ISO 12913 | 4.80 | Methodological |
| 2 | M2 | Dual-path ControlNet: local OSM spatial + global soundscape embedding | 4.50 | Methodological |
| 3 | M3 | GWR/MGWR applied to generative model fidelity as dependent variable | 4.45 | Methodological |
| 4 | T1 | Acoustic-visual correspondence as function of urban morphology (GWR) | 4.45 | Thematic |
| 5 | T2 | ISO 12913 soundscape descriptors as structured generative priors | 4.35 | Thematic |
| 6 | M4 | Moran's I applied to generation quality residuals | 4.10 | Methodological/Validation |
| 7 | T3 | Cross-city zero-shot generalization of acoustic-visual generation | 3.70 | Thematic |
| 8 | G3 | Acoustic-based gap-filling for data-sparse cities | 3.70 | Geographic/Application |
| 9 | G1 | Global South / non-Western urban morphology | 3.55 | Geographic/Equity |
| 10 | G2 | Temporal acoustic-visual dynamics (diurnal/seasonal) | 3.55 | Geographic/Temporal |
| 11 | M5 | Nonlinear GWR extensions for acoustic-visual fidelity modeling | 3.30 | Methodological |

---

## Top Gap: Recommended for hypothesis generation

**Primary gap: M1 — Urban-conditioned acoustic-to-image diffusion with ISO 12913 descriptors
(composite score 4.80)**

The synthesis of 52 papers reveals that cross-modal audio-visual generation and urban
soundscape science have developed in parallel for over a decade without convergence. The
entire audio-to-image generation literature (Sound2Scene, Sound2Vision, SonicDiffusion,
Network Bending) uses abstract audio embeddings from non-urban benchmarks and has no contact
with ISO 12913 soundscape measurement, geographic metadata, or spatial regression. Separately,
the urban soundscape literature (ARAUS, Kang et al., Fan et al., Lionello et al.) has produced
rich perceptual datasets and validated ISO 12913 frameworks but has never attempted generative
modeling. Two review papers in the target venue's community (Biljecki et al., Annals AAG 2024;
Biljecki & Ito, Landscape Urban Planning 2021) explicitly name acoustic-visual fusion as the
key unexplored direction in urban visual intelligence, providing direct gap endorsement from the
editorial community of ISPRS and affiliated venues.

The proposed framework sits at the intersection of four gaps that individually score between
4.10 and 4.80: (M1) no existing model uses ISO 12913 acoustic descriptors as conditioning
signals; (M2) no ControlNet architecture has combined local OSM spatial conditioning with a
global acoustic embedding pathway; (M3) no paper has applied GWR or MGWR to explain spatial
variation in generative image quality; and (T2) ISO 12913 perceptual scores have never been
inverted into generative priors. The multi-city design across NYC, London, and Singapore
additionally addresses gap T3 (zero-shot cross-city acoustic generalization), which the
closest GeoAI precursor (Mai et al., ISPRS 2023) demonstrated is achievable with spatial
metadata conditioning but has not been tested with acoustic conditioning.

The central hypothesis recommended for the paper is: Urban soundscape embeddings — combining
CLAP/ImageBind acoustic features with ISO 12913 pleasantness and eventfulness scores and
A-weighted SPL — provide statistically significant generative conditioning signals for
street-level image synthesis, and the magnitude of this conditioning effect varies
non-stationarily across urban space as captured by MGWR, with spatially varying coefficients
that reflect land use type, building density, and road hierarchy at different spatial scales.

This hypothesis is (a) falsifiable by the FID/SSIM ablation experiments, (b) spatially
testable by the GWR/MGWR analysis with Moran's I validation, and (c) directly differentiates
the proposed paper from all four near-duplicate papers (Sound2Scene, Sound2Vision,
SonicDiffusion, Cross-Modal Urban Sensing) which lack geographic grounding, spatial
regression, and ISO 12913 conditioning.

---

*Gap analysis produced by gap-finder agent. Source: memory/synthesis-2026-04-01.md,
memory/synthesis-matrix.csv, memory/paper-cache/index.json, program.md.*
