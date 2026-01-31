---
name: database-migration-patterns
description: Database schema migration patterns and best practices. Use when creating database migrations, implementing zero-downtime schema changes, version control for databases, or managing data migrations.
---

# Database Migration Patterns

Best practices for safe database schema migrations.

## Migration File Structure

```
migrations/
├── versions/
│   ├── 001_initial_schema.py
│   ├── 002_add_users_table.py
│   ├── 003_add_user_email_index.py
│   └── 004_add_orders_table.py
├── alembic.ini
└── env.py
```

## Alembic Migration Template

```python
"""Add users table

Revision ID: 002
Revises: 001
Create Date: 2024-01-15 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )

    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_status', 'users', ['status'])


def downgrade() -> None:
    op.drop_index('ix_users_status')
    op.drop_index('ix_users_email')
    op.drop_table('users')
```

## Zero-Downtime Migration Patterns

### Pattern 1: Expand and Contract

```python
# Step 1: Add new column (nullable)
def upgrade_step1():
    op.add_column('users', sa.Column('email_new', sa.String(255), nullable=True))

# Step 2: Backfill data (run separately, possibly in batches)
def backfill():
    connection = op.get_bind()
    connection.execute("""
        UPDATE users
        SET email_new = email
        WHERE email_new IS NULL
        LIMIT 10000
    """)

# Step 3: Make new column non-nullable, drop old column
def upgrade_step3():
    op.alter_column('users', 'email_new', nullable=False)
    op.drop_column('users', 'email')
    op.alter_column('users', 'email_new', new_column_name='email')
```

### Pattern 2: Safe Column Rename

```python
# DON'T: Direct rename causes downtime
# op.alter_column('users', 'username', new_column_name='email')

# DO: Expand-Contract pattern
def upgrade():
    # 1. Add new column
    op.add_column('users', sa.Column('email', sa.String(255)))

    # 2. Create trigger to sync data (PostgreSQL)
    op.execute("""
        CREATE OR REPLACE FUNCTION sync_username_to_email()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.email = NEW.username;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER sync_username_email
        BEFORE INSERT OR UPDATE ON users
        FOR EACH ROW EXECUTE FUNCTION sync_username_to_email();
    """)

    # 3. Backfill existing data
    op.execute("UPDATE users SET email = username WHERE email IS NULL")

# Later migration after app updated:
def upgrade_cleanup():
    op.execute("DROP TRIGGER sync_username_email ON users")
    op.execute("DROP FUNCTION sync_username_to_email()")
    op.drop_column('users', 'username')
```

### Pattern 3: Safe Index Creation

```python
def upgrade():
    # Create index concurrently to avoid locking
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_users_email
        ON users (email)
    """)

def downgrade():
    op.execute("DROP INDEX CONCURRENTLY ix_users_email")
```

### Pattern 4: Adding NOT NULL Constraint

```python
def upgrade():
    # 1. Add column as nullable
    op.add_column('users', sa.Column('verified', sa.Boolean(), nullable=True))

    # 2. Set default for new rows
    op.alter_column('users', 'verified', server_default=sa.false())

    # 3. Backfill existing rows (in batches for large tables)
    op.execute("""
        UPDATE users
        SET verified = false
        WHERE verified IS NULL
    """)

    # 4. Add NOT NULL constraint
    op.alter_column('users', 'verified', nullable=False)
```

## Batch Processing for Large Tables

```python
from sqlalchemy import text

def backfill_in_batches(connection, batch_size=10000):
    """Backfill data in batches to avoid long locks."""
    while True:
        result = connection.execute(text("""
            UPDATE users
            SET new_column = old_column
            WHERE id IN (
                SELECT id FROM users
                WHERE new_column IS NULL
                LIMIT :batch_size
                FOR UPDATE SKIP LOCKED
            )
            RETURNING id
        """), {"batch_size": batch_size})

        updated = result.rowcount
        connection.commit()

        if updated == 0:
            break

        print(f"Updated {updated} rows")
        time.sleep(0.1)  # Small delay to reduce load
```

## Data Migration Patterns

### Separate Data Migrations

```python
# Schema migration (runs during deploy)
def upgrade():
    op.add_column('orders', sa.Column('total_cents', sa.BigInteger()))

# Data migration (runs separately)
# data_migrations/migrate_order_totals.py
def run_data_migration():
    """Convert total from dollars to cents."""
    with engine.connect() as conn:
        while True:
            result = conn.execute(text("""
                UPDATE orders
                SET total_cents = total * 100
                WHERE total_cents IS NULL
                AND id IN (
                    SELECT id FROM orders
                    WHERE total_cents IS NULL
                    LIMIT 5000
                )
            """))

            if result.rowcount == 0:
                break

            conn.commit()
```

## Foreign Key Constraints

### Safe Foreign Key Addition

```python
def upgrade():
    # 1. Add column without constraint
    op.add_column('orders',
        sa.Column('user_id', postgresql.UUID(), nullable=True)
    )

    # 2. Backfill data
    op.execute("""
        UPDATE orders o
        SET user_id = (
            SELECT id FROM users u
            WHERE u.legacy_id = o.legacy_user_id
        )
    """)

    # 3. Add constraint with NOT VALID (PostgreSQL)
    op.execute("""
        ALTER TABLE orders
        ADD CONSTRAINT fk_orders_user_id
        FOREIGN KEY (user_id) REFERENCES users(id)
        NOT VALID
    """)

    # 4. Validate constraint in background
    op.execute("""
        ALTER TABLE orders
        VALIDATE CONSTRAINT fk_orders_user_id
    """)
```

## Version Control Integration

```yaml
# CI/CD pipeline for migrations
name: Database Migration

on:
  push:
    paths:
      - 'migrations/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate migration
        run: |
          alembic check
          alembic upgrade head --sql > /dev/null

      - name: Check for destructive operations
        run: |
          # Fail if migration contains DROP without review
          if grep -r "op.drop" migrations/versions/*.py; then
            echo "::warning::Migration contains DROP operations"
          fi

  deploy-staging:
    needs: validate
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Run migration
        run: alembic upgrade head
```

## Rollback Strategies

```python
# Always implement downgrade
def downgrade():
    # For additive changes, downgrade is straightforward
    op.drop_column('users', 'new_column')

# For destructive changes, preserve data
def upgrade():
    # Rename instead of drop
    op.rename_table('old_table', '_old_table_backup')

def downgrade():
    op.rename_table('_old_table_backup', 'old_table')
```

## Testing Migrations

```python
# tests/test_migrations.py
import pytest
from alembic.config import Config
from alembic import command

@pytest.fixture
def alembic_config():
    config = Config("alembic.ini")
    return config

def test_upgrade_downgrade(alembic_config, test_database):
    """Test that all migrations can upgrade and downgrade."""
    # Upgrade to head
    command.upgrade(alembic_config, "head")

    # Downgrade to base
    command.downgrade(alembic_config, "base")

    # Upgrade again
    command.upgrade(alembic_config, "head")

def test_migration_is_reversible(alembic_config, test_database):
    """Test each migration individually."""
    revisions = get_all_revisions()

    for rev in revisions:
        command.upgrade(alembic_config, rev)
        command.downgrade(alembic_config, "-1")
        command.upgrade(alembic_config, rev)
```

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [Zero-Downtime Migrations](https://blog.cloudflare.com/why-we-use-postgresqls-advisory-locks/)
- [Safe Database Migrations](https://www.braintreepayments.com/blog/safe-operations-for-high-volume-postgresql/)
