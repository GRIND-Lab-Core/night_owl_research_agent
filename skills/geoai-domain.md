# GeoAI Domain Knowledge Base

**Last Updated:** 2026-03-13
**Maintainer:** Research Agent — GeoAI Lab

---

## 1. Definition and Scope of GeoAI

GeoAI is the convergence of artificial intelligence, machine learning, and geospatial science. It applies AI methods to geographic data while simultaneously incorporating geographic principles (spatial autocorrelation, scale, topology, place semantics) into AI model design.

**Janowicz et al. (2020)** in the *International Journal of Geographical Information Science* define GeoAI as "the integration of AI methods with geospatial big data to mine complex patterns and extract insights that cannot be obtained with traditional computational approaches." They emphasize that GeoAI is not simply applying AI to geographic data, but requires fundamentally geographic thinking embedded in model architectures.

**Mai et al. (2024)** extend this to argue that GeoAI must grapple with geographic representation: encoding places, regions, coordinates, and spatial relationships in ways that capture their semantic and geometric richness. They highlight the emerging subfield of spatial representation learning as foundational.

The scope of GeoAI spans:
- Remote sensing image analysis and interpretation
- Geospatial knowledge graphs and ontologies
- Place representation and geolocalization
- Spatial prediction and interpolation
- Volunteered geographic information (VGI) analysis
- Autonomous GIS agents and spatial reasoning
- Foundation models pretrained on geospatial data
- Multi-modal fusion of geographic data types

GeoAI is distinct from general AI/ML in that it must respect: (1) spatial autocorrelation (nearby things are more similar), (2) scale sensitivity (relationships change with spatial resolution), (3) the modifiable areal unit problem (MAUP), (4) geographic context and place semantics, and (5) the non-stationarity of spatial processes.

---

## 2. Core Subfields

### 2.1 Spatial Representation Learning

Spatial representation learning concerns how to encode geographic coordinates, regions, and spatial context into dense vector embeddings that capture semantic and geometric relationships.

Key tasks include:
- **Location encoding**: mapping raw (latitude, longitude) pairs into feature vectors for downstream prediction
- **Region embedding**: representing administrative units, neighborhoods, or grid cells by aggregating multi-source data
- **Place representation**: encoding named places with their semantic, functional, and spatial attributes
- **Spatial knowledge graph embedding**: learning representations of geographic entities and their topological/semantic relationships

Critical insight: naive encoding of coordinates (treating lat/lon as raw numerical features) fails to capture spatial structure. Advanced encoders use multi-scale periodic functions, hierarchical spatial grids, or contrastive learning from co-located data.

### 2.2 Geospatial Foundation Models

Foundation models pretrained on large-scale geospatial data and adapted (fine-tuned or prompted) for diverse downstream tasks. These models inherit the paradigm of large language models (pretraining + fine-tuning) applied to satellite imagery, remote sensing time series, and multi-modal geographic data.

Foundation models in geospatial differ from LLMs in their input modalities: multi-spectral imagery (beyond RGB), synthetic aperture radar (SAR), elevation models (DEMs), and temporal sequences of the same geographic area.

### 2.3 Geospatial Computer Vision

Computer vision methods applied to overhead (aerial, satellite) and street-level imagery for geographic tasks:
- Scene classification (land use/land cover mapping)
- Object detection (building footprints, vehicle detection, road network extraction)
- Semantic segmentation (per-pixel land cover labels)
- Change detection (identifying differences between temporal image pairs)
- 3D reconstruction from imagery (stereo matching, structure-from-motion)
- Super-resolution of low-resolution satellite imagery
- Domain adaptation between satellite sensors or geographic regions

Challenges specific to geospatial computer vision: extreme class imbalance (rare damage classes), high intra-class variability across geographies, variable illumination and atmospheric conditions, and the need to integrate spectral bands beyond RGB.

### 2.4 Geolocalization

Given an image (aerial, street-level, or indoor), determine the geographic location (latitude, longitude) where it was captured. Also called image geo-localization or place recognition.

Approaches range from retrieval-based (match query image to a geo-tagged reference database) to regression-based (directly regress coordinates) to classification-based (predict a geographic cell from a hierarchical grid like S2 cells or geohash).

