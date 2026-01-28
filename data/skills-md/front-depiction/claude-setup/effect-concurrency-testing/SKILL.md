---
name: effect-concurrency-testing
description: Test Effect concurrency primitives including PubSub, Deferred, Latch, Fiber coordination, SubscriptionRef, and Stream. Use this skill when testing concurrent effects, event-driven systems, or fiber coordination.
---

# Effect Concurrency Testing Skill

This skill provides patterns for testing Effect's concurrency primitives: fibers, latches, deferreds, PubSub, SubscriptionRef, and streams.

## Core Principles

**CRITICAL**: Choose the correct coordination primitive based on what you need to synchronize.

| Need | Use |
|------|-----|
| Simple fiber yield | `Effect.yieldNow` |
| Forked PubSub subscriber ready | `yieldNow` after fork, `yieldNow` after each publish |
| Wait for subscriber ready | `Deferred.make()` + `Deferred.await` |
| Wait for stream element | `Effect.makeLatch()` + `Stream.tap(() => latch.open)` |
| Time-dependent behavior | `TestClock.adjust` |
| Verify events published | `PubSub.subscribe` + `PubSub.takeAll` |
| Check fiber status | `fiber.unsafePoll()` |

## Fiber Coordination Patterns

### Effect.yieldNow - Simple Fiber Scheduling

Use `Effect.yieldNow` when you need to allow other fibers to execute. This is preferred over `TestClock.adjust` for non-time-dependent code.

```typescript
import { it } from "@effect/vitest"
import { Effect, Exit, Fiber } from "effect"

it.effect("fiber polling with yieldNow", () =>
  Effect.gen(function* () {
    const latch = yield* Effect.makeLatch()

    const fiber = yield* latch.await.pipe(Effect.fork)

    yield* Effect.yieldNow()

    expect(fiber.unsafePoll()).toBeNull()

    yield* latch.open

    expect(yield* fiber.await).toEqual(Exit.void)
  })
)
```

### Latch - Explicit Coordination

`Effect.makeLatch()` creates a gate that blocks fibers until opened:

```typescript
import { it } from "@effect/vitest"
import { Effect, Fiber } from "effect"

it.effect("latch coordination", () =>
  Effect.gen(function* () {
    const latch = yield* Effect.makeLatch()

    const fiber = yield* Effect.gen(function* () {
      yield* latch.await
      return "completed"
    }).pipe(Effect.fork)

    yield* Effect.yieldNow()
    expect(fiber.unsafePoll()).toBeNull()

    yield* latch.open

    const result = yield* Fiber.join(fiber)
    expect(result).toBe("completed")
  })
)
```

### Latch Operations

```typescript
import { Effect } from "effect"

declare const latch: Effect.Effect.Success<ReturnType<typeof Effect.makeLatch>>

latch.await       // Wait until latch is open
latch.open        // Open the latch (allows waiters through)
latch.close       // Close the latch (blocks future waiters)
latch.release     // Open once, then close
latch.whenOpen    // Run effect only when latch is open
```

### Deferred - Signal Readiness Between Fibers

Use `Deferred` when one fiber needs to signal another with a value:

```typescript
import { it } from "@effect/vitest"
import { Effect, Deferred, Fiber } from "effect"

it.effect("deferred signaling", () =>
  Effect.gen(function* () {
    const signal = yield* Deferred.make<number>()

    const consumer = yield* Effect.gen(function* () {
      const value = yield* Deferred.await(signal)
      return value * 2
    }).pipe(Effect.fork)

    yield* Deferred.succeed(signal, 21)

    const result = yield* Fiber.join(consumer)
    expect(result).toBe(42)
  })
)
```

### fiber.unsafePoll() - Check Completion Without Blocking

```typescript
import { Effect, Exit, Fiber } from "effect"

declare const fiber: Fiber.RuntimeFiber<string>

fiber.unsafePoll()
// Returns null if running
// Returns Exit<A, E> if completed (success, failure, or interrupted)

// Check if still running
expect(fiber.unsafePoll()).toBeNull()

// Check if completed
expect(fiber.unsafePoll()).toBeDefined()

// Check specific completion
expect(fiber.unsafePoll()).toEqual(Exit.succeed("result"))
```

## PubSub Event Testing

### Direct Event Verification

