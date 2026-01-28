---
name: drizzle-migrations
description: Drizzle ORM migrations for Neon PostgreSQL. Use when creating database schemas, running migrations, or troubleshooting Drizzle issues.
---

# Drizzle ORM Migrations

## Setup

### drizzle.config.ts
```typescript
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### Connection (Neon Serverless)
```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/neon-http';
import { neon } from '@neondatabase/serverless';
import * as schema from './schema';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

## Schema Patterns

### Standard Table with Timestamps
```typescript
import { pgTable, text, timestamp, uuid, boolean } from 'drizzle-orm/pg-core';

const timestamps = {
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
};

export const projects = pgTable('projects', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  userId: uuid('user_id').notNull().references(() => users.id),
  isActive: boolean('is_active').default(true).notNull(),
  ...timestamps,
});
```

### Type Inference
```typescript
export type Project = typeof projects.$inferSelect;
export type NewProject = typeof projects.$inferInsert;
```

### Relations
```typescript
import { relations } from 'drizzle-orm';

export const usersRelations = relations(users, ({ many }) => ({
  projects: many(projects),
}));

export const projectsRelations = relations(projects, ({ one }) => ({
  owner: one(users, {
    fields: [projects.userId],
    references: [users.id],
  }),
}));
```

## Migration Commands

```bash
# Generate migration from schema changes
pnpm drizzle-kit generate

# Push schema directly (dev only, no migration file)
pnpm drizzle-kit push

# Apply migrations (production)
pnpm drizzle-kit migrate

# Open Drizzle Studio GUI
pnpm drizzle-kit studio
```

## Workflow

1. **Modify schema.ts**
2. **Generate migration**: `pnpm drizzle-kit generate`
3. **Review SQL**: Check `drizzle/` folder
4. **Apply**:
   - Dev: `pnpm drizzle-kit push`
   - Prod: `pnpm drizzle-kit migrate`
5. **Update types**: Types auto-update from schema

## Common Issues

### "relation does not exist"
- Migration not applied
- Run: `pnpm drizzle-kit push` (dev) or `migrate` (prod)

### "column X does not exist"
- Schema out of sync
- Generate new migration and apply

### Type errors after schema change
- Restart TypeScript server
- Run: `pnpm typecheck`
