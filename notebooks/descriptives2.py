"""
descriptives.py — High-quality descriptive analysis outputs (LaTeX + figures).

Functions:
- countries_per_region_table
- summary_stats_table
- histogram_mean_spread_over_time
- correlation_matrix_table
- vif_table
- build_all_descriptives

All tables are wrapped to fit page width (booktabs + siunitx + threeparttable).
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


def _ensure_outdir(out_dir: Path) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def _latex_table_wrapper(tex_body: str,
                         caption: str,
                         label: str,
                         note: Optional[str] = None,
                         landscape: bool = False) -> str:
    env_begin = "\\begin{table}[!htbp]\n\\centering\n\\begin{threeparttable}\n\\resizebox{\\textwidth}{!}{%\n"
    env_end = "}\n"
    if note:
        env_end += f"\\begin{{tablenotes}}[flushleft]\\footnotesize\\item {note}\\end{{tablenotes}}\n"
    env_end += f"\\caption{{{caption}}}\n\\label{{{label}}}\n\\end{{threeparttable}}\n\\end{{table}}\n"
    wrapped = env_begin + tex_body.strip() + "\n" + env_end
    if landscape:
        wrapped = "\\begin{landscape}\n" + wrapped + "\\end{landscape}\n"
    return wrapped


def _format_numeric_cols(df: pd.DataFrame) -> pd.DataFrame:
    num = df.select_dtypes(include=[np.number]).copy()
    num = num.loc[:, num.notna().any(axis=0)]
    return num


def countries_per_region_table(df: pd.DataFrame,
                               out_dir: Path,
                               region_col: str = "region",
                               country_col: str = "iso3c") -> Path:
    out_dir = _ensure_outdir(out_dir)
    counts = (df[[region_col, country_col]]
              .dropna(subset=[region_col, country_col])
              .drop_duplicates(subset=[region_col, country_col])
              .groupby(region_col)[country_col].nunique()
              .rename("Countries")
              .reset_index())
    counts = counts.sort_values("Countries", ascending=False)

    tex_body = counts.to_latex(index=False,
                               escape=True,
                               na_rep="",
                               float_format="%.0f",
                               column_format="lS",
                               bold_rows=False)
    tex_body = tex_body.replace("\\begin{tabular}{", "\\begin{tabular}{@{}")
    tex_body = tex_body.replace("lS}", "l S[table-format=3.0] @{} }")

    tex = _latex_table_wrapper(
        tex_body,
        caption="Number of unique countries by region.",
        label="tab:countries_by_region",
        note="Regions follow the dataset's own classification. Counts are unique by (region, country)."
    )

    path = out_dir / "countries_by_region.tex"
    path.write_text(tex, encoding="utf-8")
    return path


def summary_stats_table(df: pd.DataFrame,
                        out_dir: Path,
                        exclude: Optional[List[str]] = None,
                        decimals: int = 3) -> Path:
    out_dir = _ensure_outdir(out_dir)
    num = _format_numeric_cols(df)
    if exclude:
        num = num.drop(columns=[c for c in exclude if c in num.columns], errors="ignore")

    stats = pd.DataFrame({
        "N": num.count(),
        "Mean": num.mean(),
        "SD": num.std(),
        "Min": num.min(),
        "P25": num.quantile(0.25),
        "Median": num.median(),
        "P75": num.quantile(0.75),
        "Max": num.max(),
    }).reset_index().rename(columns={"index": "Variable"})

    stats = stats.sort_values("Variable").reset_index(drop=True)

    col_formats = ["l"] + ["S" for _ in range(8)]
    tex_body = stats.to_latex(index=False,
                              escape=True,
                              na_rep="",
                              float_format=(lambda x: f"{x:.{decimals}f}"),
                              column_format="".join(col_formats),
                              bold_rows=False)
    tex_body = tex_body.replace("\\begin{tabular}{", "\\begin{tabular}{@{}") \
                       .replace("}", " @{} }", 1)

    tex = _latex_table_wrapper(
        tex_body,
        caption="Summary statistics for numeric variables.",
        label="tab:summary_stats",
        note="Statistics computed on available observations. Values are not winsorized unless otherwise noted."
    )

    path = out_dir / "summary_stats.tex"
    path.write_text(tex, encoding="utf-8")
    return path


def plot_mean_spread_over_time(
    df: pd.DataFrame,
    out_dir: Path,
    spread_col: str = "sovereign_spread",
    year_col: str = "year",
    start_year: int = 1995,
    end_year: int = 2024
) -> Path:
    """
    Line plot of annual mean sovereign spreads over time.
    """
    out_dir = _ensure_outdir(out_dir)
    d = (
        df[[year_col, spread_col]]
        .dropna()
        .query(f"{year_col} >= @start_year and {year_col} <= @end_year")
        .groupby(year_col)[spread_col].mean()
        .rename("mean_spread")
        .reset_index()
    )

    plt.figure(figsize=(7, 4))
    plt.plot(d[year_col], d["mean_spread"], marker="o", linestyle="-", color="darkblue")
    plt.xlabel("Year")
    plt.ylabel("Annual mean sovereign spread")
    plt.title(f"Annual mean sovereign spreads, {start_year}–{end_year}")
    plt.grid(True, linestyle="--", alpha=0.6)

    fig_path = out_dir / f"line_mean_spread_{start_year}_{end_year}.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    return fig_path


def correlation_matrix_table(df: pd.DataFrame,
                             out_dir: Path,
                             max_vars: int = 15,
                             prefer_vars: Optional[List[str]] = None,
                             decimals: int = 2) -> Path:
    out_dir = _ensure_outdir(out_dir)
    num = _format_numeric_cols(df)

    cols: List[str] = []
    if prefer_vars:
        cols.extend([c for c in prefer_vars if c in num.columns])
    remaining = [c for c in num.columns if c not in cols]
    remaining.sort()
    cols.extend(remaining[: max(0, max_vars - len(cols))])

    corr = num[cols].corr().round(decimals)

    body = corr.to_latex(escape=True,
                         na_rep="",
                         column_format="l" + "r" * len(cols))
    body = body.replace("\\begin{tabular}{", "\\begin{tabular}{@{}") \
               .replace("}", " @{} }", 1)

    tex = _latex_table_wrapper(
        body,
        caption="Pearson correlation matrix (subset of variables).",
        label="tab:corr_matrix",
        note="Diagonal equals 1. Off-diagonals show pairwise correlations. Subset chosen to fit page width."
    )
    path = out_dir / "correlation_matrix.tex"
    path.write_text(tex, encoding="utf-8")
    return path


def vif_table(df: pd.DataFrame,
              out_dir: Path,
              features: Optional[List[str]] = None,
              add_constant: bool = True,
              impute_knn: bool = True,
              n_neighbors: int = 5,
              scale: bool = True,
              decimals: int = 2) -> Path:
    out_dir = _ensure_outdir(out_dir)
    num = _format_numeric_cols(df)

    if features is None:
        drop_like = {"year"}
        features = [c for c in num.columns if c not in drop_like]

    X = num[features].copy()

    if impute_knn:
        X = pd.DataFrame(KNNImputer(n_neighbors=n_neighbors).fit_transform(X),
                         columns=X.columns)

    if add_constant:
        X = sm.add_constant(X, has_constant="add")

    if scale:
        cols_to_scale = [c for c in X.columns if c != "const"]
        X[cols_to_scale] = StandardScaler().fit_transform(X[cols_to_scale])

    vif_rows: List[Tuple[str, float, float, float]] = []
    cols = list(X.columns)
    for i, col in enumerate(cols):
        if col == "const":
            continue
        v = variance_inflation_factor(X.values, i)
        if np.isfinite(v):
            r2 = 1.0 - 1.0 / v if v > 0 else np.nan
            tol = 1.0 / v if v != 0 else np.nan
        else:
            v, r2, tol = np.nan, np.nan, np.nan
        vif_rows.append((col, v, tol, r2))

    vif_df = pd.DataFrame(vif_rows, columns=["Variable", "VIF", "Tolerance", "R2"])
    vif_df = vif_df.sort_values("VIF", ascending=False).reset_index(drop=True)
    vif_df[["VIF", "Tolerance", "R2"]] = vif_df[["VIF", "Tolerance", "R2"]].round(decimals)

    body = vif_df.to_latex(index=False,
                           escape=True,
                           na_rep="",
                           column_format="lrrr")
    body = body.replace("\\begin{tabular}{", "\\begin{tabular}{@{}") \
               .replace("}", " @{} }", 1)

    tex = _latex_table_wrapper(
        body,
        caption="Variance Inflation Factors (VIF) for selected predictors.",
        label="tab:vif",
        note="VIF = 1/(1-R$^2$). Tolerance = 1/VIF. VIF > 10 often indicates severe multicollinearity."
    )
    path = out_dir / "vif.tex"
    path.write_text(tex, encoding="utf-8")
    return path


def build_all_descriptives(df: pd.DataFrame,
                           out_dir: Path = "outputs/descriptives",
                           region_col: str = "region",
                           country_col: str = "iso3c",
                           spread_col: str = "sovereign_spread",
                           year_col: str = "year",
                           prefer_corr_vars: Optional[List[str]] = None,
                           vif_features: Optional[List[str]] = None) -> Dict[str, Path]:
    out_dir = _ensure_outdir(Path(out_dir))
    paths: Dict[str, Path] = {}

    paths["countries_by_region_tex"] = countries_per_region_table(
        df, out_dir, region_col=region_col, country_col=country_col
    )
    paths["summary_stats_tex"] = summary_stats_table(df, out_dir)
    paths["plot_mean_spread_png"] = plot_mean_spread_over_time(
        df, out_dir, spread_col=spread_col, year_col=year_col, start_year=1995, end_year=2024
    )
    paths["correlations_tex"] = correlation_matrix_table(
        df, out_dir, max_vars=15, prefer_vars=prefer_corr_vars
    )
    paths["vif_tex"] = vif_table(
        df, out_dir, features=vif_features
    )
    return paths
