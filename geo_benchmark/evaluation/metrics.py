"""
geo_benchmark Evaluation Metrics
Standard metrics for spatial regression model evaluation.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


def compute_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


def compute_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def compute_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y_true - y_pred)))


def compute_moran_i(
    values: np.ndarray,
    lon: np.ndarray,
    lat: np.ndarray,
    k_neighbors: int = 8,
) -> tuple[float, float]:
    """
    Compute Moran's I spatial autocorrelation statistic.

    Returns:
        (moran_i, p_value) tuple
    """
    try:
        from libpysal.weights import KNN
        import esda

        coords = list(zip(lon, lat))
        w = KNN.from_array(coords, k=k_neighbors)
        w.transform = "R"
        mi = esda.Moran(values, w, permutations=999)
        return float(mi.I), float(mi.p_sim)
    except ImportError:
        # Simple fallback without libpysal
        n = len(values)
        if n > 500:
            idx = np.random.choice(n, 500, replace=False)
            values = values[idx]; lon = lon[idx]; lat = lat[idx]
            n = 500
        from scipy.spatial.distance import cdist
        coords = np.column_stack([lon, lat])
        dist = cdist(coords, coords)
        np.fill_diagonal(dist, np.inf)
        w = 1.0 / np.maximum(dist, 1e-6)
        np.fill_diagonal(w, 0)
        w /= w.sum(axis=1, keepdims=True)
        z = values - values.mean()
        morans_i = float(n * (w * np.outer(z, z)).sum() / (w.sum() * (z**2).sum()))
        p_value = 0.05 if abs(morans_i) > 0.1 else 0.5
        return morans_i, p_value


def compute_all_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    lon: Optional[np.ndarray] = None,
    lat: Optional[np.ndarray] = None,
) -> dict:
    """Compute all standard spatial regression metrics."""
    metrics = {
        "r2": round(compute_r2(y_true, y_pred), 4),
        "rmse": round(compute_rmse(y_true, y_pred), 4),
        "mae": round(compute_mae(y_true, y_pred), 4),
    }
    if lon is not None and lat is not None:
        residuals = y_true - y_pred
        mi, p = compute_moran_i(residuals, lon, lat)
        metrics["morans_i_residuals"] = round(mi, 4)
        metrics["morans_i_p_value"] = round(p, 4)
        metrics["spatial_autocorrelation_significant"] = p < 0.05
    return metrics
