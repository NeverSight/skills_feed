---
name: openai
description: OpenAI API via curl. Use this skill for GPT chat completions, DALL-E image generation, Whisper audio transcription, embeddings, and text-to-speech.
vm0_secrets:
  - OPENAI_API_KEY
---

# OpenAI API

Use the OpenAI API via direct `curl` calls to access **GPT models, DALL-E image generation, Whisper transcription, embeddings, and text-to-speech**.

> Official docs: `https://platform.openai.com/docs/api-reference`

---

## When to Use

Use this skill when you need to:

- **Chat completions** with GPT-4o, GPT-4, or GPT-3.5 models
- **Image generation** with DALL-E 3
- **Audio transcription** with Whisper
- **Text-to-speech** audio generation
- **Text embeddings** for semantic search and RAG
- **Vision tasks** (analyze images with GPT-4o)

---

## Prerequisites

1. Sign up at [OpenAI Platform](https://platform.openai.com/) and create an account
2. Go to [API Keys](https://platform.openai.com/api-keys) and generate a new secret key
3. Add billing information and set usage limits

```bash
export OPENAI_API_KEY="sk-..."
```

### Pricing (as of 2025)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| GPT-4 Turbo | $10.00 | $30.00 |
| text-embedding-3-small | $0.02 | - |
| text-embedding-3-large | $0.13 | - |

### Rate Limits

Rate limits vary by tier (based on usage history). Check your limits at [Platform Settings](https://platform.openai.com/settings/organization/limits).

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

All examples below assume you have `OPENAI_API_KEY` set.

Base URL: `https://api.openai.com/v1`

---

### 1. Basic Chat Completion

Send a simple chat message:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "gpt-4o-mini",
  "messages": [{"role": "user", "content": "Hello, who are you?"}]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.openai.com/v1/chat/completions" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json' | jq '.choices[0].message.content'
```

**Available models:**

- `gpt-4o`: Latest flagship model (128K context)
- `gpt-4o-mini`: Fast and affordable (128K context)
- `gpt-4-turbo`: Previous generation (128K context)
- `gpt-3.5-turbo`: Legacy model (16K context)
- `o1`: Reasoning model for complex tasks
- `o1-mini`: Smaller reasoning model

---

### 2. Chat with System Prompt

Use a system message to set behavior:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant that responds in JSON format."},
    {"role": "user", "content": "List 3 programming languages with their main use cases."}
  ]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.openai.com/v1/chat/completions" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json' | jq '.choices[0].message.content'
```

---

### 3. Streaming Response

Get real-time token-by-token output:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "gpt-4o-mini",
  "messages": [{"role": "user", "content": "Write a haiku about programming."}],
  "stream": true
}
```

Then run:

```bash
curl -s "https://api.openai.com/v1/chat/completions" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json
```

Streaming returns Server-Sent Events (SSE) with delta chunks.

---

### 4. JSON Mode

Force the model to return valid JSON:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": "Return JSON only."},
    {"role": "user", "content": "Give me info about Paris: name, country, population."}
  ],
  "response_format": {"type": "json_object"}
}
```

Then run:

```bash
bash -c 'curl -s "https://api.openai.com/v1/chat/completions" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json' | jq '.choices[0].message.content'
```

---

### 5. Vision (Image Analysis)

Analyze an image with GPT-4o:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What is in this image?"},
        {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"}}
      ]
    }
  ],
  "max_tokens": 300
}
```

Then run:

```bash
bash -c 'curl -s "https://api.openai.com/v1/chat/completions" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json' | jq '.choices[0].message.content'
```

---

### 6. Function Calling (Tools)

Define functions the model can call:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "gpt-4o-mini",
  "messages": [{"role": "user", "content": "What is the weather in Tokyo?"}],
  "tools": [
    {
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
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.openai.com/v1/chat/completions" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json' | jq '.choices[0].message.tool_calls'
```

---

### 7. Generate Embeddings

Create vector embeddings for text:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "text-embedding-3-small",
  "input": "The quick brown fox jumps over the lazy dog."
}
```

Then run:

```bash
bash -c 'curl -s "https://api.openai.com/v1/embeddings" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json' | jq '.data[0].embedding[:5]'
```

This extracts the first 5 dimensions of the embedding vector.

**Embedding models:**

- `text-embedding-3-small`: 1536 dimensions, fastest
- `text-embedding-3-large`: 3072 dimensions, most capable

---

### 8. Generate Image (DALL-E 3)

Create an image from text:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "dall-e-3",
  "prompt": "A white cat sitting on a windowsill, digital art",
  "n": 1,
  "size": "1024x1024"
}
```

Then run:

```bash
bash -c 'curl -s "https://api.openai.com/v1/images/generations" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json' | jq '.data[0].url'
```

**Parameters:**

- `size`: `1024x1024`, `1792x1024`, or `1024x1792`
- `quality`: `standard` or `hd`
- `style`: `vivid` or `natural`

---

### 9. Audio Transcription (Whisper)

Transcribe audio to text:

```bash
bash -c 'curl -s "https://api.openai.com/v1/audio/transcriptions" -H "Authorization: Bearer ${OPENAI_API_KEY}" -F "file=@audio.mp3" -F "model=whisper-1"' | jq '.text'
```

Supports: mp3, mp4, mpeg, mpga, m4a, wav, webm (max 25MB).

---

### 10. Text-to-Speech

Generate audio from text:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "tts-1",
  "input": "Hello! This is a test of OpenAI text to speech.",
  "voice": "alloy"
}
```

Then run:

```bash
curl -s "https://api.openai.com/v1/audio/speech" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json --output speech.mp3
```

**Voices:** `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

**Models:** `tts-1` (fast), `tts-1-hd` (high quality)

---

### 11. List Available Models

Get all available models:

```bash
bash -c 'curl -s "https://api.openai.com/v1/models" -H "Authorization: Bearer ${OPENAI_API_KEY}"' | jq -r '.data[].id' | sort | head -20
```

---

### 12. Check Token Usage

Extract usage from response:

Write to `/tmp/openai_request.json`:

```json
{
  "model": "gpt-4o-mini",
  "messages": [{"role": "user", "content": "Hi!"}]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.openai.com/v1/chat/completions" -H "Content-Type: application/json" -H "Authorization: Bearer ${OPENAI_API_KEY}" -d @/tmp/openai_request.json' | jq '.usage'
```

This returns token counts for both input and output.

Response includes:

- `prompt_tokens`: Input token count
- `completion_tokens`: Output token count
- `total_tokens`: Sum of both

---

## Guidelines

1. **Choose the right model**: Use `gpt-4o-mini` for most tasks, `gpt-4o` for complex reasoning, `o1` for advanced math/coding
2. **Set max_tokens**: Prevent runaway generation and control costs
3. **Use streaming for long responses**: Better UX for real-time applications
4. **JSON mode requires system prompt**: Include JSON instructions when using `response_format`
5. **Vision requires gpt-4o models**: Only `gpt-4o` and `gpt-4o-mini` support image input
6. **Batch similar requests**: Use embeddings API batch input for efficiency
7. **Monitor usage**: Check dashboard regularly to avoid unexpected charges
