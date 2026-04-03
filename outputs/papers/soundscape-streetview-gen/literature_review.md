---
section: literature_review
score: 8.4
attempt: 1
status: ACCEPTED
---

# 2. Literature Review

Four intersecting research traditions inform SoundScape-ControlNet: cross-modal
audio-visual generation, GeoAI street-level synthesis, urban soundscape science and
ISO 12913-based perception modeling, and spatially varying regression for acoustic-visual
analysis. We review each tradition thematically, identify the specific gap this paper
addresses, and conclude each subsection with an explicit positioning statement. A synthesis
table comparing the generative systems most closely related to the proposed framework
appears at the end of the section.

## 2.1 Cross-Modal Audio-Visual Generation

The possibility that audio embeddings can condition visual synthesis has been established
through a decade of progressively more capable cross-modal architectures. Early work framed
the problem as video prediction: Sound2Sight (Cherian & Chatterjee, 2020) demonstrated that
variational autoencoders with multimodal discriminators could predict future video frames from
audio, establishing the statistical coupling between sound and visual dynamics. The transition
from video to still-image generation was formalized by Sound2Scene (Sung-Bin et al., 2023),
which achieved FID 28.3 on the VEGAS environmental sound benchmark through audio-to-visual
latent alignment followed by GAN decoding — the most-cited still-image audio conditioning
result and the direct numerical baseline for the present paper. Sound2Vision (Li et al., 2024)
improved on this to FID approximately 24 by replacing the GAN decoder with a latent diffusion
model (Rombach et al., 2022) and refining cross-modal contrastive alignment via sound source
localization to select high-correspondence training pairs. SonicDiffusion (Biner et al., 2024)
took a lighter-weight architectural approach: audio tokens are injected into frozen Stable
Diffusion layers via lightweight cross-attention adapters, enabling both generation and
editing without full UNet retraining. Network Bending (Pascual et al., 2024) extends this
further toward zero-shot conditioning by steering generation through targeted activation
injection, circumventing training entirely at the cost of output quality.

Parallel to generation models, shared embedding spaces have matured considerably. CLAP
(Wu et al., 2023) provides contrastive language-audio pretraining over 633,000 audio-text
pairs, achieving state-of-the-art performance on zero-shot audio classification and
text-audio retrieval; the resulting 512-dimensional embeddings serve as the acoustic encoder
backbone in the proposed framework. ImageBind (Girdhar et al., 2023) extends contrastive
alignment across six modalities — audio, image, text, depth, thermal, and inertial — achieving
top-1 zero-shot audio-to-image retrieval accuracy of approximately 42% on ImageNet, though
retrieval rather than generation is its primary contribution. Zhu et al. (2022) survey this
entire audio-visual learning tradition through 2022 and identify urban and geographic contexts
as the central unexplored frontier.

A critical consensus across all reviewed audio-visual papers is the absence of geographic
grounding. Every system trains and evaluates on general non-urban benchmarks — VEGAS,
VGGSound, AudioCaps, SoundNet-Flickr — and none incorporates ISO 12913 soundscape
descriptors, OSM land use metadata, or spatial regression of generation quality. Chen et al.
(2025), the most recent near-duplicate work, evaluated sound-vision alignment across NYC
street-level data and reported a CLIP alignment score of approximately 0.31, confirming that
acoustic-visual coherence is detectable in urban contexts, but this paper performs alignment
analysis only and explicitly performs no generative synthesis, no spatial regression, and
covers only a single city. Cross-Modal Urban Sensing therefore establishes the existence of
urban acoustic-visual coherence without providing a generative or spatially varying model.

*Positioning statement:* SoundScape-ControlNet addresses the gap that every existing
audio-to-image system uses abstract audio embeddings from non-urban benchmarks without ISO
12913 conditioning, OSM spatial context, or multi-city spatial regression — all three of
which are absent from Sound2Scene, Sound2Vision, SonicDiffusion, and the nearest
analysis-only urban work (Chen et al., 2025).

## 2.2 GeoAI Street-Level Synthesis and Urban Visual Analytics

