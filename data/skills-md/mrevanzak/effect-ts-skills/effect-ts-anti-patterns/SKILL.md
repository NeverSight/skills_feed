---
name: effect-ts-anti-patterns
description: Use when reviewing Effect-TS code, debugging unexpected crashes, or optimizing concurrent operations.
version: 1.0.0
---

# Effect-TS Anti-Patterns

## Overview
Effect-TS provides a powerful functional framework, but common imperative habits can bypass its safety guarantees. This skill identifies and fixes patterns that lead to resource leaks, process crashes, and unhandled errors.

## When to Use
- During code reviews of Effect-TS implementations.
- When debugging "unhandled promise rejections" or process crashes in Effect code.
- When optimizing performance of parallel operations.

**When NOT to use:**
- For simple, non-Effect TypeScript code.
- When using other functional libraries (fp-ts, etc.).

## Anti-Patterns Reference

| Anti-Pattern | Bad Code | Good Code | Why |
| :--- | :--- | :--- | :--- |
| **Run Outside Boundary** | `await Effect.runPromise(fx)` mid-function | `yield* fx` (compose) | Bypasses error channel & tracing. |
| **Missing `yield*`** | `const user = yield fetchUser()` | `const user = yield* fetchUser()` | Yields the Effect object, not the result. |
| **Throwing Errors** | `if (!ok) throw new Error()` | `yield* Effect.fail(new Error())` | `throw` creates a "Defect" (crash), not a typed error. |
| **Unbounded Parallelism** | `Effect.all(tasks)` (default) | `Effect.all(tasks, { concurrency: 10 })` | Prevents OOM and rate limit exhaustion. |
| **Ignoring Errors** | `Effect.runPromise(fx)` (no catch) | `fx.pipe(Effect.catchAll(...))` | Leads to unhandled rejections. |
| **Manual Cleanup** | `try { ... } finally { cleanup() }` | `Effect.acquireRelease(...)` | `finally` doesn't guarantee cleanup on interruption. |

## Common Mistakes

### 1. The `yield` vs `yield*` Trap
```typescript
// ❌ BAD: Missing *, yields the Effect object itself
const bad = Effect.gen(function* () {
  const user = yield fetchUser(id); // Returns Effect, not User!
});

// ✅ GOOD: yield* executes the Effect
const good = Effect.gen(function* () {
  const user = yield* fetchUser(id); // Returns User
});
```

### 2. Unbounded Parallelism
```typescript
// ❌ BAD: 10,000 concurrent requests (OOM risk)
const bad = Effect.all(urls.map(fetch));

// ✅ GOOD: Bounded to 10 concurrent
const good = Effect.all(urls.map(fetch), { concurrency: 10 });
```

### 3. Running Effects Mid-Code
```typescript
// ❌ BAD: Effect.runPromise scattered throughout
const bad = async () => {
  const user = await Effect.runPromise(getUser(id));
  const posts = await Effect.runPromise(getPosts(user.id));
};

// ✅ GOOD: Compose effects, run ONCE at boundary
const good = Effect.gen(function* () {
  const user = yield* getUser(id);
  const posts = yield* getPosts(user.id);
  return { user, posts };
});
```

## Rationalization Table

| Excuse | Reality |
| :--- | :--- |
| "I'll use `concurrency: 'unbounded'` to make it fast" | Fast = Crash. Always bound parallelism for external resources. |
| "I'll just `throw` for now" | `throw` bypasses the error channel and makes code untestable. |
| "It's easier to run it here" | Running mid-code loses the context, tracing, and interruption safety. |

## Red Flags
- `Effect.runPromise` or `Effect.runSync` inside a loop or helper function.
- `Effect.all` without a `concurrency` option on large lists.
- `throw` keyword inside an `Effect.gen` block.
- `yield` without `*` when calling an Effect.

## Cross-References
- **REQUIRED BACKGROUND:** effect-ts-fundamentals
- **REQUIRED SUB-SKILL:** effect-ts-concurrency
- **REFERENCE:** effect-ts-resources
