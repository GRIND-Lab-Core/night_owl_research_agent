# Disaster Resilience Knowledge Base — GeoAI Applications

**Last Updated:** 2026-03-13
**Maintainer:** Research Agent — GeoAI Lab

---

## 1. Foundational Frameworks

### 1.1 Sendai Framework for Disaster Risk Reduction (2015–2030)
Adopted at the UN World Conference in Sendai, Japan (March 2015), the Sendai Framework is the successor to the Hyogo Framework for Action (2005–2015). It provides the global blueprint for disaster risk reduction (DRR).

**Four Priorities for Action:**
1. Understanding disaster risk
2. Strengthening disaster risk governance to manage disaster risk
3. Investing in DRR for resilience
4. Enhancing disaster preparedness for effective response, and to "Build Back Better"

**Seven Global Targets:**
- Substantially reduce global disaster mortality by 2030
- Reduce the number of directly affected people
- Reduce direct economic loss relative to GDP
- Reduce damage to critical infrastructure and disruption of basic services
- Increase the number of countries with national and local DRR strategies
- Enhance international cooperation to developing countries
- Increase the availability of and access to multi-hazard early warning systems

GeoAI relevance: targets require spatial monitoring, damage assessment, exposure modeling, and real-time early warning—all domains where GeoAI has direct application.

### 1.2 UNDRR (UN Office for Disaster Risk Reduction)
Implements the Sendai Framework; produces the Global Assessment Report (GAR) on Disaster Risk Reduction. Maintains the DesInventar disaster loss database (open access).

Key UNDRR initiatives with GeoAI components:
- Global Risk Index incorporating exposure, vulnerability, and coping capacity
- INFORM Risk Index: multi-hazard risk score for 191 countries
- Risk Data Hub: open platform aggregating disaster risk datasets

### 1.3 Hyogo Framework for Action (2005–2015)
Predecessor to Sendai; five priorities focused on risk knowledge, governance, investment in risk reduction, managing underlying risk factors, and preparedness. Established baseline expectations for national DRR programs.

### 1.4 Community Resilience Models

**Bruneau et al. (2003) Resilience Framework:** Defines resilience along four dimensions (the 4Rs):
- **Robustness**: ability of systems to withstand hazard forces without degradation
- **Redundancy**: extent to which systems have substitutable elements satisfying functional requirements when disruption occurs
- **Resourcefulness**: capacity to identify problems, establish priorities, and mobilize resources
- **Rapidity**: speed to achieve goals in a timely manner to contain losses and avoid disruption

This framework applies to physical infrastructure, social systems, and economic systems.

**BRIC (Baseline Resilience Indicators for Communities):** County-level composite index developed by Cutter et al. measuring: housing and infrastructure, institutional capacity, economic capacity, social capacity, community capital, environmental capacity.

**DROP Model (Disaster Resilience of Place):** Cutter et al. (2008) — integrates inherent vulnerability and adaptive capacity to explain differential outcomes.

---

## 2. Disaster Cycle Phases

### 2.1 Mitigation (Pre-event, long-term)
Risk reduction activities that prevent disasters or reduce their impact:
- Zoning and land use planning to avoid high-risk areas
- Building code enforcement and retrofit programs
- Ecosystem-based approaches (mangroves for storm surge, wetlands for flood buffering)
- Infrastructure hardening (flood levees, earthquake-resistant construction)

GeoAI role: spatial risk modeling, vulnerability mapping, optimal placement of protective infrastructure, change detection to monitor compliance.

### 2.2 Preparedness (Pre-event, short-term)
Actions taken in anticipation of an event:
- Early warning system development and maintenance
- Evacuation planning and route optimization
- Stockpiling resources (location optimization via GIS)
- Training exercises and community preparedness programs
- Continuity of operations planning

GeoAI role: population exposure modeling, evacuation demand forecasting, optimal shelter location, scenario-based risk simulation, real-time weather/hazard model integration.

