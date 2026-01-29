---
name: bi-fundamentals
description: BI fundamentals with metric definition, KPI calculation, dimensional modeling, dashboard optimization, and data storytelling. 40+ metric examples and calculation patterns.
sasmp_version: "1.3.0"
bonded_agent: 07-bi-analyst
bond_type: PRIMARY_BOND
---

# Business Intelligence Fundamentals

## Metric Definition & Calculation

### Business Metrics

```sql
-- Core business metrics

-- Revenue metrics
SELECT
  DATE_TRUNC('month', order_date)::DATE as month,
  ROUND(SUM(amount), 2) as total_revenue,
  COUNT(DISTINCT order_id) as order_count,
  ROUND(SUM(amount) / COUNT(DISTINCT order_id), 2) as avg_order_value,
  COUNT(DISTINCT customer_id) as unique_customers,
  ROUND(SUM(amount) / COUNT(DISTINCT customer_id), 2) as revenue_per_customer
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month DESC;

-- Customer metrics
SELECT
  customer_id,
  COUNT(DISTINCT order_id) as lifetime_orders,
  ROUND(SUM(amount), 2) as lifetime_value,
  MIN(order_date) as first_order_date,
  MAX(order_date) as last_order_date,
  ROUND(DATEDIFF(DAY, MIN(order_date), MAX(order_date)) /
    NULLIF(COUNT(DISTINCT order_id) - 1, 0), 2) as avg_days_between_orders,
  ROUND(SUM(amount) / DATEDIFF(DAY, MIN(order_date), CURRENT_DATE), 4) as revenue_per_day
FROM orders
GROUP BY customer_id;

-- Product performance
SELECT
  product_id,
  product_name,
  category,
  COUNT(DISTINCT order_id) as order_count,
  SUM(quantity) as units_sold,
  ROUND(SUM(revenue), 2) as total_revenue,
  ROUND(AVG(revenue), 2) as avg_order_value,
  ROUND(SUM(profit), 2) as total_profit,
  ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) as profit_margin_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY product_id, product_name, category
ORDER BY total_revenue DESC;
```

### KPI Definitions

```sql
-- Key Performance Indicator calculations

-- Monthly Active Users (MAU)
SELECT
  DATE_TRUNC('month', activity_date)::DATE as month,
  COUNT(DISTINCT user_id) as mau
FROM user_activity
GROUP BY DATE_TRUNC('month', activity_date);

-- Customer Acquisition Cost (CAC)
SELECT
  DATE_TRUNC('month', acquired_date)::DATE as month,
  COUNT(DISTINCT customer_id) as new_customers,
  ROUND(SUM(marketing_spend) / COUNT(DISTINCT customer_id), 2) as cac
FROM customers c
JOIN marketing_spend m ON EXTRACT(YEAR FROM c.acquired_date) = EXTRACT(YEAR FROM m.spend_date)
  AND EXTRACT(MONTH FROM c.acquired_date) = EXTRACT(MONTH FROM m.spend_date)
GROUP BY DATE_TRUNC('month', acquired_date);

-- Customer Retention Rate
WITH monthly_activity AS (
  SELECT
    DATE_TRUNC('month', activity_date)::DATE as month,
    customer_id
  FROM orders
  GROUP BY DATE_TRUNC('month', activity_date), customer_id
)
SELECT
  current_month.month,
  COUNT(DISTINCT current_month.customer_id) as current_month_customers,
  COUNT(DISTINCT previous_month.customer_id) as retained_customers,
  ROUND(100.0 * COUNT(DISTINCT previous_month.customer_id) /
    COUNT(DISTINCT current_month.customer_id), 2) as retention_rate_pct
FROM monthly_activity current_month
LEFT JOIN monthly_activity previous_month
  ON current_month.customer_id = previous_month.customer_id
  AND current_month.month = previous_month.month + INTERVAL '1 month'
GROUP BY current_month.month
ORDER BY current_month.month;

-- Net Promoter Score (NPS) calculation
SELECT
  department,
  COUNT(CASE WHEN nps_score >= 9 THEN 1 END) as promoters,
  COUNT(CASE WHEN nps_score >= 7 AND nps_score <= 8 THEN 1 END) as passives,
  COUNT(CASE WHEN nps_score <= 6 THEN 1 END) as detractors,
  COUNT(*) as total_responses,
  ROUND(100.0 * (COUNT(CASE WHEN nps_score >= 9 THEN 1 END) -
    COUNT(CASE WHEN nps_score <= 6 THEN 1 END)) / COUNT(*), 1) as nps_score
FROM customer_surveys
GROUP BY department;
```

## Dimensional Modeling for BI

### Fact Table Grain Selection

```sql
-- Atomic grain (transaction-level)
CREATE TABLE fact_sales_atomic (
  transaction_id BIGINT PRIMARY KEY,
  date_id INT,
  customer_id INT,
  product_id INT,
  store_id INT,
  quantity INT,
  unit_price DECIMAL(10, 2),
  net_sales DECIMAL(12, 2),
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- Summary grain (aggregated for performance)
CREATE TABLE fact_sales_summary (
  summary_id BIGINT PRIMARY KEY,
  date_id INT,
  customer_segment VARCHAR(50),
  product_category VARCHAR(50),
  store_region VARCHAR(50),
  transaction_count INT,
  total_quantity INT,
  total_sales DECIMAL(15, 2),
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);
```

