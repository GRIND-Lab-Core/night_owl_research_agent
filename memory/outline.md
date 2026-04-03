# Paper Outline
Title: SoundScape-ControlNet: A Dual-Path GeoAI Framework for Soundscape-Conditioned Street-Level Image Synthesis with Spatially Varying Generation Quality Analysis
Target venue: ISPRS Journal of Photogrammetry and Remote Sensing
Word budget: 10,000 words
Date: 2026-04-02

---

## Abstract (~250 words)

Key claims:
- Claim A1: A dual-path ControlNet architecture conditioning Stable Diffusion v2.1 on ISO 12913 soundscape descriptors (pleasantness, eventfulness, LAeq) combined with OSM spatial covariates achieves FID ≤ 30 on held-out Mapillary test imagery across NYC, London, and Singapore — a ≥ 10% improvement over CLAP-only baselines and ≥ 15% over text-only baselines.
- Claim A2: The dual-path model (OSM local path + acoustic global path) reduces FID by ≥ 8% relative to either path alone, with the advantage largest in mixed-use zones (FID improvement ~12%) and smallest in residential zones.
- Claim A3: MGWR applied to per-cell median LPIPS (k-NN k=8 spatial weights, UTM per city) achieves adjusted R² ≥ 0.65 and reduces residual Moran's I from ≥ 0.20 (OLS) to ≤ 0.08 (MGWR), demonstrating that generation fidelity is spatially non-stationary and explained by multi-scale acoustic-morphological covariates.
- Claim A4: Zero-shot transfer from NYC+London training to Singapore degrades FID by ≤ 15% for the dual-path model versus ≥ 25% degradation for acoustic-only conditioning, confirming that OSM spatial covariates are the cross-city generalizability enabler.

Key terms: soundscape-conditioned image synthesis, latent diffusion model, ControlNet, ISO 12913, urban soundscape, geographically weighted regression, MGWR, LPIPS, street-level imagery, GeoAI

---

## 1. Introduction (~800 words)

Subsections:
- 1.1 Motivation: the acoustic-visual gap in urban digital twins (~200 words)
- 1.2 Limitations of existing work (~200 words)
- 1.3 Contributions (~200 words, numbered list)
- 1.4 Paper organization (~100 words)

Key claims:
- Urban planners increasingly require street-level visualizations of proposed acoustic interventions, but no existing tool synthesizes street-level imagery directly from soundscape descriptions.
- The three prior paradigms (audio-to-image generation, GeoAI scene synthesis, soundscape-visual analysis) each address part of the problem but none combines all three: ISO 12913 conditioning, OSM auxiliary spatial control, and multi-scale spatial regression across contrasting cities.
- ISO 12913 perceptual descriptors (pleasantness, eventfulness) are established cross-modal predictors of visual scene character (Kang et al., 2018; Qin et al., 2019), but have never been inverted as generative conditioning signals.

Opens with: "The auditory and visual experiences of urban space are deeply coupled: a pedestrian who hears the rumble of traffic expects a different scene from one who hears birdsong, yet no computational framework has exploited this coupling to synthesize street-level imagery directly from soundscape descriptions."

Closes with: "Section 2 reviews the three relevant literature clusters and identifies the gap. Section 3 details the study area, datasets, dual-path architecture, and spatial analysis design. Section 4 reports generation fidelity, ablation results, and MGWR spatial decomposition. Section 5 interprets findings against prior benchmarks, discusses limitations, and identifies practical applications. Section 6 concludes with contributions and future directions."

Figures: Fig. 1 — Conceptual overview diagram showing the dual-path conditioning pipeline (soundscape path + OSM spatial path → Stable Diffusion → generated street-level image) alongside the GWR/MGWR spatial analysis loop. One-panel schematic, no map required. Located in Section 1.

Numbered contributions (to appear in Section 1.3):
1. First ISO 12913-conditioned latent diffusion framework for street-level image synthesis, incorporating pleasantness, eventfulness, and A-weighted SPL as structured perceptual conditioning signals alongside CLAP audio embeddings.
2. Dual-path ControlNet architecture (SoundScape-ControlNet) fusing local OSM spatial controls and global acoustic embeddings via separate zero-conv and cross-attention pathways, with learned per-resolution gating.
3. First application of OLS/GWR/MGWR spatial regression to generative model quality metrics (per-cell median LPIPS) as a spatially varying dependent variable, revealing multi-scale acoustic-morphological drivers of generation fidelity across NYC, London, and Singapore.
4. Multi-city generalization evaluation with zero-shot transfer to Singapore and quantified contribution of OSM spatial conditioning to cross-city robustness.

---

## 2. Literature Review (~1,500 words)

