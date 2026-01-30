---
name: q_descriptive-analysis
description: "Comprehensive descriptive analysis of tabular datasets with grouped statistics, entity extraction, and publication-ready summaries. Use when analyzing Excel/CSV datasets requiring: (1) Overall and grouped descriptive statistics, (2) Frequency distributions by categorical variables, (3) Entity extraction from text fields, (4) Temporal dynamics analysis, (5) CSV output tables with MD summary reports. Supports SDT scores, engagement metrics, or any continuous/categorical variables."
---

# Descriptive Analysis Skill

Generate comprehensive exploratory descriptive analysis of tabular datasets with grouped statistics, frequency tables, entity extraction, and publication-ready markdown summaries.

## Workflow

### 1. Requirements Gathering (Interview)

Before analysis, ask the user 5-10 questions covering:

1. **Research objective** - Exploratory vs. confirmatory analysis
2. **Grouping variables** - Categorical variables to stratify by
3. **Continuous variables** - Metrics to calculate descriptives for
4. **Text fields requiring extraction** - Columns with embedded entities
5. **Temporal variable** - Date/time column and desired granularity
6. **Classification schemes** - Any custom tier/category definitions
7. **Output preferences** - CSV tables, MD summary, visualizations

### 2. Data Preparation

Create derived variables as needed:

```python
# Tier classification (customize thresholds)
def classify_tier(value, tiers):
    for tier_name, (min_val, max_val) in tiers.items():
        if min_val <= value <= max_val:
            return tier_name
    return 'Other'

# Example tier structure
TIERS = {
    'Small': (0, 1000),
    'Medium': (1001, 10000),
    'Large': (10001, float('inf'))
}

# Temporal grouping
df['month'] = df['date_col'].dt.to_period('M').astype(str)
```

### 3. Analysis Structure

Generate tables in this order:

| # | File Pattern | Contents |
|---|--------------|----------|
| 01 | sample_overview.csv | N, date range, unique counts |
| 02-07 | {groupvar}_distribution.csv | Frequency for each grouping variable |
| 08 | continuous_overall.csv | Mean, SD, Median, Min, Max |
| 08a-f | continuous_by_{groupvar}.csv | Descriptives stratified by group |
| 09-10 | categorical_distribution.csv | Key categorical variables |
| 11-15 | entity_{fieldname}.csv | Extracted entity frequencies |
| 16 | temporal_trends.csv | Metrics over time |

### 4. Descriptive Statistics Function

```python
def descriptive_stats(series, name='Variable'):
    return {
        'Variable': name,
        'N': series.count(),
        'Mean': series.mean(),
        'SD': series.std(),
        'Min': series.min(),
        'Q1': series.quantile(0.25),
        'Median': series.median(),
        'Q3': series.quantile(0.75),
        'Max': series.max()
    }

def grouped_descriptives(df, var, group_var, group_col_name):
    results = []
    for group in df[group_var].dropna().unique():
        group_data = df[df[group_var] == group][var].dropna()
        if len(group_data) > 0:
            stats = descriptive_stats(group_data, var)
            stats[group_col_name] = group
            results.append(stats)
    return pd.DataFrame(results)
```

### 5. Entity Extraction

For text fields with embedded entities (timestamps, names, etc.):

```python
import re

def extract_entities(text):
    """Extract entities from bracketed text like '[00:01:23] entity_name'"""
    if pd.isna(text) or text == '':
        return []
    entities = []
    pattern = r'\[[\d:]+\]\s*([^;\[\]]+)'
    matches = re.findall(pattern, str(text))
    for match in matches:
        entity = match.strip().lower()
        if entity and len(entity) > 1:
            entities.append(entity)
    return entities

def entity_frequency(df, col):
    all_entities = []
    for text in df[col].dropna():
        all_entities.extend(extract_entities(text))
    return pd.Series(all_entities).value_counts()
```

### 6. Output Directory Structure

```
TABLE/
├── 01_sample_overview.csv
├── 02_groupvar1_distribution.csv
├── ...
├── 08_continuous_overall.csv
├── 08a_continuous_by_groupvar1.csv
├── ...
├── DESCRIPTIVE_SUMMARY.md
```

### 7. MD Summary Generator

Create comprehensive markdown summary including:

1. **Sample Overview** - Dataset dimensions and date range
2. **Distribution Tables** - Top values for each grouping variable
3. **Continuous Descriptives** - Overall + by each grouping variable
4. **Entity Summaries** - Unique counts and top entities
5. **Temporal Trends** - Key metrics over time
6. **Output Files Reference** - Links to all CSV tables

Summary should use markdown tables with proper formatting:

```markdown
| Variable | N | Mean | SD | Median |
|----------|---|------|-------|--------|
| views | 380 | 27192.59 | 133894.14 | 657.00 |
```

### 8. Key Design Principles

1. **Descriptive only** - No inferential statistics unless requested
2. **Flexible grouping** - Support any number of grouping variables
3. **Top-N limits** - Show top 5-10 for large category sets
4. **Clean entity extraction** - Normalize case, deduplicate
5. **Dual output** - CSV for validation, MD for interpretation
6. **Video/channel counts** - When applicable, report both unit types
7. **Milestone annotations** - Add context to temporal distributions

### 9. Verification Checklist

- [ ] All CSV files generated with > 0 rows
- [ ] No empty/null columns
- [ ] Sum of frequencies matches total N
- [ ] Grouped descriptives align with overall
- [ ] Entity extraction capturing expected patterns
- [ ] MD summary coherent and complete
