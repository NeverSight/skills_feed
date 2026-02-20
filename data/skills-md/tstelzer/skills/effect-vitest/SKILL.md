---
name: effect-vitest
description: Testing Effect programs with vitest. Use when writing tests for effect-based code.
---

## Entry Point

```ts
import { it, expect } from "@effect/vitest"
```

| Feature         | Description                                          |
| --------------- | ---------------------------------------------------- |
| `it.effect`     | Injects `TestContext` (includes `TestClock`)         |
| `it.live`       | Uses live Effect environment (real clock, logging)   |
| `it.scoped`     | Provides a `Scope` for resource management           |
| `it.scopedLive` | Combines `scoped` + `live`                           |
| `it.flakyTest`  | Retries flaky tests until success or timeout         |

## Basic Tests

```ts
import { it, expect } from "@effect/vitest"
import { Effect } from "effect"

it.effect("test success", () =>
  Effect.gen(function* () {
    const result = yield* Effect.succeed(42)
    expect(result).toBe(42)
  })
)
```

## Testing Failures with Exit

```ts
import { it, expect } from "@effect/vitest"
import { Effect, Exit } from "effect"

it.effect("test failure", () =>
  Effect.gen(function* () {
    const result = yield* Effect.exit(Effect.fail("oops"))
    expect(result).toStrictEqual(Exit.fail("oops"))
  })
)
```

## TestClock

`it.effect` provides `TestClock` starting at `0`. Use `it.live` for real time.

```ts
import { it } from "@effect/vitest"
import { Clock, Effect, TestClock } from "effect"

it.effect("with simulated time", () =>
  Effect.gen(function* () {
    yield* TestClock.adjust("1000 millis")
    const now = yield* Clock.currentTimeMillis
    // now === 1000
  })
)

it.live("with real time", () =>
  Effect.gen(function* () {
    const now = yield* Clock.currentTimeMillis
    // now === actual system time
  })
)
```

## Scoped Tests

Use `it.scoped` when your test acquires resources.

```ts
import { it } from "@effect/vitest"
import { Console, Effect } from "effect"

const resource = Effect.acquireRelease(
  Console.log("acquire"),
  () => Console.log("release")
)

it.scoped("manages resources", () =>
  Effect.gen(function* () {
    yield* resource // automatically released after test
  })
)
```

## Flaky Tests

```ts
import { it } from "@effect/vitest"
import { Effect, Random } from "effect"

const flaky = Effect.gen(function* () {
  if (yield* Random.nextBoolean) return yield* Effect.fail("random failure")
})

it.effect("retry until success", () =>
  it.flakyTest(flaky, "5 seconds")
)
```

## Test Modifiers

```ts
it.effect.skip("skipped test", () => Effect.void)
it.effect.only("run only this", () => Effect.void)
it.effect.fails("expected to fail", () => Effect.fail("expected"))
```

## Logging

Logging is suppressed in `it.effect`. Enable with custom logger or `it.live`:

```ts
import { it } from "@effect/vitest"
import { Effect, Logger } from "effect"

it.effect("with logging", () =>
  Effect.log("visible").pipe(Effect.provide(Logger.pretty))
)

it.live("logging enabled by default", () =>
  Effect.log("visible")
)
```
