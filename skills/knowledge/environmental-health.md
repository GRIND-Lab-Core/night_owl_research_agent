# Environmental Health and GeoAI Knowledge Base

**Last Updated:** 2026-03-13
**Maintainer:** Research Agent — GeoAI Lab

---

## 1. Core Environmental Exposures

### 1.1 Air Quality

**PM2.5 (Fine Particulate Matter, <2.5 μm diameter)**
The most extensively studied air pollutant in environmental health GeoAI. Fine particles penetrate deep into lung tissue and the bloodstream.

Health effects: cardiopulmonary disease, stroke, lung cancer, preterm birth, cognitive decline, premature mortality. No safe threshold has been established (WHO 2021 guidelines: 5 μg/m³ annual mean, reduced from 10 μg/m³).

Sources: combustion (vehicles, industry, biomass burning), secondary formation from SO2/NOx/VOC, dust. Strong seasonal and spatial variation.

GeoAI relevance: monitor network density is too sparse for fine-scale exposure estimation. Satellite-derived AOD (aerosol optical depth) provides global coverage but requires calibration to surface PM2.5. Gap: bridging the link between column-integrated AOD and surface PM2.5 is a major active research area.

**Ozone (O3)**
Ground-level ozone (not stratospheric). Secondary pollutant formed via photochemical reactions of NOx and VOCs in sunlight. Strong summer peaks, afternoon maxima.

Health effects: respiratory inflammation, asthma exacerbation, reduced lung function, mortality. EPA NAAQS: 70 ppb 8-hour average.

**NO2 (Nitrogen Dioxide)**
Primary traffic-related pollutant; strong spatial gradient near highways. Indicator for traffic-related air pollution (TRAP) more broadly.

Health effects: respiratory disease, asthma, adverse birth outcomes, cardiovascular disease. High-resolution NO2 mapping enabled by Sentinel-5P TROPOMI (3.5 × 5.5 km resolution at nadir, upgraded to 3.5 × 3.5 km post-2023).

**SO2 (Sulfur Dioxide)**
Industrial/power plant emission. Major contributor to acid rain and secondary sulfate PM2.5 formation. Sentinel-5P also provides SO2 columns.

**CO (Carbon Monoxide)**
Combustion tracer. Less health-relevant at typical ambient concentrations but useful as transport model tracer.

**Volatile Organic Compounds (VOCs)**
Hundreds of compounds; key ozone and secondary organic aerosol (SOA) precursors. Difficult to monitor; growing GeoAI interest in VOC source attribution from satellite data.

### 1.2 Extreme Heat

The deadliest weather-related hazard in the US by average annual mortality. Climate change is increasing the frequency, intensity, and duration of heat waves globally.

**Urban Heat Island (UHI) Effect:** Urban surfaces (asphalt, concrete, buildings) absorb and re-emit more heat than vegetated surfaces. Core urban areas can be 3-10°C warmer than surrounding rural areas.

**Heat-related health metrics:**
- Heat index (apparent temperature combining air temperature + humidity)
- Wet Bulb Globe Temperature (WBGT) for outdoor worker exposure
- Excess mortality during heat waves relative to expected baseline
- Emergency department visits for heat exhaustion/stroke

**GeoAI for heat:** Land Surface Temperature (LST) from MODIS/Landsat as proxy for heat exposure; machine learning models predicting neighborhood-level extreme heat risk; green space and cool surface intervention effectiveness modeling.

**Equity dimension:** Heat vulnerability is strongly spatially patterned: low-income neighborhoods with less tree canopy, older housing without air conditioning, and outdoor labor force face greatest risk. The "urban heat island + poverty" overlap is a core environmental justice issue.

### 1.3 Noise Pollution

Often overlooked environmental health hazard. Sources: road traffic, rail, aviation, industrial operations, construction.

Health effects: sleep disruption, cardiovascular disease (hypertension, heart attack), cognitive impairment in children, mental health impacts.

GeoAI approaches: noise propagation models using road network data and traffic volumes; deep learning classification of urban soundscapes from audio recordings; street-level imagery analysis for noise source proxies (road width, building canyon geometry, green barriers).

Key data: HERE Technologies noise maps, OSM road network + traffic data, US DOT Noise Exposure Maps.

### 1.4 Flood Risk

Discussed in detail in disaster-resilience.md. From an environmental health lens:
- Contaminated floodwater exposure (enteric pathogens, chemical contaminants, heavy metals from flooded brownfields)
- Mold and indoor air quality post-flood (respiratory effects)
- Mental health impacts of flood displacement
- Disproportionate flood exposure in low-income, minority communities (siting of floodplain development)

