---
name: style-guide
description: >
  SQL Naming, Formatting, and Style Guide
  Trigger: When following database naming conventions.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with style guide"

## When to Use

Use this skill when:
- Writing SQL scripts or migrations
- Naming database objects (tables, columns, indexes)
- Formatting queries for readability
- Creating reference implementations

---

## Decision Tree

```
Need table name?           → UPPER_SNAKE_CASE, singular
Need column name?          → lower_snake_case
Need boolean column?       → Prefix with is_, has_, can_
Need index name?           → idx_table_columns
Need constraint name?      → pk_, fk_, uq_, ck_ prefixes
```

---

# SQL Style Guide

To ensure maintainability, readability, and consistency across database projects, follow these styling and naming conventions.

## 1. Naming Conventions

### 1.1 Tables
- **Case:** Use `UPPER_SNAKE_CASE` or `PascalCase` consistently. (Standard: `UPPER_SNAKE_CASE` for SQL compatibility).
- **Plurality:** Use **Singular** names for entities to represent the definition of a single record (e.g., `USER`, `ORDER`, not `USERS`).
- **Prefixes:** Avoid Hungarian notation (e.g., `tbl_User`).
- **Junction Tables:** Combine names of related tables (e.g., `USER_ROLE`).

### 1.2 Columns
- **Case:** Use `lower_snake_case`.
- **Clarity:** Names should be descriptive (e.g., `created_at` instead of `date`).
- **Booleans:** Prefix with `is_`, `has_`, or `can_` (e.g., `is_active`).
- **Foreign Keys:** Use `fk_<target_table_id>` or `<target_table>_id` consistently.

### 1.3 Keys & Constraints
Explicitly name all constraints to facilitate debugging.
- **Primary Keys:** `pk_<table_name>`
- **Foreign Keys:** `fk_<source>_<target>`
- **Unique:** `uq_<table_name>_<columns>`
- **Check:** `ck_<table_name>_<condition_description>`

### 1.4 Database Objects
- **Views:** Prefix with `v_` or `vw_`.
- **Materialized Views:** Prefix with `mv_`.
- **Functions:** Prefix with `fn_` (e.g., `fn_calculate_tax`).
- **Procedures:** Prefix with `sp_` (Stored Procedure) (e.g., `sp_archive_orders`).
- **Triggers:** Prefix with `trg_` followed by timing (e.g., `trg_users_before_insert`).
- **Indexes:** Prefix with `idx_` followed by table and columns (e.g., `idx_employee_organization_id`).

## 2. Formatting

### 2.1 Keywords
- Write all SQL keywords in **UPPERCASE** (e.g., `SELECT`, `FROM`, `WHERE`).

### 2.2 Indentation
- Use 4 spaces for indentation.
- Align clauses for readability.

```sql
SELECT
    u.id,
    u.email,
    COUNT(o.id) AS total_orders
FROM USER u
LEFT JOIN ORDER o ON u.id = o.user_id
WHERE
    u.is_active = TRUE
GROUP BY
    u.id,
    u.email;
```

### 2.3 Comments
- Use `--` for single-line comments.
- Use `/* ... */` for multi-line block comments.
- **Header:** Every script/procedure must have a header documenting Author, Date, and Purpose.

```sql
-- =============================================================================
-- PURPOSE: Calculates monthly recurring revenue
-- AUTHOR:  [Name]
-- DATE:    YYYY-MM-DD
-- =============================================================================
```

## 3. Best Practices
- **No `SELECT *`:** Always specify columns explicitly to avoid breaking changes when schemas evolve.
- **Aliases:** Use short, meaningful aliases for tables (e.g., `u` for `USER`).
- **Termination:** Always terminate statements with a semicolon `;`.

## 4. Reference Implementation

Below is an example schema that demonstrates the application of these Style, Design, and Security rules.

```sql
-- =============================================================================
-- SCRIPT: Example Schema
-- PURPOSE: Demonstrates the application of custom-rules/database standards.
-- =============================================================================

-- 1. Table Creation (Style Guide: UPPER_SNAKE_CASE, Singular)
-- Design Pattern: Surrogate PK, text type usage.
CREATE TABLE ORGANIZATION (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    tax_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Explicit Constraint Naming
    CONSTRAINT uq_organization_tax_id UNIQUE (tax_id),
    CONSTRAINT ck_organization_name_len CHECK (LENGTH(name) > 0)
);

-- 2. Child Table with Foreign Key
CREATE TABLE EMPLOYEE (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    full_name TEXT NOT NULL,
    salary DECIMAL(10, 2) CHECK (salary >= 0),
    
    -- Foreign Key with Indexing (to be added below)
    CONSTRAINT fk_employee_organization FOREIGN KEY (organization_id) REFERENCES ORGANIZATION(id)
);

-- 3. Indexing (Efficiency Pattern)
-- Index FKs
CREATE INDEX idx_employee_organization_id ON EMPLOYEE(organization_id);
-- Index Searchable fields
CREATE INDEX idx_employee_email ON EMPLOYEE(email);

-- 4. Junction Table (N:M Relationship)
CREATE TABLE PROJECT (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE EMPLOYEE_ASSIGNMENT (
    employee_id INT NOT NULL,
    project_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT NOW(),
    
    PRIMARY KEY (employee_id, project_id),
    CONSTRAINT fk_assignment_employee FOREIGN KEY (employee_id) REFERENCES EMPLOYEE(id),
    CONSTRAINT fk_assignment_project FOREIGN KEY (project_id) REFERENCES PROJECT(id)
);

-- 5. Stored Procedure (Logic Guidelines)
-- Header, idempotent, error handling
CREATE OR REPLACE PROCEDURE sp_register_employee(
    p_org_id INT,
    p_email VARCHAR,
    p_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validation
    IF NOT EXISTS (SELECT 1 FROM ORGANIZATION WHERE id = p_org_id) THEN
        RAISE EXCEPTION 'Organization % does not exist', p_org_id;
    END IF;

    -- Insertion
    INSERT INTO EMPLOYEE (organization_id, email, full_name)
    VALUES (p_org_id, p_email, p_name);
    
    -- Transaction control is implicit in procedures if needed, or controlled by caller.
    
EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'Employee % already registered.', p_email;
END;
$$;

-- 6. RLS (Security Guidelines)
ALTER TABLE EMPLOYEE ENABLE ROW LEVEL SECURITY;

CREATE POLICY employee_isolation_policy ON EMPLOYEE
FOR ALL
USING (organization_id = current_setting('app.current_org_id')::INT);
```
