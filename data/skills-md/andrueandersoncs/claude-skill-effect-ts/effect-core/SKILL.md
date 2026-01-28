---
name: Effect Core
description: This skill should be used when the user asks about "Effect type", "creating effects", "running effects", "Effect.gen", "Effect.succeed", "Effect.fail", "Effect.sync", "Effect.promise", "Effect.tryPromise", "Effect.runPromise", "Effect.runSync", "pipe", "andThen", "flatMap", "map", "Effect basics", or needs to understand the fundamental Effect<Success, Error, Requirements> type and how to create, compose, and run effects.
version: 1.0.0
---

# Effect Core

## Overview

Effect is the foundational type in Effect-TS representing a computation that may succeed with value `A`, fail with error `E`, or require context `R`:

```typescript
Effect<Success, Error, Requirements>
// Also written as: Effect<A, E, R>
```

The key insight: Effects are **descriptions** of programs, not executed code. They must be explicitly run.

## Creating Effects

### From Synchronous Values

```typescript
import { Effect } from "effect"

// Success value
const success = Effect.succeed(42)

// Failure
const failure = Effect.fail(new Error("Something went wrong"))

// Lazy synchronous computation
const lazy = Effect.sync(() => {
  console.log("Computing...")
  return Math.random()
})

// Sync that may throw (converts exception to typed error)
const mayThrow = Effect.try({
  try: () => someLegacyFunction(),
  catch: (error) => new LegacyError({ cause: error })
})

// For JSON parsing, prefer Schema.parseJson (type-safe and validated)
const UserInput = Schema.parseJson(Schema.Struct({
  name: Schema.String,
  value: Schema.Number
}))
const parsed = Schema.decodeUnknown(UserInput)(userInput)
```

### From Asynchronous Values

```typescript
// From Promise (untyped error)
const fromPromise = Effect.promise(() => fetch("/api/data"))

// From Promise with typed error
const fromPromiseTyped = Effect.tryPromise({
  try: () => fetch("/api/data"),
  catch: (error) => new FetchError({ cause: error })
})
```

## Composing Effects

### Sequential Composition with pipe

```typescript
import { Effect, pipe } from "effect"

const program = pipe(
  Effect.succeed(1),
  Effect.map((n) => n + 1),          // Transform success value
  Effect.flatMap((n) =>              // Chain to another Effect
    Effect.succeed(n * 2)
  ),
  Effect.andThen((n) =>              // Shorthand for flatMap
    Effect.succeed(`Result: ${n}`)
  )
)
```

### Generator Syntax (Recommended)

The generator syntax (`Effect.gen`) provides cleaner, more readable code:

```typescript
const program = Effect.gen(function* () {
  const a = yield* Effect.succeed(1)
  const b = yield* Effect.succeed(2)
  const result = a + b
  return `Sum: ${result}`
})
```

Equivalent to:
```typescript
const program = Effect.succeed(1).pipe(
  Effect.flatMap((a) =>
    Effect.succeed(2).pipe(
      Effect.flatMap((b) => Effect.succeed(`Sum: ${a + b}`))
    )
  )
)
```

## Running Effects

Effects are descriptions that must be run to produce values:

```typescript
import { Effect } from "effect"

const program = Effect.succeed(42)

// Run and get Promise
const result = await Effect.runPromise(program)

// Run synchronous effect
const syncResult = Effect.runSync(Effect.succeed(42))

// Run with full Exit information
const exit = await Effect.runPromiseExit(program)
```

### Runtime Methods

| Method | Use Case |
|--------|----------|
| `Effect.runPromise` | Async effect → Promise (throws on failure) |
| `Effect.runPromiseExit` | Async effect → Promise<Exit> (never throws) |
| `Effect.runSync` | Sync effect → value (throws on async/failure) |
| `Effect.runSyncExit` | Sync effect → Exit (throws on async) |

## Key Composition Operators

### map - Transform Success Value

```typescript
Effect.succeed(5).pipe(
  Effect.map((n) => n * 2)  // Effect<number, never, never>
) // Result: 10
```

### flatMap / andThen - Chain Effects

```typescript
const getUser = (id: number) => Effect.succeed({ id, name: "Alice" })
const getPosts = (userId: number) => Effect.succeed([{ title: "Post 1" }])

const program = getUser(1).pipe(
  Effect.flatMap((user) => getPosts(user.id))
)
```

### tap - Side Effects Without Changing Value

```typescript
Effect.succeed(42).pipe(
  Effect.tap((n) => Effect.log(`Got value: ${n}`)),
  Effect.map((n) => n * 2)
)
```

### all - Combine Multiple Effects

```typescript
// Tuple of effects
const tuple = Effect.all([
  Effect.succeed(1),
  Effect.succeed("hello"),
  Effect.succeed(true)
]) // Effect<[number, string, boolean], never, never>

// Object of effects
const obj = Effect.all({
  id: Effect.succeed(1),
  name: Effect.succeed("Alice")
}) // Effect<{ id: number; name: string }, never, never>
```

## Effect vs Promise Comparison

| Promise | Effect |
|---------|--------|
| `new Promise((resolve) => resolve(1))` | `Effect.succeed(1)` |
| `Promise.reject(error)` | `Effect.fail(error)` |
| `promise.then(f)` | `effect.pipe(Effect.map(f))` |
| `promise.then(f)` (f returns Promise) | `effect.pipe(Effect.flatMap(f))` |
| `Promise.all([...])` | `Effect.all([...])` |
| `await promise` | `yield* effect` (in Effect.gen) |

## Dual APIs

Most Effect functions support both "data-first" and "data-last" (pipeable) styles:

```typescript
// Data-last (pipeable) - recommended
Effect.succeed(1).pipe(Effect.map((n) => n + 1))

// Data-first
Effect.map(Effect.succeed(1), (n) => n + 1)
```

## Best Practices

### Do

1. **Use Effect.gen for sequential code** - More readable than nested flatMaps
2. **Use typed errors** - Always define error types with Schema.TaggedError
3. **Use Schema.parseJson for JSON** - Never use raw JSON.parse()
4. **Prefer data-last (pipeable)** - Consistent with Effect ecosystem

### Don't

1. **Don't mix async/await with Effect** - Use Effect.promise at boundaries only
2. **Don't use try/catch** - Use Effect.try or Effect.tryPromise
3. **Don't throw exceptions** - Use Effect.fail with typed errors
4. **Don't use JSON.parse** - Use Schema.parseJson with a schema

## Additional Resources

For comprehensive documentation on all Effect APIs, patterns, and advanced usage, consult the full Effect documentation at `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Effect vs Promise" for migration patterns
- "Getting Started" for installation and setup
- "Basic Concurrency" for parallel execution
- "Dual APIs" for function calling conventions