Use `Effect.scoped` to manage PubSub subscription lifecycle:

```typescript
import { it } from "@effect/vitest"
import { Effect, PubSub } from "effect"

it.effect("verify published events", () =>
  Effect.gen(function* () {
    const pubsub = yield* PubSub.unbounded<string>()

    yield* Effect.scoped(
      Effect.gen(function* () {
        const sub = yield* PubSub.subscribe(pubsub)

        yield* PubSub.publish(pubsub, "event-1")
        yield* PubSub.publish(pubsub, "event-2")

        const events = yield* PubSub.takeAll(sub)

        expect(events).toEqual(["event-1", "event-2"])
      })
    )
  })
)
```

### Testing Event Publishers

When testing a service that publishes events:

```typescript
import { it } from "@effect/vitest"
import { Effect, PubSub, Context, Layer } from "effect"

interface UserEvent {
  readonly type: "created" | "deleted"
  readonly userId: string
}

class EventBus extends Context.Tag("EventBus")<
  EventBus,
  PubSub.PubSub<UserEvent>
>() {}

class UserService extends Context.Tag("UserService")<
  UserService,
  { readonly createUser: (id: string) => Effect.Effect<void> }
>() {}

declare const UserServiceLive: Layer.Layer<UserService, never, EventBus>

it.effect("should publish user created event", () =>
  Effect.gen(function* () {
    const pubsub = yield* PubSub.unbounded<UserEvent>()

    yield* Effect.scoped(
      Effect.gen(function* () {
        const sub = yield* PubSub.subscribe(pubsub)

        const service = yield* UserService
        yield* service.createUser("user-123")

        const events = yield* PubSub.takeAll(sub)

        expect(events).toHaveLength(1)
        expect(events[0]).toEqual({
          type: "created",
          userId: "user-123"
        })
      })
    )
  }).pipe(
    Effect.provide(UserServiceLive),
    Effect.provide(Layer.succeed(EventBus, pubsub))
  )
)
```

### Concurrent Publisher/Subscriber Testing

```typescript
import { it } from "@effect/vitest"
import { Effect, PubSub, Fiber, Array as A } from "effect"

it.effect("concurrent publishers and subscribers", () =>
  Effect.gen(function* () {
    const values = A.range(0, 9)
    const latch = yield* Effect.makeLatch()
    const pubsub = yield* PubSub.bounded<number>(10)

    const subscriber = yield* PubSub.subscribe(pubsub).pipe(
      Effect.flatMap((sub) =>
        latch.await.pipe(
          Effect.andThen(
            Effect.forEach(values, () => PubSub.take(sub))
          )
        )
      ),
      Effect.scoped,
      Effect.forkScoped
    )

    yield* PubSub.publishAll(pubsub, values)
    yield* latch.open

    const result = yield* Fiber.join(subscriber)
    expect(result).toEqual(values)
  })
)
```

## Forked Fiber PubSub Subscriptions

When testing forked fibers that subscribe to a PubSub, proper yield ordering is critical to avoid losing events.

### Correct Order: yieldNow After Subscribe, Then After Each Publish

```typescript
import { it, expect } from "@effect/vitest"
import { Effect, PubSub, Ref, Array as A } from "effect"

it.effect("forked subscriber receives all events", () =>
  Effect.gen(function* () {
    const pubsub = yield* PubSub.unbounded<string>()
    const received = yield* Ref.make<string[]>([])

    yield* Effect.scoped(
      Effect.gen(function* () {
        const sub = yield* PubSub.subscribe(pubsub)

        yield* Effect.fork(
          Effect.forever(
            Effect.gen(function* () {
              const msg = yield* PubSub.take(sub)
              yield* Ref.update(received, A.append(msg))
            })
          )
        )

        yield* Effect.yieldNow()  // Let forked fiber start and become ready

        yield* PubSub.publish(pubsub, "event-1")
        yield* Effect.yieldNow()  // Let fiber process event-1

        yield* PubSub.publish(pubsub, "event-2")
        yield* Effect.yieldNow()  // Let fiber process event-2

        const events = yield* Ref.get(received)
        expect(events).toEqual(["event-1", "event-2"])
      })
    )
  })
)
```

### Why This Order Matters

The fiber scheduling model requires explicit yields at specific points:

