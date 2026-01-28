---
name: effect-ai-prompt
description: Build prompts for Effect AI using messages, parts, and composition operators. Covers the complete Prompt API for constructing, merging, and manipulating conversations with language models.
---

# Effect AI Prompt Construction

Master the `@effect/ai` Prompt API for building type-safe conversations with language models.

## Import Patterns

**CRITICAL**: Always use namespace imports:

```typescript
import * as Prompt from "@effect/ai/Prompt"
import * as Response from "@effect/ai/Response"
import { pipe } from "effect"
```

## When to Use This Skill

- Constructing messages for language model requests
- Building multi-turn conversation history
- Adding system instructions to prompts
- Integrating tool calls and results into conversations
- Converting streaming responses to prompt history
- Managing file/image attachments in messages
- Implementing custom chat interfaces

## Conceptual Model

```haskell
-- Message hierarchy
type Message = SystemMessage | UserMessage | AssistantMessage | ToolMessage
type Part = TextPart | ReasoningPart | FilePart | ToolCallPart | ToolResultPart

-- Composition
Prompt.make       :: RawInput → Prompt
Prompt.merge      :: (Prompt, RawInput) → Prompt
Prompt.setSystem  :: (Prompt, String) → Prompt

-- History transformation
fromResponseParts :: ReadonlyArray<Response.Part> → Prompt
```

## Message Types

Each message has `role` and `content`. Content is an array of `Part` objects.

### System Messages

```typescript
import * as Prompt from "@effect/ai/Prompt"

// String content only
const system = Prompt.makeMessage("system", {
  content: "You are a helpful assistant specialized in mathematics."
})

// Shorthand constructor
const systemShorthand = Prompt.systemMessage({
  content: "You are a helpful assistant specialized in mathematics."
})

// System message with options
const systemWithOptions = Prompt.makeMessage("system", {
  content: "You are an expert coder.",
  options: {
    "anthropic": { cache_control: { type: "ephemeral" } }
  }
})
```

### User Messages

```typescript
// Text-only user message
const userText = Prompt.makeMessage("user", {
  content: [
    Prompt.makePart("text", { text: "What is 2+2?" })
  ]
})

// Shorthand constructor
const userShorthand = Prompt.userMessage({
  content: [
    Prompt.makePart("text", { text: "What is 2+2?" })
  ]
})

// Multimodal user message (text + file)
const userMultimodal = Prompt.makeMessage("user", {
  content: [
    Prompt.makePart("text", { text: "What's in this image?" }),
    Prompt.makePart("file", {
      mediaType: "image/jpeg",
      fileName: "photo.jpg",
      data: new Uint8Array([...])
    })
  ]
})
```

### Assistant Messages

```typescript
// Assistant response with text and tool call
const assistant = Prompt.makeMessage("assistant", {
  content: [
    Prompt.makePart("reasoning", {
      text: "I need to check the weather using the tool."
    }),
    Prompt.makePart("tool-call", {
      id: "call_123",
      name: "get_weather",
      params: { city: "Paris" },
      providerExecuted: false
    }),
    Prompt.makePart("text", {
      text: "The weather in Paris is sunny, 22°C."
    })
  ]
})

// Shorthand constructor
const assistantShorthand = Prompt.assistantMessage({
  content: [
    Prompt.makePart("text", {
      text: "The weather in Paris is sunny, 22°C."
    })
  ]
})
```

### Tool Messages

```typescript
// Tool execution results
const toolMessage = Prompt.makeMessage("tool", {
  content: [
    Prompt.makePart("tool-result", {
      id: "call_123",
      name: "get_weather",
      isFailure: false,
      result: { temperature: 22, condition: "sunny" }
    })
  ]
})

// Shorthand constructor
const toolShorthand = Prompt.toolMessage({
  content: [
    Prompt.makePart("tool-result", {
      id: "call_123",
      name: "get_weather",
      isFailure: false,
      result: { temperature: 22, condition: "sunny" }
    })
  ]
})
```

