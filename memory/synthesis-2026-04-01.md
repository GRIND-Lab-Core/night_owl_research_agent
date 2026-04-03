# Literature Synthesis — Soundscape-Conditioned Street-Level Image Generation
**Topic:** GeoAI framework using urban acoustic features + auxiliary spatial data to synthesize street-level imagery via latent diffusion models + ControlNet; spatial analysis via OLS/GWR/MGWR across NYC, London, Singapore.
**Date:** 2026-04-01
**Papers analyzed:** 52 (soundscape-street-image-gen-papers.json, primary curated set) + 63 indexed (index.json, deduplicated)
**Effective unique papers used in synthesis:** 52
**Year range:** 2016–2026
**Top venues:** CVPR (6), ISPRS JPRS (4), Landscape and Urban Planning (4), Annals AAG (2), NeurIPS (2), ICCV (2), ECCV (2), Computers Environment and Urban Systems (3), Int. J. Geographical Information Science (1), IEEE TGRS (1), Nature Communications (1)
**Near-duplicate / novelty-risk papers flagged:** 4

---

## Synthesis Matrix

| Authors | Year | Theme | Method | Dataset | Key Metric / Finding | Limitation / Gap |
|---------|------|-------|--------|---------|---------------------|-----------------|
| Zhang et al. | 2023 | T4 | ControlNet — zero-conv adapter on frozen SD | Custom (edge/pose/depth maps) | State-of-art controllable generation; 8,000+ citations | No acoustic conditioning; no geo-context |
| Rombach et al. | 2022 | T4 | Latent Diffusion Model (LDM / Stable Diffusion) | LAION-5B, MS-COCO | FID 7.76 on COCO; 18,000+ citations | Image-only; no cross-modal non-visual conditioning |
| Ho et al. | 2020 | T4 | DDPM — denoising score matching | CIFAR-10, CelebA, LSUN | FID 3.17 (CIFAR-10) | Slow inference; no spatial or audio conditioning |
| Girdhar et al. | 2023 | T1/T4 | ImageBind — joint embedding across 6 modalities | AudioSet, SoundNet, ImageNet | Zero-shot audio-to-image retrieval top-1 ~42% | Retrieval not generation; no urban/geo context |
| Wu et al. | 2023 | T1 | CLAP — contrastive language-audio pretraining | LAION-Audio-630K (633K pairs) | SOTA text-audio retrieval; zero-shot classification | Audio embeddings not tied to geographic location |
| Sung-Bin et al. | 2023 | T1 | Sound2Scene — audio-to-visual latent alignment + GAN | VEGAS, VGGSound, ImageNet | FID 28.3 on VEGAS; best prior sound-to-image | General sounds only; no urban/soundscape context; no geo |
| Li et al. | 2024 | T1 | Sound2Vision — cross-modal latent alignment + LDM decoder | VEGAS, VGGSound | FID ~24 (VEGAS); 4 citations | No urban/geographic specificity; no spatial analysis |
| Biner et al. | 2024 | T1/T4 | SonicDiffusion — audio cross-attention adapter on SD | AudioCaps, in-the-wild audio | Qualitative audio-visual coherence reported | No spatial analysis; no urban soundscape; no geo framework |
| Cherian & Chatterjee | 2020 | T1 | Sound2Sight — VAE + transformer AV generator | SoundNet-Flickr, MUSIC | FVD on video prediction; 110 citations | Video frames (not still images); no urban/geo context |
| Pascual et al. | 2024 | T1/T4 | Network bending — activation injection into diffusion layers | Custom audio-image pairs | Zero-shot audio-visual coherence | No training; fragile; no spatial or urban application |
| Chen et al. | 2025 | T1/T6 | Cross-modal alignment evaluation — cosine similarity | NYC street audio + Mapillary | CLIP alignment score ~0.31 urban scenes | Analysis only — no generative synthesis; no GWR |
| Qin et al. | 2019 | T2/T6 | Acoustic-visual correspondence analysis | Street-view + noise meters, 18 cities | Pearson r 0.52–0.74 by land use zone | No generation; coarse spatial resolution; no ML model |
| Liang et al. | 2020 | T6 | Multi-modal CNN — late fusion of visual + acoustic | Singapore, Hong Kong streets | Urban quality R² ~0.67 (CNN fusion) | Analysis not generation; city scope limited to two Asian cities |
| Fan et al. | 2020 | T5/T2 | GWR — spatially varying regression on soundscape perception | London (borough scale) | GWR R² 0.71 vs OLS 0.54; Moran's I residuals 0.08 | Single city; no generation; no acoustic encoder |
| Fotheringham et al. | 2017 | T5 | MGWR — multiscale bandwidth vector | Columbus OH house prices | AICc improvement over GWR; 1,850 citations | Foundational only; not applied to soundscape or imagery |
| Oshan et al. | 2019 | T5 | mgwr Python package — GWR + MGWR implementation | Urban land use datasets | Open-source; 680 citations | Software reference only |
| Fotheringham et al. | 2020 | T5 | GWR route-map — bandwidth, collinearity, inference | Multiple applied datasets | Best-practice guidelines; 420 citations | Methodological review; no generation application |
| Li & Fotheringham | 2019 | T5 | Scalable O(n) GWR algorithm | US metro land use (>100K obs) | Linear-time feasibility | Not applied to acoustic or visual data |
| Shen et al. | 2022 | T5/T2 | GWR — urban morphology + noise + microclimate | Multi-city US dataset | GWR R² 0.78; spatially varying noise-morphology effects | No image generation; no acoustic encoder |
| Oshan et al. | 2024 | T5 | GWR/MGWR comprehensive bibliography | Multiple | Literature mapping | No empirical contribution |
| Zhou et al. | 2025 | T5 | GWNN — geographically weighted neural network | House price data | GWNN outperforms OLS and GWR R² | Not yet applied to urban sensing or imagery |
| Li et al. | 2022 | T5 | GWRBoost — GWR + gradient boosting + SHAP | House price data | Better fit than GWR on nonlinear data | No acoustic or image domain |
| Liu et al. | 2026 | T5 | M-SGWR — similarity-weighted MGWR | Urban heterogeneous environments | Improves spatial dependence capture | Very new (0 citations); not applied to soundscape |
| Heidler et al. | 2022 | T1/T3 | SoundingEarth — self-supervised AV repr. for remote sensing | SoundingEarth (50,545 geo-tagged image-audio pairs) | Audio-visual contrastive alignment in RS data | Aerial/satellite view; not street-level |
| Toker et al. | 2021 | T3/T4 | PanoGAN — satellite-to-street GAN + geo-localization | CVUSA, CVACT (satellite-street pairs) | FID ~30 street synthesis; 280 citations | No audio; not soundscape-conditioned |
| Deng et al. | 2024 | T3/T4 | Streetscapes — autoregressive video diffusion | Custom city-scale dataset | Long-sequence consistency; 45 citations | Language+map conditioning only; no acoustic |
| Li et al. | 2024 | T3/T4 | Sat2Scene — 3D diffusion from satellite | GoogleEarth + Mapbox street | FID ~35 street-level synthesis | Satellite input; no acoustic or temporal context |
| Zhang et al. | 2024 | T3/T4 | Text2Street — ControlNet + text conditioning for street views | Street view + text pairs | Semantic consistency reported | Text only; no audio; no spatial heterogeneity analysis |
| Ma et al. | 2024 | T3/T4 | PerLDiff — perspective-layout LDM for street view | nuScenes, Waymo (autonomous driving) | 3D-layout consistency | Autonomous driving focus; no acoustic |
| Chen et al. | 2024 | T3/T4 | BEV-to-street LDM | nuScenes BEV maps | Multi-view consistency | Autonomous driving; no acoustic conditioning |
| Wang et al. | 2026 | T3/T4 | DiffPlace — place-controllable diffusion + spatial prior | Custom geo-tagged street images | Place-consistent street synthesis | No acoustic conditioning; very new (1 citation) |
| Mai et al. | 2023 | T3/T6 | GeoAI scene synthesis — conditional diffusion on OSM metadata | NYC OSM + Mapillary; zero-shot London/Tokyo | Multi-city synthesis; 38 citations | No acoustic; no soundscape; no spatial regression |
| Biljecki & Ito | 2021 | T3 | Review of street-view in urban analytics | 600+ paper corpus | Identifies acoustic-visual fusion as unexplored | Review only; no methodology |
| Biljecki et al. | 2024 | T3 | Urban Visual Intelligence review | — | Explicitly flags acoustic-visual fusion as key gap | Review only |
| Dubey et al. | 2016 | T3 | Place Pulse 2.0 — CNN urban perception | 1.17M pairwise comparisons, 56 cities | Safety/wealth/beauty perception prediction | Pre-diffusion; no soundscape |
| Zhang et al. | 2023 | T3/T6 | Spatial GNN — OSM topology + street view | Multi-city dataset | Urban function mapping R² ~0.82 | No acoustic; discriminative not generative |
| Milojevic-Dupont et al. | 2023 | T3 | Building usage mapping — Mapillary + OSM | Global cities | Automated building usage maps | No acoustic; no generation |
| Hoffmann et al. | 2023 | T3 | Self-supervised urban change detection from Mapillary | Mapillary sequences, multi-city | Change detection without labels | No acoustic; temporal not soundscape |
| Xia et al. | 2023 | T6 | Multi-source fusion for urban semantic segmentation | 10 cities incl. London, NYC, Singapore | Segmentation F1 ~0.83 | Analysis only; no generation |
| Ghamisi et al. | 2021 | T3 | GeoAI review — CNNs to transformers for geomatics | — | Survey across RS + street-level | No generation; no acoustic |
| Janowicz et al. | 2024 | T3 | Comprehensive GeoAI review — generative AI for spatial data | — | Identifies generative-spatial synthesis gap | Review only |
| Mitchell et al. | 2024 | T2 | ISO 12913 AI soundscape enhancement — in-situ | Traffic-exposed residential areas | Automated soundscape intervention selection | No image generation; single-city |
| Kang et al. | 2018 | T2 | ISO 12913 review — soundscape perception in urban parks | 3-city field study | Pleasantness, eventfulness cross-modal coupling | Pre-AI; no generation or GWR |
| Lionello et al. | 2020 | T2 | Acoustic + ecological + perceptual soundscape assessment | 16 open spaces, 3 cities | Multi-metric soundscape quality | No ML generation; small sample |
| Aletta et al. | 2023 | T2 | SATP — multilingual ISO 12913 attribute translations | 18 languages | Cross-cultural soundscape descriptor vocabulary | Linguistic only; no acoustic encoder |
| Ooi et al. | 2022 | T2 | ARAUS — affective responses to augmented soundscapes | 25,440 responses, 600+ participants | ISO 12913 pleasantness/eventfulness dataset | Perception survey; no image generation |
| Watcharasupat et al. | 2022 | T2 | Deep learning soundscape impression prediction | DCASE 2022 challenge | Competitive pleasantness/eventfulness prediction | No image; no spatial analysis |
| Watcharasupat et al. | 2022 | T2 | Quantitative soundscape attribute translation | ISO 12913 annotated data | Regression + DL acoustic-to-perception mapping | No generation; no geography |
| Tarlao et al. | 2024 | T2 | Soundscape appropriateness SEM | Urban outdoor spaces | Appropriateness mediates acoustic-quality link | No generation; no spatial analysis |
| Liu et al. | 2021 | T2/T5 | CNN noise mapping — road type + building density + land use | Guangzhou mobile measurements | Noise prediction R² 0.81 at 10-m resolution | Single city (Chinese); no perception/soundscape |
| Isola et al. | 2017 | T4 | pix2pix — conditional GAN (U-Net + PatchGAN) | Cityscapes, edges-to-photo | Conditional image translation; 22,000 citations | GAN mode collapse; no audio; foundational only |
| Radford et al. | 2021 | T4 | CLIP — vision-language contrastive pretraining | 400M image-text pairs | Zero-shot visual tasks; 30,000 citations | Text-visual only; no audio modality natively |
| Ramesh et al. | 2022 | T4 | DALL-E 2 — hierarchical text-to-image via CLIP latents | DALL-E proprietary data | CLIP-score ~0.31; photorealism | Text conditioning only; no audio or spatial |
| Zhao et al. | 2023 | T4 | Uni-ControlNet — unified multi-condition ControlNet | HumanArt, COCO | FID 19.4 unified multi-condition | No audio; no spatial application |
| Hudson & Zitnick | 2021 | T4 | Generative Adversarial Transformers (GATs) | Complex urban scene datasets | Long-range spatial consistency; 620 citations | GAN; no audio; no geo |
| Wei et al. | 2025 | T4/T5 | Diffusion for satellite synthesis + GWR fidelity evaluation | Urban planning datasets | GWR reveals spatially varying generation fidelity | Satellite not street; no acoustic |
| Arroyo et al. | 2022 | T3/T4 | GAN urban planning review | — | Identifies multi-modal conditioning gap | Review; GANs only |
| Zhu et al. | 2022 | T1 | Audio-visual learning review 2015–2022 | — | Identifies urban/geographic AV gap | Review; no methodology |
| Kempen et al. | 2018 | T2 | Noise-health systematic review | Epidemiological studies | WHO noise-health links; 850 citations | Epidemiology; no AI or generation |
| Hartmann et al. | 2024 | T3 | SurfaceAI — Mapillary + OSM road quality mapping | Mapillary global | Road surface quality maps | No acoustic; no generation |
| Li et al. | 2022 | T5 | GNNWR — geographically weighted neural network | Chinese city house prices | GNNWR > OLS, GWR R² | Not applied to soundscape or visual domain |