Subsections:
  2.1 Audio-to-image generation: from environmental sounds to urban scenes (~350 words)
      Covers: Sound2Sight, Sound2Scene (FID 28.3), Sound2Vision (FID ~24), SonicDiffusion,
              Network Bending; CLAP; ImageBind; consensus gap: no urban soundscape context,
              no ISO 12913, no geographic framework.
  2.2 GeoAI street-level synthesis and urban visual analytics (~400 words)
      Covers: Mai et al. (ISPRS 2023) — OSM-conditioned diffusion, key direct precursor;
              ControlNet (Zhang & Agrawala, ICCV 2023) and Uni-ControlNet (Zhao et al.,
              NeurIPS 2023); Stable Diffusion / LDM (Rombach et al., CVPR 2022);
              Toker et al. PanoGAN, Deng et al. Streetscapes, DiffPlace (Wang et al. 2026);
              Biljecki & Ito (2021) and Biljecki et al. (2024) calling for acoustic-visual fusion;
              Chen et al. (2025) sound-vision alignment analysis (no generation);
              gap: acoustic modality entirely absent from GeoAI synthesis.
  2.3 Urban soundscape perception and ISO 12913 (~350 words)
      Covers: Kang et al. (2018) cross-modal coupling; ARAUS dataset (Ooi et al., 2022);
              Watcharasupat et al. (2022) deep-learning pleasantness/eventfulness prediction;
              Aletta et al. (2023) SATP multilingual descriptors; Qin et al. (2019)
              acoustic-visual spatial correspondence (18 cities; r 0.52–0.74);
              Liang et al. (2020) multi-modal CNN fusion for urban quality;
              Mitchell et al. (2024) ISO 12913 AI soundscape enhancement;
              gap: ISO 12913 used as endpoint, never as generative conditioning input.
  2.4 Spatially varying regression for urban acoustic-visual analysis (~400 words)
      Covers: Fotheringham et al. (2017) MGWR; Oshan et al. (2019) mgwr package;
              Fotheringham et al. (2020) best-practice guidelines;
              Fan et al. (2020, IJGIS) GWR R²=0.71 vs OLS R²=0.54 for London soundscape
              (residual Moran's I=0.08 — key benchmark);
              Shen et al. (2022, TGRS) GWR for urban morphology + noise (R²=0.78);
              Wei et al. (2025) — diffusion synthesis + GWR fidelity evaluation on satellite
              imagery (closest methodological precedent; gap: no acoustic conditioning,
              no street-level);
              gap: no paper uses GWR/MGWR on generation quality metrics (FID/LPIPS/SSIM).

Key papers to cite (must-cite list):
1. Zhang & Agrawala (ICCV 2023) — ControlNet
2. Rombach et al. (CVPR 2022) — Stable Diffusion / LDM
3. Zhao et al. (NeurIPS 2023) — Uni-ControlNet
4. Girdhar et al. (CVPR 2023) — ImageBind
5. Wu et al. (2023) — CLAP
6. Sung-Bin et al. (CVPR 2023) — Sound2Scene (FID 28.3 baseline)
7. Mai et al. (ISPRS 2023) — OSM-conditioned GeoAI synthesis (direct precursor)
8. Kang et al. (Landscape Urban Planning 2018) — ISO 12913 cross-modal coupling
9. Ooi et al. (2022) — ARAUS ISO 12913 dataset
10. Fan et al. (IJGIS 2020) — GWR + soundscape (key spatial precedent)
11. Fotheringham et al. (Annals AAG 2017) — MGWR
12. Wei et al. (2025) — diffusion + GWR (closest combined precursor)
13. Biljecki et al. (Annals AAG 2024) — Urban Visual Intelligence (gap identifier)
14. Oshan et al. (2019) — mgwr Python package
15. Qin et al. (CEUS 2019) — acoustic-visual spatial correspondence

Positioning statement: "The proposed SoundScape-ControlNet framework is the first to combine ISO 12913 perceptual conditioning with OSM-derived spatial controls in a latent diffusion model for street-level image synthesis, and the first to apply OLS/GWR/MGWR to explain geographic variability in generative model fidelity — a capability not present in any prior audio-to-image, GeoAI synthesis, or soundscape-spatial regression paper."

---

## 3. Methodology (~2,500 words)

Subsections:
  3.1 Study Area and Spatial Data Infrastructure (~350 words)
      - Three cities: NYC (UTM Zone 18N, EPSG:32618), London (UTM Zone 30N, EPSG:32630),
        Singapore (UTM Zone 48N, EPSG:32648).
      - All raw data stored in WGS84 (EPSG:4326); reprojected to city-specific UTM for all
        distance, area, and spatial weight computations.
      - Spatial analysis units: 500 m grid cells (regular lattice) per city.
      - Temporal exclusion criterion: cells with >3-year gap between acoustic measurement
        date and median Mapillary image date are excluded; document per-city exclusion rate.
      - Study area boundaries: GADM v4.1 administrative boundaries with 1 km inward buffer
        to mitigate GWR edge effects (edge-zone cells retained for neighbor calculations,
        flagged in output maps with hatching).
      - Figure: Fig. 2 — Three-panel study area map (NYC / London / Singapore), each panel
        showing 500 m cell grid, OSM land use color coding, Mapillary image density per cell,
        and SoundingEarth audio point density. Include scale bar, north arrow, legend, inset
        global locator map. CRS labels per panel. Produced in UTM per city, displayed in
        EPSG:3857 for web-tile background.

  3.2 Data Acquisition and Preprocessing (~400 words)
      Subsection structure:
      3.2.1 Street-level imagery (Mapillary CC-BY-SA)
        - ≥ 5,000 images per city; spatially stratified by OSM land use class and road hierarchy.
        - Minimum 3 images per 500 m cell; cells with fewer excluded.
        - Per-image metadata: capture date, coordinates, heading; stored in WGS84,
          joined to UTM grid via point-in-polygon.
        - Temporal mismatch: per-cell acoustic measurement year vs. median imagery year documented;
          cells with |gap| > 3 years excluded.
      3.2.2 Acoustic data
        - SoundingEarth (~50,000 geotagged clips): matched to grid cells by geographic
          proximity ≤ 50 m in UTM; CLAP 512-dim embeddings extracted per clip.
        - Noise-Planet / NoiseCapture: crowdsourced LAeq; ordinary kriging to 500 m grid
          (UTM per city; variogram: spherical model; kriging weights computed in metric units).
        - BN-LOUD (London only): UK statutory road-traffic noise contours (LAden) at 10 m;
          zonal mean extracted per 500 m cell. Used in addition to Noise-Planet for London.
        - ARAUS (Ooi et al., 2022): 25,440 ISO 12913 pleasantness/eventfulness annotations;
          used to train the ISO 12913 prediction head (MLP on CLAP embeddings).
      3.2.3 Urban morphology covariates
        - OSM (Overpass API): land use (7 classes), building footprints, road hierarchy;
          rasterized to 256×256 control images at ~5 m/pixel in local UTM.
        - GHS-BUILT-S (100 m, ESA/JRC): building density surface; resampled to 500 m cells.
        - GHS-BUILT-H (100 m, ESA/JRC 2023): mean building height; extracted as zonal mean
          per 500 m cell; used as acoustic canyon proxy covariate.
        - NDVI proxy: Sentinel-2 Level-2A 10 m; summer composite (Jun–Aug) for NYC/London;
          dry-season composite (Feb–Apr) for Singapore; zonal mean per 500 m cell.

  3.3 SoundScape-ControlNet Architecture (~650 words)
      Subsection structure:
      3.3.1 Backbone and acoustic conditioning pathway
        - Backbone: Stable Diffusion v2.1 (CompVis open weights, 512×512 resolution); frozen.
        - Audio encoder: CLAP (LAION-AI, laion/larger_clap_music_and_speech, 512-dim); frozen.
        - ISO 12913 head: 3-layer MLP (hidden 256, ReLU, dropout 0.1) trained on ARAUS to
          predict pleasantness, eventfulness, and LAeq from CLAP embeddings.
        - Conditioning vector: CLAP 512-dim + ISO 12913 [pleasantness, eventfulness, LAeq]
          concatenated (515-dim total); projected via linear layer to SD hidden dim 1024;
          injected via cross-attention into all 12 UNet transformer blocks.
      3.3.2 Local OSM spatial conditioning pathway
        - ControlNet zero-conv adapter (lllyasviel open weights).
        - Input: 12-channel control raster — OSM land use one-hot (7 classes) + road
          hierarchy (4-level ordinal, rasterized) + GHS-BUILT-S density (continuous).
          All channels rasterized in local UTM at ~5 m/pixel, bilinearly resampled to 256×256.
      3.3.3 Dual-path fusion and training
        - Fusion: Uni-ControlNet-style learned gating; per-resolution-level weighted sum
          at 4 UNet resolution levels (64×64, 32×32, 16×16, 8×8).
        - Training: LoRA fine-tuning (rank r=16) on cross-attention layers only; SD backbone
          frozen; AdamW, lr=1e-4, 50K steps, batch 16, cosine LR decay with 1K warmup;
          random seed 42; 2× NVIDIA A100 80 GB.
        - Only adapter, gating, and LoRA weights trained; all pretrained backbone weights frozen.
      Key equations:
        - Conditioning vector: c = Linear(Concat(CLAP(a), MLP_ISO(CLAP(a))))
          where a is the audio clip; c ∈ R^{1024} after projection.
        - Dual-path output at resolution level l:
          h_l = σ(g_l) · h_local_l + (1 − σ(g_l)) · h_global_l
          where g_l is a learned scalar gate, σ is sigmoid.
        - Diffusion training loss: L = E_{x,c,ε,t}[||ε − ε_θ(x_t, t, c)||²₂]

  3.4 Ablation Design and Evaluation Protocol (~300 words)
      - Four-arm ablation (all arms use same Mapillary held-out test set, spatially stratified,
        500 locations per city, with temporal gap ≤ 3 years):
          Arm A: text-prompt-only ControlNet baseline
          Arm B: local OSM spatial path only (no acoustic global path)
          Arm C: global CLAP + ISO 12913 path only (no OSM local path)
          Arm D: dual-path full model (SoundScape-ControlNet)
      - Additionally Arm E: dual-path with ImageBind encoder instead of CLAP (encoder comparison).
      - Primary metrics: FID (city-level and per land use zone, ≥ 500 generated images per zone);
        SSIM (per image, aggregated to cell median); LPIPS (per image, aggregated to cell median).
      - Secondary: semantic segmentation class overlap (DeepLab v3+, 4 classes: road, vegetation,
        building, sky); CLAP cosine similarity between generated image description and source audio.
      - Statistical tests: paired Wilcoxon signed-rank on per-image LPIPS (Arm D vs. Arm C);
        Bonferroni correction for 3-city × 2-comparison (α = 0.05/6);
        bootstrap 95% CI on FID for all arm-vs-arm comparisons.
      - Cross-city transfer: train on NYC + London; evaluate zero-shot on Singapore; then
        fine-tune acoustic pathway on 500 Singapore pairs; report FID degradation %.
      Table: Table 1 — Ablation arm definitions (5 arms × dataset + model configuration).

  3.5 Spatial Analysis: OLS, GWR, and MGWR (~450 words)
      Subsection structure:
      3.5.1 Spatial unit and dependent variable
        - Spatial unit: 500 m grid cells in local UTM per city; cells require ≥ 3 Mapillary images
          and temporal gap ≤ 3 years.
        - Dependent variable: median per-cell LPIPS from Arm D generated images (lower = better).
          FID reported at city/zone level only (not cell level — insufficient image count per cell).
      3.5.2 Covariates and collinearity diagnostics
        - Independent variables: LAeq (kriged to 500 m grid), CLAP embedding PC1–PC3 (PCA to
          ≥ 80% variance), GHS-BUILT-S building density, GHS-BUILT-H building height, OSM road
          hierarchy index (weighted mean road classification per cell: motorway=5, primary=4,
          secondary=3, residential=2, path=1), NDVI proxy, ISO 12913 pleasantness estimate.
        - VIF diagnostic before GWR: remove covariates with VIF > 10; if |r| > 0.7 among
          acoustic variables, retain pleasantness + LAeq and drop eventfulness.
        - Report local condition number distribution for MGWR (flag cells where CN > 30).
      3.5.3 Spatial weights and Moran's I
        - Spatial weights: k-NN, k=8, built on projected UTM centroids (libpysal.weights.KNN).
        - Moran's I computed on raw LPIPS (pre-regression) and on OLS/GWR/MGWR residuals
          (esda.Moran, 999 permutations).
        - Moran's I correlogram: distances 500 m, 1 km, 2 km, 3 km, 5 km, 10 km (reported in
          supplementary) to document spatial dependence range before bandwidth selection.
        - Sensitivity check: k=4 and k=12 (supplementary table).
      3.5.4 OLS, GWR, and MGWR model specification
        - OLS: standard OLS with city dummy variables (London reference) for any pooled model;
          per-city OLS run first.
        - GWR: adaptive bisquare kernel; AICc golden-section bandwidth search over [10, min(n,500)]
          neighbors; per-city; max n = 5,000 (NYC hexagonal spatial subsample if n > 5,000).
        - MGWR: adaptive bisquare per covariate; backfitting, ε < 1e-5; per-city; max n = 3,000
          (stratified spatial hexagonal subsample using H3 resolution 8, ~460 m, stratified by
          land use class); minimum bandwidth floor k=20; mgwr Python package (Oshan et al., 2019).
        - If Singapore MGWR bandwidths collapse to global: report GWR as spatially varying model
          for Singapore; note limitation explicitly.
        - Reported for all models: AICc, adjusted R², spatial block CV RMSE (5 folds, block size
          ≥ 3× bandwidth radius; libpysal skater regionalization), Moran's I on residuals.
        - GWR/MGWR outputs: local R² maps, spatially varying coefficient maps (building density,
          road hierarchy, pleasantness) per city via geo_benchmark/evaluation/visualize.py.
        - MGWR per-variable bandwidths translated from k-neighbors to metric distance (multiply k
          by mean inter-cell spacing) and classified as local / regional / global per
          Fotheringham et al. (2017) terminology.
        - Additional baseline: spreg.ML_Error (PySAL spatial error model) if OLS residual
          Moran's I > 0.15 in any city.

