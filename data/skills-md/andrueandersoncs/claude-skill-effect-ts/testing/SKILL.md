---
name: Testing
description: This skill should be used when the user asks about "Effect testing", "@effect/vitest", "it.effect", "it.live", "it.scoped", "it.layer", "it.prop", "Schema Arbitrary", "property-based testing", "fast-check", "TestClock", "testing effects", "mocking services", "test layers", "TestContext", "Effect.provide test", "time testing", "Effect test utilities", "unit testing Effect", "generating test data", "flakyTest", "test coverage", "100% coverage", "service testing", "test doubles", "mock services", or needs to understand how to test Effect-based code.
version: 1.2.0
---

# Testing in Effect

## Overview

Effect testing uses **`@effect/vitest`** as the standard test runner integration. This package provides Effect-aware test functions that handle Effect execution, scoped resources, layer composition, and TestClock injection automatically.

**The two pillars of Effect testing that enable 100% test coverage:**

1. **Service-Oriented Architecture** — Every external/effectful dependency (API calls, databases, file systems, third-party services, clocks, random number generators) MUST be wrapped in an Effect Service using `Context.Tag`. Tests provide test implementations via Layers, giving you complete control over all I/O and side effects.

2. **Schema-Driven Property Testing** — Since every data type has a Schema, every data type can generate test data via `Arbitrary`. This makes property-based testing the primary approach for verifying domain logic across thousands of automatically generated inputs.

Together, these two pillars mean: **services eliminate external dependencies from tests, and Arbitrary eliminates hand-crafted test data.** The result is fast, deterministic, comprehensive tests with 100% coverage.

**Core testing tools:**

- **@effect/vitest** - Effect-native test runner (`it.effect`, `it.scoped`, `it.live`, `it.layer`, `it.prop`)
- **Effect Services + Test Layers** - Replace ALL external dependencies with test doubles via `Context.Tag` and `it.layer`
- **Schema.Arbitrary** - Generate test data from any Schema (primary approach — never hand-craft test data)
- **Property Testing** - Test invariants with generated data via `it.prop` or fast-check
- **TestClock** - Control time in tests (automatically provided by `it.effect`)

## The Service-Oriented Testing Pattern (CRITICAL)

**This is the most important testing pattern in Effect.** Every external or effectful operation MUST be wrapped in a Service so that tests can provide a test implementation. This is how you achieve 100% test coverage without hitting real APIs, databases, or file systems.

### The Rule

> **If it makes a network call, reads from disk, talks to a database, calls a third-party API, generates random values, or performs any I/O — it MUST be behind an Effect Service.**

### Why Services Are Required for Testing

Without services, your code is **untestable** because it directly depends on external systems:

```typescript
// ❌ UNTESTABLE: Direct API call baked into business logic
const getUser = (id: string) =>
  Effect.tryPromise({
    try: () => fetch(`/api/users/${id}`).then((r) => r.json()),
    catch: (error) => new NetworkError({ cause: error })
  })

// ❌ UNTESTABLE: Direct database access
const saveOrder = (order: Order) =>
  Effect.tryPromise({
    try: () => db.query("INSERT INTO orders ...", order),
    catch: (error) => new DatabaseError({ cause: error })
  })
```

With services, your business logic is **pure and fully testable**:

```typescript
// ✅ TESTABLE: Service abstraction for API calls
class UserApi extends Context.Tag("UserApi")<
  UserApi,
  {
    readonly getUser: (id: string) => Effect.Effect<User, UserNotFound | NetworkError>
    readonly saveUser: (user: User) => Effect.Effect<void, NetworkError>
  }
>() {}

// ✅ TESTABLE: Service abstraction for database
class OrderRepository extends Context.Tag("OrderRepository")<
  OrderRepository,
  {
    readonly save: (order: Order) => Effect.Effect<void, DatabaseError>
    readonly findById: (id: string) => Effect.Effect<Order, OrderNotFound>
  }
>() {}

// ✅ Business logic is pure — depends only on service interfaces
const processOrder = (orderId: string) =>
  Effect.gen(function* () {
    const userApi = yield* UserApi
    const orderRepo = yield* OrderRepository

    const order = yield* orderRepo.findById(orderId)
    const user = yield* userApi.getUser(order.userId)
    // ... pure business logic using service abstractions
  })
```

