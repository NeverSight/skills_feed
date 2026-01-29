---
name: together-api
description: Together AI API integration for building AI-powered applications with open-source models. Use when working with Together's Chat Completions API, Python SDK (together), TypeScript SDK (together-ai), CLI tool, tool use/function calling, vision/image understanding, image generation (FLUX, Stable Diffusion), video generation (Veo, Sora, Kling), audio transcription (Whisper), text-to-speech, streaming responses, embeddings, reranking, fine-tuning, or any Together AI API integration task. Triggers on mentions of Together AI, Together API, GroqCloud, open-source LLM inference, FLUX image generation, or Whisper transcription via Together.
---

# Together AI API

Build applications with Together AI's open-source model inference platform (200+ models).

## Quick Start

### Installation

```bash
# Python SDK + CLI
pip install --upgrade together

# TypeScript/JavaScript SDK
npm install together-ai
```

### Environment Setup

```bash
export TOGETHER_API_KEY=<your-api-key>
```

Get your API key at https://api.together.xyz/settings/api-keys

### Basic Chat Completion

**Python:**
```python
from together import Together

client = Together()  # Uses TOGETHER_API_KEY env var

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

**TypeScript:**
```typescript
import Together from "together-ai";

const client = new Together();

const response = await client.chat.completions.create({
    model: "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages: [{ role: "user", content: "Hello" }],
});
console.log(response.choices[0].message.content);
```

**CLI:**
```bash
together chat.completions \
  --message "system" "You are a helpful assistant" \
  --message "user" "Hello" \
  --model meta-llama/Llama-3.3-70B-Instruct-Turbo
```

## CLI Reference

The Together CLI provides command-line access to all API features. Streaming is enabled by default.

### Chat Completions

```bash
together chat.completions \
  --message "system" "You are a helpful assistant" \
  --message "user" "What is the capital of France?" \
  --model meta-llama/Llama-3.3-70B-Instruct-Turbo

# Disable streaming
together chat.completions \
  --message "user" "Hello" \
  --model meta-llama/Llama-3.3-70B-Instruct-Turbo \
  --no-stream
```

### Text Completions

```bash
together completions \
  "Large language models are " \
  --model meta-llama/Llama-3.3-70B-Instruct-Turbo \
  --max-tokens 512 \
  --stop "."
```

### Image Generation

```bash
together images generate \
  "A futuristic cityscape at sunset" \
  --model black-forest-labs/FLUX.1-schnell \
  --n 4

# Skip opening image viewer
together images generate "space robots" \
  --model stabilityai/stable-diffusion-xl-base-1.0 \
  --no-show
```

### Models

```bash
together models list          # List all available models
together models --help        # Show model commands
```

### Files Management

```bash
together files check example.jsonl              # Validate file format
together files upload example.jsonl             # Upload file
together files list                             # List uploaded files
together files retrieve <file-id>               # Get file metadata
together files retrieve-content <file-id>       # Get file content
together files delete <file-id>                 # Delete file
```

### Fine-Tuning

```bash
# Create fine-tuning job
together fine-tuning create \
  --model togethercomputer/llama-2-7b-chat \
  --training-file <file-id>

together fine-tuning list                       # List jobs
together fine-tuning retrieve <job-id>          # Get job details
together fine-tuning list-events <job-id>       # Get job events
together fine-tuning cancel <job-id>            # Cancel job
together fine-tuning download <job-id>          # Download model
```

See [references/cli.md](references/cli.md) for complete CLI reference.

## Model Selection

```bash
together models list
```

| Use Case | Model | Notes |
|----------|-------|-------|
| Fast + cheap | `meta-llama/Llama-3.2-3B-Instruct-Turbo` | $0.06/1M, 131K context |
| Balanced | `meta-llama/Llama-3.3-70B-Instruct-Turbo` | Quality/cost balance |
| Highest quality | `deepseek-ai/DeepSeek-V3` | 131K context |
| Reasoning | `deepseek-ai/DeepSeek-R1` | Chain-of-thought |
| Long context | `meta-llama/Llama-4-Scout-17B-16E-Instruct` | 1M context |
| Vision | `meta-llama/Llama-4-Scout-17B-16E-Instruct` | Multimodal |
| Code | `Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8` | Specialized |
| Audio STT | `openai/whisper-large-v3` | Transcription |
| TTS | `canopylabs/orpheus-3b` | Natural voices |
| Image Gen | `black-forest-labs/FLUX.1-schnell` | Fast generation |
| Video Gen | `google/veo-3.0` | Video generation |

See [references/models.md](references/models.md) for full model list and pricing.

## Common Patterns

### Streaming Responses

```python
stream = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Async Client