### 2.3 Response (During and immediately after event)
Actions during and immediately following a disaster:
- Search and rescue coordination
- Damage assessment and situational awareness
- Resource allocation and logistics
- Shelter-in-place vs. evacuation decision-making
- Communications and public information

GeoAI role: rapid damage mapping from satellite/aerial imagery, social media monitoring for distress signals and resource needs, optimizing rescue routing, automated situation reports.

### 2.4 Recovery (Post-event)
Short and long-term restoration of affected communities:
- Infrastructure repair and reconstruction
- Housing recovery and displacement tracking
- Economic recovery assessment
- Psychosocial support services
- Rebuilding toward greater resilience ("Build Back Better")

GeoAI role: longitudinal monitoring of reconstruction progress, displacement tracking via mobile data/remote sensing, equity analysis of recovery trajectories, monitoring return migration patterns.

---

## 3. GeoAI Applications in Disaster Management

### 3.1 Satellite-Based Damage Assessment

**SAR-Based Damage Detection:**
SAR (Synthetic Aperture Radar) penetrates cloud cover and operates day/night, making it ideal for post-disaster imagery acquisition.

Coherence-based change detection: compare interferometric coherence between pre/post-event SAR image pairs. Damaged areas show coherence loss due to structural changes. Used extensively for earthquake damage mapping (e.g., 2023 Turkey-Syria earthquake, Copernicus EMS activation).

Intensity-based change detection: compare backscatter intensity between pre/post-event images. Collapsed buildings show decreased backscatter from C-band SAR (Sentinel-1). Methods: log-ratio, mean-ratio, neighborhood correlation.

Deep learning for SAR damage: CNNs trained on labeled SAR change pairs (e.g., from xBD dataset adapted to SAR). U-Net variants dominate; transformer-based architectures (ChangeFormer) show competitive performance.

**Optical Damage Assessment:**
High-resolution optical imagery (0.3–0.5m from commercial satellites: Maxar WorldView, Planet Labs) enables building-level damage classification.

Damage grades (consistent with Copernicus EMS):
- Grade 1: Negligible to slight damage
- Grade 2: Moderate damage
- Grade 3: Substantial to heavy damage
- Grade 4: Very heavy damage
- Grade 5: Destruction

Object detection approach: detect and classify individual building footprints with damage grades. YOLO variants (YOLOv8, YOLOv9) and instance segmentation (Mask R-CNN) commonly used.

Semantic segmentation approach: pixel-level classification trained on large annotated datasets (xBD: 850,736 building annotations across 19 disaster events).

### 3.2 Social Media Crisis Mapping

Real-time geospatial intelligence from Twitter/X, Facebook, Instagram, and crisis-specific platforms (Ushahidi, Zello):

**Information extraction pipeline:**
1. Data collection: streaming API with disaster-related keywords
2. Geolocation: extract explicit GPS coordinates, place names from text (NER), profile location
3. Event detection: identify crisis-relevant posts (calls for help, reports of damage, resource offers)
4. Classification: prioritize posts by urgency, information type, actionability
5. Mapping: aggregate and visualize on real-time dashboards

**Key tasks and methods:**
- Named entity recognition for locations (transformer-based NER: BERT-GeoNER, GLiNER)
- Crisis event detection: multi-label classification (affected individuals, infrastructure damage, displaced persons, donation offers)
- Rumor detection: fact-checking credibility-based models to suppress misinformation
- Multi-lingual NLP: disaster tweets are international; multilingual BERT, XLM-R
- Image-text fusion: classify multimedia crisis posts

**Key datasets:** TREC-IS (Incident Streams), CrisisMMD (multi-modal), CrisisNLP.

### 3.3 Flood Inundation Modeling

**Hydrological modeling approaches:**
- Physics-based: HEC-RAS 2D, LISFLOOD-FP, MIKE FLOOD — computationally intensive but mechanistically sound
- Data-driven: ML surrogates for rapid inundation prediction (neural network emulators of hydraulic models)
- Hybrid: physics-informed neural networks (PINNs) for flood routing

