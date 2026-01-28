---
name: cloudflare-d1
description: |
  Build with D1 serverless SQLite database on Cloudflare's edge. Use when: creating databases, writing SQL migrations, querying D1 from Workers, handling relational data, or troubleshooting D1_ERROR, statement too long, migration failures, or query performance issues.
license: MIT
---

# Cloudflare D1 Database

**Status**: Production Ready ✅
**Last Updated**: 2025-11-23
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: wrangler@4.50.0, @cloudflare/workers-types@4.20251121.0

**Recent Updates (2025)**:
- **Nov 2025**: Jurisdiction support (data localization compliance), remote bindings GA (wrangler@4.37.0+), automatic resource provisioning
- **Sept 2025**: Automatic read-only query retries (up to 2 attempts), remote bindings public beta
- **July 2025**: Storage limits increased (250GB → 1TB), alpha backup access removed, REST API 50-500ms faster
- **May 2025**: HTTP API permissions security fix (D1:Edit required for writes)
- **April 2025**: Read replication public beta (read-only replicas across regions)
- **Feb 2025**: PRAGMA optimize support, read-only access permission bug fix
- **Jan 2025**: Free tier limits enforcement (Feb 10 start), Worker API 40-60% faster queries

---

## Quick Start (5 Minutes)

### 1. Create D1 Database

```bash
# Create a new D1 database
npx wrangler d1 create my-database

# Output includes database_id - save this!
# ✅ Successfully created DB 'my-database'
#
# [[d1_databases]]
# binding = "DB"
# database_name = "my-database"
# database_id = "<UUID>"
```

### 2. Configure Bindings

Add to your `wrangler.jsonc`:

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-10-11",
  "d1_databases": [
    {
      "binding": "DB",                    // Available as env.DB in your Worker
      "database_name": "my-database",      // Name from wrangler d1 create
      "database_id": "<UUID>",             // ID from wrangler d1 create
      "preview_database_id": "local-db"    // For local development
    }
  ]
}
```

**CRITICAL:**
- `binding` is how you access the database in code (`env.DB`)
- `database_id` is the production database UUID
- `preview_database_id` is for local dev (can be any string)
- **Never commit real `database_id` values to public repos** - use environment variables or secrets

### 3. Create Your First Migration

```bash
# Create migration file
npx wrangler d1 migrations create my-database create_users_table

# This creates: migrations/0001_create_users_table.sql
```

Edit the migration file:

```sql
-- migrations/0001_create_users_table.sql
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  username TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER
);

-- Create index for common queries
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Optimize database
PRAGMA optimize;
```

### 4. Apply Migration

```bash
# Apply locally first (for testing)
npx wrangler d1 migrations apply my-database --local

# Apply to production when ready
npx wrangler d1 migrations apply my-database --remote
```

### 5. Query from Your Worker

```typescript
// src/index.ts
import { Hono } from 'hono';

type Bindings = {
  DB: D1Database;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get('/api/users/:email', async (c) => {
  const email = c.req.param('email');

  try {
    // ALWAYS use prepared statements with bind()
    const result = await c.env.DB.prepare(
      'SELECT * FROM users WHERE email = ?'
    )
    .bind(email)
    .first();

    if (!result) {
      return c.json({ error: 'User not found' }, 404);
    }

    return c.json(result);
  } catch (error: any) {
    console.error('D1 Error:', error.message);
    return c.json({ error: 'Database error' }, 500);
  }
});

export default app;
```

---

## D1 Migrations System

### Migration Workflow

```bash
# 1. Create migration
npx wrangler d1 migrations create <DATABASE_NAME> <MIGRATION_NAME>

# 2. List unapplied migrations
npx wrangler d1 migrations list <DATABASE_NAME> --local
npx wrangler d1 migrations list <DATABASE_NAME> --remote

# 3. Apply migrations
npx wrangler d1 migrations apply <DATABASE_NAME> --local   # Test locally
npx wrangler d1 migrations apply <DATABASE_NAME> --remote  # Deploy to production
```

### Migration File Naming

Migrations are automatically versioned:

```
migrations/
├── 0000_initial_schema.sql
├── 0001_add_users_table.sql
├── 0002_add_posts_table.sql
└── 0003_add_indexes.sql
```

**Rules:**
- Files are executed in sequential order
- Each migration runs once (tracked in `d1_migrations` table)
- Failed migrations roll back (transactional)
- Can't modify or delete applied migrations

### Custom Migration Configuration

```jsonc
{
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-database",
      "database_id": "<UUID>",
      "migrations_dir": "db/migrations",        // Custom directory (default: migrations/)
      "migrations_table": "schema_migrations"   // Custom tracking table (default: d1_migrations)
    }
  ]
}
```

### Migration Best Practices

#### ✅ Always Do:

```sql
-- Use IF NOT EXISTS to make migrations idempotent
CREATE TABLE IF NOT EXISTS users (...);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Run PRAGMA optimize after schema changes
PRAGMA optimize;