### 1.5 Green Space and Blue Space Access

**Physical access to parks, forests, water bodies:** measured by Euclidean or network distance, park acreage per capita.

**Functional green space quality:** tree canopy coverage (measured via remote sensing); NDVI as surrogate for greenness exposure.

Health benefits of green/blue space exposure: reduced stress, mental health benefits, physical activity facilitation, air cooling, heat mitigation, attention restoration (Attention Restoration Theory).

GeoAI approaches:
- NDVI from Landsat/Sentinel-2 at neighborhood level
- Tree canopy mapping from LiDAR or high-resolution imagery
- Google Street View green view index (deep learning to estimate visible greenery from eye level)
- Park accessibility via OSM + routing networks
- Equity analysis: who has equitable green space access?

### 1.6 Food Environment

Access to healthy food as environmental determinant of diet and metabolic health. "Food desert" (lack of supermarket access) and "food swamp" (oversupply of unhealthy food outlets) concepts.

GeoAI approaches: POI (Points of Interest) data for food outlet mapping (OSM, Google Places API, SafeGraph); spatial access modeling (gravity-based, 2-step floating catchment area); machine learning classification of food outlet type from street-level imagery.

Limitations: POI databases have systematic errors; defining food desert boundaries is contested.

### 1.7 Chemical Contamination

Superfund sites, industrial facilities (TRI — Toxic Release Inventory), legacy contamination (brownfields), agricultural pesticide drift.

EJ relevance: chemical contamination sites are disproportionately sited near communities of color and low-income communities (historical environmental racism in siting decisions).

GeoAI: proximity-based exposure, buffer analysis, dispersion modeling from facilities using wind data, satellite-based detection of some chemical plumes (SO2 from stacks via Sentinel-5P).

---

## 2. GeoAI Methods for Exposure Assessment

### 2.1 Land Use Regression (LUR)

Statistical regression of monitored pollutant concentrations on land use variables (road length buffers, population density, industrial land, traffic counts). Produces high-resolution (25-100m) NO2, PM2.5, and BC maps.

Methodology:
1. Gather monitor measurements (EPA AQS, LTER, research campaign monitors)
2. Extract land use predictors at multiple buffer radii (100m, 500m, 1km, 5km)
3. Stepwise regression (or LASSO) selecting optimal predictors
4. Cross-validate with leave-one-out
5. Predict surface at target resolution

Limitation: requires dense monitoring network; captures long-term average better than short-term variation; interpolates poorly in areas without monitors.

### 2.2 Deep Learning for Air Quality

Replacing and augmenting LUR with neural network approaches:

**Spatial DL:** CNN applied to satellite imagery + auxiliary layers to predict surface PM2.5. Input: AOD band, RGB, land cover, road density raster. Architecture: U-Net for spatial interpolation task.

**Temporal DL:** LSTM or Transformer for air quality time series forecasting. Input: historical AQ + meteorology + emission proxies. Challenge: capturing both local and regional transport.

**Graph Neural Networks:** Represent monitoring network as a graph; GNN captures spatial dependencies without assuming isotropy (directionality of wind, road networks).

**Key papers:**
- Di et al. (2016) — annual PM2.5 from satellite AOD using deep learning, Environmental Health Perspectives.
- Chen et al. (2021) — high-resolution PM2.5 mapping with deep ensemble learning.
- Zheng et al. (2013, 2015) — air quality inference with urban computing, ACM KDD.

### 2.3 Satellite-Derived PM2.5

**Data sources:**
- MODIS MOD04 (10km) and MYD04 (Aqua 10km) AOD products
- MAIAC (Multi-Angle Implementation of Atmospheric Correction): 1km resolution AOD from MODIS, significantly improved cloud masking and land surface reflectance correction
- Sentinel-5P TROPOMI: daily global NO2, SO2, CO, O3 columns at 3.5-5.5 km resolution
- MERRA-2 reanalysis: global modeled PM2.5 with meteorological consistency

**PM2.5 estimation from AOD:**
AOD measures total column aerosol; surface PM2.5 depends on hygroscopic growth, boundary layer height, aerosol vertical profile, and composition.

Correction approaches:
- Chemical transport model (CTM) scaling: use GEOS-Chem or CESM to convert AOD to surface PM2.5 with meteorological adjustment
- Machine learning: train direct AOD → PM2.5 regression using co-located measurements (EPA AQS)
- Mixed effects LUR incorporating satellite AOD as predictor alongside traditional LUR variables