### What MUST Be a Service

Every one of these MUST be wrapped in a `Context.Tag` service:

| External Dependency | Service Example |
|---|---|
| REST/GraphQL API calls | `UserApi`, `PaymentGateway`, `NotificationService` |
| Database operations | `UserRepository`, `OrderRepository` |
| File system access | `FileStorage`, `ConfigReader` |
| Third-party SDKs | `StripeClient`, `SendGridClient`, `AwsS3Client` |
| Email/SMS sending | `EmailService`, `SmsService` |
| Message queues | `EventPublisher`, `QueueConsumer` |
| Caching systems | `CacheService`, `RedisClient` |
| Authentication providers | `AuthProvider`, `TokenService` |
| External clock/time | Use Effect's built-in `Clock` service |
| Random values | Use Effect's built-in `Random` service |

### Complete Service + Test Layer Pattern

```typescript
import { Context, Effect, Layer, Schema } from "effect"

// 1. Define the service interface
class PaymentGateway extends Context.Tag("PaymentGateway")<
  PaymentGateway,
  {
    readonly charge: (amount: number, currency: string) => Effect.Effect<PaymentResult, PaymentError>
    readonly refund: (transactionId: string) => Effect.Effect<void, RefundError>
  }
>() {}

// 2. Live implementation (used in production)
const PaymentGatewayLive = Layer.succeed(PaymentGateway, {
  charge: (amount, currency) =>
    Effect.tryPromise({
      try: () => stripe.charges.create({ amount, currency }),
      catch: (error) => new PaymentError({ cause: error })
    }),
  refund: (transactionId) =>
    Effect.tryPromise({
      try: () => stripe.refunds.create({ charge: transactionId }),
      catch: (error) => new RefundError({ cause: error })
    })
})

// 3. Test implementation (used in tests — NO real API calls)
const PaymentGatewayTest = Layer.succeed(PaymentGateway, {
  charge: (amount, currency) =>
    Effect.succeed(new PaymentResult({
      transactionId: "test-txn-001",
      amount,
      currency,
      status: "succeeded"
    })),
  refund: (_transactionId) => Effect.void
})

// 4. Test with the test layer — 100% coverage, zero external calls
import { it, expect, layer } from "@effect/vitest"

layer(PaymentGatewayTest)("PaymentService", (it) => {
  it.effect("should process payment", () =>
    Effect.gen(function* () {
      const gateway = yield* PaymentGateway
      const result = yield* gateway.charge(1000, "usd")
      expect(result.status).toBe("succeeded")
    })
  )

  it.effect("should handle refund", () =>
    Effect.gen(function* () {
      const gateway = yield* PaymentGateway
      yield* gateway.refund("test-txn-001")
      // No error = success
    })
  )
})
```

### Stateful Test Layers (for Repository Testing)

For services that need to maintain state across operations within a test, use `Layer.effect` with `Ref`:

```typescript
import { Effect, Layer, Ref, Option } from "effect"

const OrderRepositoryTest = Layer.effect(
  OrderRepository,
  Effect.gen(function* () {
    const store = yield* Ref.make<Map<string, Order>>(new Map())

    return {
      save: (order: Order) =>
        Ref.update(store, (m) => new Map(m).set(order.id, order)),

      findById: (id: string) =>
        Effect.gen(function* () {
          const orders = yield* Ref.get(store)
          return yield* Option.match(Option.fromNullable(orders.get(id)), {
            onNone: () => Effect.fail(new OrderNotFound({ orderId: id })),
            onSome: Effect.succeed
          }).pipe(Effect.flatten)
        }),

      findAll: () =>
        Ref.get(store).pipe(Effect.map((m) => Array.from(m.values())))
    }
  })
)
```