### Dashboard Query Optimization

```sql
-- Optimized for dashboard performance using pre-aggregations
SELECT
  d.month_name,
  d.quarter,
  d.year,
  dpc.product_category,
  dcs.customer_segment,
  COUNT(*) as transaction_count,
  SUM(fss.total_quantity) as units_sold,
  ROUND(SUM(fss.total_sales), 2) as revenue,
  ROUND(SUM(fss.total_sales) / COUNT(*), 2) as avg_transaction_value,
  ROUND(SUM(fss.total_sales) / NULLIF(COUNT(DISTINCT dcs.customer_id), 0), 2) as revenue_per_customer
FROM fact_sales_summary fss
JOIN dim_date d ON fss.date_id = d.date_id
JOIN dim_product_category dpc ON fss.product_category = dpc.category_id
JOIN dim_customer_segment dcs ON fss.customer_segment = dcs.segment_id
WHERE d.year = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY d.month_name, d.quarter, d.year, dpc.product_category, dcs.customer_segment
ORDER BY d.year DESC, d.quarter DESC, d.month_name DESC;
```

## Trend & Variance Analysis

```sql
-- Year-over-year comparison
SELECT
  EXTRACT(MONTH FROM order_date) as month,
  EXTRACT(YEAR FROM order_date) as year,
  ROUND(SUM(amount), 2) as monthly_revenue
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date)
ORDER BY year DESC, month;

-- Budget vs Actual variance
SELECT
  department,
  EXTRACT(MONTH FROM report_date) as month,
  SUM(budgeted_amount) as budget,
  SUM(actual_amount) as actual,
  SUM(actual_amount) - SUM(budgeted_amount) as variance,
  ROUND(100.0 * (SUM(actual_amount) - SUM(budgeted_amount)) /
    NULLIF(SUM(budgeted_amount), 0), 2) as variance_pct
FROM budget_actuals
GROUP BY department, EXTRACT(MONTH FROM report_date)
ORDER BY department, month DESC;

-- Cumulative variance analysis
WITH monthly_budget AS (
  SELECT
    department,
    EXTRACT(MONTH FROM report_date) as month,
    SUM(budgeted_amount) as budget,
    SUM(actual_amount) as actual
  FROM budget_actuals
  GROUP BY department, EXTRACT(MONTH FROM report_date)
)
SELECT
  department,
  month,
  budget,
  actual,
  SUM(actual) OVER (PARTITION BY department ORDER BY month) as ytd_actual,
  SUM(budget) OVER (PARTITION BY department ORDER BY month) as ytd_budget,
  SUM(actual) OVER (PARTITION BY department ORDER BY month) -
    SUM(budget) OVER (PARTITION BY department ORDER BY month) as ytd_variance
FROM monthly_budget
ORDER BY department, month;
```

## Advanced Analytics Calculations

```sql
-- Cohort lifetime value
WITH user_cohorts AS (
  SELECT
    DATE_TRUNC('month', customer_acquired_date)::DATE as cohort_month,
    customer_id,
    DATE_TRUNC('month', order_date)::DATE as order_month,
    amount
  FROM orders o
  JOIN customers c ON o.customer_id = c.id
)
SELECT
  cohort_month,
  DATE_PART('month', order_month::timestamp - cohort_month::timestamp) / 1 as months_since_acquisition,
  COUNT(DISTINCT customer_id) as cohort_size,
  ROUND(SUM(amount), 2) as cohort_revenue
FROM user_cohorts
WHERE order_month >= cohort_month
GROUP BY cohort_month, months_since_acquisition
ORDER BY cohort_month, months_since_acquisition;

-- Customer segmentation with RFM analysis
WITH rfm AS (
  SELECT
    customer_id,
    MAX(order_date) as last_order_date,
    DATEDIFF(DAY, MAX(order_date), CURRENT_DATE) as recency,
    COUNT(DISTINCT order_id) as frequency,
    ROUND(SUM(amount), 2) as monetary,
    NTILE(4) OVER (ORDER BY DATEDIFF(DAY, MAX(order_date), CURRENT_DATE) DESC) as r_score,
    NTILE(4) OVER (ORDER BY COUNT(DISTINCT order_id)) as f_score,
    NTILE(4) OVER (ORDER BY SUM(amount)) as m_score
  FROM orders
  GROUP BY customer_id
)
SELECT
  customer_id,
  CASE
    WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
    WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
    WHEN f_score >= 3 THEN 'At Risk'
    WHEN r_score = 4 THEN 'Lost'
    ELSE 'Other'
  END as segment,
  frequency,
  monetary,
  recency
FROM rfm
ORDER BY monetary DESC;
```

## Best Practices for BI

✅ Use conformed dimensions across all fact tables
✅ Pre-aggregate data for dashboard performance
✅ Implement slowly changing dimensions appropriately
✅ Create metrics at atomic grain level
✅ Use views for metric consistency
✅ Document metric definitions and calculations
✅ Implement data quality checks
✅ Monitor query performance with EXPLAIN PLAN
✅ Use appropriate indexes for BI queries
✅ Implement incremental loads for fact tables
