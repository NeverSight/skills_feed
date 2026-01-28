---
name: design-patterns
description: >
  Database Design, Architecture, and Efficiency Patterns
  Trigger: When implementing software design patterns.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with design patterns"

## When to Use

Use this skill when:
- Designing database schemas
- Implementing normalization strategies
- Creating indexes and optimizing queries
- Managing transactions and data integrity

---

## Decision Tree

```
Need unique identifier?    → Use surrogate key (SERIAL/UUID)
Need M:N relationship?     → Create junction table
Need query optimization?   → Index FK and WHERE columns
Need audit trail?          → Add created_at, updated_at columns
Need soft deletes?         → Add deleted_at column
Need data safety?          → Define ON DELETE behavior
```

---

# Database Design & Architecture Patterns

This guide establishes the architectural standards for designing efficient, scalable, and maintainable databases.

## 1. Normalization & Schema Design

### 1.1 Normal Form
- **Standard:** Adhere to **Third Normal Form (3NF)** for transactional (OLTP) systems to reduce redundancy and maintain data integrity.
- **Exception:** Controlled denormalization is permitted **only** for read-heavy analytical views or data warehousing (OLAP) where performance explicitly dictates it. Document these exceptions.

### 1.2 Primary Keys
- **Surrogate Keys:** Prefer system-generated keys (`SERIAL`, `IDENTITY`, `UUID`) for internal referential integrity. They are immutable and independent of business logic.
    - *Example:* `id SERIAL PRIMARY KEY`
- **Natural Keys:** Use Natural Keys (e.g., Email, SSN, SKU) as **Candidate Keys** with `UNIQUE` constraints to enforce business rules, but avoid using them as Foreign Keys if they are subject to change.

### 1.3 Relationships
- **1:N (One-to-Many):** Foreign Key on the "Many" side.
- **N:M (Many-to-Many):** Always use a dedicated Junction/Bridge table.
    - *Pattern:* `TABLE_A_HAS_TABLE_B` containing `fk_table_a` and `fk_table_b` as a composite Primary Key.

## 2. Efficiency & Performance

### 2.1 Indexing Strategy
- **Foreign Keys:** ALWAYS index Foreign Key columns. Most joins happen here.
- **Search Query:** Index columns frequently used in `WHERE`, `ORDER BY`, and `GROUP BY` clauses.
- **High Selectivity:** Only index columns with high cardinality (many unique values).
- **Avoid Over-indexing:** Indexes speed up reads but slow down writes (`INSERT`/`UPDATE`). Balance accordingly.

### 2.2 Data Types
- **Right-sizing:** Use the smallest data type that fits the future-proof requirement.
    - Use `INT` unless `BIGINT` is truly predicted.
    - Use `VARCHAR(n)` for variable text, `TEXT` for unlimited.
    - Use `DATE` if time component is irrelevant; ensure `TIMESTAMP WITH TIME ZONE` for global apps.
- **JSON/XML:** Use `JSONB` (in PostgreSQL) strictly for semi-structured data that varies wildly. Do not use it to lazily bypass schema modeling.

## 3. Concurrency & Integrity

### 3.1 Constraints
- Enforce data integrity at the database level, not just application level.
- Use `NOT NULL` for required fields.
- Use `CHECK` constraints for rigid validation (e.g., `percentage >= 0 AND percentage <= 100`).

### 3.2 Transactions
- Unit of Work: Operations modifying multiple tables must be wrapped in a Transaction (`BEGIN` ... `COMMIT`).
- Locking: Be aware of `SELECT FOR UPDATE` when reading data that will be immediately modified to prevent race conditions.

## 4. Data Lifecycle Patterns

### 4.1 Standard Audit Columns
All tables should include these columns for traceability:
- `created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()`
- `updated_at TIMESTAMP WITH TIME ZONE` — Update via trigger or application logic.
- `created_by` / `updated_by` — Optional, for user attribution.

### 4.2 Soft Deletes
Instead of physically deleting rows, mark them as deleted to preserve history and enable recovery.
- Add `deleted_at TIMESTAMP` (NULL = active, NOT NULL = deleted).
- Filter queries: `WHERE deleted_at IS NULL`.

> [!WARNING]
> Soft deletes add complexity. Use only when audit trails or undo functionality is required.

### 4.3 Cascading Behavior
Define explicit `ON DELETE` / `ON UPDATE` actions on Foreign Keys:
- `CASCADE`: Delete/update child rows automatically. Use with caution.
- `SET NULL`: Set FK to NULL if parent is deleted. Requires nullable FK.
- `RESTRICT` (default): Prevent deletion if children exist.
- `NO ACTION`: Similar to RESTRICT, checked at end of transaction.