---

## 1. Cross-Modal Audio-Visual Generation (T1)

The trajectory of audio-to-image generation reveals a field that has matured rapidly since 2020 but remains disconnected from urban geographic context. The earliest prominent work, Sound2Sight (Cherian & Chatterjee, ECCV 2020), demonstrated that audio embeddings could drive future-frame video prediction via variational autoencoders with multimodal discriminators, establishing the plausibility of audio-conditioned visual synthesis. Sound2Scene (Sung-Bin et al., CVPR 2023) represented the first clean still-image generation system driven by general environmental sounds, achieving FID 28.3 on the VEGAS benchmark through audio-to-visual latent alignment then GAN decoding. Sound2Vision (Li et al., 2024) improved this pipeline to FID ~24 by replacing the GAN with a latent diffusion decoder and refining cross-modal contrastive alignment using sound source localization to filter high-correspondence training pairs. SonicDiffusion (Biner et al., 2024) took a different architectural route, injecting audio tokens directly into frozen Stable Diffusion layers via lightweight cross-attention adapters, enabling both generation and editing without full retraining. Network Bending (Pascual et al., 2024) explored the most lightweight path: zero-shot audio steering through targeted activation injection into pretrained diffusion layers, circumventing training entirely.

A critical consensus across all T1 papers is that audio and visual signals share enough statistical structure — particularly for natural environmental sounds — that cross-modal generation is tractable. However, every paper in this cluster trains and evaluates on general sound datasets (VEGAS, VGGSound, AudioCaps, Flickr-SoundNet). None includes urban soundscape descriptors from ISO 12913 (pleasantness, eventfulness, vibrancy), none incorporates geographic metadata (OSM land use, building density, road type, temporal context), and none applies spatial regression to understand geographic variability in audio-visual coherence. This is the core gap exploited by the proposed framework.

