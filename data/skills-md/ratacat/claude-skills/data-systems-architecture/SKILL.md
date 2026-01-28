---
name: data-systems-architecture
description: Use when designing databases for data-heavy applications, making schema decisions for performance, choosing between normalization and denormalization, selecting storage/indexing strategies, planning for scale, or evaluating OLTP vs OLAP trade-offs. Also use when encountering N+1 queries, ORM issues, or concurrency problems.
---

# Data Systems Architecture

## Overview

**Core principle:** Good data system architecture balances reliability (correct operation under faults), scalability (handling growth gracefully), and maintainability (enabling productive change over time). Every architectural decision involves trade-offs between these concerns.

This skill synthesizes knowledge from three foundational texts:
- *Designing Data-Intensive Applications* (Kleppmann) - distributed systems, storage engines, scaling
- *The Art of PostgreSQL* (Fontaine) - PostgreSQL-specific patterns, SQL as programming
- *PostgreSQL Query Optimization* (Dombrovskaya et al.) - execution plans, performance tuning

## When to Use

| Symptom | Start With |
|---------|------------|
| Designing a new database/schema | `01-foundational-principles.md` |
| Normalization vs denormalization decisions | `02-data-modeling.md` |
| Need to understand OLTP vs OLAP | `03-storage-engines.md` |
| Slow queries, index selection | `04-indexing.md` |
| Planning for growth, read replicas | `05-scaling-patterns.md` |
| Race conditions, deadlocks, isolation issues | `06-transactions-concurrency.md` |
| N+1 queries, ORM problems, application integration | `07-application-integration.md` |

## Navigation

### Reference Files (Load as needed)

```
01-foundational-principles.md    - Reliability/Scalability/Maintainability, load parameters
02-data-modeling.md              - Normalization, denormalization, schema design patterns
03-storage-engines.md            - B-trees, LSM-trees, OLTP vs OLAP, PostgreSQL internals
04-indexing.md                   - Index types, compound indexes, covering indexes, maintenance
05-scaling-patterns.md           - Replication, partitioning, sharding strategies
06-transactions-concurrency.md   - ACID, isolation levels, MVCC, locking patterns
07-application-integration.md    - ORM pitfalls, N+1, business logic placement, batch processing
```

## Quick Decision Framework

```
New system design?
├─ Yes → Read 01, then 02 for data model
└─ No → What's the problem?
         ├─ "Queries are slow" → Read 04 (indexing) + 03 (storage patterns)
         ├─ "Data is inconsistent" → Read 02 (modeling) + 06 (transactions)
         ├─ "Can't handle the load" → Read 05 (scaling) + 03 (OLTP vs OLAP)
         ├─ "App makes too many queries" → Read 07 (N+1, ORM patterns)
         └─ "Race conditions/deadlocks" → Read 06 (concurrency)
```

## Core Concepts (Quick Reference)

### The Three Pillars

| Concern | Definition | Key Question |
|---------|------------|--------------|
| **Reliability** | System works correctly under faults | What happens when things fail? |
| **Scalability** | Handles growth gracefully | What's 10x load look like? |
| **Maintainability** | Easy to operate and evolve | Can new engineers understand this? |

### Data Model Selection

| Model | Best For | Avoid When |
|-------|----------|------------|
| **Relational** | Many-to-many relationships, joins, consistency | Highly hierarchical data, constant schema changes |
| **Document** | Self-contained docs, tree structures | Need for joins, many-to-many |
| **Graph** | Highly connected data, recursive queries | Simple CRUD, no relationship traversal |

### OLTP vs OLAP

| Aspect | OLTP | OLAP |
|--------|------|------|
| **Query pattern** | Point lookups, few rows | Aggregates, many rows |
| **Optimization** | Index everything used in WHERE | Fewer indexes, full scans OK |
| **Storage** | Row-oriented | Consider column-oriented |

### Index Type Quick Reference

| Type | Use Case | PostgreSQL |
|------|----------|------------|
| **B-tree** | Equality, range, sorting | Default, most queries |
| **Hash** | Equality only | Faster for exact match |
| **GIN** | Arrays, JSONB, full-text | `@>`, `@@` operators |
| **GiST** | Geometric, range types | PostGIS, nearest-neighbor |
| **BRIN** | Large, naturally ordered tables | Time-series data |

### Isolation Levels

| Level | Prevents | PostgreSQL Default? |
|-------|----------|-------------------|
| **Read Committed** | Dirty reads | Yes |
| **Repeatable Read** | + Non-repeatable reads | No |
| **Serializable** | All anomalies | No (uses SSI) |

## Design Checklist

Before finalizing a data architecture:

- [ ] Identified load parameters (read/write ratio, data volume, latency requirements)
- [ ] Chose appropriate data model (relational/document/graph hybrid?)
- [ ] Normalized to 3NF first, denormalized only with measured justification
- [ ] Designed indexes for actual query patterns (not hypothetical)
- [ ] Considered 10x growth scenario
- [ ] Established isolation level requirements
- [ ] Defined where business logic lives (app vs DB vs both)
- [ ] Planned for operations (backups, monitoring, migrations)

## References

- Kleppmann, M. *Designing Data-Intensive Applications* (O'Reilly, 2017)
- Fontaine, D. *The Art of PostgreSQL* (2nd ed., 2020)
- Dombrovskaya, H., Novikov, B., Bailliekova, A. *PostgreSQL Query Optimization* (Apress, 2021)
