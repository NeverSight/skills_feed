---
name: agentic-jumpstart-database
description: Database patterns with Drizzle ORM and PostgreSQL including schema design, queries, migrations, transactions, and relationships. Use when working with database schemas, queries, migrations, indexes, joins, or when the user mentions database, Drizzle, PostgreSQL, SQL, or data access.
---

# Database Patterns with Drizzle ORM

## Schema Design

### Table Definition

```typescript
import { pgTable, serial, varchar, text, timestamp, boolean, integer } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  name: varchar("name", { length: 100 }),
  bio: text("bio"),
  isAdmin: boolean("is_admin").default(false).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Type exports
export type User = typeof users.$inferSelect;
export type UserCreate = typeof users.$inferInsert;
```

### Relationships

```typescript
import { relations } from "drizzle-orm";

// One-to-many
export const modules = pgTable("modules", {
  id: serial("id").primaryKey(),
  title: varchar("title", { length: 255 }).notNull(),
  order: integer("order").default(0).notNull(),
});

export const segments = pgTable("segments", {
  id: serial("id").primaryKey(),
  moduleId: integer("module_id")
    .references(() => modules.id, { onDelete: "cascade" })
    .notNull(),
  title: varchar("title", { length: 255 }).notNull(),
  order: integer("order").default(0).notNull(),
});

// Define relations for query builder
export const modulesRelations = relations(modules, ({ many }) => ({
  segments: many(segments),
}));

export const segmentsRelations = relations(segments, ({ one }) => ({
  module: one(modules, {
    fields: [segments.moduleId],
    references: [modules.id],
  }),
}));
```

### Indexes

```typescript
import { pgTable, index, uniqueIndex } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: varchar("email", { length: 255 }).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
}, (table) => ({
  emailIdx: uniqueIndex("email_idx").on(table.email),
  createdAtIdx: index("created_at_idx").on(table.createdAt),
}));
```

## Data Access Layer

Data access functions go in `/src/data-access/`. They contain pure database operations with no business logic.

### Naming Convention

- Function name: `verbNoun` (e.g., `createUser`, `getSegmentById`)

### Basic CRUD Operations

```typescript
// src/data-access/users.ts
import { database } from "~/db";
import { users } from "~/db/schema";
import { eq } from "drizzle-orm";
import type { User, UserCreate } from "~/db/schema";

export async function getUsers() {
  return database.query.users.findMany();
}

export async function getUserById(id: number) {
  const result = await database
    .select()
    .from(users)
    .where(eq(users.id, id))
    .limit(1);
  return result[0];
}

export async function getUserByEmail(email: string) {
  const result = await database
    .select()
    .from(users)
    .where(eq(users.email, email))
    .limit(1);
  return result[0];
}

export async function createUser(user: UserCreate) {
  const result = await database.insert(users).values(user).returning();
  return result[0];
}

export async function updateUser(id: number, user: Partial<UserCreate>) {
  const result = await database
    .update(users)
    .set({ ...user, updatedAt: new Date() })
    .where(eq(users.id, id))
    .returning();
  return result[0];
}

export async function deleteUser(id: number) {
  const result = await database
    .delete(users)
    .where(eq(users.id, id))
    .returning();
  return result[0];
}
```

## Query Patterns

### Select Specific Columns

```typescript
// Only select what you need
const users = await database
  .select({
    id: users.id,
    name: users.name,
    email: users.email,
  })
  .from(users);
```

### Filtering

```typescript
import { eq, ne, gt, lt, gte, lte, like, and, or, isNull, isNotNull, inArray } from "drizzle-orm";

// Equality
const user = await database
  .select()
  .from(users)
  .where(eq(users.email, email));

// Multiple conditions
const activeAdmins = await database
  .select()
  .from(users)
  .where(and(eq(users.isAdmin, true), isNotNull(users.lastLoginAt)));

// OR conditions
const results = await database
  .select()
  .from(users)
  .where(or(eq(users.role, "admin"), eq(users.role, "moderator")));

// IN clause
const selectedUsers = await database
  .select()
  .from(users)
  .where(inArray(users.id, [1, 2, 3]));

// LIKE pattern matching
const matchingUsers = await database
  .select()
  .from(users)
  .where(like(users.name, `%${searchTerm}%`));
```