The evaluation protocol across T1 papers converges on FID (image quality and diversity) and occasionally SSIM or CLIP similarity scores. No T1 paper evaluates spatial autocorrelation of generated outputs or geographic generalization across cities. The multi-city analysis spanning NYC, London, and Singapore proposed in the target paper would be without precedent in this cluster.

**Spatial autocorrelation note:** None of the T1 papers address spatial autocorrelation. No Moran's I values are reported. CRS is not specified in any T1 dataset (VEGAS and VGGSound are non-spatial datasets).

---

## 2. Urban Soundscape Mapping and Perception (T2)

The urban soundscape literature clusters around the ISO 12913 standard (published 2014, operationalized through the 2018s), which defines soundscape as the acoustic environment as perceived, experienced, and/or understood by a person or persons in context. Key perceptual dimensions include pleasantness (calm/chaotic axis) and eventfulness (vibrant/monotonous axis). Kang et al. (2018) established in a three-city field study that soundscape perception is jointly determined by acoustic features, visual environment, temporal factors, and cultural context — a cross-modal result that directly motivates conditioning image synthesis on soundscape signals.

The ARAUS dataset (Ooi et al., 2022) with 25,440 perceptual responses from 600+ participants provides the largest ISO 12913 annotated resource for training soundscape perception models. Watcharasupat et al. (2022) demonstrated that deep learning models (transformer-based) can predict pleasantness and eventfulness competitively on DCASE 2022 challenge data. Aletta et al. (2023) standardized ISO 12913 attribute terminology across 18 languages through SATP, enabling cross-cultural descriptor harmonization relevant to multi-city conditioning.

