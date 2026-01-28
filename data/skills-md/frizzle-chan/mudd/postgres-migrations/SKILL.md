---
name: postgres-migrations
description: Write safe PostgreSQL migrations that avoid blocking reads/writes. Use when creating migrations, adding columns, indexes, constraints, or modifying tables. Based on Squawk linter rules.
---

# Safe PostgreSQL Migrations

This skill helps you write migrations that avoid blocking reads/writes in production. Based on [Squawk](https://squawkhq.com/docs/rules) linter rules.

## Verifying Migrations

After writing a migration, verify it with the Squawk CLI:

```bash
uv run squawk migrations/your_migration.sql
```

This will catch unsafe patterns before they reach production.

## Quick Reference: Safe Patterns

| Operation | Unsafe | Safe |
|-----------|--------|------|
| Add column with default | `ADD COLUMN x INT DEFAULT 1 NOT NULL` (PG <11) | Add nullable, set default, backfill, then add NOT NULL |
| Add NOT NULL to existing column | `ALTER COLUMN x SET NOT NULL` | Add CHECK constraint NOT VALID, validate, then SET NOT NULL |
| Add foreign key | `ADD CONSTRAINT fk FOREIGN KEY...` | `ADD CONSTRAINT fk FOREIGN KEY... NOT VALID`, then `VALIDATE CONSTRAINT` |
| Add check constraint | `ADD CONSTRAINT chk CHECK(...)` | `ADD CONSTRAINT chk CHECK(...) NOT VALID`, then `VALIDATE CONSTRAINT` |
| Add unique constraint | `ADD CONSTRAINT uniq UNIQUE(x)` | `CREATE UNIQUE INDEX CONCURRENTLY`, then `ADD CONSTRAINT USING INDEX` |
| Create index | `CREATE INDEX idx ON t(x)` | `CREATE INDEX CONCURRENTLY idx ON t(x)` |
| Drop index | `DROP INDEX idx` | `DROP INDEX CONCURRENTLY idx` |
| Change column type | `ALTER COLUMN x TYPE bigint` | Create new column, trigger-sync, backfill, swap |

## Timeouts

Always set timeouts at the start of migrations:

```sql
SET lock_timeout = '2s';
SET statement_timeout = '30s';
```

## Adding Columns

### With Default Value (PG 11+)
Non-volatile defaults are safe on PostgreSQL 11+:

```sql
ALTER TABLE users ADD COLUMN active boolean DEFAULT true NOT NULL;
```

### With Default Value (PG <11 or volatile defaults)
```sql
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN created_at timestamptz;
ALTER TABLE users ALTER COLUMN created_at SET DEFAULT now();

-- Step 2: Backfill in batches
UPDATE users SET created_at = now() WHERE id BETWEEN 1 AND 10000;
-- ... repeat for all batches

-- Step 3: Add NOT NULL (see next section)
```

### Making Column NOT NULL

```sql
-- Step 1: Add NOT VALID constraint (fast, minimal locking)
ALTER TABLE users ADD CONSTRAINT users_email_not_null
  CHECK (email IS NOT NULL) NOT VALID;

-- Step 2: Validate (acquires lighter SHARE UPDATE EXCLUSIVE lock)
ALTER TABLE users VALIDATE CONSTRAINT users_email_not_null;

-- Step 3: Set NOT NULL (PG 12+ skips table scan due to existing constraint)
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- Step 4: Drop redundant constraint
ALTER TABLE users DROP CONSTRAINT users_email_not_null;
```

### Required Field (NOT NULL without default)

Never add a NOT NULL column without a default to a table with data. Instead:

```sql
-- Option A: Add with default
ALTER TABLE users ADD COLUMN role text NOT NULL DEFAULT 'member';

-- Option B: Add nullable, backfill, then constrain
ALTER TABLE users ADD COLUMN role text;
UPDATE users SET role = 'member' WHERE role IS NULL;
-- Then use the NOT NULL pattern above
```

## Constraints

### Foreign Key

```sql
-- Step 1: Add NOT VALID (fast)
ALTER TABLE orders ADD CONSTRAINT orders_user_fk
  FOREIGN KEY (user_id) REFERENCES users(id) NOT VALID;

-- Step 2: Validate in separate transaction
ALTER TABLE orders VALIDATE CONSTRAINT orders_user_fk;
```

### Check Constraint

```sql
-- Step 1: Add NOT VALID
ALTER TABLE accounts ADD CONSTRAINT positive_balance
  CHECK (balance >= 0) NOT VALID;

-- Step 2: Validate
ALTER TABLE accounts VALIDATE CONSTRAINT positive_balance;
```

### Unique Constraint

```sql
-- Step 1: Create index concurrently (allows reads/writes)
CREATE UNIQUE INDEX CONCURRENTLY users_email_idx ON users(email);

-- Step 2: Attach as constraint (fast)
ALTER TABLE users ADD CONSTRAINT users_email_uniq
  UNIQUE USING INDEX users_email_idx;
```

## Indexes

### Create Index

```sql
-- Always use CONCURRENTLY (outside transaction)
CREATE INDEX CONCURRENTLY users_email_idx ON users(email);
```

### Drop Index

```sql
DROP INDEX CONCURRENTLY users_email_idx;
```

### Concurrent Index in Transaction

`CREATE INDEX CONCURRENTLY` cannot run inside a transaction. For migration tools that auto-wrap in transactions:

```sql
COMMIT;
CREATE INDEX CONCURRENTLY users_email_idx ON users(email);
BEGIN;
```

## Changing Column Types

### Safe Conversions (no rewrite)
- `varchar(N)` to `text`
- `varchar(N)` to `varchar(M)` where M > N
- `numeric(P,S)` to `numeric(P2,S)` where P2 > P

### Unsafe Conversions (requires table rewrite)
For `int` to `bigint` or other incompatible types:

```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN id_new bigint;

-- Step 2: Create trigger to sync writes
CREATE FUNCTION sync_id_new() RETURNS trigger AS $$
BEGIN
  NEW.id_new := NEW.id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_id_new_trigger
  BEFORE INSERT OR UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION sync_id_new();

-- Step 3: Backfill in batches
UPDATE users SET id_new = id WHERE id BETWEEN 1 AND 10000;

-- Step 4: Swap columns (requires downtime or careful coordination)
```

## Destructive Operations

### Drop Column

**Risk**: Breaks clients still reading/writing the column.

**Safe process**:
1. Stop application code from using the column
2. Deploy code changes
3. Wait for all instances updated
4. Drop the column

### Drop Table

**Risk**: Breaks all clients using the table.

**Safe process**: Same as drop column - ensure no code references it first.

### Rename Column/Table

**Risk**: Breaks clients using the old name.

**Safer alternatives**:
1. Rename in ORM only, keep database name unchanged
2. For tables: create a view with new name, migrate code, then swap

```sql
-- View approach for table rename
CREATE VIEW user_favorites AS SELECT * FROM user_stars;
-- Deploy code using user_favorites
-- Then:
BEGIN;
DROP VIEW user_favorites;
ALTER TABLE user_stars RENAME TO user_favorites;
COMMIT;
```

## Type Preferences

### Use BIGINT over INT

```sql
-- Avoid (2B limit)
CREATE TABLE posts (id serial PRIMARY KEY);
CREATE TABLE posts (id int PRIMARY KEY);

-- Prefer (9 quintillion limit)
CREATE TABLE posts (id bigserial PRIMARY KEY);
CREATE TABLE posts (id bigint PRIMARY KEY);
```

### Use IDENTITY over SERIAL

```sql
-- Avoid (permission/schema issues)
CREATE TABLE posts (id bigserial PRIMARY KEY);

-- Prefer (SQL standard, better usability)
CREATE TABLE posts (id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY);
```

### Use TEXT over VARCHAR

```sql
-- Avoid (changing size requires ACCESS EXCLUSIVE lock)
CREATE TABLE users (email varchar(255));

-- Prefer (add check constraint for length)
CREATE TABLE users (email text);
ALTER TABLE users ADD CONSTRAINT email_length CHECK (length(email) <= 255);
```

### Use TIMESTAMPTZ over TIMESTAMP

```sql
-- Avoid (loses timezone info)
CREATE TABLE events (created_at timestamp);

-- Prefer (preserves timezone)
CREATE TABLE events (created_at timestamptz);
```

### Avoid CHAR

```sql
-- Avoid (pads with spaces, unexpected behavior)
CREATE TABLE t (code char(3));

-- Prefer
CREATE TABLE t (code text);
ALTER TABLE t ADD CONSTRAINT code_length CHECK (length(code) = 3);
```

## Idempotent Migrations

Use `IF EXISTS` / `IF NOT EXISTS` for retryable migrations:

```sql
-- Adding
ALTER TABLE users ADD COLUMN IF NOT EXISTS email text;
CREATE INDEX CONCURRENTLY IF NOT EXISTS users_email_idx ON users(email);

-- Removing
DROP INDEX CONCURRENTLY IF EXISTS users_email_idx;
DROP TABLE IF EXISTS old_users;
ALTER TABLE users DROP COLUMN IF EXISTS deprecated_col;
```

## Lock Types Reference

| Lock | Blocks | Common Operations |
|------|--------|-------------------|
| ACCESS EXCLUSIVE | All operations | `ALTER TABLE` (most), `DROP`, `TRUNCATE` |
| SHARE ROW EXCLUSIVE | Writes | `CREATE INDEX` (non-concurrent), `ADD FOREIGN KEY` |
| SHARE UPDATE EXCLUSIVE | Schema changes | `VALIDATE CONSTRAINT`, `CREATE INDEX CONCURRENTLY` |

## Alembic/SQLAlchemy Examples

### Concurrent Index

```python
from alembic import op

def upgrade():
    with op.get_context().autocommit_block():
        op.create_index(
            'users_email_idx',
            'users',
            ['email'],
            postgresql_concurrently=True,
        )
```

### NOT VALID Constraint

```python
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_check_constraint(
        'positive_balance',
        'accounts',
        'balance >= 0',
        postgresql_not_valid=True,
    )

def upgrade_validate():
    op.execute(sa.text('ALTER TABLE accounts VALIDATE CONSTRAINT positive_balance'))
```

### Foreign Key with NOT VALID

```python
from alembic import op

def upgrade():
    op.create_foreign_key(
        'orders_user_fk',
        'orders', 'users',
        ['user_id'], ['id'],
        postgresql_not_valid=True,
    )

def upgrade_validate():
    op.execute(sa.text('ALTER TABLE orders VALIDATE CONSTRAINT orders_user_fk'))
```
