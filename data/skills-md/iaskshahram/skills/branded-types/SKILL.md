---
name: branded-types
description: Implement branded (nominal/opaque) types in TypeScript to prevent accidental mixing of structurally identical types. Use when writing type-safe IDs (UserId, PostId), validated strings (Email, URL), unit-specific numbers (Meters, Seconds), or any scenario requiring nominal typing in TypeScript's structural type system.
---

# Branded Types

## What & Why

TypeScript uses **structural typing** — two types with the same shape are interchangeable. This means `UserId` and `PostId` (both `string`) can be silently swapped, causing bugs:

```typescript
type UserId = string
type PostId = string

function getUser(id: UserId) { /* ... */ }

const postId: PostId = "post-123"
getUser(postId) // No error! Both are just `string`
```

**Branded types** add a compile-time-only marker that makes structurally identical types incompatible. Zero runtime overhead — brands are erased during compilation.

## Core Pattern (Recommended)

Use a generic `Brand` utility with a single `unique symbol`:

```typescript
// brand.ts
declare const __brand: unique symbol
type Brand<T, B extends string> = T & { readonly [__brand]: B }
```

Define specific branded types:

```typescript
import type { Brand } from './brand'

type UserId = Brand<string, 'UserId'>
type PostId = Brand<string, 'PostId'>
type Email  = Brand<string, 'Email'>

type Meters       = Brand<number, 'Meters'>
type Seconds      = Brand<number, 'Seconds'>
type PositiveInt  = Brand<number, 'PositiveInt'>
```

Now `UserId` and `PostId` are incompatible at compile time:

```typescript
function getUser(id: UserId) { /* ... */ }

const postId = "post-123" as PostId
getUser(postId) // TS Error: PostId is not assignable to UserId
```

## Constructor Functions

Never use bare `as` casts in application code. Create constructor/validation functions:

```typescript
function createUserId(id: string): UserId {
  if (!id || id.length === 0) throw new Error('Invalid UserId')
  return id as UserId
}

function validateEmail(input: string): Email {
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input)) {
    throw new Error('Invalid email')
  }
  return input as Email
}

function toPositiveInt(n: number): PositiveInt {
  if (!Number.isInteger(n) || n <= 0) throw new Error('Must be positive integer')
  return n as PositiveInt
}
```

The `as` cast is confined to these constructor functions — the only place it should appear.

## Implementation Variants

| Pattern | Approach | Strength | Verbosity |
|---------|----------|----------|-----------|
| **A** `__brand` property | `T & { __brand: B }` | Good | Low |
| **B** Per-type `unique symbol` | `T & { [MyBrand]: true }` | Strongest | High |
| **C** Generic `unique symbol` (recommended) | `T & { [__brand]: B }` | Strong | Low |

**Default to Pattern C** — it balances safety with ergonomics. For detailed trade-offs and full examples, see [references/patterns.md](references/patterns.md).

## Real-World Use Cases

### Type-safe IDs

```typescript
type UserId    = Brand<string, 'UserId'>
type PostId    = Brand<string, 'PostId'>
type CommentId = Brand<string, 'CommentId'>

function getPost(postId: PostId) { /* ... */ }
function deleteComment(commentId: CommentId) { /* ... */ }
```

### Validated strings

```typescript
type Email           = Brand<string, 'Email'>
type NonEmptyString  = Brand<string, 'NonEmptyString'>
type SanitizedHTML   = Brand<string, 'SanitizedHTML'>
type TranslationKey  = Brand<string, 'TranslationKey'>
```

### Unit-specific numbers

```typescript
type Meters       = Brand<number, 'Meters'>
type Feet         = Brand<number, 'Feet'>
type Seconds      = Brand<number, 'Seconds'>
type Milliseconds = Brand<number, 'Milliseconds'>
type Percentage   = Brand<number, 'Percentage'> // 0-100
```

### Tokens and sensitive values

```typescript
type AccessToken  = Brand<string, 'AccessToken'>
type RefreshToken = Brand<string, 'RefreshToken'>
type ApiKey       = Brand<string, 'ApiKey'>
```

## Anti-Patterns

### 1. Checking brand at runtime

```typescript
// WRONG — __brand does not exist at runtime
if ((value as any).__brand === 'UserId') { /* ... */ }
```

Branded types are compile-time only. For runtime checks, use your constructor/validation functions.

### 2. Bare `as` casts in application code

```typescript
// BAD — no validation, defeats the purpose
const userId = someString as UserId

// GOOD — validated constructor
const userId = createUserId(someString)
```

Confine `as` casts to constructor functions only.

### 3. Over-branding

Don't brand every `string` or `number`. Use branded types when:
- Mixing values would cause bugs (IDs, units, validated data)
- Multiple similar types exist that should not be interchangeable
- The project is large enough to benefit from the safety

### 4. Duplicate brand names across modules

```typescript
// file-a.ts — Brand<string, 'Id'>
// file-b.ts — Brand<number, 'Id'>
// These share the brand name 'Id' but mean different things!
```

Use specific, descriptive brand names: `'UserId'`, `'PostId'`, not just `'Id'`.

## Library Integrations

### Zod

```typescript
import { z } from 'zod'

const UserIdSchema = z.string().uuid().brand<'UserId'>()
type UserId = z.infer<typeof UserIdSchema> // string & Brand<'UserId'>

const parsed = UserIdSchema.parse(input) // typed as UserId
```

### Drizzle ORM

```typescript
import { text } from 'drizzle-orm/pg-core'

// Brand the column output type
const users = pgTable('users', {
  id: text('id').primaryKey().$type<UserId>(),
})

// Queries return UserId, not plain string
const user = await db.select().from(users).where(eq(users.id, userId))
```

For detailed integration examples (end-to-end flows, more libraries), see [references/integrations.md](references/integrations.md).

## When to Use Branded Types

| Scenario | Use branded types? |
|----------|-------------------|
| Multiple ID types that should not mix | Yes |
| Validated vs. unvalidated data | Yes |
| Unit-specific numbers (meters vs feet) | Yes |
| Tokens/secrets vs plain strings | Yes |
| Small script with few types | Probably not |
| Single ID type in a small project | Probably not |
| Need runtime type discrimination | Use discriminated unions instead |

## Additional Resources

- For detailed pattern comparisons: [references/patterns.md](references/patterns.md)
- For library integration examples: [references/integrations.md](references/integrations.md)