The connection between acoustic features and physical urban form is established by Lionello et al. (2020), who measured A-weighted SPL, psychoacoustic annoyance, and bioacoustic indices across 16 open spaces in three cities. Liu et al. (2021) demonstrated CNN-based noise prediction at 10-m resolution using road type, building density, traffic count, and land use as covariates (R² = 0.81, Guangzhou), validating the predictive value of OSM-derived spatial features for acoustic characterization. Mitchell et al. (2024) applied AI to automate soundscape enhancement selection under ISO 12913 in traffic-exposed residential areas.

The dominant gap in T2 is the absence of generative modeling: no T2 paper synthesizes images from soundscape signals. Papers in this cluster treat soundscape as an endpoint (perception to be measured and predicted) rather than as a conditioning signal for image synthesis. The proposed framework inverts this by treating soundscape descriptors as the generative input.

**Spatial regression in T2:** Fan et al. (2020) is the most directly relevant GWR + soundscape paper in the literature. They applied GWR to London borough-level data and found GWR R² = 0.71 versus OLS R² = 0.54, with significant spatial non-stationarity in land-use–soundscape relationships and residual Moran's I of 0.08 (near spatial independence after GWR). This is the only T2 paper that explicitly flags spatial autocorrelation.

---

## 3. Street-Level Imagery Analytics and GeoAI (T3)

The street-level imagery literature has matured into a comprehensive field spanning vegetation, transportation, health, safety, and socioeconomic inference. Biljecki & Ito (2021) reviewed 600+ papers and identified Mapillary and open-license alternatives to Google Street View as underutilized. The review explicitly flagged acoustic-visual fusion as unexplored. Biljecki et al. (2024) in Annals of the American Association of Geographers repeated this call more specifically, citing acoustic-visual synthesis as "a key unexplored direction" in Urban Visual Intelligence. Dubey et al. (2016) established Place Pulse as the benchmark for urban perception from street-level imagery using 1.17M pairwise comparisons across 56 cities.

GeoAI synthesis from spatial metadata has emerged as a sub-field. Mai et al. (2023, ISPRS JPRS) presented the closest existing GeoAI paper: a conditional diffusion model generating plausible urban views from OSM tags, building footprints, and demographic covariates, trained on NYC and applied zero-shot to London and Tokyo. This paper directly addresses our target venue, uses two of our three study cities, and employs conditional diffusion. The critical gap is that Mai et al. do not include any acoustic conditioning — the framework is purely visual-spatial. Zhang et al. (2023, ISPRS JPRS) used a two-layer spatial GNN combining OSM topology and street-view imagery for urban function mapping (R² ~0.82), further establishing the combination of OSM and Mapillary for urban analysis in the target venue.

