---
name: z-ai-api
description: |
  Z.ai API integration for building applications with GLM models. Use when working with Z.ai/ZhipuAI APIs for: (1) Chat completions with GLM-4.7/4.6/4.5 models, (2) Vision/multimodal tasks with GLM-4.6V, (3) Image generation with GLM-Image or CogView-4, (4) Video generation with CogVideoX-3 or Vidu models, (5) Audio transcription with GLM-ASR-2512, (6) Function calling and tool use, (7) Web search integration, (8) Translation, slide/poster generation agents. Triggers: Z.ai, ZhipuAI, GLM, BigModel, Zhipu, CogVideoX, CogView, Vidu.
---

# Z.ai API Skill

## Quick Reference

**Base URL:** `https://api.z.ai/api/paas/v4`
**Coding Plan URL:** `https://api.z.ai/api/coding/paas/v4`
**Auth:** `Authorization: Bearer YOUR_API_KEY`

## Core Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/chat/completions` | Text/vision chat |
| `/images/generations` | Image generation |
| `/videos/generations` | Video generation (async) |
| `/audio/transcriptions` | Speech-to-text |
| `/web_search` | Web search |
| `/async-result/{id}` | Poll async tasks |
| `/v1/agents` | Translation, slides, effects |

## Model Selection

**Chat (pick by need):**
- `glm-4.7` — Latest flagship, best quality, agentic coding
- `glm-4.7-flash` — Fast, high quality
- `glm-4.6` — Reliable general use
- `glm-4.5-flash` — Fastest, lower cost

**Vision:**
- `glm-4.6v` — Best multimodal (images, video, files)
- `glm-4.6v-flash` — Fast vision

**Media:**
- `glm-image` — High-quality images (HD, ~20s)
- `cogview-4-250304` — Fast images (~5-10s)
- `cogvideox-3` — Video, up to 4K, 5-10s
- `viduq1-text/image` — Vidu video generation

## Implementation Patterns

### Basic Chat
```python
from zai import ZaiClient

client = ZaiClient(api_key="YOUR_KEY")

response = client.chat.completions.create(
    model="glm-4.7",
    messages=[
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(response.choices[0].message.content)
```

### OpenAI SDK Compatibility
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_ZAI_KEY",
    base_url="https://api.z.ai/api/paas/v4/"
)
# Use exactly like OpenAI SDK
```

### Streaming
```python
response = client.chat.completions.create(
    model="glm-4.7",
    messages=[...],
    stream=True
)
for chunk in response:
    print(chunk.choices[0].delta.content, end="")
```

### Function Calling
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
}]

response = client.chat.completions.create(
    model="glm-4.7",
    messages=[{"role": "user", "content": "Weather in Tokyo?"}],
    tools=tools,
    tool_choice="auto"
)

# Handle tool_calls in response.choices[0].message.tool_calls
```

### Vision (Images/Video/Files)
```python
response = client.chat.completions.create(
    model="glm-4.6v",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://..."}},
            {"type": "text", "text": "Describe this image"}
        ]
    }]
)
```

### Image Generation
```python
response = client.images.generate(
    model="glm-image",
    prompt="A serene mountain at sunset",
    size="1280x1280",
    quality="hd"
)
print(response.data[0].url)  # Expires in 30 days
```

### Video Generation (Async)
```python
# Submit
response = client.videos.generate(
    model="cogvideox-3",
    prompt="A cat playing with yarn",
    size="1920x1080",
    duration=5
)
task_id = response.id

# Poll for result
import time
while True:
    result = client.async_result.get(task_id)
    if result.task_status == "SUCCESS":
        print(result.video_result[0].url)
        break
    time.sleep(5)
```

### Web Search Integration
```python
response = client.chat.completions.create(
    model="glm-4.7",
    messages=[{"role": "user", "content": "Latest AI news?"}],
    tools=[{
        "type": "web_search",
        "web_search": {
            "enable": True,
            "search_result": True
        }
    }]
)
# Access response.web_search for sources
```

### Thinking Mode (Chain-of-Thought)
```python
response = client.chat.completions.create(
    model="glm-4.7",
    messages=[...],
    thinking={"type": "enabled"},
    stream=True  # Recommended with thinking
)
# Access reasoning_content in response
```

## Key Parameters

| Parameter | Values | Notes |
|-----------|--------|-------|
| `temperature` | 0.0-1.0 | GLM-4.7: 1.0, GLM-4.5: 0.6 default |
| `top_p` | 0.01-1.0 | Default ~0.95 |
| `max_tokens` | varies | GLM-4.7: 128K, GLM-4.5: 96K max |
| `stream` | bool | Enable SSE streaming |
| `response_format` | `{"type": "json_object"}` | Force JSON output |

## Error Handling

- **429**: Rate limited — implement exponential backoff
- **401**: Bad API key — verify credentials
- **sensitive**: Content filtered — modify input

```python
if response.choices[0].finish_reason == "tool_calls":
    # Execute function and continue conversation
elif response.choices[0].finish_reason == "length":
    # Increase max_tokens or truncate
elif response.choices[0].finish_reason == "sensitive":
    # Content was filtered
```

## Reference Files

For detailed API specifications, consult:
- `references/chat-completions.md` — Full chat API, parameters, models
- `references/tools-and-functions.md` — Function calling, web search, retrieval
- `references/media-generation.md` — Image, video, audio APIs
- `references/agents.md` — Translation, slides, effects agents
- `references/error-codes.md` — Error handling, rate limits
