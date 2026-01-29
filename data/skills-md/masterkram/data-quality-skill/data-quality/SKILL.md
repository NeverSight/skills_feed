---
name: data-quality
description: Diagnose and fix data quality problems in datasets. Use when working with dirty data, finding duplicates, handling missing values, detecting outliers/anomalies, validating constraints (functional dependencies, referential integrity), profiling datasets, or cleaning data for analysis or ML. Covers the full data quality lifecycle - define, detect, clean, measure.
---

# Data Quality Skill

Systematic approach to diagnosing and fixing data quality problems.

## Data Quality Process

```
Define & Identify → Detect & Quantify → Clean & Rectify → Measure & Verify
```

1. **Define:** Understand data context, business rules, quality requirements
2. **Detect:** Profile data, find glitches (missing, duplicates, outliers, violations)
3. **Clean:** Apply appropriate repair strategies
4. **Measure:** Validate repairs, quantify improvement

## Quick Reference

| Problem | Script | Key Function |
|---------|--------|--------------|
| Data overview | `data_profiling.py` | `profile_dataframe(df)` |
| Find quality issues | `data_profiling.py` | `detect_glitches(df)` |
| Missing values | `missing_data.py` | `analyze_missing(df)` |
| Imputation | `missing_data.py` | `impute_mean/median/regression()` |
| Duplicates | `duplicate_detection.py` | `find_duplicates(df, cols)` |
| Deduplication | `duplicate_detection.py` | `deduplicate(df, cols)` |
| Outliers | `anomaly_detection.py` | `detect_anomalies(df)` |
| Constraint check | `constraint_checking.py` | `validate_constraints(df, rules)` |
| String matching | `similarity_metrics.py` | `jaro_winkler_similarity()` |

## Workflow

### Step 1: Profile the Data

```python
from scripts.data_profiling import profile_dataframe, detect_glitches, generate_quality_report

# Quick overview
print(generate_quality_report(df))

# Detailed profile
profile = profile_dataframe(df)

# Find issues
glitches = detect_glitches(df)
```

### Step 2: Analyze Specific Issues

**Missing Data:**
```python
from scripts.missing_data import analyze_missing, test_mcar

analysis = analyze_missing(df)
# Check if safe to delete rows
mcar_test = test_mcar(df, 'column_with_missing', ['other_cols'])
```

**Duplicates:**
```python
from scripts.duplicate_detection import find_duplicates, cluster_duplicates

matches = find_duplicates(df, ['name', 'email'], threshold=0.85)
clusters = cluster_duplicates(matches)
```

**Outliers:**
```python
from scripts.anomaly_detection import detect_anomalies, iqr_outliers

# Multi-column summary
anomalies = detect_anomalies(df, method='iqr')

# Single column detail
result = iqr_outliers(df, 'price', multiplier=1.5)
```

**Constraints:**
```python
from scripts.constraint_checking import validate_constraints

constraints = [
    {'type': 'unique', 'columns': ['id']},
    {'type': 'not_null', 'columns': ['name', 'email']},
    {'type': 'fd', 'determinant': ['id'], 'dependent': ['name']},
    {'type': 'domain', 'column': 'age', 'min_value': 0, 'max_value': 150},
]
results = validate_constraints(df, constraints)
```

### Step 3: Clean the Data

**Handle Missing:**
```python
from scripts.missing_data import impute_median, impute_regression, listwise_deletion

# Simple: median for numeric
df_clean = impute_median(df, 'age')

# Better: regression-based
df_clean = impute_regression(df, 'income', ['age', 'education'])

# If MCAR confirmed
df_clean = listwise_deletion(df)
```

**Remove Duplicates:**
```python
from scripts.duplicate_detection import deduplicate

df_clean, summary = deduplicate(
    df, 
    columns=['name', 'email', 'address'],
    threshold=0.8,
    merge_strategy='most_complete'
)
print(f"Reduced from {summary['original_rows']} to {summary['final_rows']} rows")
```

**Handle Outliers:**
```python
# Cap extreme values
q01, q99 = df['col'].quantile([0.01, 0.99])
df['col'] = df['col'].clip(q01, q99)

# Or remove
df_clean = df[~detect_anomalies(df)['col']['outlier_indices']]
```

### Step 4: Validate

Re-run profiling and constraint checks on cleaned data to verify improvements.

## References

For deeper understanding:
- **[references/dimensions.md](references/dimensions.md):** Data quality dimensions (accuracy, completeness, etc.)
- **[references/glitch_taxonomy.md](references/glitch_taxonomy.md):** Types of data glitches and detection approaches
- **[references/repair_strategies.md](references/repair_strategies.md):** Detailed repair and cleaning strategies

## Key Concepts

**Data Quality = Fit for Use**
- Free of defects
- Has features needed for the task
- Right information, right place, right time

**Missing Data Mechanisms:**
- MCAR: Missing Completely At Random (safe to delete)
- MAR: Missing At Random (imputation may work)
- MNAR: Missing Not At Random (most problematic)

**Constraints:**
- Functional Dependency: `X → Y` means X uniquely determines Y
- Referential Integrity: foreign keys reference valid primary keys
- Domain Constraints: values within allowed set/range

**Entity Resolution:**
- Blocking reduces O(n²) to O(n·window)
- Similarity metrics: Jaro-Winkler (names), Levenshtein (typos), Jaccard (sets)
- Cluster by transitive closure, merge by strategy

## Similarity Metrics Comparison

| Metric | Best For | Example |
|--------|----------|---------|
| Jaro-Winkler | Names, short strings | "Robert" vs "Rupert" |
| Levenshtein | Typos, edit distance | "recieve" vs "receive" |
| Jaccard | Token/word comparison | "John Doe" vs "Doe, John" |
| Q-gram | Fuzzy substring matching | Partial matches |
