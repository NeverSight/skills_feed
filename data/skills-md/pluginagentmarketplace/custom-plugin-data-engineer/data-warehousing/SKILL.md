---
name: data-warehousing
description: Snowflake, BigQuery, Redshift, dimensional modeling, and modern data warehouse architecture
sasmp_version: "1.3.0"
bonded_agent: 01-data-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 130
prerequisites: [sql-databases]
unlocks: [big-data, etl-tools]
---

# Data Warehousing

Production-grade data warehouse design with Snowflake, BigQuery, and dimensional modeling patterns.

## Quick Start

```sql
-- Snowflake Modern Data Warehouse Setup
CREATE WAREHOUSE analytics_wh
    WITH WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 4;

-- Create dimensional model
CREATE TABLE marts.fact_orders (
    order_key BIGINT AUTOINCREMENT PRIMARY KEY,
    date_key INT NOT NULL REFERENCES dim_date(date_key),
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
) CLUSTER BY (date_key);

-- Dimension with SCD Type 2
CREATE TABLE marts.dim_customer (
    customer_key INT AUTOINCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(255),
    segment VARCHAR(50),
    valid_from DATE NOT NULL,
    valid_to DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE
);
```

## Core Concepts

### 1. Dimensional Modeling (Kimball)

```sql
-- Star Schema Design
-- Fact table: measurable business events
-- Dimension tables: context for analysis

-- Date dimension (conformed)
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week INT,
    day_name VARCHAR(10),
    month_num INT,
    month_name VARCHAR(10),
    quarter INT,
    year INT,
    is_weekend BOOLEAN,
    fiscal_year INT,
    fiscal_quarter INT
);

-- SCD Type 2 MERGE pattern
MERGE INTO dim_customer AS target
USING staging_customer AS source
ON target.customer_id = source.customer_id AND target.is_current = TRUE
WHEN MATCHED AND (
    target.customer_name != source.customer_name OR
    target.segment != source.segment
) THEN UPDATE SET valid_to = CURRENT_DATE - 1, is_current = FALSE
WHEN NOT MATCHED THEN INSERT (
    customer_id, customer_name, segment, valid_from
) VALUES (
    source.customer_id, source.customer_name, source.segment, CURRENT_DATE
);
```

### 2. Snowflake Optimization

```sql
-- Clustering for performance
ALTER TABLE fact_orders CLUSTER BY (date_key, customer_key);
SELECT SYSTEM$CLUSTERING_INFORMATION('fact_orders');

-- Materialized views for aggregations
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT date_key, SUM(total_amount) AS daily_revenue, COUNT(*) AS order_count
FROM fact_orders GROUP BY date_key;

-- Search optimization
ALTER TABLE fact_orders ADD SEARCH OPTIMIZATION ON EQUALITY(order_id);

-- Time travel for debugging
SELECT * FROM fact_orders AT(TIMESTAMP => '2024-01-15 10:00:00'::TIMESTAMP);

-- Zero-copy cloning
CREATE TABLE fact_orders_dev CLONE fact_orders;
```

### 3. BigQuery Patterns

```sql
-- Partitioned and clustered table
CREATE TABLE `project.dataset.fact_events`
PARTITION BY DATE(event_timestamp)
CLUSTER BY user_id, event_type
OPTIONS (partition_expiration_days = 365, require_partition_filter = TRUE)
AS SELECT * FROM source_events;

-- Efficient query with partition pruning
SELECT event_type, COUNT(*) AS event_count
FROM `project.dataset.fact_events`
WHERE DATE(event_timestamp) BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY event_type;

-- BigQuery ML inline
CREATE OR REPLACE MODEL `project.dataset.churn_model`
OPTIONS (model_type = 'LOGISTIC_REG', input_label_cols = ['churned'])
AS SELECT tenure_months, monthly_spend, churned FROM customer_features;
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **Snowflake** | Cloud data warehouse | Latest |
| **BigQuery** | Serverless analytics | Latest |
| **Redshift** | AWS data warehouse | Serverless |
| **Databricks SQL** | Lakehouse analytics | Latest |
| **dbt** | Transformation | 1.7+ |
| **Monte Carlo** | Data observability | Latest |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Slow Query** | Query timeout | No clustering | Add clustering key |
| **High Cost** | Budget exceeded | Large warehouse | Auto-suspend, right-size |
| **Data Skew** | Uneven processing | Poor partition key | Choose better key |

## Best Practices

```sql
-- ✅ DO: Use surrogate keys
customer_key INT AUTOINCREMENT PRIMARY KEY

-- ✅ DO: Add audit columns
_loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()

-- ✅ DO: Cluster on filter columns
CLUSTER BY (date_key)

-- ❌ DON'T: Use natural keys as PK
-- ❌ DON'T: SELECT * in production
```

## Resources

- [Snowflake Docs](https://docs.snowflake.com/)
- [BigQuery Docs](https://cloud.google.com/bigquery/docs)
- "The Data Warehouse Toolkit" by Ralph Kimball

---

**Skill Certification Checklist:**
- [ ] Can design star/snowflake schemas
- [ ] Can implement SCD Type 2 dimensions
- [ ] Can optimize with clustering/partitioning
- [ ] Can monitor and optimize costs
