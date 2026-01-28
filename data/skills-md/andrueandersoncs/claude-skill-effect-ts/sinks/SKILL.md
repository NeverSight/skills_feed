---
name: Sinks
description: This skill should be used when the user asks about "Effect Sink", "Sink.collectAll", "Sink.sum", "Sink.fold", "stream consumers", "Sink.forEach", "creating sinks", "sink operations", "sink leftovers", "sink concurrency", "Stream.run with Sink", or needs to understand how Effect Sinks consume stream data.
version: 1.0.0
---

# Sinks in Effect

## Overview

A `Sink` is a consumer of stream elements that produces a result:

```typescript
Sink<A, In, L, E, R>
// A  - Result type (what sink produces)
// In - Input element type (what sink consumes)
// L  - Leftover type (unconsumed elements)
// E  - Error type
// R  - Required environment
```

Sinks are the counterpart to Streams - while Streams produce data, Sinks consume it.

## Built-in Sinks

### Collecting Elements

```typescript
import { Stream, Sink } from "effect"

// Collect all elements to Chunk
const all = yield* Stream.make(1, 2, 3, 4, 5).pipe(
  Stream.run(Sink.collectAll())
) // Chunk(1, 2, 3, 4, 5)

// Collect to Array
const array = yield* Stream.make(1, 2, 3).pipe(
  Stream.run(Sink.collectAllToArray())
)

// Collect N elements
const firstThree = yield* Stream.range(1, 100).pipe(
  Stream.run(Sink.collectAllN(3))
) // Chunk(1, 2, 3)

// Collect while condition
const whileSmall = yield* Stream.iterate(1, (n) => n + 1).pipe(
  Stream.run(Sink.collectAllWhile((n) => n < 5))
) // Chunk(1, 2, 3, 4)
```

### Aggregation Sinks

```typescript
// Sum numbers
const total = yield* Stream.make(1, 2, 3, 4, 5).pipe(
  Stream.run(Sink.sum)
) // 15

// Count elements
const count = yield* Stream.make("a", "b", "c").pipe(
  Stream.run(Sink.count)
) // 3

// Find first element
const first = yield* Stream.make(1, 2, 3).pipe(
  Stream.run(Sink.head)
) // Option.some(1)

// Find last element
const last = yield* Stream.make(1, 2, 3).pipe(
  Stream.run(Sink.last)
) // Option.some(3)

// Take N elements
const taken = yield* Stream.make(1, 2, 3, 4, 5).pipe(
  Stream.run(Sink.take(3))
) // Chunk(1, 2, 3)
```

### Folding Sinks

```typescript
// Fold left (reduce)
const product = yield* Stream.make(1, 2, 3, 4, 5).pipe(
  Stream.run(Sink.foldLeft(1, (acc, n) => acc * n))
) // 120

// Fold with early termination
const sumUntil100 = yield* Stream.iterate(1, (n) => n + 1).pipe(
  Stream.run(
    Sink.fold(
      0,
      (sum) => sum < 100,  // Continue while sum < 100
      (sum, n) => sum + n
    )
  )
)

// Fold with effect
const foldWithLog = Sink.foldEffect(
  0,
  (sum) => sum < 100,
  (sum, n) =>
    Effect.gen(function* () {
      yield* Effect.log(`Adding ${n} to ${sum}`)
      return sum + n
    })
)
```

### Side Effect Sinks

```typescript
// Execute effect for each element
yield* Stream.make(1, 2, 3).pipe(
  Stream.run(Sink.forEach((n) => Effect.log(`Got: ${n}`)))
)

// Drain (consume all, return nothing)
yield* Stream.make(1, 2, 3).pipe(
  Stream.run(Sink.drain)
)
```

## Creating Custom Sinks

### Sink.make

```typescript
const maxSink = Sink.make<number, number, never, never, never>(
  // Initial state
  Number.NEGATIVE_INFINITY,
  // Process each element
  (max, n) => n > max ? n : max,
  // Extract result
  (max) => max
)

const max = yield* Stream.make(3, 1, 4, 1, 5, 9).pipe(
  Stream.run(maxSink)
) // 9
```

### Sink.fromEffect

```typescript
const logAndReturn = <A>(label: string) =>
  Sink.fromEffect(
    Effect.gen(function* () {
      yield* Effect.log(`Starting ${label}`)
      return [] as A[]
    })
  )
```

