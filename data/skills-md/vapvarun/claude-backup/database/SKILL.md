---
name: database
description: Database design, optimization, and management for SQL and NoSQL databases. Covers schema design, indexing, query optimization, migrations, and database best practices. Use when designing database schemas, optimizing queries, troubleshooting database performance, or implementing data models.
---

# Database Development

Schema design, optimization, and management best practices.

## Schema Design

### Normalization

```sql
-- 1NF: Atomic values, no repeating groups
-- BAD
CREATE TABLE orders (
    id INT,
    products VARCHAR(255)  -- "shirt,pants,shoes" - NOT atomic
);

-- GOOD
CREATE TABLE orders (id INT PRIMARY KEY);
CREATE TABLE order_items (
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT
);

-- 2NF: No partial dependencies (all non-key columns depend on entire PK)
-- 3NF: No transitive dependencies (non-key columns don't depend on other non-key columns)
```

### Data Types

```sql
-- Use appropriate types
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- BIGINT for large tables
    uuid CHAR(36) NOT NULL UNIQUE,                  -- Fixed-length UUID
    email VARCHAR(255) NOT NULL,                    -- Variable length
    status ENUM('active', 'inactive', 'banned'),    -- Constrained values
    balance DECIMAL(10,2) NOT NULL DEFAULT 0,       -- Exact precision for money
    metadata JSON,                                   -- Flexible schema
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- PostgreSQL specific
CREATE TABLE events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    data JSONB NOT NULL,                            -- Binary JSON, indexable
    tags TEXT[] NOT NULL DEFAULT '{}',              -- Array type
    tsv TSVECTOR,                                   -- Full-text search
    created_at TIMESTAMPTZ DEFAULT NOW()            -- Timezone-aware
);
```

### Relationships

```sql
-- One-to-Many
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL
);

-- Many-to-Many with pivot table
CREATE TABLE post_tags (
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (post_id, tag_id)
);

-- One-to-One
CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    bio TEXT,
    avatar_url VARCHAR(255)
);
```

## Indexing

### Index Types

```sql
-- B-Tree (default, most common)
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- Good for: WHERE user_id = ? AND status = ?
-- Good for: WHERE user_id = ?
-- NOT good for: WHERE status = ?  (leftmost prefix rule)

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Partial index (PostgreSQL)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Full-text index (MySQL)
CREATE FULLTEXT INDEX idx_posts_content ON posts(title, content);

-- GIN index for JSONB (PostgreSQL)
CREATE INDEX idx_events_data ON events USING GIN(data);
```

### Index Strategy

```sql
-- Index columns used in:
-- 1. WHERE clauses
-- 2. JOIN conditions
-- 3. ORDER BY (if used frequently)
-- 4. Foreign keys

-- Check existing indexes
SHOW INDEX FROM orders;  -- MySQL
\d orders               -- PostgreSQL

-- Analyze query execution
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

## Query Optimization

### EXPLAIN Analysis

```sql
-- MySQL
EXPLAIN SELECT * FROM orders
WHERE user_id = 123
AND created_at > '2024-01-01';

-- Look for:
-- type: "ref" or "range" (good), "ALL" (table scan, bad)
-- key: Which index is used (NULL = no index)
-- rows: Estimated rows examined

-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123;
```

### Common Optimizations

```sql
-- BAD: SELECT *
SELECT * FROM users WHERE id = 1;

-- GOOD: Select only needed columns
SELECT id, name, email FROM users WHERE id = 1;

-- BAD: OR can prevent index usage
SELECT * FROM users WHERE email = 'a@b.com' OR name = 'John';

-- GOOD: Use UNION for OR conditions
SELECT * FROM users WHERE email = 'a@b.com'
UNION ALL
SELECT * FROM users WHERE name = 'John' AND email != 'a@b.com';

-- BAD: Functions on indexed columns
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- GOOD: Use range
SELECT * FROM users
WHERE created_at >= '2024-01-01'
AND created_at < '2025-01-01';

-- BAD: LIKE with leading wildcard
SELECT * FROM products WHERE name LIKE '%shirt%';

-- GOOD: Full-text search
SELECT * FROM products
WHERE MATCH(name) AGAINST('shirt' IN BOOLEAN MODE);
```

### N+1 Problem

```sql
-- BAD: N+1 queries
-- Query 1: SELECT * FROM posts LIMIT 10
-- Query 2-11: SELECT * FROM users WHERE id = ?  (for each post)

-- GOOD: JOIN
SELECT p.*, u.name as author_name
FROM posts p
JOIN users u ON p.user_id = u.id
LIMIT 10;