Street-level imagery has become a dominant data source for urban analytics. Biljecki & Ito
(2021) synthesized over 600 published papers using Mapillary, Google Street View, and
equivalent open-license sources, mapping applications across health, transportation, safety,
vegetation, and socioeconomic inference. Their review explicitly identified acoustic-visual
fusion as an unexplored direction in urban visual intelligence. Biljecki et al. (2024),
revisiting the field in the Annals of the American Association of Geographers, named
acoustic-visual synthesis as "a key unexplored direction" in Urban Visual Intelligence —
providing direct editorial endorsement of the present paper's gap from within the target
community. The urban perception tradition anchored by Dubey et al. (2016) — Place Pulse 2.0's
1.17 million pairwise comparisons across 56 cities for safety, wealth, and beauty prediction
— established the benchmark for large-scale perceptual inference from street-level images,
though it predates the diffusion era and includes no soundscape component.

Generative synthesis from geographic metadata emerged as a sub-field with Mai et al. (2023,
ISPRS Journal of Photogrammetry and Remote Sensing), who trained a conditional diffusion model
on OSM building tags, land use classes, and demographic covariates from New York City, then
evaluated zero-shot transfer to London and Tokyo. This paper is the closest direct precursor
to the proposed framework: it shares the target venue, uses two of the three study cities,
employs conditional diffusion, and demonstrates cross-city generalization. The critical gap
is that Mai et al. (2023) include no acoustic conditioning channel whatsoever — the framework
is purely visual-spatial. ControlNet (Zhang & Agrawala, 2023), with over 8,000 citations and
demonstrating FID improvements over unconditioned diffusion on diverse spatial controls,
provides the foundational architecture on which the proposed dual-path system is built.
Uni-ControlNet (Zhao et al., 2023) extended this by unifying local spatial controls and
global semantic embeddings in a single framework, achieving FID 19.4 on COCO under
multi-condition generation — the Uni-ControlNet global-control pathway directly informs the
acoustic embedding injection design used here. The latent diffusion model (LDM) backbone
itself (Rombach et al., 2022), which demonstrated FID 7.76 on MS-COCO through latent-space
compression via a variational autoencoder and cross-attention-conditioned UNet, underpins
all diffusion-based street-level synthesis reviewed here.

Other street-level synthesis works have extended the frontier. Streetscapes (Deng et al.,
2024) produced long-sequence autoregressive video diffusion conditioned on language and map
layouts. DiffPlace (Wang et al., 2026) introduced geolocation embeddings and a spatial prior
for place-consistent generation. Text2Street (Zhang et al., 2024) adapted ControlNet to
text-conditioned street-view generation. Sat2Scene (Li et al., 2024) achieved FID
approximately 35 for satellite-to-street synthesis using a 3D diffusion architecture.
None of these systems incorporates acoustic conditioning. Cross-view synthesis from
satellite imagery (Toker et al., 2021) achieved FID approximately 30 for street-view
generation from satellite-street pairs, establishing the competitive range for street-level
FID targets. Multi-source fusion for urban scene understanding at scale is validated by Xia
et al. (2023), who combined satellite, street-level, and OSM data across 10 cities —
including NYC, London, and Singapore — for semantic segmentation (F1 approximately 0.83),
demonstrating that the exact three-city combination targeted by the proposed framework
supports cross-source fusion at geographic scale.

OSM-anchored spatial analysis has been validated as a framework for urban function
identification. Zhang et al. (2023, ISPRS Journal of Photogrammetry and Remote Sensing)
combined OSM topology and street-view imagery via a spatial graph neural network, achieving
urban function mapping R² approximately 0.82 across multiple cities. Hartmann et al. (2024)
used the Mapillary-plus-OSM pipeline for road surface quality detection globally. Both papers
confirm that open-license street-level imagery combined with OSM metadata supports
geographically generalizable urban sensing, but both are discriminative models with no
acoustic dimension. Janowicz et al. (2024) explicitly flag generative-spatial synthesis gaps
in their comprehensive GeoAI review, naming the combination of conditional diffusion with
geographic metadata as an emerging frontier. Ghamisi et al. (2021) provide a complementary
survey of GeoAI methods from CNNs to transformers in the ISPRS JPRS, confirming that
acoustic-visual generative models remain absent from the GeoAI literature.

