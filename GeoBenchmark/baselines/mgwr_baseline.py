"""
MGWR Baseline — Multiscale Geographically Weighted Regression.

Key advantage over GWR: Each predictor variable gets its own optimal bandwidth,
allowing simultaneous modeling of processes at different spatial scales.

Uses the mgwr library (https://github.com/pysal/mgwr).
Reference: Fotheringham, Yang, & Kang (2017). Annals of the AAG.

Usage:
    python GeoBenchmark/baselines/mgwr_baseline.py --dataset california_housing
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
    output_dir: str | Path = "GeoBenchmark/results/mgwr/",
    kernel: str = "bisquare",
    fixed: bool = False,
    max_n: int = 3000,
    tol: float = 1e-5,
    max_iter: int = 200,
) -> dict:
    """
    Fit MGWR model and return evaluation metrics.

    MGWR estimates a separate bandwidth for each predictor, revealing at which
    spatial scale each relationship operates.

    Args:
        dataset_path: Path to CSV
        dependent_var: Target column
        lat_col: Latitude column
        lon_col: Longitude column
        output_dir: Output directory
        kernel: 'bisquare' (default), 'gaussian', 'exponential'
        fixed: Fixed vs adaptive bandwidth
        max_n: Max observations (MGWR is slower than GWR)
        tol: Convergence tolerance for backfitting algorithm
        max_iter: Maximum backfitting iterations

    Returns:
        Dict of metrics
    """
    try:
        from mgwr.gwr import MGWR
        from mgwr.sel_bw import Sel_BW
    except ImportError:
        print("mgwr not installed. Run: pip install mgwr")
        return {"error": "mgwr not installed"}

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    df = pd.read_csv(dataset_path).dropna()
    print(f"Loaded {len(df)} observations")

    if len(df) > max_n:
        df = df.sample(n=max_n, random_state=42)
        print(f"Subsampled to {max_n} observations (MGWR memory/time constraint)")

    exclude_cols = {dependent_var, lat_col, lon_col}
    feature_cols = [c for c in df.columns if c not in exclude_cols]

    # Limit to reasonable number of features for MGWR (computational cost scales with features)
    if len(feature_cols) > 8:
        print(f"  Limiting to 8 features for MGWR (had {len(feature_cols)})")
        feature_cols = feature_cols[:8]

    X = df[feature_cols].values.astype(float)
    y = df[dependent_var].values.astype(float).reshape(-1, 1)
    coords = list(zip(df[lon_col], df[lat_col]))

    # Standardize
    X_mean, X_std_dev = X.mean(axis=0), X.std(axis=0)
    X_std_dev[X_std_dev == 0] = 1
    X_scaled = (X - X_mean) / X_std_dev

    y_mean, y_std_val = y.mean(), y.std()
    y_scaled = (y - y_mean) / y_std_val

    # Initial bandwidth selection using GWR (starting point for MGWR)
    print("Selecting initial bandwidth for MGWR (backfitting algorithm)...")
    selector = Sel_BW(coords, y_scaled, X_scaled, kernel=kernel, fixed=fixed, multi=True)
    bws = selector.search(multi_bw_min=[10] * len(feature_cols), multi_bw_max=[len(df)] * len(feature_cols))
    print(f"  Optimal bandwidths: {dict(zip(feature_cols, bws.tolist()))}")

    # Fit MGWR
    print("Fitting MGWR model (backfitting)...")
    mgwr_model = MGWR(
        coords, y_scaled, X_scaled,
        selector,
        kernel=kernel,
        fixed=fixed,
    )
    result = mgwr_model.fit(tol=tol, max_iter=max_iter)

    # Back-transform predictions
    y_pred = result.predy * y_std_val + y_mean
    y_actual = y.flatten()
    residuals = y_actual - y_pred.flatten()

    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_actual - y_actual.mean())**2)
    r2 = 1 - ss_res / ss_tot
    rmse = np.sqrt(np.mean(residuals**2))
    mae = np.mean(np.abs(residuals))

    local_r2 = result.localR2
    morans_i, morans_p = _quick_morans_i(residuals, df[lat_col].values, df[lon_col].values)

    # Per-variable bandwidths — the key MGWR output
    bandwidth_dict = {
        feature_cols[i]: int(bws[i]) if not fixed else float(bws[i])
        for i in range(len(feature_cols))
    }

    metrics = {
        "model": "MGWR",
        "dataset": str(dataset_path),
        "n_observations": len(df),
        "n_features": len(feature_cols),
        "bandwidths_per_variable": bandwidth_dict,
        "kernel": kernel,
        "fixed_bandwidth": fixed,
        "convergence_iterations": getattr(result, "n_iter", None),
        "r2": round(float(r2), 4),
        "rmse": round(float(rmse), 4),
        "mae": round(float(mae), 4),
        "aic": round(float(result.aicc), 2),
        "local_r2_mean": round(float(np.mean(local_r2)), 4),
        "local_r2_std": round(float(np.std(local_r2)), 4),
        "local_r2_min": round(float(local_r2.min()), 4),
        "local_r2_max": round(float(local_r2.max()), 4),
        "morans_i_residuals": round(float(morans_i), 4),
        "morans_i_p_value": round(float(morans_p), 4),
        "spatial_autocorrelation_in_residuals": morans_p < 0.05,
        "feature_names": feature_cols,
    }

    # Save local coefficients
    coef_df = pd.DataFrame(result.params, columns=["intercept"] + feature_cols)
    coef_df["lat"] = df[lat_col].values
    coef_df["lon"] = df[lon_col].values
    coef_df["local_r2"] = local_r2
    coef_df["residuals"] = residuals

    # Add t-values for significance filtering
    if hasattr(result, "tvalues"):
        t_df = pd.DataFrame(result.tvalues, columns=[f"t_{c}" for c in ["intercept"] + feature_cols])
        coef_df = pd.concat([coef_df, t_df], axis=1)

    coef_df.to_csv(output_dir / "mgwr_local_coefficients.csv", index=False)

    result_path = output_dir / "mgwr_results.json"
    result_path.write_text(json.dumps(metrics, indent=2))

    print(f"\nMGWR Results:")
    print(f"  R²:               {metrics['r2']:.4f}")
    print(f"  RMSE:             {metrics['rmse']:.4f}")
    print(f"  Local R² (mean):  {metrics['local_r2_mean']:.4f} ± {metrics['local_r2_std']:.4f}")
    print(f"  AICc:             {metrics['aic']:.2f}")
    print(f"  Moran's I:        {metrics['morans_i_residuals']:.4f} (p={metrics['morans_i_p_value']:.4f})")
    print(f"  Variable bandwidths:")
    for var, bw in bandwidth_dict.items():
        scale = "global" if bw > 0.8 * len(df) else ("regional" if bw > 0.3 * len(df) else "local")
        print(f"    {var}: {bw} neighbors ({scale} scale)")
    print(f"  Local coefficients → {output_dir / 'mgwr_local_coefficients.csv'}")
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
    parser = argparse.ArgumentParser(description="Run MGWR baseline")
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output", type=str, default="GeoBenchmark/results/mgwr/")
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
