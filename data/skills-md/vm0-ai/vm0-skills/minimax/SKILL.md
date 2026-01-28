---
name: minimax
description: MiniMax API via curl. Use this skill for Chinese LLM chat, text-to-speech, and AI video generation.
vm0_secrets:
  - MINIMAX_API_KEY
---

# MiniMax API

Use the MiniMax API via direct `curl` calls for **AI chat completion**, **text-to-speech**, and **video generation**.

> Official docs: `https://platform.minimax.io/docs`

---

## When to Use

Use this skill when you need to:

- **Chat completion** with Chinese-optimized LLM (MiniMax-M1/M2)
- **Text-to-speech** with natural voices and emotion control
- **Video generation** from text prompts (T2V)
- **Image-to-video** conversion (I2V)

---

## Prerequisites

1. Sign up at [MiniMax Platform](https://platform.minimax.io/)
2. Go to Account Management > API Keys to create an API key
3. Note: Global users should use `api.minimaxi.chat` (with extra "i")

```bash
export MINIMAX_API_KEY="your-api-key"
```

### API Hosts

| Region | Base URL |
|--------|----------|
| China | `https://api.minimax.io` |
| Global | `https://api.minimaxi.chat` |

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume you have `MINIMAX_API_KEY` set.

Authentication uses Bearer token in the `Authorization` header.

---

### 1. Basic Chat Completion

Send a chat message:

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "MiniMax-Text-01",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, who are you?"}
  ]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.minimax.io/v1/text/chatcompletion_v2" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json' | jq '.choices[0].message.content'
```

**Available models:**

- `MiniMax-M2`: Reasoning model (best quality)
- `MiniMax-M1`: Reasoning model (balanced)
- `MiniMax-Text-01`: Standard model (fastest)

---

### 2. Chat with Temperature Control

Adjust creativity:

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "MiniMax-Text-01",
  "messages": [
    {"role": "user", "content": "Write a short poem about AI."}
  ],
  "temperature": 0.7,
  "max_tokens": 200
}
```

Then run:

```bash
bash -c 'curl -s "https://api.minimax.io/v1/text/chatcompletion_v2" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json' | jq '.choices[0].message.content'
```

**Parameters:**

- `temperature` (0-1): Higher = more creative
- `top_p` (0-1, default 0.95): Sampling diversity
- `max_tokens`: Maximum output tokens

---

### 3. Streaming Response

Get real-time output:

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "MiniMax-M1",
  "messages": [
    {"role": "user", "content": "Explain quantum computing."}
  ],
  "stream": true
}
```

Then run:

```bash
curl -s "https://api.minimax.io/v1/text/chatcompletion_v2" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json
```

Streaming is recommended for reasoning models (M1/M2).

---

### 4. Reasoning Model (M1/M2)

Use reasoning models for complex tasks:

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "MiniMax-M1",
  "messages": [
    {"role": "user", "content": "Solve step by step: A train travels 120km in 2 hours. What is its average speed in m/s?"}
  ],
  "stream": true
}
```

Then run:

```bash
curl -s "https://api.minimax.io/v1/text/chatcompletion_v2" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json
```

Response includes `reasoning_content` field with thought process.

---

### 5. Text-to-Speech (Basic)

Convert text to speech:

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "speech-02-hd",
  "text": "Hello, this is a test of MiniMax text to speech.",
  "voice_id": "male-qn-qingse",
  "speed": 1.0,
  "format": "mp3"
}
```

Then run:

```bash
curl -s "https://api.minimax.io/v1/t2a_v2" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json --output speech.mp3
```

---

### 6. TTS with Emotion

Add emotion to speech (speech-02 models):

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "speech-02-hd",
  "text": "I am so happy to meet you today!",
  "voice_id": "female-shaonv",
  "emotion": "happy",
  "speed": 1.0,
  "format": "mp3"
}
```

Then run:

```bash
curl -s "https://api.minimax.io/v1/t2a_v2" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json --output happy_speech.mp3
```

**Emotion options:** `happy`, `sad`, `angry`, `fearful`, `disgusted`, `surprised`, `neutral`

