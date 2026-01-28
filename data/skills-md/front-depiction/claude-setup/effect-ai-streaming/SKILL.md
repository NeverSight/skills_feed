---
name: effect-ai-streaming
description: Master Effect AI streaming response patterns including start/delta/end protocol, accumulation strategies, resource-safe consumption, and history management with SubscriptionRef.
---

# Effect AI Streaming

## When to Use This Skill

- Real-time streaming responses from language models
- Building chat interfaces with incremental updates
- Managing conversation history with streaming
- Protecting concurrent stream operations
- Accumulating stream parts with side effects
- Converting stream responses to prompt history

## Import Patterns

**CRITICAL**: Always use namespace imports:

```typescript
import * as Stream from "effect/Stream"
import * as Effect from "effect/Effect"
import * as Channel from "effect/Channel"
import * as SubscriptionRef from "effect/SubscriptionRef"
import * as Match from "effect/Match"
import * as Response from "@effect/ai/Response"
```

## StreamPart Protocol

stream := start → delta* → end

StreamPart lifecycle for each content type follows a three-phase protocol:

```haskell
text      :: text-start → text-delta* → text-end
reasoning :: reasoning-start → reasoning-delta* → reasoning-end
toolParam :: tool-params-start → tool-params-delta* → tool-params-end
finish    :: { type: "finish", reason: FinishReason, usage: Usage }
```

Each streaming sequence has a unique `id` field that links start/delta/end parts.

## Part Type Matching

Pattern match on stream parts using Match.value:

```typescript
import * as Match from "effect/Match"
import * as Effect from "effect/Effect"

const processPart = (part: StreamPart) =>
  Match.value(part).pipe(
    Match.tag("text-delta", ({ delta }) =>
      Effect.sync(() => console.log(delta))
    ),
    Match.tag("reasoning-delta", ({ delta }) =>
      Effect.sync(() => logReasoning(delta))
    ),
    Match.tag("finish", ({ usage, reason }) =>
      Effect.sync(() => recordUsage(usage, reason))
    ),
    Match.orElse(() => Effect.void)
  )
```

Type guards for stream parts (polymorphic over encoded/decoded):

```typescript
isTextDelta :: ∀ P. HasType P ⇒ P → P is TextDelta
isToolCallPart :: ∀ P. HasType P ⇒ P → P is ToolCall
isFinishPart :: ∀ P. HasType P ⇒ P → P is Finish
```

## Accumulation Pattern

Accumulate stream parts incrementally using mutable state for efficiency:

```typescript
import * as Stream from "effect/Stream"
import * as Effect from "effect/Effect"
import * as Prompt from "@effect/ai/Prompt"

const accumulated: Array<StreamPart> = []
let combined = Prompt.empty

stream.pipe(
  Stream.mapChunksEffect(Effect.fnUntraced(function* (chunk) {
    const parts = Array.from(chunk)

    // Append to mutable accumulator
    accumulated.push(...parts)

    // Build prompt from accumulated parts
    combined = Prompt.merge(combined, Prompt.fromResponseParts(parts))

    // Update history incrementally
    yield* SubscriptionRef.set(history, Prompt.merge(checkpoint, combined))

    return chunk
  }))
)
```

Key insight: `Stream.mapChunksEffect` enables side-effectful accumulation while preserving stream semantics.

## Resource-Safe Streaming

Prevent concurrent stream operations using semaphore protection:

```typescript
import * as Channel from "effect/Channel"
import * as Semaphore from "effect/Semaphore"
import * as Stream from "effect/Stream"

const streamWithProtection = Stream.fromChannel(
  Channel.acquireUseRelease(
    // Acquire: Take semaphore, get checkpoint
    semaphore.take(1).pipe(
      Effect.zipRight(SubscriptionRef.get(history)),
      Effect.map((hist) => Prompt.merge(hist, newPrompt)),
      Effect.tap((checkpoint) =>
        SubscriptionRef.set(history, checkpoint)
      )
    ),

    // Use: Stream with accumulation
    (checkpoint) => LanguageModel.streamText({ prompt: checkpoint }).pipe(
      Stream.mapChunksEffect(accumulateAndUpdate),
      Stream.toChannel
    ),

    // Release: Always release semaphore
    () => semaphore.release(1)
  )
)
```

