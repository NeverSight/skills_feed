---
name: database-layer
description: "Load PROACTIVELY when task involves database design, schemas, or data access. Use when user says \"set up the database\", \"create a schema\", \"add a migration\", \"write a query\", or \"set up Prisma\". Covers schema design and normalization, ORM setup (Prisma, Drizzle), migration workflows, connection pooling, query optimization, indexing strategies, seeding, and transaction patterns for PostgreSQL, MySQL, SQLite, and MongoDB."
metadata:
  version: 1.0.0
  category: outcome
  tags: [database, orm, schema, migration, query, prisma, drizzle, sql]
---

## Resources
```
scripts/
  database-checklist.sh
references/
  orm-comparison.md
```

# Database Layer Implementation

This skill guides you through implementing database layers in applications, from initial schema design to query optimization. It leverages GoodVibes precision tools and project analysis tools for type-safe, production-ready database implementations.

## When to Use This Skill

Use this skill when you need to:

- Set up a new database connection and ORM
- Design and implement database schemas
- Create and run migrations
- Generate type-safe database clients
- Write queries and handle relationships
- Optimize database performance
- Integrate with existing database infrastructure

## Workflow

Follow this sequence for database layer implementation:

### 1. Discover Existing Database Infrastructure

Before implementing any database changes, understand the current state using the `detect_stack` analysis tool:

```yaml
detect_stack:
  project_root: "."
  categories: ["database", "orm"]
```

This identifies:
- Existing database technology (PostgreSQL, MySQL, MongoDB, SQLite)
- ORM/query builder in use (Prisma, Drizzle, Kysely, Mongoose)
- Schema definition files
- Migration tooling
- Connection management patterns

**Check project memory for database decisions:**

```yaml
precision_read:
  files:
    - path: ".goodvibes/memory/decisions.json"
    - path: ".goodvibes/memory/patterns.json"
  verbosity: minimal
```

Look for:
- Previous database technology choices ("Use Prisma for type safety")
- Migration strategies ("Always use reversible migrations")
- Performance patterns ("Add indexes for foreign keys")
- Known issues ("Avoid N+1 queries in user endpoints")

**If database already exists, map the current schema:**

```yaml
get_database_schema:
  project_root: "."
  include_relations: true
  include_indexes: true
```

This returns:
- Table/collection definitions
- Column types and constraints
- Relationships (foreign keys, references)
- Indexes and unique constraints
- Enums and custom types

### 2. Choose Database Technology

If starting fresh, consult the ORM comparison reference to select the appropriate technology stack.

See: **[references/orm-comparison.md](references/orm-comparison.md)** for decision trees.

**Key decision factors:**

| Factor | Recommendation |
|--------|---------------|
| Type safety priority | Prisma or Drizzle |
| Maximum SQL control | Kysely or Drizzle |
| Document database | Mongoose (MongoDB) |
| Serverless/edge | Drizzle with libSQL/Turso |
| Existing PostgreSQL | Prisma or Drizzle |
| Learning curve | Prisma (best DX) |

**Record your decision in memory:**

After choosing, document the decision in `.goodvibes/memory/decisions.json` for future reference.

### 3. Design Schema

**Identify entities and relationships first:**

```
Entities: User, Post, Comment, Category

Relationships:
- User 1:N Post (author)
- Post N:M Category (through PostCategory)
- Post 1:N Comment
- User 1:N Comment (author)
```

**Create schema files using precision_write:**

For Prisma:

```yaml
precision_write:
  files:
    - path: "prisma/schema.prisma"
      content: |
        generator client {
          provider = "prisma-client-js"
        }

        datasource db {
          provider = "postgresql"
          url      = env("DATABASE_URL")
        }

        model User {
          id        String   @id @default(cuid())
          email     String   @unique
          name      String?
          posts     Post[]
          comments  Comment[]
          createdAt DateTime @default(now())
          updatedAt DateTime @updatedAt
        }

        model Post {
          id         String     @id @default(cuid())
          title      String
          content    String
          published  Boolean    @default(false)
          author     User       @relation(fields: [authorId], references: [id])
          authorId   String
          categories Category[]
          comments   Comment[]
          createdAt  DateTime   @default(now())
          updatedAt  DateTime   @updatedAt

          @@index([authorId])
          @@index([published, createdAt])
        }

        model Category {
          id    String @id @default(cuid())
          name  String @unique
          posts Post[]
        }

        model Comment {
          id        String   @id @default(cuid())
          content   String
          post      Post     @relation(fields: [postId], references: [id])
          postId    String
          author    User     @relation(fields: [authorId], references: [id])
          authorId  String
          createdAt DateTime @default(now())

          @@index([postId])
          @@index([authorId])
        }
  verbosity: minimal
```