-- GOOD: Subquery with IN
SELECT * FROM users
WHERE id IN (SELECT DISTINCT user_id FROM posts WHERE ...);
```

## Migrations

### Migration Best Practices

```sql
-- Always wrap in transactions
BEGIN;

-- Add column (non-locking in PostgreSQL)
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Add index concurrently (PostgreSQL, non-locking)
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);

-- Rename column safely
ALTER TABLE users RENAME COLUMN phone TO phone_number;

COMMIT;

-- Rollback script
BEGIN;
ALTER TABLE users DROP COLUMN phone_number;
DROP INDEX idx_users_phone;
COMMIT;
```

### Safe Migration Patterns

```sql
-- Adding NOT NULL column with default
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN status VARCHAR(20);

-- Step 2: Backfill data
UPDATE users SET status = 'active' WHERE status IS NULL;

-- Step 3: Add NOT NULL constraint
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';

-- Renaming tables (zero downtime)
-- Step 1: Create new table
CREATE TABLE accounts (LIKE users INCLUDING ALL);

-- Step 2: Copy data
INSERT INTO accounts SELECT * FROM users;

-- Step 3: Create triggers for sync
-- Step 4: Switch application
-- Step 5: Drop old table
```

## Performance

### Connection Pooling

```javascript
// Node.js with pg-pool
const { Pool } = require('pg');

const pool = new Pool({
    host: 'localhost',
    database: 'myapp',
    max: 20,                    // Max connections
    idleTimeoutMillis: 30000,   // Close idle connections
    connectionTimeoutMillis: 2000
});

// Always use pool, not direct connections
const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### Pagination

```sql
-- BAD: OFFSET for large datasets
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 10000;
-- Gets slower as offset increases

-- GOOD: Cursor-based pagination
SELECT * FROM posts
WHERE created_at < '2024-01-15 10:30:00'
ORDER BY created_at DESC
LIMIT 20;

-- GOOD: Keyset pagination with ID
SELECT * FROM posts
WHERE (created_at, id) < ('2024-01-15 10:30:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

### Batch Operations

```sql
-- BAD: Many individual inserts
INSERT INTO logs (message) VALUES ('log1');
INSERT INTO logs (message) VALUES ('log2');
-- ... 1000 more

-- GOOD: Batch insert
INSERT INTO logs (message) VALUES
    ('log1'),
    ('log2'),
    ('log3');
    -- Up to ~1000 at a time

-- GOOD: COPY for bulk loading (PostgreSQL)
COPY logs (message) FROM '/path/to/file.csv' WITH CSV;
```

## Transactions

### ACID Properties

```sql
-- Atomicity: All or nothing
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- If any fails, ROLLBACK
COMMIT;

-- Isolation levels
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;  -- Default
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;   -- Strictest

-- Deadlock prevention: Always lock in same order
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- Lock row
SELECT * FROM accounts WHERE id = 2 FOR UPDATE;
-- Do work
COMMIT;
```

## NoSQL Patterns

### Document Database (MongoDB)

```javascript
// Schema design: Embed vs Reference
// Embed: Data accessed together, 1:few relationships
{
    _id: ObjectId("..."),
    title: "Blog Post",
    author: {                    // Embedded
        name: "John",
        email: "john@example.com"
    },
    comments: [                  // Embedded array
        { text: "Great!", user: "Jane" }
    ]
}

// Reference: Large documents, many relationships
{
    _id: ObjectId("..."),
    title: "Blog Post",
    author_id: ObjectId("...")   // Reference to users collection
}

// Indexes
db.posts.createIndex({ "author_id": 1 });
db.posts.createIndex({ "title": "text", "content": "text" });  // Text search
```

### Key-Value (Redis)

```bash
# Caching pattern
SET user:123 '{"name":"John"}' EX 3600  # Expires in 1 hour
GET user:123

# Counter
INCR page:views:homepage
GET page:views:homepage

# Rate limiting
INCR rate:ip:192.168.1.1
EXPIRE rate:ip:192.168.1.1 60  # Reset every minute
```

## Backup & Recovery

```bash
# MySQL
mysqldump -u root -p database > backup.sql
mysql -u root -p database < backup.sql

# PostgreSQL
pg_dump -Fc database > backup.dump
pg_restore -d database backup.dump

# Point-in-time recovery (PostgreSQL)
# Requires WAL archiving configured
pg_basebackup -D /backup/base -Fp -Xs -P
```

## Monitoring Queries

```sql
-- MySQL slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- Log queries > 1 second

-- PostgreSQL: Currently running queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;

-- Table sizes
SELECT
    table_name,
    pg_size_pretty(pg_total_relation_size(quote_ident(table_name)))
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC;
```