### 2.5 Spatial Prediction and Interpolation

Predicting values at unobserved locations from known observations. Classical approaches: kriging (spatial statistics), IDW (inverse distance weighting). GeoAI approaches: Gaussian process regression with learned kernels, graph neural networks on spatial graphs, attention-based models that incorporate distance decay.

Applications: PM2.5 mapping from sparse monitors, temperature interpolation, soil property mapping, species distribution modeling.

---

## 3. Key Methodologies

### 3.1 Location Encoders

**Space2Vec (Mai et al., 2020, ICLR)**
- Encodes (lat, lon) as multi-scale sinusoidal position embeddings
- Captures spatial hierarchy via multiple frequency bands
- Outperforms naive coordinate encoding on species distribution modeling and POI classification
- Architecture: wrap position encoding into an MLP; learn frequency parameters from data

**SatCLIP (Klemmer et al., 2023)**
- Location encoder trained with contrastive learning on satellite imagery
- Positive pairs: different views of the same location; negative pairs: distant locations
- Encoder learns to predict where an image was taken from its visual content
- Produces transferable location embeddings for downstream tasks without retraining

**GeoCLIP (Vivanco Cepeda et al., 2023, NeurIPS)**
- Contrastive language-image pretraining for geolocalization
- Aligns image embeddings with GPS coordinate embeddings via CLIP-style training
- Achieves state-of-the-art worldwide image geolocalization
- Operates at multiple geographic granularities (country, region, city, exact)

**CSP (Contrastive Spatial Pretraining, Cole et al., 2023)**
- Self-supervised pretraining of location encoders using satellite imagery as supervision signal
- Does not require manual labels; leverages massive unlabeled geo-tagged image datasets

### 3.2 Geo-Foundation Models

**Prithvi (Jakubik et al., 2023, arXiv)**
- Developed by NASA and IBM
- Masked autoencoder (MAE) architecture pretrained on HLS (Harmonized Landsat and Sentinel-2) data
- 6-band multispectral input (RGB + NIR + SWIR1 + SWIR2)
- Temporal self-supervised pretraining: mask patches across space and time, reconstruct
- Fine-tuned for: flood mapping, wildfire scar detection, land cover classification
- Open weights; available on Hugging Face

**SpectralGPT (Hong et al., 2024)**
- Generative pretraining on multi-spectral satellite imagery
- Handles arbitrary spectral band configurations
- Generates band predictions autoregressively, enabling flexible sensor adaptation
- Strong performance on DOTA, BigEarthNet, and EuroSAT benchmarks

**SkySense (Guo et al., 2024)**
- Multi-modal remote sensing foundation model integrating optical, SAR, and temporal data
- Contrastive and generative pretraining objectives
- Multi-granularity spatial-temporal encoding
- Demonstrates strong generalization across diverse remote sensing tasks

**DOFA (Dynamic One-For-All, Xiong et al., 2024)**
- Handles arbitrary number of spectral bands via dynamic weight generation
- One model for multispectral, hyperspectral, SAR, and RGB imagery
- Pretrained on 14 diverse datasets spanning multiple sensor types

**GFM (Geospatial Foundation Model, Mendieta et al., 2023)**
- MAE-based pretraining on Sentinel-2 imagery at global scale
- Strong downstream performance with limited labeled data

### 3.3 Vision-Language Models for Remote Sensing

**RemoteCLIP (Liu et al., 2024)**
- CLIP model fine-tuned on remote sensing image-text pairs
- Enables zero-shot scene classification and cross-modal retrieval
- Outperforms zero-shot transfer from standard CLIP by large margin
- Training data: curated RS image-caption pairs from public datasets

**GeoChat (Kuckreja et al., 2023, arXiv)**
- Multi-modal instruction-following model for remote sensing
- Enables conversational image analysis: "What is the damage level of this building?"
- Architecture: vision encoder + LLM (Vicuna) + instruction tuning on RS-specific conversations
- Demonstrates grounded question answering and visual reasoning for aerial imagery

**RSGPT (Hu et al., 2023)**
- Remote sensing image captioning and visual question answering
- Fine-tuned on RS-specific instruction pairs

