---
name: effect-ai-provider
description: Configure and compose AI provider layers using @effect/ai packages. Covers Anthropic, OpenAI, OpenRouter, Google, and Amazon Bedrock providers with config management, model abstraction, and runtime overrides for language model integration.
---

# Effect AI Provider

Configure AI provider layers for language model integration using Effect's @effect/ai ecosystem.

## When to Use This Skill

Use this skill when:
- Integrating AI language models (Anthropic, OpenAI, Google, etc.) into Effect applications
- Setting up multi-provider AI architectures with runtime switching
- Implementing stateful chat conversations with context history
- Working with embeddings for semantic search or RAG systems
- Managing AI provider configuration and API keys securely
- Composing AI capabilities with other Effect services

## Import Patterns

**CRITICAL**: Always use namespace imports:

```typescript
// Core
import * as LanguageModel from "@effect/ai/LanguageModel"
import * as Chat from "@effect/ai/Chat"
import * as EmbeddingModel from "@effect/ai/EmbeddingModel"
import * as Model from "@effect/ai/Model"

// Anthropic
import * as AnthropicClient from "@effect/ai-anthropic/AnthropicClient"
import * as AnthropicLanguageModel from "@effect/ai-anthropic/AnthropicLanguageModel"
import * as AnthropicTokenizer from "@effect/ai-anthropic/AnthropicTokenizer"

// OpenAI
import * as OpenAiClient from "@effect/ai-openai/OpenAiClient"
import * as OpenAiLanguageModel from "@effect/ai-openai/OpenAiLanguageModel"
import * as OpenAiEmbeddingModel from "@effect/ai-openai/OpenAiEmbeddingModel"

// OpenRouter
import * as OpenRouterClient from "@effect/ai-openrouter/OpenRouterClient"
import * as OpenRouterLanguageModel from "@effect/ai-openrouter/OpenRouterLanguageModel"

// Google
import * as GoogleClient from "@effect/ai-google/GoogleClient"
import * as GoogleLanguageModel from "@effect/ai-google/GoogleLanguageModel"

// Amazon Bedrock
import * as BedrockClient from "@effect/ai-amazon-bedrock/BedrockClient"
import * as BedrockLanguageModel from "@effect/ai-amazon-bedrock/BedrockLanguageModel"

// Effect
import * as Config from "effect/Config"
import * as Layer from "effect/Layer"
import * as Effect from "effect/Effect"
```

## Provider Layer Pattern

```haskell
providerLayer :: Model → Layer LanguageModel Client
providerLayer model = ProviderLanguageModel.layer({ model })
  |> Layer.provide(ProviderClient.layerConfig(...))

configLayer :: Config → Layer Client ∅
configLayer = Client.layerConfig({ apiKey: Config.redacted("API_KEY") })
```

## Anthropic Provider

```typescript
import * as AnthropicClient from "@effect/ai-anthropic/AnthropicClient"
import * as AnthropicLanguageModel from "@effect/ai-anthropic/AnthropicLanguageModel"
import * as Config from "effect/Config"
import * as Layer from "effect/Layer"

const AnthropicLive = AnthropicLanguageModel.layer({
  model: "claude-sonnet-4-20250514"
}).pipe(
  Layer.provide(
    AnthropicClient.layerConfig({
      apiKey: Config.redacted("ANTHROPIC_API_KEY")
    })
  )
)
```

## OpenAI Provider

```typescript
import * as OpenAiClient from "@effect/ai-openai/OpenAiClient"
import * as OpenAiLanguageModel from "@effect/ai-openai/OpenAiLanguageModel"

const OpenAiLive = OpenAiLanguageModel.layer({
  model: "gpt-4o"
}).pipe(
  Layer.provide(
    OpenAiClient.layerConfig({
      apiKey: Config.redacted("OPENAI_API_KEY")
    })
  )
)
```

## OpenRouter Provider

Multi-provider access through unified interface:

```typescript
import * as OpenRouterClient from "@effect/ai-openrouter/OpenRouterClient"
import * as OpenRouterLanguageModel from "@effect/ai-openrouter/OpenRouterLanguageModel"

const OpenRouterLive = OpenRouterLanguageModel.layer({
  model: "anthropic/claude-sonnet-4"
}).pipe(
  Layer.provide(
    OpenRouterClient.layerConfig({
      apiKey: Config.redacted("OPENROUTER_API_KEY")
    })
  )
)
```

