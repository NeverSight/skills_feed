---
name: data-analysis-sql
description: SQL for data analysis with exploratory analysis, advanced aggregations, statistical functions, outlier detection, and business insights. 50+ real-world analytics queries.
sasmp_version: "1.3.0"
bonded_agent: 05-data-analyst
bond_type: PRIMARY_BOND
---

# SQL for Data Analysis

## Exploratory Data Analysis (EDA)

### Data Profiling

```sql
-- Understand data structure and quality
SELECT COUNT(*) as record_count FROM employees;
SELECT COUNT(DISTINCT department) as unique_departments FROM employees;
SELECT COUNT(*) - COUNT(email) as missing_emails FROM employees;

-- Column value distribution
SELECT salary, COUNT(*) as frequency
FROM employees
GROUP BY salary
ORDER BY frequency DESC;

-- Missing data analysis
SELECT
  COUNT(*) as total_records,
  COUNT(phone) as non_null_phone,
  COUNT(*) - COUNT(phone) as missing_phone,
  ROUND(100.0 * (COUNT(*) - COUNT(phone)) / COUNT(*), 2) as missing_percentage
FROM employees;

-- Data type and range checks
SELECT
  MIN(salary) as min_salary,
  MAX(salary) as max_salary,
  ROUND(AVG(salary), 2) as avg_salary,
  ROUND(STDDEV(salary), 2) as salary_stddev
FROM employees;
```

### Distribution Analysis

```sql
-- Value frequency distribution
SELECT
  department,
  COUNT(*) as emp_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
FROM employees
GROUP BY department
ORDER BY emp_count DESC;

-- Salary ranges and distribution
SELECT
  CASE
    WHEN salary < 50000 THEN 'Under 50K'
    WHEN salary < 75000 THEN '50K-75K'
    WHEN salary < 100000 THEN '75K-100K'
    ELSE '100K+'
  END as salary_range,
  COUNT(*) as emp_count,
  MIN(salary) as min_sal,
  MAX(salary) as max_sal,
  ROUND(AVG(salary), 2) as avg_sal
FROM employees
GROUP BY salary_range
ORDER BY MIN(salary);

-- Distribution visualization data
SELECT
  salary,
  COUNT(*) as frequency,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct,
  RPAD('*', COUNT(*) / 10, '*') as bar_chart
FROM employees
GROUP BY salary
ORDER BY salary;
```

## Statistical Analysis

### Summary Statistics

```sql
-- Comprehensive statistics by group
SELECT
  department,
  COUNT(*) as count,
  ROUND(AVG(salary), 2) as mean_salary,
  ROUND(MIN(salary), 2) as min_salary,
  ROUND(MAX(salary), 2) as max_salary,
  ROUND(STDDEV(salary), 2) as stddev_salary,
  ROUND(AVG(ABS(salary - (SELECT AVG(salary) FROM employees WHERE department = e.department))), 2) as avg_deviation
FROM employees e
GROUP BY department
ORDER BY mean_salary DESC;

-- Percentile analysis
SELECT
  department,
  ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary), 2) as q1,
  ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY salary), 2) as median,
  ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary), 2) as q3,
  ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY salary), 2) as p95
FROM employees
GROUP BY department;
```

### Outlier Detection

```sql
-- Find outliers using standard deviation
SELECT
  emp_id,
  first_name,
  salary,
  ROUND(AVG(salary) OVER (), 2) as avg_salary,
  ROUND(STDDEV(salary) OVER (), 2) as stddev_salary,
  ROUND(ABS(salary - AVG(salary) OVER ()) / NULLIF(STDDEV(salary) OVER (), 0), 2) as z_score
FROM employees
HAVING ABS(salary - AVG(salary) OVER ()) / NULLIF(STDDEV(salary) OVER (), 0) > 3
ORDER BY z_score DESC;

-- IQR method for outliers
WITH salary_stats AS (
  SELECT
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary) as q1,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary) as q3
  FROM employees
)
SELECT
  emp_id,
  salary,
  CASE
    WHEN salary < (SELECT q1 FROM salary_stats) - 1.5 * ((SELECT q3 FROM salary_stats) - (SELECT q1 FROM salary_stats))
    OR salary > (SELECT q3 FROM salary_stats) + 1.5 * ((SELECT q3 FROM salary_stats) - (SELECT q1 FROM salary_stats))
    THEN 'Outlier'
    ELSE 'Normal'
  END as outlier_status
FROM employees;
```

## Comparative Analysis

### Period-over-Period Comparison