For Drizzle:

```yaml
precision_write:
  files:
    - path: "src/db/schema.ts"
      content: |
        import { pgTable, text, timestamp, boolean, index } from 'drizzle-orm/pg-core';
        import { relations } from 'drizzle-orm';

        export const users = pgTable('users', {
          id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
          email: text('email').notNull().unique(),
          name: text('name'),
          createdAt: timestamp('created_at').defaultNow().notNull(),
          updatedAt: timestamp('updated_at').defaultNow().notNull(),
        });

        export const posts = pgTable('posts', {
          id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
          title: text('title').notNull(),
          content: text('content').notNull(),
          published: boolean('published').default(false).notNull(),
          authorId: text('author_id').notNull().references(() => users.id),
          createdAt: timestamp('created_at').defaultNow().notNull(),
          updatedAt: timestamp('updated_at').defaultNow().notNull(),
        }, (table) => ({
          authorIdx: index('author_idx').on(table.authorId),
          publishedCreatedIdx: index('published_created_idx').on(table.published, table.createdAt),
        }));

        export const usersRelations = relations(users, ({ many }) => ({
          posts: many(posts),
        }));

        export const postsRelations = relations(posts, ({ one }) => ({
          author: one(users, {
            fields: [posts.authorId],
            references: [users.id],
          }),
        }));
  verbosity: minimal
```

**Schema best practices:**

1. **Use appropriate ID strategy:**
   - CUID/UUID for distributed systems
   - Auto-increment for simple apps
   - Composite keys for join tables

2. **Add timestamps:**
   - Always include `createdAt`
   - Include `updatedAt` for mutable entities
   - Consider `deletedAt` for soft deletes

3. **Index strategically:**
   - Foreign keys (for joins)
   - Frequently queried fields
   - Composite indexes for multi-column filters
   - Unique constraints where applicable

4. **Plan for scale:**
   - Text vs VARCHAR limits
   - JSONB for flexible data (PostgreSQL)
   - Separate tables for large text/blobs

### 4. Configure Database Connection

**Create environment configuration:**

```yaml
precision_write:
  files:
    - path: ".env.example"
      content: |
        # Database
        DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
        # For Prisma with connection pooling
        # DATABASE_URL="postgresql://user:password@localhost:5432/dbname?pgbouncer=true"
        # DIRECT_URL="postgresql://user:password@localhost:5432/dbname"
      mode: overwrite
  verbosity: minimal
```

**Create database client module:**

For Prisma:

```yaml
precision_write:
  files:
    - path: "src/lib/db.ts"
      content: |
        import { PrismaClient } from '@prisma/client';

        const globalForPrisma = globalThis as unknown as {
          prisma: PrismaClient | undefined;
        };

        export const db =
          globalForPrisma.prisma ??
          new PrismaClient({
            log:
              process.env.NODE_ENV === 'development'
                ? ['query', 'error', 'warn']
                : ['error'],
          });

        if (process.env.NODE_ENV !== 'production') {
          globalForPrisma.prisma = db;
        }
  verbosity: minimal
```

For Drizzle:

```yaml
precision_write:
  files:
    - path: "src/lib/db.ts"
      content: |
        import { drizzle } from 'drizzle-orm/postgres-js';
        import postgres from 'postgres';
        import * as schema from '@/db/schema';

        const connectionString = process.env.DATABASE_URL!;

        const client = postgres(connectionString, {
          max: process.env.NODE_ENV === 'production' ? 10 : 1,
        });

        export const db = drizzle(client, { schema });
  verbosity: minimal
```

### 5. Run Migrations

Use `precision_exec` to run migration commands with expectations:

**For Prisma:**

```yaml
precision_exec:
  commands:
    - cmd: "npx prisma migrate dev --name init"
      timeout_ms: 60000
      expect:
        exit_code: 0
      # Note: Prisma outputs progress to stderr; this is expected behavior
    - cmd: "npx prisma generate"
      expect:
        exit_code: 0
  verbosity: standard
```

**For Drizzle:**

```yaml
precision_exec:
  commands:
    - cmd: "npx drizzle-kit generate"
      expect:
        exit_code: 0
    - cmd: "npx drizzle-kit push"
      timeout_ms: 60000
      expect:
        exit_code: 0
  verbosity: standard
```

