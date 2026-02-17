---
name: data-engineering
description: Use when "data pipelines", "ETL", "data warehousing", "data lakes", or asking about "Airflow", "Spark", "dbt", "Snowflake", "BigQuery", "data modeling"
version: 1.0.0
---

<!-- Adapted from: claude-skills/engineering-team/senior-data-engineer -->

# Data Engineering Guide

Data pipelines, warehousing, and modern data stack.

## When to Use

- Building data pipelines
- Designing data warehouses
- Implementing ETL/ELT processes
- Setting up data lakes
- Optimizing data infrastructure

## Modern Data Stack

### Components

```
Sources → Ingestion → Storage → Transform → Serve → Consume
```

| Layer | Tools |
|-------|-------|
| Ingestion | Fivetran, Airbyte, Stitch |
| Storage | S3, GCS, Snowflake, BigQuery |
| Transform | dbt, Spark, Airflow |
| Orchestration | Airflow, Dagster, Prefect |
| Serving | Looker, Tableau, Metabase |

## Data Pipeline Patterns

### Batch Processing

```python
# Airflow DAG example
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG(
    'daily_etl',
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 1, 1)
)

def extract():
    # Extract from source
    pass

def transform():
    # Transform data
    pass

def load():
    # Load to warehouse
    pass

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

### Streaming Processing

```python
# Kafka consumer example
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    process_event(message.value)
```

## dbt Patterns

### Model Structure

```
models/
├── staging/           # 1:1 with source
│   ├── stg_orders.sql
│   └── stg_customers.sql
├── intermediate/      # Business logic
│   └── int_order_items.sql
└── marts/             # Final models
    ├── dim_customers.sql
    └── fct_orders.sql
```

### Example Model

```sql
-- models/marts/fct_orders.sql
{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

select
    o.order_id,
    o.customer_id,
    o.order_date,
    sum(oi.quantity * oi.unit_price) as order_total
from {{ ref('stg_orders') }} o
join {{ ref('stg_order_items') }} oi
    on o.order_id = oi.order_id
{% if is_incremental() %}
where o.order_date > (select max(order_date) from {{ this }})
{% endif %}
group by 1, 2, 3
```

## Data Modeling

### Dimensional Modeling

```
Fact Tables (events/transactions)
├── fct_orders
├── fct_page_views
└── fct_transactions

Dimension Tables (context)
├── dim_customers
├── dim_products
├── dim_dates
└── dim_locations
```

### Star Schema

```
        dim_customers
              │
dim_dates ── fct_orders ── dim_products
              │
        dim_locations
```

## Data Quality

### Validation Rules

```sql
-- dbt tests
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: order_total
        tests:
          - not_null
          - positive_value
```

### Quality Metrics

| Metric | Description |
|--------|-------------|
| Completeness | % non-null values |
| Uniqueness | % distinct values |
| Timeliness | Data freshness |
| Accuracy | Matches source |
| Consistency | Across systems |

## Performance Optimization

### Partitioning

```sql
-- BigQuery partitioned table
CREATE TABLE orders
PARTITION BY DATE(order_date)
CLUSTER BY customer_id
AS SELECT * FROM staging.orders
```

### Query Optimization

| Technique | Impact |
|-----------|--------|
| Partitioning | Reduce scanned data |
| Clustering | Improve filter speed |
| Materialization | Pre-compute joins |
| Caching | Reduce repeat queries |

## Monitoring

### Pipeline Metrics

| Metric | Alert Threshold |
|--------|-----------------|
| Runtime | >2x normal |
| Row count | ±20% variance |
| Freshness | >SLA |
| Failures | Any failure |

### Data Observability

```yaml
# Monte Carlo / Elementary example
monitors:
  - table: fct_orders
    tests:
      - freshness:
          threshold: 6 hours
      - volume:
          threshold: 10%
      - schema_change: true
```

## Best Practices

### Pipeline Design

- Idempotent operations
- Incremental processing
- Clear data lineage
- Automated testing

### Data Governance

- Document all models
- Track data lineage
- Implement access controls
- Version control SQL

### Cost Management

- Monitor query costs
- Use partitioning
- Schedule off-peak
- Archive old data
