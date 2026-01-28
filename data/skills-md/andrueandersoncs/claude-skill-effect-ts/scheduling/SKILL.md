---
name: Scheduling
description: This skill should be used when the user asks about "Effect Schedule", "retry schedules", "repetition", "Schedule.exponential", "Schedule.spaced", "Schedule.recurs", "cron scheduling", "backoff strategy", "schedule combinators", "Effect.repeat", "Effect.retry", "polling", or needs to understand how Effect handles scheduled operations and retry policies.
version: 1.0.0
---

# Scheduling in Effect

## Overview

Effect's `Schedule` type describes patterns for:

- **Retrying** failed operations
- **Repeating** successful operations
- **Polling** at intervals
- **Backoff strategies** for resilience

```typescript
Schedule<Out, In, Requirements>
//       ^^^  ^^ Output and input types
```

## Built-In Schedules

### Fixed Intervals

```typescript
import { Schedule } from "effect"

// Every 1 second
const everySecond = Schedule.spaced("1 second")

// Fixed delay between end and start
const fixed = Schedule.fixed("500 millis")
```

### Recurrence Limits

```typescript
// Exactly 5 times
const fiveTimes = Schedule.recurs(5)

// Once
const once = Schedule.once

// Forever
const forever = Schedule.forever
```

### Exponential Backoff

```typescript
// Exponential: 100ms, 200ms, 400ms, 800ms...
const exponential = Schedule.exponential("100 millis")

// With max delay cap
const capped = Schedule.exponential("100 millis").pipe(
  Schedule.upTo("30 seconds")
)

// With jitter (randomization)
const jittered = Schedule.exponential("100 millis").pipe(
  Schedule.jittered
)
```

### Time-Based Limits

```typescript
// Run for 1 minute
const forOneMinute = Schedule.spaced("1 second").pipe(
  Schedule.upTo("1 minute")
)

// Until specific condition
const untilSuccess = Schedule.recurWhile(
  (result) => result.status === "pending"
)
```

## Using Schedules

### Effect.retry - Retry on Failure

```typescript
const resilientFetch = fetchData().pipe(
  Effect.retry(
    Schedule.exponential("1 second").pipe(
      Schedule.compose(Schedule.recurs(5))
    )
  )
)
```

### Effect.repeat - Repeat on Success

```typescript
// Poll every 5 seconds
const polling = checkStatus().pipe(
  Effect.repeat(Schedule.spaced("5 seconds"))
)
```

### Effect.schedule - Full Control

```typescript
const scheduled = effect.pipe(
  Effect.schedule(mySchedule)
)
```

## Schedule Combinators

### Composing Schedules

```typescript
// Both must allow (intersection)
const exponentialWithLimit = Schedule.exponential("1 second").pipe(
  Schedule.compose(Schedule.recurs(10))
)

// Either allows (union)
const eitherSchedule = Schedule.union(
  Schedule.spaced("1 second"),
  Schedule.recurs(5)
)
```

### Adding Jitter

```typescript
// Random jitter ±20%
const jittered = Schedule.exponential("1 second").pipe(
  Schedule.jittered
)

// Custom jitter
const customJitter = Schedule.exponential("1 second").pipe(
  Schedule.jittered({ min: 0.8, max: 1.2 })
)
```

### Delaying First Execution

```typescript
// Wait before first attempt
const delayed = Schedule.spaced("1 second").pipe(
  Schedule.delayed(() => "5 seconds")
)
```

### Resetting Schedule

```typescript
// Reset after 1 minute of no calls
const resetting = Schedule.exponential("1 second").pipe(
  Schedule.resetAfter("1 minute")
)
```

## Conditional Retrying

### Retry While Condition

```typescript
// Use Match.tag for error type checking in predicates
const retryTransient = effect.pipe(
  Effect.retry({
    schedule: Schedule.exponential("1 second"),
    while: (error) =>
      Match.value(error).pipe(
        Match.tag("TransientError", () => true),
        Match.orElse(() => false)
      )
  })
)
```

