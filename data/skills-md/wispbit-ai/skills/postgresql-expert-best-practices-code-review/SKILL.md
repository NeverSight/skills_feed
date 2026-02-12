---
name: postgresql-expert-best-practices-code-review
description: PostgreSQL database design, migration, and performance optimization best practices. This skill should be used when writing, reviewing, or refactoring database schemas, migrations, or query patterns. Triggers on tasks involving PostgreSQL databases, schema design, migration optimization, or data modeling.
license: MIT
metadata:
  author: wispbit
  version: "1.0.0"
---

# PostgreSQL Expert Best Practices

Simple, pragmatic, opinionated. Only what matters for writing production-grade PostgreSQL queries.

## When to Apply

Reference these guidelines when:
- Writing database migrations or schema changes
- Creating or modifying PostgreSQL tables and columns
- Adding indexes, constraints, or foreign keys
- Reviewing database schema for performance issues
- Refactoring existing database structures
- Optimizing query performance or database design

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Index Management | CRITICAL-HIGH | `only-concurrent-indexes`, `add-index-for-foreign-key` |
| 2 | Constraint Safety | HIGH | `unique-constraint`, `split-foreign-key`, `set-column-not-null` |
| 3 | Schema Design | MEDIUM | `only-jsonb`, `always-include-columns`, `limit-non-unique-index` |
| 4 | Naming Standards | LOW | `index-naming-standards`, `column-naming-standards` |

## Quick Reference

- `only-concurrent-indexes` - Always use CONCURRENTLY to prevent blocking writes during index creation
- `add-index-for-foreign-key` - Create indexes for foreign keys to improve query performance
- `unique-constraint` - Split unique constraint creation into concurrent index + constraint steps
- `split-foreign-key` - Add foreign keys without validation first, then validate separately
- `set-column-not-null` - Use check constraints before setting NOT NULL to avoid table locks
- `only-jsonb` - Use JSONB instead of JSON for better performance and indexing capabilities
- `always-include-columns` - Include id, created_at, and updated_at in all tables for auditability
- `limit-non-unique-index` - Limit non-unique indexes to maximum three columns for efficiency
- `index-naming-standards` - Use consistent index naming: idx_tablename_columnname
- `column-naming-standards` - Maintain consistent snake_case naming and use id suffix for foreign keys

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/only-concurrent-indexes.md
rules/add-index-for-foreign-key.md
rules/unique-constraint.md
rules/split-foreign-key.md
rules/set-column-not-null.md
rules/only-jsonb.md
rules/always-include-columns.md
rules/limit-non-unique-index.md
rules/index-naming-standards.md
rules/column-naming-standards.md
```

Each rule file contains:
- Brief explanation of why it matters
- Impact level and description
- Incorrect migration example with explanation
- Correct migration example with best practices
- Additional context and references