**GeoAI enhancements:**
- Flood extent mapping from Sentinel-1 SAR: threshold-based or CNN-based water body extraction
- Flood depth estimation from post-event imagery and LiDAR
- Real-time flood forecasting integrating NWP rainfall forecasts + hydrological models + GNN routing
- Historical inundation learning: training data from MODIS/Landsat flood frequency maps

**Key datasets:**
- Global Flood Database (Tellman et al., 2021, Nature): 30m resolution global flood maps from Landsat/MODIS (2000-2018)
- Copernicus Emergency Management Service flood activations
- FEMA FIRM (Flood Insurance Rate Maps) for US regulatory floodplains

### 3.4 Wildfire Spread Prediction

**Fire behavior modeling:**
- Physical models: FARSITE, FlamMap, Phoenix — require fuel maps, topography, weather
- Statistical: logistic regression, MaxEnt for fire occurrence probability
- Deep learning: ConvLSTM, graph neural networks for spatiotemporal fire spread

**Satellite monitoring:**
- FIRMS (Fire Information for Resource Management System): near real-time active fire detections from MODIS and VIIRS
- Sentinel-2 and Landsat: post-fire burn severity mapping (NBR — Normalized Burn Ratio)
- GOES-16/17/18: 10-minute scan rate for rapid fire progression monitoring

**GeoAI approaches:**
- U-Net for burn area delineation from multi-spectral imagery
- ResNet/ViT for fire risk classification (fuel type, slope, wind exposure)
- LSTM/Transformer for fire progression prediction integrating weather forecast data
- Ensemble methods combining physics-based spread models with ML correction

### 3.5 Earthquake Damage Mapping

**Rapid damage assessment pipeline:**
1. Trigger: earthquake detected by seismic networks (USGS ShakeMap, EMSC)
2. Automated ShakeMap analysis: predict ground motion intensity (PGA, PGV, MMI)
3. Exposure calculation: overlay ShakeMap with population and building inventory
4. Satellite tasking: request high-resolution optical and SAR imagery of affected area
5. Change detection: compare pre/post-event imagery
6. Damage classification: assign grade to affected structures
7. Casualty estimation: combine damage grades with population exposure

Key datasets: USGS ShakeMap, Global Earthquake Model (GEM) building exposure, Copernicus EMS rapid mapping activations.

Benchmark: DEBrisMap 2023 (Turkey-Syria earthquake damage dataset).

### 3.6 Hurricane Track and Intensity Forecasting

**Operational forecast systems:** NHC (National Hurricane Center) uses ensemble NWP models (GFS, ECMWF, HWRF, HAFS) and track consensus methods.

**GeoAI approaches:**
- Deep learning track prediction: PanguWeather, GraphCast, FourCastNet provide skillful medium-range track forecasts
- Intensity forecasting: CNN analysis of microwave and infrared satellite eye structure
- Rapid intensification detection: critical life-safety issue; ML classification of 24-hour wind speed changes ≥35 kt
- Storm surge modeling: SLOSH model + ML surrogates for rapid scenario generation

**Key datasets:** HURDAT2 (1851-present Atlantic hurricane database), IBTrACS (global best-track data), SHIPS (Statistical Hurricane Intensity Prediction Scheme) predictors.

---

## 4. Vulnerability Dimensions

### 4.1 Social Vulnerability Index (SoVI)
Developed by Cutter et al. (2003); measures socioeconomic and demographic factors that enhance or reduce a community's capacity to prepare, respond to, and recover from disasters.

**SoVI components (US Census based):**
- Socioeconomic status (poverty, income, employment)
- Household composition and disability
- Minority status and language
- Housing type and transportation
- Race/ethnicity (Black, Hispanic, Native American)
- Gender (female-headed households)
- Special needs (elderly, children)

SoVI score: composite index from principal components analysis; higher scores = more socially vulnerable. Available at county and census tract level.

**Limitations:** static (census-based, 5-10 year lag), does not capture dynamic vulnerability, sensitivity to component selection and weighting.

