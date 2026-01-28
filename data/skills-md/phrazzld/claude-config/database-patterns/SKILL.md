---
name: database-patterns
description: |
  Database operations: migrations, queries, transactions, and performance. Use when:
  - Writing database migrations
  - Optimizing queries or adding indexes
  - Managing transactions and connections
  - Setting up connection pooling
  - Designing audit logging
  Keywords: database, migration, SQL, query optimization, index, transaction,
  connection pool, N+1, ORM, audit log
---

# Database Patterns

Forward-only migrations, explicit transactions, measured optimization.

## Migrations

**Forward-only. No rollbacks. Maintain backward compatibility:**
```sql
-- Add nullable column (backward compatible)
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Later: make required after backfill
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
```

**Break large changes into smaller steps. Use feature flags during transitions.**

## Query Optimization

**Always check execution plans before optimizing:**
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

**Index based on actual query patterns:**
```sql
-- Composite for common query
CREATE INDEX idx_orders_user_date ON orders (user_id, created_at DESC);

-- Partial for filtered queries
CREATE INDEX idx_orders_pending ON orders (status) WHERE status = 'pending';
```

**Monitor unused indexes. Remove if `idx_scan < 100`.**

## N+1 Prevention

**Always eager load in loops:**
```python
# Good
users = User.query.options(joinedload(User.posts)).all()

# Bad (N+1)
users = User.query.all()
for user in users:
    print(user.posts)  # N queries!
```

## Transactions

**Scope to single business operation. Keep short:**
```python
async with db.transaction():
    order = await create_order(data)
    await update_inventory(order.items)
    # Commit on exit

# OUTSIDE transaction: send emails, call external APIs
await send_confirmation(order)
```

**Never hold transactions during external calls.**

## Connection Pooling

```python
# Size based on measured peak concurrency
create_engine(
    url,
    pool_size=15,      # Based on load testing
    max_overflow=5,    # Burst capacity
    pool_timeout=30,   # Fail fast
    pool_recycle=3600, # Prevent stale connections
    pool_pre_ping=True # Validate before use
)
```

**Monitor utilization. Alert at 80%.**

## Data Validation

**Validate at boundaries, not just in database:**
```python
# Validate input before INSERT
validated = CreateUserSchema.parse(input)
if await email_exists(validated.email):
    raise ValidationError("Email taken")

# Validate output after retrieval (detect corruption)
return UserOutputSchema.parse(row)
```

## Anti-Patterns

- Rollback migrations (use forward-only)
- Indexes without query pattern analysis
- N+1 queries in loops
- Long-running transactions with external calls
- Relying only on DB constraints for validation
- Default pool settings without measurement

## References

- [audit-logging.md](references/audit-logging.md) - Immutable audit trails