**Migration best practices:**

1. **Always review generated migrations** before applying
2. **Use reversible migrations** (include both up and down)
3. **Test migrations on dev database** before production
4. **Backup production data** before running migrations
5. **Use transactions** for multi-step migrations

### 6. Generate Type-Safe Client

Use the `generate_types` project tool to generate TypeScript types from your schema:

```yaml
generate_types:
  project_root: "."
  source: "database"
  output_path: "src/types/db.ts"
```

This creates type definitions for:
- Table/collection types
- Insert types (omitting auto-generated fields)
- Update types (all fields optional)
- Select types (with relations)

**Verify type generation:**

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
  verbosity: minimal
```

### 7. Implement Queries

**Start with basic CRUD operations:**

```yaml
precision_write:
  files:
    - path: "src/db/queries/users.ts"
      content: |
        import { db } from '@/lib/db';

        export async function createUser(data: { email: string; name?: string }) {
          return db.user.create({
            data,
          });
        }

        export async function getUserById(id: string) {
          return db.user.findUnique({
            where: { id },
            include: {
              posts: true,
            },
          });
        }

        export async function updateUser(
          id: string,
          data: { email?: string; name?: string }
        ) {
          return db.user.update({
            where: { id },
            data,
          });
        }

        export async function deleteUser(id: string) {
          return db.user.delete({
            where: { id },
          });
        }
  verbosity: minimal
```

**Check for N+1 query patterns using project tools:**

```yaml
get_prisma_operations:
  project_root: "."
  analyze_performance: true
```

This identifies:
- N+1 query opportunities (missing `include` or `select`)
- Missing indexes on frequently queried fields
- Inefficient relationship loading

**Optimize queries:**

1. **Use select to limit fields:**
   ```typescript
   db.user.findMany({
     select: { id: true, email: true }, // Don't fetch unused fields
   });
   ```

2. **Eager load relationships:**
   ```typescript
   db.post.findMany({
     include: { author: true }, // Prevents N+1
   });
   ```

3. **Use pagination:**
   ```typescript
   db.post.findMany({
     take: 20,
     skip: (page - 1) * 20,
   });
   ```

4. **Add database-level constraints:**
   ```prisma
   @@index([userId, createdAt(sort: Desc)])
   ```

### 8. Implement Transactions

**For multi-step operations, use transactions:**

Prisma:
```typescript
export async function createPostWithCategories(
  postData: { title: string; content: string; authorId: string },
  categoryIds: string[]
) {
  return db.$transaction(async (tx) => {
    const post = await tx.post.create({
      data: {
        ...postData,
        categories: {
          connect: categoryIds.map((id) => ({ id })),
        },
      },
    });

    await tx.user.update({
      where: { id: postData.authorId },
      data: { updatedAt: new Date() },
    });

    return post;
  });
}
```

Drizzle:
```typescript
export async function createPostWithCategories(
  postData: { title: string; content: string; authorId: string },
  categoryIds: string[]
) {
  return db.transaction(async (tx) => {
    const [post] = await tx.insert(posts).values(postData).returning();

    await tx.insert(postCategories).values(
      categoryIds.map((categoryId) => ({
        postId: post.id,
        categoryId,
      }))
    );

    return post;
  });
}
```

### 9. Seed Development Data

**Create seed script for local development:**

```yaml
precision_write:
  files:
    - path: "prisma/seed.ts"
      content: |
        import { PrismaClient } from '@prisma/client';

        const prisma = new PrismaClient();

        async function main() {
          // Clear existing data
          await prisma.comment.deleteMany();
          await prisma.post.deleteMany();
          await prisma.user.deleteMany();
          await prisma.category.deleteMany();

          // Create users
          const alice = await prisma.user.create({
            data: {
              email: 'alice@example.com',
              name: 'Alice',
            },
          });

          const bob = await prisma.user.create({
            data: {
              email: 'bob@example.com',
              name: 'Bob',
            },
          });

          // Create categories
          const tech = await prisma.category.create({
            data: { name: 'Technology' },
          });

          const news = await prisma.category.create({
            data: { name: 'News' },
          });

          // Create posts
          await prisma.post.create({
            data: {
              title: 'First Post',
              content: 'This is the first post',
              published: true,
              authorId: alice.id,
              categories: {
                connect: [{ id: tech.id }],
              },
            },
          });

          console.log('Database seeded successfully');
        }

        main()
          .catch((e) => {
            console.error(e);
            process.exit(1);
          })
          .finally(async () => {
            await prisma.$disconnect();
          });
  verbosity: minimal