## Part Types

### Text Part

```typescript
const textPart = Prompt.makePart("text", {
  text: "Hello, world!"
})
```

### Reasoning Part

```typescript
const reasoningPart = Prompt.makePart("reasoning", {
  text: "Let me think step by step..."
})
```

### File Part

```typescript
// From URL
const fileFromUrl = Prompt.makePart("file", {
  mediaType: "image/png",
  fileName: "screenshot.png",
  data: new URL("https://example.com/image.png")
})

// From bytes
const fileFromBytes = Prompt.makePart("file", {
  mediaType: "application/pdf",
  fileName: "report.pdf",
  data: new Uint8Array([1, 2, 3])
})

// From base64
const fileFromBase64 = Prompt.makePart("file", {
  mediaType: "image/jpeg",
  data: "data:image/jpeg;base64,/9j/4AAQ..."
})
```

### Tool Call Part

```typescript
const toolCall = Prompt.makePart("tool-call", {
  id: "call_abc123",
  name: "calculate",
  params: { expression: "2 + 2" },
  providerExecuted: false
})
```

### Tool Result Part

```typescript
const toolResult = Prompt.makePart("tool-result", {
  id: "call_abc123",
  name: "calculate",
  isFailure: false,
  result: 4
})
```

## Prompt Construction

### From String

```typescript
// Creates a user message with text part
const prompt = Prompt.make("Hello, how are you?")
```

### From Messages

```typescript
const prompt = Prompt.make([
  { role: "system", content: "You are helpful." },
  { role: "user", content: [{ type: "text", text: "Hi!" }] }
])
```

### From Existing Prompt

```typescript
const copy = Prompt.make(existingPrompt)
```

### Empty Prompt

```typescript
const empty = Prompt.empty
```

### From Messages Array

```typescript
// Using fromMessages constructor
const messages: ReadonlyArray<Prompt.Message> = [
  Prompt.systemMessage({ content: "You are an expert." }),
  Prompt.userMessage({
    content: [Prompt.makePart("text", { text: "Help me." })]
  })
]

const prompt = Prompt.fromMessages(messages)

// Alternative: Using make with messages array
const prompt2 = Prompt.make([
  Prompt.makeMessage("system", { content: "You are an expert." }),
  Prompt.makeMessage("user", {
    content: [Prompt.makePart("text", { text: "Help me." })]
  })
])
```

## Prompt Composition

### Merge Prompts

```typescript
import { pipe } from "effect"

const systemPrompt = Prompt.make([{
  role: "system",
  content: "You are a coding assistant."
}])

const userPrompt = Prompt.make("Write a function")

// Data-last (pipeline)
const combined = pipe(
  systemPrompt,
  Prompt.merge(userPrompt)
)

// Data-first
const combined2 = Prompt.merge(systemPrompt, userPrompt)
```

### System Message Manipulation

```typescript
import { pipe } from "effect"

const prompt = Prompt.make([
  { role: "system", content: "You are helpful." },
  { role: "user", content: [{ type: "text", text: "Hi" }] }
])

// Replace system message
const replaced = pipe(
  prompt,
  Prompt.setSystem("You are an expert in TypeScript.")
)

// Prepend to system message
const prepended = pipe(
  prompt,
  Prompt.prependSystem("IMPORTANT: ")
)
// Result: "IMPORTANT: You are helpful."

// Append to system message
const appended = pipe(
  prompt,
  Prompt.appendSystem(" Be concise.")
)
// Result: "You are helpful. Be concise."
```

## History Management

### Convert AI Response to Prompt

