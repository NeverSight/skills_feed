---
name: data-science-eda
description: "Exploratory Data Analysis (EDA): profiling, visualization, correlation analysis, and data quality checks. Use when understanding dataset structure, distributions, relationships, or preparing for feature engineering and modeling."
dependsOn: ["@data-engineering-core"]
---

# Exploratory Data Analysis (EDA)

Use this skill for understanding datasets before modeling: profiling distributions, detecting anomalies, identifying relationships, and assessing data quality.

## When to use this skill

- New dataset — need orientation on structure, types, distributions
- Before feature engineering — understand variable relationships
- Data quality investigation — find anomalies, missing patterns, outliers
- Model preparation — validate assumptions about data

## Core EDA workflow

1. **Profile structure**
   - Schema, types, cardinality
   - Missing value patterns
2. **Analyze distributions**
   - Numerical: histograms, boxplots, skewness
   - Categorical: frequencies, rare categories
3. **Explore relationships**
   - Correlation matrix (numerical)
   - Cross-tabulations (categorical)
   - Target-variable relationships
4. **Identify issues**
   - Outliers, duplicates, inconsistencies
   - Class imbalance (classification)
   - Temporal patterns (time series)

## Quick tool selection

| Task | Default choice | Notes |
|---|---|---|
| Automated profiling | **ydata-profiling / pandas-profiling** | Fast comprehensive reports |
| Interactive exploration | **ipywidgets + plotly** | Drill-down capability |
| Statistical tests | **scipy.stats** | Normality, correlations |
| Large datasets | **Polars + lazy** | Memory-efficient |

## Core implementation rules

### 1) Start with automated profiling

```python
import polars as pl
from ydata_profiling import ProfileReport

df = pl.read_parquet("data.parquet")
profile = ProfileReport(df.to_pandas(), title="Data Profile")
profile.to_file("profile_report.html")
```

### 2) Focus on actionable insights

- Document outliers worth investigating (not all outliers are problems)
- Flag features with high cardinality or rare categories
- Note strong correlations that may cause multicollinearity

### 3) Visualize for communication

- Distribution plots for key variables
- Correlation heatmap
- Missing value patterns
- Target relationship plots

### 4) Validate assumptions

- Check for expected ranges/business rules
- Verify temporal consistency
- Confirm key relationships match domain knowledge

## Common anti-patterns

- ❌ Skipping EDA and jumping to modeling
- ❌ Treating all outliers as errors
- ❌ Ignoring missing value mechanisms (MCAR/MAR/MNAR)
- ❌ Over-plotting large datasets without sampling
- ❌ Not documenting findings for team

## Progressive disclosure

- `../references/automated-profiling.md` — ydata-profiling, Sweetviz, D-Tale
- `../references/visualization-patterns.md` — Matplotlib, Seaborn, Plotly patterns
- `../references/statistical-tests.md` — Scipy statistical tests guide
- `../references/large-dataset-eda.md` — Sampling, Polars, Dask approaches

## Related skills

- `@data-science-feature-engineering` — Next step after EDA
- `@data-science-model-evaluation` — Validate modeling assumptions
- `@data-engineering-quality` — Data validation frameworks

## References

- [ydata-profiling Documentation](https://docs.profiling.ydata.ai/)
- [Pandas Visualization](https://pandas.pydata.org/docs/user_guide/visualization.html)
- [Seaborn Statistical Visualization](https://seaborn.pydata.org/)
- [SciPy Statistics](https://docs.scipy.org/doc/scipy/reference/stats.html)
