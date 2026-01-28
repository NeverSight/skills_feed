---
name: schema-design
description: Design or modify Drizzle ORM schemas with proper relationships, constraints, and indexes. Use when adding new tables, modifying existing schemas, or optimizing database structure.
allowed-tools: Read, Edit, Grep, Glob
---

# Schema Design Skill

This skill helps you design and modify database schemas using Drizzle ORM in `packages/database/`.

## When to Use This Skill

- Creating new database tables
- Adding columns to existing tables
- Defining relationships between tables
- Creating indexes for query optimization
- Adding constraints (unique, not null, default values)
- Renaming or dropping tables/columns
- Optimizing schema for performance

## Database Architecture

```
packages/database/
├── src/
│   ├── db/
│   │   └── schema/
│   │       ├── cars.ts         # Car registration data
│   │       ├── coe.ts          # COE bidding results
│   │       ├── pqp.ts          # PQP data
│   │       ├── posts.ts        # Blog posts
│   │       ├── analytics.ts    # Analytics events
│   │       └── index.ts        # Schema exports
│   ├── index.ts                # Database client export
│   └── migrate.ts              # Migration runner
├── migrations/                  # Migration files
└── drizzle.config.ts           # Drizzle configuration
```

## Naming Conventions

The project uses **camelCase** for column names:

```typescript
// ✅ Correct
export const cars = pgTable("cars", {
  vehicleClass: text("vehicle_class"),
  fuelType: text("fuel_type"),
  registrationDate: timestamp("registration_date"),
});

// ❌ Wrong
export const cars = pgTable("cars", {
  vehicle_class: text("vehicle_class"),  // snake_case
  FuelType: text("fuel_type"),            // PascalCase
});
```

## Basic Schema Patterns

### Simple Table

```typescript
// packages/database/src/db/schema/example.ts
import { pgTable, text, integer, timestamp, boolean } from "drizzle-orm/pg-core";

export const examples = pgTable("examples", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  description: text("description"),
  count: integer("count").default(0).notNull(),
  isActive: boolean("is_active").default(true).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});
```

### Table with Relationships

```typescript
import { pgTable, text, integer, timestamp } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";
import { users } from "./users";

export const posts = pgTable("posts", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content").notNull(),
  authorId: text("author_id").notNull().references(() => users.id),
  publishedAt: timestamp("published_at"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Define relations
export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

### Table with Indexes

```typescript
import { pgTable, text, integer, timestamp, index, uniqueIndex } from "drizzle-orm/pg-core";

export const cars = pgTable("cars", {
  id: text("id").primaryKey(),
  make: text("make").notNull(),
  model: text("model").notNull(),
  year: integer("year").notNull(),
  registrationDate: timestamp("registration_date").notNull(),
}, (table) => ({
  // Single column index
  makeIdx: index("cars_make_idx").on(table.make),

  // Composite index
  makeModelIdx: index("cars_make_model_idx").on(table.make, table.model),

  // Unique index
  registrationIdx: uniqueIndex("cars_registration_idx").on(table.registrationDate),
}));
```

## Existing Schema Examples

### Cars Table

```typescript
// packages/database/src/db/schema/cars.ts
import { pgTable, text, integer, timestamp, index } from "drizzle-orm/pg-core";

export const cars = pgTable("cars", {
  id: text("id").primaryKey(),
  make: text("make").notNull(),
  model: text("model"),
  vehicleClass: text("vehicle_class"),
  fuelType: text("fuel_type"),
  month: text("month").notNull(),
  number: integer("number").default(0).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
}, (table) => ({
  monthIdx: index("cars_month_idx").on(table.month),
  makeIdx: index("cars_make_idx").on(table.make),
}));
```

### COE Table

```typescript
// packages/database/src/db/schema/coe.ts
import { pgTable, text, integer, timestamp, numeric, index } from "drizzle-orm/pg-core";