Figures:
  - Fig. 1 — Conceptual pipeline overview (Section 1)
  - Fig. 2 — Three-panel study area maps (Section 3.1)
  - Fig. 3 — SoundScape-ControlNet dual-path architecture diagram showing the two conditioning
    pathways, UNet structure, cross-attention injection points, and gating mechanism (Section 3.3)

Tables:
  - Table 1 — Ablation arm definitions: 5 rows × columns: Arm ID, audio encoder, ISO 12913
    path, OSM spatial path, gating, description (Section 3.4)
  - Table 2 — Dataset summary: dataset name, city coverage, spatial resolution, CRS,
    record count, license, role in framework (Section 3.2)

---

## 4. Results (~2,000 words)

Subsections:
  4.1 Ablation results: generation fidelity across conditioning configurations (~500 words)
      - Lead result: Arm D (dual-path full model) achieves FID ≤ 30 pooled; ≥ 10% lower FID
        than Arm C (CLAP + ISO 12913 only) and ≥ 15% lower than Arm A (text-only baseline).
      - FID by city: NYC, London, Singapore — dual-path advantage largest in NYC commercial core
        and London mixed-use zones; smallest in Singapore residential areas.
      - FID by land use zone (commercial, residential, industrial, green): consistent dual-path
        advantage in commercial/mixed zones; near-parity in residential/green zones.
      - LPIPS and SSIM per arm, per city: Arm D median LPIPS lowest across cities;
        Wilcoxon p values (Bonferroni-corrected) for Arm D vs. Arm C.
      - Semantic segmentation class overlap (DeepLab v3+): Arm D ≥ 0.75 for building, road,
        vegetation, sky; improvement over Arm C reported in percentage points.
      - Arm E (ImageBind) vs. Arm C (CLAP): FID comparison; whether CLAP ≥ 5% lower FID than
        ImageBind in ≥ 2 cities; per-land-use-category breakdown.
      - Bootstrap 95% CI on FID for all arm-vs-arm comparisons (non-overlapping CIs confirm
        statistical significance).
      Report: all results without interpretation (save for Discussion).

  4.2 Spatial autocorrelation of generation quality (~300 words)
      - Global Moran's I on raw per-cell median LPIPS: statistic, z-score, pseudo-p value
        (999 permutations) per city and pooled; expected I ≈ 0.15–0.35.
      - Moran's I correlogram (supplementary) summarized: effective range of spatial dependence.
      - LISA cluster maps: HH/LL/HL/LH clusters per city; overlay with OSM land use.
      - Report: whether HH clusters (poor generation, high LPIPS) concentrate in
        commercial/industrial zones; LL clusters in residential/park zones.

  4.3 OLS, GWR, and MGWR model comparison (~600 words)
      - Per-city OLS results: adjusted R², coefficient table (building density, road hierarchy,
        pleasantness, LAeq, NDVI, building height, CLAP PC1–PC3), Moran's I on residuals.
      - GWR results per city: AICc vs. OLS AICc, adjusted R² improvement, Moran's I of
        GWR residuals; local R² map summary (mean, min, max local R²).
      - MGWR results per city: AICc vs. GWR AICc, adjusted R² improvement, Moran's I of
        MGWR residuals; per-variable bandwidths (k and approximate metric distance,
        classified local/regional/global).
      - Model selection summary: MGWR AICc < GWR AICc by ≥ 5 units; GWR AICc < OLS AICc
        by ≥ 10 units; MGWR residual Moran's I ≤ 0.08 in all cities.
      - Spatial block CV RMSE: 5-fold leave-one-block-out per city for OLS, GWR, MGWR.
      - Spatial error model (spreg.ML_Error) if triggered by OLS residual Moran's I > 0.15.
      - Building density and road hierarchy MGWR bandwidth comparison: confirm
        different bandwidths (local vs. regional scale) as evidence of multi-scale structure.

  4.4 Coefficient maps: spatially varying acoustic-morphological drivers (~300 words)
      - MGWR spatially varying coefficient maps for building density and road hierarchy per city.
      - GWR local R² maps per city (areas of better/worse model fit).
      - Narrative description of geographic patterns: where does building density explain
        generation fidelity strongly? Where does road hierarchy dominate?
      - ISO 12913 pleasantness coefficient: global or local bandwidth? direction of effect?
      - No interpretation in this subsection — pure reporting.

  4.5 Multi-city generalization: zero-shot transfer to Singapore (~300 words)
      - FID degradation (%) when Arm D trained on NYC+London is evaluated zero-shot on Singapore.
      - FID degradation for Arm C (acoustic only) on same Singapore test set.
      - Comparison: dual-path ≤ 15% degradation vs. acoustic-only ≥ 25% degradation.
      - Fine-tuning acoustic pathway on 500 Singapore pairs: FID recovery to ≤ 30.
      - Report LPIPS and SSIM for zero-shot and fine-tuned Singapore models.