Resource acquisition order:
1. Take semaphore (exclusive access)
2. Get current history snapshot
3. Merge with new prompt
4. Update history with checkpoint
5. Stream response (with incremental updates)
6. Release semaphore (guaranteed via `acquireUseRelease`)

## Consumption Patterns

runForEach :: (A → Effect<R, E>) → Stream<A, E, R> → Effect<Unit, E, R>
runDrain   :: Stream<A, E, R> → Effect<Unit, E, R>
runLast    :: Stream<A, E, R> → Effect<Option<A>, E, R>

```typescript
// Process each part with side effects
stream.pipe(
  Stream.runForEach((part) =>
    Match.value(part).pipe(
      Match.tag("text-delta", ({ delta }) => updateUI(delta)),
      Match.tag("finish", ({ usage }) => recordMetrics(usage)),
      Match.orElse(() => Effect.void)
    )
  )
)

// Consume without collecting (memory efficient)
stream.pipe(
  Stream.tap(logPart),
  Stream.runDrain
)

// Get final accumulated value
stream.pipe(
  Stream.runFold(initialState, (acc, part) => merge(acc, part)),
  Effect.map(Option.some)
)
```

## History Update Pattern

Incremental merge strategy for conversation history:

```typescript
Prompt.merge :: Prompt → Prompt → Prompt
Prompt.fromResponseParts :: Array<StreamPart> → Prompt

// Pattern: checkpoint + incremental merge
let combined = Prompt.empty

Stream.mapChunksEffect(function* (chunk) {
  const parts = Array.from(chunk)

  // Merge new parts into combined prompt
  combined = Prompt.merge(combined, Prompt.fromResponseParts(parts))

  // Update history: base checkpoint + accumulated response
  yield* SubscriptionRef.set(
    history,
    Prompt.merge(filteredCheckpoint, combined)
  )

  return chunk
})
```

Why checkpoint-based merging:
- Prevents re-merging entire history on each chunk
- Separates base state (checkpoint) from streaming accumulation (combined)
- Enables atomic history updates via SubscriptionRef

## Complete Example

```typescript
import * as AI from "@effect/ai"
import * as Stream from "effect/Stream"
import * as Effect from "effect/Effect"
import * as SubscriptionRef from "effect/SubscriptionRef"
import * as Semaphore from "effect/Semaphore"
import * as Match from "effect/Match"

const Chat = Effect.gen(function* () {
  const history = yield* SubscriptionRef.make(AI.Prompt.empty)
  const semaphore = yield* Semaphore.make(1)

  const streamText = (prompt: string) =>
    Stream.fromChannel(
      Channel.acquireUseRelease(
        // Acquire
        semaphore.take(1).pipe(
          Effect.zipRight(SubscriptionRef.get(history)),
          Effect.map((hist) => AI.Prompt.merge(hist, AI.Prompt.make(prompt))),
          Effect.tap((checkpoint) => {
            combined = AI.Prompt.empty
            return SubscriptionRef.set(history, checkpoint)
          })
        ),

        // Use
        (checkpoint) => {
          let combined = AI.Prompt.empty
          const accumulated: Array<AI.Response.StreamPart> = []

          return AI.LanguageModel.streamText({ prompt: checkpoint }).pipe(
            Stream.mapChunksEffect(Effect.fnUntraced(function* (chunk) {
              const parts = Array.from(chunk)
              accumulated.push(...parts)

              combined = AI.Prompt.merge(
                combined,
                AI.Prompt.fromResponseParts(parts)
              )

              yield* SubscriptionRef.set(
                history,
                AI.Prompt.merge(checkpoint, combined)
              )

              return chunk
            })),
            Stream.toChannel
          )
        },

        // Release
        () => semaphore.release(1)
      )
    )

  return { streamText }
})

// Consume stream
chat.streamText("Hello").pipe(
  Stream.runForEach((part) =>
    Match.value(part).pipe(
      Match.tag("text-delta", ({ delta }) => Effect.sync(() => console.log(delta))),
      Match.tag("finish", ({ usage }) => Effect.sync(() => console.log(usage))),
      Match.orElse(() => Effect.void)
    )
  )
)
```