*Positioning statement:* The proposed framework extends the GeoAI synthesis tradition of
Mai et al. (2023) by adding the acoustic modality — ISO 12913 perceptual descriptors and
CLAP embeddings — as a second conditioning channel absent from every existing GeoAI
synthesis system, and by introducing OLS/GWR/MGWR spatial regression over generation quality
metrics that no GeoAI synthesis paper, including Mai et al. (2023) and DiffPlace (Wang et al.,
2026), has applied.

## 2.3 Urban Soundscape Perception and ISO 12913

Urban soundscape science is anchored in ISO 12913-1 (2014), which defines soundscape as the
acoustic environment as perceived, experienced, and understood by a person or persons in
context. The standard establishes pleasantness and eventfulness as the primary perceptual
axes, with additional dimensions including vibrancy and appropriateness. Kang et al. (2018)
conducted a three-city field study that established that soundscape perception is jointly
determined by acoustic features, visual environment, temporal factors, and cultural context —
the cross-modal coupling result that motivates treating ISO 12913 descriptors as generative
conditioning signals rather than endpoints. That ISO 12913 pleasantness and eventfulness
co-vary with visual scene character was further confirmed by Qin et al. (2019), who analyzed
acoustic-visual spatial correspondence across 18 cities globally and found Pearson r of 0.52
to 0.74 in residential and commercial zones, dropping to approximately 0.30 in mixed-use
areas — a spatial heterogeneity in correspondence that directly motivates the GWR spatial
analysis component of the proposed framework.

The ARAUS dataset (Ooi et al., 2022), compiled from 25,440 human affective responses to
augmented soundscapes contributed by over 600 participants, provides the largest open
ISO 12913-annotated resource for training soundscape perception models. Watcharasupat et al.
(2022a) demonstrated that deep learning models can predict pleasantness and eventfulness
competitively on DCASE 2022 challenge data using CNN-transformer architectures, and
Watcharasupat et al. (2022b) established regression models for quantitative acoustic-to-
perception translation. Aletta et al. (2023) standardized ISO 12913 attribute terminology
across 18 languages through the SATP project, enabling cross-cultural descriptor
harmonization relevant to multi-city conditioning. Tarlao et al. (2024) used structural
equation modeling to demonstrate that appropriateness mediates the acoustic-quality
relationship in urban outdoor spaces, underscoring that the mapping from acoustic features
to perceptual quality is not a simple monotonic function and motivating the multi-signal
conditioning design used in the proposed framework.

The connection between acoustic features and physical urban form is validated quantitatively
by Liu et al. (2021), who demonstrated CNN-based noise prediction at 10-meter spatial
resolution using road type, building density, traffic count, and land use as covariates
(R² = 0.81, Guangzhou, projected to UTM Zone 49N, EPSG:32649), establishing that
OSM-derived spatial features carry strong predictive value for acoustic characterization.
Liang et al. (2020) fused street-level images and acoustic measurements via CNN late fusion
across Singapore and Hong Kong, achieving urban quality prediction R² approximately 0.67 —
the first paper to directly combine acoustic and visual street-level data in a predictive
urban model, though this work performs analysis rather than generation and does not apply
spatial regression. Mitchell et al. (2024) applied AI to automate soundscape enhancement
selection under the ISO 12913 framework in traffic-exposed residential areas. Lionello et al.
(2020) measured A-weighted SPL, psychoacoustic annoyance, and bioacoustic indices across 16
open spaces in three cities, confirming the multi-scale drivers of soundscape quality. The
health consequences of soundscape degradation, documented by Kempen et al. (2018) across
epidemiological studies, provide motivating context: WHO Europe estimates at least one
million disability-adjusted life years lost annually to traffic-related noise, underscoring
the practical urgency of tools that translate acoustic environments into visualizable urban
scenes.

Critically, no paper in the urban soundscape tradition synthesizes images from soundscape
signals. Every paper in this cluster treats soundscape as a measurement endpoint — something
to be predicted, assessed, or enhanced — rather than as a generative prior for visual output.
The proposed framework inverts this paradigm by treating ISO 12913 pleasantness, eventfulness,
and A-weighted SPL as structured conditioning inputs from which street-level imagery is
generated.