### Composing Multiple Test Layers

Real tests often need multiple services. Compose test layers with `Layer.merge`:

```typescript
const TestEnv = Layer.merge(
  UserApiTest,
  Layer.merge(OrderRepositoryTest, PaymentGatewayTest)
)

layer(TestEnv)("Order Processing", (it) => {
  it.effect("should process complete order flow", () =>
    Effect.gen(function* () {
      const userApi = yield* UserApi
      const orderRepo = yield* OrderRepository
      const gateway = yield* PaymentGateway

      // Full integration test with ALL services mocked
      const user = yield* userApi.getUser("user-123")
      const order = yield* orderRepo.findById("order-456")
      const payment = yield* gateway.charge(order.total, "usd")

      expect(payment.status).toBe("succeeded")
    })
  )
})
```

### Combining Services with Property Testing

The ultimate testing pattern: **service test layers + Schema Arbitrary.** This lets you test business logic across thousands of generated inputs with all external dependencies controlled:

```typescript
import { it, expect, layer } from "@effect/vitest"
import { Schema, Arbitrary, Effect } from "effect"

layer(TestEnv)("Order Processing Properties", (it) => {
  it.effect.prop(
    "should calculate correct total for any valid order",
    [Arbitrary.make(Order)],
    ([order]) =>
      Effect.gen(function* () {
        const orderRepo = yield* OrderRepository
        yield* orderRepo.save(order)
        const saved = yield* orderRepo.findById(order.id)
        expect(saved.total).toBe(order.items.reduce((sum, i) => sum + i.price, 0))
      })
  )

  it.effect.prop(
    "should never charge negative amounts",
    [Arbitrary.make(Order)],
    ([order]) =>
      Effect.gen(function* () {
        const gateway = yield* PaymentGateway
        const result = yield* gateway.charge(order.total, "usd")
        expect(result.amount).toBeGreaterThanOrEqual(0)
      })
  )
})
```

## Setup

Install `@effect/vitest` alongside vitest (v1.6.0+):

```bash
pnpm add -D vitest @effect/vitest
```

Enable Effect-aware equality in your test setup:

```typescript
// vitest.setup.ts (or at top of test files)
import { addEqualityTesters } from "@effect/vitest"

addEqualityTesters()
```

## @effect/vitest - Core Test Functions

### it.effect - Standard Effect Tests

**Use `it.effect` for all Effect tests.** It automatically provides `TestContext` (including `TestClock`) and runs the Effect to completion. No `async`/`await` or `Effect.runPromise` needed.

```typescript
import { it, expect } from "@effect/vitest"
import { Effect } from "effect"

it.effect("should return user", () =>
  Effect.gen(function* () {
    const user = yield* getUser("123")
    expect(user.name).toBe("Alice")
  })
)
```

**NEVER use plain vitest `it` with `Effect.runPromise` when `it.effect` is available:**

```typescript
// ❌ FORBIDDEN: manual Effect.runPromise in async test
import { it, expect } from "vitest"

it("should return user", async () => {
  const result = await Effect.runPromise(getUser("123"))
  expect(result.name).toBe("Alice")
})

// ✅ REQUIRED: it.effect handles execution automatically
import { it, expect } from "@effect/vitest"

it.effect("should return user", () =>
  Effect.gen(function* () {
    const user = yield* getUser("123")
    expect(user.name).toBe("Alice")
  })
)
```

### it.scoped - Tests with Resource Management

Use `it.scoped` when your test needs a `Scope` (e.g., acquireRelease resources). The scope is automatically closed when the test ends.

```typescript
import { it, expect } from "@effect/vitest"
import { Effect } from "effect"

it.scoped("should manage database connection", () =>
  Effect.gen(function* () {
    const conn = yield* acquireDbConnection  // acquireRelease resource
    const result = yield* conn.query("SELECT 1")
    expect(result).toBeDefined()
    // Connection is automatically released when test ends
  })
)
```