### Sink.fromPush

For more control over the sink lifecycle:

```typescript
const customSink = Sink.fromPush<number, number, never, never>((input) =>
  Effect.sync(() =>
    Option.match(input, {
      onNone: () => Either.left(finalResult),  // Stream ended
      onSome: (chunk) => {
        // Process chunk
        // Return Either.right to continue, Either.left to finish
        return Either.right(undefined)
      }
    })
  )
)
```

## Sink Operations

### Transforming Sinks

```typescript
// Map over result
const doubledSum = Sink.sum.pipe(
  Sink.map((sum) => sum * 2)
)

// Contramap over input
const lengthSum = Sink.sum.pipe(
  Sink.contramap((s: string) => s.length)
)

// Dimap both
const processStrings = Sink.sum.pipe(
  Sink.dimap(
    (s: string) => s.length,  // Transform input
    (sum) => `Total length: ${sum}`  // Transform output
  )
)
```

### Combining Sinks

```typescript
// Zip two sinks (run both, combine results)
const sumAndCount = Sink.zip(Sink.sum, Sink.count)

const [sum, count] = yield* Stream.make(1, 2, 3, 4, 5).pipe(
  Stream.run(sumAndCount)
) // [15, 5]

// Race two sinks (first to complete wins)
const firstOrSum = Sink.race(
  Sink.head,
  Sink.sum.pipe(Sink.map(Option.some))
)
```

### Filtering

```typescript
// Filter input before processing
const sumPositive = Sink.sum.pipe(
  Sink.filterInput((n: number) => n > 0)
)

const result = yield* Stream.make(-1, 2, -3, 4, -5).pipe(
  Stream.run(sumPositive)
) // 6
```

## Leftovers

Sinks can leave unconsumed elements:

```typescript
// Take returns leftovers
const takeThree = Sink.take<number>(3)

// When used with splitSink, leftovers go to next sink
const [first, rest] = yield* Stream.make(1, 2, 3, 4, 5).pipe(
  Stream.run(
    Sink.take<number>(3).pipe(
      Sink.collectLeftover
    )
  )
)
// first: Chunk(1, 2, 3)
// rest: Chunk(4, 5) - leftovers
```

## Sink Concurrency

### Parallel Sinks

```typescript
// Run sinks in parallel
const parallelSinks = Sink.zipPar(
  Sink.sum,
  Sink.count,
  Sink.collectAll<number>()
)

const [sum, count, all] = yield* Stream.make(1, 2, 3, 4, 5).pipe(
  Stream.run(parallelSinks)
)
```

### Chunked Processing

```typescript
// Process in chunks for efficiency
const chunkedSum = Sink.foldChunks(
  0,
  () => true,
  (sum, chunk: Chunk.Chunk<number>) =>
    sum + Chunk.reduce(chunk, 0, (a, b) => a + b)
)
```

## Common Patterns

### Batched Database Insert

```typescript
const batchInsert = (batchSize: number) =>
  Sink.collectAllN<Record>(batchSize).pipe(
    Sink.mapEffect((batch) =>
      Effect.tryPromise(() => db.insertMany(Chunk.toArray(batch)))
    )
  )

yield* recordStream.pipe(
  Stream.run(batchInsert(100))
)
```

### Aggregation Pipeline

```typescript
const stats = Sink.zip(
  Sink.sum,
  Sink.zip(Sink.count, Sink.zip(Sink.head, Sink.last))
).pipe(
  Sink.map(([sum, [count, [first, last]]]) => ({
    sum,
    count,
    average: count > 0 ? sum / count : 0,
    first,
    last
  }))
)
```

### Write to File

```typescript
const writeToFile = (path: string) =>
  Sink.forEach((line: string) =>
    Effect.gen(function* () {
      const fs = yield* FileSystem
      yield* fs.appendFileString(path, line + "\n")
    })
  )
```

## Best Practices

1. **Use built-in sinks when possible** - Optimized and tested
2. **Combine sinks with zip** - Run multiple aggregations in one pass
3. **Use foldChunks for efficiency** - Process chunks, not elements
4. **Handle leftovers** - Consider unconsumed elements
5. **Prefer Sink over forEach** - More composable

## Additional Resources

For comprehensive sink documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Creating Sinks" for sink construction
- "Sink Operations" for transformations
- "Sink Concurrency" for parallel processing
- "Leftovers" for handling unconsumed elements
