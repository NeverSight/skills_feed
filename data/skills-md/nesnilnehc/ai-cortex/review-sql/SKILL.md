---
name: review-sql
description: Review SQL and query code for injection risk, parameterization, indexing and performance, transactions, NULL and constraints, and dialect portability. Language-only atomic skill; output is a findings list.
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-security, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review SQL

## Purpose

Review **SQL** and query-related code for **language and query conventions** only. Cover injection and parameterization, indexing and execution-plan concerns, transactions and isolation, NULL and unique constraints, dialect portability, large-table and paging patterns, and sensitive columns and permissions. Emit a **findings list** in the standard format for aggregation. Do not define scope or perform full security/architecture review; injection is in scope here as an SQL-specific concern, but broader security is for [review-security](../review-security/SKILL.md).

---

## Use Cases

- **Orchestrated review**: Used as the language step when [review-code](../review-code/SKILL.md) runs for projects that include SQL (.sql files, embedded SQL, or ORM-generated SQL).
- **SQL-only review**: When the user wants only query correctness, performance, and safety checked.
- **Migration or portability**: Check dialect-specific constructs and portability across databases.

**When to use**: When the code under review includes SQL (raw .sql, embedded in code, or ORM-generated). Scope (diff vs paths) is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: SQL and query logic in the **given scope** (files, snippets, or diff). Accept .sql files, embedded SQL in application code, or ORM-generated SQL when visible.
- **Do not**: Decide scope (diff vs codebase); do not perform full application security or architecture review. Focus on SQL/query dimension.

### Review checklist (SQL dimension only)

1. **Injection and parameterization**: No string concatenation or interpolation for user input in SQL; use parameterized queries or prepared statements; avoid dynamic SQL from untrusted input.
2. **Indexing and execution plan**: Queries that filter or join on unindexed columns; SELECT * on large tables; missing indexes for WHERE/JOIN/ORDER BY.
3. **Transactions and isolation**: Appropriate transaction boundaries; isolation level and locking; avoid long-running transactions; deadlock risk.
4. **NULL and unique constraints**: Handling of NULL in comparisons and aggregates; unique constraints and duplicate handling; NOT NULL where appropriate.
5. **Dialect and portability**: Database-specific syntax (e.g. LIMIT vs OFFSET/FETCH, date functions) and portability if multi-DB support is required.
6. **Large tables and paging**: Full scans on large tables; paging (keyset vs OFFSET) and scalability.
7. **Sensitive columns and permissions**: Sensitive data in SELECT; least-privilege and role usage in SQL (where visible).

### Tone and references

- **Professional and technical**: Reference specific locations (file:line or query identifier). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or snippets containing SQL (e.g. .sql files, code with embedded SQL, or ORM-generated SQL when available). Provided by the user or scope skill.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **language-sql**.

---

## Restrictions

- **Do not** perform scope selection or full security/architecture review. Stay within SQL and query conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** assume a specific database vendor unless stated; note dialect when relevant.

---

## Self-Check

- [ ] Was only the SQL/query dimension reviewed (no scope/architecture beyond query design)?
- [ ] Are parameterization, indexing, transactions, NULL/constraints, and portability covered where relevant?
- [ ] Is each finding emitted with Location, Category=language-sql, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line or query identifier?

---

## Examples

### Example 1: String concatenation in query

- **Input**: Query built with string concatenation including user input.
- **Expected**: Emit a critical finding for SQL injection; suggest parameterized query or prepared statement. Category = language-sql.

### Example 2: Large table without paging

- **Input**: SELECT * FROM large_table ORDER BY id without LIMIT or paging.
- **Expected**: Emit finding for performance and scalability; suggest paging (e.g. keyset or OFFSET/FETCH) and avoid SELECT * if not needed. Category = language-sql.

### Edge case: ORM-generated SQL

- **Input**: Only application code using an ORM; generated SQL not visible.
- **Expected**: Review any raw SQL or query builders in the code; if no SQL is visible, state that and skip or report "No SQL to review in scope." Do not invent SQL.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range) or query identifier. |
| **Category** | `language-sql`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `scripts/orders.sql:12`
- **Category**: language-sql
- **Severity**: critical
- **Title**: Query built with string concatenation; injection risk
- **Description**: User-controlled input is concatenated into the WHERE clause.
- **Suggestion**: Use parameterized query or prepared statement with placeholders.
```
