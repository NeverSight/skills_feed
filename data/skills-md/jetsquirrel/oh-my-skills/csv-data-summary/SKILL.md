---
name: csv-data-summary
description: Analyzes CSV files, generates comprehensive summary statistics, identifies data patterns, and creates visualizations using Python and pandas. Automatically adapts analysis based on data type (sales, customer, financial, survey, operational).
---

# CSV Data Summary Skill

This skill helps you analyze CSV files and generate comprehensive summaries with statistical insights and visualizations. It automatically detects the type of data you're working with and adapts the analysis accordingly.

## Use Cases

- Quick data exploration and understanding
- Identifying data quality issues (missing values, outliers)
- Discovering patterns and correlations in datasets
- Creating visual summaries for reports and presentations
- Time-series analysis when date columns are present
- Categorical data distribution analysis

## Prerequisites

You'll need Python with the following libraries:

```bash
pip install pandas>=2.0.0 matplotlib>=3.7.0 seaborn>=0.12.0
```

## When to Use This Skill

Use this skill whenever you need to:
- Understand the structure and content of a CSV file
- Get summary statistics for numeric columns
- Identify missing data and data quality issues
- Visualize distributions and correlations
- Analyze time-series trends
- Get a comprehensive overview of categorical variables

## How It Works

The skill automatically:

1. **Loads and inspects** the CSV file
2. **Identifies data structure** - column types, date columns, numeric columns, categories
3. **Adapts analysis** based on data type:
   - **Sales/E-commerce data**: Time-series trends, revenue analysis, product performance
   - **Customer data**: Distribution analysis, segmentation, geographic patterns
   - **Financial data**: Trend analysis, statistical summaries, correlations
   - **Operational data**: Time-series, performance metrics, distributions
   - **Survey data**: Frequency analysis, cross-tabulations, distributions
4. **Generates visualizations** relevant to the specific dataset:
   - Time-series plots (if date/timestamp columns exist)
   - Correlation heatmaps (if multiple numeric columns exist)
   - Category distributions (if categorical columns exist)
   - Histograms for numeric distributions
5. **Provides comprehensive output** including:
   - Data overview (rows, columns, types)
   - Key statistics and metrics
   - Missing data analysis
   - Multiple relevant visualizations
   - Actionable insights

## Python Implementation

### Basic Usage

```python
from analyze import summarize_csv

# Analyze any CSV file
summary = summarize_csv('your_data.csv')
print(summary)
```

The script will automatically generate:
- A comprehensive text summary
- Multiple visualization files (PNG format)

### Example Output

```
============================================================
📊 DATA OVERVIEW
============================================================
Rows: 5,000 | Columns: 8

📋 DATA TYPES:
  • order_date: object
  • total_revenue: float64
  • customer_segment: object
  ...

🔍 DATA QUALITY:
✓ No missing values - dataset is complete!

📈 NUMERICAL ANALYSIS:
[Summary statistics for all numeric columns]

🔗 CORRELATIONS:
[Correlation matrix showing relationships]

📅 TIME SERIES ANALYSIS:
Date range: 2024-01-05 to 2024-04-11
Span: 97 days

📊 VISUALIZATIONS CREATED:
  ✓ correlation_heatmap.png
  ✓ time_series_analysis.png
  ✓ distributions.png
  ✓ categorical_distributions.png
```

## Command Line Usage

You can run the analysis from the command line:

```bash
# Analyze a specific CSV file
python scripts/analyze.py path/to/your/data.csv

# Use the sample data
python scripts/analyze.py resources/sample.csv
```

## Understanding the Output

### Data Overview
- Shows the dimensions of your dataset (rows × columns)
- Lists all column names
- Shows data type for each column

### Data Quality
- Reports missing values by column
- Shows percentage of missing data
- Helps identify data cleaning needs

### Numerical Analysis
- Provides descriptive statistics (mean, std, min, max, quartiles)
- Shows correlations between numeric columns
- Creates correlation heatmap visualization

### Categorical Analysis
- Shows frequency distribution for each categorical variable
- Displays top 10 values per category
- Creates bar charts for categorical distributions

### Time Series Analysis
- Automatically detected when date/time columns are present
- Shows date range and span
- Creates trend plots for numeric metrics over time
- Calculates daily/periodic aggregations

## Visualizations Generated

The skill automatically creates relevant visualizations:

1. **Correlation Heatmap** (`correlation_heatmap.png`)
   - Shows relationships between numeric variables
   - Color-coded for easy interpretation
   - Only generated when 2+ numeric columns exist

2. **Time Series Analysis** (`time_series_analysis.png`)
   - Trend lines for numeric metrics over time
   - Only generated when date/time columns exist
   - Shows up to 3 key metrics

3. **Distributions** (`distributions.png`)
   - Histograms for numeric columns
   - Shows up to 4 numeric variables
   - Helps identify outliers and data shape

4. **Categorical Distributions** (`categorical_distributions.png`)
   - Bar charts for categorical variables
   - Shows top 10 values per category
   - Up to 4 categorical variables

## Tips and Best Practices

1. **Clean column names**: Use lowercase and underscores for better readability
2. **Date formats**: Ensure date columns contain 'date' or 'time' in the name
3. **Numeric data**: Ensure numeric columns are properly typed (not strings)
4. **Large files**: The skill handles large files efficiently with pandas
5. **Missing data**: Review the data quality section carefully before analysis

## Troubleshooting

**Issue: Date columns not detected**
- Ensure column names contain 'date' or 'time'
- Check date format is recognizable (YYYY-MM-DD, MM/DD/YYYY, etc.)

**Issue: Numeric columns treated as text**
- Check for non-numeric characters in the data
- Clean data or use pandas type conversion

**Issue: Too many visualizations**
- The script automatically limits visualizations to the most relevant ones
- Focus on the first few metrics of each type

**Issue: Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ recommended)

## Advanced Usage

### Customizing the Analysis

You can modify `analyze.py` to:
- Add custom metrics specific to your domain
- Change visualization styles and colors
- Adjust the number of categories shown
- Add domain-specific insights

### Integration with Other Tools

The script outputs:
- Plain text summary (easy to parse)
- PNG images (ready for reports)
- Can be extended to output JSON, HTML, or PDF reports

## Additional Resources

- [pandas documentation](https://pandas.pydata.org/docs/)
- [matplotlib gallery](https://matplotlib.org/stable/gallery/index.html)
- [seaborn tutorial](https://seaborn.pydata.org/tutorial.html)
- [CSV data best practices](https://www.w3.org/TR/tabular-data-primer/)

## Differences from Excel Sheet Reference Skill

This skill focuses on:
- **Data analysis and visualization** (not Excel formula creation)
- **CSV file format** (not Excel workbooks)
- **Statistical insights** (not cross-sheet references)
- **Python pandas** (not openpyxl)

Use the `excel-sheet-reference` skill when you need to:
- Create Excel files with multiple sheets
- Use cross-sheet formulas (VLOOKUP, COUNTIFS, etc.)
- Maintain data in Excel format with formulas
