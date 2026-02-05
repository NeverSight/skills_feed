---
name: d1-database
description: Serverless SQLite database for structured data at the edge. Load when building relational schemas, running SQL queries, managing migrations, performing CRUD operations, using JOINs/aggregations, handling JSON columns, or enforcing foreign keys with D1.
---

# D1 Database

D1 is Cloudflare's native serverless SQL database built on SQLite. Run queries at the edge with automatic replication and low latency.

## FIRST: Create Database

```bash
# Create D1 database
wrangler d1 create my-database

# Output includes database_id - add to wrangler.jsonc
```

Add binding to `wrangler.jsonc`:

```jsonc
{
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-database",
      "database_id": "<DATABASE_ID>",
      "migrations_dir": "./migrations"
    }
  ]
}
```

Generate TypeScript types:

```bash
wrangler types
```

## When to Use

| Use Case | Why D1 |
|----------|--------|
| Relational data | Structured tables with relationships |
| Complex queries | JOINs, aggregations, full SQL support |
| User data | Accounts, profiles, settings |
| Content management | Posts, comments, metadata |
| E-commerce | Products, orders, inventory |
| Analytics | Event tracking with SQL queries |

**When NOT to use D1:**
- Simple key-value data → Use Workers KV
- Large files/objects → Use R2
- Real-time coordination → Use Durable Objects
- High-frequency writes → Use Queues + D1

## Quick Reference

| Operation | Method | Returns |
|-----------|--------|---------|
| Execute query | `db.prepare(sql).bind(...).run()` | `{ success: boolean, meta: {...} }` |
| Get all rows | `db.prepare(sql).bind(...).all()` | `{ results: T[], success: boolean }` |
| Get first row | `db.prepare(sql).bind(...).first()` | `T \| null` |
| Get single value | `db.prepare(sql).bind(...).first('column')` | `any \| null` |
| Batch queries | `db.batch([stmt1, stmt2, ...])` | `Array<D1Result>` |
| Raw query | `db.prepare(sql).bind(...).raw()` | `Array<Array<any>>` |

## Minimal Example

```typescript
// src/index.ts
interface Env {
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env) {
    // Get all users
    const { results } = await env.DB
      .prepare("SELECT * FROM users WHERE active = ?")
      .bind(true)
      .all<{ id: number; name: string; email: string }>();

    return Response.json(results);
  }
} satisfies ExportedHandler<Env>;
```

## CRUD Operations

```typescript
interface Env {
  DB: D1Database;
}

type User = {
  id: number;
  name: string;
  email: string;
  created_at: string;
};

type NewUser = Omit<User, "id" | "created_at">;

export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);
    const { pathname } = url;

    // CREATE - Insert new user
    if (pathname === "/users" && request.method === "POST") {
      const user: NewUser = await request.json();
      
      const result = await env.DB
        .prepare("INSERT INTO users (name, email) VALUES (?, ?)")
        .bind(user.name, user.email)
        .run();

      if (!result.success) {
        return Response.json({ error: "Failed to create user" }, { status: 500 });
      }

      return Response.json({ 
        id: result.meta.last_row_id,
        message: "User created" 
      }, { status: 201 });
    }

    // READ - Get user by ID
    if (pathname.startsWith("/users/") && request.method === "GET") {
      const id = pathname.split("/")[2];
      
      const user = await env.DB
        .prepare("SELECT * FROM users WHERE id = ?")
        .bind(id)
        .first<User>();

      if (!user) {
        return Response.json({ error: "User not found" }, { status: 404 });
      }

      return Response.json(user);
    }

    // READ - Get all users (with pagination)
    if (pathname === "/users" && request.method === "GET") {
      const page = parseInt(url.searchParams.get("page") || "1");
      const limit = parseInt(url.searchParams.get("limit") || "10");
      const offset = (page - 1) * limit;

      const { results } = await env.DB
        .prepare("SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?")
        .bind(limit, offset)
        .all<User>();

      return Response.json({
        users: results,
        page,
        limit
      });
    }

    // UPDATE - Update user
    if (pathname.startsWith("/users/") && request.method === "PUT") {
      const id = pathname.split("/")[2];
      const updates: Partial<NewUser> = await request.json();

      const result = await env.DB
        .prepare("UPDATE users SET name = ?, email = ? WHERE id = ?")
        .bind(updates.name, updates.email, id)
        .run();

      if (result.meta.changes === 0) {
        return Response.json({ error: "User not found" }, { status: 404 });
      }

      return Response.json({ message: "User updated" });
    }

    // DELETE - Delete user
    if (pathname.startsWith("/users/") && request.method === "DELETE") {
      const id = pathname.split("/")[2];

      const result = await env.DB
        .prepare("DELETE FROM users WHERE id = ?")
        .bind(id)
        .run();

      if (result.meta.changes === 0) {
        return Response.json({ error: "User not found" }, { status: 404 });
      }

      return Response.json({ message: "User deleted" });
    }

    return Response.json({ error: "Not found" }, { status: 404 });
  }
} satisfies ExportedHandler<Env>;
```