### it.live - Tests with Live Environment

Use `it.live` when you need the real runtime environment (real clock, real logger) instead of test services.

```typescript
import { it, expect } from "@effect/vitest"
import { Effect } from "effect"

it.live("should measure real time", () =>
  Effect.gen(function* () {
    const start = Date.now()
    yield* Effect.sleep("10 millis")
    const elapsed = Date.now() - start
    expect(elapsed).toBeGreaterThanOrEqual(10)
  })
)
```

- `it.scopedLive` combines scoped resources with the live environment.

### it.layer - Tests with Shared Layers

Use `it.layer` to provide dependencies to a group of tests. The layer is constructed once and shared across all tests in the block.

```typescript
import { it, expect, layer } from "@effect/vitest"
import { Effect, Layer, Context } from "effect"

class UserRepository extends Context.Tag("UserRepository")<
  UserRepository,
  {
    readonly findById: (id: string) => Effect.Effect<User, UserNotFound>
    readonly save: (user: User) => Effect.Effect<void>
  }
>() {}

const TestUserRepo = Layer.succeed(UserRepository, {
  findById: (id) =>
    id === "123"
      ? Effect.succeed(new User({ id: "123", name: "Alice", email: "alice@test.com" }))
      : Effect.fail(new UserNotFound({ userId: id })),
  save: () => Effect.void
})

// Top-level layer wrapping a describe block
layer(TestUserRepo)("UserService", (it) => {
  it.effect("should find user by id", () =>
    Effect.gen(function* () {
      const repo = yield* UserRepository
      const user = yield* repo.findById("123")
      expect(user.name).toBe("Alice")
    })
  )

  it.effect("should fail for missing user", () =>
    Effect.gen(function* () {
      const repo = yield* UserRepository
      const exit = yield* Effect.exit(repo.findById("unknown"))
      expect(exit._tag).toBe("Failure")
    })
  )
})

// Nested layers for composing dependencies
layer(TestUserRepo)("nested layers", (it) => {
  it.layer(AnotherLayer)((it) => {
    it.effect("has both dependencies", () =>
      Effect.gen(function* () {
        const repo = yield* UserRepository
        const other = yield* AnotherService
        // Both available
      })
    )
  })
})
```

### Test Modifiers

All test variants support standard Vitest modifiers:

```typescript
it.effect.skip("temporarily disabled", () => Effect.sync(() => {}))
it.effect.only("run only this test", () => Effect.sync(() => {}))
it.effect.fails("expected to fail", () => Effect.fail(new Error("expected")))

// Conditional execution
it.effect.skipIf(process.env.CI)("skip on CI", () => Effect.sync(() => {}))
it.effect.runIf(process.env.CI)("only on CI", () => Effect.sync(() => {}))

// Parameterized tests
it.effect.each([1, 2, 3])("processes %d", (num) =>
  Effect.gen(function* () {
    const result = yield* processNumber(num)
    expect(result).toBeGreaterThan(0)
  })
)
```

### it.flakyTest - Retry Flaky Tests

Use `it.flakyTest` for tests that may not succeed on the first attempt due to timing, external dependencies, or randomness:

```typescript
import { it } from "@effect/vitest"
import { Effect } from "effect"

it.effect("should eventually succeed", () =>
  it.flakyTest(
    unreliableExternalCall(),
    "5 seconds"  // Max retry duration
  )
)
```

## Property-Based Testing

### it.prop - Schema-Aware Property Tests

`it.prop` integrates property-based testing directly into `@effect/vitest`. It accepts Schema types or fast-check Arbitraries.