1. **yieldNow after subscribe/fork**: The forked fiber needs a chance to execute its first instruction (the `PubSub.take`) before any events are published. Without this yield, the fiber hasn't started yet.

2. **yieldNow after each publish**: After publishing, the subscriber fiber needs a turn to process the event. Without yielding, you may publish multiple events before the fiber processes any.

### Common Mistake: Events Lost

```typescript
import { Effect, PubSub, Ref } from "effect"

// BAD - Events are lost because fiber hasn't started
Effect.gen(function* () {
  const pubsub = yield* PubSub.unbounded<string>()
  const received = yield* Ref.make<string[]>([])

  yield* Effect.scoped(
    Effect.gen(function* () {
      const sub = yield* PubSub.subscribe(pubsub)

      yield* Effect.fork(/* subscriber logic */)

      // WRONG: Publishing immediately - fiber not ready yet!
      yield* PubSub.publish(pubsub, "event-1")
      yield* PubSub.publish(pubsub, "event-2")

      yield* Effect.yieldNow()  // Too late - events already missed

      const events = yield* Ref.get(received)
      // events may be [] or incomplete!
    })
  )
})
```

### Single yieldNow Is Sufficient

Unlike `sleep(0)` patterns in other runtimes, Effect's `yieldNow` is deterministic within the fiber scheduler. A single `yieldNow` is sufficient at each synchronization point - no need for multiple yields or retry loops.

```typescript
import { Effect, PubSub } from "effect"

// GOOD - Single yield at each point
yield* Effect.fork(subscriber)
yield* Effect.yieldNow()  // One yield is enough

yield* PubSub.publish(pubsub, "event")
yield* Effect.yieldNow()  // One yield is enough

// BAD - Unnecessary multiple yields
yield* Effect.fork(subscriber)
yield* Effect.yieldNow()
yield* Effect.yieldNow()  // Redundant
yield* Effect.yieldNow()  // Redundant
```

### Testing Observer Pattern with Session

This pattern applies to any forked subscriber, including observer patterns:

```typescript
import { it, expect } from "@effect/vitest"
import { Effect } from "effect"

declare const Observer: {
  attach: (
    session: unknown,
    observer: unknown,
    args: unknown
  ) => Effect.Effect<void>
}

declare const Session: {
  publish: (session: unknown, event: unknown) => Effect.Effect<void>
}

declare const session: unknown
declare const observer: unknown
declare const args: unknown
declare const event1: unknown
declare const event2: unknown
declare const getResults: () => Effect.Effect<unknown[]>

it.effect("observer receives session events", () =>
  Effect.gen(function* () {
    yield* Observer.attach(session, observer, args)  // Forks subscriber
    yield* Effect.yieldNow()                         // Let fiber start

    yield* Session.publish(session, event1)
    yield* Effect.yieldNow()                         // Let event process

    yield* Session.publish(session, event2)
    yield* Effect.yieldNow()                         // Let event process

    const results = yield* getResults()
    expect(results).toHaveLength(2)
  })
)
```

## SubscriptionRef Testing

### Testing Stream Changes with Latches

The latch pattern ensures the stream subscription is ready before mutations:

```typescript
import { it } from "@effect/vitest"
import { Effect, Fiber, Number } from "effect"
import { Stream, SubscriptionRef } from "effect/stream"

it.effect("multiple subscribers can receive changes", () =>
  Effect.gen(function* () {
    const ref = yield* SubscriptionRef.make(0)
    const latch1 = yield* Effect.makeLatch()
    const latch2 = yield* Effect.makeLatch()

    const fiber1 = yield* SubscriptionRef.changes(ref).pipe(
      Stream.tap(() => latch1.open),
      Stream.take(3),
      Stream.runCollect,
      Effect.forkScoped
    )

    yield* latch1.await
    yield* SubscriptionRef.update(ref, Number.increment)

    const fiber2 = yield* SubscriptionRef.changes(ref).pipe(
      Stream.tap(() => latch2.open),
      Stream.take(2),
      Stream.runCollect,
      Effect.forkScoped
    )

    yield* latch2.await
    yield* SubscriptionRef.update(ref, Number.increment)

    const result1 = yield* Fiber.join(fiber1)
    const result2 = yield* Fiber.join(fiber2)

    expect(result1).toEqual([0, 1, 2])
    expect(result2).toEqual([1, 2])
  })
)
```