export const coe = pgTable("coe", {
  id: text("id").primaryKey(),
  biddingNo: integer("bidding_no").notNull(),
  month: text("month").notNull(),
  vehicleClass: text("vehicle_class").notNull(),
  quota: integer("quota").default(0).notNull(),
  bidsReceived: integer("bids_received").default(0).notNull(),
  premium: numeric("premium", { precision: 10, scale: 2 }).default("0").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
}, (table) => ({
  biddingNoIdx: index("coe_bidding_no_idx").on(table.biddingNo),
  monthIdx: index("coe_month_idx").on(table.month),
}));
```

### Posts Table

```typescript
// packages/database/src/db/schema/posts.ts
import { pgTable, text, timestamp, boolean, index } from "drizzle-orm/pg-core";

export const posts = pgTable("posts", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  slug: text("slug").notNull().unique(),
  content: text("content").notNull(),
  excerpt: text("excerpt"),
  published: boolean("published").default(false).notNull(),
  publishedAt: timestamp("published_at"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
}, (table) => ({
  slugIdx: index("posts_slug_idx").on(table.slug),
  publishedAtIdx: index("posts_published_at_idx").on(table.publishedAt),
}));
```

## Column Types

### Text Types

```typescript
import { pgTable, text, varchar, char } from "drizzle-orm/pg-core";

export const examples = pgTable("examples", {
  // Unlimited text
  description: text("description"),

  // Limited varchar
  email: varchar("email", { length: 255 }),

  // Fixed length
  code: char("code", { length: 10 }),
});
```

### Numeric Types

```typescript
import { pgTable, integer, bigint, numeric, real, doublePrecision } from "drizzle-orm/pg-core";

export const examples = pgTable("examples", {
  // Integer types
  count: integer("count"),
  bigCount: bigint("big_count", { mode: "number" }),  // or "bigint" for BigInt

  // Decimal types
  price: numeric("price", { precision: 10, scale: 2 }),  // 10 digits, 2 decimal

  // Floating point
  rating: real("rating"),
  coordinate: doublePrecision("coordinate"),
});
```

### Date/Time Types

```typescript
import { pgTable, timestamp, date, time } from "drizzle-orm/pg-core";

export const examples = pgTable("examples", {
  // Timestamp with timezone
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow(),

  // Timestamp without timezone
  scheduledAt: timestamp("scheduled_at", { withTimezone: false }),

  // Date only
  birthDate: date("birth_date"),

  // Time only
  openingTime: time("opening_time"),
});
```

### Boolean and JSON

```typescript
import { pgTable, boolean, json, jsonb } from "drizzle-orm/pg-core";

export const examples = pgTable("examples", {
  // Boolean
  isActive: boolean("is_active").default(true),

  // JSON (slower, stores as text)
  settings: json("settings"),

  // JSONB (faster, binary format)
  metadata: jsonb("metadata").$type<{ key: string; value: any }>(),
});
```

### Array Types

```typescript
import { pgTable, text } from "drizzle-orm/pg-core";

export const examples = pgTable("examples", {
  tags: text("tags").array(),
  emails: text("emails").array().notNull().default([]),
});
```

## Relationships

### One-to-Many

```typescript
import { pgTable, text, timestamp } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// Users table
export const users = pgTable("users", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
});

// Posts table (many posts belong to one user)
export const posts = pgTable("posts", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  authorId: text("author_id").notNull().references(() => users.id),
});

// Define relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

### Many-to-Many

```typescript
import { pgTable, text, primaryKey } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// Posts table
export const posts = pgTable("posts", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
});

// Tags table
export const tags = pgTable("tags", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
});

// Junction table
export const postsToTags = pgTable("posts_to_tags", {
  postId: text("post_id").notNull().references(() => posts.id),
  tagId: text("tag_id").notNull().references(() => tags.id),
}, (table) => ({
  pk: primaryKey({ columns: [table.postId, table.tagId] }),
}));

// Define relations
export const postsRelations = relations(posts, ({ many }) => ({
  postsToTags: many(postsToTags),
}));

export const tagsRelations = relations(tags, ({ many }) => ({
  postsToTags: many(postsToTags),
}));

export const postsToTagsRelations = relations(postsToTags, ({ one }) => ({
  post: one(posts, {
    fields: [postsToTags.postId],
    references: [posts.id],
  }),
  tag: one(tags, {
    fields: [postsToTags.tagId],
    references: [tags.id],
  }),
}));
```