```python
import asyncio
from together import AsyncTogether

async def main():
    client = AsyncTogether()
    response = await client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
    return response.choices[0].message.content

print(asyncio.run(main()))
```

### JSON Mode

```python
response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "List 3 colors as JSON array"}],
    response_format={"type": "json_object"}
)
```

### Structured Outputs (JSON Schema)

```python
response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Extract: John is 30. Respond in JSON."}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                },
                "required": ["name", "age"]
            }
        }
    }
)
```

## Vision

Process images with vision-language models. **Models:** `meta-llama/Llama-4-Scout-17B-16E-Instruct` (faster), `meta-llama/Llama-4-Maverick-17B-128E-Instruct` (higher quality)

### Image from URL

```python
response = client.chat.completions.create(
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
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
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image('photo.jpg')}"}}
        ]
    }]
)
```

See [references/vision.md](references/vision.md) for multi-image, video, and OCR patterns.

## Image Generation

```python
response = client.images.generate(
    prompt="A serene mountain landscape at sunset",
    model="black-forest-labs/FLUX.1-schnell",
    steps=4,
    width=1024,
    height=1024
)
print(f"Image URL: {response.data[0].url}")
```

See [references/images.md](references/images.md) for all parameters and models.

## Audio

### Transcription (Speech-to-Text)

```python
response = client.audio.transcriptions.create(
    file="meeting.mp3",
    model="openai/whisper-large-v3",
    language="en",
    response_format="verbose_json",
    timestamp_granularities=["word", "segment"]
)
print(response.text)
```

### Text-to-Speech

```python
response = client.audio.speech.create(
    model="canopylabs/orpheus-3b",
    input="Hello, world!",
    voice="tara"
)
with open("output.wav", "wb") as f:
    f.write(response.content)
```

See [references/audio.md](references/audio.md) for streaming, WebSocket, and voice options.

## Tool Use / Function Calling

See [references/tool-use.md](references/tool-use.md) for complete patterns.

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
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Weather in Paris?"}],
    tools=tools
)

if response.choices[0].message.tool_calls:
    for tc in response.choices[0].message.tool_calls:
        args = json.loads(tc.function.arguments)
        # Execute function and continue conversation
```

## Embeddings

```python
response = client.embeddings.create(
    model="togethercomputer/m2-bert-80M-8k-retrieval",
    input="Hello, world!"
)
print(response.data[0].embedding)
```

## Reranking

```python
response = client.rerank.create(
    model="Salesforce/Llama-Rank-V1",
    query="What is the capital of France?",
    documents=["Paris is the capital.", "London is in England.", "Berlin is in Germany."],
    top_n=2
)
for result in response.results:
    print(f"Index {result.index}: {result.relevance_score}")
```

## Error Handling

```python
from together import Together
from together._exceptions import RateLimitError, APIConnectionError, APIStatusError

client = Together()

try:
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    # Wait and retry with exponential backoff
    pass
except APIConnectionError:
    # Network issue
    pass
except APIStatusError as e:
    if e.status_code == 402:
        # Insufficient credits
        pass
    elif e.status_code == 400:
        # Invalid parameters
        pass
```

## Resources

- **CLI reference**: [references/cli.md](references/cli.md)
- **Models & pricing**: [references/models.md](references/models.md)
- **Tool use guide**: [references/tool-use.md](references/tool-use.md)
- **Vision guide**: [references/vision.md](references/vision.md)
- **Audio guide**: [references/audio.md](references/audio.md)
- **Image generation**: [references/images.md](references/images.md)
- **Official docs**: https://docs.together.ai
- **Python SDK**: https://github.com/togethercomputer/together-python
- **TypeScript SDK**: https://github.com/togethercomputer/together-typescript