### Testing Subscription Interruption

```typescript
import { it } from "@effect/vitest"
import { Effect, Exit, Fiber, Number, Cause } from "effect"
import { Pull, Stream, SubscriptionRef } from "effect/stream"

it.effect("subscriptions are interruptible", () =>
  Effect.gen(function* () {
    const ref = yield* SubscriptionRef.make(0)
    const latch = yield* Effect.makeLatch()

    const fiber = yield* SubscriptionRef.changes(ref).pipe(
      Stream.tap(() => latch.open),
      Stream.take(10),
      Stream.runCollect,
      Effect.forkScoped
    )

    yield* latch.await
    yield* SubscriptionRef.update(ref, Number.increment)
    yield* Fiber.interrupt(fiber)

    const result = yield* Fiber.await(fiber)

    expect(
      Exit.isFailure(result) && Pull.isHaltCause(result.cause)
    ).toBe(true)
  })
)
```

## Stream Testing

### Collecting Stream Results

```typescript
import { it } from "@effect/vitest"
import { Effect } from "effect"
import { Stream } from "effect/stream"

it.effect("should collect stream elements", () =>
  Effect.gen(function* () {
    const result = yield* Stream.make(1, 2, 3, 4, 5).pipe(
      Stream.filter((n) => n % 2 === 0),
      Stream.runCollect
    )

    expect(result).toEqual([2, 4])
  })
)
```

### Testing Stream Side Effects

```typescript
import { it } from "@effect/vitest"
import { Effect, Ref } from "effect"
import { Stream } from "effect/stream"

it.effect("should track side effects", () =>
  Effect.gen(function* () {
    const log = yield* Ref.make<string[]>([])

    yield* Stream.make("a", "b", "c").pipe(
      Stream.tap((item) => Ref.update(log, (items) => [...items, item])),
      Stream.runDrain
    )

    const logged = yield* Ref.get(log)
    expect(logged).toEqual(["a", "b", "c"])
  })
)
```

### Testing Stream Errors

```typescript
import { it } from "@effect/vitest"
import { Effect, Exit, Data } from "effect"
import { Stream } from "effect/stream"

class StreamError extends Data.TaggedError("StreamError")<{
  readonly message: string
}> {}

it.effect("should handle stream errors", () =>
  Effect.gen(function* () {
    const result = yield* Stream.make(1, 2, 3).pipe(
      Stream.mapEffect((n) =>
        n === 2
          ? Effect.fail(new StreamError({ message: "boom" }))
          : Effect.succeed(n)
      ),
      Stream.runCollect,
      Effect.exit
    )

    expect(Exit.isFailure(result)).toBe(true)
  })
)
```

### Testing Stream Finalization

```typescript
import { it } from "@effect/vitest"
import { Effect, Ref } from "effect"
import { Stream } from "effect/stream"

it.effect("should run finalizers", () =>
  Effect.gen(function* () {
    const finalized = yield* Ref.make(false)

    yield* Stream.make(1, 2, 3).pipe(
      Stream.ensuring(Ref.set(finalized, true)),
      Stream.take(1),
      Stream.runDrain
    )

    expect(yield* Ref.get(finalized)).toBe(true)
  })
)
```

## Interruption Testing

### Testing Fiber Interruption

```typescript
import { it } from "@effect/vitest"
import { Effect, Exit, Fiber, Cause } from "effect"

it.effect("should handle interruption", () =>
  Effect.gen(function* () {
    const fiber = yield* Effect.never.pipe(Effect.fork)

    yield* Fiber.interrupt(fiber)

    const result = yield* Fiber.await(fiber)

    expect(Exit.isInterrupted(result)).toBe(true)
  })
)
```

### Testing Interrupted-Only Cause

```typescript
import { it } from "@effect/vitest"
import { Effect, Exit, Fiber, Cause } from "effect"

it.effect("should have interrupted-only cause", () =>
  Effect.gen(function* () {
    const fiber = yield* Effect.never.pipe(Effect.fork)

    yield* Fiber.interrupt(fiber)

    const result = yield* Fiber.await(fiber)

    expect(
      Exit.isFailure(result) && Cause.isInterruptedOnly(result.cause)
    ).toBe(true)
  })
)
```