-- Use transactions for data migrations
BEGIN TRANSACTION;
UPDATE users SET updated_at = unixepoch() WHERE updated_at IS NULL;
COMMIT;
```

#### ❌ Never Do:

```sql
-- DON'T include BEGIN TRANSACTION at start (D1 handles this)
BEGIN TRANSACTION;  -- ❌ Remove this

-- DON'T use MySQL/PostgreSQL syntax
ALTER TABLE users MODIFY COLUMN email VARCHAR(255);  -- ❌ Not SQLite

-- DON'T create tables without IF NOT EXISTS
CREATE TABLE users (...);  -- ❌ Fails if table exists
```

### Handling Foreign Keys in Migrations

```sql
-- Temporarily disable foreign key checks during schema changes
PRAGMA defer_foreign_keys = true;

-- Make schema changes that would violate foreign keys
ALTER TABLE posts DROP COLUMN author_id;
ALTER TABLE posts ADD COLUMN user_id INTEGER REFERENCES users(user_id);

-- Foreign keys re-enabled automatically at end of migration
```

---

## D1 Workers API

**Type Definitions:**
```typescript
interface Env { DB: D1Database; }
type Bindings = { DB: D1Database; };
const app = new Hono<{ Bindings: Bindings }>();
```

**prepare() - PRIMARY METHOD (always use for user input):**
```typescript
const user = await env.DB.prepare('SELECT * FROM users WHERE email = ?')
  .bind(email).first();
```
Why: Prevents SQL injection, reusable, better performance, type-safe

**Query Result Methods:**
- `.all()` → `{ results, meta }` - Get all rows
- `.first()` → row object or null - Get first row
- `.first('column')` → value - Get single column value (e.g., COUNT)
- `.run()` → `{ success, meta }` - Execute INSERT/UPDATE/DELETE (no results)

**batch() - CRITICAL FOR PERFORMANCE:**
```typescript
const results = await env.DB.batch([
  env.DB.prepare('SELECT * FROM users WHERE user_id = ?').bind(1),
  env.DB.prepare('SELECT * FROM posts WHERE user_id = ?').bind(1)
]);
```
- Executes sequentially, single network round trip
- If one fails, remaining statements don't execute
- Use for: bulk inserts, fetching related data

**exec() - AVOID IN PRODUCTION:**
```typescript
await env.DB.exec('SELECT * FROM users;'); // Only for migrations/maintenance
```
- ❌ Never use with user input (SQL injection risk)
- ✅ Only use for: migration files, one-off tasks

---

## Query Patterns

### Basic CRUD Operations

```typescript
// CREATE
const { meta } = await env.DB.prepare(
  'INSERT INTO users (email, username, created_at) VALUES (?, ?, ?)'
).bind(email, username, Date.now()).run();
const newUserId = meta.last_row_id;

// READ (single)
const user = await env.DB.prepare('SELECT * FROM users WHERE user_id = ?')
  .bind(userId).first();

// READ (multiple)
const { results } = await env.DB.prepare('SELECT * FROM users LIMIT ?')
  .bind(10).all();

// UPDATE
const { meta } = await env.DB.prepare('UPDATE users SET username = ? WHERE user_id = ?')
  .bind(newUsername, userId).run();
