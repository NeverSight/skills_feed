---
name: duckdb
description: Fast in-process analytical database for SQL queries on DataFrames, CSV, Parquet, JSON files, and more. Use when user wants to perform SQL analytics on data files or Python DataFrames (pandas, Polars), run complex aggregations, joins, or window functions, or query external data sources without loading into memory. Best for analytical workloads, OLAP queries, and data exploration.
---

# DuckDB

## Overview

DuckDB is a high-performance, in-process analytical database management system (often called "SQLite for analytics"). Execute complex SQL queries directly on CSV, Parquet, JSON files, and Python DataFrames (pandas, Polars) without importing data or running a separate database server.

## When to Use This Skill

Activate when the user:
- Wants to run SQL queries on data files (CSV, Parquet, JSON)
- Needs to perform complex analytical queries (aggregations, joins, window functions)
- Asks to query pandas or Polars DataFrames using SQL
- Wants to explore or analyze data without loading it into memory
- Needs fast analytical performance on medium to large datasets
- Mentions DuckDB explicitly or wants OLAP-style analytics

## Installation

Check if DuckDB is installed:

```bash
python3 -c "import duckdb; print(duckdb.__version__)"
```

If not installed:

```bash
pip3 install duckdb
```

For Polars integration:

```bash
pip3 install duckdb 'polars[pyarrow]'
```

## Core Capabilities

### 1. Querying Data Files Directly

DuckDB can query files without loading them into memory:

```python
import duckdb

# Query CSV file
result = duckdb.sql("SELECT * FROM 'data.csv' WHERE age > 25")
print(result.df())  # Convert to pandas DataFrame

# Query Parquet file
result = duckdb.sql("""
    SELECT category, SUM(amount) as total
    FROM 'sales.parquet'
    GROUP BY category
    ORDER BY total DESC
""")

# Query JSON file
result = duckdb.sql("SELECT * FROM 'users.json' LIMIT 10")

# Query multiple files with wildcards
result = duckdb.sql("SELECT * FROM 'data/*.parquet'")
```

### 2. Working with Pandas DataFrames

DuckDB can directly query pandas DataFrames:

```python
import duckdb
import pandas as pd

# Create or load a DataFrame
df = pd.read_csv('data.csv')

# Query the DataFrame using SQL
result = duckdb.sql("""
    SELECT
        category,
        AVG(price) as avg_price,
        COUNT(*) as count
    FROM df
    WHERE price > 100
    GROUP BY category
    HAVING count > 5
""")

# Convert result to pandas DataFrame
result_df = result.df()
print(result_df)
```

### 3. Working with Polars DataFrames

DuckDB integrates seamlessly with Polars using Apache Arrow:

```python
import duckdb
import polars as pl

# Create or load a Polars DataFrame
df = pl.read_csv('data.csv')

# Query Polars DataFrame with DuckDB
result = duckdb.sql("""
    SELECT
        date_trunc('month', date) as month,
        SUM(revenue) as monthly_revenue
    FROM df
    GROUP BY month
    ORDER BY month
""")

# Convert result to Polars DataFrame
result_df = result.pl()

# For lazy evaluation, use lazy=True
lazy_result = result.pl(lazy=True)
```

### 4. Creating Persistent Databases

Create database files for persistent storage:

```python
import duckdb

# Connect to a persistent database (creates file if doesn't exist)
con = duckdb.connect('my_database.duckdb')

# Create table and insert data
con.execute("""
    CREATE TABLE users AS
    SELECT * FROM 'users.csv'
""")

# Query the database
result = con.execute("SELECT * FROM users WHERE age > 30").fetchdf()

# Close connection
con.close()
```

### 5. Complex Analytical Queries

DuckDB excels at analytical queries:

```python
import duckdb

# Window functions
result = duckdb.sql("""
    SELECT
        name,
        department,
        salary,
        AVG(salary) OVER (PARTITION BY department) as dept_avg,
        RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
    FROM 'employees.csv'
""")

# CTEs and subqueries
result = duckdb.sql("""
    WITH monthly_sales AS (
        SELECT
            date_trunc('month', sale_date) as month,
            product_id,
            SUM(amount) as total_sales
        FROM 'sales.parquet'
        GROUP BY month, product_id
    )
    SELECT
        m.month,
        p.product_name,
        m.total_sales,
        LAG(m.total_sales) OVER (
            PARTITION BY m.product_id
            ORDER BY m.month
        ) as prev_month_sales
    FROM monthly_sales m
    JOIN 'products.csv' p ON m.product_id = p.id
    ORDER BY m.month DESC, m.total_sales DESC
""")
```

### 6. Joins Across Different Data Sources

Join data from multiple files and DataFrames:

```python
import duckdb
import pandas as pd

# Load DataFrame
customers_df = pd.read_csv('customers.csv')

# Join DataFrame with Parquet file
result = duckdb.sql("""
    SELECT
        c.customer_name,
        c.email,
        o.order_date,
        o.total_amount
    FROM customers_df c
    JOIN 'orders.parquet' o ON c.customer_id = o.customer_id
    WHERE o.order_date >= '2024-01-01'
    ORDER BY o.order_date DESC
""")
```

