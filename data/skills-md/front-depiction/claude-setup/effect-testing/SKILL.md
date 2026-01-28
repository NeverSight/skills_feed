---
name: effect-testing
description: Write comprehensive tests using @effect/vitest for Effect code and vitest for pure functions. Use this skill when implementing tests for Effect-based applications, including services, layers, time-dependent effects, error handling, and property-based testing.
---

# Effect Testing Skill

This skill provides comprehensive guidance for testing Effect-based applications using `@effect/vitest` and standard `vitest`.

## Framework Selection

**CRITICAL**: Choose the correct testing framework based on the code being tested.

### Use @effect/vitest for Effect Code

Use `@effect/vitest` when testing:
- Functions that return `Effect<A, E, R>`
- Code that uses services and layers
- Time-dependent operations with `TestClock`
- Asynchronous operations coordinated with Effect
- STM (Software Transactional Memory) operations

```typescript
import { it, expect } from "@effect/vitest"
import { Effect } from "effect"

declare const fetchUser: (id: string) => Effect.Effect<{ id: string }, Error>

it.effect("should fetch user", () =>
  Effect.gen(function* () {
    const user = yield* fetchUser("123")
    expect(user.id).toBe("123")
  })
)
```

### Use Regular vitest for Pure Functions

Use standard `vitest` for:
- Pure functions with no Effect wrapper
- Simple data transformations
- Helper utilities
- Type constructors (brands, newtypes)

```typescript
import { describe, expect, it } from "vitest"

declare const Cents: {
  make: (value: bigint) => bigint
  add: (a: bigint, b: bigint) => bigint
}

describe("Cents", () => {
  it("should add cents correctly", () => {
    const result = Cents.add(Cents.make(100n), Cents.make(50n))
    expect(result).toBe(150n)
  })
})
```

## Test Variants

### it.effect - Default Test Environment

Provides `TestContext` including `TestClock`, `TestRandom`, etc.

```typescript
import { it, expect } from "@effect/vitest"
import { Effect } from "effect"

declare const someEffect: Effect.Effect<number>
declare const expected: number

it.effect("test name", () =>
  Effect.gen(function* () {
    // Test implementation with TestContext available
    const result = yield* someEffect
    expect(result).toBe(expected)
  })
)
```

### it.live - Live Environment

Uses real services (real clock, real random, etc.).

```typescript
import { it } from "@effect/vitest"
import { Effect, Clock } from "effect"

it.live("test with real time", () =>
  Effect.gen(function* () {
    const now = yield* Clock.currentTimeMillis
    // Uses actual system time
  })
)
```

### it.scoped - Resource Management

For tests requiring `Scope` to manage resource lifecycle.

```typescript
import { it } from "@effect/vitest"
import { Effect } from "effect"

declare const acquire: Effect.Effect<unknown>
declare const release: Effect.Effect<void>

it.scoped("test with resources", () =>
  Effect.gen(function* () {
    const resource = yield* Effect.acquireRelease(
      acquire,
      () => release
    )
    // Resource automatically cleaned up after test
  })
)
```

### it.scopedLive - Combined Scoped + Live

Uses live environment with scope for resource management.

```typescript
import { it } from "@effect/vitest"
import { Effect } from "effect"

declare const acquireRealResource: Effect.Effect<unknown>
declare const releaseRealResource: Effect.Effect<void>

it.scopedLive("live test with resources", () =>
  Effect.gen(function* () {
    const resource = yield* Effect.acquireRelease(
      acquireRealResource,
      () => releaseRealResource
    )
  })
)
```

## Assertions

### Use expect from vitest

For all assertions, use the standard `expect` from vitest:

```typescript
import { it, expect } from "@effect/vitest"
import { Effect } from "effect"

declare const computation: Effect.Effect<number>
declare const array: unknown[]

it.effect("assertions", () =>
  Effect.gen(function* () {
    const result = yield* computation
    expect(result).toBe(42)
    expect(result).toBeGreaterThan(0)
    expect(array).toHaveLength(3)
  })
)
```

