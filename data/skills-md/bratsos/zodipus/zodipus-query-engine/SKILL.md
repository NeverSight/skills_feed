---
name: zodipus-query-engine
description: Build type-safe, composable Prisma queries with automatic Zod validation. Use when working with createRegistry, query builders, select/include patterns, validated database queries, findMany validation, or type-safe Prisma results.
license: MIT
metadata:
  author: zodipus
  version: "1.0.0"
---

# Query Engine

Build validated, type-safe Prisma queries with automatic result validation.

## When to Apply

- User mentions "query engine" or "createRegistry"
- User wants type-safe Prisma queries
- User asks about select/include with validation
- User needs to validate Prisma query results
- User mentions "composable queries"
- User asks about relation queries with Zod

## Core Concept

The Query Engine creates **composable query builders** that:
1. Generate Prisma query objects (`select`, `include`)
2. Provide matching Zod schemas for validation
3. Infer TypeScript types automatically

```
User Request → Query Builder → Prisma Query + Zod Schema → Validated Result
```

## Setup

```typescript
import { createRegistry } from 'zodipus/queryEngine';
import { models, modelRelations } from './generated/generated-index';

// Create registry with all models
const registry = createRegistry({
  models,
  relations: modelRelations,
});

// Create query builders for each model you need
const userQuery = registry.createQuery('user');
const postQuery = registry.createQuery('post');
const commentQuery = registry.createQuery('comment');
```

## Basic Patterns

### Pattern 1: Select Specific Fields

Select only the fields you need. Validation matches your selection.

```typescript
const query = userQuery({
  select: { id: true, email: true, name: true }
});

// query.query = { select: { id: true, email: true, name: true } }
const user = await prisma.user.findFirst(query.query);

// Validates and types only selected fields
const validated = query.parse(user);
// Type: { id: string; email: string; name: string | null }
```

### Pattern 2: Include Relations

Include related records with their own field selection.

```typescript
const query = userQuery({
  select: { id: true, email: true },
  posts: {
    select: { id: true, title: true, published: true }
  }
});

const users = await prisma.user.findMany(query.query);
const validated = query.array().parse(users);
// Type: {
//   id: string;
//   email: string;
//   posts: { id: string; title: string; published: boolean }[]
// }[]
```

### Pattern 3: Nested Relations

Chain relations as deeply as your `relationDepth` allows.

```typescript
const query = userQuery({
  select: { id: true, name: true },
  posts: {
    select: { title: true },
    comments: {
      select: { content: true, createdAt: true },
      author: {
        select: { name: true, email: true }
      }
    }
  }
});

// 4 levels deep: User → posts → comments → author
```

### Pattern 4: Array Results (findMany)

Use `.array()` for validating arrays of results.

```typescript
const query = userQuery({
  select: { id: true, email: true }
});

const users = await prisma.user.findMany(query.query);

// Validate array
const validated = query.array().parse(users);
// Type: { id: string; email: string }[]
```

### Pattern 5: Safe Parsing

Handle validation errors without throwing.

```typescript
const result = query.safeParse(data);

if (result.success) {
  // result.data is fully typed
  console.log(result.data.email);
} else {
  // result.error is ZodError
  console.error(result.error.issues);
  console.error(result.error.format()); // Formatted errors
}
```

### Pattern 6: Partial Validation

For PATCH endpoints or partial updates.

```typescript
const query = userQuery({
  select: { id: true, email: true, name: true }
});

// Make all fields optional
const partialQuery = query.partial();

const updates = partialQuery.parse({ name: 'New Name' });
// Type: { id?: string; email?: string; name?: string | null }
```

## Advanced Patterns

### Combining with Prisma Where/OrderBy

The Query Engine generates `select`/`include` objects. Combine with your own conditions:

```typescript
const query = userQuery({
  select: { id: true, email: true, name: true },
  posts: { select: { title: true } }
});

// Add where, orderBy, pagination
const users = await prisma.user.findMany({
  ...query.query,
  where: { role: 'ADMIN' },
  orderBy: { createdAt: 'desc' },
  take: 10,
  skip: 0,
});

const validated = query.array().parse(users);
```

### Reusable Query Fragments

Create reusable query configurations:

```typescript
// Define reusable configs
const minimalUser = { select: { id: true, email: true } } as const;
const fullUser = {
  select: { id: true, email: true, name: true, role: true },
  posts: { select: { id: true, title: true } }
} as const;

// Use them
const minimalQuery = userQuery(minimalUser);
const fullQuery = userQuery(fullUser);
```

### Conditional Relations

Include relations conditionally:

```typescript
function getUserQuery(includePosts: boolean) {
  const base = { select: { id: true, email: true, name: true } };

  if (includePosts) {
    return userQuery({
      ...base,
      posts: { select: { id: true, title: true } }
    });
  }

  return userQuery(base);
}
```

### Type Extraction

Extract types from queries:

```typescript
import { z } from 'zod';

const query = userQuery({
  select: { id: true, email: true },
  posts: { select: { title: true } }
});

// Extract the validated type
type UserWithPosts = z.infer<ReturnType<typeof query.parse>>;
// or
type UserWithPosts = z.output<typeof query>;
```

## API Reference

### `createRegistry(config)`

Creates a registry for building queries.

```typescript
const registry = createRegistry({
  models,           // From generated-index.ts
  relations: modelRelations,  // From generated-index.ts
});
```

### `registry.createQuery(modelName)`

Returns a query builder function for the specified model.

```typescript
const userQuery = registry.createQuery('user');
const postQuery = registry.createQuery('post');
```

### Query Builder Return Object

```typescript
const query = userQuery({ select: { id: true } });

query.query       // Prisma query object: { select: { id: true } }
query.parse()     // Validates single result (throws on error)
query.safeParse() // Validates single result (returns result object)
query.array()     // Returns schema for validating arrays
query.partial()   // Returns schema with all fields optional
```

## Priority Patterns

| Priority | Pattern | When to Use |
|----------|---------|-------------|
| **Critical** | `query.parse(result)` | Validate findFirst/findUnique results |
| **Critical** | `query.array().parse(results)` | Validate findMany results |
| **High** | `query.safeParse(result)` | When you need error handling |
| **High** | Nested relations | Querying with related data |
| **Medium** | `query.partial()` | PATCH endpoints, partial updates |
| **Medium** | Combining with where/orderBy | Filtered queries |
| **Low** | Type extraction | Advanced TypeScript usage |

## Common Mistakes

### Mistake 1: Forgetting `.array()` for findMany

```typescript
// Wrong - will fail validation
const users = await prisma.user.findMany(query.query);
const validated = query.parse(users); // Error: expected object, got array

// Correct
const validated = query.array().parse(users);
```

### Mistake 2: Using query.query as the whole argument

```typescript
// Wrong - overwrites your conditions
const user = await prisma.user.findFirst(query.query); // OK
const user = await prisma.user.findFirst({
  query.query, // Syntax error!
  where: { id: '123' }
});

// Correct - spread the query
const user = await prisma.user.findFirst({
  ...query.query,
  where: { id: '123' }
});
```

### Mistake 3: Accessing unselected fields

```typescript
const query = userQuery({ select: { id: true } });
const user = query.parse(result);

// Wrong - 'email' wasn't selected
console.log(user.email); // TypeScript error

// Correct - add 'email' to select
const query = userQuery({ select: { id: true, email: true } });
```

For more patterns, see [references/QUERY-PATTERNS.md](references/QUERY-PATTERNS.md).