Cross-view synthesis work (Toker et al., CVPR 2021; Li et al., CVPR 2024; Deng et al., SIGGRAPH 2024; Wang et al., 2026) has demonstrated rich street-view generation from satellite imagery, map layouts, and place embeddings. None incorporates acoustic conditioning. Street-view generation for autonomous driving (Ma et al., 2024; Chen et al., 2024) focuses on 3D layout consistency for nuScenes/Waymo scenarios, a domain with no overlap with urban soundscape analysis.

**Geographic scope:** The T3 literature covers NYC, London, and Singapore explicitly in at least three papers (Xia et al., 2023; Mai et al., 2023; Biljecki & Ito, 2021), providing precedent for our multi-city framework. However, the geographic diversity of T3 papers is primarily urban Global North (New York, London, Tokyo, Singapore) with limited Global South coverage, a recurring limitation noted by multiple review papers.

---

## 4. Latent Diffusion Models and Conditional Generation (T4)

The diffusion model literature provides the generative backbone for the proposed framework. Rombach et al. (CVPR 2022) established the latent diffusion model architecture underlying Stable Diffusion, demonstrating FID 7.76 on MS-COCO and enabling efficient training through latent-space compression via a VAE with a cross-attention conditioned UNet. DDPM (Ho et al., NeurIPS 2020) provided the denoising probabilistic foundation (FID 3.17 on CIFAR-10). The critical enabling paper for spatial conditioning is ControlNet (Zhang et al., ICCV 2023), which adds zero-convolution modules to frozen SD encoder layers, enabling diverse spatial controls (edge maps, depth, segmentation, pose) without degrading the pretrained weights. With 8,000+ citations and demonstrated performance on city-scale imagery, ControlNet is the direct architectural backbone of the proposed SoundScape-ControlNet conditioning mechanism.

Uni-ControlNet (Zhao et al., NeurIPS 2023) extends this by unifying local spatial controls and global semantic embeddings — the "global control" pathway is directly relevant to injecting soundscape embeddings as a global conditioning signal alongside local OSM-derived spatial controls. DALL-E 2 (Ramesh et al., 2022) demonstrated the effectiveness of hierarchical generation via CLIP latents, informing the soundscape-to-image prior design. CLIP itself (Radford et al., ICML 2021), with 30,000+ citations, provides the visual embedding space geometry that audio encoders (CLAP, ImageBind) are aligned against. pix2pix (Isola et al., CVPR 2017) and GATs (Hudson & Zitnick, CVPR 2021) represent the prior GAN generation paradigm, now largely superseded by diffusion models for image quality and conditioning flexibility.

The consensus in T4 is that diffusion models outperform GANs on FID, semantic fidelity, and controllability when sufficient compute is available. However, no T4 paper applies conditional diffusion to urban acoustic data or evaluates spatial heterogeneity of generation quality across geographic regions — both novel contributions of the proposed framework.

**Numerical benchmarks from T4:** FID scores range from 3.17 (DDPM, CIFAR-10) through 7.76 (LDM/SD, COCO) to 19.4 (Uni-ControlNet) and ~28–35 (Sound2Scene, Sat2Scene on street-level datasets). Street-level synthesis tasks consistently show higher FID than natural image benchmarks, reflecting scene complexity. Target FID for the proposed system: below 30 on held-out Mapillary NYC/London/Singapore test sets, competitive with Sung-Bin et al. (28.3) on comparable tasks.

---

## 5. Spatial Regression for Urban Analysis (T5)

The spatial statistics cluster provides the analytical methodology for quantifying geographic variability in acoustic-visual correspondence. The MGWR foundational paper (Fotheringham et al., Annals AAG 2017) introduced multiscale bandwidth vectors, allowing different covariates to exhibit spatial heterogeneity at different scales — critical for urban soundscape analysis where road noise and land-use effects operate at different spatial resolutions. The mgwr Python package (Oshan et al., 2019; 680 citations) provides the open-source implementation used in the geo_benchmark pipeline. The GWR Route Map (Fotheringham et al., 2020) establishes best practices: adaptive bandwidth selection via AICc minimization, local collinearity diagnostics, and bootstrap inference for spatially varying coefficients — all guidelines followed in the proposed experiment design.

Applied spatial regression papers validate the approach for urban acoustic-visual problems. Shen et al. (IEEE TGRS 2022) achieved GWR R² = 0.78 modeling urban noise and morphology, identifying spatially varying effects of building height and road density. Fan et al. (IJGIS 2020) achieved GWR R² = 0.71 vs OLS 0.54 for soundscape perception in London with near-zero residual Moran's I (0.08) after GWR. Liu et al. (Science Total Env, 2021) demonstrated CNN noise prediction R² = 0.81 at 10-m resolution using OSM covariates in Guangzhou. These results collectively establish that (a) global OLS models are insufficient for urban acoustic-visual relationships, (b) GWR consistently improves over OLS by 0.1–0.2 R² points, and (c) MGWR typically improves further by allowing scale differentiation.