Best-in-class: two-stage hybrid models (Apte et al. 2021; van Donkelaar et al. 2021) produce global annual PM2.5 estimates at 0.01° (~1 km) from satellite + CTM + monitor calibration.

### 2.4 Street-Level Imagery for Built Environment

Google Street View (GSV) and Mapillary provide panoramic street-level imagery covering most urban areas globally. GeoAI methods extract built environment features:

- **Green View Index (GVI):** pixel fraction of vegetation from semantic segmentation. Proxy for perceived greenness, tree canopy from eye level.
- **Sky View Factor:** fraction of visible sky; related to urban canyon geometry and UHI effect.
- **Walkability and built environment quality:** pedestrian infrastructure, land use activity, building condition scoring.
- **Food environment audit:** classify food outlets visible in imagery.
- **Safety perception:** deep learning models predicting perceived safety ratings (Place Pulse dataset).

Key limitation: GSV image vintage varies by location (2007-present); coverage is street-accessible areas only; limited in rural, informal settlement, and Global South contexts.

### 2.5 Spatial Interpolation with Machine Learning

Estimating values at unmonitored locations using ML:
- Random Forest with spatial lag features and distance-to-monitor features
- Kriging + ML hybrids (regression kriging, random forest kriging)
- Gaussian process regression as principled Bayesian spatial interpolation
- Neural network kriging: replacing variogram fitting with learned spatial covariance

Key concept: all ML interpolation must be evaluated with spatial cross-validation (blocking or buffering) to avoid inflated performance from spatial autocorrelation leakage.

---

## 3. Environmental Justice

### 3.1 Foundational Concepts

Environmental justice (EJ): the principle that all people, regardless of race, income, national origin, or color, should have equal protection from environmental and health hazards, and equal access to decision-making processes.

Historical evidence: communities of color and low-income communities face higher exposure to air pollution, proximity to hazardous facilities, flood risk, heat, and lower access to green space and healthy food.

### 3.2 Cumulative Burden Indices

**CalEnviroScreen (California Office of Environmental Health Hazard Assessment):**
- Ranks census tracts by environmental burden AND social vulnerability
- Environmental indicators: ozone, PM2.5, diesel PM, pesticides, drinking water contaminants, cleanup sites, groundwater threats, hazardous waste, impaired waterways, solid waste sites
- Population vulnerability indicators: asthma ED visits, low birth weight, cardiovascular disease, educational attainment, linguistic isolation, poverty, unemployment, housing burden
- Score = (pollution burden) × (population characteristics)
- Version 4.0 (2021): 8,000+ CA census tracts

**EJSCREEN (EPA):**
- National EJ screening tool at census block group level
- Environmental indicators: air toxics cancer risk, diesel PM, ozone, PM2.5, traffic proximity, lead paint, Superfund proximity, RMP facility proximity, wastewater discharge, drinking water non-compliance
- Demographic indicators: low income, POC, linguistically isolated, less than HS education, low life expectancy, unemployment
- EJ Index = EI percentile × demographic index percentile

**EJScreen Limitations:** treats indicators as independent (no cumulative interaction); does not include health outcome data directly.

**CDCPlaces:** county and census tract-level estimates of chronic disease prevalence from CDC for 500+ Cities project and extension nationwide. Enables EJ analysis linking exposure to health outcomes.

### 3.3 Disparate Impact Testing

Formal methods to determine whether a policy, model, or allocation creates or perpetuates inequitable outcomes:
- Regression-based: test whether race/income variables explain residual exposure after controlling for geography
- Four-fifths rule (disparate impact in legal context): outcome for protected group < 80% of highest group
- Lorenz curve and Gini coefficient adapted to pollution burden
- Concentration indices (health economics)

GeoAI obligation: when deploying air quality models, resource allocation tools, or damage assessment systems, test for differential performance and outcomes across demographic groups.

---

## 4. Health Outcomes

### 4.1 Respiratory Disease
- Asthma: prevalence, emergency department visits, hospitalizations
- COPD (Chronic Obstructive Pulmonary Disease): irreversible airway obstruction
- Lung cancer: PM2.5 and radon exposure as major modifiable risk factors
- Acute respiratory infections: worsened by air pollution

GeoAI relevance: spatial prediction of asthma ED visit rates from environmental exposure + socioeconomic + built environment features; temporal forecasting of asthma attacks based on daily AQ and weather.

