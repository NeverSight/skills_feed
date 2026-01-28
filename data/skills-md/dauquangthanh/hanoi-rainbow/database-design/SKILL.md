---
name: database-design
description: Designs comprehensive database schemas including relational and NoSQL models, normalization, indexing strategies, relationship modeling, data types, constraints, and performance optimization. Covers entity-relationship diagrams, schema migrations, partitioning, and best practices for PostgreSQL, MySQL, MongoDB, and other databases. Use when designing databases, creating schemas, modeling data, optimizing queries, or when users mention "database design", "schema design", "data modeling", "ERD", "normalization", "indexing", or "database architecture".
---

# Database Design

## Overview

Provides comprehensive guidance for designing robust, scalable, and maintainable database schemas for both relational (SQL) and NoSQL databases, from conceptual modeling to physical implementation.

## Design Workflow

1. **Requirements Analysis** - Gather data requirements and usage patterns
2. **Conceptual Modeling** - Create entity-relationship diagrams (ERD)
3. **Logical Modeling** - Define normalized schema with relationships
4. **Physical Modeling** - Select data types, indexes, and constraints
5. **Validation** - Review design against requirements and best practices

## Quick Start

**Basic E-commerce Schema:**

```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  stock_quantity INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_name (name)
);

-- Orders table
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  total_amount DECIMAL(10,2) NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user_created (user_id, created_at)
);
```

## Core Principles

- **Start normalized, denormalize only when proven necessary**
- **Index strategically based on actual query patterns**
- **Use constraints to enforce data integrity at database level**
- **Choose appropriate data types to optimize storage and performance**
- **Plan for growth with partitioning and sharding strategies**
- **Document design decisions and their rationale**
- **Test with realistic data volumes**

## When to Load References

- **Design Workflow**: See [database-design-workflow.md](references/database-design-workflow.md) for step-by-step design process including requirements analysis, conceptual/logical/physical modeling, normalization steps, and relationship patterns

- **Advanced Patterns**: See [advanced-design-patterns.md](references/advanced-design-patterns.md) for many-to-many relationships, inheritance/polymorphism, temporal data, soft deletes, audit trails, and hierarchical data

- **NoSQL Design**: See [nosql-database-design.md](references/nosql-database-design.md) when designing MongoDB documents, Cassandra column families, or Redis data structures

- **Anti-Patterns**: See [common-anti-patterns-to-avoid.md](references/common-anti-patterns-to-avoid.md) to identify EAV pattern issues, generic tables, redundant data, multi-value columns, and other problematic designs

- **Performance**: See [performance-optimization.md](references/performance-optimization.md) for query optimization, partitioning strategies, caching patterns, and index tuning

- **Migration**: See [schema-migration-best-practices.md](references/schema-migration-best-practices.md) for zero-downtime migrations, backward compatibility, and rollback strategies

- **Checklist**: See [database-design-checklist.md](references/database-design-checklist.md) for comprehensive validation before implementation
