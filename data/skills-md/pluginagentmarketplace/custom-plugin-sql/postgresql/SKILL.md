---
name: postgresql
description: PostgreSQL administration and setup including installation, configuration, backup/recovery, replication, and high-availability. Learn production PostgreSQL operations.
sasmp_version: "1.3.0"
bonded_agent: 02-postgresql-dba
bond_type: PRIMARY_BOND
---

# PostgreSQL Administration

## Installation & Setup

```bash
# On Linux (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# On macOS
brew install postgresql@15

# Docker installation
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Connection Basics

```bash
# Connect to default database
psql -U postgres

# Connect to specific database
psql -U postgres -d mydb -h localhost -p 5432

# List databases
\l

# List tables in current database
\dt

# Get table info
\d table_name

# Quit psql
\q
```

## User & Role Management

```sql
-- Create a new role
CREATE ROLE developer WITH LOGIN PASSWORD 'secure_password';

-- Create superuser role
CREATE ROLE admin WITH SUPERUSER LOGIN PASSWORD 'admin_password';

-- Grant privileges on database
GRANT CONNECT ON DATABASE mydb TO developer;

-- Grant privileges on schema
GRANT USAGE ON SCHEMA public TO developer;

-- Grant privileges on tables
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO developer;

-- Grant privileges on specific table
GRANT SELECT ON employees TO developer;

-- Make role a database owner
ALTER DATABASE mydb OWNER TO developer;

-- Revoke privileges
REVOKE INSERT, UPDATE ON employees FROM developer;

-- Drop role
DROP ROLE developer;
```

## Configuration & Tuning

```bash
# PostgreSQL configuration file
sudo nano /etc/postgresql/15/main/postgresql.conf

# Key configuration parameters:

# Memory
shared_buffers = 256MB          # 25% of RAM for dedicated server
effective_cache_size = 1GB      # 50-75% of RAM
work_mem = 64MB                 # RAM per operation

# Connections
max_connections = 200
superuser_reserved_connections = 3

# Write-Ahead Log
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64

# Query planning
random_page_cost = 1.1          # For SSD
log_min_duration_statement = 1000  # Log slow queries
```

## Backup & Recovery

```bash
# Full database backup (text format)
pg_dump -U postgres -d mydb -f mydb_backup.sql

# Binary backup (faster, compressed)
pg_dump -U postgres -d mydb -Fc -f mydb_backup.dump

# Backup specific table
pg_dump -U postgres -d mydb -t employees -f employees_backup.sql

# Backup all databases
pg_dumpall -U postgres -f all_databases.sql

# Restore from backup
psql -U postgres -d mydb -f mydb_backup.sql

# Restore from binary dump
pg_restore -U postgres -d mydb mydb_backup.dump
```

## Maintenance Operations

```sql
-- VACUUM (reclaim space)
VACUUM;                    -- Full vacuum

-- VACUUM ANALYZE (reclaim space & update stats)
VACUUM ANALYZE;

-- ANALYZE (update table statistics)
ANALYZE;

-- Check database integrity
REINDEX DATABASE mydb;

-- Show database size
SELECT pg_database.datname,
       pg_size_pretty(pg_database_size(pg_database.datname))
FROM pg_database;

-- Show table sizes
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname != 'pg_catalog'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Monitoring

```sql
-- Active connections
SELECT * FROM pg_stat_activity WHERE state != 'idle';

-- Database statistics
SELECT * FROM pg_stat_database WHERE datname = 'mydb';

-- Table statistics
SELECT * FROM pg_stat_user_tables;

-- Index statistics
SELECT * FROM pg_stat_user_indexes;

-- Cache hit ratio
SELECT
  sum(heap_blks_read) as heap_read,
  sum(heap_blks_hit) as heap_hit,
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;
```

## Performance Tuning

```sql
-- Check slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

-- Find unused indexes
SELECT schemaname, tablename, indexname
FROM pg_stat_user_indexes
WHERE idx_scan = 0;

-- Find missing indexes
SELECT * FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
AND n_live_tup > 1000;

-- Analyze query plan
EXPLAIN ANALYZE
SELECT * FROM employees WHERE salary > 50000;
```

## Replication Setup

```bash
# On primary server - enable replication in postgresql.conf
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64

# Create replication user
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'rep_password';

# On standby - base backup from primary
pg_basebackup -h primary_host -D /var/lib/postgresql/15/main -U replicator -v -P -W

# Create recovery.conf on standby
standby_mode = 'on'
primary_conninfo = 'host=primary_host port=5432 user=replicator password=password'
```

## High Availability with pgBouncer

```bash
# Install pgBouncer
sudo apt-get install pgbouncer

# Configuration - /etc/pgbouncer/pgbouncer.ini
[databases]
mydb = host=primary_host port=5432 dbname=mydb

[pgbouncer]
listen_port = 6432
max_client_conn = 1000
default_pool_size = 25
reserve_pool_size = 5
```

## Next Steps

Learn advanced security features including row-level security and SSL/TLS configuration in the `postgresql-security` skill.
