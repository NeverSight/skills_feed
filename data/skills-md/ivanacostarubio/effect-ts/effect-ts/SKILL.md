---
name: effect-ts
description: ALWAYS use this skill when writing ANY TypeScript code. All TypeScript in this project MUST use the Effect library. Use Effect for error handling (not try/catch), Effect.gen for async code (not async/await with Promises), Schema for validation (not zod/yup), Services and Layers for dependency injection, and Effect patterns for all business logic. This applies to any TypeScript file creation, modification, or code generation.
---

# Effect TypeScript Library

Effect is a powerful TypeScript library for building type-safe, composable, synchronous and asynchronous programs with:
- **Typed errors** - Track expected errors at the type level
- **Dependency injection** - Services, Context, and Layers
- **Resource management** - Safe acquisition and release
- **Concurrency** - Fiber-based lightweight threads
- **Composability** - Pipe-based functional programming

## Quick Reference

For detailed patterns and examples, see:
- [CORE.md](CORE.md) - Effect basics, creating and running effects
- [ERRORS.md](ERRORS.md) - Error handling patterns
- [SERVICES.md](SERVICES.md) - Dependency injection with Services and Layers
- [SCHEMA.md](SCHEMA.md) - Data validation with Schema
- [PATTERNS.md](PATTERNS.md) - Common patterns and best practices

## The Effect Type

```typescript
Effect<Success, Error, Requirements>
```

- `Success` (A) - The value produced on success
- `Error` (E) - Expected errors that can occur
- `Requirements` (R) - Services/dependencies needed to run

## Essential Imports

```typescript
import { Effect, pipe } from "effect"
import { Schema } from "effect"
import { Context, Layer } from "effect"
import { Option, Either } from "effect"
```

## Creating Effects

```typescript
// Success values
const success = Effect.succeed(42)
const lazy = Effect.sync(() => computeValue())

// Failures
const fail = Effect.fail(new MyError())
const die = Effect.die("unexpected error")

// From promises
const fromPromise = Effect.tryPromise({
  try: () => fetch(url),
  catch: (e) => new FetchError(e)
})

// From sync that may throw
const fromSync = Effect.try({
  try: () => JSON.parse(input),
  catch: (e) => new ParseError(e)
})
```

## Running Effects

```typescript
// Async execution
await Effect.runPromise(effect)
await Effect.runPromiseExit(effect)

// Sync execution (only for sync effects)
Effect.runSync(effect)

// Fork as fiber
const fiber = Effect.runFork(effect)
```

## Composing Effects (Generators - Recommended)

```typescript
const program = Effect.gen(function* () {
  const a = yield* getUser(id)
  const b = yield* getProfile(a.profileId)
  return { user: a, profile: b }
})
```

## Composing Effects (Pipe Style)

```typescript
const program = pipe(
  getUser(id),
  Effect.flatMap(user => getProfile(user.profileId)),
  Effect.map(profile => profile.name)
)

// Or using .pipe() method
const program = getUser(id).pipe(
  Effect.flatMap(user => getProfile(user.profileId)),
  Effect.map(profile => profile.name)
)
```

## Error Handling

```typescript
// Catch specific error
effect.pipe(
  Effect.catchTag("NotFound", (e) => Effect.succeed(defaultValue))
)

// Catch all errors
effect.pipe(
  Effect.catchAll((e) => Effect.succeed(fallback))
)

// Map errors
effect.pipe(
  Effect.mapError((e) => new WrappedError(e))
)
```

## Defining Services

```typescript
// Define service interface
class UserService extends Context.Tag("UserService")<
  UserService,
  {
    readonly getUser: (id: string) => Effect.Effect<User, NotFoundError>
    readonly saveUser: (user: User) => Effect.Effect<void, DatabaseError>
  }
>() {}

// Use service
const program = Effect.gen(function* () {
  const userService = yield* UserService
  const user = yield* userService.getUser("123")
  return user
})

// Implement as Layer
const UserServiceLive = Layer.succeed(UserService, {
  getUser: (id) => Effect.succeed({ id, name: "John" }),
  saveUser: (user) => Effect.succeed(undefined)
})

// Provide layer
Effect.runPromise(program.pipe(Effect.provide(UserServiceLive)))
```

## Schema Validation

```typescript
import { Schema } from "effect"

// Define schema
const User = Schema.Struct({
  id: Schema.String,
  name: Schema.String,
  age: Schema.Number.pipe(Schema.positive())
})

// Infer type
type User = Schema.Schema.Type<typeof User>

// Decode
const decode = Schema.decodeUnknown(User)
const result = decode({ id: "1", name: "John", age: 30 })

// Use in Effect
const parseUser = Schema.decodeUnknown(User)
const user = yield* parseUser(rawData)
```

## Concurrency

```typescript
// Run in parallel
const [a, b, c] = yield* Effect.all([effectA, effectB, effectC], {
  concurrency: "unbounded"
})

// Race - first to complete wins
const result = yield* Effect.race(effectA, effectB)

// Timeout
const result = yield* effect.pipe(Effect.timeout("5 seconds"))
```

## Resource Management

```typescript
// Scoped resource
const file = Effect.acquireRelease(
  Effect.sync(() => openFile(path)),
  (file) => Effect.sync(() => file.close())
)

// Use with scoped
const program = Effect.scoped(
  Effect.gen(function* () {
    const f = yield* file
    return yield* f.read()
  })
)
```

## API Reference

For complete API documentation: https://tim-smart.github.io/effect-io-ai/

## Official Documentation

- Getting Started: https://effect.website/docs/getting-started/introduction/
- Schema: https://effect.website/docs/schema/introduction/
- Error Management: https://effect.website/docs/error-management/two-error-types/
- Requirements (DI): https://effect.website/docs/requirements-management/services/
- Concurrency: https://effect.website/docs/concurrency/fibers/
