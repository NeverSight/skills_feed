---
name: zodipus
description: Prisma-to-Zod schema generator with composable Query Engine. Use when user mentions zodipus, prisma zod schemas, prisma validation, zod from prisma, query builders with zod, runtime database validation, or type-safe prisma queries.
license: MIT
metadata:
  author: zodipus
  version: "1.0.0"
---

# Zodipus

Type-safe Zod schema generator for Prisma with composable Query Engine.

## When to Apply

- User mentions "zodipus" anywhere in conversation
- User wants Zod schemas generated from Prisma
- User needs runtime validation for Prisma queries
- User asks about type-safe query builders
- User has Prisma + Zod integration questions
- User mentions "prisma-zod" or similar terms

## Quick Routing

| User Intent | Skill |
|-------------|-------|
| Install, setup, configure generator | `zodipus-setup` |
| Query engine, createRegistry, type-safe queries | `zodipus-query-engine` |
| JSON fields, @zodSchema, custom schemas | `zodipus-custom-schemas` |
| Errors, validation failed, not working | `zodipus-troubleshooting` |
| Migrate from other generators | `zodipus-migration` |

## Core Concepts

### 1. Generator
Zodipus is a Prisma generator that outputs Zod schemas:

```prisma
generator zodipus {
  provider = "zodipus"
  output   = "./generated"
}
```

### 2. Clean Schemas
Generated schemas contain **scalar fields only** (no relations). This keeps validation fast and focused:

```typescript
// Generated UserSchema validates: id, email, name, role, createdAt, updatedAt
// Does NOT include: posts, comments, profile (relations)
const user = UserSchema.parse(data);
```

### 3. Query Engine
Build composable queries with automatic validation:

```typescript
import { createRegistry } from 'zodipus/queryEngine';
import { models, modelRelations } from './generated/generated-index';

const registry = createRegistry({ models, relations: modelRelations });
const userQuery = registry.createQuery('user');

const query = userQuery({
  select: { id: true, email: true },
  posts: { select: { title: true } }
});

const result = query.parse(await prisma.user.findFirst(query.query));
// Fully typed: { id: string; email: string; posts: { title: string }[] }
```

### 4. Custom JSON Schemas
Type Prisma JSON fields with `@zodSchema`:

```prisma
model Post {
  /// @zodSchema PostMetadataSchema
  metadata Json?
}
```

## Minimal Working Example

### Step 1: Install
```bash
npm install zodipus zod
```

### Step 2: Configure
```prisma
generator client {
  provider = "prisma-client-js"
}

generator zodipus {
  provider = "zodipus"
  output   = "./generated"
}

model User {
  id    String @id @default(cuid())
  email String @unique
  name  String?
  posts Post[]
}

model Post {
  id       String  @id @default(cuid())
  title    String
  author   User    @relation(fields: [authorId], references: [id])
  authorId String
}
```

### Step 3: Generate
```bash
npx prisma generate
```

### Step 4: Use
```typescript
import { UserSchema, PostSchema } from './generated';
import { createRegistry } from 'zodipus/queryEngine';
import { models, modelRelations } from './generated/generated-index';

// Direct validation
const user = UserSchema.parse(userData);

// Query with validation
const registry = createRegistry({ models, relations: modelRelations });
const query = registry.createQuery('user')({
  select: { id: true, email: true, name: true }
});

const users = await prisma.user.findMany(query.query);
const validated = query.array().parse(users);
```

## Generated Files

After running `prisma generate`, Zodipus creates:

| File | Contents |
|------|----------|
| `enums.ts` | Prisma enums as Zod schemas |
| `models.ts` | Clean model schemas (no relations) |
| `custom-schemas.ts` | Placeholder for @zodSchema definitions |
| `generated-relations.ts` | Relation metadata for Query Engine |
| `generated-index.ts` | Re-exports and convenience exports |

## Priority Reference

| Priority | Feature | When to Use |
|----------|---------|-------------|
| **Critical** | `UserSchema.parse()` | Validate any model data |
| **Critical** | `createRegistry()` | Set up Query Engine |
| **High** | `query.array().parse()` | Validate findMany results |
| **High** | `query.safeParse()` | Handle errors without throwing |
| **Medium** | `@zodSchema` annotation | Type JSON fields |
| **Medium** | `relationDepth` config | Deep nested queries |
| **Low** | CLI inspect command | Debug schema issues |

## Quick Reference

See [references/QUICK-REFERENCE.md](references/QUICK-REFERENCE.md) for a complete cheat sheet.
