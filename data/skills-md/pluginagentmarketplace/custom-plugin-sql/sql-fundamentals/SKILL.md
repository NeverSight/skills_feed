---
name: sql-fundamentals
description: Master SQL fundamentals including SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP operations. Learn data types, WHERE clauses, ORDER BY, GROUP BY, and basic joins.
sasmp_version: "1.3.0"
bonded_agent: 01-sql-fundamentals
bond_type: PRIMARY_BOND
---

# SQL Fundamentals

## Quick Start

### Your First SELECT Query

```sql
-- Select all employees
SELECT * FROM employees;

-- Select specific columns with WHERE clause
SELECT first_name, last_name, salary
FROM employees
WHERE salary > 50000;

-- Order results by salary
SELECT first_name, last_name, salary
FROM employees
WHERE salary > 50000
ORDER BY salary DESC;
```

## Core Concepts

### Data Types

```sql
-- Numeric types
BIGINT, INT, SMALLINT, TINYINT  -- Integer types
DECIMAL(10,2), FLOAT, DOUBLE     -- Decimal types

-- String types
VARCHAR(255), CHAR(10), TEXT     -- Text types

-- Date/Time types
DATE, TIME, TIMESTAMP, DATETIME  -- Temporal types

-- Other types
BOOLEAN, BLOB, JSON, UUID
```

### DDL Operations (Data Definition Language)

```sql
-- Create a table
CREATE TABLE employees (
  id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE,
  salary DECIMAL(10,2),
  hire_date DATE,
  department_id INT,
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Modify a table
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);
ALTER TABLE employees MODIFY COLUMN salary DECIMAL(12,2);
ALTER TABLE employees DROP COLUMN phone;

-- Drop a table
DROP TABLE employees;
```

### DML Operations (Data Manipulation Language)

```sql
-- Insert single row
INSERT INTO employees (first_name, last_name, salary)
VALUES ('John', 'Doe', 75000);

-- Insert multiple rows
INSERT INTO employees (first_name, last_name, salary) VALUES
('Jane', 'Smith', 80000),
('Bob', 'Johnson', 70000);

-- Update records
UPDATE employees
SET salary = 85000
WHERE first_name = 'John';

-- Delete records
DELETE FROM employees WHERE id = 1;
```

### Query Filtering

```sql
-- WHERE with various operators
SELECT * FROM employees WHERE salary > 50000;
SELECT * FROM employees WHERE salary BETWEEN 40000 AND 80000;
SELECT * FROM employees WHERE first_name IN ('John', 'Jane', 'Bob');
SELECT * FROM employees WHERE email IS NOT NULL;
SELECT * FROM employees WHERE first_name LIKE 'J%';  -- Starts with J
```

### Sorting Results

```sql
-- Single column sorting
SELECT * FROM employees ORDER BY salary DESC;

-- Multiple column sorting
SELECT * FROM employees
ORDER BY department_id ASC, salary DESC;

-- LIMIT results
SELECT * FROM employees
ORDER BY salary DESC
LIMIT 10;  -- Top 10 highest paid
```

## Aggregate Functions

```sql
-- Count, Sum, Average
SELECT COUNT(*) as employee_count FROM employees;
SELECT SUM(salary) as total_salary FROM employees;
SELECT AVG(salary) as avg_salary FROM employees;
SELECT MIN(salary) as min_salary, MAX(salary) as max_salary FROM employees;

-- Group By
SELECT department_id, COUNT(*) as emp_count, AVG(salary) as avg_salary
FROM employees
GROUP BY department_id;

-- Having clause (filter groups)
SELECT department_id, COUNT(*) as emp_count
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 5;
```

## Basic JOINs

```sql
-- INNER JOIN
SELECT e.first_name, e.last_name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;

-- LEFT JOIN
SELECT e.first_name, e.last_name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;

-- Multiple joins
SELECT e.first_name, d.department_name, p.project_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
INNER JOIN projects p ON e.id = p.employee_id;
```

## Common String Functions

```sql
-- Concatenation
SELECT CONCAT(first_name, ' ', last_name) as full_name FROM employees;

-- Length
SELECT first_name, LENGTH(first_name) as name_length FROM employees;

-- Substring
SELECT SUBSTRING(email, 1, POSITION('@' IN email)-1) as username FROM employees;

-- Case functions
SELECT UPPER(first_name), LOWER(last_name) FROM employees;
SELECT TRIM(first_name) FROM employees;
```

## Date Functions

```sql
-- Current date/time
SELECT CURRENT_DATE, CURRENT_TIME, CURRENT_TIMESTAMP;

-- Extract parts
SELECT YEAR(hire_date), MONTH(hire_date), DAY(hire_date)
FROM employees;

-- Date arithmetic
SELECT first_name, hire_date,
       DATEDIFF(CURRENT_DATE, hire_date) as days_employed
FROM employees;

SELECT first_name, hire_date,
       DATE_ADD(hire_date, INTERVAL 1 YEAR) as one_year_anniversary
FROM employees;
```

## Subqueries & Nested Queries

