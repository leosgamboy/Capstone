DML Project - Results package
Generated: 2025-08-22T08:42:06.847816 UTC

Files included (best-effort):
- summary_overview.csv / .json
- dml_regression_summary.txt
- p_oos_r2_folds.csv
- m_oos_r2_folds.csv
- stacked_residuals_uv_all.csv
- per_fold_artifacts.json
- perm_thetas_clean.csv
- oster_adjustments.csv
- placebo_diag_df.csv
- placebo_theta.csv
- fold_models/ (copied from fold_output_dir)
- dml_placebo_fold_diagnostics.csv
- analysis_panel_snapshot.csv
- env_versions.json

Notes:
- summary_overview contains key scalars to inspect quickly.
- dml_regression_summary contains the statsmodels OLS on residuals (clustered SEs).
- stacked_residuals_uv_all.csv contains the u and v residuals used in the final orthogonal regression.
- fold_models/ holds per-fold pickled nuisances (if they were saved during modeling).
- analysis_panel_snapshot.csv is a CSV snapshot of the data used; remove if too large or sensitive.