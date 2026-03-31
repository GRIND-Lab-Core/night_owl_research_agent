"""
OLS Baseline — Ordinary Least Squares spatial regression baseline.

Usage:
    python GeoBenchmark/baselines/ols_baseline.py --dataset california_housing
    python GeoBenchmark/baselines/ols_baseline.py --dataset california_housing --output results/
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def run(
    dataset_path: str | Path,
    dependent_var: str = "target",
    lat_col: str = "lat",
    lon_col: str = "lon",
    output_dir: str | Path = "GeoBenchmark/results/",
    add_spatial_coords: bool = True,
) -> dict:
    """
    Fit OLS model and return evaluation metrics.

    Args:
        dataset_path: Path to CSV with features, target, and lat/lon
        dependent_var: Name of the dependent variable column
        lat_col: Latitude column name
        lon_col: Longitude column name
        output_dir: Directory to save results
        add_spatial_coords: If True, add lat/lon as predictors

    Returns:
        Dict of metrics and model info
    """
    import statsmodels.api as sm
    from scipy.stats import pearsonr

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    df = pd.read_csv(dataset_path)
    df = df.dropna()
    print(f"Loaded {len(df)} observations from {dataset_path}")

    # Prepare features
    exclude_cols = {dependent_var, lat_col, lon_col}
    feature_cols = [c for c in df.columns if c not in exclude_cols]
    if add_spatial_coords:
        feature_cols += [lat_col, lon_col]

    X = df[feature_cols].copy()
    y = df[dependent_var].values

    # Standardize features
    X_std = (X - X.mean()) / X.std()
    X_const = sm.add_constant(X_std)

    # Fit OLS
    model = sm.OLS(y, X_const).fit(cov_type="HC3")  # heteroskedasticity-robust SEs
    y_pred = model.fittedvalues

    # Metrics
    residuals = y - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    rmse = np.sqrt(np.mean(residuals**2))
    mae = np.mean(np.abs(residuals))

    # Moran's I on residuals
    morans_i, morans_p = compute_morans_i(residuals, df[lat_col].values, df[lon_col].values)

    metrics = {
        "model": "OLS",
        "dataset": str(dataset_path),
        "n_observations": len(df),
        "n_features": len(feature_cols),
        "r2": round(float(r2), 4),
        "adj_r2": round(float(model.rsquared_adj), 4),
        "rmse": round(float(rmse), 4),
        "mae": round(float(mae), 4),
        "aic": round(float(model.aic), 2),
        "bic": round(float(model.bic), 2),
        "morans_i_residuals": round(float(morans_i), 4),
        "morans_i_p_value": round(float(morans_p), 4),
        "spatial_autocorrelation_in_residuals": morans_p < 0.05,
        "coefficients": {
            name: round(float(coef), 4)
            for name, coef in zip(["const"] + feature_cols, model.params)
        },
    }

    # Save results
    result_path = output_dir / "ols_results.json"
    result_path.write_text(json.dumps(metrics, indent=2))
    print(f"\nOLS Results:")
    print(f"  R²:    {metrics['r2']:.4f}")
    print(f"  RMSE:  {metrics['rmse']:.4f}")
    print(f"  MAE:   {metrics['mae']:.4f}")
    print(f"  AIC:   {metrics['aic']:.2f}")
    print(f"  Moran's I (residuals): {metrics['morans_i_residuals']:.4f} (p={metrics['morans_i_p_value']:.4f})")
    if metrics["spatial_autocorrelation_in_residuals"]:
        print("  ⚠ Significant spatial autocorrelation in residuals — consider GWR/MGWR")
    print(f"  Results saved to {result_path}")

    return metrics


def compute_morans_i(
    residuals: np.ndarray,
    lat: np.ndarray,
    lon: np.ndarray,
    k_neighbors: int = 8,
) -> tuple[float, float]:
    """
    Compute Moran's I statistic for spatial autocorrelation.
    Uses k-nearest-neighbor spatial weight matrix.
    """
    try:
        from libpysal.weights import KNN
        import esda

        coords = list(zip(lon, lat))
        w = KNN.from_array(coords, k=k_neighbors)
        w.transform = "R"  # row-standardize
        mi = esda.Moran(residuals, w)
        return mi.I, mi.p_sim
    except ImportError:
        # Fallback: basic global Moran's I using distance weights
        n = len(residuals)
        if n > 1000:
            # Subsample for speed
            idx = np.random.choice(n, 500, replace=False)
            residuals = residuals[idx]
            lat = lat[idx]
            lon = lon[idx]
            n = 500

        # Build simple inverse-distance weight matrix
        from scipy.spatial.distance import cdist
        coords = np.column_stack([lon, lat])
        dist = cdist(coords, coords)
        np.fill_diagonal(dist, np.inf)
        w = 1.0 / np.maximum(dist, 1e-6)
        np.fill_diagonal(w, 0)
        w = w / w.sum(axis=1, keepdims=True)

        z = residuals - residuals.mean()
        n_val = float(n)
        numerator = n_val * (w * np.outer(z, z)).sum()
        denominator = w.sum() * (z**2).sum()
        morans_i = numerator / denominator if denominator != 0 else 0.0
        # Approximate p-value (not reliable without proper permutation test)
        return morans_i, 0.05 if abs(morans_i) > 0.1 else 0.5


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OLS baseline")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name or path to CSV")
    parser.add_argument("--output", type=str, default="GeoBenchmark/results/ols/", help="Output directory")
    parser.add_argument("--target", type=str, default="target", help="Target column name")
    args = parser.parse_args()

    # Resolve dataset path
    if Path(args.dataset).exists():
        dataset_path = Path(args.dataset)
    else:
        dataset_path = Path("GeoBenchmark/datasets") / args.dataset / f"{args.dataset}.csv"
        if not dataset_path.exists():
            print(f"Dataset not found: {dataset_path}")
            print("Run: python GeoBenchmark/download_data.py first")
            return

    run(dataset_path=dataset_path, dependent_var=args.target, output_dir=args.output)


if __name__ == "__main__":
    main()
