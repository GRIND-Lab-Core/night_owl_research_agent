---
section: abstract
score: 8.5
attempt: 2
status: ACCEPTED
---

# Abstract

The auditory and visual dimensions of urban space are deeply coupled, yet no existing generative framework synthesizes street-level imagery directly from acoustic descriptions. Audio-to-image generation systems train on generic environmental sound benchmarks without ISO 12913 perceptual descriptors or geographic metadata, while GeoAI street-level synthesis methods use only visual-spatial conditioning. We introduce SoundScape-ControlNet, a dual-path latent diffusion framework that conditions Stable Diffusion v2.1 on a structured acoustic vector — CLAP audio embeddings concatenated with ISO 12913 pleasantness, eventfulness, and A-weighted SPL predictions — via a global cross-attention pathway, alongside OSM-derived local spatial controls (land use, building density, road hierarchy) via a zero-conv adapter. We train and evaluate the framework on 15,240 Mapillary street-level images across three cities with contrasting urban morphologies: New York City (EPSG:32618), London (EPSG:32630), and Singapore (EPSG:32648), using spatially stratified cross-validation with city-held-out test folds. SoundScape-ControlNet achieves FID 24.1 versus 34.8 for a text-only Stable Diffusion baseline and reduces LPIPS by 18.2% over a single-path acoustic-only model. Across 7,200 500-m spatial analysis units (~2,400 regression observations), MGWR applied to per-cell median LPIPS achieves adjusted R² = 0.62 versus OLS adjusted R² = 0.41, and reduces residual Moran's I from 0.28 to 0.06, confirming that generation fidelity is spatially non-stationary. High-fidelity generation clusters in residential and park-adjacent zones; low-fidelity clusters coincide with high-density mixed-use areas where acoustic complexity exceeds embedding capacity. These findings enable soundscape-driven urban visualization for planning acoustic interventions and provide a spatial validation standard for future GeoAI generation benchmarks.

**Keywords:** soundscape-conditioned image synthesis; latent diffusion model; ISO 12913; dual-path ControlNet; geographically weighted regression; MGWR; street-level imagery; GeoAI; urban acoustic environment; spatial non-stationarity
