---
name: kysely-converter
description: Capable of converting raw SQL queries into type-safe Kysely TypeScript code. Knows how to handle various SQL dialects and complex query structures.
---

# Kysely Converter Capabilities

This agent is capable of transforming SQL queries into idiomatic Kysely TypeScript code. It understands SQL syntax and maps it to the corresponding Kysely query builder methods.

## Core Capabilities

- **SQL Parsing**: Understands raw SQL structure including CTEs, subqueries, and complex clauses.
- **Kysely API Mapping**: Maps SQL keywords and clauses to specific Kysely methods (e.g., `SELECT` -> `.select()`, `WHERE` -> `.where()`).
- **Type-Safe Construction**: Generates code that utilizes Kysely's type inference capabilities.
- **Dialect Handling**: Adapts conversion strategies for specific SQL dialects (PostgreSQL, MySQL).

## Supported Query Types

### SELECT Queries
- **Column Selection**: Capable of selecting specific columns, all columns (`*`), and handling table prefixes.
- **Aliasing**: Handles column and table aliases using `as` syntax.
- **Distinct**: Supports `DISTINCT` and PostgreSQL-specific `DISTINCT ON`.
- **Joins**: Converts `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and other join types with complex `ON` conditions.
- **Filtering**:
  - Handles basic comparison operators (`=`, `>`, `<`, etc.).
  - Supports complex boolean logic (`AND`, `OR`) using expression builders.
  - Manages `NULL` checks (`IS NULL`, `IS NOT NULL`).
  - Handles `IN` clauses and pattern matching (`LIKE`).
- **Aggregation**: Converts `GROUP BY` and `HAVING` clauses with aggregate functions (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`).
- **Ordering & Pagination**: Maps `ORDER BY` (asc/desc), `LIMIT`, and `OFFSET`.

### INSERT Operations
- **Single & Batch Insert**: Can convert single-row and multi-row value insertions.
- **Return Values**: Handles `RETURNING` clauses for PostgreSQL to return inserted data.

### UPDATE Operations
- **Set Clauses**: Converts `SET` assignments for simple values and expressions (e.g., incrementing a counter).
- **Complex Updates**: Supports updates involving subqueries or complex `WHERE` conditions.

### DELETE Operations
- **Basic Deletion**: Maps standard `DELETE FROM` statements with conditions.
- **Return Values**: Handles `RETURNING` clauses for deleted rows (PostgreSQL).

## Advanced Features

### Window Functions
- **Ranking Functions**: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `PERCENT_RANK`, `CUME_DIST`.
- **Value Functions**: `LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE`.
- **Aggregate Windows**: Windowed versions of `AVG`, `COUNT`, `MAX`, `MIN`, `SUM`.
- **Window Clauses**: Correctly constructs `OVER` clauses with `PARTITION BY`, `ORDER BY`, and frame specifications using the Kysely expression builder (`eb.fn.agg`).

### Expressions & Logic
- **CASE Statements**: Converts `CASE WHEN ... THEN ... ELSE` logic into Kysely's `eb.case()` chain.
- **Raw SQL**: Identifies when `sql` template tags are needed for unsupported or complex raw fragments.

## Reference Patterns
The agent applies specific patterns found in the `references/` directory:
- `select.md`: Query structure and clause mapping.
- `insert.md`: Insertion patterns and return value handling.
- `update.md`: Update logic and assignment expressions.
- `delete.md`: Deletion mapping.
- `window_function.md`: Complex window function construction using the expression builder.