```typescript
import { it, expect } from "@effect/vitest"
import { Schema } from "effect"

// Array form with positional arguments
it.prop("addition is commutative", [Schema.Int, Schema.Int], ([a, b]) => {
  expect(a + b).toBe(b + a)
})

// Object form with named arguments
it.prop(
  "validates user fields",
  {
    name: Schema.NonEmptyString,
    age: Schema.Number.pipe(Schema.int(), Schema.between(0, 150))
  },
  ({ name, age }) => {
    expect(name.length).toBeGreaterThan(0)
    expect(age).toBeGreaterThanOrEqual(0)
  }
)

// Effect-based property test
it.effect.prop(
  "async property",
  [Schema.String],
  ([input]) =>
    Effect.gen(function* () {
      const result = yield* processInput(input)
      expect(result).toBeDefined()
    })
)

// With fast-check options
it.prop(
  "with custom runs",
  [Schema.Int],
  ([n]) => { expect(n + 0).toBe(n) },
  { fastCheck: { numRuns: 1000 } }
)
```

### Schema.Arbitrary - Generating Test Data

Every Schema can generate random valid test data. This is the foundation of Effect testing.

```typescript
import { Schema, Arbitrary } from "effect"
import * as fc from "fast-check"

// Define your schema (you should already have this)
class User extends Schema.Class<User>("User")({
  id: Schema.String.pipe(Schema.minLength(1)),
  name: Schema.String.pipe(Schema.minLength(1)),
  email: Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/)),
  age: Schema.Number.pipe(Schema.int(), Schema.between(0, 150))
}) {}

// Create an arbitrary from the schema
const UserArbitrary = Arbitrary.make(User)

// Generate test data
fc.sample(UserArbitrary(fc), 3)
// => [
//   User { id: "a", name: "xyz", email: "foo@bar.com", age: 42 },
//   User { id: "test", name: "b", email: "x@y.z", age: 0 },
//   ...
// ]
```

### With Schema.TaggedClass (Discriminated Unions)

```typescript
import { Schema, Arbitrary, Match } from "effect"
import * as fc from "fast-check"

class Pending extends Schema.TaggedClass<Pending>()("Pending", {
  orderId: Schema.String,
  items: Schema.Array(Schema.String)
}) {}

class Shipped extends Schema.TaggedClass<Shipped>()("Shipped", {
  orderId: Schema.String,
  items: Schema.Array(Schema.String),
  trackingNumber: Schema.String
}) {}

class Delivered extends Schema.TaggedClass<Delivered>()("Delivered", {
  orderId: Schema.String,
  items: Schema.Array(Schema.String),
  deliveredAt: Schema.Date
}) {}

const Order = Schema.Union(Pending, Shipped, Delivered)
type Order = Schema.Schema.Type<typeof Order>

// Arbitrary for the entire union - generates all variants
const OrderArbitrary = Arbitrary.make(Order)

// Arbitrary for specific variants
const PendingArbitrary = Arbitrary.make(Pending)
const ShippedArbitrary = Arbitrary.make(Shipped)
```

### Customizing Arbitrary Generation

Use `Schema.annotations` to control generated values:

```typescript
const Email = Schema.String.pipe(
  Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/),
  Schema.annotations({
    arbitrary: () => (fc) =>
      fc.emailAddress()  // Use fast-check's email generator
  })
)

const UserId = Schema.String.pipe(
  Schema.minLength(1),
  Schema.annotations({
    arbitrary: () => (fc) =>
      fc.uuid()  // Generate UUIDs
  })
)

const Age = Schema.Number.pipe(
  Schema.int(),
  Schema.between(18, 100),
  Schema.annotations({
    arbitrary: () => (fc) =>
      fc.integer({ min: 18, max: 100 })
  })
)
```

## Property-Based Testing Patterns

### Round-Trip Testing (Encode/Decode)

Every Schema should pass round-trip testing:

```typescript
import { it, expect } from "@effect/vitest"
import { Schema, Arbitrary } from "effect"
import * as fc from "fast-check"

describe("User schema", () => {
  const UserArbitrary = Arbitrary.make(User)

  it.prop("should survive encode/decode round-trip", [UserArbitrary], ([user]) => {
    const encoded = Schema.encodeSync(User)(user)
    const decoded = Schema.decodeUnknownSync(User)(encoded)

    // Verify structural equality
    expect(decoded).toEqual(user)

    // Verify it's still a User instance
    expect(decoded).toBeInstanceOf(User)
  })
})
```

