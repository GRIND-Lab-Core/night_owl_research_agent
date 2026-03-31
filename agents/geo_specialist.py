"""
Geo Specialist Agent — injects domain-specific context into all research stages.
Acts as a persistent domain expert layer that augments other agents.
"""

from __future__ import annotations

from typing import Any

import anthropic

from core.config import AgentConfig


class GeoSpecialistAgent:
    """
    Provides geo-domain context injection for other agents.
    Does not run independently — called by the orchestrator to enrich prompts.
    """

    DOMAIN_PATTERNS = {
        "giscience": ["gis", "gwr", "mgwr", "spatial regression", "spatial autocorrelation",
                      "geostatistic", "kriging", "spatial lag", "spatial weights", "choroplet"],
        "remote_sensing": ["sar", "optical", "lidar", "radar", "satellite", "landsat", "sentinel",
                           "ndvi", "classification", "change detection", "hyperspectral"],
        "geoscience": ["seismic", "geology", "hydrology", "climate", "geophysics",
                       "dem", "topography", "geomorphology", "lithology"],
    }

    def __init__(self, client: anthropic.Anthropic, config: AgentConfig) -> None:
        self.client = client
        self.config = config

    def infer_domain(self, topic: str) -> str:
        topic_lower = topic.lower()
        scores = {
            domain: sum(1 for kw in keywords if kw in topic_lower)
            for domain, keywords in self.DOMAIN_PATTERNS.items()
        }
        return max(scores, key=scores.get, default="giscience")

    def get_context(self, topic: str) -> dict[str, Any]:
        """Build geo-domain context dict for injection into agent prompts."""
        domain = self.infer_domain(topic)
        return {
            "domain": domain,
            "relevant_methods": self._get_methods(domain, topic),
            "recommended_software": self._get_software(domain),
            "open_data_sources": self._get_data_sources(domain),
            "evaluation_standards": self._get_eval_standards(domain),
            "common_pitfalls": self._get_pitfalls(domain),
        }

    def _get_methods(self, domain: str, topic: str) -> list[str]:
        methods = {
            "giscience": ["OLS", "GWR", "MGWR", "Spatial Lag/Error Models", "Kriging", "Moran's I"],
            "remote_sensing": ["Random Forest", "CNN", "Transformer", "SVM", "OBIA", "SAM"],
            "geoscience": ["Interpolation", "Geostatistics", "Climate Models", "Hydrological Models"],
        }
        return methods.get(domain, methods["giscience"])

    def _get_software(self, domain: str) -> list[str]:
        software = {
            "giscience": ["Python/geopandas", "mgwr", "pysal", "R/spdep", "GWmodel (R)", "QGIS"],
            "remote_sensing": ["Python/rasterio", "earthpy", "Google Earth Engine", "SNAP", "ENVI"],
            "geoscience": ["Python/xarray", "GMT", "MATLAB", "ArcGIS Pro", "SAGA GIS"],
        }
        return software.get(domain, software["giscience"])

    def _get_data_sources(self, domain: str) -> list[str]:
        sources = {
            "giscience": ["US Census (data.census.gov)", "OSM (geofabrik.de)", "GADM (gadm.org)",
                          "OpenStreetMap", "World Bank Open Data"],
            "remote_sensing": ["USGS EarthExplorer", "Copernicus Open Access Hub",
                               "NASA Earthdata", "Google Earth Engine", "JAXA G-Portal"],
            "geoscience": ["USGS Science Data Catalog", "NOAA Climate Data Online",
                           "Copernicus CDS", "SRTM (OpenTopography)", "PANGAEA"],
        }
        return sources.get(domain, sources["giscience"])

    def _get_eval_standards(self, domain: str) -> list[str]:
        standards = {
            "giscience": ["R², RMSE, MAE", "Moran's I on residuals", "AIC/AICc", "Local R² (GWR/MGWR)"],
            "remote_sensing": ["OA, Kappa, F1 per class", "RMSE (regression)", "Confusion matrix"],
            "geoscience": ["NSE (Nash-Sutcliffe)", "KGE (Kling-Gupta)", "Bias, PBIAS"],
        }
        return standards.get(domain, standards["giscience"])

    def _get_pitfalls(self, domain: str) -> list[str]:
        pitfalls = {
            "giscience": [
                "Ignoring spatial autocorrelation (use Moran's I first)",
                "Using random train/test splits (spatial leakage)",
                "Wrong CRS for area/distance calculations",
                "Ignoring MAUP (Modifiable Areal Unit Problem)",
            ],
            "remote_sensing": [
                "Using training pixels adjacent to test pixels (spatial leakage)",
                "Reporting only overall accuracy (omit per-class metrics)",
                "Not correcting for atmospheric effects",
                "Mixing image dates without cloud/shadow masking",
            ],
            "geoscience": [
                "Ignoring non-stationarity in time series",
                "Using inappropriate projection for area calculations",
                "Extrapolating beyond training data extent",
            ],
        }
        return pitfalls.get(domain, pitfalls["giscience"])
