---
name: database
description: >
  Database design patterns, SQL best practices, and data modeling guidelines.
  Trigger: When designing schemas, writing SQL, or implementing database security.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with database"

## When to Use

Use this skill when:
- Designing database schemas
- Writing SQL queries or stored procedures
- Implementing RBAC or row-level security
- Optimizing queries for performance

---

## Critical Patterns

### Naming Conventions (REQUIRED)

```sql
-- ✅ ALWAYS: snake_case for tables and columns
CREATE TABLE user_accounts (
    user_id UUID PRIMARY KEY,
    first_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ❌ NEVER: Mixed case or camelCase
CREATE TABLE UserAccounts (
    userId UUID,
    firstName VARCHAR(100)
);
```

### Soft Deletes (RECOMMENDED)

```sql
-- ✅ ALWAYS: Use soft deletes for audit trail
ALTER TABLE orders ADD COLUMN deleted_at TIMESTAMP NULL;

-- Query active records
SELECT * FROM orders WHERE deleted_at IS NULL;
```

### Audit Columns (REQUIRED)

```sql
-- ✅ ALWAYS: Include audit columns
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    -- Audit columns
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id)
);
```

---

## Decision Tree

```
Need unique identifier?    → Use UUID over serial
Need audit trail?          → Add created_at, updated_at, *_by columns
Need to delete records?    → Use soft delete (deleted_at)
Need fast lookups?         → Add appropriate indexes
Need data integrity?       → Use foreign keys + constraints
Need row-level security?   → Implement RLS policies
```

---

## Code Examples

### Index Strategy

```sql
-- ✅ Good: Composite index for common query patterns
CREATE INDEX idx_orders_user_status 
ON orders(user_id, status) 
WHERE deleted_at IS NULL;

-- Use EXPLAIN ANALYZE to verify
EXPLAIN ANALYZE 
SELECT * FROM orders 
WHERE user_id = '...' AND status = 'pending';
```

### Row-Level Security

```sql
-- Enable RLS
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy: Users see only their documents
CREATE POLICY user_documents ON documents
    FOR ALL
    USING (owner_id = current_user_id());
```

---

## Commands

```sql
-- Check table size
SELECT pg_size_pretty(pg_total_relation_size('table_name'));

-- Analyze query performance
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;

-- View index usage
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

---

## Resources

Specialized database documentation:
- **Design Patterns**: [design-patterns.md](design-patterns.md)
- **Logic & Procedures**: [logic-procedures.md](logic-procedures.md)
- **Reporting Optimization**: [reporting-optimization.md](reporting-optimization.md)
- **Security & RBAC**: [security-rbac.md](security-rbac.md)
- **Style Guide**: [style-guide.md](style-guide.md)

---

## Database Design Principles

> **Learn to THINK, not copy SQL patterns.**

### ⚠️ Core Principle

- ASK user for database preferences when unclear
- Choose database/ORM based on CONTEXT
- Don't default to PostgreSQL for everything

### Decision Checklist

Before designing schema:

- [ ] Asked user about database preference?
- [ ] Chosen database for THIS context?
- [ ] Considered deployment environment?
- [ ] Planned index strategy?
- [ ] Defined relationship types?

### Anti-Patterns

❌ Default to PostgreSQL for simple apps (SQLite may suffice)
❌ Skip indexing
❌ Use SELECT * in production
❌ Store JSON when structured data is better
❌ Ignore N+1 queries

---

## Specialized Extensions

For specific technologies, use these skills if available:
- **Vector DB**: `lancedb`
- **Supabase**: `supabase-postgres-best-practices`, `supabase-auth`
- **NoSQL**: `nosql-expert`
- **Prisma**: `backend-dev-guidelines` (includes Prisma patterns)