### Testing Discriminated Unions Exhaustively

```typescript
describe("Order processing", () => {
  it.prop("should handle all order states", [Arbitrary.make(Order)], ([order]) => {
    // This must handle ALL variants - Match.exhaustive ensures it
    const result = Match.value(order).pipe(
      Match.when(Schema.is(Pending), (o) => `Pending: ${o.orderId}`),
      Match.when(Schema.is(Shipped), (o) => `Shipped: ${o.trackingNumber}`),
      Match.when(Schema.is(Delivered), (o) => `Delivered: ${o.deliveredAt}`),
      Match.exhaustive
    )

    expect(typeof result).toBe("string")
  })
})
```

### Testing Invariants

```typescript
class BankAccount extends Schema.Class<BankAccount>("BankAccount")({
  id: Schema.String,
  balance: Schema.Number.pipe(Schema.nonNegative()),
  transactions: Schema.Array(Schema.Number)
}) {
  get computedBalance() {
    return this.transactions.reduce((sum, t) => sum + t, 0)
  }
}

describe("BankAccount invariants", () => {
  it.prop("should never have negative balance", [Arbitrary.make(BankAccount)], ([account]) => {
    expect(account.balance).toBeGreaterThanOrEqual(0)
  })
})
```

### Testing Transformations

```typescript
const MoneyFromCents = Schema.transform(
  Schema.Number.pipe(Schema.int()),
  Schema.Number,
  {
    decode: (cents) => cents / 100,
    encode: (dollars) => Math.round(dollars * 100)
  }
)

describe("Money transformation", () => {
  it.prop("should preserve value through transform", [Schema.Int.pipe(Schema.between(0, 1000000))], ([cents]) => {
    const dollars = Schema.decodeSync(MoneyFromCents)(cents)
    const backToCents = Schema.encodeSync(MoneyFromCents)(dollars)

    // Allow for floating point rounding
    expect(backToCents).toBe(cents)
  })
})
```

### Testing Idempotency

```typescript
describe("Normalization is idempotent", () => {
  it.prop("normalizing twice equals normalizing once", [Arbitrary.make(Email)], ([email]) => {
    const once = normalizeEmail(email)
    const twice = normalizeEmail(normalizeEmail(email))
    expect(twice).toBe(once)
  })
})
```

### Testing Commutativity

```typescript
describe("Order total calculation", () => {
  it.prop("total is independent of item order", { items: Schema.Array(OrderItem) }, ({ items }) => {
    const total1 = calculateTotal(items)
    const total2 = calculateTotal([...items].reverse())
    expect(total1).toBe(total2)
  })
})
```

## Testing Services with Layers

Combine `it.layer` with Arbitrary for service-level testing:

```typescript
import { it, expect, layer } from "@effect/vitest"
import { Effect, Layer, Context, Ref, Option } from "effect"

class UserRepository extends Context.Tag("UserRepository")<
  UserRepository,
  {
    readonly save: (user: User) => Effect.Effect<void>
    readonly findById: (id: string) => Effect.Effect<User, UserNotFound>
  }
>() {}

// Stateful test layer
const TestUserRepo = Layer.effect(
  UserRepository,
  Effect.gen(function* () {
    const usersRef = yield* Ref.make<Map<string, User>>(new Map())

    return {
      save: (user: User) =>
        Ref.update(usersRef, (users) => new Map(users).set(user.id, user)),

      findById: (id: string) =>
        Effect.gen(function* () {
          const users = yield* Ref.get(usersRef)
          const user = users.get(id)
          return yield* Option.match(Option.fromNullable(user), {
            onNone: () => Effect.fail(new UserNotFound({ userId: id })),
            onSome: Effect.succeed
          })
        }).pipe(Effect.flatten)
    }
  })
)

layer(TestUserRepo)("UserService", (it) => {
  it.effect("should save and retrieve user", () =>
    Effect.gen(function* () {
      const repo = yield* UserRepository
      const user = new User({ id: "1", name: "Alice", email: "alice@test.com", age: 30 })
      yield* repo.save(user)
      const found = yield* repo.findById("1")
      expect(found).toEqual(user)
    })
  )

  it.effect("should fail for missing user", () =>
    Effect.gen(function* () {
      const repo = yield* UserRepository
      const exit = yield* Effect.exit(repo.findById("missing"))
      expect(exit._tag).toBe("Failure")
    })
  )
})
```