```sql
-- Subquery in WHERE clause
SELECT first_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Subquery in FROM clause
SELECT dept, avg_salary
FROM (
  SELECT department_id as dept, AVG(salary) as avg_salary
  FROM employees
  GROUP BY department_id
) dept_averages
WHERE avg_salary > 70000;

-- Subquery with IN
SELECT first_name, department_id
FROM employees
WHERE department_id IN (
  SELECT id FROM departments
  WHERE location = 'New York'
);

-- EXISTS clause
SELECT d.department_name
FROM departments d
WHERE EXISTS (
  SELECT 1 FROM employees e
  WHERE e.department_id = d.id
  AND e.salary > 100000
);
```

## CASE Statements

```sql
-- Simple CASE
SELECT first_name, salary,
  CASE
    WHEN salary < 50000 THEN 'Junior'
    WHEN salary < 80000 THEN 'Mid-Level'
    WHEN salary < 120000 THEN 'Senior'
    ELSE 'Executive'
  END as level
FROM employees;

-- Multiple conditions
SELECT first_name, salary, years_employed,
  CASE
    WHEN years_employed >= 10 AND salary > 100000 THEN 'Senior Executive'
    WHEN years_employed >= 5 AND salary > 75000 THEN 'Senior Staff'
    WHEN salary > 60000 THEN 'Mid-Level'
    ELSE 'Junior'
  END as category
FROM employees;

-- CASE with aggregation
SELECT department_id,
  COUNT(CASE WHEN salary > 80000 THEN 1 END) as high_earners,
  COUNT(CASE WHEN salary <= 80000 THEN 1 END) as low_earners
FROM employees
GROUP BY department_id;
```

## NULL Handling

```sql
-- COALESCE - return first non-null value
SELECT first_name,
  COALESCE(phone, 'No Phone', 'Unknown') as contact
FROM employees;

-- NULLIF - return NULL if equal
SELECT first_name,
  NULLIF(salary, 0) as salary
FROM employees;

-- IFNULL / ISNULL
SELECT first_name,
  IFNULL(bonus, 0) as bonus_amount
FROM employees;

-- ISNULL in WHERE clause
SELECT first_name FROM employees
WHERE phone IS NULL;
```

## Distinct & Duplicates

```sql
-- DISTINCT
SELECT DISTINCT department_id FROM employees;

-- COUNT DISTINCT
SELECT COUNT(DISTINCT department_id) as unique_departments
FROM employees;

-- Find duplicates
SELECT email, COUNT(*) as count
FROM employees
GROUP BY email
HAVING COUNT(*) > 1;
```

## Union & Set Operations

```sql
-- UNION (removes duplicates)
SELECT first_name FROM employees WHERE salary > 100000
UNION
SELECT first_name FROM contractors WHERE hourly_rate > 100;

-- UNION ALL (keeps duplicates)
SELECT first_name FROM employees
UNION ALL
SELECT first_name FROM contractors;

-- INTERSECT (common records)
SELECT department_id FROM employees
INTERSECT
SELECT department_id FROM projects;

-- EXCEPT (in first but not second)
SELECT employee_id FROM employees
EXCEPT
SELECT employee_id FROM time_off;
```

## Window Functions (Introduction)

```sql
-- ROW_NUMBER
SELECT first_name, salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- RANK with partitioning
SELECT first_name, department_id, salary,
  RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as dept_rank
FROM employees;

-- Running total
SELECT first_name, salary,
  SUM(salary) OVER (ORDER BY id) as running_total
FROM employees;

-- LAG and LEAD
SELECT first_name, salary,
  LAG(salary) OVER (ORDER BY id) as prev_salary,
  LEAD(salary) OVER (ORDER BY id) as next_salary
FROM employees;
```

## Common SQL Patterns

### Employee Salaries Problem
```sql
-- Find employees earning more than their manager
SELECT e.first_name, e.salary
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;

-- Top earner per department
SELECT department_id, first_name, salary
FROM (
  SELECT department_id, first_name, salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as rn
  FROM employees
) ranked
WHERE rn = 1;
```

### Sales & Orders
```sql
-- Monthly sales totals
SELECT DATE_TRUNC('month', order_date) as month,
  SUM(total_amount) as monthly_total
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- Customer lifetime value
SELECT customer_id, COUNT(order_id) as num_orders,
  SUM(total_amount) as lifetime_value
FROM orders
GROUP BY customer_id
ORDER BY lifetime_value DESC;

-- Products never ordered
SELECT product_id, product_name
FROM products
WHERE product_id NOT IN (
  SELECT DISTINCT product_id FROM order_items
);
```

## Performance Tips

```sql
-- Use indexes on frequently filtered columns
CREATE INDEX idx_employee_dept ON employees(department_id);
CREATE INDEX idx_order_date ON orders(order_date);

-- Avoid SELECT * - specify columns
SELECT id, first_name, last_name FROM employees;  -- Better
SELECT * FROM employees;  -- Avoid

-- Filter early - put conditions before joins
SELECT *
FROM employees e
WHERE e.department_id = 1
INNER JOIN departments d ON e.department_id = d.id;

-- Use LIMIT when you only need a sample
SELECT * FROM large_table LIMIT 100;
```

## Next Steps

Learn Advanced SQL including CTEs, complex window functions, and query optimization in the `advanced-sql` skill.