```

**Update package.json:**

```yaml
precision_edit:
  edits:
    - path: "package.json"
      find: '"scripts": {'
      hints:
        near_line: 2
      replace: |
        "prisma": {
          "seed": "tsx prisma/seed.ts"
        },
        "scripts": {
  verbosity: minimal
```

### 10. Validate Implementation

**Run the database checklist script:**

```bash
./plugins/goodvibes/skills/outcome/database-layer/scripts/database-checklist.sh .
```

This validates:
- Schema file exists and is valid
- Migration directory present
- Database URL documented in .env.example
- Type generation configured
- No SQL injection vulnerabilities (string concatenation)
- Connection pooling configured
- Indexes on foreign keys

**Run type checking and tests:**

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
    - cmd: "npm run test -- db"
      expect:
        exit_code: 0
  verbosity: minimal
```

**Use query_database to verify data integrity:**

```yaml
query_database:
  project_root: "."
  query: "SELECT COUNT(*) FROM users;"
```

## Common Patterns

### Soft Deletes

Add `deletedAt` field and filter in queries:

```prisma
model Post {
  id        String    @id
  deletedAt DateTime?
}
```

```typescript
// Soft delete
await db.post.update({
  where: { id },
  data: { deletedAt: new Date() },
});

// Query only active records
await db.post.findMany({
  where: { deletedAt: null },
});
```

### Optimistic Locking

Use version field to prevent concurrent updates:

```prisma
model Post {
  id      String @id
  version Int    @default(0)
}
```

```typescript
await db.post.update({
  where: {
    id: postId,
    version: currentVersion,
  },
  data: {
    title: newTitle,
    version: { increment: 1 },
  },
});
```

### Connection Pooling

For serverless environments, use connection pooling:

```env
# PgBouncer
DATABASE_URL="postgresql://user:password@localhost:6543/db?pgbouncer=true"
DIRECT_URL="postgresql://user:password@localhost:5432/db"
```

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}
```

### Full-Text Search

PostgreSQL:
```prisma
@@index([content(ops: raw("gin_trgm_ops"))], type: Gin)
```

```typescript
await db.$queryRaw`
  SELECT * FROM posts
  WHERE to_tsvector('english', content) @@ to_tsquery('search terms')
`;
```

## Security Checklist

- [ ] Database credentials in environment variables (not committed)
- [ ] Input validation on all user-provided data
- [ ] Parameterized queries (no string concatenation)
- [ ] Row-level security for multi-tenant apps
- [ ] Rate limiting on expensive queries
- [ ] Audit logging for sensitive operations
- [ ] Least privilege database user permissions
- [ ] SSL/TLS for database connections in production

## Performance Checklist

- [ ] Indexes on foreign keys
- [ ] Composite indexes for multi-column filters
- [ ] Connection pooling configured
- [ ] Query result pagination
- [ ] Eager loading to prevent N+1 queries
- [ ] Database query logging in development
- [ ] Explain/analyze for slow queries
- [ ] Caching for frequently accessed data

## Troubleshooting

### Migration fails with constraint violation

1. Check existing data conflicts with new constraints
2. Add data migration before schema migration
3. Use multi-step migrations (add column nullable, populate, make required)

### N+1 query detected

1. Use `get_prisma_operations` to identify location
2. Add `include` or `select` with relations
3. Consider using `dataloader` for complex cases

### Connection pool exhausted

1. Increase pool size in connection string (`?pool_timeout=10`)
2. Check for missing `await` (connections not released)
3. Use connection pooler (PgBouncer, Prisma Accelerate)

### Type generation fails

1. Verify schema syntax with `npx prisma validate`
2. Clear generated files and regenerate
3. Check for circular dependencies in relations

## Next Steps

After implementing the database layer:

1. **Add caching** - Use Redis for frequently accessed data
2. **Implement search** - Add full-text search or Elasticsearch
3. **Add monitoring** - Track query performance and slow queries
4. **Write tests** - Unit tests for queries, integration tests for transactions
5. **Document schema** - Add comments to schema for team reference
6. **Plan backups** - Set up automated database backups

For additional reference material and decision trees, see:

- **[references/orm-comparison.md](references/orm-comparison.md)** - ORM selection guide
- **[scripts/database-checklist.sh](scripts/database-checklist.sh)** - Validation script