```typescript
import * as Response from "@effect/ai/Response"

const responseParts: ReadonlyArray<Response.AnyPart> = [
  Response.makePart("text", { text: "Hello!" }),
  Response.makePart("tool-call", {
    id: "call_1",
    name: "get_time",
    params: {},
    providerExecuted: false
  }),
  Response.makePart("tool-result", {
    id: "call_1",
    name: "get_time",
    isFailure: false,
    result: "10:30 AM",
    encodedResult: "10:30 AM",
    providerExecuted: false
  })
]

// Converts to assistant + tool messages
const historyPrompt = Prompt.fromResponseParts(responseParts)
```

### Typical Chat Pattern

```typescript
import { Effect } from "effect"
import * as SubscriptionRef from "effect/SubscriptionRef"
import * as LanguageModel from "@effect/ai/LanguageModel"

const chat = Effect.gen(function* () {
  const history = yield* SubscriptionRef.make(Prompt.empty)

  function* generateText(userInput: string) {
    const currentHistory = yield* SubscriptionRef.get(history)
    const prompt = pipe(
      currentHistory,
      Prompt.merge(userInput)
    )

    const response = yield* LanguageModel.generateText({ prompt })

    // Update history with user input + response
    const newHistory = pipe(
      prompt,
      Prompt.merge(Prompt.fromResponseParts(response.content))
    )
    yield* SubscriptionRef.set(history, newHistory)

    return response
  }

  return { generateText }
})
```

## Usage with LanguageModel

### Generate Text

```typescript
import * as LanguageModel from "@effect/ai/LanguageModel"
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const prompt = Prompt.make([
    { role: "system", content: "You are helpful." },
    { role: "user", content: [{ type: "text", text: "Explain Effect" }] }
  ])

  const response = yield* LanguageModel.generateText({ prompt })

  return response.content
})
```

### Stream Text

```typescript
import * as LanguageModel from "@effect/ai/LanguageModel"
import { Effect, Stream } from "effect"

const program = Effect.gen(function* () {
  const prompt = Prompt.make("Write a story")

  yield* LanguageModel.streamText({ prompt }).pipe(
    Stream.runForEach((part) =>
      part.type === "text-delta"
        ? Effect.sync(() => process.stdout.write(part.delta))
        : Effect.void
    )
  )
})
```

### Generate Object

```typescript
import * as LanguageModel from "@effect/ai/LanguageModel"
import { Effect, Schema } from "effect"

const Contact = Schema.Struct({
  name: Schema.String,
  email: Schema.String,
  phone: Schema.optional(Schema.String)
})

const program = Effect.gen(function* () {
  const prompt = Prompt.make(
    "Extract: John Doe, john@example.com, 555-1234"
  )

  const response = yield* LanguageModel.generateObject({
    prompt,
    schema: Contact
  })

  return response.object
})
```

## Provider-Specific Options

```typescript
// Augment options interfaces via module augmentation
declare module "@effect/ai/Prompt" {
  interface TextPartOptions {
    readonly anthropic?: {
      readonly cache_control?: {
        readonly type: "ephemeral"
      }
    }
  }
}

// Use in parts
const cachedPart = Prompt.makePart("text", {
  text: "Large document...",
  options: {
    anthropic: { cache_control: { type: "ephemeral" } }
  }
})

// Use in messages
const cachedMessage = Prompt.makeMessage("system", {
  content: "You are an expert.",
  options: {
    anthropic: { cache_control: { type: "ephemeral" } }
  }
})
```

## Serialization

### Export/Import

```typescript
import * as Schema from "effect/Schema"
import { Effect } from "effect"

const encode = Schema.encode(Prompt.Prompt)
const decode = Schema.decodeUnknown(Prompt.Prompt)

const program = Effect.gen(function* () {
  const prompt = Prompt.make("Hello")

  // Export to structured data
  const exported = yield* encode(prompt)

  // Import from structured data
  const imported = yield* decode(exported)

  return imported
})
```

### JSON Serialization