Key results to report (specific metrics):
- FID per arm per city (5 arms × 3 cities = 15 values)
- LPIPS per arm per city (Wilcoxon p, Bonferroni-corrected)
- Global Moran's I on raw LPIPS per city (pre-regression)
- OLS adjusted R² per city; Moran's I on OLS residuals
- GWR adjusted R² per city; AICc improvement over OLS; Moran's I on GWR residuals
- MGWR adjusted R² per city; AICc improvement over GWR; Moran's I on MGWR residuals
- MGWR per-variable bandwidths (metric distances) for all covariates, per city
- Zero-shot Singapore FID degradation %

Figures:
  - Fig. 4 — Qualitative generation comparison: 4 rows (Arm A/B/C/D) × 3 columns (NYC/London/Singapore) grid of generated vs. ground-truth pairs; one representative location per city × arm. Include soundscape descriptor values and OSM context labels.
  - Fig. 5 — Bar chart: FID, LPIPS, and SSIM per arm per city (3 metric subplots × 5 arms × 3 cities, grouped by city). Error bars = bootstrap 95% CI.
  - Fig. 6 — LISA cluster maps: three-panel (NYC/London/Singapore) showing HH/LL/HL/LH clusters of raw per-cell median LPIPS overlaid on OSM land use background. Scale bar, north arrow, legend per panel.
  - Fig. 7 — MGWR spatially varying coefficient maps: building density coefficient (top row) and road hierarchy coefficient (bottom row) for NYC, London, Singapore (6 panels). Colour scale, scale bar, north arrow, boundary buffer hatching.
  - Fig. 8 — GWR local R² maps: one panel per city. Colour scale showing R² range.