### 4.2 Cardiovascular Disease
PM2.5, noise, and extreme heat all independently increase CVD risk. Spatial epidemiology links proximity to highways (NO2/TRAP exposure) with CVD mortality.

### 4.3 Mental Health
Green space reduces stress and depression risk. Noise pollution disrupts sleep and elevates cortisol. Disaster displacement causes PTSD, depression, anxiety.

GeoAI: mapping neighborhood-level mental health risk from satellite-derived vegetation, street-level greenery, noise exposure models, and walkability indices.

### 4.4 Heat-Related Illness
Heat stroke and exhaustion are directly attributable to extreme heat exposure. Indirect health effects include worsened CVD and respiratory outcomes. GeoAI: predicting census tract-level heat mortality risk from LST, SVI, green space, housing type.

### 4.5 Vector-Borne Disease
Climate and land use changes expand geographic range of disease vectors (Aedes aegypti for dengue/Zika, Ixodes scapularis for Lyme disease, Anopheles mosquitoes for malaria).

GeoAI approaches: species distribution modeling (SDM) with MaxEnt, BRT, Random Forest; satellite-derived habitat suitability (temperature, precipitation, NDVI, standing water); forecasting range expansion under climate scenarios.

---

## 5. Epidemiological Frameworks

### 5.1 Exposome
Defined by Wild (2005) as "the totality of human environmental exposures from conception onwards." Complementary to genome. Includes: urban environment, diet, lifestyle, social environment, chemical exposures.

GeoAI supports exposome research by enabling high-resolution, multi-domain exposure assessment integrating dozens of environmental layers.

### 5.2 Health Impact Assessment (HIA)
Systematic process to evaluate potential health effects of a policy, plan, or project before decisions are made. Steps: screening, scoping, assessment (using epidemiological exposure-response functions), recommendations, evaluation.

GeoAI: quantifying exposure changes from proposed land use changes, transportation investments, or climate adaptation interventions; spatial distribution of health impacts.