**SkyEyeGPT (Zhan et al., 2024)**
- Unified instruction tuning for remote sensing with multi-task conversational capability

### 3.4 Autonomous GIS Agents

Emerging paradigm: LLM-based agents that can autonomously perform GIS analyses, write Python/R/SQL code for spatial operations, retrieve and process geodata, and interpret results.

**LLM-Geo (Li et al., 2024, International Journal of Applied Earth Observation)**
- GPT-4-based agent for autonomous geospatial analysis
- Decomposes user queries into spatial reasoning tasks
- Generates and executes Python code with GDAL, rasterio, geopandas, ArcPy
- Produces maps and analysis reports with minimal human intervention

Key capabilities needed in GIS agents:
- Tool use (spatial databases, web APIs, geoprocessing libraries)
- Spatial reasoning (topology, proximity, overlay, routing)
- Map generation and cartographic communication
- Error recovery from failed spatial operations

---

## 4. Key Datasets

### 4.1 OpenStreetMap (OSM)
- Global crowdsourced map database; over 10 billion GPS points, 900M+ nodes
- Contains: roads, buildings, land use, POIs, natural features
- Access: Overpass API, Geofabrik extracts, OSMnx (Python library)
- GeoAI uses: training data for road/building detection, graph neural networks, urban analytics

### 4.2 Sentinel-2 (ESA Copernicus)
- 13 spectral bands (443-2190 nm), 10m/20m/60m resolution
- 5-day revisit time; global coverage since 2015 (Sentinel-2A) and 2017 (Sentinel-2B)
- Access: Copernicus Open Access Hub, Microsoft Planetary Computer, Google Earth Engine
- GeoAI uses: land cover mapping, vegetation monitoring, flood/fire detection, pretraining data

### 4.3 Landsat Collection 2 (USGS/NASA)
- 8-11 spectral bands; 30m resolution
- Continuous record from 1972 to present (Landsat 1-9)
- Access: USGS Earth Explorer, Google Earth Engine
- GeoAI uses: long-term change detection, deforestation monitoring, pretraining (HLS)

### 4.4 NAIP (National Agriculture Imagery Program)
- 0.6-1.0m resolution aerial imagery for continental US
- 4 bands: R, G, B, NIR
- Updated 3-year cycle, state by state
- GeoAI uses: building footprint extraction, urban morphology, tree canopy mapping

### 4.5 NLCD (National Land Cover Database)
- 30m resolution land cover for CONUS; classes: developed, forest, wetlands, agriculture, etc.
- Updated every 2-3 years; products from 2001-2023
- GeoAI uses: training labels for land cover models, baseline comparisons

### 4.6 Social Media Geotagged Data
- Twitter/X: geotagged tweets with coordinates or place polygons
- Flickr: geotagged photos with Creative Commons licenses
- Instagram: limited API access post-2020
- Uses: event detection, urban activity patterns, crisis mapping, POI semantics
- Caveats: strong demographic bias (urban, young, tech-literate), declining geotagging rates

### 4.7 Benchmark Datasets for GeoAI
- **BigEarthNet**: 590,326 Sentinel-2 patches with multi-label land cover annotations
- **DOTA (Detection in Optical Remote Sensing Images)**: 188,282 instances across 15 categories
- **DeepGlobe**: road extraction, building detection, land cover segmentation benchmarks
- **xBD (xView2)**: pre/post disaster image pairs with building damage labels (6 categories)
- **SpaceNet**: building footprints and road networks for 30+ cities worldwide
- **EuroSAT**: land use classification across 10 classes, Sentinel-2 based

---

## 5. Evaluation Metrics

### 5.1 Spatial Cross-Validation
Standard k-fold cross-validation ignores spatial autocorrelation, leading to optimistic performance estimates when training and test samples are spatially proximate.

**Spatial blocking**: divide study area into geographic blocks; hold out entire blocks as test sets.
**Buffered leave-one-out (BLOO)**: exclude observations within a buffer zone around each test point.
**Cluster-based CV**: use spatial clustering (k-means, DBSCAN) to create folds of spatially coherent groups.

Implementation: `blockCV` (R), `sklearn-spatial-cv` patterns, `skcv` library.