## Testing Error Handling

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Schema, Match, Arbitrary } from "effect"

class ValidationError extends Schema.TaggedError<ValidationError>()(
  "ValidationError",
  { field: Schema.String, message: Schema.String }
) {}

class NotFoundError extends Schema.TaggedError<NotFoundError>()(
  "NotFoundError",
  { resourceId: Schema.String }
) {}

const AppError = Schema.Union(ValidationError, NotFoundError)
type AppError = Schema.Schema.Type<typeof AppError>

describe("Error handling", () => {
  it.prop("should handle all error types", [Arbitrary.make(AppError)], ([error]) => {
    const message = Match.value(error).pipe(
      Match.tag("ValidationError", (e) => `Validation: ${e.field}`),
      Match.tag("NotFoundError", (e) => `Not found: ${e.resourceId}`),
      Match.exhaustive
    )

    expect(typeof message).toBe("string")
  })
})
```

## Testing with Exit

Use `Effect.exit` within `it.effect` to inspect success/failure outcomes:

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Exit, Cause, Option } from "effect"

it.effect("should fail with specific error", () =>
  Effect.gen(function* () {
    const exit = yield* Effect.exit(
      Effect.fail(new UserNotFound({ userId: "123" }))
    )

    expect(Exit.isFailure(exit)).toBe(true)

    Exit.match(exit, {
      onFailure: (cause) => {
        const error = Cause.failureOption(cause)
        expect(Option.isSome(error)).toBe(true)
        expect(Schema.is(UserNotFound)(Option.getOrThrow(error))).toBe(true)
      },
      onSuccess: () => {
        throw new Error("Expected failure")
      }
    })
  })
)
```

## TestClock - Controlling Time

`it.effect` automatically provides `TestClock`. No need to manually provide `TestClock.layer`.

### Basic Time Control

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, TestClock, Fiber } from "effect"

it.effect("should complete after simulated delay", () =>
  Effect.gen(function* () {
    const fiber = yield* Effect.fork(
      Effect.sleep("1 hour").pipe(Effect.as("completed"))
    )

    yield* TestClock.adjust("1 hour")

    const result = yield* Fiber.join(fiber)
    expect(result).toBe("completed")
  })
)
```

### Testing Scheduled Operations

```typescript
it.effect("should retry 3 times", () =>
  Effect.gen(function* () {
    let attempts = 0

    const fiber = yield* Effect.fork(
      Effect.sync(() => { attempts++ }).pipe(
        Effect.flatMap(() => Effect.fail("error")),
        Effect.retry(Schedule.spaced("1 second").pipe(Schedule.recurs(3)))
      )
    )

    yield* TestClock.adjust("1 second")
    yield* TestClock.adjust("1 second")
    yield* TestClock.adjust("1 second")

    yield* Fiber.join(fiber).pipe(Effect.ignore)

    expect(attempts).toBe(4) // Initial + 3 retries
  })
)
```

## Testing Configuration

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, Config, ConfigProvider, Layer } from "effect"

const TestConfigProvider = ConfigProvider.fromMap(
  new Map([
    ["DATABASE_URL", "postgres://test:test@localhost/test"],
    ["API_KEY", "test-api-key"],
    ["DEBUG", "true"]
  ])
)

const TestConfig = Layer.setConfigProvider(TestConfigProvider)

it.effect("should use test configuration", () =>
  Effect.gen(function* () {
    const dbUrl = yield* Config.string("DATABASE_URL")
    const debug = yield* Config.boolean("DEBUG")
    expect(dbUrl).toContain("localhost/test")
    expect(debug).toBe(true)
  }).pipe(Effect.provide(TestConfig))
)
```

