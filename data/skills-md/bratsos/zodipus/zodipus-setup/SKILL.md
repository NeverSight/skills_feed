---
name: zodipus-setup
description: Install and configure Zodipus Prisma generator. Use when installing zodipus, setting up generator options, configuring output paths, choosing date formats, or integrating with Next.js/Express/Fastify/tRPC.
license: MIT
metadata:
  author: zodipus
  version: "1.0.0"
---

# Zodipus Setup

Complete guide for installing and configuring Zodipus.

## When to Apply

- User is installing zodipus for the first time
- User asks about generator configuration options
- User needs framework-specific setup (Next.js, Express, tRPC)
- User wants to understand dateFormat, relationDepth, or other options
- User is setting up a new Prisma project with Zod validation

## Installation

```bash
# npm
npm install zodipus zod

# pnpm
pnpm add zodipus zod

# yarn
yarn add zodipus zod
```

**Requirements:**
- Node.js 18+
- Prisma 6.0+
- Zod 3.25.0+

## Basic Configuration

Add to your `schema.prisma`:

```prisma
generator client {
  provider = "prisma-client-js"
}

generator zodipus {
  provider = "zodipus"
  output   = "./generated"
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  posts     Post[]
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
}

enum Role {
  USER
  ADMIN
}
```

## Generate Schemas

```bash
npx prisma generate
```

This creates:
```
generated/
├── enums.ts              # RoleSchema
├── models.ts             # UserSchema, PostSchema
├── custom-schemas.ts     # Placeholder for @zodSchema
├── generated-relations.ts
└── generated-index.ts
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `provider` | string | Required | Must be `"zodipus"` |
| `output` | string | Required | Output directory for generated files |
| `relationDepth` | string | `"5"` | Maximum depth for nested relation extraction |
| `dateFormat` | string | `"coerce"` | DateTime handling: `"coerce"` or `"string"` |
| `passthroughEnabled` | string | `"false"` | Allow unknown keys in objects |
| `debug` | string | `"false"` | Enable verbose debug logging |
| `zodImport` | string | `"zod"` | Custom Zod import path |

## Date Format Options

### `dateFormat = "coerce"` (Default)
Accepts multiple input types, converts to Date:

```typescript
// All valid inputs:
UserSchema.parse({ createdAt: new Date() });           // Date object
UserSchema.parse({ createdAt: '2024-01-15T10:30:00Z' }); // ISO string
UserSchema.parse({ createdAt: 1705315800000 });        // Timestamp
```

**Use when:** Receiving data from various sources (APIs, databases, user input).

### `dateFormat = "string"`
Requires strict ISO 8601 format:

```typescript
// Only ISO strings accepted:
UserSchema.parse({ createdAt: '2024-01-15T10:30:00.000Z' }); // OK
UserSchema.parse({ createdAt: new Date() }); // Error!
```

**Use when:** Building strict APIs, need consistent date format.

## Passthrough Mode

### `passthroughEnabled = "false"` (Default)
Unknown keys are stripped:

```typescript
const data = { id: '1', email: 'a@b.com', unknownField: 'ignored' };
const user = UserSchema.parse(data);
// user = { id: '1', email: 'a@b.com' } - unknownField removed
```

**Use when:** Sanitizing input, preventing data leakage.

### `passthroughEnabled = "true"`
Unknown keys are preserved:

```typescript
const data = { id: '1', email: 'a@b.com', extra: 'kept' };
const user = UserSchema.parse(data);
// user = { id: '1', email: 'a@b.com', extra: 'kept' }
```

**Use when:** Transforming data, need to preserve extra fields.

## Relation Depth

Controls how deeply nested relations are extracted for the Query Engine:

```prisma
generator zodipus {
  relationDepth = "10"  # Allow queries 10 levels deep
}
```

**Default: 5** - Sufficient for most apps. Increase if you have deeply nested queries.

## Common Configurations

### Strict API Server
Best for REST/GraphQL APIs with strict validation:

```prisma
generator zodipus {
  provider           = "zodipus"
  output             = "./src/generated/zodipus"
  passthroughEnabled = "false"
  dateFormat         = "string"
  relationDepth      = "5"
}
```

### Flexible Data Pipeline
Best for ETL, migrations, or internal tools:

```prisma
generator zodipus {
  provider           = "zodipus"
  output             = "./generated"
  passthroughEnabled = "true"
  dateFormat         = "coerce"
  relationDepth      = "8"
}
```

### Minimal Setup
Quick start with sensible defaults:

```prisma
generator zodipus {
  provider = "zodipus"
  output   = "./generated"
}
```

## Framework Integration

### Next.js App Router

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { UserSchema } from '@/generated';
import { prisma } from '@/lib/prisma';

export async function POST(request: NextRequest) {
  const body = await request.json();

  const result = UserSchema.omit({ id: true, createdAt: true, updatedAt: true })
    .safeParse(body);

  if (!result.success) {
    return NextResponse.json({ errors: result.error.flatten() }, { status: 400 });
  }

  const user = await prisma.user.create({ data: result.data });
  return NextResponse.json(UserSchema.parse(user));
}
```

### Express.js

```typescript
// routes/users.ts
import { Router } from 'express';
import { UserSchema } from '../generated';
import { prisma } from '../lib/prisma';

const router = Router();

router.post('/', async (req, res) => {
  const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true, updatedAt: true });
  const result = CreateUserSchema.safeParse(req.body);

  if (!result.success) {
    return res.status(400).json({ errors: result.error.flatten() });
  }

  const user = await prisma.user.create({ data: result.data });
  res.json(UserSchema.parse(user));
});

export default router;
```

### tRPC

```typescript
// server/routers/user.ts
import { router, publicProcedure } from '../trpc';
import { UserSchema } from '../../generated';
import { prisma } from '../../lib/prisma';

export const userRouter = router({
  create: publicProcedure
    .input(UserSchema.omit({ id: true, createdAt: true, updatedAt: true }))
    .mutation(async ({ input }) => {
      const user = await prisma.user.create({ data: input });
      return UserSchema.parse(user);
    }),

  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input }) => {
      const user = await prisma.user.findUnique({ where: { id: input.id } });
      return user ? UserSchema.parse(user) : null;
    }),
});
```

## Verification

After setup, verify everything works:

```typescript
// test-setup.ts
import { UserSchema, RoleSchema } from './generated';
import { createRegistry } from 'zodipus/queryEngine';
import { models, modelRelations } from './generated/generated-index';

// Test schema parsing
const user = UserSchema.parse({
  id: 'test-id',
  email: 'test@example.com',
  name: null,
  role: 'USER',
  createdAt: new Date(),
  updatedAt: new Date(),
});
console.log('Schema validation:', user);

// Test Query Engine
const registry = createRegistry({ models, relations: modelRelations });
const userQuery = registry.createQuery('user');
console.log('Query Engine:', userQuery({ select: { id: true } }).query);
```

## Troubleshooting Setup

### "Cannot find module './generated'"
Run `npx prisma generate` after adding the generator.

### TypeScript errors after generation
Ensure your tsconfig includes the output directory:
```json
{
  "include": ["src/**/*", "generated/**/*"]
}
```

### ESM/CJS conflicts
Zodipus outputs CommonJS. If using ESM, ensure your bundler handles the conversion.

For detailed options, see [references/GENERATOR-OPTIONS.md](references/GENERATOR-OPTIONS.md).