const rowsAffected = meta.rows_written;

// DELETE
await env.DB.prepare('DELETE FROM users WHERE user_id = ?').bind(userId).run();

// COUNT
const count = await env.DB.prepare('SELECT COUNT(*) as total FROM users').first('total');

// EXISTS check
const exists = await env.DB.prepare('SELECT 1 FROM users WHERE email = ? LIMIT 1')
  .bind(email).first();
```

### Pagination Pattern

```typescript
const page = parseInt(c.req.query('page') || '1');
const limit = 20;
const offset = (page - 1) * limit;

const [countResult, usersResult] = await c.env.DB.batch([
  c.env.DB.prepare('SELECT COUNT(*) as total FROM users'),
  c.env.DB.prepare('SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?')
    .bind(limit, offset)
]);

return c.json({
  users: usersResult.results,
  pagination: { page, limit, total: countResult.results[0].total }
});
```

### Batch Pattern (Pseudo-Transactions)

```typescript
// D1 doesn't support multi-statement transactions, but batch() provides sequential execution
await env.DB.batch([
  env.DB.prepare('UPDATE users SET credits = credits - ? WHERE user_id = ?').bind(amount, fromUserId),
  env.DB.prepare('UPDATE users SET credits = credits + ? WHERE user_id = ?').bind(amount, toUserId),
  env.DB.prepare('INSERT INTO transactions (from_user, to_user, amount) VALUES (?, ?, ?)').bind(fromUserId, toUserId, amount)
]);
// If any statement fails, batch stops (transaction-like behavior)
```

---

## Error Handling

**Common Error Types:**
- `D1_ERROR` - General D1 error
- `D1_EXEC_ERROR` - SQL syntax error
- `D1_TYPE_ERROR` - Type mismatch (undefined instead of null)
- `D1_COLUMN_NOTFOUND` - Column doesn't exist

**Common Errors and Fixes:**

| Error | Cause | Solution |
|-------|-------|----------|
| **Statement too long** | Large INSERT with 1000+ rows | Break into batches of 100-250 using `batch()` |
| **Too many requests queued** | Individual queries in loop | Use `batch()` instead of loop |
| **D1_TYPE_ERROR** | Using `undefined` in bind | Use `null` for optional values: `.bind(email, bio \|\| null)` |
| **Transaction conflicts** | BEGIN TRANSACTION in migration | Remove BEGIN/COMMIT (D1 handles automatically) |
| **Foreign key violations** | Schema changes break constraints | Use `PRAGMA defer_foreign_keys = true` |

**Automatic Retries (Sept 2025):**
D1 automatically retries read-only queries (SELECT, EXPLAIN, WITH) up to 2 times on retryable errors. Check `meta.total_attempts` in response for retry count.

---

## Performance Optimization

**Index Best Practices:**
- ✅ Index columns in WHERE clauses: `CREATE INDEX idx_users_email ON users(email)`
- ✅ Index foreign keys: `CREATE INDEX idx_posts_user_id ON posts(user_id)`
- ✅ Index columns for sorting: `CREATE INDEX idx_posts_created_at ON posts(created_at DESC)`
- ✅ Multi-column indexes: `CREATE INDEX idx_posts_user_published ON posts(user_id, published)`
- ✅ Partial indexes: `CREATE INDEX idx_users_active ON users(email) WHERE deleted = 0`
- ✅ Test with: `EXPLAIN QUERY PLAN SELECT ...`

**PRAGMA optimize (Feb 2025):**
```sql
CREATE INDEX idx_users_email ON users(email);
PRAGMA optimize;  -- Run after schema changes
```

**Query Optimization:**
- ✅ Use specific columns (not `SELECT *`)
- ✅ Always include LIMIT on large result sets
- ✅ Use indexes for WHERE conditions
- ❌ Avoid functions in WHERE (can't use indexes): `WHERE LOWER(email)` → store lowercase instead

---

## Local Development

**Local vs Remote (Nov 2025 - Remote Bindings GA):**
```bash
# Local database (automatic creation)
npx wrangler d1 migrations apply my-database --local
npx wrangler d1 execute my-database --local --command "SELECT * FROM users"