```typescript
import * as Schema from "effect/Schema"
import { Effect } from "effect"

const encodeJson = Schema.encode(Prompt.FromJson)
const decodeJson = Schema.decodeUnknown(Prompt.FromJson)

const program = Effect.gen(function* () {
  const prompt = Prompt.make([
    { role: "system", content: "You are helpful." },
    { role: "user", content: [{ type: "text", text: "Hi" }] }
  ])

  // To JSON
  const json = yield* encodeJson(prompt)
  console.log(json) // string

  // From JSON
  const restored = yield* decodeJson(json)

  return restored
})
```

## Common Patterns

### Multi-turn Conversation

```typescript
const conversation = Prompt.make([
  { role: "system", content: "You are a math tutor." },
  { role: "user", content: [{ type: "text", text: "What is 2+2?" }] },
  { role: "assistant", content: [{ type: "text", text: "2+2 equals 4." }] },
  { role: "user", content: [{ type: "text", text: "What about 3+3?" }] }
])
```

### Dynamic System Prompt

```typescript
import { pipe } from "effect"

function withSystemPrompt(content: string) {
  return (prompt: Prompt.Prompt) => pipe(
    prompt,
    Prompt.setSystem(content)
  )
}

const userPrompt = Prompt.make("Help me code")
const withContext = pipe(
  userPrompt,
  withSystemPrompt("You are an expert TypeScript developer.")
)
```

### Tool Interaction History

```typescript
const toolInteraction = Prompt.make([
  { role: "user", content: [{ type: "text", text: "What's the weather?" }] },
  {
    role: "assistant",
    content: [
      { type: "tool-call", id: "1", name: "weather", params: {}, providerExecuted: false }
    ]
  },
  {
    role: "tool",
    content: [
      { type: "tool-result", id: "1", name: "weather", isFailure: false, result: "Sunny, 22°C" }
    ]
  },
  {
    role: "assistant",
    content: [{ type: "text", text: "It's sunny and 22°C." }]
  }
])
```

## Type Guards

```typescript
import * as Prompt from "@effect/ai/Prompt"

declare const value: unknown

if (Prompt.isPrompt(value)) {
  // value: Prompt.Prompt
  console.log(value.content)
}

if (Prompt.isMessage(value)) {
  // value: Prompt.Message
  console.log(value.role)
}

if (Prompt.isPart(value)) {
  // value: Prompt.Part
  console.log(value.type)
}
```

## Anti-Patterns

```typescript
// DON'T: Manually construct messages without constructors
const bad = {
  role: "user",
  content: [{ type: "text", text: "Hello" }]
} as Prompt.UserMessage

// DO: Use constructors
const good = Prompt.makeMessage("user", {
  content: [Prompt.makePart("text", { text: "Hello" })]
})

// DO: Use shorthand constructors
const better = Prompt.userMessage({
  content: [Prompt.makePart("text", { text: "Hello" })]
})

// DON'T: Mutate prompt content
const prompt = Prompt.make("Hi")
prompt.content.push(someMessage) // Error: readonly

// DO: Use merge for composition
const extended = Prompt.merge(prompt, "Additional message")

// DON'T: Manually filter response parts
const filtered = responseParts.filter(p => p.type === "text")

// DO: Use fromResponseParts (handles streaming deltas, tool results, etc.)
const historyPrompt = Prompt.fromResponseParts(responseParts)
```

## Related Skills

- effect-ai-language-model - Using prompts with LanguageModel service
- effect-ai-streaming - Converting streaming responses to prompt history
- effect-ai-tool - Integrating tool call/result messages

## Quality Checklist

- [ ] Messages use `Prompt.makeMessage` or shorthand constructors
- [ ] Parts use `Prompt.makePart` constructors
- [ ] System messages managed with `setSystem`/`prependSystem`/`appendSystem`
- [ ] History updates use `Prompt.fromResponseParts`
- [ ] Prompt composition uses `Prompt.merge` (not mutation)
- [ ] Namespace imports for all @effect/ai modules