---

### 7. TTS with Audio Settings

Fine-tune audio output:

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "speech-02-hd",
  "text": "High quality audio test.",
  "voice_id": "male-qn-qingse",
  "speed": 1.0,
  "vol": 1.0,
  "pitch": 0,
  "audio_sample_rate": 32000,
  "bitrate": 128000,
  "format": "mp3"
}
```

Then run:

```bash
curl -s "https://api.minimax.io/v1/t2a_v2" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json --output hq_speech.mp3
```

**TTS models:**

- `speech-02-hd`: High definition (best quality)
- `speech-02-turbo`: Fast generation
- `speech-01-hd`: Previous gen HD
- `speech-01-turbo`: Previous gen fast

---

### 8. Text-to-Video (T2V)

Generate video from text prompt:

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "T2V-01-Director",
  "prompt": "A cat playing with a ball of yarn [Static shot].",
  "duration": 6,
  "resolution": "1080P"
}
```

Then run:

```bash
bash -c 'curl -s "https://api.minimax.io/v1/video_generation" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json' | jq '.task_id'
```

Video generation is async - returns a task ID to poll for completion.

---

### 9. T2V with Camera Control

Control camera movement in videos:

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "A person walking through a forest [Tracking shot], then stops to look at a bird [Push in].",
  "duration": 6,
  "resolution": "1080P"
}
```

Then run:

```bash
bash -c 'curl -s "https://api.minimax.io/v1/video_generation" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json' | jq '.task_id'
```

**Camera commands (in brackets):**

- Movement: `Truck left/right`, `Pan left/right`, `Push in/Pull out`
- Vertical: `Pedestal up/down`, `Tilt up/down`
- Zoom: `Zoom in/out`
- Special: `Shake`, `Tracking shot`, `Static shot`

Combine with `[Pan left, Pedestal up]` (max 3 simultaneous).

---

### 10. Image-to-Video (I2V)

Generate video from an image:

> **Note:** For I2V, use `MiniMax-Hailuo-2.3` or `S2V-01` model which supports `first_frame_image`. The `T2V-01-Director` model is text-to-video only.

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "The scene comes to life with gentle movement [Static shot].",
  "first_frame_image": "https://example.com/image.jpg",
  "duration": 6,
  "resolution": "1080P"
}
```

Then run:

```bash
bash -c 'curl -s "https://api.minimax.io/v1/video_generation" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json' | jq '.task_id'
```

Provide `first_frame_image` as URL or base64-encoded image.

---

### 11. Function Calling (Tools)

Use tools with chat:

Write to `/tmp/minimax_request.json`:

```json
{
  "model": "MiniMax-Text-01",
  "messages": [
    {"role": "user", "content": "What is the weather in Beijing?"}
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "City name"}
          },
          "required": ["location"]
        }
      }
    }
  ],
  "tool_choice": "auto"
}
```

Then run:

```bash
bash -c 'curl -s "https://api.minimax.io/v1/text/chatcompletion_v2" -X POST -H "Authorization: Bearer ${MINIMAX_API_KEY}" -H "Content-Type: application/json" -d @/tmp/minimax_request.json' | jq '.choices[0]'
```

---

## Response Format

### Chat Completion

```json
{
  "id": "string",
  "choices": [{
  "message": {
  "role": "assistant",
  "content": "Response text",
  "reasoning_content": "Thought process (M1/M2 only)"
  },
  "finish_reason": "stop"
  }],
  "usage": {
  "prompt_tokens": 10,
  "completion_tokens": 50,
  "total_tokens": 60
  }
}
```

---

## Guidelines

1. **Use correct host**: China uses `api.minimax.io`, global uses `api.minimaxi.chat`
2. **Streaming for reasoning**: M1/M2 models work best with `stream: true`
3. **Camera syntax**: Video commands go in `[brackets]` within prompts
4. **Emotion in TTS**: Only works with `speech-02-*` and `speech-01-*` models
5. **Async video**: Video generation returns task ID - poll for completion
6. **Chinese optimized**: MiniMax excels at Chinese language tasks