## Google Provider

```typescript
import * as GoogleClient from "@effect/ai-google/GoogleClient"
import * as GoogleLanguageModel from "@effect/ai-google/GoogleLanguageModel"

const GoogleLive = GoogleLanguageModel.layer({
  model: "gemini-2.0-flash-exp"
}).pipe(
  Layer.provide(
    GoogleClient.layerConfig({
      apiKey: Config.redacted("GOOGLE_API_KEY")
    })
  )
)
```

## Amazon Bedrock Provider

```typescript
import * as BedrockClient from "@effect/ai-amazon-bedrock/BedrockClient"
import * as BedrockLanguageModel from "@effect/ai-amazon-bedrock/BedrockLanguageModel"

const BedrockLive = BedrockLanguageModel.layer({
  model: "anthropic.claude-3-5-sonnet-20241022-v2:0"
}).pipe(
  Layer.provide(
    BedrockClient.layerConfig({
      region: "us-east-1"
    })
  )
)
```

## Tokenizer Integration

Count and manage tokens for model context limits:

```typescript
import * as AnthropicTokenizer from "@effect/ai-anthropic/AnthropicTokenizer"
import * as Effect from "effect/Effect"

const program = Effect.gen(function* () {
  // Count tokens
  const count = yield* AnthropicTokenizer.countTokens("Hello world")

  // Truncate to limit
  const text = "Very long text that exceeds token limit..."
  const truncated = yield* AnthropicTokenizer.truncate(text, 4000)

  return { count, truncated }
})
```

## EmbeddingModel Service

Generate vector embeddings for semantic search and RAG:

```typescript
import * as EmbeddingModel from "@effect/ai/EmbeddingModel"
import * as OpenAiEmbeddingModel from "@effect/ai-openai/OpenAiEmbeddingModel"
import * as OpenAiClient from "@effect/ai-openai/OpenAiClient"
import * as Config from "effect/Config"
import * as Layer from "effect/Layer"

const EmbeddingLive = OpenAiEmbeddingModel.layer({
  model: "text-embedding-3-small"
}).pipe(
  Layer.provide(
    OpenAiClient.layerConfig({
      apiKey: Config.redacted("OPENAI_API_KEY")
    })
  )
)

const program = Effect.gen(function* () {
  // Single embedding
  const embedding = yield* EmbeddingModel.embed("Search query")

  // Batch embeddings
  const embeddings = yield* EmbeddingModel.embedAll([
    "Document 1",
    "Document 2",
    "Document 3"
  ])

  return embeddings
})

Effect.runPromise(program.pipe(Effect.provide(EmbeddingLive)))
```

## Chat Service (Stateful Conversations)

Maintain conversation history with automatic context management:

```typescript
import * as Chat from "@effect/ai/Chat"
import * as AnthropicLanguageModel from "@effect/ai-anthropic/AnthropicLanguageModel"
import * as AnthropicClient from "@effect/ai-anthropic/AnthropicClient"
import * as Config from "effect/Config"
import * as Layer from "effect/Layer"
import * as Effect from "effect/Effect"

const AnthropicLive = AnthropicLanguageModel.layer({
  model: "claude-sonnet-4-20250514"
}).pipe(
  Layer.provide(
    AnthropicClient.layerConfig({
      apiKey: Config.redacted("ANTHROPIC_API_KEY")
    })
  )
)

const program = Effect.gen(function* () {
  // Create empty chat
  const chat = yield* Chat.empty

  // Or with initial system prompt
  const chatWithSystem = yield* Chat.make({
    system: "You are a helpful assistant"
  })

  // Methods mirror LanguageModel but maintain history
  const response1 = yield* chat.generateText({
    prompt: "What is Effect?"
  })

  // Follow-up has context from previous message
  const response2 = yield* chat.generateText({
    prompt: "Can you elaborate on that?"
  })

  // Export for persistence
  const exported = yield* chat.exportJson

  // Import from persisted state
  const restored = yield* Chat.fromJson(exported)

  return { response1, response2, exported }
})

Effect.runPromise(program.pipe(Effect.provide(AnthropicLive)))
```