## Anti-Patterns

```typescript
// ❌ Avoid Effect.either for pattern matching
Effect.either(effect).pipe(
  Effect.map((result) => result._tag === "Left" ? ... : ...)
)

// ✓ Use Match.typeTags or Effect.match
effect.pipe(
  Effect.match({
    onFailure: (error) => ...,
    onSuccess: (value) => ...
  })
)

// ❌ Manual type checking (use Match.tag instead)
if (part.type === "text-delta") { ... }

// ✓ Use Match.tag or type guards
Match.value(part).pipe(Match.tag("text-delta", handler))
isTextDelta(part) ? handler(part.delta) : ...

// ❌ Accumulating in Stream.map (loses effects)
Stream.map((chunk) => {
  accumulated.push(...chunk) // side effect ignored
  return chunk
})

// ✓ Use Stream.mapChunksEffect
Stream.mapChunksEffect(Effect.fnUntraced(function* (chunk) {
  accumulated.push(...chunk)
  yield* updateHistory()
  return chunk
}))
```

## Additional Stream Part Types

### File Parts
```typescript
{ type: "file", mediaType: "image/png", data: Uint8Array }
```

### Source Parts
```typescript
{ type: "document-source", id: string, title?: string }
{ type: "url-source", url: string, title?: string }
```

### Metadata Parts
```typescript
{ type: "response-metadata", id: string, modelId: string, timestamp: Date }
```

### Error Parts
```typescript
{ type: "error", error: AiError }
// Handle with:
Match.tag("error", ({ error }) => Effect.fail(error))
```

## Quality Checklist

- [ ] Use start/delta/end protocol for streaming content
- [ ] Match stream parts with Match.tag (not manual type checks)
- [ ] Accumulate using Stream.mapChunksEffect (not Stream.map)
- [ ] Use SubscriptionRef for reactive history updates
- [ ] Protect concurrent streams with Semaphore
- [ ] Use Channel.acquireUseRelease for resource safety
- [ ] Handle error parts appropriately
- [ ] Checkpoint history before streaming

## Related Skills

- effect-ai-language-model - streamText method that produces these streams
- effect-ai-prompt - Converting stream responses to history with fromResponseParts
- effect-ai-tool - Tool call streaming parts
- effect-ai-provider - Provider-specific streaming behavior

## Reference

StreamPart types:
- `text-start`, `text-delta`, `text-end` - Text content streaming
- `reasoning-start`, `reasoning-delta`, `reasoning-end` - Chain-of-thought streaming
- `tool-params-start`, `tool-params-delta`, `tool-params-end` - Tool parameter streaming
- `tool-call` - Complete tool invocation (non-streaming)
- `tool-result` - Tool execution result
- `finish` - Stream completion with usage stats
- `error` - Error part

Key modules:
- `@effect/ai/Response` - Response part schemas and constructors
- `@effect/ai/Prompt` - Prompt construction and merging
- `effect/Stream` - Stream combinators (`mapChunksEffect`, `runForEach`, `runDrain`)
- `effect/Channel` - Low-level resource management (`acquireUseRelease`)
- `effect/SubscriptionRef` - Reactive shared state
- `effect/Match` - Pattern matching on tagged types