### 4.2 Exposure
The degree to which people, infrastructure, and assets are located in hazard-prone areas. Purely geographic: proximity to flood zone, seismic zone, wildfire urban-wildland interface.

GeoAI measures: satellite-derived building inventory, LiDAR-based infrastructure mapping, population density grids (WorldPop, GPW, LandScan).

### 4.3 Sensitivity
The degree to which a system is affected by hazard exposure, given equal exposure. Determined by structural vulnerability (building material, age, construction type), physiological vulnerability (elderly, young children, health status), and economic fragility.

### 4.4 Adaptive Capacity
The ability to adjust to hazard conditions, take advantage of opportunities, or cope with consequences. Determined by resources, institutions, governance, knowledge, technology, and social capital.

---

## 5. Key Datasets

- **FEMA Disaster Declarations:** 1953-present; county-level major disaster, emergency, and fire management declarations. Open API. Used for longitudinal disaster trend analysis.
- **NOAA Storm Events Database:** 1950-present; 48 event types; damage estimates, injuries, fatalities, geographic coordinates. Includes Hurricane, Tornado, Flood, Wildfire, Winter Storm, and 44 other types.
- **Global Earthquake Model (GEM):** Open exposure database; building inventory, fragility functions, hazard maps for global earthquake risk.
- **Copernicus Emergency Management Service (EMS):** Rapid mapping activations with damage grading products; available for academic download. Activation IDs trace to specific events.
- **xBD (xView2 Building Damage):** 850,000+ annotated buildings across 19 disasters in 15 countries; pre/post optical imagery pairs; 4 damage classes. The primary benchmark for building damage assessment.
- **FIRMS (NASA):** Near real-time fire detections; accessible via API and bulk download.
- **Global Flood Database:** Landsat/MODIS-derived flood extents 2000-2018; 913 events; Tellman et al. (2021), Nature.
- **OpenStreetMap:** Building footprints for urban areas globally; critical for exposure modeling.
- **WorldPop / GPW / LandScan:** High-resolution population grids at 100m, 1km, 1km resolution respectively.
- **Twitter/X Disaster Archives:** CrisisNLP, TREC-IS; labeled crisis tweets across multiple event types.

---

## 6. Methodologies for Crisis GeoAI

### 6.1 Change Detection
Binary or multi-class comparison between pre/post-event imagery to identify areas of change.
- Pixel-based: difference images, log-ratio, Otsu thresholding
- Object-based: segment, then compare object attributes
- Deep learning: Siamese networks, transformer-based change detection (BIT, ChangeFormer, SNUNet)
- Evaluation: F1 for change class, precision/recall tradeoff critical for damage mapping

### 6.2 Multi-Temporal Analysis
Analyzing time series of satellite imagery to track processes:
- NDVI time series for vegetation recovery after wildfire
- SAR coherence stack for earthquake-triggered landslide monitoring
- Nighttime light time series (VIIRS DNB) for power outage mapping and recovery tracking

### 6.3 Object Detection in Post-Disaster Imagery
Detecting and classifying specific features in aerial/satellite imagery:
- Collapsed buildings (debris fields)
- Flooded roads and infrastructure
- Displaced populations / refugee settlements
- Rescue vessels and emergency vehicles
- Methods: YOLO, RetinaNet, Faster R-CNN; architectures adapted for overhead perspective (rotation-invariant features)

### 6.4 NLP for Social Media Triage
Priority-ranking of social media posts in crisis context:
- BERT-based multi-label classifiers for crisis information type
- Urgency scoring for search-and-rescue request prioritization
- Named entity extraction for location disambiguation and routing
- Misinformation flagging to prevent resource misallocation

---

## 7. Equity Considerations

### 7.1 Differential Impacts on Marginalized Communities
Disasters do not affect all communities equally. Low-income communities, racial minorities, elderly, disabled, and linguistically isolated populations face higher exposure, greater sensitivity, and lower adaptive capacity.

