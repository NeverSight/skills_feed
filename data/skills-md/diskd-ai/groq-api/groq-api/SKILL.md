---
name: groq-api
description: Groq API integration for building AI-powered applications with ultra-fast LLM inference. Use when working with Groq's Chat Completions API, Python SDK (groq), TypeScript SDK (groq-sdk), tool use/function calling, vision/image processing, audio transcription with Whisper, streaming responses, text-to-speech, content moderation with Llama Guard, batch processing, or any Groq API integration task. Triggers on mentions of Groq, GroqCloud, or fast LLM inference needs.
---

# Groq API

Build applications with Groq's ultra-fast LLM inference (300-1000+ tokens/sec).

## Quick Start

### Installation

```bash
# Python
pip install groq

# TypeScript/JavaScript
npm install groq-sdk
```

### Environment Setup

```bash
export GROQ_API_KEY=<your-api-key>
```

### Basic Chat Completion

**Python:**
```python
from groq import Groq

client = Groq()  # Uses GROQ_API_KEY env var

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

**TypeScript:**
```typescript
import Groq from "groq-sdk";

const client = new Groq();

const response = await client.chat.completions.create({
    model: "llama-3.3-70b-versatile",
    messages: [{ role: "user", content: "Hello" }],
});
console.log(response.choices[0].message.content);
```

## Model Selection

| Use Case | Model | Notes |
|----------|-------|-------|
| Fast + cheap | `llama-3.1-8b-instant` | Best for simple tasks |
| Balanced | `llama-3.3-70b-versatile` | Quality/cost balance |
| Highest quality | `openai/gpt-oss-120b` | Built-in tools + reasoning |
| Agentic | `groq/compound` | Web search + code exec |
| Reasoning | `openai/gpt-oss-20b` | Fast reasoning (low/med/high) |
| Vision/OCR | `llama-4-scout-17b-16e-instruct` | Image understanding |
| Audio STT | `whisper-large-v3-turbo` | Transcription |
| TTS | `playai-tts` | Text-to-speech |

See [references/models.md](references/models.md) for full model list and pricing.

## Common Patterns

### Streaming Responses

```python
stream = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### System Messages

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"}
    ]
)
```

### Async Client (Python)

```python
import asyncio
from groq import AsyncGroq

async def main():
    client = AsyncGroq()
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Hello"}]
    )
    return response.choices[0].message.content

print(asyncio.run(main()))
```

### JSON Mode

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "List 3 colors as JSON array"}],
    response_format={"type": "json_object"}
)
```

### Structured Outputs (JSON Schema)

Force output to match a schema. Two modes available:

| Mode | Guarantee | Models |
|------|-----------|--------|
| `strict: true` | 100% schema compliance | `openai/gpt-oss-20b`, `openai/gpt-oss-120b` |
| `strict: false` | Best-effort compliance | All supported models |

**Strict Mode (guaranteed compliance):**
```python
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Extract: John is 30 years old"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                },
                "required": ["name", "age"],
                "additionalProperties": False
            }
        }
    }
)
```

**With Pydantic:**
```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Extract: John is 30"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person",
            "strict": True,
            "schema": Person.model_json_schema()
        }
    }
)
person = Person.model_validate(json.loads(response.choices[0].message.content))
```

See [references/structured-outputs.md](references/structured-outputs.md) for schema requirements, validation libraries, and examples.

## Audio

### Transcription (Speech-to-Text)

```python
with open("audio.mp3", "rb") as f:
    transcription = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=f,
        language="en",  # Optional: ISO-639-1 code
        response_format="verbose_json",  # json, text, verbose_json
        timestamp_granularities=["word", "segment"]
    )
print(transcription.text)
```

### Translation (to English)

```python
with open("french_audio.mp3", "rb") as f:
    translation = client.audio.translations.create(
        model="whisper-large-v3",
        file=f
    )
print(translation.text)  # English text
```

### Text-to-Speech

```python
response = client.audio.speech.create(
    model="playai-tts",
    input="Hello, world!",
    voice="Fritz-PlayAI",
    response_format="wav",  # flac, mp3, mulaw, ogg, wav
    speed=1.0  # 0.5 to 5
)
response.write_to_file("output.wav")
```

## Vision

Process images with Llama 4 multimodal models. Supports up to 5 images per request.

**Models:** `meta-llama/llama-4-scout-17b-16e-instruct` (faster), `meta-llama/llama-4-maverick-17b-128e-instruct` (higher quality)

### Image from URL

```python
response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]
    }]
)
```

### Local Image (Base64)

```python
import base64

def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image('photo.jpg')}"}}
        ]
    }]
)
```

### OCR / Extract Data as JSON

```python
response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Extract all text and data as JSON"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
        ]
    }],
    response_format={"type": "json_object"}
)
```

See [references/vision.md](references/vision.md) for multi-image, tool use with images, and multi-turn conversations.

## Tool Use

For tool calling patterns and examples, see [references/tool-use.md](references/tool-use.md).

**Quick example:**
```python
import json

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    }
}]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Weather in Paris?"}],
    tools=tools
)

if response.choices[0].message.tool_calls:
    for tc in response.choices[0].message.tool_calls:
        args = json.loads(tc.function.arguments)
        # Execute function and continue conversation
```

## Built-In Tools (Agentic)

Use `groq/compound` or `openai/gpt-oss-120b` for built-in web search and code execution:

```python
response = client.chat.completions.create(
    model="groq/compound",
    messages=[{"role": "user", "content": "Search for latest Python news"}]
)
# Model automatically uses web search
```

## MCP (Remote Tools)

Connect to third-party MCP servers for tools like Stripe, GitHub, web scraping. Use the Responses API:

```python
import openai

client = openai.OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.responses.create(
    model="openai/gpt-oss-120b",
    input="What models are trending on Huggingface?",
    tools=[{
        "type": "mcp",
        "server_label": "Huggingface",
        "server_url": "https://huggingface.co/mcp"
    }]
)
```

See [references/tool-use.md](references/tool-use.md) for MCP configuration and popular servers.

## Reasoning Models

Control how models think through complex problems.

**Models:** `openai/gpt-oss-20b`, `openai/gpt-oss-120b` (low/medium/high), `qwen/qwen3-32b` (none/default)

### GPT-OSS with Reasoning Effort

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "How many r's in strawberry?"}],
    reasoning_effort="high",  # low, medium, high
    temperature=0.6,
    max_completion_tokens=1024
)

print(response.choices[0].message.content)
print("Reasoning:", response.choices[0].message.reasoning)
```

### Qwen3 with Parsed Reasoning

```python
response = client.chat.completions.create(
    model="qwen/qwen3-32b",
    messages=[{"role": "user", "content": "Solve: x + 5 = 12"}],
    reasoning_format="parsed"  # raw, parsed, hidden
)

print("Answer:", response.choices[0].message.content)
print("Reasoning:", response.choices[0].message.reasoning)
```

### Hide Reasoning (GPT-OSS)

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "What is 15% of 80?"}],
    include_reasoning=False  # Hide reasoning in response
)
```

See [references/reasoning.md](references/reasoning.md) for streaming, tool use with reasoning, and best practices.

## Batch Processing

For high-volume async processing (24h-7d completion window):

```python
# 1. Create JSONL file with requests
# 2. Upload file
# 3. Create batch
batch = client.batches.create(
    input_file_id=file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)

# 4. Check status
batch = client.batches.retrieve(batch.id)
if batch.status == "completed":
    results = client.files.content(batch.output_file_id)
```

See [references/api-reference.md](references/api-reference.md) for full batch API details.

## Prompt Caching

Automatically reduce latency and costs by 50% for repeated prompt prefixes. No code changes required.

**Supported models:** `moonshotai/kimi-k2-instruct-0905`, `openai/gpt-oss-20b`, `openai/gpt-oss-120b`, `openai/gpt-oss-safeguard-20b`

**How it works:**
- Place static content (system prompts, tools, examples) at the beginning
- Place dynamic content (user queries) at the end
- Cache automatically matches prefixes and applies 50% discount
- Cache expires after 2 hours without use

**Track cache usage:**
```python
response = client.chat.completions.create(
    model="moonshotai/kimi-k2-instruct-0905",
    messages=[{"role": "system", "content": large_system_prompt}, ...]
)

cached = response.usage.prompt_tokens_details.cached_tokens
print(f"Cached tokens: {cached}")  # 50% discount applied to these
```

See [references/prompt-caching.md](references/prompt-caching.md) for optimization strategies and examples.

## Content Moderation

Detect and filter harmful content using safeguard models.

### Llama Guard 4

General content safety classification. Returns `safe` or `unsafe\nSX` (category code).

```python
response = client.chat.completions.create(
    model="meta-llama/Llama-Guard-4-12B",
    messages=[{"role": "user", "content": user_input}]
)

if response.choices[0].message.content.startswith("unsafe"):
    # Block or handle unsafe content
    pass
```

### GPT-OSS Safeguard 20B

Prompt injection detection with custom policies. Returns structured JSON.

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-safeguard-20b",
    messages=[
        {"role": "system", "content": injection_detection_policy},
        {"role": "user", "content": user_input}
    ]
)
# Returns: {"violation": 1, "category": "Direct Override", "rationale": "..."}
```

See [references/moderation.md](references/moderation.md) for complete policies, harm taxonomy, and integration patterns.

## Error Handling

```python
from groq import Groq, RateLimitError, APIConnectionError, APIStatusError

client = Groq()

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    # Wait and retry with exponential backoff
    pass
except APIConnectionError:
    # Network issue
    pass
except APIStatusError as e:
    # API error (check e.status_code)
    pass
```

See [references/audio.md](references/audio.md) for complete audio API reference including file handling, metadata fields, and prompting guidelines.

## Resources

- **Models & pricing**: [references/models.md](references/models.md)
- **Tool use guide**: [references/tool-use.md](references/tool-use.md)
- **Vision guide**: [references/vision.md](references/vision.md)
- **Audio guide**: [references/audio.md](references/audio.md)
- **Reasoning guide**: [references/reasoning.md](references/reasoning.md)
- **Structured outputs**: [references/structured-outputs.md](references/structured-outputs.md)
- **Prompt caching**: [references/prompt-caching.md](references/prompt-caching.md)
- **Moderation guide**: [references/moderation.md](references/moderation.md)
- **SDK reference**: [references/sdk.md](references/sdk.md)
- **Full API reference**: [references/api-reference.md](references/api-reference.md)
- **Official docs**: https://console.groq.com/docs
- **Python SDK**: https://github.com/groq/groq-python
- **TypeScript SDK**: https://github.com/groq/groq-typescript
