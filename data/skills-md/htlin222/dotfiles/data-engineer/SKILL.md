---
name: data-engineer
description: Build ETL pipelines, data warehouses, and streaming architectures. Use for data pipeline design or analytics infrastructure.
---

# Data Engineering

Build scalable data pipelines and analytics infrastructure.

## When to use

- ETL/ELT pipeline design
- Data warehouse modeling
- Streaming data processing
- Data quality monitoring

## Airflow DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
}

with DAG(
    'etl_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    start_date=days_ago(1),
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load_data,
    )

    validate = PythonOperator(
        task_id='validate',
        python_callable=validate_data,
    )

    extract >> transform >> load >> validate
```

## Data warehouse schema

### Star schema

```sql
-- Fact table
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    quantity INT,
    amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Dimension tables
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    date DATE,
    year INT,
    quarter INT,
    month INT,
    week INT,
    day_of_week INT
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    name VARCHAR(255),
    category VARCHAR(100),
    -- SCD Type 2 fields
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN
);
```

## Spark job

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg

spark = SparkSession.builder \
    .appName("ETL Job") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Read with partitioning
df = spark.read \
    .option("inferSchema", "true") \
    .parquet("s3://bucket/data/") \
    .filter(col("date") >= "2024-01-01")

# Transform
result = df \
    .groupBy("category", "date") \
    .agg(
        sum("amount").alias("total_amount"),
        avg("quantity").alias("avg_quantity")
    ) \
    .repartition(10, "date")  # Optimize for writes

# Write partitioned
result.write \
    .mode("overwrite") \
    .partitionBy("date") \
    .parquet("s3://bucket/output/")
```

## Data quality

```python
from great_expectations.core import ExpectationSuite

suite = ExpectationSuite("sales_data")

# Define expectations
suite.add_expectation(
    expect_column_values_to_not_be_null(column="sale_id")
)
suite.add_expectation(
    expect_column_values_to_be_between(
        column="amount", min_value=0, max_value=1000000
    )
)
suite.add_expectation(
    expect_column_values_to_be_unique(column="sale_id")
)
```

## Best practices

- Idempotent operations (re-runnable)
- Incremental processing over full refresh
- Data lineage tracking
- Schema evolution handling
- Cost monitoring for cloud services

## Examples

**Input:** "Design ETL for user events"
**Action:** Create Airflow DAG with extract/transform/load, add quality checks

**Input:** "Optimize slow Spark job"
**Action:** Check partitioning, reduce shuffles, tune memory settings