## Migrations Workflow

D1 uses SQL migration files to manage schema changes over time.

### Create Migration

```bash
# Create new migration file
wrangler d1 migrations create my-database create_users_table

# Creates: migrations/0001_create_users_table.sql
```

Edit the generated migration file:

```sql
-- migrations/0001_create_users_table.sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Apply Migrations

```bash
# Apply locally for testing
wrangler d1 migrations apply my-database --local

# Apply to remote database
wrangler d1 migrations apply my-database --remote

# List pending migrations
wrangler d1 migrations list my-database --local
```

### Migration Best Practices

1. **One migration per change**: Create separate migrations for each schema change
2. **Test locally first**: Always run `--local` before `--remote`
3. **Never edit applied migrations**: Create new migrations to fix issues
4. **Use transactions**: Migrations run in transactions by default
5. **Add indexes**: Include indexes in migrations for query performance

Example migration with multiple tables:

```sql
-- migrations/0002_add_posts.sql
CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  published BOOLEAN DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_published ON posts(published);
```

## Batch Operations

Execute multiple statements in a single transaction for better performance and atomicity.

```typescript
interface Env {
  DB: D1Database;
}

type Post = {
  title: string;
  content: string;
  userId: number;
};

export default {
  async fetch(request: Request, env: Env) {
    const posts: Post[] = await request.json();

    // Prepare all statements
    const statements = posts.map(post =>
      env.DB
        .prepare("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)")
        .bind(post.title, post.content, post.userId)
    );

    // Execute as a batch (all or nothing)
    try {
      const results = await env.DB.batch(statements);
      
      const insertedIds = results.map(r => r.meta.last_row_id);
      
      return Response.json({
        message: "Posts created",
        ids: insertedIds,
        count: results.length
      });
    } catch (error) {
      return Response.json(
        { error: "Batch insert failed", details: error.message },
        { status: 500 }
      );
    }
  }
} satisfies ExportedHandler<Env>;
```

**Batch benefits:**
- All statements succeed or all fail (atomic)
- Single round-trip to database
- Better performance for bulk operations
- Automatic transaction handling

**Batch limitations:**
- Maximum 100 statements per batch
- All statements must be from same database
- Cannot read from one statement and use in another within batch

## SQLite Features

D1 supports comprehensive SQLite features including:

- **JSON Functions** - Query and manipulate JSON data in columns. See [references/json-functions.md](references/json-functions.md)
- **Foreign Keys** - Enforce referential integrity across tables. See [references/foreign-keys.md](references/foreign-keys.md)
- **Full-Text Search (FTS5)** - Fast text search with stemming and ranking. See [references/sql-statements.md](references/sql-statements.md)
- **Math Functions** - sqrt(), pow(), sin(), cos(), and more
- **PRAGMA Statements** - Schema introspection, optimization, constraint checking

## Query Patterns

### Parameterized Queries (Required)

**ALWAYS** use parameterized queries to prevent SQL injection:

```typescript
// ✅ CORRECT - Parameterized query
const user = await env.DB
  .prepare("SELECT * FROM users WHERE email = ?")
  .bind(userEmail)
  .first<User>();

// ❌ DANGEROUS - String concatenation (SQL injection risk)
const user = await env.DB
  .prepare(`SELECT * FROM users WHERE email = '${userEmail}'`)
  .first<User>();
```

### Type-Safe Queries

Use TypeScript generics for type-safe results:

```typescript
type UserWithPosts = {
  id: number;
  name: string;
  email: string;
  post_count: number;
};

const { results } = await env.DB
  .prepare(`
    SELECT u.*, COUNT(p.id) as post_count
    FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
    GROUP BY u.id
  `)
  .all<UserWithPosts>();

// results is typed as UserWithPosts[]
results.forEach(user => {
  console.log(`${user.name} has ${user.post_count} posts`);
});
```

### Complex Queries with JOINs

```typescript
type PostDetail = {
  post_id: number;
  post_title: string;
  post_content: string;
  author_name: string;
  author_email: string;
  created_at: string;
};

