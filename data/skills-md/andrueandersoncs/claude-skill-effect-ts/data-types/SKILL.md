---
name: Data Types
description: This skill should be used when the user asks about "Effect Option", "Effect Either", "Option.some", "Option.none", "Either.left", "Either.right", "Cause", "Exit", "Chunk", "Data", "Data.TaggedEnum", "Data.Class", "Duration", "DateTime", "HashMap", "HashSet", "Redacted", or needs to understand Effect's built-in data types and functional data structures.
version: 1.0.0
---

# Data Types in Effect

## Overview

Effect provides immutable, type-safe data structures:

- **Option** - Represents optional values (Some/None)
- **Either** - Represents success/failure (Right/Left)
- **Cause** - Detailed failure information
- **Exit** - Effect execution result
- **Data** - Value equality for classes
- **Chunk** - Immutable indexed sequence
- **Duration** - Time spans
- **DateTime** - Date/time handling

## Option

Represents a value that may or may not exist:

```typescript
import { Option } from "effect"

// Creating Options
const some = Option.some(42)
const none = Option.none()

// From nullable
const fromNull = Option.fromNullable(maybeNull)

// Pattern matching
const result = Option.match(option, {
  onNone: () => "No value",
  onSome: (value) => `Got: ${value}`
})

// Get with default
const value = Option.getOrElse(option, () => defaultValue)

// Map over Some
const doubled = Option.map(option, (n) => n * 2)

// FlatMap for chaining
const chained = Option.flatMap(option, (n) =>
  n > 0 ? Option.some(n) : Option.none()
)

// Filter
const positive = Option.filter(option, (n) => n > 0)
```

### Option with Effect

```typescript
const program = Effect.gen(function* () {
  const maybeUser = yield* findUser(id)

  // Convert Option to Effect
  const user = yield* Option.match(maybeUser, {
    onNone: () => Effect.fail(new UserNotFound()),
    onSome: Effect.succeed
  })

  // Or use Effect.fromOption
  const user = yield* maybeUser.pipe(
    Effect.fromOption,
    Effect.mapError(() => new UserNotFound())
  )
})
```

## Either

Represents a value that is either Left (failure) or Right (success):

```typescript
import { Either } from "effect"

// Creating Either
const right = Either.right(42)
const left = Either.left("error")

// Pattern matching
const result = Either.match(either, {
  onLeft: (error) => `Error: ${error}`,
  onRight: (value) => `Success: ${value}`
})

// Map over Right
const doubled = Either.map(either, (n) => n * 2)

// MapLeft over Left
const mapped = Either.mapLeft(either, (e) => new Error(e))

// MapBoth
const both = Either.mapBoth(either, {
  onLeft: (e) => new Error(e),
  onRight: (n) => n * 2
})

// FlatMap
const chained = Either.flatMap(either, (n) =>
  n > 0 ? Either.right(n) : Either.left("negative")
)

// Get or throw
const value = Either.getOrThrow(either)
```

## Cause

Complete failure information for an Effect:

```typescript
import { Cause } from "effect"

// Cause variants
Cause.fail(error)      // Expected error
Cause.die(defect)      // Unexpected error (defect)
Cause.interrupt(id)    // Interruption
Cause.empty           // No failure
Cause.sequential(c1, c2) // Sequential failures
Cause.parallel(c1, c2)   // Parallel failures

// Inspecting Cause
Cause.isFailure(cause)
Cause.isDie(cause)
Cause.isInterrupt(cause)

// Extracting errors
const failures = Cause.failures(cause) // Chunk of E
const defects = Cause.defects(cause)   // Chunk of unknown

// Pretty print
const message = Cause.pretty(cause)
```

## Exit

The result of running an Effect:

```typescript
import { Exit } from "effect"

// Exit variants
Exit.succeed(value)    // Success
Exit.fail(cause)       // Failure with Cause

// Pattern matching
const result = Exit.match(exit, {
  onFailure: (cause) => `Failed: ${Cause.pretty(cause)}`,
  onSuccess: (value) => `Succeeded: ${value}`
})

// Check type
Exit.isSuccess(exit)
Exit.isFailure(exit)

// Extract value
const value = Exit.getOrElse(exit, () => defaultValue)

// Map
const mapped = Exit.map(exit, (a) => a * 2)
```

## Data - Value Equality

Create classes with structural equality:

