---
name: db
description: Database operations for SQLite, PostgreSQL, and MySQL. Use for queries, schema inspection, migrations, and AI-assisted query generation.
---

# Database Manager

Query and manage databases across SQLite, PostgreSQL, and MySQL.

## Prerequisites

Install database CLIs as needed:

```bash
# SQLite (usually pre-installed on macOS/Linux)
sqlite3 --version

# PostgreSQL
brew install postgresql
# or
apt install postgresql-client

# MySQL
brew install mysql-client
# or
apt install mysql-client
```

## CLI Reference

### SQLite

```bash
# Connect to database
sqlite3 database.db

# Execute query
sqlite3 database.db "SELECT * FROM users LIMIT 10"

# Output as CSV
sqlite3 -csv database.db "SELECT * FROM users"

# Output as JSON (requires sqlite 3.33+)
sqlite3 -json database.db "SELECT * FROM users"

# Column headers
sqlite3 -header database.db "SELECT * FROM users"

# Execute SQL file
sqlite3 database.db < queries.sql

# Schema commands
sqlite3 database.db ".schema"
sqlite3 database.db ".tables"
sqlite3 database.db ".schema users"
```

### PostgreSQL

```bash
# Connect
psql postgresql://user:pass@host:5432/dbname

# Execute query
psql -c "SELECT * FROM users LIMIT 10" postgresql://...

# Tuples only (no headers)
psql -t -c "SELECT count(*) FROM users" postgresql://...

# No alignment (machine-readable)
psql -t -A -c "SELECT id,name FROM users" postgresql://...

# Execute SQL file
psql -f queries.sql postgresql://...

# List tables
psql -c "\dt" postgresql://...

# Describe table
psql -c "\d users" postgresql://...

# Output format
psql -c "SELECT * FROM users" --csv postgresql://...
psql -c "SELECT * FROM users" --html postgresql://...
```

### MySQL

```bash
# Connect
mysql -h host -u user -p dbname

# Execute query
mysql -h host -u user -p -e "SELECT * FROM users LIMIT 10" dbname

# Batch mode (no headers)
mysql -h host -u user -p -B -e "SELECT * FROM users" dbname

# Execute SQL file
mysql -h host -u user -p dbname < queries.sql

# Show tables
mysql -h host -u user -p -e "SHOW TABLES" dbname

# Describe table
mysql -h host -u user -p -e "DESCRIBE users" dbname
```

## Common Operations

### Schema Inspection

#### SQLite
```bash
# All tables
sqlite3 db.sqlite ".tables"

# Table schema
sqlite3 db.sqlite ".schema tablename"

# All schemas
sqlite3 db.sqlite ".schema"
```

#### PostgreSQL
```bash
# All tables
psql -c "\dt" $DATABASE_URL

# Table schema
psql -c "\d tablename" $DATABASE_URL

# Table with indexes
psql -c "\d+ tablename" $DATABASE_URL
```

#### MySQL
```bash
# All tables
mysql -e "SHOW TABLES" -h host -u user -p dbname

# Table schema
mysql -e "DESCRIBE tablename" -h host -u user -p dbname

# Create statement
mysql -e "SHOW CREATE TABLE tablename" -h host -u user -p dbname
```

### Query Explanation

```bash
# SQLite
sqlite3 db.sqlite "EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'x'"

# PostgreSQL
psql -c "EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'x'" $DATABASE_URL

# MySQL
mysql -e "EXPLAIN SELECT * FROM users WHERE email = 'x'" dbname
```

### Data Export

```bash
# SQLite to CSV
sqlite3 -csv -header db.sqlite "SELECT * FROM users" > users.csv

# PostgreSQL to CSV
psql -c "\COPY users TO 'users.csv' CSV HEADER" $DATABASE_URL

# MySQL to CSV
mysql -e "SELECT * FROM users" -B dbname | tr '\t' ',' > users.csv
```

## AI-Assisted Query Generation

Use Gemini to help write queries:

```bash
# Describe what you want
gemini -m pro -o text -e "" "Write a SQL query to:
- Find all users who signed up in the last 30 days
- Who have made at least one purchase
- Order by purchase count descending

Table schemas:
- users (id, email, created_at)
- purchases (id, user_id, amount, created_at)

Output PostgreSQL-compatible SQL."
```

### Safe Query Review

```bash
# Generate query
QUERY=$(gemini -m pro -o text -e "" "Write SQL for: [your request]")

# Review before executing
echo "Generated query:"
echo "$QUERY"

# Then execute if safe
# psql -c "$QUERY" $DATABASE_URL
```

## Migration Patterns

### Schema Changes
```bash
# Create migration file
cat > migrations/001_add_column.sql << 'EOF'
ALTER TABLE users ADD COLUMN status VARCHAR(50) DEFAULT 'active';
EOF

# Apply migration
psql -f migrations/001_add_column.sql $DATABASE_URL
```

### Safe Migration Workflow
```bash
# 1. Test on copy first
createdb test_migration
pg_dump $DATABASE_URL | psql test_migration

# 2. Run migration on test
psql -f migration.sql test_migration

# 3. Verify
psql -c "\d tablename" test_migration

# 4. Apply to production
psql -f migration.sql $DATABASE_URL

# 5. Cleanup
dropdb test_migration
```

## Environment Variables

Store connection strings securely:

```bash
# .env file (don't commit!)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SQLITE_DB=./data/app.db

# Usage
psql $DATABASE_URL
sqlite3 $SQLITE_DB
```

## Best Practices

1. **Never hardcode credentials** - Use environment variables
2. **Review AI-generated queries** - Before executing
3. **Use EXPLAIN** - Check query performance
4. **Test migrations** - On copy before production
5. **Backup before changes** - Especially destructive ones
6. **Use transactions** - For multi-statement changes
7. **Limit results** - Always use LIMIT during exploration