## Config Override Pattern

Runtime configuration adjustment without rebuilding layers:

```haskell
withConfigOverride :: Partial<ProviderConfig> → Layer LanguageModel Client
```

```typescript
const CustomAnthropicLive = AnthropicLanguageModel.layer({
  model: "claude-sonnet-4-20250514"
}).pipe(
  AnthropicLanguageModel.withConfigOverride({
    temperature: 0.7,
    max_tokens: 4096
  }),
  Layer.provide(
    AnthropicClient.layerConfig({
      apiKey: Config.redacted("ANTHROPIC_API_KEY")
    })
  )
)
```

## Model Abstraction

Wrap provider layers with metadata:

```haskell
Model.make :: { name :: String, layer :: Layer LanguageModel Client } → Model
Model.ProviderName :: Model → String
```

```typescript
import * as Model from "@effect/ai/Model"

const Claude = Model.make({
  name: "claude-sonnet-4",
  layer: AnthropicLive
})

const provider = Model.ProviderName(Claude) // "anthropic"
```

## Multi-Provider Setup

```typescript
import * as Effect from "effect/Effect"
import * as Layer from "effect/Layer"
import * as LanguageModel from "@effect/ai/LanguageModel"

const AppLive = Layer.mergeAll(
  AnthropicLive,
  OpenAiLive,
  OpenRouterLive
)

const program = Effect.gen(function* () {
  const model = yield* LanguageModel.LanguageModel
  const response = yield* model.generate("Hello")
  return response
})

Effect.runPromise(program.pipe(Effect.provide(AnthropicLive)))
```

## Available Providers

| Package | Provider | Models |
|---------|----------|--------|
| `@effect/ai-anthropic` | Anthropic | Claude 3.x, Claude Sonnet 4 |
| `@effect/ai-openai` | OpenAI | GPT-4, GPT-4o, o1 |
| `@effect/ai-openrouter` | OpenRouter | Multi-provider proxy |
| `@effect/ai-google` | Google | Gemini 1.5, 2.0 |
| `@effect/ai-amazon-bedrock` | AWS Bedrock | Cross-provider on AWS |

## Patterns

```haskell
-- Layer composition
providerLayer ∘ configLayer :: Layer LanguageModel ∅

-- Config management
Config.redacted :: String → Config Redacted<String>

-- Runtime override
layer |> withConfigOverride(config) :: Layer A R

-- Provider selection
Model.make({ name, layer }) :: Model
```

## Anti-Patterns

```typescript
// ❌ Hardcoded API keys
AnthropicClient.layerConfig({ apiKey: "sk-..." })

// ✅ Config.redacted for secrets
AnthropicClient.layerConfig({
  apiKey: Config.redacted("ANTHROPIC_API_KEY")
})

// ❌ Rebuilding layer for config changes
const newLayer = AnthropicLanguageModel.layer({
  model: "claude-sonnet-4-20250514",
  temperature: 0.9
})

// ✅ Use withConfigOverride
AnthropicLive.pipe(
  AnthropicLanguageModel.withConfigOverride({ temperature: 0.9 })
)

// ❌ Direct client construction
new AnthropicClient({ apiKey: "..." })

// ✅ Layer-based dependency injection
AnthropicClient.layerConfig({ apiKey: Config.redacted("...") })
```

## Quality Checklist

- [ ] Use Config.redacted for API keys (never hardcode)
- [ ] Compose with Layer.provide for dependencies
- [ ] Use withConfigOverride for runtime config changes
- [ ] Wrap in Model.make for metadata abstraction
- [ ] Layer.mergeAll for multi-provider setups
- [ ] Include Tokenizer for token counting
- [ ] Use Chat service for stateful conversations
- [ ] Use EmbeddingModel for vector embeddings

## Complete Working Example

Full application with language model, chat, embeddings, and tokenization:

