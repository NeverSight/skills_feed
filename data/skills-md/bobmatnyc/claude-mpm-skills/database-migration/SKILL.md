---
name: database-migration
description: Safe patterns for evolving database schemas in production with decision trees and troubleshooting guidance.
updated_at: 2025-12-03T00:00:00Z
tags: [database, migration, schema, production, decision-trees, troubleshooting, zero-downtime]
progressive_disclosure:
  entry_point:
    summary: "Safe patterns for evolving database schemas in production with decision trees and troubleshooting guidance."
    when_to_use: "When working with data, databases, or data transformations."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
  references:
    - decision-trees.md
    - troubleshooting.md
---
# Database Migration

Safe patterns for evolving database schemas in production.

## Migration Principles

1. **Backward compatible** - New code works with old schema
2. **Reversible** - Can rollback if needed
3. **Tested** - Verify on staging before production
4. **Incremental** - Small changes, not big-bang
5. **Zero downtime** - No service interruption

## Safe Migration Pattern

### Phase 1: Add New (Compatible)
```sql
-- Add new column (nullable initially)
ALTER TABLE users ADD COLUMN full_name VARCHAR(255) NULL;

-- Deploy new code that writes to both old and new
UPDATE users SET full_name = CONCAT(first_name, ' ', last_name);
```

### Phase 2: Migrate Data
```sql
-- Backfill existing data
UPDATE users
SET full_name = CONCAT(first_name, ' ', last_name)
WHERE full_name IS NULL;
```

### Phase 3: Make Required
```sql
-- Make column required
ALTER TABLE users ALTER COLUMN full_name SET NOT NULL;
```

### Phase 4: Remove Old (After New Code Deployed)
```sql
-- Remove old columns
ALTER TABLE users DROP COLUMN first_name;
ALTER TABLE users DROP COLUMN last_name;
```

## Common Migrations

### Adding Index
```sql
-- Create index concurrently (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### Renaming Column
```sql
-- Phase 1: Add new column
ALTER TABLE users ADD COLUMN email_address VARCHAR(255);

-- Phase 2: Copy data
UPDATE users SET email_address = email;

-- Phase 3: Drop old column (after deploy)
ALTER TABLE users DROP COLUMN email;
```

### Changing Column Type
```sql
-- Phase 1: Add new column with new type
ALTER TABLE products ADD COLUMN price_cents INTEGER;

-- Phase 2: Migrate data
UPDATE products SET price_cents = CAST(price * 100 AS INTEGER);

-- Phase 3: Drop old column
ALTER TABLE products DROP COLUMN price;
ALTER TABLE products RENAME COLUMN price_cents TO price;
```

### Adding Foreign Key
```sql
-- Add column first
ALTER TABLE orders ADD COLUMN user_id INTEGER NULL;

-- Populate data
UPDATE orders SET user_id = (
    SELECT id FROM users WHERE users.email = orders.user_email
);

-- Add foreign key
ALTER TABLE orders
ADD CONSTRAINT fk_orders_users
FOREIGN KEY (user_id) REFERENCES users(id);
```

## Migration Tools

### Python (Alembic)
```python
# Generate migration
alembic revision --autogenerate -m "add user full_name"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### JavaScript (Knex)
```javascript
// Create migration
knex migrate:make add_full_name

// Apply migrations
knex migrate:latest

// Rollback
knex migrate:rollback
```

### Rails
```ruby
# Generate migration
rails generate migration AddFullNameToUsers full_name:string

# Run migrations
rails db:migrate

# Rollback
rails db:rollback
```

## Testing Migrations

```python
def test_migration_forward_backward():
    # Apply migration
    apply_migration("add_full_name")

    # Verify schema
    assert column_exists("users", "full_name")

    # Rollback
    rollback_migration()

    # Verify rollback
    assert not column_exists("users", "full_name")
```

## Dangerous Operations

### ❌ Avoid in Production
```sql
-- Locks table for long time
ALTER TABLE users ADD COLUMN email VARCHAR(255) NOT NULL;

-- Can't rollback
DROP TABLE old_users;

-- Breaks existing code immediately
ALTER TABLE users DROP COLUMN email;
```

### ✅ Safe Alternatives
```sql
-- Add as nullable first
ALTER TABLE users ADD COLUMN email VARCHAR(255) NULL;

-- Rename instead of drop
ALTER TABLE old_users RENAME TO archived_users;

-- Keep old column until new code deployed
-- (multi-phase approach)
```

## Rollback Strategy

```sql
-- Every migration needs DOWN
-- UP
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- DOWN
ALTER TABLE users DROP COLUMN full_name;
```

## Decision Support

### Quick Decision Guide

**Making a schema change?**
- Breaking change (drops/modifies data) → Multi-phase migration (expand-contract)
- Additive change (new columns/tables) → Single-phase migration
- Large table (millions of rows) → Use CONCURRENTLY for indexes

**Need zero downtime?**
- Schema change → Expand-contract pattern (5 phases)
- Data migration (< 10k rows) → Synchronous in-migration
- Data migration (> 1M rows) → Background worker pattern

**Planning rollback?**
- Added new schema only → Simple DOWN migration
- Modified/removed schema → Multi-phase rollback or fix forward
- Cannot lose data → Point-in-time recovery (PITR)

**Choosing migration tool?**
- Python/Django → Django Migrations
- Python/SQLAlchemy → Alembic
- Node.js/TypeScript → Prisma Migrate or Knex.js
- Enterprise/multi-language → Flyway or Liquibase

**→ See [references/decision-trees.md](./references/decision-trees.md) for comprehensive decision frameworks**

## Troubleshooting

### Common Issues Quick Reference

**Migration failed halfway** → Check database state, fix forward with repair migration

**Schema drift detected** → Use autogenerate to create reconciliation migration

**Cannot rollback (no downgrade)** → Create reverse migration or fix forward

**Foreign key violation** → Clean data before adding constraint, or add as NOT VALID

**Migration locks table too long** → Use CONCURRENTLY, add columns in phases, batch updates

**Circular dependency** → Create merge migration or reorder dependencies

**→ See [references/troubleshooting.md](./references/troubleshooting.md) for detailed solutions with examples**

## Navigation

### Detailed References

- **[🌳 Decision Trees](./references/decision-trees.md)** - Schema migration strategies, zero-downtime patterns, rollback strategies, migration tool selection, and data migration approaches. Load when planning migrations or choosing strategies.

- **[🔧 Troubleshooting](./references/troubleshooting.md)** - Failed migration recovery, schema drift detection, migration conflicts, rollback failures, data integrity issues, and performance problems. Load when debugging migration issues.

## Remember
- Test migrations on copy of production data
- Have rollback plan ready
- Monitor during deployment
- Communicate with team about schema changes
- Keep migrations small and focused
