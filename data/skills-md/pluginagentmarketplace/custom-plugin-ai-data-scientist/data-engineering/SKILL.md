---
name: data-engineering
description: ETL pipelines, Apache Spark, data warehousing, and big data processing. Use for building data pipelines, processing large datasets, or data infrastructure.
sasmp_version: "1.3.0"
bonded_agent: 03-data-engineering
bond_type: PRIMARY_BOND
---

# Data Engineering

Build scalable data pipelines and infrastructure for big data processing.

## Quick Start with Apache Spark

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum, count

# Initialize Spark
spark = SparkSession.builder \
    .appName("DataProcessing") \
    .config("spark.executor.memory", "4g") \
    .getOrCreate()

# Read data
df = spark.read.parquet("s3://bucket/data/")

# Transformations (lazy evaluation)
df_clean = df \
    .filter(col("value") > 0) \
    .groupBy("category") \
    .agg(
        sum("sales").alias("total_sales"),
        avg("price").alias("avg_price"),
        count("*").alias("count")
    ) \
    .orderBy(col("total_sales").desc())

# Write results
df_clean.write \
    .mode("overwrite") \
    .partitionBy("date") \
    .parquet("s3://bucket/output/")
```

## ETL Pipeline with Apache Airflow

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

def extract(**context):
    # Extract data from source
    data = fetch_api_data()
    context['task_instance'].xcom_push(key='raw_data', value=data)

def transform(**context):
    # Transform data
    data = context['task_instance'].xcom_pull(key='raw_data')
    cleaned = clean_and_transform(data)
    context['task_instance'].xcom_push(key='clean_data', value=cleaned)

def load(**context):
    # Load to data warehouse
    data = context['task_instance'].xcom_pull(key='clean_data')
    load_to_warehouse(data)

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag
)

extract_task >> transform_task >> load_task
```

## Data Warehousing

### Star Schema Design
```sql
-- Fact Table
CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    quantity INT,
    revenue DECIMAL(10,2),
    cost DECIMAL(10,2)
);

-- Dimension Table
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    brand VARCHAR(100)
);
```

### Snowflake Data Warehouse
```sql
-- Create warehouse
CREATE WAREHOUSE compute_wh
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- Load data from S3
COPY INTO sales_table
FROM 's3://bucket/data/'
FILE_FORMAT = (TYPE = 'PARQUET')
ON_ERROR = 'CONTINUE';

-- Clustering
ALTER TABLE sales CLUSTER BY (date, region);

-- Time travel
SELECT * FROM sales AT (OFFSET => -3600);  -- 1 hour ago
```

## Big Data Processing

### Spark SQL
```python
# Register as temp view
df.createOrReplaceTempView("sales")

# SQL queries
result = spark.sql("""
    SELECT
        category,
        SUM(sales) as total_sales,
        AVG(price) as avg_price
    FROM sales
    WHERE date >= '2024-01-01'
    GROUP BY category
    HAVING SUM(sales) > 10000
    ORDER BY total_sales DESC
""")

result.show()
```

### Spark Optimization
```python
# Cache in memory
df.cache()

# Repartition
df.repartition(200)

# Broadcast small tables
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")

# Persist
from pyspark.storagelevel import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)
```

## Stream Processing with Kafka

```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send('topic-name', {'key': 'value'})

# Consumer
consumer = KafkaConsumer(
    'topic-name',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='my-group',
    auto_offset_reset='earliest'
)

for message in consumer:
    process_message(message.value)
```

## Data Quality Validation

```python
import great_expectations as ge

# Load data
df = ge.read_csv('data.csv')

# Define expectations
df.expect_column_values_to_not_be_null('user_id')
df.expect_column_values_to_be_unique('email')
df.expect_column_values_to_be_between('age', 0, 120)
df.expect_column_values_to_match_regex(
    'email',
    r'^[\w\.-]+@[\w\.-]+\.\w+$'
)

# Validate
results = df.validate()
print(results)
```

## Delta Lake (Data Lakehouse)

```python
from delta.tables import DeltaTable

# Write to Delta
df.write.format("delta") \
    .mode("overwrite") \
    .save("/path/to/delta-table")

# Read from Delta
df = spark.read.format("delta").load("/path/to/delta-table")

# ACID transactions
deltaTable = DeltaTable.forPath(spark, "/path/to/delta-table")

# Upsert (merge)
deltaTable.alias("target") \
    .merge(
        updates.alias("source"),
        "target.id = source.id"
    ) \
    .whenMatchedUpdate(set={"value": "source.value"}) \
    .whenNotMatchedInsert(
        values={"id": "source.id", "value": "source.value"}
    ) \
    .execute()

# Time travel
df = spark.read.format("delta") \
    .option("versionAsOf", 10) \
    .load("/path/to/delta-table")
```

## Best Practices

1. **Incremental processing**: Process only new data
2. **Idempotency**: Same input produces same output
3. **Data validation**: Check quality at every stage
4. **Monitoring**: Track pipeline health and performance
5. **Error handling**: Retry logic, dead letter queues
6. **Partitioning**: Partition large datasets by date/category
7. **Compression**: Use Parquet, ORC for storage efficiency