Tables:
  - Table 3 — Ablation fidelity results: rows = 5 arms; columns = FID (NYC, London, Singapore, pooled), median LPIPS (NYC, London, Singapore), SSIM (pooled); Wilcoxon p (Arm D vs. C, Bonferroni). Best value per column in bold.
  - Table 4 — OLS/GWR/MGWR/SEM model comparison: rows = 4 models × 3 cities; columns = AICc, adjusted R², spatial block CV RMSE, Moran's I of residuals. Best value per column in bold.
  - Table 5 — MGWR per-variable bandwidths: rows = covariates (8); columns = NYC bandwidth (k, km, classification), London bandwidth, Singapore bandwidth.

---

## 5. Discussion (~1,200 words)

Subsections:
  5.1 ISO 12913 conditioning as a generative prior (~250 words)
      Key arguments:
      - Why structured perceptual descriptors (pleasantness, eventfulness) provide richer conditioning
        than raw CLAP embeddings alone: ISO 12913 dimensions are validated cross-modal signals
        co-varying with visual scene semantics (Kang et al., 2018; Qin et al., 2019); the
        MLP ISO 12913 head encodes domain knowledge that raw embeddings lack.
      - FID improvement of ≥ 10% over CLAP-only baseline (Arm C vs. Arm B) relative to prior
        work: compare to Sound2Scene FID 28.3 (VEGAS benchmark) and Sound2Vision FID ~24.
      - Magnitude and direction of improvement relative to previous state of the art.
      - Why NYC/London show stronger ISO 12913 gains than Singapore (ARAUS training distribution
        skewed toward Western urban soundscapes; Singapore tropical compact morphology less
        represented).

  5.2 Dual-path architecture and OSM spatial conditioning (~250 words)
      Key arguments:
      - Why OSM spatial path complements acoustic global path: local scene geometry (building
        density, road type) constrains visual structure at ~100 m scale while soundscape character
        operates at ~500 m neighborhood scale (consistent with MGWR bandwidth results).
      - Dual-path advantage largest in mixed-use zones: interpretation against MGWR coefficient
        maps — in mixed-use zones, neither acoustic nor spatial signal alone is sufficient
        because scene character is compositionally ambiguous.
      - Comparison to Mai et al. (ISPRS 2023) OSM-only approach: acoustic path adds measurable
        FID improvement; confirms acoustic conditioning is not redundant given OSM conditioning.
      - Comparison to Uni-ControlNet (Zhao et al., NeurIPS 2023): dual-path pattern confirmed;
        acoustic global path behaves analogously to global semantic embedding pathway.

  5.3 Spatial non-stationarity of generation fidelity: GWR/MGWR interpretation (~300 words)
      Key arguments:
      - MGWR adjusted R² vs. Fan et al. (2020) GWR R²=0.71: contextualise improvement;
        multi-scale bandwidth results confirm that generation fidelity is driven by covariates
        at different spatial scales simultaneously — road hierarchy at local scale (~1–2 km)
        and building density at regional scale (~3–5 km) — consistent with acoustic physics
        (road noise propagation range vs. morphological zone extent).
      - Residual Moran's I trajectory: I(OLS residuals) → I(GWR residuals) → I(MGWR residuals);
        reduction pattern consistent with Shen et al. (2022) OLS Moran's I ≈ 0.23 → GWR ≈ 0.06.
      - Geographic narrative: HH clusters (poor generation quality, high LPIPS) in commercial
        CBD zones (NYC Midtown, London City, Singapore CBD) — interpret as acoustic complexity
        exceeding CLAP embedding capacity in multi-source environments; LL clusters in residential
        areas (interpret as acoustic-visual coherence higher in acoustically simpler, morphologically
        homogeneous zones).
      - Practical significance: MGWR coefficient maps identify where soundscape conditioning
        works well and where it requires augmentation with additional covariates.

  5.4 Cross-city generalizability (~150 words)
      Key arguments:
      - Zero-shot transfer results: OSM spatial conditioning is the portability enabler
        (consistent with Mai et al. 2023); acoustic conditioning is city-specific (consistent
        with Liang et al. 2020 Singapore→Hong Kong R² drop from 0.67 to 0.54).
      - Fine-tuning cost (500 Singapore pairs sufficient): practical implication for deployment
        in data-scarce cities.
      - Singapore as hardest transfer case: tropical compact morphology, distinct acoustic
        character; results generalise the claim only to cities with OSM coverage.

  5.5 Limitations (~250 words)
      Honest limitations (4):
      L1: Temporal mismatch: despite the 3-year exclusion criterion, residual temporal
          confound remains between acoustic and visual data. A fully temporally matched
          dataset would require co-located, simultaneous audio-image collection.
      L2: ARAUS geographic bias: the ISO 12913 prediction MLP is trained on ARAUS, which
          overrepresents Northern European and North American urban soundscapes; pleasantness
          estimates for Singapore may be systematically biased by cultural perception differences
          documented by Aletta et al. (2023).
      L3: MGWR scale boundary: the analysis uses 500 m cells; acoustic effects at finer
          scales (street-canyon level, <100 m) cannot be captured at this resolution.
          Sub-cell variation is assessed via the LPIPS IQR auxiliary variable but not modeled.
      L4: Generative model scope: the framework is evaluated on 512×512 Mapillary images;
          panoramic synthesis or video generation from soundscapes is outside the current scope.