### Effect-Specific Utilities

`@effect/vitest` provides additional assertion utilities in `utils`:

```typescript
import { it } from "@effect/vitest"
import {
  assertEquals,       // Uses Effect's Equal.equals
  assertTrue,
  assertFalse,
  assertSome,        // For Option.Some
  assertNone,        // For Option.None
  assertRight,       // For Either.Right
  assertLeft,        // For Either.Left
  assertSuccess,     // For Exit.Success
  assertFailure      // For Exit.Failure
} from "@effect/vitest/utils"
import { Effect, Option, Either } from "effect"

declare const someOptionalEffect: Effect.Effect<Option.Option<number>>
declare const someEitherEffect: Effect.Effect<Either.Either<number, Error>>
declare const expectedValue: number

it.effect("with effect assertions", () =>
  Effect.gen(function* () {
    const option = yield* someOptionalEffect
    assertSome(option, expectedValue)

    const either = yield* someEitherEffect
    assertRight(either, expectedValue)
  })
)
```

## Testing with Services and Layers

### Providing Services to Tests

Use `Effect.provide` to supply test implementations:

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Context, Layer } from "effect"

class UserService extends Context.Tag("UserService")<UserService, {
  getUser: (id: string) => Effect.Effect<{ name: string }>
}>() {}

declare const TestUserServiceLayer: Layer.Layer<UserService>

it.effect("should work with dependencies", () =>
  Effect.gen(function* () {
    const userService = yield* UserService
    const result = yield* userService.getUser("123")
    expect(result.name).toBe("John")
  }).pipe(Effect.provide(TestUserServiceLayer))
)
```

### Using layer Helper

Share a layer across multiple tests with the `layer` function:

```typescript
import { layer, it, expect } from "@effect/vitest"
import { Effect, Context, Layer } from "effect"

class Database extends Context.Tag("Database")<Database, {
  query: (sql: string) => Effect.Effect<Array<unknown>>
}>() {
  static Test = Layer.succeed(Database, {
    query: (sql) => Effect.succeed([])
  })
}

layer(Database.Test)((it) => {
  it.effect("test 1", () =>
    Effect.gen(function* () {
      const db = yield* Database
      const results = yield* db.query("SELECT *")
      expect(results).toEqual([])
    })
  )

  it.effect("test 2", () =>
    Effect.gen(function* () {
      const db = yield* Database
      // Database available in all tests
    })
  )
})

// With name for describe block
layer(Database.Test)("Database tests", (it) => {
  it.effect("query test", () => Effect.succeed(true))
})
```

### Nested Layers

Compose layers for complex dependencies:

```typescript
import { layer, it } from "@effect/vitest"
import { Effect, Context, Layer } from "effect"

class Database extends Context.Tag("Database")<Database, {
  query: (sql: string) => Effect.Effect<Array<unknown>>
}>() {}

class UserService extends Context.Tag("UserService")<UserService, {
  getUser: (id: string) => Effect.Effect<unknown>
}>() {}

declare const DatabaseLayer: Layer.Layer<Database>
declare const UserServiceLayer: Layer.Layer<UserService, never, Database>

layer(DatabaseLayer)((it) => {
  it.layer(UserServiceLayer)("user tests", (it) => {
    it.effect("has both dependencies", () =>
      Effect.gen(function* () {
        const db = yield* Database
        const userService = yield* UserService
        // Both available
      })
    )
  })
})
```

### Excluding Test Services

Use live services instead of test services:

```typescript
import { layer, it } from "@effect/vitest"
import { Effect, Layer } from "effect"

declare const MyServiceLayer: Layer.Layer<never>