*Positioning statement:* This paper is the first to treat ISO 12913 perceptual descriptors
as structured generative priors for image synthesis: where the soundscape literature uses
these dimensions as dependent variables to be measured and predicted, SoundScape-ControlNet
inverts the pipeline and uses them as conditioning inputs, operationalizing the cross-modal
acoustic-visual coupling established by Kang et al. (2018) and Qin et al. (2019) as a
generative rather than analytical relationship.

## 2.4 Spatially Varying Regression for Urban Acoustic-Visual Analysis

Global linear regression systematically underperforms locally adaptive models for urban
acoustic-visual problems because the relationships between land use, building morphology, and
acoustic environment are non-stationary across space. Fotheringham et al. (2017) introduced
multiscale geographically weighted regression (MGWR) in the Annals of the American
Association of Geographers, extending single-bandwidth GWR by assigning each covariate its
own spatially adaptive bandwidth via backfitting — allowing predictors that operate at
fundamentally different spatial scales (road noise, locally concentrated; land use character,
regionally distributed) to be modeled simultaneously. With over 1,850 citations, MGWR is now
the standard approach where spatial scale heterogeneity among predictors is hypothesized. The
mgwr Python package (Oshan et al., 2019), with 680 citations, provides the open-source
implementation used in the geo_benchmark pipeline underlying the present paper, following the
bandwidth selection, local collinearity diagnostics, and bootstrap inference guidelines
formalized in Fotheringham et al. (2020).

Applied spatial regression papers establish the empirical foundation for the acoustic-visual
regression component. Fan et al. (2020, International Journal of Geographical Information
Science) applied GWR to London soundscape data at the borough scale — projected to British
National Grid (EPSG:27700) — and found GWR R² = 0.71 versus OLS R² = 0.54 for the
soundscape-land-use relationship, with residual Moran's I reduced to 0.08 after GWR
adjustment, closely approaching spatial independence. This Moran's I = 0.08 result serves as
the key benchmark for the spatial analysis section of the present paper, which targets MGWR
residual Moran's I ≤ 0.08 across all three study cities. Shen et al. (2022, IEEE Transactions
on Geoscience and Remote Sensing) modeled urban morphology, noise, and microclimate jointly
using GWR across multiple US cities (local UTM projections per city), achieving GWR R² = 0.78
and reducing OLS residual Moran's I from approximately 0.23 to 0.06 after GWR correction —
confirming the consistent pattern that spatial adjustment both improves fit and largely
eliminates residual autocorrelation. Li & Fotheringham (2019) demonstrated a scalable O(n)
GWR algorithm feasible for datasets exceeding 100,000 observations, establishing that the
method is computationally tractable at city scale. Emerging nonlinear extensions including
GWRBoost (Li et al., 2022), GWNN (Zhou et al., 2025), GNNWR (Li et al., 2022), and M-SGWR
(Liu et al., 2026) all report improvements over standard GWR on nonlinear urban datasets but
none has been applied to soundscape or image generation contexts.

The sole existing paper combining generative diffusion with GWR-based fidelity analysis is
Wei et al. (2025), who synthesized satellite imagery and applied GWR to evaluate spatially
varying generation quality across urban morphologies. This work demonstrates that generative
model fidelity is itself a spatially varying dependent variable explicable by local
covariates — directly anticipating the proposed paper's spatial analysis design. The critical
gap is that Wei et al. (2025) use satellite imagery rather than street-level scenes and
include no acoustic conditioning, leaving both dimensions open for the present contribution.

No existing paper applies OLS, GWR, or MGWR to explain spatial variation in street-level
image generation quality metrics — FID per grid cell, SSIM per location, or LPIPS per
spatial unit — as a function of acoustic and morphological covariates. SoundScape-ControlNet
addresses this gap directly by applying the three-model OLS/GWR/MGWR progression to
per-cell median LPIPS across 500-meter grid cells in NYC (UTM Zone 18N, EPSG:32618), London
(UTM Zone 30N, EPSG:32630), and Singapore (UTM Zone 48N, EPSG:32648), with Moran's I
reported for residuals of all three models and spatial cross-validation used throughout.

