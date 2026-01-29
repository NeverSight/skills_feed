---
name: data-warehouse
description: Data warehouse design mastery with star schema, dimensional modeling, fact/dimension tables, slowly changing dimensions, and enterprise best practices. Complete schema examples included.
sasmp_version: "1.3.0"
bonded_agent: 06-data-engineer
bond_type: PRIMARY_BOND
---

# Data Warehouse Design

## Star Schema Basics

### Fact Table Design

```sql
-- Star schema with sales fact table
CREATE TABLE fact_sales (
  sales_id BIGINT PRIMARY KEY,
  date_id INT NOT NULL,
  customer_id INT NOT NULL,
  product_id INT NOT NULL,
  store_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10, 2),
  sale_amount DECIMAL(12, 2),
  discount_amount DECIMAL(12, 2),
  net_sales DECIMAL(12, 2),
  tax_amount DECIMAL(12, 2),
  total_sale DECIMAL(12, 2),

  -- Foreign keys
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);

-- Create indexes on foreign keys for query performance
CREATE INDEX idx_fact_sales_date ON fact_sales(date_id);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_id);
CREATE INDEX idx_fact_sales_store ON fact_sales(store_id);
```

### Dimension Table Design

```sql
-- Date dimension (conformed dimension - used across multiple facts)
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  full_date DATE UNIQUE,
  day_of_week INT,
  day_of_week_name VARCHAR(10),
  day_of_month INT,
  week_of_year INT,
  month_number INT,
  month_name VARCHAR(12),
  quarter INT,
  year INT,
  fiscal_quarter INT,
  fiscal_year INT,
  is_holiday BOOLEAN,
  is_weekend BOOLEAN,
  is_weekday BOOLEAN
);

-- Customer dimension
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_code VARCHAR(20),
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  email VARCHAR(100),
  phone VARCHAR(20),
  gender VARCHAR(10),
  birth_date DATE,
  -- Address hierarchy
  street_address VARCHAR(100),
  city VARCHAR(50),
  state_province VARCHAR(50),
  postal_code VARCHAR(10),
  country VARCHAR(50),
  region VARCHAR(50),
  -- Customer segment
  customer_segment VARCHAR(50),
  customer_lifetime_value DECIMAL(12, 2),
  -- Slowly changing dimension columns
  effective_date DATE,
  end_date DATE,
  is_current BOOLEAN,
  -- Audit columns
  created_date DATE,
  updated_date DATE
);

-- Product dimension
CREATE TABLE dim_product (
  product_id INT PRIMARY KEY,
  product_code VARCHAR(50),
  product_name VARCHAR(200),
  product_category VARCHAR(50),
  product_subcategory VARCHAR(50),
  product_line VARCHAR(50),
  supplier_id INT,
  brand VARCHAR(50),
  model VARCHAR(100),
  color VARCHAR(30),
  size VARCHAR(10),
  unit_cost DECIMAL(10, 2),
  list_price DECIMAL(10, 2),
  cost_to_list_ratio DECIMAL(5, 4),
  product_status VARCHAR(20),
  effective_date DATE,
  end_date DATE,
  is_current BOOLEAN
);
```

## Slowly Changing Dimensions (SCD)

### Type 1: Overwrite

```sql
-- Simply update the existing record
UPDATE dim_customer
SET
  email = 'new_email@example.com',
  phone = '555-9999',
  updated_date = CURRENT_DATE
WHERE customer_id = 1;
```

### Type 2: Add New Row

```sql
-- Close old row
UPDATE dim_customer
SET
  is_current = FALSE,
  end_date = CURRENT_DATE - INTERVAL '1 day'
WHERE customer_id = 1 AND is_current = TRUE;

-- Insert new row
INSERT INTO dim_customer
VALUES (
  customer_id,
  customer_code,
  new_values...,
  CURRENT_DATE,  -- effective_date
  NULL,          -- end_date
  TRUE,          -- is_current
  CURRENT_DATE   -- created_date
);
```

### Type 3: Add New Column

