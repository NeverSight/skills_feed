---
name: data-analysis
description: Analyze datasets using Python with pandas, numpy, and visualization libraries. Generates statistical summaries, identifies patterns, creates charts, and provides insights. Use when analyzing CSV/Excel files, exploring data, creating visualizations, or when users mention data analysis, statistics, charts, or datasets.
license: MIT
metadata:
  author: agent-skills-demo
  version: "1.0"
  category: data-science
compatibility: Requires Python 3.8+ with pandas, numpy, matplotlib, and seaborn
---

# Data Analysis Skill

## When to Use This Skill

Use this skill when:
- Analyzing datasets (CSV, Excel, JSON)
- Performing statistical analysis
- Creating data visualizations
- Identifying trends and patterns
- Data cleaning and preprocessing
- Users mention "analyze data", "statistics", "charts", "trends", or "insights"

## Analysis Process

### 1. Data Loading & Initial Exploration

**Load the data:**
```python
import pandas as pd
import numpy as np

# CSV files
df = pd.read_csv('data.csv')

# Excel files
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# JSON files
df = pd.read_json('data.json')

# From database
import sqlalchemy
engine = sqlalchemy.create_engine('postgresql://user:pass@localhost/db')
df = pd.read_sql('SELECT * FROM table', engine)
```

**Initial exploration:**
```python
# Basic information
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMemory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# First look at data
print("\nFirst 5 rows:")
print(df.head())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Basic statistics
print("\nDescriptive statistics:")
print(df.describe())
```

### 2. Data Cleaning

**Handle missing values:**
```python
# Check missing data patterns
missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
print("Missing data percentage:")
print(missing_pct[missing_pct > 0])

# Drop columns with too many missing values
df = df.drop(columns=missing_pct[missing_pct > 50].index)

# Fill missing values
df['numeric_column'].fillna(df['numeric_column'].median(), inplace=True)
df['categorical_column'].fillna(df['categorical_column'].mode()[0], inplace=True)

# Or drop rows with missing values
df = df.dropna()
```

**Handle duplicates:**
```python
# Check for duplicates
print(f"Duplicate rows: {df.duplicated().sum()}")

# Remove duplicates
df = df.drop_duplicates()

# Keep specific duplicates
df = df.drop_duplicates(subset=['id'], keep='first')
```

**Data type conversions:**
```python
# Convert to datetime
df['date'] = pd.to_datetime(df['date'])

# Convert to numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Convert to category (saves memory)
df['category'] = df['category'].astype('category')
```

### 3. Statistical Analysis

See [references/STATISTICS.md](references/STATISTICS.md) for detailed formulas.

**Descriptive statistics:**
```python
# Central tendency
mean = df['column'].mean()
median = df['column'].median()
mode = df['column'].mode()[0]

# Dispersion
std = df['column'].std()
variance = df['column'].var()
range_val = df['column'].max() - df['column'].min()
iqr = df['column'].quantile(0.75) - df['column'].quantile(0.25)

# Distribution
skewness = df['column'].skew()
kurtosis = df['column'].kurtosis()

print(f"""
Statistics for {column}:
  Mean: {mean:.2f}
  Median: {median:.2f}
  Std Dev: {std:.2f}
  Range: {range_val:.2f}
  IQR: {iqr:.2f}
  Skewness: {skewness:.2f}
""")
```

**Correlation analysis:**
```python
# Correlation matrix
correlation = df[numeric_columns].corr()
print(correlation)

# Find strong correlations
strong_corr = correlation[(correlation > 0.7) | (correlation < -0.7)]
strong_corr = strong_corr[strong_corr != 1.0].stack()
print("\nStrong correlations:")
print(strong_corr)
```

**Group analysis:**
```python
# Group by categorical variable
grouped = df.groupby('category').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': ['sum', 'mean'],
    'quantity': 'sum'
})
print(grouped)

# Multiple grouping
df.groupby(['region', 'category'])['sales'].sum().unstack()
```

### 4. Data Visualization

**Distribution plots:**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# Histogram
plt.figure()
df['column'].hist(bins=30, edgecolor='black')
plt.title('Distribution of Column')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.savefig('histogram.png', dpi=300, bbox_inches='tight')
plt.close()

