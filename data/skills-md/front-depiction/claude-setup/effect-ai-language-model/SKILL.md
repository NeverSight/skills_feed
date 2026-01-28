---
name: effect-ai-language-model
description: Master the Effect AI LanguageModel service for text generation, structured output, streaming, and tool calling. Use when working with LLM interactions, schema-validated responses, or building conversational AI systems.
---

# Effect AI Language Model

Pattern guide for working with the LanguageModel service from @effect/ai for type-safe LLM interactions with Effect's functional patterns.

## Import Patterns

**CRITICAL**: Always use namespace imports:

```typescript
import * as LanguageModel from "@effect/ai/LanguageModel"
import * as Prompt from "@effect/ai/Prompt"
import * as Response from "@effect/ai/Response"
import * as Toolkit from "@effect/ai/Toolkit"
import * as Tool from "@effect/ai/Tool"
import * as Effect from "effect/Effect"
import * as Stream from "effect/Stream"
import * as Schema from "effect/Schema"
```

## When to Use This Skill

- Generating text completions from language models
- Extracting structured data with schema validation
- Real-time streaming responses for chat interfaces
- Tool calling and function execution
- Multi-turn conversations with history
- Switching between different AI providers

## Service Interface

```haskell
LanguageModel :: Service

-- Core operations
generateText   :: Options → Effect GenerateTextResponse E R
generateObject :: Options → Schema A → Effect (GenerateObjectResponse A) E R
streamText     :: Options → Stream StreamPart E R

-- Service as dependency
LanguageModel ∈ R → Effect.gen(function*() {
  const model = yield* LanguageModel
  const response = yield* model.generateText(options)
})
```

## generateText Pattern

Basic text generation with optional tool calling:

```typescript
import * as LanguageModel from "@effect/ai/LanguageModel"
import * as Effect from "effect/Effect"

// Simple text generation
const simple = LanguageModel.generateText({
  prompt: "Explain quantum computing"
})

// With system prompt and conversation history
const withHistory = LanguageModel.generateText({
  prompt: [
    { role: "system", content: "You are a helpful assistant" },
    { role: "user", content: [{ type: "text", text: "Hello!" }] }
  ]
})

// With toolkit for tool calling
const withTools = LanguageModel.generateText({
  prompt: "What's the weather in SF?",
  toolkit: weatherToolkit,
  toolChoice: "auto"  // "none" | "required" | { tool: "name" } | { oneOf: [...] }
})

// Parallel tool call execution
const withConcurrency = LanguageModel.generateText({
  prompt: "Search multiple sources",
  toolkit: searchToolkit,
  concurrency: "unbounded"  // or number for limited parallelism
})

// Disable automatic tool call resolution
const manualTools = LanguageModel.generateText({
  prompt: "Search for X",
  toolkit: searchToolkit,
  disableToolCallResolution: true  // Get tool calls without executing
})
```

### Response Accessors

```typescript
const response = yield* LanguageModel.generateText({ prompt: "..." })

response.text          // string - concatenated text content
response.toolCalls     // Array<ToolCallParts> - tool invocations
response.toolResults   // Array<ToolResultParts> - tool outputs
response.finishReason  // "stop" | "length" | "tool-calls" | "content-filter" | "unknown"
response.usage         // { inputTokens, outputTokens, totalTokens, reasoningTokens?, cachedInputTokens? }
response.reasoning     // Array<ReasoningPart> - reasoning steps (when model provides extended thinking)
response.reasoningText // string | undefined - concatenated reasoning content
```

## generateObject Pattern (Structured Output)

Force schema-validated output from the model:

```typescript
import * as LanguageModel from "@effect/ai/LanguageModel"
import * as Schema from "effect/Schema"
import * as Effect from "effect/Effect"

// Define output schema
const ContactSchema = Schema.Struct({
  name: Schema.String,
  email: Schema.String,
  phone: Schema.optional(Schema.String)
})

// Generate structured output
const extractContact = LanguageModel.generateObject({
  prompt: "Extract: John Doe, john@example.com, 555-1234",
  schema: ContactSchema,
  objectName: "contact"  // Optional, aids model understanding
})

// Usage
const program = Effect.gen(function* () {
  const response = yield* extractContact

  response.value  // { name: "John Doe", email: "john@example.com", phone: "555-1234" }
  response.text   // Raw generated text (JSON)
  response.usage  // Token usage stats

  return response.value
})
```

### Schema-driven ADT extraction