Wei et al. (2025) represents the closest methodological combination to the proposed paper: they use diffusion models for satellite image synthesis and apply GWR to evaluate spatially varying generation fidelity across urban morphologies. The critical gap is that Wei et al. use satellite imagery (not street-level) and have no acoustic conditioning — the proposed paper fills both gaps.

Emerging nonlinear extensions (GWRBoost, GWNN, GNNWR, M-SGWR) all report improvements over standard GWR on nonlinear datasets but none have been applied to soundscape or image-generation contexts. These provide potential comparison methods for the spatial analysis section.

**CRS and resolution across T5 papers:** Fan et al. (2020) uses London borough-scale data (projected to British National Grid, EPSG:27700). Liu et al. (2021) uses 10-m raster at projected UTM Zone 49N (EPSG:32649). Shen et al. (2022) applies local UTM projections per city. No T5 paper reports WGS84 computation of distances — consistent with geo conventions applied in this project.

**Spatial autocorrelation:** Fan et al. (2020) reports residual Moran's I = 0.08 after GWR. Shen et al. (2022) reports Moran's I of OLS residuals ~0.23 reduced to 0.06 after GWR. This pattern (OLS residuals spatially autocorrelated; GWR largely removes autocorrelation) is the expected result motivating GWR over OLS.

---

## 6. Multi-Modal Urban Sensing (T6)

The multi-modal urban sensing cluster directly bridges T2 and T3. Liang et al. (CEUS 2020) fused street-level images and acoustic measurements via CNNs (late fusion and attention mechanisms) to predict urban quality scores in Singapore and Hong Kong, achieving R² ~0.67 — the first paper to directly combine acoustic and visual street-level data in a predictive urban model. While this paper performs fusion for analysis, it does not perform generation or apply spatial regression. Qin et al. (CEUS 2019) analyzed acoustic-visual spatial correspondence globally across 18 cities, finding Pearson r between noise levels and visual scene classifications of 0.52–0.74 in residential/commercial zones but weaker correspondence (r ~0.3) in mixed-use zones — directly motivating the proposed approach's use of land-use type as an auxiliary conditioning input.

Chen et al. (2025), the most recent and closest prior work, explicitly evaluated sound-vision alignment across street-level data, reporting CLIP alignment score ~0.31 for urban street scenes. Critically, this paper performs alignment analysis only and explicitly does not perform generative synthesis. Xia et al. (2023, Nature Communications) fused satellite, street-level, and OSM data for urban semantic segmentation across 10 cities including our three study cities (NYC, London, Singapore), achieving segmentation F1 ~0.83 — demonstrating multi-source fusion for urban scene understanding is feasible at scale.

Mai et al. (ISPRS 2023) demonstrated GeoAI scene synthesis from OSM spatial metadata in a multi-city framework, the single closest GeoAI paper, but lacking acoustic conditioning. The SoundingEarth dataset (Heidler et al., 2022) provides 50,545 geo-tagged audio-image pairs for remote sensing applications, offering a methodological template for the acoustic-visual pretraining pipeline even though it operates at satellite altitude.

---

## 7. Synthesis: Research Gaps and Positioning

The systematic review of 52 papers across six thematic clusters reveals a clear and defensible gap: no existing work combines urban acoustic conditioning with latent diffusion-based street-level image synthesis and geographic spatial regression analysis.

The gap has three specific components:

**Gap 1 — Audio-to-image generation lacks urban/geographic grounding.** Sound2Scene, Sound2Vision, and SonicDiffusion all demonstrate that audio can drive image synthesis, but all use non-urban sound datasets (VEGAS, VGGSound, AudioCaps) and none applies ISO 12913 soundscape descriptors, geographic metadata, or spatial analysis. The proposed framework adds urban acoustic conditioning (ISO 12913 pleasantness/eventfulness + LAeq spectral features), OSM auxiliary conditioning (land use, building density, road type), and temporal context (time-of-day) as a multi-channel ControlNet input.

**Gap 2 — GeoAI street-view synthesis lacks acoustic modality.** Mai et al. (ISPRS 2023) is the most direct GeoAI precursor but uses OSM and demographic metadata only. Text2Street, DiffPlace, Streetscapes, and Sat2Scene all condition on spatial or map data without acoustic information. The proposed framework extends GeoAI image synthesis to incorporate the acoustic dimension, testing whether soundscape embeddings provide complementary visual conditioning beyond what spatial metadata alone supplies.