---

## 6. Conclusion (~500 words)

Key takeaways (3 numbered contributions):
1. ISO 12913-conditioned latent diffusion: SoundScape-ControlNet is the first framework to use structured soundscape perceptual descriptors (pleasantness, eventfulness, LAeq) as conditioning signals for street-level image synthesis, achieving FID ≤ 30 across NYC, London, and Singapore and outperforming CLAP-only baselines by ≥ 10%.
2. Dual-path conditioning architecture: the dual-path design fusing local OSM spatial controls and global acoustic embeddings via learned gating consistently outperforms single-path configurations by ≥ 8% FID, with gains concentrated in morphologically mixed zones where neither modality alone constrains scene content.
3. Multi-scale spatial analysis of generation fidelity: MGWR analysis of per-cell median LPIPS — the first application of geographically weighted regression to generative model quality — reveals that acoustic-morphological drivers of street-level generation fidelity are spatially non-stationary and operate at different scales (road hierarchy local; building density regional), with residual Moran's I falling from ≥ 0.20 to ≤ 0.08 after MGWR adjustment.

Future work (3–5 actionable directions):
FW1: Temporal conditioning — extend SoundScape-ControlNet to condition on time-of-day and seasonal acoustic inputs, enabling dynamic visualization of how streetscapes change with acoustic environment through the day.
FW2: Global South generalization — evaluate the framework in cities with distinct acoustic characters (Mumbai, Lagos, São Paulo) where OSM and Mapillary coverage is sparser; assess whether OSM-based portability holds outside the Global North training distribution.
FW3: Sub-cell acoustic modeling — integrate street-canyon-scale acoustic simulation (BEM or FDTD) to provide higher-resolution (<100 m) acoustic conditioning beyond what kriged Noise-Planet measurements support.
FW4: Nonlinear GWR extensions — apply GWRBoost or GWNN to the spatial analysis component to test whether nonlinear spatially varying models further improve explanation of generation fidelity over MGWR.
FW5: Downstream application validation — test whether soundscape-conditioned generated imagery is accepted as a valid input to urban perception models (e.g., Place Pulse-style preference prediction) and acoustic-visual design evaluation tools used in planning practice.

