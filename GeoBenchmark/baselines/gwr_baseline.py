"""
GWR Baseline — Geographically Weighted Regression.

Uses the mgwr library (https://github.com/pysal/mgwr).
Adaptive bi-square kernel with AICc-based bandwidth selection.

Usage:
    python GeoBenchmark/baselines/gwr_baseline.py --dataset california_housing
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
    output_dir: str | Path = "GeoBenchmark/results/gwr/",
    kernel: str = "bisquare",
    fixed: bool = False,
    max_n: int = 5000,
) -> dict:
    """
    Fit GWR model and return evaluation metrics.

    Args:
        dataset_path: Path to CSV with features, target, and lat/lon
        dependent_var: Dependent variable column name
        lat_col: Latitude column name
        lon_col: Longitude column name
        output_dir: Directory to save results
        kernel: Kernel type ('bisquare', 'gaussian', 'exponential')
        fixed: If True, use fixed bandwidth; if False, use adaptive (k neighbors)
        max_n: Maximum observations (subsample if larger, GWR is O(n²))

    Returns:
        Dict of metrics and model info
    """
    try:
        from mgwr.gwr import GWR
        from mgwr.sel_bw import Sel_BW
    except ImportError:
        print("mgwr not installed. Run: pip install mgwr")
        return {"error": "mgwr not installed"}

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load and prepare data
    df = pd.read_csv(dataset_path).dropna()
    print(f"Loaded {len(df)} observations")

    # Subsample for large datasets (GWR is O(n²) in memory)
    if len(df) > max_n:
        df = df.sample(n=max_n, random_state=42)
        print(f"Subsampled to {max_n} observations (GWR memory constraint)")

    exclude_cols = {dependent_var, lat_col, lon_col}
    feature_cols = [c for c in df.columns if c not in exclude_cols]

    X = df[feature_cols].values.astype(float)
    y = df[dependent_var].values.astype(float).reshape(-1, 1)
    coords = list(zip(df[lon_col], df[lat_col]))

    # Standardize
    X_mean, X_std_dev = X.mean(axis=0), X.std(axis=0)
    X_std_dev[X_std_dev == 0] = 1  # avoid division by zero
    X_scaled = (X - X_mean) / X_std_dev

    y_mean, y_std_val = y.mean(), y.std()
    y_scaled = (y - y_mean) / y_std_val

    # Bandwidth selection via AICc
    print("Selecting optimal bandwidth (AICc minimization)...")
    selector = Sel_BW(coords, y_scaled, X_scaled, kernel=kernel, fixed=fixed, multi=False)
    bw = selector.search(bw_min=10 if not fixed else None)
    print(f"  Optimal bandwidth: {bw} {'meters' if fixed else 'neighbors'}")

    # Fit GWR
    print("Fitting GWR model...")
    model = GWR(coords, y_scaled, X_scaled, bw=bw, kernel=kernel, fixed=fixed)
    result = model.fit()

    # Back-transform predictions
    y_pred = result.predy * y_std_val + y_mean
    y_actual = y.flatten()
    residuals = y_actual - y_pred.flatten()

    # Global metrics
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_actual - y_actual.mean())**2)
    r2 = 1 - ss_res / ss_tot
    rmse = np.sqrt(np.mean(residuals**2))
    mae = np.mean(np.abs(residuals))

    # Local R² statistics
    local_r2 = result.localR2
    local_r2_mean = float(np.mean(local_r2))
    local_r2_std = float(np.std(local_r2))

    # Moran's I on residuals
    morans_i, morans_p = _quick_morans_i(residuals, df[lat_col].values, df[lon_col].values)

    metrics = {
        "model": "GWR",
        "dataset": str(dataset_path),
        "n_observations": len(df),
        "n_features": len(feature_cols),
        "bandwidth": float(bw),
        "kernel": kernel,
        "fixed_bandwidth": fixed,
        "r2": round(float(r2), 4),
        "rmse": round(float(rmse), 4),
        "mae": round(float(mae), 4),
        "aic": round(float(result.aicc), 2),
        "local_r2_mean": round(local_r2_mean, 4),
        "local_r2_std": round(local_r2_std, 4),
        "local_r2_min": round(float(local_r2.min()), 4),
        "local_r2_max": round(float(local_r2.max()), 4),
        "morans_i_residuals": round(float(morans_i), 4),
        "morans_i_p_value": round(float(morans_p), 4),
        "spatial_autocorrelation_in_residuals": morans_p < 0.05,
        "feature_names": feature_cols,
    }

    # Save local coefficients for mapping
    coef_df = pd.DataFrame(
        result.params,
        columns=["intercept"] + feature_cols,
    )
    coef_df["lat"] = df[lat_col].values
    coef_df["lon"] = df[lon_col].values
    coef_df["local_r2"] = local_r2
    coef_df["residuals"] = residuals
    coef_df.to_csv(output_dir / "gwr_local_coefficients.csv", index=False)

    result_path = output_dir / "gwr_results.json"
    result_path.write_text(json.dumps(metrics, indent=2))

    print(f"\nGWR Results:")
    print(f"  Bandwidth:        {bw}")
    print(f"  R²:               {metrics['r2']:.4f}")
    print(f"  RMSE:             {metrics['rmse']:.4f}")
    print(f"  Local R² (mean):  {metrics['local_r2_mean']:.4f} ± {metrics['local_r2_std']:.4f}")
    print(f"  AICc:             {metrics['aic']:.2f}")
    print(f"  Moran's I:        {metrics['morans_i_residuals']:.4f} (p={metrics['morans_i_p_value']:.4f})")
    print(f"  Local coefficients → {output_dir / 'gwr_local_coefficients.csv'}")
    print(f"  Results → {result_path}")

    return metrics


def _quick_morans_i(residuals: np.ndarray, lat: np.ndarray, lon: np.ndarray, k: int = 8) -> tuple[float, float]:
    try:
        from libpysal.weights import KNN
        import esda
        coords = list(zip(lon, lat))
        w = KNN.from_array(coords, k=k)
        w.transform = "R"
        mi = esda.Moran(residuals, w)
        return mi.I, mi.p_sim
    except ImportError:
        return 0.0, 1.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run GWR baseline")
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output", type=str, default="GeoBenchmark/results/gwr/")
    parser.add_argument("--target", type=str, default="target")
    parser.add_argument("--kernel", type=str, default="bisquare")
    parser.add_argument("--fixed", action="store_true")
    args = parser.parse_args()

    if Path(args.dataset).exists():
        dataset_path = Path(args.dataset)
    else:
        dataset_path = Path("GeoBenchmark/datasets") / args.dataset / f"{args.dataset}.csv"

    run(
        dataset_path=dataset_path,
        dependent_var=args.target,
        output_dir=args.output,
        kernel=args.kernel,
        fixed=args.fixed,
    )


if __name__ == "__main__":
    main()