```typescript
import { Data, Schema } from "effect"

// Tagged class
class Person extends Data.Class<{
  readonly name: string
  readonly age: number
}> {}

const alice1 = new Person({ name: "Alice", age: 30 })
const alice2 = new Person({ name: "Alice", age: 30 })

alice1 === alice2  // false (reference)
Equal.equals(alice1, alice2)  // true (structural)

// Tagged errors (used with Effect.fail)
// Use Schema.TaggedError for domain errors - works with Schema.is(), catchTag, and Match.tag
class UserNotFound extends Schema.TaggedError<UserNotFound>()(
  "UserNotFound",
  { userId: Schema.String }
) {}

// Tagged enum
type Shape = Data.TaggedEnum<{
  Circle: { radius: number }
  Rectangle: { width: number; height: number }
}>
const { Circle, Rectangle } = Data.taggedEnum<Shape>()

const circle = Circle({ radius: 10 })
const rect = Rectangle({ width: 5, height: 3 })
```

## Chunk

Immutable indexed sequence optimized for Effect:

```typescript
import { Chunk } from "effect"

// Creating
const chunk = Chunk.make(1, 2, 3, 4, 5)
const fromArray = Chunk.fromIterable([1, 2, 3])
const empty = Chunk.empty<number>()

// Operations
const head = Chunk.head(chunk)          // Option<number>
const tail = Chunk.tail(chunk)          // Chunk
const take = Chunk.take(chunk, 2)       // Chunk
const drop = Chunk.drop(chunk, 2)       // Chunk

// Functional operations
const doubled = Chunk.map(chunk, (n) => n * 2)
const filtered = Chunk.filter(chunk, (n) => n > 2)
const sum = Chunk.reduce(chunk, 0, (acc, n) => acc + n)

// Conversion
const array = Chunk.toArray(chunk)
const readonlyArray = Chunk.toReadonlyArray(chunk)
```

## Duration

Represent time spans:

```typescript
import { Duration } from "effect"

// Creating
const ms = Duration.millis(100)
const secs = Duration.seconds(5)
const mins = Duration.minutes(10)
const hours = Duration.hours(2)
const days = Duration.days(1)

// From string
const fromString = Duration.decode("5 seconds")

// Operations
const total = Duration.sum(duration1, duration2)
const remaining = Duration.subtract(total, elapsed)

// Comparison
Duration.greaterThan(a, b)
Duration.lessThanOrEqualTo(a, b)

// Conversion
const milliseconds = Duration.toMillis(duration)
const seconds = Duration.toSeconds(duration)
```

## DateTime

Date and time handling:

```typescript
import { DateTime } from "effect"

// Current time
const now = DateTime.now

// From Date
const fromDate = DateTime.fromDate(new Date())

// From parts
const specific = DateTime.make({
  year: 2024,
  month: 1,
  day: 15,
  hours: 10,
  minutes: 30
})

// Operations
const tomorrow = DateTime.add(now, { days: 1 })
const lastWeek = DateTime.subtract(now, { weeks: 1 })

// Formatting
const formatted = DateTime.format(now, "yyyy-MM-dd")

// Timezone
const utc = DateTime.setZone(now, "UTC")
const local = DateTime.setZone(now, DateTime.zoneLocal)
```

## HashMap & HashSet

Immutable hash-based collections:

```typescript
import { HashMap, HashSet } from "effect"

// HashMap
const map = HashMap.make(
  ["a", 1],
  ["b", 2],
  ["c", 3]
)

const value = HashMap.get(map, "a")  // Option<number>
const updated = HashMap.set(map, "d", 4)
const removed = HashMap.remove(map, "a")

// HashSet
const set = HashSet.make(1, 2, 3, 4, 5)

const has = HashSet.has(set, 3)  // true
const added = HashSet.add(set, 6)
const removed = HashSet.remove(set, 1)
const union = HashSet.union(set1, set2)
const intersection = HashSet.intersection(set1, set2)
```

## Redacted

Protect sensitive values from logging:

```typescript
import { Redacted } from "effect"

// Create redacted value
const apiKey = Redacted.make("sk-secret-key-123")

// Logging shows <redacted>
console.log(apiKey)  // Redacted(<redacted>)
console.log(`Key: ${apiKey}`)  // Key: <redacted>

// Get actual value when needed
const actual = Redacted.value(apiKey)  // "sk-secret-key-123"
```

## Best Practices

1. **Use Option for nullable values** - Explicit handling required
2. **Use Either for validation** - Accumulate errors
3. **Use Schema.TaggedError for Effect errors** - Enables catchTag and Schema.is()
4. **Use Chunk in streaming** - Optimized for Effect operations
5. **Use Redacted for secrets** - Prevents accidental exposure
6. **Use Duration for time** - Type-safe time operations

## Additional Resources

For comprehensive data type documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Option" for optional values
- "Either" for success/failure
- "Cause" for error details
- "Exit" for execution results
- "Data" for value equality
- "Chunk" for sequences
- "DateTime" for date handling