### 5.2 Geographic Generalization
Measures how well models trained in one region perform in new, unseen regions.
Evaluated by: train on Region A, test on Region B; report performance gap vs. same-region test.
Related concepts: domain adaptation gap, spatial transferability, geographic out-of-distribution generalization.

### 5.3 Localization Error
For geolocalization tasks: great-circle distance (km) between predicted and true coordinates.
Reported at multiple thresholds: error within 1km, 25km, 200km, 750km, 2500km.
Standard benchmark: Im2GPS, GWS (Google World Streets), YFCC26k dataset.

### 5.4 Task-Specific Metrics
- **Classification**: Accuracy, F1 (macro/weighted), Cohen's Kappa (important for imbalanced spatial classes)
- **Object Detection**: mAP@50, mAP@50:95, IoU threshold sensitivity
- **Semantic Segmentation**: mean IoU (mIoU), per-class IoU, boundary accuracy
- **Change Detection**: F1 for change class, OA, Kappa
- **Regression/Interpolation**: RMSE, MAE, R², RPIQ (for skewed distributions)

---

## 6. Major Research Groups and Venues

### 6.1 Journals
- **IJGIS (International Journal of Geographical Information Science)**: top GIScience theory and methods
- **Annals of the American Association of Geographers**: broad human/physical geography
- **ISPRS Journal of Photogrammetry and Remote Sensing**: remote sensing methods
- **Remote Sensing of Environment**: applications-focused RS
- **International Journal of Applied Earth Observation and Geoinformation (JAG)**: applied GeoAI
- **Cartography and Geographic Information Science**: cartography, visualization, GIScience
- **Transactions in GIS**: applied GIS methods
- **GeoHealth**: geographic approaches to health

### 6.2 Conferences
- **ACM SIGSPATIAL**: premier venue for spatial computing and GeoAI
- **ICCV, CVPR, NeurIPS, ICLR**: top ML/CV venues with significant GeoAI presence
- **ISPRS Congress / ISPRS Geospatial Week**: international remote sensing
- **AAG Annual Meeting**: geographic perspectives on GeoAI
- **AAAI, IJCAI**: AI venues with spatial reasoning tracks

### 6.3 Key Research Groups (as of 2026)
- **GeoDS Lab (Yingjie Hu, University at Buffalo)**: place representation, knowledge graphs, spatial reasoning
- **Spatial Computing Lab (Krzysztof Janowicz, UCSB)**: GeoAI theory, knowledge graphs, place semantics
- **Mai Lab (Gengchen Mai, UT Austin)**: location encoders, geospatial foundation models, spatial LLMs
- **CogGeoLab (Yao-Yi Chiang, Univ. of Minnesota)**: map understanding, historical maps, autonomous GIS
- **CESAR Lab (Dalton Lunga, ORNL)**: satellite imagery for humanitarian applications
- **Remote Sensing + AI groups at DLR, ESA, NUS**: geo-foundation model development

---

## 7. Open Challenges

### 7.1 Geographic Bias
Most GeoAI models are trained predominantly on data from North America, Europe, and East Asia. Performance degrades substantially in underrepresented regions (sub-Saharan Africa, Central Asia, rural Global South). This is both a technical problem (domain shift) and an equity problem (models are least useful where they are most needed).

### 7.2 Spatial Autocorrelation in Machine Learning
Spatial autocorrelation violates the i.i.d. assumption underlying most ML methods. This leads to:
- Overly optimistic cross-validation estimates
- Inflated feature importance when spatially correlated predictors are included
- Poorly calibrated uncertainty estimates in spatial prediction