---

## References
Target: ≥ 25 citations (majority ≥ 2020; geo venues represented)

Priority papers (must-cite):
1. Zhang, L. & Agrawala, M. (2023). Adding Conditional Control to Text-to-Image Diffusion Models. ICCV 2023.
2. Rombach, R. et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR 2022.
3. Zhao, S. et al. (2023). Uni-ControlNet: All-in-One Control to Text-to-Image Diffusion Models. NeurIPS 2023.
4. Girdhar, R. et al. (2023). ImageBind: One Embedding Space To Bind Them All. CVPR 2023.
5. Wu, Y. et al. (2023). Large-Scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation. ICASSP 2023. [CLAP]
6. Sung-Bin, K. et al. (2023). Sound to Visual Scene Generation by Audio-to-Visual Latent Alignment. CVPR 2023. [Sound2Scene, FID 28.3]
7. Li, H. et al. (2024). Sound2Vision. [FID ~24]
8. Biner, O. et al. (2024). SonicDiffusion: Audio-Driven Image Generation and Editing with Pretrained Diffusion Models. arXiv 2024.
9. Mai, G. et al. (2023). Towards a Foundation Model for Geospatial Artificial Intelligence. ISPRS Journal of Photogrammetry and Remote Sensing, 2023.
10. Kang, J. et al. (2018). Ten questions on the soundscapes of the built environment. Building and Environment. [ISO 12913 cross-modal coupling]
11. Ooi, K. et al. (2022). ARAUS: A Large-Scale Dataset and Baseline Models of Affective Responses to Augmented Urban Soundscapes. IEEE TASLP 2022.
12. Watcharasupat, K. N. et al. (2022). Towards Perceptually Inspired Soundscape Enhancement. DCASE 2022.
13. Aletta, F. et al. (2023). Soundscape Attribute Translation Project. Applied Acoustics 2023. [SATP, ISO 12913 multilingual]
14. Qin, Y. et al. (2019). Investigating the link between perceived acoustic and visual characteristics of urban spaces. Computers, Environment and Urban Systems, 2019.
15. Fan, Y. et al. (2020). Examining the Relationship between Neighborhood Soundscapes and Urban Land Use. International Journal of Geographical Information Science, 2020.
16. Fotheringham, A. S., Yang, W. & Kang, W. (2017). Multiscale Geographically Weighted Regression (MGWR). Annals of the American Association of Geographers, 2017.
17. Fotheringham, A. S. et al. (2020). The Scalescape: Multiscale GWR and Unravelling Complexity in a Spatial GWR Route Map. Geographical Analysis, 2020.
18. Oshan, T. M. et al. (2019). mgwr: A Python Implementation of Multiscale Geographically Weighted Regression for Investigating Process Spatial Heterogeneity and Scale. ISPRS International Journal of Geo-Information, 2019.
19. Shen, X. et al. (2022). Spatially Varying Relationships between Urban Morphology and Noise. IEEE Transactions on Geoscience and Remote Sensing, 2022.
20. Wei, Y. et al. (2025). Diffusion-Based Satellite Image Synthesis with GWR Fidelity Evaluation. arXiv 2025.
21. Biljecki, F. & Ito, K. (2021). Street view imagery in urban analytics and GIS: A review. Landscape and Urban Planning, 2021.
22. Biljecki, F. et al. (2024). Urban Visual Intelligence. Annals of the American Association of Geographers, 2024.
23. Heidler, K. et al. (2022). Self-supervised audiovisual representation learning for remote sensing data. ISPRS Journal of Photogrammetry and Remote Sensing, 2022. [SoundingEarth]
24. Chen, A. et al. (2025). Cross-Modal Sound-Vision Alignment in Urban Street Scenes. arXiv 2025.
25. Liang, J. et al. (2020). Urban Acoustic-Visual Quality Prediction via Multi-Modal CNN Fusion. Computers, Environment and Urban Systems, 2020.
26. Liang, J. et al. (2020). Urban Acoustic-Visual Quality Prediction via Multi-Modal CNN Fusion. [Singapore/HK CNN R²=0.67]
27. Ho, J. et al. (2020). Denoising Diffusion Probabilistic Models. NeurIPS 2020.
28. Radford, A. et al. (2021). Learning Transferable Visual Models From Natural Language Supervision. ICML 2021. [CLIP]
29. Dubey, A. et al. (2016). StreetsScore — Predicting the Perceived Safety of One Million Streetscapes. CVPR Workshop 2016. [Place Pulse 2.0]
30. Boeing, G. (2017). OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks. Computers, Environment and Urban Systems, 2017.

