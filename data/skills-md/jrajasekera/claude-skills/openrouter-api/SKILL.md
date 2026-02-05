---
name: openrouter-api
description: OpenRouter API integration for unified access to 400+ LLM models from 70+ providers. Use when building applications that need to call OpenRouter's API for chat completions, streaming, tool calling, structured outputs, or model routing. Triggers on OpenRouter, model routing, multi-model, provider fallbacks, or when users need to access multiple LLM providers through a single API.
---

# OpenRouter API

OpenRouter provides a unified API to access 400+ models from 70+ providers (OpenAI, Anthropic, Google, Meta, Mistral, etc.) through a single OpenAI-compatible interface.

## Quick Start

```typescript
// Using fetch
const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "openai/gpt-5.2",
    messages: [{ role: "user", content: "Hello!" }]
  })
});

// Using OpenAI SDK (Python)
from openai import OpenAI
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
response = client.chat.completions.create(
    model="openai/gpt-5.2",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Core Concepts

### Model Format

Models use `provider/model-name` format: `openai/gpt-5.2`, `anthropic/claude-sonnet-4.5`, `google/gemini-3-pro`

### Model Variants

Append suffixes to modify behavior:
- `:thinking` - Extended reasoning
- `:free` - Free tier (rate limited)
- `:nitro` - Speed-optimized
- `:extended` - Larger context
- `:online` - Web search enabled
- `:exacto` - Tool-calling optimized

Example: `openai/gpt-5.2:online`, `deepseek/deepseek-r1:thinking`

### Provider Routing

Control which providers serve your requests:

```typescript
{
  model: "anthropic/claude-sonnet-4.5",
  provider: {
    order: ["Anthropic", "Amazon Bedrock"],  // Preference order
    allow_fallbacks: true,                    // Enable backup providers
    sort: "price",                            // "price" | "throughput" | "latency"
    data_collection: "deny",                  // Privacy control
    zdr: true                                 // Zero Data Retention
  }
}
```

### Model Fallbacks

Specify backup models:

```typescript
{
  models: ["anthropic/claude-sonnet-4.5", "openai/gpt-5.2", "google/gemini-3-pro"]
}
```

## Common Patterns

### Streaming

```typescript
const response = await fetch(url, {
  body: JSON.stringify({ ...params, stream: true })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value);
  // Parse SSE: "data: {...}\n"
  const data = JSON.parse(chunk.slice(6));
  console.log(data.choices[0]?.delta?.content);
}
```

### Tool Calling

```typescript
const response = await fetch(url, {
  body: JSON.stringify({
    model: "openai/gpt-5.2",
    messages: [{ role: "user", content: "What's the weather in NYC?" }],
    tools: [{
      type: "function",
      function: {
        name: "get_weather",
        description: "Get weather for a location",
        parameters: {
          type: "object",
          properties: { location: { type: "string" } },
          required: ["location"]
        }
      }
    }]
  })
});

// Handle tool_calls in response, execute locally, return results
```

### Structured Output

```typescript
{
  response_format: {
    type: "json_schema",
    json_schema: {
      name: "response",
      strict: true,
      schema: {
        type: "object",
        properties: {
          answer: { type: "string" },
          confidence: { type: "number" }
        },
        required: ["answer", "confidence"],
        additionalProperties: false
      }
    }
  }
}
```

### Web Search

```typescript
// Using plugin
{ plugins: [{ id: "web", max_results: 5 }] }

// Or model suffix
{ model: "openai/gpt-5.2:online" }
```

### Reasoning (Thinking Models)

```typescript
{
  model: "deepseek/deepseek-r1:thinking",
  reasoning: {
    effort: "high",       // xhigh, high, medium, low, minimal, none
    summary: "concise"    // auto, concise, detailed
  }
}
```

## Reference Documentation

For detailed API documentation, read the appropriate reference file:

- **[chat-completions.md](references/chat-completions.md)** - Core chat API, request/response formats, code examples
- **[routing-providers.md](references/routing-providers.md)** - Provider routing, model variants, fallbacks, Auto Router
- **[tool-calling.md](references/tool-calling.md)** - Function calling, tool definitions, agentic loops
- **[streaming.md](references/streaming.md)** - SSE streaming, cancellation, error handling
- **[plugins-features.md](references/plugins-features.md)** - Plugins, structured outputs, multimodal, caching, reasoning
- **[responses-api.md](references/responses-api.md)** - Beta stateless Responses API
- **[api-endpoints.md](references/api-endpoints.md)** - All API endpoints reference

## Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (e.g., `openai/gpt-5.2`) |
| `messages` | Message[] | Conversation history |
| `stream` | boolean | Enable streaming |
| `max_tokens` | number | Max completion tokens |
| `temperature` | number | Randomness [0-2] |
| `tools` | Tool[] | Function definitions |
| `response_format` | object | Output format control |
| `provider` | object | Routing preferences |
| `plugins` | Plugin[] | Enable plugins |

## Error Handling

```typescript
// Check response status
if (!response.ok) {
  const error = await response.json();
  // error.error.code: 400, 401, 402, 403, 429, 502, 503
  // error.error.message: Human-readable error
}
```

Key status codes:
- `401` - Invalid API key
- `402` - Insufficient credits
- `429` - Rate limited
- `502` - Provider error
- `503` - No available provider