```typescript
import * as LanguageModel from "@effect/ai/LanguageModel"
import * as Chat from "@effect/ai/Chat"
import * as EmbeddingModel from "@effect/ai/EmbeddingModel"
import * as Model from "@effect/ai/Model"
import * as AnthropicClient from "@effect/ai-anthropic/AnthropicClient"
import * as AnthropicLanguageModel from "@effect/ai-anthropic/AnthropicLanguageModel"
import * as AnthropicTokenizer from "@effect/ai-anthropic/AnthropicTokenizer"
import * as OpenAiClient from "@effect/ai-openai/OpenAiClient"
import * as OpenAiEmbeddingModel from "@effect/ai-openai/OpenAiEmbeddingModel"
import * as Config from "effect/Config"
import * as Layer from "effect/Layer"
import * as Effect from "effect/Effect"
import * as Console from "effect/Console"

// Provider Layers
const AnthropicLive = AnthropicLanguageModel.layer({
  model: "claude-sonnet-4-20250514"
}).pipe(
  AnthropicLanguageModel.withConfigOverride({
    temperature: 0.7,
    max_tokens: 4096
  }),
  Layer.provide(
    AnthropicClient.layerConfig({
      apiKey: Config.redacted("ANTHROPIC_API_KEY")
    })
  )
)

const EmbeddingLive = OpenAiEmbeddingModel.layer({
  model: "text-embedding-3-small"
}).pipe(
  Layer.provide(
    OpenAiClient.layerConfig({
      apiKey: Config.redacted("OPENAI_API_KEY")
    })
  )
)

// Combined application layer
const AppLive = Layer.mergeAll(AnthropicLive, EmbeddingLive)

// Program using all AI capabilities
const program = Effect.gen(function* () {
  // Token counting
  const prompt = "Explain functional programming"
  const tokenCount = yield* AnthropicTokenizer.countTokens(prompt)
  yield* Console.log(`Prompt tokens: ${tokenCount}`)

  // Simple generation
  const model = yield* LanguageModel.LanguageModel
  const simple = yield* model.generateText({ prompt })
  yield* Console.log(`Simple response: ${simple}`)

  // Stateful chat
  const chat = yield* Chat.make({
    system: "You are a functional programming expert"
  })

  const response1 = yield* chat.generateText({
    prompt: "What is Effect?"
  })

  const response2 = yield* chat.generateText({
    prompt: "How does it handle errors?"
  })

  // Export chat for persistence
  const chatState = yield* chat.exportJson

  // Generate embeddings
  const embedding = yield* EmbeddingModel.embed(
    "functional programming concepts"
  )

  const batchEmbeddings = yield* EmbeddingModel.embedAll([
    "monads",
    "functors",
    "effect systems"
  ])

  return {
    tokenCount,
    simple,
    chatResponses: { response1, response2 },
    chatState,
    embeddingDimensions: embedding.length,
    batchCount: batchEmbeddings.length
  }
})

// Run with environment variables:
// ANTHROPIC_API_KEY=sk-... OPENAI_API_KEY=sk-... node program.js
Effect.runPromise(program.pipe(Effect.provide(AppLive)))
```

## Model Abstraction Pattern

Create reusable model configurations:

```typescript
import * as Model from "@effect/ai/Model"

const Claude = Model.make({
  name: "claude-sonnet-4",
  layer: AnthropicLive
})

const GPT4 = Model.make({
  name: "gpt-4o",
  layer: OpenAiLive
})

// Runtime model selection
const selectModel = (useGPT: boolean) =>
  useGPT ? GPT4.layer : Claude.layer

const program = Effect.gen(function* () {
  const model = yield* LanguageModel.LanguageModel
  return yield* model.generateText({ prompt: "Hello" })
})

// Switch providers at runtime
Effect.runPromise(
  program.pipe(Effect.provide(selectModel(false)))
)
```

## Related Skills

- effect-ai-language-model - Using LanguageModel service with providers
- effect-ai-prompt - Provider-specific message options
- effect-ai-tool - Provider-defined tools (Anthropic bash, OpenAI web search)
- effect-ai-streaming - Provider-specific streaming behavior
- layer-design - General Effect layer composition patterns

## References

- `.context/effect/packages/ai/anthropic/src/AnthropicLanguageModel.ts`
- `.context/effect/packages/ai/openai/src/OpenAiLanguageModel.ts`
- `apps/ui/src/lib/AppLive.ts`
