"""
geo_benchmark Visualization
Generates maps, scatter plots, and residual diagnostics for model outputs.

Usage:
    python geo_benchmark/evaluation/visualize.py --results geo_benchmark/results/california_housing/
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_coefficient_map(
    coef_df: pd.DataFrame,
    variable: str,
    output_path: Path,
    title: str = "",
    crs: str = "EPSG:4326",
) -> None:
    """Plot a map of local GWR/MGWR coefficients."""
    try:
        import geopandas as gpd
        from shapely.geometry import Point
        import contextily as ctx

        gdf = gpd.GeoDataFrame(
            coef_df,
            geometry=[Point(xy) for xy in zip(coef_df["lon"], coef_df["lat"])],
            crs=crs,
        )

        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        gdf.plot(
            column=variable,
            cmap="RdYlBu_r",
            legend=True,
            legend_kwds={"label": variable, "orientation": "horizontal", "shrink": 0.6},
            markersize=5,
            ax=ax,
        )
        try:
            gdf_web = gdf.to_crs(epsg=3857)
            ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron, alpha=0.5)
        except Exception:
            pass

        ax.set_title(title or f"Local Coefficients: {variable}", fontsize=14, fontweight="bold")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"  Saved: {output_path}")

    except ImportError:
        _fallback_scatter_map(coef_df, variable, output_path, title)


def _fallback_scatter_map(coef_df: pd.DataFrame, variable: str, output_path: Path, title: str) -> None:
    """Fallback scatter map without geopandas/contextily."""
    fig, ax = plt.subplots(figsize=(10, 7))
    sc = ax.scatter(
        coef_df["lon"], coef_df["lat"],
        c=coef_df[variable], cmap="RdYlBu_r",
        s=10, alpha=0.7,
    )
    plt.colorbar(sc, ax=ax, label=variable, orientation="horizontal", pad=0.05, shrink=0.6)
    ax.set_title(title or f"Local Coefficients: {variable}", fontsize=14)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


def plot_residuals_map(coef_df: pd.DataFrame, output_path: Path) -> None:
    """Plot residuals map with diverging colormap."""
    _fallback_scatter_map(coef_df, "residuals", output_path, "Prediction Residuals")


def plot_local_r2_map(coef_df: pd.DataFrame, output_path: Path) -> None:
    """Plot local R² map."""
    _fallback_scatter_map(coef_df, "local_r2", output_path, "Local R²")


def plot_comparison_bar(results: list[dict], output_path: Path) -> None:
    """Bar chart comparing models on R², RMSE, MAE."""
    models = [r.get("model", "?") for r in results if "error" not in r]
    r2s = [r.get("r2", 0) for r in results if "error" not in r]
    rmses = [r.get("rmse", 0) for r in results if "error" not in r]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    bars1 = ax1.bar(models, r2s, color=["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"][:len(models)])
    ax1.set_title("R² Comparison", fontsize=13, fontweight="bold")
    ax1.set_ylabel("R²")
    ax1.set_ylim(0, 1)
    for bar, val in zip(bars1, r2s):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{val:.3f}", ha="center", fontsize=10)

    bars2 = ax2.bar(models, rmses, color=["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"][:len(models)])
    ax2.set_title("RMSE Comparison", fontsize=13, fontweight="bold")
    ax2.set_ylabel("RMSE")
    for bar, val in zip(bars2, rmses):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001, f"{val:.3f}", ha="center", fontsize=10)

    plt.suptitle("geo_benchmark Model Comparison", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate geo_benchmark visualizations")
    parser.add_argument("--results", type=str, default="geo_benchmark/results/", help="Results directory")
    parser.add_argument("--dataset", type=str, default="", help="Dataset name")
    args = parser.parse_args()

    results_dir = Path(args.results)
    figs_dir = results_dir / "figures"
    figs_dir.mkdir(parents=True, exist_ok=True)

    print("Generating visualizations...")

    # GWR coefficient maps
    for model in ["gwr", "mgwr"]:
        coef_file = results_dir / model / f"{model}_local_coefficients.csv"
        if coef_file.exists():
            coef_df = pd.read_csv(coef_file)
            plot_local_r2_map(coef_df, figs_dir / f"{model}_local_r2.png")
            plot_residuals_map(coef_df, figs_dir / f"{model}_residuals.png")

            # Plot first non-intercept coefficient
            feat_cols = [c for c in coef_df.columns if c not in ("lat", "lon", "local_r2", "residuals", "intercept") and not c.startswith("t_")]
            if feat_cols:
                plot_coefficient_map(coef_df, feat_cols[0], figs_dir / f"{model}_coef_{feat_cols[0]}.png")

    print(f"Figures saved to {figs_dir}")


if __name__ == "__main__":
    main()