### 7.3 Scale Sensitivity
Geographic phenomena exhibit different patterns at different spatial scales (Tobler's Second Law). A model trained at 30m resolution may not transfer to 1m resolution, and vice versa. Scale-invariant representation learning remains an active challenge.

### 7.4 Privacy in Geospatial AI
Fine-grained location data enables powerful inferences about individual behavior, home/work locations, health conditions, and social relationships. Differential privacy for location data, location obfuscation, and federated learning for distributed geospatial data are active research areas.

### 7.5 Interpretability and Spatial Reasoning
Neural GeoAI models produce accurate outputs but opaque reasoning. Spatial explainability: "why does the model predict high flood risk here?" requires spatial attribution methods adapted from SHAP/LIME to respect spatial structure.

---

## 8. Terminology Glossary

**First Law of Geography (Tobler, 1970):** "Everything is related to everything else, but near things are more related than distant things." Foundation of spatial autocorrelation theory.

**Spatial Autocorrelation:** The correlation of a variable with itself across geographic space. Positive: nearby values are similar (common). Negative: nearby values are dissimilar (checkerboard pattern, rare). Measured by Moran's I, Geary's C.

**Scale Invariance:** A model or pattern that behaves consistently across different spatial resolutions or extents.

**Multimodal Fusion:** Combining multiple data types (optical imagery, SAR, text, GPS traces) into a unified model. Late fusion: combine predictions; early fusion: combine inputs; cross-modal attention: learn interactions.

**MAUP (Modifiable Areal Unit Problem):** Statistical results change depending on how spatial units are defined (e.g., census tracts vs. counties vs. zip codes). A fundamental challenge in spatial statistics.

**Place:** A location imbued with human meaning, identity, and context—distinct from "space" (abstract coordinates). Place semantics is the study of what locations mean to people.

**Geohash / S2 Cells / H3:** Hierarchical spatial indexing systems that divide the Earth into nested cells at multiple resolutions. Used for spatial bucketing in GeoAI.

**Spatial Transfer Learning:** Adapting a model trained in one geographic region or at one spatial scale to new regions or scales with minimal retraining.

**VGI (Volunteered Geographic Information):** Geographic data contributed by non-expert citizens (OSM contributors, Flickr users, Twitter posters). Rich but biased.

**Remote Sensing:** Observation of Earth's surface from aircraft or satellites, producing imagery across spectral bands. Key data type for GeoAI.

---

## 9. Key Paper Milestones (2019–2026)

### 2019
- **Janowicz et al. (2019)** "GeoAI: Spatially Explicit Artificial Intelligence Techniques for Geographic Knowledge Discovery and Beyond" — foundational framing paper, IJGIS.

### 2020
- **Mai et al. (2020)** "Multi-Scale Representation Learning for Spatial Feature Distributions using Grid Cells" (Space2Vec) — ICLR, fundamental location encoding method.
- **Janowicz et al. (2020)** — expanded GeoAI definition and research agenda.

### 2021
- **Ayush et al. (2021)** "Geography-Aware Self-Supervised Learning" — ICCV, contrastive pretraining using geographic proximity as supervision signal.
- **Jean et al. (2019/expanded 2021)** — combining satellite imagery with survey data for poverty mapping.

### 2022
- **Wang et al. (2022)** SatMAE — masked autoencoder pretraining for multi-temporal satellite imagery, NeurIPS.
- **Li et al. (2022)** — large-scale remote sensing pretraining surveys.

### 2023
- **Jakubik et al. (2023)** — Prithvi, NASA-IBM geospatial foundation model (arXiv).
- **Cole et al. (2023)** — CSP location encoder for species distribution modeling.
- **Klemmer et al. (2023)** — SatCLIP, satellite-based contrastive location encoders.
- **Vivanco Cepeda et al. (2023)** — GeoCLIP, NeurIPS.
- **Kuckreja et al. (2023)** — GeoChat, multi-modal RS conversational model.

### 2024
- **Mai et al. (2024)** — comprehensive survey on spatial representation learning and GeoAI progress.
- **Hong et al. (2024)** — SpectralGPT, generative model for multi-spectral RS.
- **Xiong et al. (2024)** — DOFA, dynamic one-for-all remote sensing foundation model.
- **Li et al. (2024)** — LLM-Geo, autonomous GIS agent with GPT-4.
- **Guo et al. (2024)** — SkySense multi-modal RS foundation model.

### 2025–2026
- Rapid proliferation of GeoAI agents capable of autonomous spatial analysis pipelines.
- Integration of geographic context into general-purpose LLMs (geographic grounding).
- Multi-modal geo-foundation models capable of joint reasoning over imagery, text, and coordinates.
- Equity-aware GeoAI: methods explicitly accounting for geographic bias and underrepresentation.