## Common Patterns

### Pattern 1: Quick Data Exploration

```python
import duckdb

# Get table schema
duckdb.sql("DESCRIBE SELECT * FROM 'data.parquet'").show()

# Quick statistics
duckdb.sql("""
    SELECT
        COUNT(*) as rows,
        COUNT(DISTINCT user_id) as unique_users,
        MIN(created_at) as earliest_date,
        MAX(created_at) as latest_date
    FROM 'data.csv'
""").show()

# Sample data
duckdb.sql("SELECT * FROM 'large_file.parquet' USING SAMPLE 1000").show()
```

### Pattern 2: Data Transformation Pipeline

```python
import duckdb

# ETL pipeline using DuckDB
con = duckdb.connect('analytics.duckdb')

# Extract and transform
con.execute("""
    CREATE TABLE clean_sales AS
    SELECT
        date_trunc('day', timestamp) as sale_date,
        UPPER(TRIM(product_name)) as product_name,
        quantity,
        price,
        quantity * price as total_amount,
        CASE
            WHEN quantity > 10 THEN 'bulk'
            ELSE 'retail'
        END as sale_type
    FROM 'raw_sales.csv'
    WHERE price > 0 AND quantity > 0
""")

# Create aggregated view
con.execute("""
    CREATE VIEW daily_summary AS
    SELECT
        sale_date,
        sale_type,
        COUNT(*) as num_sales,
        SUM(total_amount) as revenue
    FROM clean_sales
    GROUP BY sale_date, sale_type
""")

result = con.execute("SELECT * FROM daily_summary ORDER BY sale_date DESC").fetchdf()
con.close()
```

### Pattern 3: Combining DuckDB + Polars for Optimal Performance

```python
import duckdb
import polars as pl

# Read multiple parquet files with Polars
df = pl.read_parquet('data/*.parquet')

# Use DuckDB for complex SQL analytics
result = duckdb.sql("""
    SELECT
        customer_segment,
        product_category,
        COUNT(DISTINCT customer_id) as customers,
        SUM(revenue) as total_revenue,
        AVG(revenue) as avg_revenue,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY revenue) as median_revenue
    FROM df
    WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY customer_segment, product_category
    HAVING total_revenue > 10000
    ORDER BY total_revenue DESC
""").pl()  # Return as Polars DataFrame

# Continue processing with Polars
final_result = result.with_columns([
    (pl.col('total_revenue') / pl.col('customers')).alias('revenue_per_customer')
])
```

### Pattern 4: Export Query Results

```python
import duckdb

# Export to CSV
duckdb.sql("""
    COPY (
        SELECT * FROM 'input.parquet' WHERE status = 'active'
    ) TO 'output.csv' (HEADER, DELIMITER ',')
""")

# Export to Parquet
duckdb.sql("""
    COPY (
        SELECT date, category, SUM(amount) as total
        FROM 'sales.csv'
        GROUP BY date, category
    ) TO 'summary.parquet' (FORMAT PARQUET)
""")

# Export to JSON
duckdb.sql("""
    COPY (SELECT * FROM users WHERE age > 21)
    TO 'filtered_users.json' (FORMAT JSON)
""")
```

## Performance Tips

1. **Use Parquet for large datasets**: Parquet is columnar and compressed, ideal for analytical queries
2. **Filter early**: Push filters down to file reads when possible
3. **Partition large files**: Use DuckDB's automatic partitioning for large datasets
4. **Use projections**: Only select columns you need
5. **Leverage indexes**: For persistent databases, create indexes on frequently queried columns

```python
# Good: Filter and project early
duckdb.sql("SELECT name, age FROM 'users.parquet' WHERE age > 25")

# Less efficient: Select all then filter
duckdb.sql("SELECT * FROM 'users.parquet'").df()[lambda x: x['age'] > 25]
```

## Integration with Polars

DuckDB and Polars work together seamlessly via Apache Arrow:

```python
import duckdb
import polars as pl

# Polars for data loading and transformation
df = (
    pl.scan_parquet('data/*.parquet')
    .filter(pl.col('date') >= '2024-01-01')
    .collect()
)

# DuckDB for complex SQL analytics
result = duckdb.sql("""
    SELECT
        user_id,
        COUNT(*) as sessions,
        SUM(duration) as total_duration,
        AVG(duration) as avg_duration,
        MAX(duration) as max_duration
    FROM df
    GROUP BY user_id
    HAVING sessions > 5
""").pl()

# Back to Polars for final processing
top_users = result.top_k(10, by='total_duration')
```

See the `polars` skill for more Polars-specific operations and the references/integration.md file for detailed integration examples.

## Error Handling

Common issues and solutions:

```python
import duckdb

try:
    result = duckdb.sql("SELECT * FROM 'data.csv'")
except duckdb.Error as e:
    print(f"DuckDB error: {e}")
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Resources

- **references/integration.md**: Detailed examples of DuckDB + Polars integration patterns
- Official docs: https://duckdb.org/docs/
- Python API: https://duckdb.org/docs/api/python/overview