```sql
-- Add previous value columns
ALTER TABLE dim_customer ADD COLUMN previous_city VARCHAR(50);
ALTER TABLE dim_customer ADD COLUMN previous_city_start_date DATE;

-- Update previous columns when changing current
UPDATE dim_customer
SET
  previous_city = city,
  previous_city_start_date = CURRENT_DATE,
  city = 'New York'
WHERE customer_id = 1;
```

## Conformed Dimensions

```sql
-- Single dim_date used across all fact tables
SELECT
  f.sales_id,
  f.quantity * f.unit_price as revenue,
  d.month_name,
  d.year
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id;

-- Reuse dim_customer in multiple facts
SELECT
  fs.sales_id,
  fc.call_id,
  c.customer_segment
FROM fact_sales fs
JOIN dim_customer c ON fs.customer_id = c.customer_id
LEFT JOIN fact_customer_calls fc ON c.customer_id = fc.customer_id;
```

## Aggregate Tables (Materialized Views)

```sql
-- Pre-calculate common aggregations for performance
CREATE MATERIALIZED VIEW sales_summary_daily AS
SELECT
  d.full_date,
  d.month_name,
  d.year,
  p.product_category,
  c.customer_segment,
  COUNT(DISTINCT fs.sales_id) as transaction_count,
  SUM(fs.quantity) as total_quantity,
  ROUND(SUM(fs.net_sales), 2) as total_sales,
  ROUND(AVG(fs.net_sales), 2) as avg_sale,
  COUNT(DISTINCT fs.customer_id) as unique_customers
FROM fact_sales fs
JOIN dim_date d ON fs.date_id = d.date_id
JOIN dim_product p ON fs.product_id = p.product_id
JOIN dim_customer c ON fs.customer_id = c.customer_id
GROUP BY d.full_date, d.month_name, d.year, p.product_category, c.customer_segment;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW sales_summary_daily;

-- Query aggregate table instead of fact table
SELECT
  month_name,
  product_category,
  SUM(total_sales) as monthly_sales
FROM sales_summary_daily
WHERE year = 2024
GROUP BY month_name, product_category;
```

## Bridge Tables (Many-to-Many)

```sql
-- For many-to-many relationships (e.g., product to categories)
CREATE TABLE bridge_product_category (
  product_id INT,
  category_id INT,
  PRIMARY KEY (product_id, category_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  FOREIGN KEY (category_id) REFERENCES dim_category(category_id)
);

-- Query with bridge table
SELECT
  p.product_name,
  STRING_AGG(DISTINCT c.category_name, ', ') as categories,
  COUNT(DISTINCT bc.category_id) as category_count
FROM dim_product p
LEFT JOIN bridge_product_category bc ON p.product_id = bc.product_id
LEFT JOIN dim_category c ON bc.category_id = c.category_id
GROUP BY p.product_id, p.product_name;
```

## Data Quality Metrics

```sql
-- Monitor fact table metrics
SELECT
  COUNT(*) as total_records,
  COUNT(DISTINCT customer_id) as unique_customers,
  COUNT(DISTINCT product_id) as unique_products,
  MIN(sale_amount) as min_sale,
  MAX(sale_amount) as max_sale,
  ROUND(AVG(sale_amount), 2) as avg_sale,
  COUNT(CASE WHEN sale_amount < 0 THEN 1 END) as negative_sales,
  COUNT(CASE WHEN sale_amount IS NULL THEN 1 END) as null_sales,
  MAX(load_timestamp) as last_load_time
FROM fact_sales;

-- Dimension quality checks
SELECT
  'dim_customer' as dimension,
  COUNT(*) as total_records,
  COUNT(DISTINCT customer_id) as distinct_ids,
  COUNT(CASE WHEN first_name IS NULL THEN 1 END) as null_first_names,
  COUNT(CASE WHEN is_current = TRUE THEN 1 END) as current_records
FROM dim_customer;
```

## Next Steps

Learn ETL/ELT pipeline design and data transformation patterns in the `etl-pipelines` skill.