### Retry Until Condition

```typescript
// Stop retrying when a fatal error occurs
const retryUntilFatal = effect.pipe(
  Effect.retry({
    schedule: Schedule.recurs(10),
    until: (error) =>
      Match.value(error).pipe(
        Match.tag("FatalError", () => true),
        Match.orElse(() => false)
      )
  })
)
```

## Cron Scheduling

```typescript
import { Cron } from "effect"

// Every day at midnight
const daily = Cron.parse("0 0 * * *")

// Every hour
const hourly = Cron.parse("0 * * * *")

// Use with schedule
const cronSchedule = Schedule.cron(daily)
```

## Schedule Outputs

Schedules can produce values:

```typescript
// Track elapsed time
const withElapsed = Schedule.elapsed

// Count iterations
const withCount = Schedule.count

// Collect inputs
const collecting = Schedule.collectAll<number>()
```

### Using Schedule Output

```typescript
const [result, elapsed] = yield* effect.pipe(
  Effect.retry(
    Schedule.exponential("1 second").pipe(
      Schedule.compose(Schedule.elapsed)
    )
  )
)
console.log(`Took ${elapsed}ms after retries`)
```

## Common Patterns

### API Retry with Backoff

```typescript
const apiCall = fetchFromApi().pipe(
  Effect.retry(
    Schedule.exponential("500 millis").pipe(
      Schedule.jittered,
      Schedule.compose(Schedule.recurs(5)),
      Schedule.upTo("30 seconds")
    )
  )
)
```

### Polling with Timeout

```typescript
const poll = checkJobStatus(jobId).pipe(
  Effect.repeat(
    Schedule.spaced("2 seconds").pipe(
      Schedule.upTo("5 minutes")
    )
  ),
  Effect.timeout("5 minutes")
)
```

### Circuit Breaker Pattern

```typescript
const circuitBreaker = (effect: Effect.Effect<A, E>) => {
  let failures = 0
  const maxFailures = 5
  const resetTimeout = "30 seconds"

  return effect.pipe(
    Effect.retry(
      Schedule.exponential("1 second").pipe(
        Schedule.compose(Schedule.recurs(3)),
        Schedule.tapOutput(() =>
          Effect.sync(() => { failures++ })
        )
      )
    )
  )
}
```

### Retry with Logging

```typescript
const retryWithLogs = effect.pipe(
  Effect.retry(
    Schedule.exponential("1 second").pipe(
      Schedule.compose(Schedule.recurs(5)),
      Schedule.tapInput((error) =>
        Effect.log(`Retrying after error: ${error}`)
      )
    )
  )
)
```

## Schedule Reference

| Schedule | Pattern |
|----------|---------|
| `Schedule.forever` | Never stops |
| `Schedule.once` | Single execution |
| `Schedule.recurs(n)` | Exactly n times |
| `Schedule.spaced(d)` | Fixed delay d |
| `Schedule.fixed(d)` | Fixed interval from start |
| `Schedule.exponential(d)` | d, 2d, 4d, 8d... |
| `Schedule.fibonacci(d)` | d, d, 2d, 3d, 5d... |
| `Schedule.linear(d)` | d, 2d, 3d, 4d... |

## Best Practices

1. **Always add recurs limit** - Avoid infinite retries
2. **Use jitter for distributed systems** - Prevents thundering herd
3. **Cap exponential backoff** - Use upTo() for max delay
4. **Log retry attempts** - Use tapInput for visibility
5. **Different schedules for different errors** - Transient vs permanent

## Additional Resources

For comprehensive scheduling documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Built-In Schedules" for schedule types
- "Schedule Combinators" for composition
- "Repetition" for repeat patterns
- "Retrying" for retry patterns
- "Cron" for cron expressions
