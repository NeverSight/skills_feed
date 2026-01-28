---
name: schema-design
description: "Universal database schema design principles: normalization strategy, data types, primary keys, constraints, anti-patterns, and red flags. Apply when designing schemas, reviewing database architecture, or refactoring data models."
---

# Database Schema Design Principles

**"Schema design debt compounds faster than code debt. Fix it now or pay 10x later."**

## Foundation Principles

### Primary Keys
- Every table MUST have a primary key
- Prefer surrogate keys (auto-increment, UUIDv7) over composite natural keys
- UUIDv7 for distributed systems, auto-increment BIGINT for monoliths

### Foreign Keys
- Use FK constraints unless specific reason not to (high-volume logging, sharded DBs)
- ON DELETE: RESTRICT (safest), CASCADE (use sparingly), SET NULL (breaks audit)

### Data Types
- Choose smallest sufficient type (BIGINT vs INT = 4 bytes * rows)
- Money: DECIMAL (never FLOAT/DOUBLE)
- Dates without time: DATE not DATETIME
- Small sets: ENUM not VARCHAR

### Constraints
- NOT NULL on required columns
- UNIQUE on natural keys
- CHECK for business rules
- DEFAULT where appropriate

## Quality Checklist

### Structural Integrity
- [ ] Every table has primary key
- [ ] Foreign key constraints defined
- [ ] Appropriate data types (smallest sufficient)
- [ ] NOT NULL, UNIQUE, CHECK constraints

### Anti-Pattern Scan
- [ ] No EAV (entity-attribute-value) patterns
- [ ] No god tables (> 50 columns)
- [ ] No multi-valued fields (CSV in columns)
- [ ] No DATETIME for date-only data

### Performance
- [ ] Indexes match query patterns
- [ ] Foreign keys indexed
- [ ] Composite index column order optimized

## Decision Trees

### "Should I denormalize this?"
```
Have evidence of query performance problem?
├─ NO → DON'T denormalize (premature optimization)
└─ YES → Tried indexes, query optimization, caching?
   ├─ NO → Try those first
   └─ YES → Read-heavy (> 100:1)?
      ├─ NO → Normalize, optimize queries
      └─ YES → Denormalize specific fields
```

### "UUID or auto-increment?"
```
Distributed system (multiple write nodes)?
├─ YES → UUIDv7 (time-ordered, better than v4)
└─ NO → Exposed to users (issue-123)?
   ├─ YES → Auto-increment (better UX)
   └─ NO → Auto-increment (better performance)
```

### "Soft or hard delete?"
```
GDPR "right to erasure" applies?
├─ YES → Hard delete or audit table
└─ NO → Need audit trail?
   ├─ YES → Audit table pattern (recommended)
   └─ NO → High deletion rate (> 20%)?
      ├─ YES → Hard delete
      └─ NO → Soft delete acceptable
```

## References

Detailed patterns and examples:
- `references/anti-patterns.md` — EAV, god tables, multi-valued fields, red flags
- `references/normalization.md` — 1NF/2NF/3NF, when to denormalize, OLTP vs OLAP
- `references/advanced-patterns.md` — Soft delete, temporal data, JSON columns
- `references/naming-conventions.md` — Tables, columns, indexes, constraints
- `references/performance-patterns.md` — Indexing strategy, partitioning, data types

## Remember

**"The best schema is one you can understand in 6 months and modify with confidence."**

Design schemas that:
1. **Enforce integrity** — Constraints, foreign keys, data types
2. **Optimize for common patterns** — Indexes, denormalization where proven
3. **Enable evolution** — Proper normalization, migration strategy
4. **Prevent known anti-patterns** — No EAV, god tables, multi-valued fields