# Remote database
npx wrangler d1 execute my-database --remote --command "SELECT * FROM users"

# Remote bindings (wrangler@4.37.0+) - connect local Worker to deployed D1
# Add to wrangler.jsonc: { "binding": "DB", "remote": true }
```

**Local Database Location:**
`.wrangler/state/v3/d1/miniflare-D1DatabaseObject/<database_id>.sqlite`

**Seed Local Database:**
```bash
npx wrangler d1 execute my-database --local --file=seed.sql
```

---

## Best Practices Summary

### ✅ Always Do:

1. **Use prepared statements** with `.bind()` for user input
2. **Use `.batch()`** for multiple queries (reduces latency)
3. **Create indexes** on frequently queried columns
4. **Run `PRAGMA optimize`** after schema changes
5. **Use `IF NOT EXISTS`** in migrations for idempotency
6. **Test migrations locally** before applying to production
7. **Handle errors gracefully** with try/catch
8. **Use `null`** instead of `undefined` for optional values
9. **Validate input** before binding to queries
10. **Check `meta.rows_written`** after UPDATE/DELETE

### ❌ Never Do:

1. **Never use `.exec()`** with user input (SQL injection risk)
2. **Never hardcode `database_id`** in public repos
3. **Never use `undefined`** in bind parameters (causes D1_TYPE_ERROR)
4. **Never fire individual queries in loops** (use batch instead)
5. **Never forget `LIMIT`** on potentially large result sets
6. **Never use `SELECT *`** in production (specify columns)
7. **Never include `BEGIN TRANSACTION`** in migration files
8. **Never modify applied migrations** (create new ones)
9. **Never skip error handling** on database operations
10. **Never assume queries succeed** (always check results)

---

## Known Issues Prevented

| Issue | Description | How to Avoid |
|-------|-------------|--------------|
| **Statement too long** | Large INSERT statements exceed D1 limits | Break into batches of 100-250 rows |
| **Transaction conflicts** | `BEGIN TRANSACTION` in migration files | Remove BEGIN/COMMIT (D1 handles this) |
| **Foreign key violations** | Schema changes break foreign key constraints | Use `PRAGMA defer_foreign_keys = true` |
| **Rate limiting / queue overload** | Too many individual queries | Use `batch()` instead of loops |
| **Memory limit exceeded** | Query loads too much data into memory | Add LIMIT, paginate results, shard queries |
| **Type mismatch errors** | Using `undefined` instead of `null` | Always use `null` for optional values |

---

## Wrangler Commands Reference

```bash
# Database management
wrangler d1 create <DATABASE_NAME>
wrangler d1 list
wrangler d1 delete <DATABASE_NAME>
wrangler d1 info <DATABASE_NAME>

# Migrations
wrangler d1 migrations create <DATABASE_NAME> <MIGRATION_NAME>
wrangler d1 migrations list <DATABASE_NAME> --local|--remote
wrangler d1 migrations apply <DATABASE_NAME> --local|--remote

# Execute queries
wrangler d1 execute <DATABASE_NAME> --local|--remote --command "SELECT * FROM users"
wrangler d1 execute <DATABASE_NAME> --local|--remote --file=./query.sql

# Time Travel (view historical data)
wrangler d1 time-travel info <DATABASE_NAME> --timestamp "2025-10-20"
wrangler d1 time-travel restore <DATABASE_NAME> --timestamp "2025-10-20"
```

---

## Official Documentation

- **D1 Overview**: https://developers.cloudflare.com/d1/
- **Get Started**: https://developers.cloudflare.com/d1/get-started/
- **Migrations**: https://developers.cloudflare.com/d1/reference/migrations/
- **Workers API**: https://developers.cloudflare.com/d1/worker-api/
- **Best Practices**: https://developers.cloudflare.com/d1/best-practices/
- **Wrangler Commands**: https://developers.cloudflare.com/workers/wrangler/commands/#d1

---

**Ready to build with D1!** 🚀
