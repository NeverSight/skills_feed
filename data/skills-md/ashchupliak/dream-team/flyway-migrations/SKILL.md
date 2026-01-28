---
name: flyway-migrations
description: Flyway database migrations - use for schema changes, data migrations, version management, and PostgreSQL DDL
---

# Flyway Migration Patterns

## Naming Convention

```
V{version}__{description}.sql

Examples:
V001__create_environment_table.sql
V002__add_status_column.sql
V003__create_index_on_name.sql
V010__add_labels_jsonb.sql
V011__data_migration_normalize_status.sql
```

**Rules:**
- Version: Padded numbers (001, 002... or 1.0.0, 1.0.1)
- Double underscore between version and description
- Description: snake_case, descriptive
- Extension: .sql

## Basic Table Creation

```sql
-- V001__create_environment_table.sql
CREATE TABLE environment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    owner_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT uk_environment_name UNIQUE (name),
    CONSTRAINT fk_environment_owner FOREIGN KEY (owner_id)
        REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_environment_status ON environment(status);
CREATE INDEX idx_environment_owner_id ON environment(owner_id);
CREATE INDEX idx_environment_created_at ON environment(created_at DESC);

-- Comments
COMMENT ON TABLE environment IS 'Orca development environments';
COMMENT ON COLUMN environment.status IS 'PENDING, RUNNING, STOPPED, FAILED';
```

## Adding Columns

```sql
-- V002__add_labels_to_environment.sql
ALTER TABLE environment
ADD COLUMN labels JSONB NOT NULL DEFAULT '{}';

-- Add GIN index for JSONB queries
CREATE INDEX idx_environment_labels ON environment USING GIN (labels);

-- Add specific key index if frequently queried
CREATE INDEX idx_environment_labels_team ON environment ((labels->>'team'));
```

## Safe Column Modifications

```sql
-- V003__change_description_length.sql
-- Safe: increasing length
ALTER TABLE environment
ALTER COLUMN description TYPE VARCHAR(2000);

-- V004__make_description_not_null.sql
-- First: set default for existing nulls
UPDATE environment SET description = '' WHERE description IS NULL;
-- Then: add constraint
ALTER TABLE environment
ALTER COLUMN description SET NOT NULL,
ALTER COLUMN description SET DEFAULT '';
```

## Enum-like Columns

```sql
-- V005__add_environment_type.sql
-- Option 1: VARCHAR with CHECK constraint
ALTER TABLE environment
ADD COLUMN type VARCHAR(20) NOT NULL DEFAULT 'STANDARD'
    CONSTRAINT chk_environment_type
    CHECK (type IN ('STANDARD', 'PREMIUM', 'ENTERPRISE'));

-- Option 2: PostgreSQL ENUM type
CREATE TYPE environment_type AS ENUM ('STANDARD', 'PREMIUM', 'ENTERPRISE');
ALTER TABLE environment ADD COLUMN type environment_type NOT NULL DEFAULT 'STANDARD';
```

## Data Migrations

```sql
-- V006__migrate_status_values.sql
-- Normalize status values
UPDATE environment
SET status = CASE
    WHEN status IN ('pending', 'Pending', 'PENDING') THEN 'PENDING'
    WHEN status IN ('running', 'Running', 'RUNNING', 'active') THEN 'RUNNING'
    WHEN status IN ('stopped', 'Stopped', 'STOPPED', 'inactive') THEN 'STOPPED'
    WHEN status IN ('failed', 'Failed', 'FAILED', 'error') THEN 'FAILED'
    ELSE 'PENDING'
END
WHERE status NOT IN ('PENDING', 'RUNNING', 'STOPPED', 'FAILED');
```

## Creating Related Tables

```sql
-- V007__create_environment_tag_table.sql
CREATE TABLE environment_tag (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    environment_id UUID NOT NULL,
    key VARCHAR(100) NOT NULL,
    value VARCHAR(500) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_tag_environment FOREIGN KEY (environment_id)
        REFERENCES environment(id) ON DELETE CASCADE,
    CONSTRAINT uk_tag_env_key UNIQUE (environment_id, key)
);

CREATE INDEX idx_tag_environment_id ON environment_tag(environment_id);
CREATE INDEX idx_tag_key_value ON environment_tag(key, value);
```

## Idempotent Migrations

```sql
-- V008__add_column_if_not_exists.sql
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'environment' AND column_name = 'region'
    ) THEN
        ALTER TABLE environment ADD COLUMN region VARCHAR(50);
    END IF;
END $$;

-- Create index if not exists
CREATE INDEX IF NOT EXISTS idx_environment_region ON environment(region);

-- Create table if not exists
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
```

## Dropping Columns Safely

```sql
-- V009__remove_deprecated_column.sql
-- Step 1: Remove any defaults/constraints first
ALTER TABLE environment ALTER COLUMN legacy_field DROP DEFAULT;
ALTER TABLE environment DROP CONSTRAINT IF EXISTS chk_legacy_field;

-- Step 2: Drop dependent indexes
DROP INDEX IF EXISTS idx_environment_legacy;

-- Step 3: Drop the column
ALTER TABLE environment DROP COLUMN IF EXISTS legacy_field;
```

## Performance-Sensitive Migrations

```sql
-- V010__add_index_concurrently.sql
-- CONCURRENTLY prevents table locks (requires no transaction)
-- Add to flyway.conf: flyway.postgresql.transactional.lock=false

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_environment_name_lower
ON environment (LOWER(name));

-- For large data updates, batch them
-- V011__batch_update_large_table.sql
DO $$
DECLARE
    batch_size INT := 10000;
    affected INT;
BEGIN
    LOOP
        UPDATE environment
        SET normalized_name = LOWER(TRIM(name))
        WHERE normalized_name IS NULL
        LIMIT batch_size;

        GET DIAGNOSTICS affected = ROW_COUNT;
        EXIT WHEN affected = 0;

        COMMIT;
        PERFORM pg_sleep(0.1); -- Small pause to reduce load
    END LOOP;
END $$;
```

## Rollback Migrations (Undo)

```sql
-- U010__undo_add_region.sql (Flyway Teams/Enterprise)
ALTER TABLE environment DROP COLUMN IF EXISTS region;
DROP INDEX IF EXISTS idx_environment_region;
```

## Gradle Configuration

```kotlin
// build.gradle.kts
plugins {
    id("org.flywaydb.flyway") version "11.11.2"
}

flyway {
    url = "jdbc:postgresql://localhost:5432/orca"
    user = System.getenv("DB_USER") ?: "orca"
    password = System.getenv("DB_PASSWORD") ?: "orca"
    schemas = arrayOf("public")
    locations = arrayOf("classpath:db/migration")
    cleanDisabled = true // Prevent accidental clean in production
    validateMigrationNaming = true
}

tasks.named("flywayMigrate") {
    dependsOn("processResources")
}
```

## Best Practices

1. **Never modify applied migrations** - Create new ones instead
2. **Test migrations** - Run against a copy of production data
3. **Keep migrations small** - One logical change per migration
4. **Use transactions** - Flyway wraps each migration in a transaction
5. **Document** - Add comments explaining why, not just what
6. **Version carefully** - Use consistent numbering scheme
7. **Handle nulls** - Set defaults before adding NOT NULL
8. **Index wisely** - Consider CONCURRENTLY for large tables