layer(MyServiceLayer, { excludeTestServices: true })((it) => {
  it.effect("uses real clock", () =>
    Effect.gen(function* () {
      // Uses actual Clock, not TestClock
    })
  )
})
```

## Time-Dependent Testing with TestClock

### Basic TestClock Usage

`TestClock` allows controlling time without waiting:

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, TestClock, Fiber } from "effect"

it.effect("should handle delays", () =>
  Effect.gen(function* () {
    const fiber = yield* Effect.fork(
      Effect.sleep("5 seconds").pipe(Effect.as("done"))
    )

    // Advance time by 5 seconds instantly
    yield* TestClock.adjust("5 seconds")

    const result = yield* Fiber.join(fiber)
    expect(result).toBe("done")
  })
)
```

### Testing Recurring Effects

Test periodic operations efficiently:

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Queue, TestClock, Option } from "effect"

it.effect("should execute every minute", () =>
  Effect.gen(function* () {
    const queue = yield* Queue.unbounded<number>()

    // Fork effect that repeats every minute
    yield* Effect.fork(
      Queue.offer(queue, 1).pipe(
        Effect.delay("60 seconds"),
        Effect.forever
      )
    )

    // No effect before time passes
    const empty = yield* Queue.poll(queue)
    expect(Option.isNone(empty)).toBe(true)

    // Advance time
    yield* TestClock.adjust("60 seconds")

    // Effect executed once
    const value = yield* Queue.take(queue)
    expect(value).toBe(1)

    // Verify only one execution
    const stillEmpty = yield* Queue.poll(queue)
    expect(Option.isNone(stillEmpty)).toBe(true)
  })
)
```

### Testing Clock Methods

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Clock, TestClock } from "effect"

it.effect("should track time correctly", () =>
  Effect.gen(function* () {
    const start = yield* Clock.currentTimeMillis

    yield* TestClock.adjust("1 minute")

    const end = yield* Clock.currentTimeMillis

    expect(end - start).toBeGreaterThanOrEqual(60_000)
  })
)
```

### TestClock with Deferred

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Deferred, TestClock } from "effect"

it.effect("should handle deferred with delays", () =>
  Effect.gen(function* () {
    const deferred = yield* Deferred.make<number, void>()

    yield* Effect.fork(
      Effect.sleep("10 seconds").pipe(
        Effect.zipRight(Deferred.succeed(deferred, 42))
      )
    )

    yield* TestClock.adjust("10 seconds")

    const result = yield* Deferred.await(deferred)
    expect(result).toBe(42)
  })
)
```

## Error Testing

### Testing Expected Failures

Use `Effect.flip` to convert failures to successes:

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Data } from "effect"

class UserNotFoundError extends Data.TaggedError("UserNotFoundError")<{
  userId: string
}> {}

declare const failingOperation: () => Effect.Effect<never, UserNotFoundError>

it.effect("should fail with error", () =>
  Effect.gen(function* () {
    const error = yield* Effect.flip(failingOperation())
    expect(error).toBeInstanceOf(UserNotFoundError)
    expect(error.userId).toBe("123")
  })
)
```

### Testing with Exit

Use `Effect.exit` to capture both success and failure:

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Exit } from "effect"

declare const divide: (a: number, b: number) => Effect.Effect<number, string>

it.effect("should handle success", () =>
  Effect.gen(function* () {
    const exit = yield* Effect.exit(divide(4, 2))
    expect(exit).toEqual(Exit.succeed(2))
  })
)