*Positioning statement:* This paper extends the spatial regression tradition from soundscape
perception modeling (Fan et al., 2020; Shen et al., 2022) and satellite image synthesis
analysis (Wei et al., 2025) to the novel dependent variable of per-cell street-level
generation fidelity (LPIPS), and applies MGWR across three contrasting global cities where
no prior GWR or MGWR analysis of generative model quality has been conducted.

---

**Table 1.** Comparison of generative and acoustic-visual approaches most related to the
proposed SoundScape-ControlNet framework. FID values are reported on each paper's primary
benchmark; street-level FID scores are not directly comparable with general-image benchmarks
owing to urban scene complexity. "–" indicates metric not reported.

| Study | Method | Audio conditioning | Spatial context | Evaluation | Key limitation |
|---|---|---|---|---|---|
| Sung-Bin et al. (2023) — Sound2Scene | Audio-visual latent alignment + GAN decoder | VEGAS / VGGSound raw audio | None | FID 28.3 (VEGAS) | General sounds only; no ISO 12913; no geographic framework; no spatial regression |
| Li et al. (2024) — Sound2Vision | LDM + cross-modal contrastive alignment + source localization | VEGAS / VGGSound raw audio | None | FID ~24 (VEGAS) | No urban / geographic specificity; no ISO 12913; no spatial analysis |
| Biner et al. (2024) — SonicDiffusion | Cross-attention audio adapter on frozen Stable Diffusion | AudioCaps raw audio | None | Qualitative coherence | No urban soundscape; no ISO 12913; no geographic framework |
| Chen et al. (2025) — Cross-Modal Urban Sensing | CLIP cosine similarity analysis (no generation) | NYC street audio | NYC streets (single city, analysis only) | CLIP alignment ~0.31 | Analysis only — no generative synthesis; no GWR; single city |
| Mai et al. (2023) — GeoAI Synthesis | Conditional diffusion on OSM metadata | None | OSM tags + building footprints + demographics; NYC / London / Tokyo | FID reported; zero-shot transfer | No acoustic conditioning; no soundscape; no spatial regression |
| Wei et al. (2025) — Diffusion + GWR | Diffusion satellite synthesis + GWR fidelity evaluation | None | Urban planning covariates (satellite imagery) | GWR spatially varying FID | Satellite not street-level; no acoustic conditioning |
| Zhao et al. (2023) — Uni-ControlNet | Unified local + global multi-condition ControlNet | None | Local: edges / depth / segmentation; Global: semantic embedding | FID 19.4 (COCO) | No audio conditioning; no geographic application |
| **SoundScape-ControlNet (proposed)** | **Dual-path ControlNet: local OSM spatial path + global CLAP + ISO 12913 acoustic path on Stable Diffusion v2.1** | **CLAP 512-dim + ISO 12913 pleasantness, eventfulness, LAeq (515-dim total)** | **OSM land use + GHS-BUILT-S building density + road hierarchy; NYC, London, Singapore** | **FID / SSIM / LPIPS per city and land use zone; OLS / GWR / MGWR on per-cell LPIPS; Moran's I on all residuals; zero-shot Singapore transfer** | **First combined ISO 12913-conditioned GeoAI synthesis system; cross-city coverage limited to three cities** |

---

The systematic review of 52 papers across four thematic clusters reveals a three-part gap
that no existing work closes: (1) every audio-to-image generation system operates without
urban soundscape semantics or geographic metadata; (2) every GeoAI street-level synthesis
system omits acoustic conditioning; and (3) no paper applies GWR or MGWR to explain spatial
variation in generative model fidelity at street level. Two editorial assessments in the
target community (Biljecki & Ito, 2021; Biljecki et al., 2024) name acoustic-visual fusion
as the key open direction in urban visual intelligence. SoundScape-ControlNet addresses all
three components simultaneously by combining ISO 12913-conditioned latent diffusion,
OSM-derived dual-path spatial control, and OLS/GWR/MGWR spatial analysis across NYC, London,
and Singapore — a combination absent from every prior paper reviewed.