### 5.3 Spatial Epidemiology
Analysis of geographic distribution of disease and its determinants. Methods: spatial cluster detection (SaTScan, Moran's I), ecological regression (disease rates on area-level exposures), spatial multilevel modeling, disease mapping (BYM model in INLA).

Key challenge: ecological fallacy (inferring individual-level relationships from area-level data). GeoAI partially addresses this by providing individual-level exposure estimates rather than area averages.

---

## 6. Data Sources

| Dataset | Source | Resolution | What it Contains |
|---|---|---|---|
| EPA AQS | EPA | Point (monitor) | Criteria pollutants: PM2.5, O3, NO2, SO2, CO, Pb at 4,000+ US monitors |
| CDC PLACES | CDC | Census tract / county | Chronic disease prevalence (asthma, diabetes, CVD, etc.) |
| US Census ACS | Census Bureau | Block group / tract | Income, race, housing, employment, education |
| MODIS MAIAC AOD | NASA | 1 km daily | Aerosol optical depth for PM2.5 estimation |
| Sentinel-5P TROPOMI | ESA | 3.5 km daily | NO2, O3, SO2, CO, CH4 column concentrations |
| NLCD | USGS/MRLC | 30 m | Land cover / land use classes for CONUS |
| OSM | OpenStreetMap | Vector | Roads, buildings, POIs, parks, water bodies |
| Google Street View | Google | Street-level panoramas | Built environment, vegetation, infrastructure |
| CalEnviroScreen | OEHHA | Census tract | CA cumulative environmental burden scores |
| EJSCREEN | EPA | Census block group | National EJ screening indicators |
| EPA TRI | EPA | Facility point | Industrial toxic releases by chemical and media |
| CDC WONDER | CDC | County / state | Mortality by cause, race, sex, age |
| Healthy Places Index | CPHD | Census tract | CA health opportunity domains |

---

## 7. Causal Inference in Spatial Epidemiology

### 7.1 Confounding in Spatial Contexts
Environmental exposures are spatially correlated with potential confounders: lower-income areas have both higher pollution AND worse food access AND less green space AND higher stress. Disentangling individual exposure effects requires careful confounding control.

Standard approaches:
- Covariate adjustment in regression: include socioeconomic, behavioral, and access covariates
- Propensity score methods: balance exposure groups on observed confounders; limited to point treatments
- Instrumental variable (IV): find an instrument exogenously varying exposure (e.g., wind direction as IV for downwind pollution)
- Regression discontinuity: exploit sharp geographic thresholds (regulatory borders, policy implementation zones)
- Difference-in-differences: compare change in health outcomes before/after a change in exposure for affected vs. control areas

### 7.2 Propensity Scores in Spatial Context
Spatial propensity scores balance treatment and control units on spatial confounders. Challenges: spatial autocorrelation in covariates, SUTVA (stable unit treatment value assumption) violated when spillover effects exist across space.

### 7.3 Spatial Causal Inference Frontier
Recent work uses causal forests (Wager & Athey, 2018) for heterogeneous treatment effect estimation; adapted for spatial data by incorporating geographic location as a feature and using spatial blocking for honest causal trees.

---

## 8. Research Gaps (2025–2026)

1. **Simultaneous multi-domain exposure integration:** current models typically estimate one exposure at a time (PM2.5 OR heat OR noise). Health is determined by the joint distribution of all exposures simultaneously. Unified multi-exposure models remain rare.

2. **Real-time personal exposure tracking:** static satellite-based exposure models assign one value per person per residential location per year. Mobile data (GPS traces, wearables) enable dynamic personal exposure estimation but raise profound privacy concerns.

3. **Longitudinal cohort studies with GeoAI exposures:** prospective cohorts with long-term health follow-up linked to GeoAI-derived exposure histories would provide stronger causal evidence than cross-sectional ecological studies.

4. **Global South environmental health GeoAI:** most methods validated in US/Europe with dense monitoring networks. Application in data-sparse African, South Asian, and Latin American contexts requires transfer learning, global-scale satellite methods, and local validation.

5. **Causal identification in observational GeoAI studies:** most GeoAI environmental health papers report associations, not causal effects. Rigorous causal identification strategies are underused.

6. **Uncertainty quantification and communication:** models produce point estimates; decision-makers need uncertainty bounds. Probabilistic output and uncertainty maps should be standard.

7. **Health outcome prediction from exposure:** linking GeoAI exposure maps to health outcome prediction (not just correlation) for policy-relevant health impact estimates.

---

## 9. Regulatory Context

### 9.1 US EPA Standards
- **NAAQS (National Ambient Air Quality Standards):** primary (health-based) and secondary (welfare-based) standards for 6 criteria pollutants. PM2.5 annual: 9 μg/m³ (revised 2024, reduced from 12 μg/m³). PM2.5 24-hour: 35 μg/m³. Ozone 8-hour: 70 ppb.
- **CERCLA (Superfund):** hazardous waste site cleanup program; HRS (Hazard Ranking System) determines National Priorities List inclusion.
- **TRI (Toxics Release Inventory):** EPCRA Section 313 reporting of toxic chemical releases by industrial facilities.
- **Title VI of Civil Rights Act:** prohibits discrimination in federally assisted programs; has been invoked in EJ contexts challenging siting decisions.

### 9.2 WHO Guidelines (2021 Update)
WHO tightened air quality guidelines in 2021 for the first time in 15 years:
- PM2.5 annual: 5 μg/m³ (from 10); 24-hour: 15 μg/m³ (from 25)
- PM10 annual: 15 μg/m³; 24-hour: 45 μg/m³
- NO2 annual: 10 μg/m³ (from 40); 24-hour: 25 μg/m³
- O3 peak season: 60 μg/m³; 8-hour: 100 μg/m³

Nearly all major global cities fail WHO PM2.5 guidelines; provides political framing for GeoAI research impact.

### 9.3 Environmental Impact Assessment (EIA)
Required for major federal projects in the US under NEPA (National Environmental Policy Act). GeoAI exposure modeling increasingly informs EIA health impact components.

---

## 10. Key Journals

- **Environmental Health Perspectives (EHP):** flagship journal of NIEHS; highest-impact env health journal. Strong methodological diversity including GeoAI methods.
- **GeoHealth (AGU):** interdisciplinary journal bridging geosciences and health; particularly receptive to GeoAI-environmental health work.
- **Science of the Total Environment:** broad environmental science; high volume, strong GeoAI presence.
- **Environmental Research:** Elsevier; broad scope including exposure science and epidemiology.
- **Environmental Science & Technology (ES&T):** ACS; strong analytical and exposure science emphasis.
- **The Lancet Planetary Health:** high-impact health + environment + climate nexus.
- **International Journal of Epidemiology:** methodological spatial epidemiology papers.
- **American Journal of Epidemiology:** traditional epidemiology with growing GeoAI content.
- **Environment International:** Elsevier; strong for multi-country environmental health studies.
- **IJGIS / JAG / Remote Sensing of Environment:** for the GeoAI methods side of environmental health work.