---

## Figures Plan

| Fig # | Type | Content | Section |
|-------|------|---------|---------|
| Fig. 1 | Conceptual schematic | Dual-path conditioning pipeline: acoustic path (audio → CLAP → ISO 12913 head → cross-attention) + OSM spatial path (land use / building density / road hierarchy rasters → ControlNet zero-conv) → fused generation → generated street-level image; plus arrow indicating downstream GWR/MGWR spatial analysis loop | 1 (Introduction) |
| Fig. 2 | Three-panel map | Study area maps: NYC (EPSG:32618), London (EPSG:32630), Singapore (EPSG:32648); 500 m cell grid, OSM land use colour, Mapillary image density per cell, SoundingEarth audio clip density; scale bar, north arrow, legend, global inset locator | 3.1 (Study Area) |
| Fig. 3 | Architecture diagram | SoundScape-ControlNet UNet diagram: frozen SD backbone (grey), ControlNet zero-conv local path (blue), CLAP + ISO 12913 cross-attention global path (orange), learned gating at 4 resolution levels; annotated with conditioning vector dimensions | 3.3 (Architecture) |
| Fig. 4 | Image grid | Qualitative generation comparison: 4 rows (Arms A/B/C/D) × 3 columns (NYC/London/Singapore); each cell shows generated image + ground-truth reference; soundscape descriptor annotations (pleasantness score, LAeq) and OSM land use label per row | 4.1 (Ablation results) |
| Fig. 5 | Bar chart | FID, median LPIPS, SSIM per arm per city: 3 subplots, 5 groups per subplot (one per arm), 3 bars per group (one per city); error bars = bootstrap 95% CI; colour-coded by city | 4.1 (Ablation results) |
| Fig. 6 | Three-panel choropleth map | LISA cluster maps of raw per-cell median LPIPS: NYC / London / Singapore; HH (red) / LL (blue) / HL / LH / non-significant; OSM land use background (low opacity); scale bar, north arrow, legend with Moran's I value annotated | 4.2 (Spatial autocorrelation) |
| Fig. 7 | Six-panel coefficient map | MGWR spatially varying coefficients: top row = building density β per city (NYC/London/Singapore); bottom row = road hierarchy β per city; colour scale diverging from zero; 1 km boundary buffer hatching; scale bar, north arrow per panel | 4.4 (Coefficient maps) |
| Fig. 8 | Three-panel choropleth map | GWR local R² maps per city; colour scale 0–1; OSM land use overlay at low opacity; scale bar, north arrow | 4.4 (Coefficient maps) |

---

## Tables Plan

| Table # | Type | Content | Section |
|---------|------|---------|---------|
| Table 1 | Arm definition table | 5 rows (Arms A–E) × columns: Arm ID, audio encoder, ISO 12913 path (Y/N), OSM local path (Y/N), dual-path gating (Y/N), description, training status | 3.4 (Ablation design) |
| Table 2 | Dataset inventory | Rows = 8 datasets; columns: name, source, city coverage, spatial resolution, CRS, record count / image count, license, role in framework | 3.2 (Data) |
| Table 3 | Generation fidelity results | Rows = 5 arms; columns: FID-NYC, FID-London, FID-Singapore, FID-pooled, median LPIPS-NYC, median LPIPS-London, median LPIPS-Singapore, SSIM-pooled, Wilcoxon p (Arm D vs. C, Bonferroni-corrected); best value per column in bold | 4.1 (Ablation) |
| Table 4 | Spatial regression model comparison | Rows = OLS/GWR/MGWR/SEM × 3 cities (9 rows); columns: model, city, n, AICc, adjusted R², spatial block CV RMSE, Moran's I on residuals; best value per column in bold | 4.3 (OLS/GWR/MGWR) |
| Table 5 | MGWR per-variable bandwidths | Rows = covariates (8: LAeq, CLAP-PC1, CLAP-PC2, CLAP-PC3, building density, building height, road hierarchy, pleasantness); columns: NYC bandwidth (k, km, classification), London bandwidth (k, km, classification), Singapore bandwidth (k, km, classification) | 4.3 (OLS/GWR/MGWR) |

---

## Word Budget Allocation Summary

| Section | Target words |
|---------|-------------|
| Abstract | 250 |
| 1. Introduction | 800 |
| 2. Literature Review | 1,500 |
| 3. Methodology | 2,500 |
| 4. Results | 2,000 |
| 5. Discussion | 1,200 |
| 6. Conclusion | 500 |
| References (text overhead) | ~250 |
| Figure/table captions | ~500 |
| **Total** | **~9,500** |

*500-word buffer for revision; aggregate stays within 10,000-word ISPRS limit.*
