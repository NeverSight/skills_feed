---
name: zodipus-migration
description: Migrate to Zodipus from other Prisma-Zod generators like prisma-zod-generator, zod-prisma, zod-prisma-types, or zmodel. Use when switching from another Prisma validation library.
license: MIT
metadata:
  author: zodipus
  version: "1.0.0"
---

# Migration Guide

Migrate to Zodipus from other Prisma-Zod generators.

## When to Apply

- User mentions migrating from another generator
- User has existing prisma-zod-generator setup
- User wants to switch from zod-prisma or zod-prisma-types
- User asks about differences between generators
- User needs to replace existing Prisma-Zod solution

## Why Migrate to Zodipus?

| Feature | prisma-zod-generator | zod-prisma | Zodipus |
|---------|---------------------|------------|---------|
| Clean schemas (no relations) | No | No | Yes |
| Query Engine | No | No | Yes |
| Automatic result validation | No | No | Yes |
| Custom JSON schemas | Limited | No | Yes |
| Selective field validation | No | No | Yes |
| Type-safe query builder | No | No | Yes |
| Active maintenance | Limited | Limited | Yes |

---

## From prisma-zod-generator

### Step 1: Remove Old Generator

```prisma
// Before: Remove this
generator zod {
  provider = "prisma-zod-generator"
  output   = "./generated/zod"
}

// After: Add Zodipus
generator zodipus {
  provider = "zodipus"
  output   = "./generated"
}
```

### Step 2: Update Imports

**Before:**
```typescript
import {
  UserSchema,
  UserCreateInputSchema,
  UserUpdateInputSchema,
  PostSchema,
} from '@generated/zod';
```

**After:**
```typescript
import { UserSchema, PostSchema } from './generated';

// For create/update inputs, derive from schema:
const UserCreateInputSchema = UserSchema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});

const UserUpdateInputSchema = UserSchema.partial().omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});
```

### Step 3: Update Validation Code

**Before (prisma-zod-generator):**
```typescript
import { UserSchema } from '@generated/zod';

const user = UserSchema.parse(data);
// Includes relations in type, may have extra fields
```

**After (Zodipus):**
```typescript
import { UserSchema } from './generated';

// For simple validation
const user = UserSchema.parse(data);

// For queries with relations, use Query Engine
import { createRegistry } from 'zodipus/queryEngine';
import { models, modelRelations } from './generated/generated-index';

const registry = createRegistry({ models, relations: modelRelations });
const userQuery = registry.createQuery('user');

const query = userQuery({
  select: { id: true, email: true },
  posts: { select: { title: true } }
});

const result = query.parse(await prisma.user.findFirst(query.query));
```

### Step 4: Handle Relation Schemas

**Before (relations in schema):**
```typescript
// prisma-zod-generator includes relations
const userWithPosts = UserWithRelationsSchema.parse(data);
```

**After (Query Engine):**
```typescript
// Zodipus uses Query Engine for relations
const query = userQuery({
  select: { id: true, email: true, name: true },
  posts: {
    select: { id: true, title: true, published: true }
  }
});

const userWithPosts = query.parse(data);
```

### Key Differences

1. **No relation schemas** - Use Query Engine instead
2. **No input schemas** - Derive with `.omit()` and `.partial()`
3. **Cleaner output** - Only model schemas and enums
4. **Better performance** - Validates only selected fields

---

## From zod-prisma

### Step 1: Replace Generator

```prisma
// Before
generator zod {
  provider        = "zod-prisma"
  output          = "./zod"
  relationModel   = true
  modelCase       = "PascalCase"
}

// After
generator zodipus {
  provider = "zodipus"
  output   = "./generated"
}
```

### Step 2: Update Imports

**Before:**
```typescript
import { UserModel, PostModel } from './zod';
```

**After:**
```typescript
import { UserSchema, PostSchema } from './generated';
```

### Step 3: Naming Convention Changes

| zod-prisma | Zodipus |
|------------|---------|
| `UserModel` | `UserSchema` |
| `PostModel` | `PostSchema` |
| `RoleEnum` | `RoleSchema` |

### Step 4: Handle RelationModel

**Before (zod-prisma relationModel):**
```typescript
import { UserModelWithRelations } from './zod';
```

**After (Zodipus Query Engine):**
```typescript
import { createRegistry } from 'zodipus/queryEngine';
import { models, modelRelations } from './generated/generated-index';

const registry = createRegistry({ models, relations: modelRelations });
const query = registry.createQuery('user')({
  select: { id: true, email: true },
  posts: { select: { title: true } }
});
```

