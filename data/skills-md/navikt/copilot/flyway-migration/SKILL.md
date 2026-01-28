---
name: flyway-migration
description: Database migration patterns using Flyway with versioned SQL scripts
---

# Flyway Migration Skill

This skill provides patterns for managing database schema changes with Flyway.

## Migration File Naming

```text
db/migration/V{version}__{description}.sql
```

Examples:

- `V1__create_users_table.sql`
- `V2__add_email_to_users.sql`
- `V3__create_payments_table.sql`
- `V1.1__add_phone_to_users.sql`

## Creating Tables

```sql
-- V1__create_users_table.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Automatic updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## Adding Columns

```sql
-- V2__add_phone_to_users.sql
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);
CREATE INDEX idx_users_phone ON users(phone_number);
```

## Creating Indexes

```sql
-- V3__add_user_indexes.sql
CREATE INDEX CONCURRENTLY idx_users_created_at ON users(created_at DESC);
CREATE INDEX CONCURRENTLY idx_users_name ON users(name);
```

## Adding Foreign Keys

```sql
-- V4__create_orders_table.sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
```

## Data Migrations

```sql
-- V5__set_default_status.sql
UPDATE users
SET status = 'active'
WHERE status IS NULL;

ALTER TABLE users
ALTER COLUMN status SET NOT NULL;
```

## Kotlin Integration

```kotlin
import org.flywaydb.core.Flyway
import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource

fun createDataSource(jdbcUrl: String): HikariDataSource {
    val config = HikariConfig().apply {
        this.jdbcUrl = jdbcUrl
        username = System.getenv("DATABASE_USERNAME")
        password = System.getenv("DATABASE_PASSWORD")
        maximumPoolSize = 5
        minimumIdle = 1
        idleTimeout = 60000
        maxLifetime = 600000
    }

    return HikariDataSource(config)
}

fun runMigrations(dataSource: HikariDataSource) {
    Flyway.configure()
        .dataSource(dataSource)
        .locations("classpath:db/migration")
        .load()
        .migrate()
}

// In main()
fun main() {
    val dataSource = createDataSource(env.databaseUrl)
    runMigrations(dataSource)

    logger.info("Database migrations completed")
}
```

## Best Practices

1. **Never modify existing migrations**: Create a new migration instead
2. **Use CONCURRENTLY for indexes**: Avoid locking tables in production
3. **Test migrations on dev first**: Always test before production
4. **Keep migrations small**: One logical change per migration
5. **Use transactions**: Wrap changes in BEGIN/COMMIT when possible
6. **Add rollback notes**: Comment how to manually rollback if needed