## Constraints

### Primary Keys

```typescript
import { pgTable, text, integer, primaryKey } from "drizzle-orm/pg-core";

// Single column primary key
export const users = pgTable("users", {
  id: text("id").primaryKey(),
});

// Composite primary key
export const userRoles = pgTable("user_roles", {
  userId: text("user_id").notNull(),
  roleId: text("role_id").notNull(),
}, (table) => ({
  pk: primaryKey({ columns: [table.userId, table.roleId] }),
}));
```

### Unique Constraints

```typescript
import { pgTable, text, unique } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),  // Column-level unique
  username: text("username").notNull(),
}, (table) => ({
  // Table-level unique constraint
  uniqueUsername: unique("users_username_unique").on(table.username),
}));
```

### Foreign Keys

```typescript
import { pgTable, text, foreignKey } from "drizzle-orm/pg-core";

export const posts = pgTable("posts", {
  id: text("id").primaryKey(),
  authorId: text("author_id").notNull(),
}, (table) => ({
  // Inline foreign key
  authorFk: foreignKey({
    columns: [table.authorId],
    foreignColumns: [users.id],
  }).onDelete("cascade"),  // Options: cascade, set null, restrict, no action
}));

// Or use references() shorthand
export const posts2 = pgTable("posts", {
  id: text("id").primaryKey(),
  authorId: text("author_id").notNull().references(() => users.id, { onDelete: "cascade" }),
});
```

### Check Constraints

```typescript
import { pgTable, integer, check, sql } from "drizzle-orm/pg-core";

export const products = pgTable("products", {
  id: text("id").primaryKey(),
  price: integer("price").notNull(),
  discount: integer("discount").notNull(),
}, (table) => ({
  // Ensure discount is less than price
  priceCheck: check("price_check", sql`${table.price} > ${table.discount}`),
}));
```

## Indexes

### Single Column Index

```typescript
import { pgTable, text, index } from "drizzle-orm/pg-core";

export const cars = pgTable("cars", {
  id: text("id").primaryKey(),
  make: text("make").notNull(),
}, (table) => ({
  makeIdx: index("cars_make_idx").on(table.make),
}));
```

### Composite Index

```typescript
export const cars = pgTable("cars", {
  id: text("id").primaryKey(),
  make: text("make").notNull(),
  model: text("model").notNull(),
}, (table) => ({
  makeModelIdx: index("cars_make_model_idx").on(table.make, table.model),
}));
```

### Unique Index

```typescript
import { uniqueIndex } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull(),
}, (table) => ({
  emailIdx: uniqueIndex("users_email_idx").on(table.email),
}));
```

### Partial Index

```typescript
import { sql } from "drizzle-orm";

export const posts = pgTable("posts", {
  id: text("id").primaryKey(),
  published: boolean("published").default(false),
  publishedAt: timestamp("published_at"),
}, (table) => ({
  // Index only published posts
  publishedIdx: index("posts_published_idx")
    .on(table.publishedAt)
    .where(sql`${table.published} = true`),
}));
```

## Schema Workflow

### 1. Create Schema File

```typescript
// packages/database/src/db/schema/my-table.ts
import { pgTable, text, timestamp } from "drizzle-orm/pg-core";

export const myTable = pgTable("my_table", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

### 2. Export from Index

```typescript
// packages/database/src/db/schema/index.ts
export * from "./cars";
export * from "./coe";
export * from "./posts";
export * from "./my-table";  // Add new export
```

### 3. Generate Migration

```bash
cd packages/database

# Generate migration from schema changes
pnpm db:generate