it.effect("should handle failure", () =>
  Effect.gen(function* () {
    const exit = yield* Effect.exit(divide(4, 0))
    expect(exit).toEqual(Exit.fail("Cannot divide by zero"))
  })
)
```

### Testing Error Types

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Exit, Cause, Context, Data } from "effect"

class NotFoundError extends Data.TaggedError("NotFoundError")<{
  id: string
}> {}

class UserService extends Context.Tag("UserService")<UserService, {
  getUser: (id: string) => Effect.Effect<unknown, NotFoundError>
}>() {}

declare const userService: {
  getUser: (id: string) => Effect.Effect<unknown, NotFoundError>
}

it.effect("should fail with specific error", () =>
  Effect.gen(function* () {
    const exit = yield* Effect.exit(
      userService.getUser("nonexistent")
    )

    if (Exit.isFailure(exit)) {
      const cause = exit.cause
      expect(Cause.isFailType(cause)).toBe(true)
      const error = Cause.failureOrCause(cause)
      expect(error).toBeInstanceOf(NotFoundError)
    } else {
      throw new Error("Expected failure")
    }
  })
)
```

## Property-Based Testing

### Using it.prop for Pure Properties

```typescript
import { FastCheck } from "effect"
import { it } from "@effect/vitest"

it.prop(
  "addition is commutative",
  [FastCheck.integer(), FastCheck.integer()],
  ([a, b]) => a + b === b + a
)

// With object syntax
it.prop(
  "multiplication distributes",
  { a: FastCheck.integer(), b: FastCheck.integer(), c: FastCheck.integer() },
  ({ a, b, c }) => a * (b + c) === a * b + a * c
)
```

### Using it.effect.prop for Effect Properties

```typescript
import { it } from "@effect/vitest"
import { Effect, Context } from "effect"
import { FastCheck } from "effect"

class Database extends Context.Tag("Database")<Database, {
  set: (key: string, value: number) => Effect.Effect<void>
  get: (key: string) => Effect.Effect<number>
}>() {}

it.effect.prop(
  "database operations are idempotent",
  [FastCheck.string(), FastCheck.integer()],
  ([key, value]) =>
    Effect.gen(function* () {
      const db = yield* Database

      yield* db.set(key, value)
      const result1 = yield* db.get(key)

      yield* db.set(key, value)
      const result2 = yield* db.get(key)

      return result1 === result2
    })
)
```

### With Schema Arbitraries

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Schema } from "effect"

const User = Schema.Struct({
  id: Schema.String,
  age: Schema.Number.pipe(Schema.between(0, 120))
})

it.effect.prop(
  "user validation works",
  { user: User },
  ({ user }) =>
    Effect.gen(function* () {
      expect(user.age).toBeGreaterThanOrEqual(0)
      expect(user.age).toBeLessThanOrEqual(120)
      return true
    })
)
```

### Configuring FastCheck

```typescript
import { it } from "@effect/vitest"
import { Effect, FastCheck } from "effect"

it.effect.prop(
  "property test",
  [FastCheck.integer()],
  ([n]) => Effect.succeed(n >= 0 || n < 0),
  {
    timeout: 10000,
    fastCheck: {
      numRuns: 1000,
      seed: 42,
      verbose: true
    }
  }
)
```

## Test Control

### Skipping Tests

```typescript
import { it } from "@effect/vitest"
import { Effect } from "effect"

declare const condition: boolean

it.effect.skip("not ready yet", () =>
  Effect.gen(function* () {
    // Will not run
  })
)

it.effect.skipIf(condition)("conditional skip", () =>
  Effect.gen(function* () {
    // Only runs if condition is false
  })
)
```

### Running Single Tests

```typescript
import { it } from "@effect/vitest"
import { Effect } from "effect"

it.effect.only("debug this test", () =>
  Effect.gen(function* () {
    // Only this test runs
  })
)
```

### Running Conditionally

```typescript
import { it } from "@effect/vitest"
import { Effect } from "effect"

it.effect.runIf(process.env.INTEGRATION_TESTS)("integration test", () =>
  Effect.gen(function* () {
    // Only runs if condition is true
  })
)
```

### Expecting Failures

```typescript
import { it, expect } from "@effect/vitest"
import { Effect } from "effect"