---

## From zod-prisma-types

### Step 1: Replace Generator

```prisma
// Before
generator zod {
  provider = "zod-prisma-types"
  output   = "./zod"
}

// After
generator zodipus {
  provider = "zodipus"
  output   = "./generated"
}
```

### Step 2: Update Imports

**Before:**
```typescript
import {
  UserSchema,
  UserCreateInputSchema,
  UserUpdateInputSchema,
  UserWhereInputSchema,
} from './zod';
```

**After:**
```typescript
import { UserSchema } from './generated';

// Create input schemas as needed
const CreateUserSchema = UserSchema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});
```

### Key Difference

zod-prisma-types generates many schema variants (Create, Update, Where, OrderBy, etc.). Zodipus generates only the core model schema - derive variants as needed.

---

## Migration Checklist

### Phase 1: Setup

- [ ] Install Zodipus: `npm install zodipus`
- [ ] Remove old generator from `schema.prisma`
- [ ] Add Zodipus generator to `schema.prisma`
- [ ] Run `npx prisma generate`

### Phase 2: Update Imports

- [ ] Find all imports from old generator
- [ ] Update to Zodipus import path
- [ ] Update schema names (if different)

### Phase 3: Refactor Relation Handling

- [ ] Identify code using relation schemas
- [ ] Set up Query Engine registry
- [ ] Replace relation schemas with Query Engine queries

### Phase 4: Derive Input Schemas

- [ ] Find all `CreateInput` / `UpdateInput` usage
- [ ] Create derived schemas with `.omit()` / `.partial()`

### Phase 5: Test

- [ ] Run existing tests
- [ ] Verify validation behavior
- [ ] Check type inference

### Phase 6: Cleanup

- [ ] Remove old generated files
- [ ] Uninstall old generator: `npm uninstall [old-package]`
- [ ] Update documentation

---

## Common Migration Patterns

### Create Input Schema

```typescript
// Reusable pattern for all models
function createInputSchema<T extends z.ZodObject<any>>(
  schema: T,
  autoFields = ['id', 'createdAt', 'updatedAt']
) {
  return schema.omit(
    Object.fromEntries(autoFields.map(f => [f, true])) as any
  );
}

const CreateUserSchema = createInputSchema(UserSchema);
const CreatePostSchema = createInputSchema(PostSchema);
```

### Update Input Schema

```typescript
function updateInputSchema<T extends z.ZodObject<any>>(
  schema: T,
  immutableFields = ['id', 'createdAt']
) {
  return schema.partial().omit(
    Object.fromEntries(immutableFields.map(f => [f, true])) as any
  );
}

const UpdateUserSchema = updateInputSchema(UserSchema);
```

### Relation Query Factory

```typescript
// Create reusable query configurations
const queries = {
  minimalUser: { select: { id: true, email: true } },
  fullUser: {
    select: { id: true, email: true, name: true, role: true },
    posts: { select: { id: true, title: true } }
  },
  minimalPost: { select: { id: true, title: true } },
  fullPost: {
    select: { id: true, title: true, content: true, published: true },
    author: { select: { id: true, name: true } }
  },
};

const userQ = registry.createQuery('user');
const fullUserQuery = userQ(queries.fullUser);
```

---

## Troubleshooting Migration

### Types Don't Match After Migration

**Cause:** Different nullability or optionality.

**Debug:**
```typescript
// Compare types
type OldUser = z.infer<typeof OldUserSchema>;
type NewUser = z.infer<typeof UserSchema>;

// Check specific fields
type OldName = OldUser['name']; // string | null ?
type NewName = NewUser['name']; // string | null ?
```

### Relation Data Not Validated

**Cause:** Using plain schema instead of Query Engine.

**Fix:** Switch to Query Engine for relation queries.

### Missing Schema Variants

**Cause:** Zodipus doesn't generate `CreateInput`, `WhereInput`, etc.

**Fix:** Derive them:
```typescript
const CreateUserInput = UserSchema.omit({ id: true, createdAt: true, updatedAt: true });
const UpdateUserInput = CreateUserInput.partial();
```

---

## Feature Comparison

| Feature | Before | After (Zodipus) |
|---------|--------|-----------------|
| Model schemas | Yes | Yes |
| Enum schemas | Yes | Yes |
| Input schemas | Auto-generated | Derive with `.omit()` |
| Relation schemas | Auto-generated | Query Engine |
| Query validation | Manual | Automatic |
| Type-safe queries | No | Yes |
| Selective validation | No | Yes |