## Time-Dependent Concurrency Testing

Use `TestClock` only when testing time-dependent behavior like delays, timeouts, or schedules.

```typescript
import { it } from "@effect/vitest"
import { Effect, Fiber, TestClock, Duration } from "effect"

it.effect("should handle delayed concurrent operations", () =>
  Effect.gen(function* () {
    const fiber = yield* Effect.gen(function* () {
      yield* Effect.sleep(Duration.seconds(5))
      return "done"
    }).pipe(Effect.fork)

    yield* TestClock.adjust(Duration.seconds(5))

    const result = yield* Fiber.join(fiber)
    expect(result).toBe("done")
  })
)
```

## Anti-Patterns

### DON'T use TestClock for non-time-dependent code

```typescript
import { Effect, TestClock, Duration } from "effect"

// BAD - Using TestClock when not needed
Effect.gen(function* () {
  const fiber = yield* someEffect.pipe(Effect.fork)
  yield* TestClock.adjust(Duration.millis(100))
  yield* Fiber.join(fiber)
})

// GOOD - Use yieldNow for simple yielding
Effect.gen(function* () {
  const fiber = yield* someEffect.pipe(Effect.fork)
  yield* Effect.yieldNow()
  yield* Fiber.join(fiber)
})
```

### DON'T poll in a loop without yieldNow

```typescript
import { Effect, Fiber } from "effect"

declare const fiber: Fiber.RuntimeFiber<void>

// BAD - Busy loop
while (fiber.unsafePoll() === null) {
  // Spins forever!
}

// GOOD - Yield between polls or use Fiber.await
Effect.gen(function* () {
  while (fiber.unsafePoll() === null) {
    yield* Effect.yieldNow()
  }
})

// BETTER - Just await the fiber
Effect.gen(function* () {
  yield* Fiber.await(fiber)
})
```

### DON'T forget Effect.scoped for PubSub subscriptions

```typescript
import { Effect, PubSub } from "effect"

declare const pubsub: PubSub.PubSub<string>

// BAD - Subscription leaks
Effect.gen(function* () {
  const sub = yield* PubSub.subscribe(pubsub)
  // Sub is never cleaned up!
})

// GOOD - Scoped subscription
Effect.gen(function* () {
  yield* Effect.scoped(
    Effect.gen(function* () {
      const sub = yield* PubSub.subscribe(pubsub)
      const events = yield* PubSub.takeAll(sub)
      // Sub cleaned up when scope closes
    })
  )
})
```

### DON'T start subscriptions after mutations

```typescript
import { Effect } from "effect"
import { Stream, SubscriptionRef } from "effect/stream"

declare const ref: SubscriptionRef.SubscriptionRef<number>

// BAD - May miss events
Effect.gen(function* () {
  yield* SubscriptionRef.update(ref, (n) => n + 1)
  const fiber = yield* SubscriptionRef.changes(ref).pipe(
    Stream.take(1),
    Stream.runCollect,
    Effect.fork
  )
  // Subscription started after mutation - may miss it!
})

// GOOD - Use latch to ensure subscription is ready
Effect.gen(function* () {
  const latch = yield* Effect.makeLatch()

  const fiber = yield* SubscriptionRef.changes(ref).pipe(
    Stream.tap(() => latch.open),
    Stream.take(2),
    Stream.runCollect,
    Effect.forkScoped
  )

  yield* latch.await
  yield* SubscriptionRef.update(ref, (n) => n + 1)

  const result = yield* Fiber.join(fiber)
})
```

## Quality Checklist

- [ ] Using correct coordination primitive for the use case
- [ ] `Effect.scoped` wraps PubSub subscriptions
- [ ] Latches ensure stream subscriptions are ready before mutations
- [ ] `Effect.yieldNow` after fork to let subscriber fiber start
- [ ] `Effect.yieldNow` after each publish to let fiber process event
- [ ] `Effect.yieldNow` used instead of TestClock for non-time-dependent code
- [ ] Fiber interruption tested with `Exit.isInterrupted` or `Cause.isInterruptedOnly`
- [ ] Stream finalizers verified with `Stream.ensuring`
- [ ] No busy polling without yields
- [ ] Test is deterministic (no race conditions)