it.effect.fails("known failing test", () =>
  Effect.gen(function* () {
    // This test is expected to fail
    // Will pass if it fails, fail if it passes
    expect(1).toBe(2)
  })
)
```

## Testing Flaky Operations

Use `it.flakyTest` for operations that may fail intermittently:

```typescript
import { it } from "@effect/vitest"
import { Effect, Random } from "effect"

it.effect("retrying flaky operation", () =>
  it.flakyTest(
    Effect.gen(function* () {
      const random = yield* Random.nextBoolean
      if (random) {
        yield* Effect.fail("Random failure")
      }
    }),
    "5 seconds"  // Retry timeout
  )
)
```

## Logging in Tests

### Default Behavior (Suppressed)

```typescript
import { it } from "@effect/vitest"
import { Effect } from "effect"

it.effect("logs are suppressed", () =>
  Effect.gen(function* () {
    yield* Effect.log("This won't appear")
  })
)
```

### Enabling Logs

```typescript
import { it } from "@effect/vitest"
import { Effect, Logger } from "effect"

it.effect("logs visible", () =>
  Effect.gen(function* () {
    yield* Effect.log("This will appear")
  }).pipe(Effect.provide(Logger.pretty))
)

// Or use it.live
it.live("logs visible", () =>
  Effect.gen(function* () {
    yield* Effect.log("This will appear")
  })
)
```

## Testing Patterns

### Arrange-Act-Assert Pattern

```typescript
import { describe, it, expect } from "@effect/vitest"
import { Effect, Context, Layer } from "effect"

class UserService extends Context.Tag("UserService")<UserService, {
  getUser: (id: string) => Effect.Effect<{ id: string; name: string }>
}>() {}

declare const TestUserServiceLayer: Layer.Layer<UserService>

describe("UserService", () => {
  describe("getUser", () => {
    it.effect("should return user by id", () =>
      Effect.gen(function* () {
        // Arrange
        const userId = "user-123"
        const expectedUser = { id: userId, name: "Alice" }

        // Act
        const service = yield* UserService
        const user = yield* service.getUser(userId)

        // Assert
        expect(user).toEqual(expectedUser)
      }).pipe(Effect.provide(TestUserServiceLayer))
    )
  })
})
```

### Testing STM Operations

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, STM, TRef } from "effect"

it.effect("should handle concurrent updates", () =>
  Effect.gen(function* () {
    const counter = yield* TRef.make(0)

    const increment = STM.updateAndGet(counter, (n) => n + 1)

    yield* STM.commit(increment)
    yield* STM.commit(increment)

    const final = yield* STM.commit(TRef.get(counter))
    expect(final).toBe(2)
  })
)
```

### Testing CRDT Operations

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, STM } from "effect"

declare const GCounter: {
  make: (id: string) => Effect.Effect<unknown>
  increment: (counter: unknown, value: number) => STM.STM<void>
  query: (counter: unknown) => STM.STM<unknown>
  merge: (counter: unknown, state: unknown) => STM.STM<void>
  value: (counter: unknown) => STM.STM<number>
}

declare const ReplicaId: (id: string) => string

it.effect("should merge states correctly", () =>
  Effect.gen(function* () {
    const counter1 = yield* GCounter.make(ReplicaId("replica-1"))
    const counter2 = yield* GCounter.make(ReplicaId("replica-2"))

    yield* STM.commit(GCounter.increment(counter1, 10))
    yield* STM.commit(GCounter.increment(counter2, 20))

    const state2 = yield* STM.commit(GCounter.query(counter2))
    yield* STM.commit(GCounter.merge(counter1, state2))

    const result = yield* STM.commit(GCounter.value(counter1))
    expect(result).toBe(30)
  })
)
```

## Testing Checklist

Before completing a testing task, verify:

- [ ] Correct framework chosen (@effect/vitest vs vitest)
- [ ] Test variant appropriate (effect/live/scoped/scopedLive)
- [ ] Services provided via layers when needed
- [ ] TestClock used for time-dependent operations
- [ ] Errors tested with Effect.flip or Effect.exit
- [ ] Edge cases covered
- [ ] Property-based tests for general properties
- [ ] Tests are deterministic (no real time, real random unless intended)
- [ ] Test names describe behavior clearly
- [ ] Resources properly scoped and cleaned up
- [ ] All tests pass

## Common Pitfalls

### Don't Mix expect with assert

```typescript
// ❌ Wrong - mixing assertion libraries
import { it } from "@effect/vitest"
import { Effect } from "effect"

