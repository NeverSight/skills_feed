---
name: openai-api
description: OpenAI API integration for building AI-powered applications. Use when working with OpenAI's Chat Completions API, Python SDK (openai), TypeScript SDK (openai), tool use/function calling, vision/image inputs, streaming responses, DALL-E image generation, Whisper audio transcription, text-to-speech, embeddings, Assistants API, fine-tuning, or any OpenAI API integration task. Triggers on mentions of OpenAI, GPT-4, GPT-4o, GPT-5, o1, o3, o4, DALL-E, Whisper, Sora, or OpenAI SDK usage.
---

# OpenAI API

Build AI applications using OpenAI's APIs with Python or TypeScript SDKs.

## Quick Start

### Installation

```bash
# Python
pip install openai

# TypeScript/Node.js
npm install openai
```

### Client Setup

**Python:**
```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var
# Or: client = OpenAI(api_key="sk-...")
```

**TypeScript:**
```typescript
import OpenAI from 'openai';

const client = new OpenAI();  // Uses OPENAI_API_KEY env var
// Or: new OpenAI({ apiKey: 'sk-...' })
```

## Chat Completions

Basic chat completion:

**Python:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(response.choices[0].message.content)
```

**TypeScript:**
```typescript
const response = await client.chat.completions.create({
    model: 'gpt-4o',
    messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: 'Hello!' }
    ]
});
console.log(response.choices[0].message.content);
```

### Streaming

**Python:**
```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

**TypeScript:**
```typescript
const stream = await client.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'Tell me a story' }],
    stream: true
});
for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

### Tool Use / Function Calling

**Python:**
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools
)

# Check if tool call requested
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    # Execute function, then send result back
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": '{"temp": 22, "condition": "sunny"}'
    })
```

**TypeScript:**
```typescript
const tools: OpenAI.ChatCompletionTool[] = [{
    type: 'function',
    function: {
        name: 'get_weather',
        description: 'Get current weather for a location',
        parameters: {
            type: 'object',
            properties: {
                location: { type: 'string', description: 'City name' }
            },
            required: ['location']
        }
    }
}];

const response = await client.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: "What's the weather in Paris?" }],
    tools
});

if (response.choices[0].message.tool_calls) {
    const toolCall = response.choices[0].message.tool_calls[0];
    // Execute function, then continue conversation
}
```

### Vision (Image Input)

**Python:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]
    }]
)
```

For base64 images: `"url": "data:image/jpeg;base64,{base64_string}"`

### Structured Outputs (JSON Mode)

**Python:**
```python
from pydantic import BaseModel

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Create a meeting for tomorrow"}],
    response_format=CalendarEvent
)
event = response.choices[0].message.parsed
```

**TypeScript (with Zod):**
```typescript
import { zodResponseFormat } from 'openai/helpers/zod';
import { z } from 'zod';

const CalendarEvent = z.object({
    name: z.string(),
    date: z.string(),
    participants: z.array(z.string())
});

const response = await client.beta.chat.completions.parse({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'Create a meeting for tomorrow' }],
    response_format: zodResponseFormat(CalendarEvent, 'event')
});
const event = response.choices[0].message.parsed;
```

## Models

### Chat/Completion Models

| Model | Best For |
|-------|----------|
| `gpt-5.2` | Latest flagship, best quality |
| `gpt-5.2-pro` | Premium tier for complex tasks |
| `gpt-5` | Previous flagship, excellent quality |
| `gpt-5-mini` | Cost-effective GPT-5 |
| `gpt-5-nano` | Lightweight GPT-5 |
| `gpt-4.1` | Strong general purpose |
| `gpt-4.1-mini` | Cost-effective GPT-4.1 |
| `gpt-4.1-nano` | Lightweight GPT-4.1 |
| `gpt-4o` | Fast, vision support |
| `gpt-4o-mini` | Cost-effective, simpler tasks |

### Reasoning Models

| Model | Best For |
|-------|----------|
| `o4-mini` | Latest reasoning, efficient |
| `o3` | Strong reasoning |
| `o3-mini` | Reasoning with lower cost |
| `o1` | Complex reasoning, math, code |
| `o1-pro` | Premium reasoning tier |

### Specialized Models

| Model | Purpose |
|-------|---------|
| `gpt-4o-realtime-preview` | Real-time voice conversations |
| `gpt-4o-audio-preview` | Audio input/output |
| `gpt-4o-search-preview` | Web search integration |
| `gpt-image-1` / `gpt-image-1.5` | Image understanding |
| `sora-2` / `sora-2-pro` | Video generation |
| `dall-e-3` | Image generation |
| `whisper-1` | Audio transcription |
| `tts-1` / `tts-1-hd` | Text-to-speech |
| `text-embedding-3-small/large` | Text embeddings |

## Feature References

- **Advanced chat patterns**: See [references/chat-completions.md](references/chat-completions.md)
- **Image generation (DALL-E)**: See [references/images.md](references/images.md)
- **Audio (Whisper/TTS)**: See [references/audio.md](references/audio.md)
- **Embeddings**: See [references/embeddings.md](references/embeddings.md)
- **Assistants API**: See [references/assistants.md](references/assistants.md)
- **Fine-tuning**: See [references/fine-tuning.md](references/fine-tuning.md)

## Error Handling

**Python:**
```python
from openai import APIError, RateLimitError, APIConnectionError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    # Implement backoff/retry
    pass
except APIConnectionError:
    # Network issue
    pass
except APIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

**TypeScript:**
```typescript
import OpenAI from 'openai';

try {
    const response = await client.chat.completions.create({...});
} catch (error) {
    if (error instanceof OpenAI.RateLimitError) {
        // Implement backoff/retry
    } else if (error instanceof OpenAI.APIConnectionError) {
        // Network issue
    } else if (error instanceof OpenAI.APIError) {
        console.error(`API error: ${error.status} - ${error.message}`);
    }
}
```

## Common Parameters

| Parameter | Description |
|-----------|-------------|
| `temperature` | 0-2, lower = deterministic, higher = creative |
| `max_tokens` | Maximum response length |
| `top_p` | Nucleus sampling alternative to temperature |
| `stop` | Stop sequences to end generation |
| `n` | Number of completions to generate |