const { results } = await env.DB
  .prepare(`
    SELECT 
      p.id as post_id,
      p.title as post_title,
      p.content as post_content,
      u.name as author_name,
      u.email as author_email,
      p.created_at
    FROM posts p
    INNER JOIN users u ON p.user_id = u.id
    WHERE p.published = ?
    ORDER BY p.created_at DESC
    LIMIT ?
  `)
  .bind(true, 10)
  .all<PostDetail>();

return Response.json(results);
```

### Pagination and Search

```typescript
// Pagination
const offset = (page - 1) * limit;
const { results } = await env.DB
  .prepare("SELECT * FROM users ORDER BY id LIMIT ? OFFSET ?")
  .bind(limit, offset)
  .all<User>();

// Search with LIKE
const { results } = await env.DB
  .prepare("SELECT * FROM users WHERE name LIKE ? LIMIT 20")
  .bind(`%${searchTerm}%`)
  .all<User>();
```

See [references/queries.md](references/queries.md) for complete pagination patterns with total counts and hasMore flags

## Error Handling

```typescript
try {
  const result = await env.DB
    .prepare("INSERT INTO users (name, email) VALUES (?, ?)")
    .bind(name, email)
    .run();

  if (!result.success) {
    throw new Error("Insert failed");
  }

  return Response.json({ id: result.meta.last_row_id });
} catch (error) {
  // Handle specific SQLite errors
  if (error.message.includes("UNIQUE constraint failed")) {
    return Response.json(
      { error: "Email already exists" },
      { status: 409 }
    );
  }

  console.error("Database error:", error);
  return Response.json(
    { error: "Database operation failed" },
    { status: 500 }
  );
}
```

## Result Metadata

Query results include metadata about the operation:

```typescript
const result = await env.DB
  .prepare("UPDATE users SET name = ? WHERE id = ?")
  .bind("New Name", 123)
  .run();

// Check metadata
console.log({
  success: result.success,          // boolean - operation succeeded
  changes: result.meta.changes,     // number - rows affected
  lastRowId: result.meta.last_row_id, // number - last inserted ID
  duration: result.meta.duration    // number - query time in ms
});

// Common patterns
if (result.meta.changes === 0) {
  return Response.json({ error: "Not found" }, { status: 404 });
}
```

## Detailed References

### Core SQL Features
- **[references/queries.md](references/queries.md)** - Advanced query patterns, aggregations, window functions, CTEs, subqueries
- **[references/json-functions.md](references/json-functions.md)** - Complete JSON API: extract, modify, arrays, objects, generated columns
- **[references/foreign-keys.md](references/foreign-keys.md)** - Foreign key constraints, CASCADE, RESTRICT, SET NULL, deferring constraints
- **[references/sql-statements.md](references/sql-statements.md)** - SQLite extensions (FTS5, Math), PRAGMA statements, schema introspection

### D1-Specific
- **[references/migrations.md](references/migrations.md)** - Schema design, migration strategies, rollback patterns
- **[references/testing.md](references/testing.md)** - Vitest integration, applying migrations in tests, test isolation

## Best Practices

1. **Always use parameterized queries**: Use `.bind()` to prevent SQL injection
2. **Use TypeScript generics**: Type your query results with `.first<T>()` and `.all<T>()`
3. **Batch for bulk operations**: Use `db.batch()` for multiple related operations
4. **Index your queries**: Add indexes on columns used in WHERE, JOIN, and ORDER BY
5. **Test migrations locally**: Run `wrangler d1 migrations apply --local` before `--remote`
6. **Handle unique constraint errors**: Check for specific error messages like "UNIQUE constraint failed"
7. **Use transactions via batch**: Batch operations are automatically atomic
8. **Paginate large result sets**: Use LIMIT and OFFSET to avoid memory issues
9. **Check result.success**: Always verify operation success before proceeding
10. **Design for eventual consistency**: D1 replicates across regions, reads may lag slightly

## Performance Tips

- **Limit results**: Always use LIMIT for queries that could return many rows
- **Use indexes**: Create indexes on frequently queried columns
- **Batch writes**: Use `db.batch()` instead of multiple individual `run()` calls
- **Avoid SELECT \***: Only select columns you need
- **Use first() for single rows**: More efficient than `.all()` when you need one result
- **Cache read-heavy data**: Consider Workers KV for frequently accessed data