# This creates a new migration file in migrations/
```

### 4. Review Migration

Check generated SQL in `migrations/XXXX_migration_name.sql`:

```sql
CREATE TABLE IF NOT EXISTS "my_table" (
  "id" text PRIMARY KEY NOT NULL,
  "name" text NOT NULL,
  "created_at" timestamp DEFAULT now() NOT NULL
);
```

### 5. Run Migration

```bash
# Apply migration to database
pnpm db:migrate
```

## Common Schema Patterns

### Soft Delete

```typescript
export const posts = pgTable("posts", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  deletedAt: timestamp("deleted_at"),  // null = not deleted
});

// Query only non-deleted posts
const activePosts = await db.query.posts.findMany({
  where: isNull(posts.deletedAt),
});
```

### Timestamps

```typescript
export const posts = pgTable("posts", {
  id: text("id").primaryKey(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Update updatedAt on every change
await db.update(posts)
  .set({
    title: "New Title",
    updatedAt: new Date(),
  })
  .where(eq(posts.id, postId));
```

### Enum Types

```typescript
import { pgTable, text, pgEnum } from "drizzle-orm/pg-core";

// Define enum
export const roleEnum = pgEnum("role", ["admin", "user", "guest"]);

export const users = pgTable("users", {
  id: text("id").primaryKey(),
  role: roleEnum("role").default("user").notNull(),
});
```

### UUID Primary Keys

```typescript
import { pgTable, uuid, text } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: uuid("id").defaultRandom().primaryKey(),  // Auto-generate UUID
  name: text("name").notNull(),
});
```

## Performance Optimization

### Choose Appropriate Indexes

```typescript
// ✅ Index frequently queried columns
export const cars = pgTable("cars", {
  make: text("make").notNull(),
  registrationDate: timestamp("registration_date").notNull(),
}, (table) => ({
  makeIdx: index().on(table.make),              // For: WHERE make = 'Toyota'
  dateIdx: index().on(table.registrationDate),  // For: WHERE registrationDate > '2024-01-01'
}));

// ❌ Don't index every column
// Only index columns used in WHERE, JOIN, ORDER BY
```

### Use Appropriate Data Types

```typescript
// ✅ Use smallest appropriate type
count: integer("count"),              // -2B to 2B
price: numeric("price", { precision: 10, scale: 2 }),  // $99,999,999.99

// ❌ Don't use text for everything
count: text("count"),  // Wastes space, slower queries
```

### Denormalization for Performance

```typescript
// Store computed values to avoid expensive joins
export const posts = pgTable("posts", {
  id: text("id").primaryKey(),
  authorId: text("author_id").notNull(),
  authorName: text("author_name").notNull(),  // Denormalized from users table
  commentsCount: integer("comments_count").default(0),  // Denormalized count
});
```

## Testing Schemas

```typescript
// packages/database/src/db/schema/__tests__/cars.test.ts
import { describe, it, expect } from "vitest";
import { db } from "../../index";
import { cars } from "../cars";

describe("Cars Schema", () => {
  it("inserts and queries car data", async () => {
    const [car] = await db.insert(cars).values({
      id: "test-1",
      make: "Toyota",
      model: "Camry",
      month: "2024-01",
      number: 100,
    }).returning();

    expect(car.make).toBe("Toyota");
    expect(car.number).toBe(100);
  });
});
```

## References

- Drizzle ORM Documentation: Use Context7 for latest docs
- Related files:
  - `packages/database/src/db/schema/` - All schema files
  - `packages/database/drizzle.config.ts` - Drizzle configuration
  - `packages/database/CLAUDE.md` - Database package documentation

## Best Practices

1. **Naming**: Use camelCase for columns, snake_case for table names
2. **Not Null**: Use .notNull() for required fields
3. **Defaults**: Provide sensible defaults where appropriate
4. **Indexes**: Index columns used in WHERE, JOIN, ORDER BY
5. **Relationships**: Define relations for type-safe queries
6. **Timestamps**: Always include createdAt/updatedAt
7. **Constraints**: Use unique, foreign key constraints
8. **Migrations**: Always review generated migrations before running