## @effect/vitest Quick Reference

| Function | Environment | Scope | Use Case |
|---|---|---|---|
| `it.effect` | Test (TestClock, etc.) | No | Most common; deterministic tests |
| `it.live` | Live (real clock) | No | Tests needing real environment |
| `it.scoped` | Test | Auto-cleanup | Tests with acquireRelease resources |
| `it.scopedLive` | Live | Auto-cleanup | Resources + real environment |
| `it.layer` | Test | Shared layer | Providing dependencies to test groups |
| `it.prop` | Sync | No | Property-based testing with Schema/Arbitrary |
| `it.effect.prop` | Test | No | Effect-based property testing |
| `it.flakyTest` | Test | No | Retry flaky tests with timeout |

## Best Practices

### Do

1. **Wrap ALL external dependencies in Services** - Every API call, database query, file read, and third-party SDK call MUST go through a `Context.Tag` service. This is the foundation of testable Effect code.
2. **Create test Layers for every Service** - Every service MUST have a corresponding test implementation. Use `Layer.succeed` for simple mocks, `Layer.effect` with `Ref` for stateful mocks.
3. **Use `it.layer` to provide test services** - Share test layers across test blocks. Compose multiple test layers with `Layer.merge`.
4. **Use `@effect/vitest` for ALL Effect tests** - Never use plain vitest `it` with `Effect.runPromise`
5. **Use `it.effect` as the default** - It provides TestContext automatically
6. **Use `it.prop` or `it.effect.prop` for property tests** - Prefer over manual `fc.assert`/`fc.property`. Combine with service test layers for full coverage.
7. **Use Arbitrary for ALL test data** - Never hand-craft test objects. Every Schema generates Arbitrary data.
8. **Combine services + Arbitrary for 100% coverage** - Service test layers control all I/O; Arbitrary generates all data. Together they eliminate every testing gap.
9. **Test round-trips for every Schema** - Encode/decode should be lossless
10. **Test all union variants** - Use Match.exhaustive to ensure coverage
11. **Test invariants with properties** - Not just specific examples
12. **Generate errors too** - Use Arbitrary on error schemas
13. **Use TestClock for time** - Deterministic, fast tests (automatic in `it.effect`)
14. **Call `addEqualityTesters()`** - For proper Effect type equality in assertions

### Don't

1. **Don't call external APIs/databases directly in business logic** - Always go through a Service. Direct calls make code untestable.
2. **Don't skip writing test Layers** - Every Service needs a test Layer. If a service doesn't have one, your coverage is incomplete.
3. **Don't use `Effect.runPromise` in tests** - Use `it.effect` instead
4. **Don't import `it` from `vitest`** - Import from `@effect/vitest`
5. **Don't hard-code test data** - Use Arbitrary.make(YourSchema) or `it.prop`
6. **Don't test just "happy path"** - Generate edge cases automatically
7. **Don't use `._tag` directly** - Use Match.tag or Schema.is() (for Schema types only)
8. **Don't skip round-trip tests** - They catch serialization bugs
9. **Don't manually provide TestClock** - `it.effect` does this automatically

### The Path to 100% Test Coverage

```
1. Define Services (Context.Tag)     → Every external dependency has an interface
2. Create Test Layers               → Every service has a test implementation
3. Use it.layer / layer()           → Tests compose all test layers automatically
4. Use Arbitrary + it.prop          → Test data is generated, not hand-crafted
5. Test error paths with Arbitrary  → Error schemas generate error cases too
6. Test unions exhaustively         → Match.exhaustive ensures all variants covered
```

This combination guarantees full coverage: services control all side effects, Arbitrary covers all data shapes, and Match.exhaustive covers all code paths.

## Additional Resources

For comprehensive testing documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Arbitrary" for test data generation
- "TestClock" for time control
- "Testability" for testing patterns
