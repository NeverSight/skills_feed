---
name: effect-ts-fundamentals
description: Use when implementing type-safe, composable, and testable applications using Effect-TS, specifically for service definition, dependency injection, and sequential async logic.
version: 1.0.0
---

# Effect-TS Fundamentals

## Overview
Effect-TS provides a unified toolkit for building robust applications by treating side effects as values. It enables type-safe error handling, dependency injection, and resource management.

## When to Use
- When building complex TypeScript applications requiring strict error tracking.
- When you need to decouple implementation from interface via dependency injection.
- When managing multiple async operations that must be composed safely.

**When NOT to use:**
- Simple scripts where standard `Promise` and `try/catch` suffice.
- Projects where team overhead for learning Effect outweighs architectural benefits.

## Core Pattern
Effect replaces manual dependency passing and nested `try/catch` with a declarative, generator-based flow.

**Before (Plain TS):**
```typescript
async function getUserData(userId: string, db: Database) {
  try {
    const user = await db.findUser(userId);
    const posts = await fetchPosts(user.id);
    return { user, posts };
  } catch (e) {
    throw new Error("Failed");
  }
}
```

**After (Effect):**
```typescript
const getUserData = (userId: string) =>
  Effect.gen(function* () {
    const db = yield* DatabaseService;
    const user = yield* db.findUser(userId);
    const posts = yield* fetchPosts(user.id);
    return { user, posts };
  });
```

## Quick Reference
| Feature | Tool | Purpose |
|---------|------|---------|
| Sequential Logic | `Effect.gen` | Readable async pipelines |
| Service Definition | `Effect.Service` | Type-safe DI containers |
| Layer Composition | `Layer.merge/provide` | Wiring dependencies |

## Implementation

### 1. Modern Service Pattern
Define services with built-in accessors for seamless dependency injection.

```typescript
export class UserService extends Effect.Service<UserService>()("UserService", {
  accessors: true,
  effect: Effect.gen(function* () {
    const db = yield* DatabaseService;
    return {
      getUser: (id: string) => db.query(`SELECT * FROM users WHERE id = ${id}`)
    };
  }),
  dependencies: [DatabaseService.Default]
}) {}
```

### 2. Sequential Logic with Generators
Use `Effect.gen` and `yield*` to compose effects without callback hell or manual promise chaining.

```typescript
const getUserData = (userId: number) =>
  Effect.gen(function* () {
    const user = yield* fetchUser(userId);
    const posts = yield* fetchUserPosts(user.id);
    return { user, posts };
  });
```

### 3. Layer-Based Dependency Injection
Compose implementation layers and provide them to your program.

```typescript
const MainLayer = Layer.merge(DatabaseService.Default, LoggerService.Default);
const program = pipe(myEffect, Effect.provide(MainLayer));
```

## Common Mistakes
- **Forgetting `yield*`**: Calling an effect without `yield*` inside `Effect.gen` returns the effect itself, not its value.
- **Manual try/catch**: Use `Effect.try` or `Effect.catchTag` instead of standard `try/catch` to keep errors in the type channel.

**REQUIRED SUB-SKILLS:**
- `effect-ts-errors` for advanced error handling.
- `effect-ts-resources` for safe resource management.