# Box plot
plt.figure()
df.boxplot(column='value', by='category')
plt.title('Value by Category')
plt.suptitle('')  # Remove default title
plt.savefig('boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

# Violin plot
plt.figure()
sns.violinplot(data=df, x='category', y='value')
plt.title('Value Distribution by Category')
plt.savefig('violin.png', dpi=300, bbox_inches='tight')
plt.close()
```

**Relationship plots:**
```python
# Scatter plot
plt.figure()
plt.scatter(df['x'], df['y'], alpha=0.5)
plt.xlabel('X Variable')
plt.ylabel('Y Variable')
plt.title('X vs Y')
plt.savefig('scatter.png', dpi=300, bbox_inches='tight')
plt.close()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# Pair plot for multiple variables
sns.pairplot(df[['var1', 'var2', 'var3', 'category']], hue='category')
plt.savefig('pairplot.png', dpi=300, bbox_inches='tight')
plt.close()
```

**Time series plots:**
```python
# Line plot
plt.figure()
df.set_index('date')['value'].plot()
plt.title('Value Over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.savefig('timeseries.png', dpi=300, bbox_inches='tight')
plt.close()

# Multiple time series
df.pivot(index='date', columns='category', values='value').plot()
plt.title('Values by Category Over Time')
plt.legend(title='Category')
plt.savefig('timeseries_multi.png', dpi=300, bbox_inches='tight')
plt.close()
```

**Categorical plots:**
```python
# Bar plot
category_counts = df['category'].value_counts()
plt.figure()
category_counts.plot(kind='bar')
plt.title('Count by Category')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.savefig('barplot.png', dpi=300, bbox_inches='tight')
plt.close()

# Stacked bar plot
df.groupby(['region', 'category'])['sales'].sum().unstack().plot(kind='bar', stacked=True)
plt.title('Sales by Region and Category')
plt.savefig('stacked_bar.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 5. Advanced Analysis

**Trend detection:**
```python
from scipy import stats

# Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(df['x'], df['y'])
print(f"Trend: slope={slope:.4f}, R²={r_value**2:.4f}, p={p_value:.4f}")

# Moving average
df['ma_7'] = df['value'].rolling(window=7).mean()
df['ma_30'] = df['value'].rolling(window=30).mean()
```

**Outlier detection:**
```python
# Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(df['column']))
outliers = df[z_scores > 3]
print(f"Outliers detected: {len(outliers)}")

# IQR method
Q1 = df['column'].quantile(0.25)
Q3 = df['column'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['column'] < Q1 - 1.5*IQR) | (df['column'] > Q3 + 1.5*IQR)]
print(f"Outliers by IQR: {len(outliers)}")
```

**Statistical tests:**
```python
from scipy import stats

# T-test (compare two groups)
group1 = df[df['category'] == 'A']['value']
group2 = df[df['category'] == 'B']['value']
t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"T-test: t={t_stat:.4f}, p={p_value:.4f}")

# ANOVA (compare multiple groups)
groups = [df[df['category'] == cat]['value'] for cat in df['category'].unique()]
f_stat, p_value = stats.f_oneway(*groups)
print(f"ANOVA: F={f_stat:.4f}, p={p_value:.4f}")

# Chi-square test (categorical variables)
contingency_table = pd.crosstab(df['category1'], df['category2'])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
print(f"Chi-square: χ²={chi2:.4f}, p={p_value:.4f}")
```

### 6. Generate Report

**Use the analysis script:**
```bash
python scripts/analyze.py --file data.csv --output report.html
```

**Create summary:**
```python
summary = f"""
# Data Analysis Report

## Dataset Overview
- Rows: {len(df):,}
- Columns: {len(df.columns)}
- Date range: {df['date'].min()} to {df['date'].max()}

## Key Findings

### 1. [Finding Title]
{description_of_finding}

### 2. [Finding Title]
{description_of_finding}

## Statistical Summary
{df.describe().to_markdown()}

## Recommendations
1. [Recommendation based on analysis]
2. [Recommendation based on analysis]
"""

with open('analysis_report.md', 'w') as f:
    f.write(summary)
```

## Best Practices

### Memory Optimization
```python
# Read large files in chunks
chunk_size = 10000
chunks = []
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    processed_chunk = chunk.process()  # Your processing
    chunks.append(processed_chunk)
df = pd.concat(chunks)

# Optimize data types
df['int_col'] = df['int_col'].astype('int32')  # Instead of int64
df['float_col'] = df['float_col'].astype('float32')  # Instead of float64
```

### Performance Tips
```python
# Use vectorized operations instead of loops
# Bad
result = []
for value in df['column']:
    result.append(value * 2)

# Good
result = df['column'] * 2

# Use .query() for filtering
df_filtered = df.query('age > 30 and city == "NYC"')

# Use .loc for setting values
df.loc[df['age'] > 30, 'category'] = 'senior'
```

### Reproducibility
```python
# Set random seed
np.random.seed(42)

# Save processed data
df.to_csv('processed_data.csv', index=False)
df.to_parquet('processed_data.parquet')  # Better for large datasets

# Export analysis
import pickle
with open('analysis_results.pkl', 'wb') as f:
    pickle.dump({'stats': stats, 'model': model}, f)
```

## Common Analysis Types

### Sales Analysis
```python
# Total sales by period
sales_by_month = df.groupby(df['date'].dt.to_period('M'))['sales'].sum()

# Top products
top_products = df.groupby('product')['sales'].sum().sort_values(ascending=False).head(10)

# Growth rate
df['growth_rate'] = df['sales'].pct_change() * 100
```

### Customer Analysis
```python
# Customer segmentation
df['segment'] = pd.cut(df['total_purchases'], 
                       bins=[0, 100, 500, float('inf')],
                       labels=['Low', 'Medium', 'High'])

# Retention analysis
cohort = df.groupby(['cohort_month', 'purchase_month']).size()
```

### Performance Analysis
```python
# Year-over-year comparison
df['year'] = df['date'].dt.year
yoy = df.groupby('year')['metric'].sum()
yoy_growth = yoy.pct_change() * 100
```

## Error Handling

```python
try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    print("Error: File not found")
    sys.exit(1)
except pd.errors.EmptyDataError:
    print("Error: File is empty")
    sys.exit(1)
except Exception as e:
    print(f"Error loading data: {e}")
    sys.exit(1)

# Validate data
assert not df.empty, "DataFrame is empty"
assert 'required_column' in df.columns, "Missing required column"
assert df['date'].dtype == 'datetime64[ns]', "Date column not in datetime format"
```

## Output Guidelines

Always provide:
1. **Summary**: High-level findings in plain language
2. **Statistics**: Key numbers and metrics
3. **Visualizations**: Charts that support findings
4. **Insights**: Actionable conclusions
5. **Recommendations**: Next steps based on analysis