### Joins

```typescript
import { eq } from "drizzle-orm";

// Inner join
const segmentsWithModules = await database
  .select({
    segment: segments,
    moduleTitle: modules.title,
  })
  .from(segments)
  .innerJoin(modules, eq(segments.moduleId, modules.id));

// Left join (optional relationship)
const usersWithProgress = await database
  .select()
  .from(users)
  .leftJoin(progress, eq(users.id, progress.userId));
```

### Using Query Builder with Relations

```typescript
// Get segments with their modules (using relations)
const result = await database.query.segments.findMany({
  with: {
    module: true,
  },
  orderBy: [segments.order],
});

// Nested relations
const modulesWithSegments = await database.query.modules.findMany({
  with: {
    segments: {
      with: {
        attachments: true,
      },
    },
  },
});
```

### Ordering and Pagination

```typescript
import { desc, asc } from "drizzle-orm";

const paginatedUsers = await database
  .select()
  .from(users)
  .orderBy(desc(users.createdAt))
  .limit(20)
  .offset(40);
```

### Aggregations

```typescript
import { sql, count } from "drizzle-orm";

// Count
const [{ total }] = await database
  .select({ total: count() })
  .from(users);

// Sum, avg, etc.
const [{ avgPrice }] = await database
  .select({ avgPrice: sql`avg(${products.price})` })
  .from(products);
```

## Transactions

```typescript
export async function reorderSegmentsUseCase(
  updates: { id: number; order: number }[]
) {
  return database.transaction(async (tx) => {
    const results = [];
    for (const update of updates) {
      const [result] = await tx
        .update(segments)
        .set({ order: update.order, updatedAt: new Date() })
        .where(eq(segments.id, update.id))
        .returning();
      results.push(result);
    }
    return results;
  });
}
```

## Migration Commands

```bash
# Generate migration from schema changes
npm run db:generate

# Run migrations
npm run db:migrate

# Push schema directly (development only)
npm run db:push

# Open Drizzle Studio
npm run db:studio

# Reset database (clear, migrate, seed)
npm run db:reset
```

## Common Patterns

### Soft Delete

```typescript
export const users = pgTable("users", {
  // ...other fields
  deletedAt: timestamp("deleted_at"),
});

// Query only non-deleted
const activeUsers = await database
  .select()
  .from(users)
  .where(isNull(users.deletedAt));

// Soft delete
await database
  .update(users)
  .set({ deletedAt: new Date() })
  .where(eq(users.id, id));
```

### Timestamp Management

```typescript
// Always update updatedAt on modifications
export async function updateUser(id: number, data: Partial<UserCreate>) {
  const result = await database
    .update(users)
    .set({ ...data, updatedAt: new Date() })
    .where(eq(users.id, id))
    .returning();
  return result[0];
}
```

### Check if Exists

```typescript
export async function isEmailInUse(email: string): Promise<boolean> {
  const existing = await database
    .select({ id: users.id })
    .from(users)
    .where(eq(users.email, email))
    .limit(1);
  return existing.length > 0;
}
```

## Database Checklist

- [ ] Tables have appropriate indexes for queried columns
- [ ] Foreign keys use onDelete cascade where appropriate
- [ ] Data access functions use `verbNoun` naming
- [ ] Select only needed columns, not `select()`
- [ ] Use transactions for multi-step operations
- [ ] Always update `updatedAt` on modifications
- [ ] Use parameterized queries (automatic with Drizzle)
- [ ] Run `db:generate` after schema changes
- [ ] Type exports for `$inferSelect` and `$inferInsert`
- [ ] Relations defined for query builder usage
