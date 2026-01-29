---
name: cerebras-api
description: Cerebras API integration for building AI-powered applications with ultra-fast LLM inference. Use when working with Cerebras's Chat Completions API, Python SDK (cerebras_cloud_sdk), TypeScript SDK (@cerebras/cerebras_cloud_sdk), tool use/function calling, structured outputs with JSON schemas, reasoning models with thinking tokens, streaming responses, or any Cerebras API integration task. Triggers on mentions of Cerebras, Cerebras Inference, Llama on Cerebras, Qwen on Cerebras, GLM, or fast LLM inference needs.
---

# Cerebras API

Cerebras provides the world's fastest AI inference (2,000+ tokens/s). OpenAI-compatible API with Python and TypeScript SDKs.

## Quick Reference

| Resource | Location |
|----------|----------|
| API Base URL | `https://api.cerebras.ai/v1` |
| Get API Key | https://cloud.cerebras.ai |
| Python SDK | `pip install cerebras_cloud_sdk` |
| TypeScript SDK | `npm install @cerebras/cerebras_cloud_sdk` |

## Available Models

> **Deprecation Notice:** `qwen-3-32b` and `llama-3.3-70b` are scheduled for deprecation on February 16, 2026.

### Production Models

Fully supported for production use.

| Model | Model ID | Parameters | Speed |
|-------|----------|------------|-------|
| [Llama 3.1 8B](https://inference-docs.cerebras.ai/models/llama-31-8b) | `llama3.1-8b` | 8B | ~2200 tok/s |
| [Llama 3.3 70B](https://inference-docs.cerebras.ai/models/llama-33-70b) | `llama-3.3-70b` | 70B | ~2100 tok/s |
| [OpenAI GPT OSS](https://inference-docs.cerebras.ai/models/openai-oss) | `gpt-oss-120b` | 120B | ~3000 tok/s |
| [Qwen 3 32B](https://inference-docs.cerebras.ai/models/qwen-3-32b) | `qwen-3-32b` | 32B | ~2600 tok/s |

### Preview Models

For evaluation only - may be discontinued with short notice.

| Model | Model ID | Parameters | Speed |
|-------|----------|------------|-------|
| [Qwen 3 235B Instruct](https://inference-docs.cerebras.ai/models/qwen-3-235b-2507) | `qwen-3-235b-a22b-instruct-2507` | 235B | ~1400 tok/s |
| [Z.ai GLM 4.7](https://inference-docs.cerebras.ai/models/zai-glm-47) | `zai-glm-4.7` | 355B | ~1000 tok/s |

Migrating to GLM? See [GLM 4.7 Migration Guide](https://inference-docs.cerebras.ai/resources/glm-47-migration).

### Model Selection Guide

| Use Case | Recommended Model |
|----------|-------------------|
| Speed-critical (real-time chat) | `llama3.1-8b` |
| Balanced (chat, coding, math) | `llama-3.3-70b` |
| Hybrid reasoning | `qwen-3-32b` |
| Multilingual, instruction following | `qwen-3-235b-a22b-instruct-2507` |
| Science, math, complex reasoning | `gpt-oss-120b` |
| Agents, superior tool use | `zai-glm-4.7` |

### Model Compression

All models are unpruned original versions. Precision varies:

| Model | Precision | Weights |
|-------|-----------|---------|
| `llama3.1-8b` | FP16 | [HuggingFace](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) |
| `llama-3.3-70b` | FP16 | [HuggingFace](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) |
| `gpt-oss-120b` | FP16/FP8 (weights only) | [HuggingFace](https://huggingface.co/openai/gpt-oss-120b) |
| `qwen-3-32b` | FP16 | [HuggingFace](https://huggingface.co/Qwen/Qwen3-32B) |
| `qwen-3-235b-a22b-instruct-2507` | FP16/FP8 (weights only) | [HuggingFace](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507) |
| `zai-glm-4.7` | FP16/FP8 (weights only) | [HuggingFace](https://huggingface.co/zai-org/GLM-4.7) |

Note: FP16/FP8 models use selective weight-only quantization for storage. Sensitive layers remain at full precision, with dequantization on-the-fly. Activations and KV cache remain unquantized.

## Basic Usage

### Python

```python
import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Explain quantum computing"}]
)
print(response.choices[0].message.content)
```

### TypeScript

```typescript
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras({ apiKey: process.env.CEREBRAS_API_KEY });

const response = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [{ role: 'user', content: 'Explain quantum computing' }]
});
console.log(response.choices[0].message.content);
```

## Streaming

The Cerebras API supports streaming responses, allowing messages to be sent back in chunks and displayed incrementally as they are generated. Set `stream=True` to receive an iterable of chunks.

### Python

```python
stream = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Why is fast inference important?"}],
    stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

### TypeScript

```typescript
const stream = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [{ role: 'user', content: 'Why is fast inference important?' }],
    stream: true
});

for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

### Streaming Notes

- Each chunk contains a `delta` object with incremental content
- `usage` and `time_info` are only available in the final chunk
- Use `flush=True` in Python print for real-time display: `print(..., end="", flush=True)`

### Cancel Streaming (TypeScript)

```typescript
const stream = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [{ role: 'user', content: 'Long response' }],
    stream: true
});

for await (const chunk of stream) {
    if (shouldStop) {
        stream.controller.abort();
        break;
    }
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

### Async Streaming (Python)

```python
from cerebras.cloud.sdk import AsyncCerebras

client = AsyncCerebras()

async def stream_response():
    stream = await client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": "Tell me a joke"}],
        stream=True
    )

    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
```

## Tool Calling

Tool calling (also known as function calling) enables models to interact with external tools, APIs, or applications to perform actions and access real-time information.

**Supported models:** `gpt-oss-120b`, `qwen-3-32b`, `zai-glm-4.7`

### How It Works

1. **Define tools** - Provide name, description, and parameters for each tool
2. **Send request** - Include tool definitions with your API call
3. **Model decides** - Model analyzes if a tool can help answer the question
4. **Execute & respond** - Your code executes the tool and returns results to the model

### Define Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "strict": True,
            "description": "Get temperature for a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and country e.g. Toronto, Canada"
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    }
]
```

### Make API Call

```python
response = client.chat.completions.create(
    model="zai-glm-4.7",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools
)
```

### Handle Tool Calls

```python
import json

choice = response.choices[0].message

if choice.tool_calls:
    # Add assistant message with tool_calls
    messages.append(choice)

    for tool_call in choice.tool_calls:
        # Execute your tool
        arguments = json.loads(tool_call.function.arguments)
        result = get_weather(arguments["location"])

        # Append tool result
        messages.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })

    # Get final response
    final_response = client.chat.completions.create(
        model="zai-glm-4.7",
        messages=messages
    )
    print(final_response.choices[0].message.content)
```

### Parallel Tool Calling

When a query requires multiple independent data points (e.g., comparing weather in different cities), the model can request multiple tools at once.

```python
response = client.chat.completions.create(
    model="zai-glm-4.7",
    messages=[{"role": "user", "content": "Is Toronto warmer than Montreal?"}],
    tools=tools,
    parallel_tool_calls=True  # Default: enabled
)

# Response may contain multiple tool_calls
for tool_call in response.choices[0].message.tool_calls:
    print(f"Tool: {tool_call.function.name}, Args: {tool_call.function.arguments}")
```

To disable parallel calling:

```python
response = client.chat.completions.create(
    model="zai-glm-4.7",
    messages=messages,
    tools=tools,
    parallel_tool_calls=False  # Force sequential execution
)
```

### TypeScript Example

```typescript
const tools: Cerebras.Chat.ChatCompletionTool[] = [{
    type: 'function',
    function: {
        name: 'get_weather',
        strict: true,
        description: 'Get temperature for a given location.',
        parameters: {
            type: 'object',
            properties: {
                location: { type: 'string', description: 'City name' }
            },
            required: ['location'],
            additionalProperties: false
        }
    }
}];

const response = await client.chat.completions.create({
    model: 'zai-glm-4.7',
    messages: [{ role: 'user', content: 'Weather in Paris?' }],
    tools
});

if (response.choices[0].message.tool_calls) {
    for (const toolCall of response.choices[0].message.tool_calls) {
        const args = JSON.parse(toolCall.function.arguments);
        // Execute tool and continue conversation
    }
}
```

### Best Practices

- Use `strict: true` for reliable JSON argument parsing
- Always set `additionalProperties: false` in parameter schemas
- Provide clear, descriptive tool descriptions
- Handle cases where model doesn't call any tools

## Structured Outputs

Generate structured data with enforced JSON schema compliance. Key benefits:

- **Reduced Variability** - Consistent outputs adhering to predefined fields
- **Type Safety** - Enforces correct data types, preventing mismatches
- **Easier Parsing** - Direct use in applications without extra processing

### Defining the Schema

Define a JSON schema specifying fields, types, and required properties.

> For every `required` array, you must set `additionalProperties: false`.

### Python (with Pydantic)

```python
from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    director: str
    year: int

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Suggest a sci-fi movie"}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "movie",
            "strict": True,
            "schema": Movie.model_json_schema()
        }
    }
)

import json
movie = json.loads(response.choices[0].message.content)
```

### Python (with raw schema)

```python
movie_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "director": {"type": "string"},
        "year": {"type": "integer"}
    },
    "required": ["title", "director", "year"],
    "additionalProperties": False
}

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Suggest a sci-fi movie"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "movie",
            "strict": True,
            "schema": movie_schema
        }
    }
)
```

### TypeScript (with Zod)

```typescript
import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

const MovieSchema = z.object({
    title: z.string(),
    director: z.string(),
    year: z.number().int()
});

const response = await client.chat.completions.create({
    model: 'llama-3.3-70b',
    messages: [{ role: 'user', content: 'Suggest a sci-fi movie' }],
    response_format: {
        type: 'json_schema',
        json_schema: {
            name: 'movie',
            strict: true,
            schema: zodToJsonSchema(MovieSchema)
        }
    }
});

const movie = MovieSchema.parse(JSON.parse(response.choices[0].message.content || '{}'));
```

### Response Format Modes

| Mode | Valid JSON | Adheres to Schema | Extra Fields | Constrained Decoding |
|------|------------|-------------------|--------------|----------------------|
| `json_schema` (strict: true) | Yes | Yes (guaranteed) | No | Yes |
| `json_schema` (strict: false) | Yes (best-effort) | Yes | Yes | No |
| `json_object` | Yes | No (flexible) | No | No |

**Enabling each mode:**
- **Strict**: `response_format: { type: "json_schema", json_schema: { strict: true, schema: ... } }`
- **Non-strict**: `response_format: { type: "json_schema", json_schema: { strict: false, schema: ... } }`
- **JSON object**: `response_format: { type: "json_object" }`

### Schema Requirements

- Set `"additionalProperties": false` for all objects with required fields
- Max nesting: 5 levels
- Max schema length: 5,000 chars
- No recursive schemas

> `tools` and `response_format` cannot be used in the same request.

## Reasoning Models

Reasoning models generate intermediate thinking tokens before their final response, enabling better problem-solving and allowing inspection of the model's thought process.

**Supported models:** `qwen-3-32b`, `gpt-oss-120b`, `zai-glm-4.7`

### Reasoning Format Options

| Format | Behavior | Use Case |
|--------|----------|----------|
| `parsed` | Reasoning in separate `reasoning` field, logprobs split into `reasoning_logprobs` | When you need structured access to thinking |
| `raw` | Reasoning prepended to content with wrapper tokens (`<think>...</think>` for GLM/Qwen) | When you want full visibility |
| `hidden` | Reasoning text dropped from response (tokens still counted/billed) | When you want benefits without exposing thinking |
| `none` | Uses model's default behavior | Default |

**Default behaviors by model:**
- Qwen3: `raw` (or `hidden` for JSON output)
- GLM: `text_parsed`
- GPT-OSS: `text_parsed`

### Basic Usage

```python
response = client.chat.completions.create(
    model="qwen-3-32b",
    messages=[{"role": "user", "content": "Solve: 15% of 240"}],
    reasoning_format="parsed"
)
print("Thinking:", response.choices[0].message.reasoning)
print("Answer:", response.choices[0].message.content)
```

```typescript
const response = await client.chat.completions.create({
    model: 'qwen-3-32b',
    messages: [{ role: 'user', content: 'Solve: 15% of 240' }],
    reasoning_format: 'parsed'
});
console.log('Thinking:', response.choices[0].message.reasoning);
console.log('Answer:', response.choices[0].message.content);
```

### GPT-OSS: Reasoning Effort

Control reasoning intensity with `reasoning_effort`:

```python
response = client.chat.completions.create(
    model="gpt-oss-120b",
    messages=[{"role": "user", "content": "Prove the Pythagorean theorem"}],
    reasoning_effort="high"  # "low", "medium" (default), "high"
)
```

### GLM: Disable Reasoning

Toggle reasoning on/off for GLM:

```python
response = client.chat.completions.create(
    model="zai-glm-4.7",
    messages=[{"role": "user", "content": "Quick factual question"}],
    disable_reasoning=True  # Skip thinking for simple queries
)
```

### Multi-Turn Reasoning Context

To retain reasoning awareness across conversation turns, include prior reasoning in assistant messages using the model's native format.

**GPT-OSS** (reasoning prepended directly):
```python
messages = [
    {"role": "user", "content": "What is 25 * 4?"},
    {"role": "assistant", "content": "Multiply 25 times 4 equals 100. The answer is 100."},
    {"role": "user", "content": "Now divide that by 2."}
]
response = client.chat.completions.create(model="gpt-oss-120b", messages=messages)
```

**GLM/Qwen** (reasoning in `<think>` tags):
```python
messages = [
    {"role": "user", "content": "What is 25 * 4?"},
    {"role": "assistant", "content": "<think>Multiply 25 times 4 equals 100.</think>The answer is 100."},
    {"role": "user", "content": "Now divide that by 2."}
]
response = client.chat.completions.create(model="zai-glm-4.7", messages=messages)
```

## Predicted Outputs

> Reduce latency by specifying parts of the response that are already known. (Public Preview)

**Supported models:** `gpt-oss-120b`, `llama3.1-8b`, `zai-glm-4.7`

Predicted Outputs speed up response generation when parts of the output are already known. This is most useful when regenerating text or code that requires only minor changes.

### Python

```python
code = """
html {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    color: #00FF00;
}
"""

response = client.chat.completions.create(
    model="gpt-oss-120b",
    messages=[
        {"role": "user", "content": "Change the color to blue. Respond only with code."},
        {"role": "user", "content": code}
    ],
    prediction={"type": "content", "content": code}
)
```

### TypeScript

```typescript
const code = `
html {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    color: #00FF00;
}
`;

const response = await client.chat.completions.create({
    model: 'gpt-oss-120b',
    messages: [
        { role: 'user', content: "Change the color to blue. Respond only with code." },
        { role: 'user', content: code }
    ],
    prediction: { type: 'content', content: code }
});
```

### Token-Reuse Metrics

The response includes usage metrics showing prediction efficiency:

```json
{
  "usage": {
    "completion_tokens": 224,
    "prompt_tokens": 204,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 76,
      "rejected_prediction_tokens": 20
    }
  }
}
```

A high ratio of accepted to rejected tokens indicates efficient prediction reuse.

### Best Practices

- **Use when most output is known** - The larger the known section, the greater the efficiency gain
- **Set `temperature=0`** - Reduces randomness and increases token acceptance
- **Keep predictions accurate** - Misaligned predictions increase rejected tokens
- **Monitor metrics** - Track accepted vs rejected tokens to evaluate effectiveness

### Limitations

- Rejected tokens are billed at completion-token rates
- Not compatible with: `logprobs`, `n > 1`, `tools`
- Reasoning tokens may generate additional `rejected_prediction_tokens`

## Prompt Caching

Store and reuse previously processed prompts to reduce latency. Designed to significantly reduce Time to First Token (TTFT) for long-context workloads like multi-turn conversations, RAG, and agentic workflows.

### How It Works

**Automatic** - No code changes required. Works on all supported API requests.

1. **Prefix Matching** - System analyzes the beginning of your prompt (system prompts, tool definitions, few-shot examples)
2. **Block-Based Caching** - Prompts processed in blocks (100-600 tokens). Matching blocks reuse cached computation
3. **Cache Hit** - Cached blocks skip processing, resulting in lower latency
4. **Cache Miss** - Prompt processed normally, prefix stored for future matches
5. **Auto Expiration** - TTL guaranteed 5 minutes, may persist up to 1 hour

> The entire beginning of your prompt must match *exactly* with a cached prefix. Even a single character difference causes a cache miss.

### Checking Cache Usage

Check the `usage.prompt_tokens_details.cached_tokens` field in your response:

```python
response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=messages
)

cached = response.usage.prompt_tokens_details.cached_tokens
print(f"Cached tokens: {cached}")
```

```json
{
  "usage": {
    "prompt_tokens": 1500,
    "prompt_tokens_details": {
      "cached_tokens": 1200
    }
  }
}
```

### Best Practices for Cache Hits

- **Keep prefixes consistent** - System prompts, tool definitions, and few-shot examples should be identical across requests
- **Order matters** - Place stable content (system prompt, tools) before dynamic content (user messages)
- **Multi-turn conversations** - Cache naturally builds as conversation history grows
- **RAG workflows** - Place frequently-used context at the beginning

### Example: Multi-Turn with Tools

```python
# System message and tools are cached across turns
messages = [
    {"role": "system", "content": "You are a shopping assistant."},
    {"role": "user", "content": "Where is my order ORD-123456?"}
]

# Turn 1 - creates cache for system + tools
response = client.chat.completions.create(
    model="qwen-3-32b",
    messages=messages,
    tools=tools
)
print(f"Turn 1 cached: {response.usage.prompt_tokens_details.cached_tokens}")

# Turn 2 - reuses cached system + tools
messages.append(response.choices[0].message)
messages.append({"role": "user", "content": "Please cancel it."})

response = client.chat.completions.create(
    model="qwen-3-32b",
    messages=messages,
    tools=tools
)
print(f"Turn 2 cached: {response.usage.prompt_tokens_details.cached_tokens}")
```

### FAQ

- **Pricing**: No additional cost. Standard token rates apply
- **Quality**: Caching only affects input processing. Output generation unchanged
- **Manual clear**: Not available. System manages cache automatically
- **TTL**: Guaranteed 5 minutes, up to 1 hour depending on load

## Async Usage (Python)

```python
import asyncio
from cerebras.cloud.sdk import AsyncCerebras

client = AsyncCerebras()

async def main():
    response = await client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

## Error Handling

All errors inherit from `cerebras.cloud.sdk.APIError`. Main categories:
- `APIConnectionError` - Unable to connect to the API
- `APIStatusError` - API returns non-success status code (4xx or 5xx)

### Error Codes

| Status | Exception | Description |
|--------|-----------|-------------|
| 400 | `BadRequestError` | Invalid request parameters |
| 401 | `AuthenticationError` | Invalid or missing API key |
| 402 | `PaymentRequired` | Payment required |
| 403 | `PermissionDeniedError` | Insufficient permissions |
| 404 | `NotFoundError` | Resource not found |
| 422 | `UnprocessableEntityError` | Validation error |
| 429 | `RateLimitError` | Too many requests |
| 500 | `InternalServerError` | Server error |
| 503 | `ServiceUnavailable` | Service temporarily unavailable |
| N/A | `APIConnectionError` | Network/connection issue |

### Python Example

```python
import cerebras.cloud.sdk
from cerebras.cloud.sdk import Cerebras

client = Cerebras()

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": "Hello"}]
    )
except cerebras.cloud.sdk.APIConnectionError as e:
    print("Server could not be reached")
    print(e.__cause__)
except cerebras.cloud.sdk.RateLimitError as e:
    print("Rate limited - implement backoff")
except cerebras.cloud.sdk.APIStatusError as e:
    print(f"Error {e.status_code}: {e.response}")
```

### TypeScript Example

```typescript
try {
    const response = await client.chat.completions.create({
        model: 'llama-3.3-70b',
        messages: [{ role: 'user', content: 'Hello' }]
    });
} catch (err) {
    if (err instanceof Cerebras.APIError) {
        console.log(err.status);   // 400
        console.log(err.name);     // BadRequestError
        console.log(err.headers);  // Response headers
    } else {
        throw err;
    }
}
```

## Retries & Timeouts

### Automatic Retries

By default, these errors are retried 2 times with exponential backoff:
- Connection errors
- 408 Request Timeout
- 429 Rate Limit
- >= 500 Internal errors

```python
# Python - configure retries
client = Cerebras(max_retries=0)  # Disable retries

# Per-request override
client.with_options(max_retries=5).chat.completions.create(...)
```

```typescript
// TypeScript - configure retries
const client = new Cerebras({ maxRetries: 0 });

// Per-request override
await client.chat.completions.create(params, { maxRetries: 5 });
```

### Timeouts

Default timeout is 60 seconds. On timeout, `APITimeoutError` is thrown.

```python
# Python - configure timeout
client = Cerebras(timeout=20.0)  # 20 seconds

# Granular control
import httpx
client = Cerebras(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0)
)

# Per-request override
client.with_options(timeout=5.0).chat.completions.create(...)
```

```typescript
// TypeScript - configure timeout
const client = new Cerebras({ timeout: 20 * 1000 });

// Per-request override
await client.chat.completions.create(params, { timeout: 5 * 1000 });
```

### TCP Warming

SDK sends warmup requests on init to reduce first-token latency. Disable if needed:

```python
client = Cerebras(warm_tcp_connection=False)
```

```typescript
const client = new Cerebras({ warmTCPConnection: false });
```

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `model` | Model identifier (required) |
| `messages` | Conversation history (required) |
| `temperature` | Randomness 0-1.5 (default varies) |
| `max_completion_tokens` | Max output tokens |
| `stop` | Up to 4 stop sequences |
| `stream` | Enable streaming |
| `response_format` | `text`, `json_object`, or `json_schema` |
| `tools` | Function definitions for tool calling |
| `reasoning_format` | `parsed`, `raw`, `hidden` |
| `reasoning_effort` | `low`, `medium`, `high` (gpt-oss only) |

## References

For detailed SDK documentation:
- Python: See [references/python.md](references/python.md)
- TypeScript: See [references/typescript.md](references/typescript.md)