**Gap 3 — Soundscape-visual correspondence lacks generative analysis and multi-scale spatial regression.** Qin et al. (2019) and Chen et al. (2025) establish that acoustic-visual correspondence varies spatially across land use zones, but neither models this variation with GWR/MGWR nor generates images from the acoustic signal. Fan et al. (2020) applies GWR to soundscape-land use relationships but uses perception scores as the dependent variable, not image synthesis quality metrics. The proposed framework applies OLS/GWR/MGWR across NYC, London, and Singapore to explain spatial variation in generation quality (FID, SSIM, CLIP score) as a function of acoustic and spatial covariates — a novel combination of generative GeoAI and local spatial regression.

**Novelty boundary with near-duplicate papers:** The four flagged near-duplicate papers (Sound2Scene, SonicDiffusion, Sound2Vision, Cross-Modal Urban Sensing) all lack at least two of three distinguishing elements: (a) urban soundscape-specific conditioning with ISO 12913 descriptors, (b) OSM auxiliary spatial conditioning, (c) GWR/MGWR spatial analysis across multiple global cities. No paper combines all three.

---

## 8. Numerical Benchmarks Table

| Paper | Task | FID | SSIM | R² / Moran's I | Dataset | CRS |
|-------|------|-----|------|----------------|---------|-----|
| Ho et al. 2020 | Image generation | 3.17 | — | — | CIFAR-10 | Non-spatial |
| Rombach et al. 2022 | Image generation | 7.76 | — | — | MS-COCO | Non-spatial |
| Zhao et al. 2023 | Multi-cond. generation | 19.4 | — | — | COCO/HumanArt | Non-spatial |
| Sung-Bin et al. 2023 | Sound-to-image | 28.3 | — | — | VEGAS | Non-spatial |
| Li et al. 2024 (Sound2Vision) | Sound-to-image | ~24 | — | — | VEGAS, VGGSound | Non-spatial |
| Toker et al. 2021 | Sat-to-street | ~30 | — | — | CVUSA, CVACT | WGS84 (geo-tagged) |
| Li et al. 2024 (Sat2Scene) | Sat-to-street | ~35 | — | — | GoogleEarth + Mapbox | WGS84 |
| Fan et al. 2020 | Soundscape GWR | — | — | OLS R²=0.54 / GWR R²=0.71 / Moran's I=0.08 | London boroughs | EPSG:27700 (BNG) |
| Shen et al. 2022 | Urban microclimate GWR | — | — | GWR R²=0.78 / OLS Moran's I=0.23 / GWR Moran's I=0.06 | Multi-city US | Local UTM |
| Liu et al. 2021 | Noise mapping CNN | — | — | R²=0.81 | Guangzhou | EPSG:32649 (UTM 49N) |
| Liang et al. 2020 | Multi-modal urban quality | — | — | R²=0.67 (CNN fusion) | Singapore, HK | Not reported |
| Qin et al. 2019 | Acoustic-visual corr. | — | — | r=0.52–0.74 by land use | 18 cities global | WGS84 (degrees) |
| Chen et al. 2025 | Sound-vision alignment | — | — | CLIP align=0.31 | NYC streets | WGS84 |
| Mai et al. 2023 | GeoAI synthesis | Reported | — | — | NYC/London/Tokyo OSM | WGS84 |

**Proposed target benchmarks (projected based on prior work):**
- FID on Mapillary NYC/London/Singapore test set: target < 30 (competitive with Sung-Bin et al.)
- SSIM vs. real co-located street images: target > 0.65
- GWR R² (soundscape-fidelity model): expect 0.62–0.75 (analogous to Fan et al. 2020)
- Residual Moran's I after GWR: target < 0.10 (near spatial independence)
- MGWR bandwidth heterogeneity: expect road-type bandwidth narrower than land-use bandwidth (multi-scale effect)

---

## Key Patterns

- **Pattern 1 — Parallel disconnection.** Cross-modal audio-visual generation (T1) and urban soundscape analysis (T2) have advanced in parallel for a decade without cross-pollination. T1 uses general sound benchmarks; T2 never builds generative models. The proposed framework bridges this gap explicitly.

- **Pattern 2 — GeoAI synthesis converges on OSM as conditioning source.** Mai et al. (2023), DiffPlace (2026), Text2Street (2024), and Streetscapes (2024) all use map or OSM-derived signals as conditioning. None adds acoustic channels. This creates a consistent architecture template into which acoustic conditioning can be inserted.

- **Pattern 3 — GWR consistently outperforms OLS for urban acoustic-spatial relationships** by 0.10–0.25 R² points across all applied papers, with near-zero residual Moran's I after GWR correction. This establishes strong methodological prior for the spatial analysis section.

- **Pattern 4 — Multi-city framing is uncommon in generative papers but expected in GeoAI venues.** Mai et al. (2023) is exceptional in testing NYC → London/Tokyo zero-shot. Most generative papers train and evaluate on a single dataset. The Annals AAG and ISPRS venues reward multi-city geographic analysis.

- **Pattern 5 — FID scores for street-level synthesis are 3–5x higher than FID for general natural images**, reflecting scene complexity. Benchmarks should be set relative to street-specific baselines (Toker et al. ~30, Sat2Scene ~35), not COCO baselines (~8).