Evidence: Hurricane Katrina (2005) deaths disproportionately concentrated in predominantly Black neighborhoods (Lower 9th Ward); Hurricane Maria (2022) fatalities undercounted in Puerto Rico (official 64 vs. estimated 2,975+); wildfire evacuation compliance lower in mobile home communities and low-income areas.

### 7.2 Environmental Justice in Disaster Policy
FEMA assistance distribution has been documented to favor wealthier, whiter communities (Flores et al., 2020). Recovery grant allocation algorithms may embed historical inequities.

GeoAI equity research:
- Audit whether damage assessment models perform equally across neighborhood types
- Identify geographic gaps in VGI (OSM building coverage skews urban and wealthy areas)
- Ensure early warning systems are accessible in multiple languages and to populations without smartphones

### 7.3 Researcher Obligations
GeoAI researchers should: report disaggregated performance metrics by vulnerability class, test for differential error rates, engage affected communities in validation, and avoid using disaster data for surveillance.

---

## 8. Key Metrics for Disaster GeoAI

- **Overall Accuracy (OA)**: proportion of correctly classified pixels/objects — misleading for imbalanced damage classes
- **F1 Score for Damage Class**: harmonic mean of precision and recall for positive (damaged) class; preferred metric for rare events
- **mAP (mean Average Precision)**: for object detection tasks; sensitive to IoU threshold
- **False Alarm Rate / FAR**: critical for early warning — high FAR erodes public trust
- **Detection Probability / Pd**: probability of detecting a true event; tradeoff with FAR via ROC curve
- **Lead Time**: hours/days of warning before impact; the primary operational value metric for early warning systems
- **Damage Grade Accuracy**: match between assessed and true damage grade (1-5 scale); weighted kappa appropriate
- **Localization Error**: distance between predicted and actual event/damage location

---

## 9. Research Gaps (2025–2026)

1. **Real-time fusion of heterogeneous data streams**: integrating satellite imagery, SAR, NWP forecasts, sensor IoT, and social media in a unified near-real-time pipeline. Current systems are siloed.

2. **Equity-aware damage assessment models**: models explicitly calibrated to perform equitably across communities of different socioeconomic status, building quality, and geography. Standard benchmarks (xBD) skew toward urban areas.

3. **Longitudinal recovery tracking**: most GeoAI work focuses on immediate post-disaster period. Recovery can last 10+ years; long-term satellite monitoring of reconstruction and displacement remains underdeveloped.

4. **Few-shot / zero-shot disaster response**: rapid model adaptation for new disaster types and new geographies without labeled training data. Foundation models offer promise.

5. **Compound and cascading events**: single-hazard models poorly handle compounding (fire after drought, flood after earthquake). Models integrating multi-hazard dependencies are rare.

6. **Human-AI teaming in crisis response**: how human experts and AI damage assessment tools interact, disagree, and reach consensus decisions. Critical for operational deployment.

7. **Counterfactual impact estimation**: quantifying "how much worse would outcomes have been without intervention X?" requires causal inference methods in spatial context, rarely applied in disaster research.

---

## 10. Major Research Groups and Organizations

- **UNOSAT (UN Satellite Centre)**: operational rapid mapping using satellite imagery; publishes activation products. Active in every major disaster since 2000.
- **World Bank Disaster Risk Management (DRM)**: global risk modeling, financial protection instruments, data collection in LMICs.
- **USGS NHSS (Natural Hazards Science Center)**: earthquake, volcano, landslide, coastal hazard research and real-time monitoring.
- **FEMA (Federal Emergency Management Agency)**: US operational disaster response, FIRM flood maps, hazard mitigation grants.
- **NASA SERVIR**: satellite data and tools for development applications including disaster management in developing countries (Africa, Asia, Latin America).
- **Copernicus EMS**: European rapid mapping service, EFAS (flood forecasting), EFFIS (fire monitoring).
- **Pacific Disaster Center (PDC)**: data integration, risk analysis, early warning for Pacific Rim nations.
- **Humanitarian OpenStreetMap Team (HOT)**: crisis mapping activation coordinators, OSM data for disaster response.
