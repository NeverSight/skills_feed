---
name: effect
description: Explains basic effect usage and terms. Use when using effect in typescript.
---

# Effect Basics

## The Effect Type

```ts
Effect<Success, Error, Requirements>
```

- **Lazy**: describes a workflow, doesn't execute until run
- **Immutable**: every operation returns a new Effect
- Aliases: `A` (success), `E` (error), `R` (requirements)

## Creating Effects

| Combinator      | Input                              | Output                        |
| --------------- | ---------------------------------- | ----------------------------- |
| `succeed`       | `A`                                | `Effect<A>`                   |
| `fail`          | `E`                                | `Effect<never, E>`            |
| `sync`          | `() => A`                          | `Effect<A>`                   |
| `try`           | `() => A`                          | `Effect<A, UnknownException>` |
| `try`           | `{ try, catch }`                   | `Effect<A, E>`                |
| `promise`       | `() => Promise<A>`                 | `Effect<A>`                   |
| `tryPromise`    | `() => Promise<A>`                 | `Effect<A, UnknownException>` |
| `tryPromise`    | `{ try, catch }`                   | `Effect<A, E>`                |
| `async`         | `(resume) => void`                 | `Effect<A, E>`                |
| `suspend`       | `() => Effect<A, E, R>`            | `Effect<A, E, R>`             |

```ts
import { Effect } from "effect"

const ok = Effect.succeed(42)
const err = Effect.fail(new Error("oops"))
const sync = Effect.sync(() => console.log("hi"))
const trySync = Effect.try(() => JSON.parse(str))
const tryAsync = Effect.tryPromise(() => fetch(url))
```

Use `suspend` for:
- Lazy evaluation with side effects
- Recursive effects (prevents stack overflow)
- Unifying return types

## Running Effects

| Runner           | Output                |
| ---------------- | --------------------- |
| `runSync`        | `A` (throws on async) |
| `runPromise`     | `Promise<A>`          |
| `runFork`        | `RuntimeFiber<A, E>`  |

```ts
Effect.runSync(program)           // sync only
Effect.runPromise(program)        // async
Effect.runFork(program)           // background fiber
```

## When to Run Effects

**Run effects ONLY at program edges:**
- Entry point (`main`)
- Controller/route handlers
- Event handlers

**Anti-pattern** - wrapping effects in async functions:
```ts
// BAD: runs effect mid-chain
async function getUser(id: string) {
  return Effect.runPromise(fetchUser(id))
}

// GOOD: return the effect, run at edge
const getUser = (id: string): Effect.Effect<User, Error> =>
  fetchUser(id)
```

## Pipelines

| Operator  | Purpose                                      |
| --------- | -------------------------------------------- |
| `map`     | Transform success value: `A => B`            |
| `flatMap` | Chain effects: `A => Effect<B, E, R>`        |
| `andThen` | Flexible chain (value, fn, Effect, Promise)  |
| `tap`     | Side effect, keeps original value            |
| `all`     | Combine effects into tuple/struct            |

```ts
import { Effect, pipe } from "effect"

const program = pipe(
  fetchAmount,
  Effect.map((n) => n * 2),
  Effect.flatMap((n) => applyDiscount(n)),
  Effect.tap((n) => Console.log(`Result: ${n}`))
)

// or with .pipe method
const program2 = fetchAmount.pipe(
  Effect.andThen((n) => n * 2),
  Effect.andThen((n) => applyDiscount(n))
)

// combine multiple effects
const both = Effect.all([effectA, effectB])
const struct = Effect.all({ a: effectA, b: effectB })
```

## Generators

```ts
const program = Effect.gen(function* () {
  const a = yield* effectA
  const b = yield* effectB
  return a + b
})
```

Supports standard control flow:
```ts
Effect.gen(function* () {
  const user = yield* getUser(id)
  if (!user) {
    return yield* Effect.fail("not found")
  }
  return user.name
})
```

## Gen vs Pipe: When to Use

**Use `Effect.gen` when:**
- Control flow needed (`if`/`else`, `for`, `while`, early returns)
- Multiple dependent sequential steps

**Use `pipe` when:**
- Linear transformations
- Simple chains without branching

## Tagged Errors

```ts
import { Effect, Data } from "effect"

class NotFound extends Data.TaggedError("NotFound")<{
  id: string
}> {}

class Unauthorized extends Data.TaggedError("Unauthorized")<{}> {}

const program: Effect.Effect<User, NotFound | Unauthorized> = 
  Effect.gen(function* () {
    // ...
    yield* Effect.fail(new NotFound({ id }))
  })

// Handle specific errors
program.pipe(
  Effect.catchTag("NotFound", (e) => Effect.succeed(null)),
  Effect.catchTag("Unauthorized", () => Effect.fail("denied"))
)
```

## Short-Circuiting

Effects stop at first error:
```ts
Effect.gen(function* () {
  yield* task1          // runs
  yield* Effect.fail(e) // fails here
  yield* task2          // never runs
})
```

Use `Effect.all` with `{ mode: "either" }` to collect all results regardless of failures.

## Additional Resources

[For pattern matching](./effect-match.md)
[For working with streams](./effect-stream.md)
[Advanced concurrency (when basics aren't enough)](./effect-advanced-concurrency.md)
[One-time signaling between fibers](./effect-deferred.md)
[Producer-consumer with back-pressure](./effect-queue.md)
[Broadcasting messages to multiple subscribers](./effect-pubsub.md)
[Limiting concurrent access to a resource](./effect-semaphore.md)
[Blocking fibers until a condition/event](./effect-latch.md)
[Concurrent-safe LRU caching with TTL](./effect-cache.md)
