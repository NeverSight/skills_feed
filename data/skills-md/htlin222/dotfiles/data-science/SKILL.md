---
name: data-science
description: Data analysis, SQL queries, BigQuery operations, and data insights. Use for data analysis tasks and queries.
---

# Data Science

Data analysis, SQL, and insights generation.

## When to Use

- Writing SQL queries
- Data analysis and exploration
- Creating visualizations
- Statistical analysis
- ETL and data pipelines

## SQL Patterns

### Common Queries

```sql
-- Aggregation with window functions
SELECT
    user_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY order_date) as running_total,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date DESC) as recency_rank
FROM orders;

-- CTEs for readability
WITH monthly_stats AS (
    SELECT
        DATE_TRUNC('month', created_at) as month,
        COUNT(*) as total_orders,
        SUM(amount) as revenue
    FROM orders
    GROUP BY 1
),
growth AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) as prev_revenue,
        (revenue - LAG(revenue) OVER (ORDER BY month)) / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) as growth_rate
    FROM monthly_stats
)
SELECT * FROM growth;
```

### BigQuery Specifics

```sql
-- Partitioned table query
SELECT *
FROM `project.dataset.events`
WHERE DATE(_PARTITIONTIME) BETWEEN '2024-01-01' AND '2024-01-31';

-- UNNEST for arrays
SELECT
    user_id,
    item
FROM `project.dataset.orders`,
UNNEST(items) as item;

-- Approximate counts for large data
SELECT APPROX_COUNT_DISTINCT(user_id) as unique_users
FROM `project.dataset.events`;
```

## Python Analysis

```python
import pandas as pd
import numpy as np

# Load and explore
df = pd.read_csv('data.csv')
df.info()
df.describe()

# Clean and transform
df['date'] = pd.to_datetime(df['date'])
df = df.dropna(subset=['required_field'])
df['category'] = df['category'].fillna('Unknown')

# Aggregate
summary = df.groupby('category').agg({
    'value': ['mean', 'sum', 'count'],
    'date': ['min', 'max']
}).round(2)

# Visualize
import matplotlib.pyplot as plt
df.groupby('date')['value'].sum().plot(figsize=(12, 6))
plt.title('Daily Values')
plt.savefig('chart.png', dpi=150, bbox_inches='tight')
```

## Statistical Analysis

```python
from scipy import stats

# Hypothesis testing
t_stat, p_value = stats.ttest_ind(group_a, group_b)

# Correlation
correlation = df['x'].corr(df['y'])

# Regression
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X, y)
print(f"R² = {model.score(X, y):.3f}")
```

## Output Format

```markdown
## Analysis Summary

**Question:** [What we're trying to answer]
**Data Source:** [Tables/files used]
**Date Range:** [Time period]

### Key Findings

1. [Finding with supporting metric]
2. [Finding with supporting metric]

### Visualization

[Chart description or embedded image]

### Recommendations

- [Actionable insight]
```

## Examples

**Input:** "Analyze user retention"
**Action:** Query cohort data, calculate retention rates, visualize trends

**Input:** "Find top customers"
**Action:** Write SQL for RFM analysis, segment users, summarize findings