```typescript
const EventType = Schema.TaggedStruct("EventType", {
  _tag: Schema.Literal("meeting", "deadline", "reminder"),
  title: Schema.String,
  date: Schema.String
})

const extractEvent = LanguageModel.generateObject({
  prompt: "Parse: Team meeting on March 15th",
  schema: EventType
})
```

## streamText Pattern

Real-time streaming text generation:

```typescript
import * as LanguageModel from "@effect/ai/LanguageModel"
import * as Stream from "effect/Stream"
import * as Effect from "effect/Effect"
import * as Console from "effect/Console"

// Basic streaming
const streamStory = LanguageModel.streamText({
  prompt: "Write a story about space exploration"
})

// Process stream parts
const program = streamStory.pipe(
  Stream.runForEach((part) => {
    if (part.type === "text-delta") {
      return Console.log(part.delta)
    }
    if (part.type === "tool-params-delta") {
      return Console.log("Tool params:", part.paramsDelta)
    }
    return Effect.void
  })
)
```

### StreamPart Types

```haskell
StreamPart =
  | { type: "text-delta", delta: string }
  | { type: "tool-params-start", id, name }
  | { type: "tool-params-delta", id, paramsDelta }
  | { type: "tool-call", id, name, params }
  | { type: "tool-result", id, name, result, isFailure }
  | { type: "finish", reason: FinishReason, usage: Usage }
  | { type: "error", error: AiError }
```

### Stream Processing Patterns

```typescript
// Collect all text deltas
const collectText = streamText.pipe(
  Stream.filter((part) => part.type === "text-delta"),
  Stream.map((part) => part.delta),
  Stream.runFold("", (acc, delta) => acc + delta)
)

// Process chunks efficiently
const processChunks = streamText.pipe(
  Stream.mapChunksEffect((chunk) =>
    Effect.gen(function* () {
      const parts = Array.from(chunk)
      // Process batch of parts
      yield* handleBatch(parts)
      return chunk
    })
  )
)

// Aggregate response with side effects
let combined: Array<StreamPart> = []
const aggregated = streamText.pipe(
  Stream.mapChunks((chunk) => {
    combined = [...combined, ...chunk]
    return chunk
  }),
  Stream.ensuring(Effect.sync(() => {
    // Finalization logic with full response
    console.log("Total parts:", combined.length)
  }))
)
```

## toolChoice Options

Control when and which tools the model can use:

```typescript
// Auto-decide (default)
toolChoice: "auto"  // Model decides whether to call tools

// Never use tools
toolChoice: "none"  // Force text-only response

// Must use a tool
toolChoice: "required"  // Model must call at least one tool

// Specific tool required
toolChoice: { tool: "search" }  // Must call "search" tool

// Restricted subset - auto mode
toolChoice: {
  oneOf: ["search", "calculate"]  // Can use these tools or respond with text
}

// Restricted subset - required mode
toolChoice: {
  mode: "required",
  oneOf: ["search", "calculate"]  // Must call one of these tools
}
```

## Error Handling

```typescript
import * as AiError from "@effect/ai/AiError"

const robust = LanguageModel.generateText({
  prompt: "Analyze this..."
}).pipe(
  Effect.catchTag("AiError", (error) => {
    // Handle API errors, rate limits, malformed output, etc.
    return Effect.succeed(fallbackResponse)
  }),
  Effect.catchTag("MalformedOutput", (error) => {
    // Schema validation failed in generateObject
    return Effect.succeed(defaultValue)
  })
)
```

## Type Extraction Utilities

```typescript
import type * as LanguageModel from "@effect/ai/LanguageModel"

// Extract error types from options
type MyError = LanguageModel.ExtractError<typeof options>

// Extract context requirements from options
type MyRequirements = LanguageModel.ExtractContext<typeof options>

// Inferred based on:
// - toolkit: Toolkit.WithHandler<Tools> → Tool.HandlerError<Tools> ∈ E
// - toolkit: Effect<Toolkit, E, R> → E | Tool.HandlerError<Tools> ∈ E, R ∈ R
// - disableToolCallResolution: true → no Tool.HandlerError in E
```

## Provider Implementation Pattern

Create custom LanguageModel providers using `LanguageModel.make`:

```haskell
make :: ConstructorParams → Effect Service
```

When implementing a custom LanguageModel provider:

```typescript
import * as LanguageModel from "@effect/ai/LanguageModel"
import * as Response from "@effect/ai/Response"
import * as AiError from "@effect/ai/AiError"

const makeCustomProvider = Effect.gen(function* () {
  const service = yield* LanguageModel.make({
    generateText: (options: LanguageModel.ProviderOptions) =>
      Effect.gen(function* () {
        // options.prompt: Prompt.Prompt
        // options.tools: ReadonlyArray<Tool.Any>
        // options.toolChoice: ToolChoice<any>
        // options.responseFormat: { type: "text" } | { type: "json", schema, objectName }
        // options.span: Span (for telemetry)

        const result = yield* callProviderAPI(options)

        // Return Response.PartEncoded[]
        return [
          Response.makePart("text", { text: result.content }),
          Response.makePart("finish", {
            reason: "stop",
            usage: new Response.Usage({
              inputTokens: result.usage.input,
              outputTokens: result.usage.output,
              totalTokens: result.usage.total
            })
          })
        ]
      }),

    streamText: (options: LanguageModel.ProviderOptions) =>
      Stream.fromAsyncIterable(
        providerStreamAPI(options),
        (error) => new AiError.AiError({ message: String(error) })
      ).pipe(
        Stream.map((chunk) =>
          Response.makePart("text-delta", { delta: chunk.text })
        )
      )
  })

  return service
})
```

## Common Patterns

### Multi-turn with context

```typescript
const conversation = Effect.gen(function* () {
  let history: Prompt.Prompt = Prompt.empty

  const ask = (message: string) =>
    Effect.gen(function* () {
      const prompt = Prompt.merge(history, Prompt.user(message))
      const response = yield* LanguageModel.generateText({ prompt })
      history = Prompt.merge(prompt, Prompt.fromResponseParts(response.content))
      return response.text
    })

  const answer1 = yield* ask("What is TypeScript?")
  const answer2 = yield* ask("How does it differ from JavaScript?")

  return { answer1, answer2 }
})
```

### Parallel requests

```typescript
const parallel = Effect.all([
  LanguageModel.generateText({ prompt: "Summarize A" }),
  LanguageModel.generateText({ prompt: "Summarize B" }),
  LanguageModel.generateText({ prompt: "Summarize C" })
], { concurrency: "unbounded" })
```

### Retry with backoff

```typescript
const resilient = LanguageModel.generateText({ prompt: "..." }).pipe(
  Effect.retry({
    times: 3,
    schedule: Schedule.exponential("100 millis")
  })
)
```

## Anti-patterns

```typescript
// ❌ Nested callbacks
LanguageModel.generateText({ prompt: "A" }).pipe(
  Effect.flatMap((r1) =>
    LanguageModel.generateText({ prompt: "B" }).pipe(
      Effect.flatMap((r2) => ...)
    )
  )
)

// ✅ Effect.gen
Effect.gen(function* () {
  const r1 = yield* LanguageModel.generateText({ prompt: "A" })
  const r2 = yield* LanguageModel.generateText({ prompt: "B" })
  return combine(r1, r2)
})

// ❌ Manual error construction
Effect.fail(new Error("Failed"))

// ✅ Tagged errors
Effect.fail(new AiError.AiError({ message: "Failed" }))

// ❌ Promise-based streaming
streamText.pipe(Stream.runCollect, Effect.map(toPromise))

// ✅ Effect-based consumption
streamText.pipe(Stream.runForEach(processPart))

// ❌ Ignoring finishReason
const text = response.text  // May be truncated

// ✅ Check finish reason
if (response.finishReason === "length") {
  // Handle truncation
}
```

## Quality Checklist

- [ ] Use `generateText` for single-turn completions
- [ ] Use `generateObject` with Schema for structured output
- [ ] Use `streamText` for real-time streaming responses
- [ ] Check `finishReason` to detect truncation
- [ ] Handle errors with `catchTag("AiError", ...)`
- [ ] Use `Effect.gen` over flatMap chains
- [ ] Access service via `yield* LanguageModel`
- [ ] Provide toolkit for tool calling
- [ ] Set appropriate `toolChoice` mode
- [ ] Use `concurrency` for parallel tool execution

## Related Skills

- effect-ai-prompt - Constructing and composing prompts
- effect-ai-tool - Creating tools and toolkits
- effect-ai-streaming - Processing stream responses
- effect-ai-provider - Configuring provider layers

## References

- Source: `.context/effect/packages/ai/ai/src/LanguageModel.ts`
- Chat integration: `packages/ai/src/Chat.ts`
- Response types: `@effect/ai/Response`
- Tool system: `@effect/ai/Tool`, `@effect/ai/Toolkit`