```sql
-- Year-over-year sales comparison
SELECT
  EXTRACT(QUARTER FROM order_date) as quarter,
  EXTRACT(YEAR FROM order_date) as year,
  ROUND(SUM(amount), 2) as total_sales,
  ROUND(LAG(SUM(amount)) OVER (ORDER BY EXTRACT(YEAR FROM order_date), EXTRACT(QUARTER FROM order_date)), 2) as prev_period,
  ROUND(SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY EXTRACT(YEAR FROM order_date), EXTRACT(QUARTER FROM order_date)), 2) as yoy_change,
  ROUND(100.0 * (SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY EXTRACT(YEAR FROM order_date), EXTRACT(QUARTER FROM order_date))) / LAG(SUM(amount)) OVER (ORDER BY EXTRACT(YEAR FROM order_date), EXTRACT(QUARTER FROM order_date)), 2) as yoy_pct_change
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(QUARTER FROM order_date)
ORDER BY year, quarter;
```

### Cohort Analysis

```sql
-- User cohort analysis
WITH user_cohorts AS (
  SELECT
    DATE_TRUNC('month', first_order_date)::DATE as cohort_month,
    user_id,
    DATE_TRUNC('month', order_date)::DATE as order_month
  FROM users u
  LEFT JOIN orders o ON u.id = o.user_id
)
SELECT
  cohort_month,
  DATE_PART('month', order_month - cohort_month) / 1 as months_since_cohort,
  COUNT(DISTINCT user_id) as users,
  ROUND(100.0 * COUNT(DISTINCT user_id) /
    (SELECT COUNT(DISTINCT user_id) FROM user_cohorts WHERE order_month = cohort_month), 2) as retention_rate
FROM user_cohorts
WHERE order_month >= cohort_month
GROUP BY cohort_month, months_since_cohort
ORDER BY cohort_month, months_since_cohort;
```

## Correlation & Relationship Analysis

```sql
-- Correlation between variables
WITH salary_data AS (
  SELECT
    years_experience,
    salary,
    AVG(salary) OVER () as avg_salary,
    AVG(years_experience) OVER () as avg_experience,
    STDDEV(salary) OVER () as stddev_salary,
    STDDEV(years_experience) OVER () as stddev_experience
  FROM employees
)
SELECT
  ROUND(
    SUM((years_experience - avg_experience) * (salary - avg_salary)) /
    (COUNT(*) * stddev_salary * stddev_experience),
    4
  ) as correlation
FROM salary_data;

-- Segment analysis
SELECT
  CASE
    WHEN years_experience < 2 THEN 'Junior'
    WHEN years_experience < 5 THEN 'Mid-level'
    WHEN years_experience < 10 THEN 'Senior'
    ELSE 'Expert'
  END as experience_level,
  COUNT(*) as count,
  ROUND(AVG(salary), 2) as avg_salary,
  ROUND(AVG(performance_rating), 2) as avg_rating
FROM employees
GROUP BY experience_level
ORDER BY COUNT(*) DESC;
```

## Data Quality Validation

```sql
-- Check for invalid values
SELECT
  CASE
    WHEN salary < 0 THEN 'Negative salary'
    WHEN salary > 1000000 THEN 'Unusually high salary'
    WHEN email NOT LIKE '%@%' THEN 'Invalid email'
    WHEN hire_date > CURRENT_DATE THEN 'Future hire date'
    WHEN years_experience > 70 THEN 'Impossible experience'
    ELSE NULL
  END as data_quality_issue,
  COUNT(*) as count
FROM employees
WHERE salary < 0
  OR salary > 1000000
  OR email NOT LIKE '%@%'
  OR hire_date > CURRENT_DATE
  OR years_experience > 70
GROUP BY data_quality_issue;

-- Duplicate detection
SELECT
  email,
  COUNT(*) as occurrence_count,
  STRING_AGG(DISTINCT emp_id::text, ', ') as emp_ids
FROM employees
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;
```

## Trend Analysis

```sql
-- Moving average
SELECT
  order_date,
  amount,
  ROUND(AVG(amount) OVER (
    ORDER BY order_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ), 2) as moving_avg_7day,
  ROUND(AVG(amount) OVER (
    ORDER BY order_date
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  ), 2) as moving_avg_30day
FROM daily_orders
ORDER BY order_date;

-- Growth rate
SELECT
  DATE_TRUNC('month', order_date)::DATE as month,
  ROUND(SUM(amount), 2) as monthly_revenue,
  ROUND((SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', order_date))) /
    LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) * 100, 2) as growth_rate_pct
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

## Next Steps

Learn advanced SQL concepts and optimization techniques in the `advanced-sql` skill.