declare const result: unknown
declare const expected: unknown

it.effect("test", () =>
  Effect.gen(function* () {
    // assert.strictEqual(result, expected)  // Don't use this
  })
)

// ✅ Correct - use expect
import { it, expect } from "@effect/vitest"

it.effect("test", () =>
  Effect.gen(function* () {
    expect(result).toBe(expected)
  })
)
```

### Don't Forget to Fork for TestClock

```typescript
import { it } from "@effect/vitest"
import { Effect, TestClock, Fiber } from "effect"

// ❌ Wrong - will hang waiting for real time
it.effect("test", () =>
  Effect.gen(function* () {
    yield* Effect.sleep("5 seconds")  // Blocks!
    yield* TestClock.adjust("5 seconds")
  })
)

// ✅ Correct - fork the effect
it.effect("test", () =>
  Effect.gen(function* () {
    const fiber = yield* Effect.fork(Effect.sleep("5 seconds"))
    yield* TestClock.adjust("5 seconds")
    yield* Fiber.join(fiber)
  })
)
```

### Provide Layers to Effect, Not Test

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Layer } from "effect"

declare const someEffect: Effect.Effect<number>
declare const expected: number
declare const layer: Layer.Layer<never>

// ❌ Wrong - providing to wrong level
it.effect("test", () =>
  Effect.gen(function* () {
    const result = yield* someEffect
    expect(result).toBe(expected)
  })
)  // ❌ Can't provide to test function
// .pipe(Effect.provide(layer))

// ✅ Correct - provide to Effect
it.effect("test", () =>
  Effect.gen(function* () {
    const result = yield* someEffect
    expect(result).toBe(expected)
  }).pipe(Effect.provide(layer))  // ✅ Provide to Effect
)
```

## Running Tests

```bash
# Run all tests
bun run test

# Watch mode
bun run test:watch

# Run specific file
bun run test path/to/file.test.ts

# Run with coverage
bun run test --coverage
```

## Example: Complete Test Suite

```typescript
import { describe, expect, it, layer } from "@effect/vitest"
import { Effect, Context, Layer, TestClock, Exit } from "effect"

// Service definition
class Counter extends Context.Tag("Counter")<Counter, {
  increment: () => Effect.Effect<void>
  value: () => Effect.Effect<number>
}>() {
  static Live = Layer.effect(
    Counter,
    Effect.gen(function* () {
      let count = 0
      return {
        increment: () => Effect.sync(() => { count++ }),
        value: () => Effect.succeed(count)
      }
    })
  )
}

// Tests
layer(Counter.Live)("Counter", (it) => {
  it.effect("should start at 0", () =>
    Effect.gen(function* () {
      const counter = yield* Counter
      const value = yield* counter.value()
      expect(value).toBe(0)
    })
  )

  it.effect("should increment", () =>
    Effect.gen(function* () {
      const counter = yield* Counter
      yield* counter.increment()
      const value = yield* counter.value()
      expect(value).toBe(1)
    })
  )

  it.effect("should handle multiple increments", () =>
    Effect.gen(function* () {
      const counter = yield* Counter
      yield* counter.increment()
      yield* counter.increment()
      yield* counter.increment()
      const value = yield* counter.value()
      expect(value).toBe(3)
    })
  )
})
```

This skill ensures comprehensive, reliable testing of Effect-based applications following best practices.