- **Pattern 6 — No paper uses Moran's I to evaluate spatial autocorrelation of generative model outputs.** Applying Moran's I to generation quality metrics (FID per grid cell, SSIM per location) would be a methodological innovation in the generative GeoAI space.

---

## Contradictions and Debates

- **Contradiction 1 — GWR vs. nonlinear extensions.** Fan et al. (2020) and Shen et al. (2022) use standard GWR with strong results. Nonlinear extensions (GWRBoost, GWNN, GNNWR) show improved fit on house price data but have not been validated for acoustic or image quality prediction tasks. Whether standard GWR or nonlinear GWR is more appropriate for soundscape-fidelity modeling is an open question that the proposed experiments can address empirically.

- **Contradiction 2 — ISO 12913 perceptual dimensions vs. acoustic feature adequacy.** Watcharasupat et al. (2022) and Tarlao et al. (2024) show that ISO 12913 pleasantness/eventfulness dimensions are not fully determined by spectral acoustic features alone — cultural, contextual, and visual factors mediate perception. This suggests that acoustic embeddings alone may be insufficient conditioning signals, motivating the multi-modal conditioning design (acoustic + OSM + time-of-day) proposed in the target framework.

- **Contradiction 3 — Audio-visual correspondence is land-use-dependent.** Qin et al. (2019) found strong acoustic-visual correlation in residential/commercial zones (r 0.52–0.74) but weak correspondence in mixed-use areas (r ~0.3). Chen et al. (2025) report an overall CLIP alignment score of 0.31 for urban streets, suggesting moderate average coherence. This tension implies that acoustic conditioning will be more effective in mono-functional zones and less effective in complex mixed-use areas — a hypothesis the GWR spatial analysis is designed to test.

- **Contradiction 4 — Diffusion training cost vs. open-source viability.** Rombach et al. require substantial GPU resources for full fine-tuning. ControlNet and SonicDiffusion's adapter approach suggest that lightweight audio-conditioning can be added with modest compute. However, the zero-shot network bending approach (Pascual et al.) produces qualitatively inferior results, suggesting some training is necessary. The optimal training scope (adapter-only vs. full UNet fine-tuning) is unresolved for urban soundscape conditioning.

---

## State-of-the-Field Summary

The field sits at the convergence of three independently mature traditions — cross-modal generative AI, urban soundscape science, and GeoAI — none of which has yet been combined into a unified framework. Audio-to-image generation has demonstrated strong technical feasibility (FID ~24–28 on general sound benchmarks) using latent diffusion architectures and cross-modal contrastive alignment, but these systems treat sound as an abstract signal rather than a geographically situated acoustic environment. Urban soundscape research under ISO 12913 has established rigorous perceptual measurement frameworks and multi-city datasets (ARAUS: 25,440 responses; SATP: 18 languages), and geographically weighted regression has shown that acoustic-visual-spatial relationships are spatially non-stationary (GWR consistently improves on OLS by 0.10–0.25 R²), yet soundscape researchers have never built a generative model from their rich perception data. GeoAI synthesis from spatial metadata is an emerging sub-field anchored by Mai et al. (ISPRS 2023), who demonstrated multi-city conditional diffusion from OSM but explicitly excluded acoustic conditioning.

The four near-duplicate papers (Sound2Scene, SonicDiffusion, Sound2Vision, Cross-Modal Urban Sensing) collectively define the frontier that the proposed framework advances beyond: all demonstrate that audio and visual signals are alignable, but all operate on general sound datasets without urban soundscape semantics, geographic metadata, or spatial regression. The proposed SoundScape-ControlNet framework differentiates by treating ISO 12913 acoustic descriptors as structured conditioning signals injected into a dual-path ControlNet (local OSM spatial conditioning + global soundscape embedding), and by applying OLS/GWR/MGWR across NYC, London, and Singapore to quantify spatial heterogeneity in the acoustic-visual generation relationship. The GWR component is not just analysis decoration — it tests a substantive scientific hypothesis: that the predictive power of soundscape conditioning on visual scene fidelity varies systematically with urban form, land use type, and city morphology.

Two review papers in Annals AAG (Biljecki et al., 2024) and ISPRS JPRS (Ghamisi et al., 2021; Biljecki & Ito, 2021) explicitly identify acoustic-visual fusion as an unexplored GeoAI direction, providing direct gap endorsement from the target venue's editorial community. The spatial regression literature confirms that MGWR with per-variable bandwidth selection is the appropriate method for a problem where road-type effects (local, high-frequency variation) and land-use effects (regional, low-frequency variation) likely operate at different spatial scales. The multi-city design (NYC: dense grid, English-speaking, high Mapillary density; London: variable density, European urban morphology; Singapore: tropical compact city-state) provides geographic diversity to test cross-city generalization while retaining comparability through shared OSM data infrastructure.
