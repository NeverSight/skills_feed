---
name: claude-api
description: Anthropic Claude API integration for building AI-powered applications. Use when working with Anthropic's Messages API, Claude SDKs (Python or TypeScript), tool use/function calling, vision/image inputs, streaming responses, prompt caching, message batches, token counting, extended thinking, PDF processing, or any Claude API integration task.
---

# Claude API

Build applications with Anthropic's Claude API using official Python and TypeScript SDKs.

**Base URL:** `https://api.anthropic.com`

## Authentication

All requests require these headers (SDKs handle automatically):

| Header | Value |
|--------|-------|
| `x-api-key` | API key from [Console](https://platform.claude.com/settings/keys) |
| `anthropic-version` | `2023-06-01` |
| `content-type` | `application/json` |

## Quick Start

### Python

```python
from anthropic import Anthropic

client = Anthropic()  # Uses ANTHROPIC_API_KEY env var

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}]
)
print(message.content[0].text)
```

### TypeScript

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();  // Uses ANTHROPIC_API_KEY env var

const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
});
console.log(message.content[0].text);
```

## Available Models

| Model | Model ID | Best For | Pricing |
|-------|----------|----------|---------|
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | Complex agents, coding (recommended) | $3/$15 per MTok |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast, lightweight tasks | $1/$5 per MTok |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | Maximum intelligence | $5/$25 per MTok |

For complete model details, platform IDs (AWS Bedrock, GCP Vertex AI), and legacy models, see [references/models.md](references/models.md).

## Available APIs

| API | Endpoint | Purpose |
|-----|----------|---------|
| Messages | `POST /v1/messages` | Conversational interactions |
| Message Batches | `POST /v1/messages/batches` | Async bulk processing (50% cost reduction) |
| Token Counting | `POST /v1/messages/count_tokens` | Count tokens before sending |
| Models | `GET /v1/models` | List available models |
| Files (beta) | `/v1/files` | Upload/manage files across calls |

For full API details, rate limits, and third-party platforms, see [references/api-overview.md](references/api-overview.md).

## Core Capabilities

### Messages API
Basic chat completions, multi-turn conversations, system prompts, streaming responses.

### Tool Use
Define tools with JSON schemas, handle tool calls, return results to Claude.

### Vision
Send images (base64 or URL), analyze multiple images, extract information.

### Streaming
Real-time token streaming with event handlers or async iterators.

### Token Counting
Count tokens before sending requests to manage costs and rate limits.

## API & SDK References

- **API Overview**: See [references/api-overview.md](references/api-overview.md) - endpoints, authentication, rate limits, third-party platforms
- **Messages API**: See [references/messages-api.md](references/messages-api.md) - request/response structure, content types
- **Vision**: See [references/vision.md](references/vision.md) - image inputs, base64/URL/Files API sources, limits
- **Streaming**: See [references/streaming.md](references/streaming.md) - SSE events, deltas, error recovery
- **Python SDK**: See [references/python-sdk.md](references/python-sdk.md)
- **TypeScript SDK**: See [references/typescript-sdk.md](references/typescript-sdk.md)

## Advanced Features

- **Extended Thinking**: See [references/extended-thinking.md](references/extended-thinking.md) - step-by-step reasoning, tool use, interleaved thinking
- **Citations**: See [references/citations.md](references/citations.md) - document citations, source verification
- **Token Counting**: See [references/token-counting.md](references/token-counting.md) - count tokens before sending, free endpoint
- **Context Windows**: See [references/context-windows.md](references/context-windows.md) - 200K/1M context, context awareness
- **Prompt Caching**: See [references/prompt-caching.md](references/prompt-caching.md) - reduce latency and costs
- **Batches, PDFs**: See [references/advanced-features.md](references/advanced-features.md)

## Common Patterns

### Conversation Loop with Tools

```python
messages = [{"role": "user", "content": user_input}]

while True:
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    if response.stop_reason == "end_turn":
        break

    if response.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })
        messages.append({"role": "user", "content": tool_results})
```

### Error Handling with Retries

```python
from anthropic import RateLimitError
import time

def call_with_retry(fn, max_retries=3):
    for attempt in range(max_retries):
        try:
            return fn()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait = int(e.response.headers.get("retry-after", 60))
            time.sleep(wait)
```

## Required Parameters

Every `messages.create()` call requires:

| Parameter | Description |
|-----------|-------------|
| `model` | Model ID (e.g., `claude-sonnet-4-5-20250929`) |
| `max_tokens` | Maximum tokens in response |
| `messages` | Array of message objects with `role` and `content` |
