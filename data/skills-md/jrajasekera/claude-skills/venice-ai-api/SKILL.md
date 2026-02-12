---
name: venice-ai-api
description: Venice.ai API integration for privacy-first AI applications. Use when building applications with Venice.ai API for chat completions, image generation, video generation, text-to-speech, speech-to-text, or embeddings. Triggers on Venice, Venice.ai, uncensored AI, privacy-first AI, or when users need OpenAI-compatible API with uncensored models.
---

# Venice.ai API Skill

Venice.ai provides privacy-first AI infrastructure with uncensored models and zero data retention. The API is OpenAI-compatible, allowing use of the OpenAI SDK with Venice's base URL. Inference runs on a decentralized network (DePIN) where nodes are disincentivized from retaining user data.

## Quick Reference

**Base URL:** `https://api.venice.ai/api/v1`
**Auth:** `Authorization: Bearer VENICE_API_KEY`
**SDK:** Use OpenAI SDK with custom base URL
**API Key Types:** `ADMIN` (full access) or `INFERENCE` (inference only)

## Setup

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("VENICE_API_KEY"),
    base_url="https://api.venice.ai/api/v1"
)
```

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
    apiKey: process.env.VENICE_API_KEY,
    baseURL: 'https://api.venice.ai/api/v1'
});
```

## Account Tiers

| Tier | Qualification | Rate Limits | Use Case |
|------|--------------|-------------|----------|
| Explorer | Pro subscription | Low RPM/TPM (~15-25 req/day) | Testing, prototyping |
| Paid | USD balance or staked VVV (Diems) | Standard production limits | Commercial apps |
| Partner | Enterprise agreement | Custom high-volume | Enterprise SaaS |

## API Capabilities

### 1. Chat Completions
Text inference with multimodal support (text, images, audio, video).

```python
completion = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello!"}
    ]
)
```

**Popular Models:**
- `llama-3.3-70b` - Balanced performance (Tier M, 128K context)
- `zai-org-glm-4.7` - Complex tasks, deep reasoning (Tier L, 128K context)
- `mistral-31-24b` - Vision + function calling (Tier S, 131K context)
- `venice-uncensored` - No content filtering (Tier S, 32K context)
- `deepseek-ai-DeepSeek-R1` - Advanced reasoning, math, coding (Tier L, 64K context)
- `qwen3-235b` - Massive MoE reasoning (Tier L)
- `qwen3-4b` - Fast, lightweight (Tier XS, 40K context)

**Venice Parameters** (via `extra_body` in Python, direct in JS):
- `enable_web_search`: "off" | "on" | "auto"
- `enable_web_scraping`: boolean
- `enable_web_citations`: boolean — adds `^index^` citation format
- `include_venice_system_prompt`: boolean (default: true)
- `strip_thinking_response`: boolean
- `disable_thinking`: boolean
- `character_slug`: string
- `prompt_cache_key`: string — routing hint for cache hits
- `prompt_cache_retention`: "default" | "extended" | "24h"

See [references/chat-completions.md](references/chat-completions.md) for full parameter reference.

### 2. Image Generation
Generate images from text prompts.

```python
import requests

response = requests.post(
    "https://api.venice.ai/api/v1/image/generate",
    headers={"Authorization": f"Bearer {os.getenv('VENICE_API_KEY')}"},
    json={
        "model": "venice-sd35",
        "prompt": "A sunset over mountains",
        "width": 1024,
        "height": 1024
    }
)
# Response contains base64 images in images array
```

**Image Models:**
| Model | Best For | Pricing |
|-------|----------|---------|
| `qwen-image` | Highest quality, editing | Variable |
| `venice-sd35` | General purpose (default) | ~$0.01/image |
| `hidream` | Fast generation | ~$0.01/image |
| `flux-2-pro` | Professional quality | ~$0.04/image |
| `flux-2-max` | High-quality output | ~$0.02/image |
| `nano-banana-pro` | Photorealism, 2K/4K support | $0.18-$0.35 |

### 3. Image Upscaling
Enhance image resolution 2x or 4x.

```python
import base64

with open("image.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "https://api.venice.ai/api/v1/image/upscale",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "image": image_base64,
        "scale": 4  # 2 or 4
    }
)
# Returns raw image binary
with open("upscaled.png", "wb") as f:
    f.write(response.content)
```

**Pricing:** $0.02 (2x), $0.08 (4x)

### 4. Image Editing (Inpainting)
Modify existing images with AI-powered instructions.

```python
import base64

with open("photo.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "https://api.venice.ai/api/v1/image/edit",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "prompt": "Change the sky to a sunset",
        "image": image_base64  # or URL starting with http/https
    }
)
# Returns raw image binary
with open("edited.png", "wb") as f:
    f.write(response.content)
```

**Model:** Uses Qwen-Image. **Pricing:** ~$0.04/edit.

See [references/image-api.md](references/image-api.md) for all parameters and style presets.

### 5. Video Generation
Async queue-based video generation. Always call `/video/quote` first for pricing.

**Full Workflow:**

```python
import requests
import time
import base64

api_key = os.getenv("VENICE_API_KEY")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Step 1: Get price quote
quote = requests.post(
    "https://api.venice.ai/api/v1/video/quote",
    headers=headers,
    json={
        "model": "kling-2.5-turbo-pro-text-to-video",
        "duration": "10s",
        "resolution": "720p",
        "aspect_ratio": "16:9",
        "audio": True
    }
)
print(f"Estimated cost: ${quote.json()['quote']}")

# Step 2: Queue the job (text-to-video)
queue_resp = requests.post(
    "https://api.venice.ai/api/v1/video/queue",
    headers=headers,
    json={
        "model": "kling-2.5-turbo-pro-text-to-video",
        "prompt": "A serene forest with sunlight filtering through trees",
        "negative_prompt": "low quality, blurry",
        "duration": "10s",
        "resolution": "720p",
        "aspect_ratio": "16:9",
        "audio": True
    }
)
queue_id = queue_resp.json()["queueid"]

# Step 3: Poll until complete
while True:
    status_resp = requests.post(
        "https://api.venice.ai/api/v1/video/retrieve",
        headers=headers,
        json={
            "model": "kling-2.5-turbo-pro-text-to-video",
            "queueid": queue_id,
            "delete_media_on_completion": False
        }
    )
    if (status_resp.status_code == 200
            and status_resp.headers.get("Content-Type") == "video/mp4"):
        with open("output.mp4", "wb") as f:
            f.write(status_resp.content)
        print("Video saved!")
        break
    else:
        status = status_resp.json()
        print(f"Status: {status['status']}, Duration: {status['executionDuration']}ms")
        time.sleep(10)

# Step 4: Cleanup (optional — deletes from Venice storage)
requests.post(
    "https://api.venice.ai/api/v1/video/complete",
    headers=headers,
    json={
        "model": "kling-2.5-turbo-pro-text-to-video",
        "queueid": queue_id
    }
)
```

**Image-to-Video:**
```python
with open("image.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

queue_resp = requests.post(
    "https://api.venice.ai/api/v1/video/queue",
    headers=headers,
    json={
        "model": "wan-2.5-preview-image-to-video",
        "prompt": "Animate this scene with gentle motion",
        "image_url": f"data:image/png;base64,{img_b64}",
        "duration": "5s",
        "resolution": "720p"
    }
)
```

**Video Models:**
| Model | Type | Features |
|-------|------|----------|
| `kling-2.5-turbo-pro` | Text/Image-to-Video | Fast, high quality |
| `wan-2.5-preview` | Image-to-Video | Animation specialist |
| `ltx-2-full` | Text/Image-to-Video | Full quality |
| `veo3-fast` | Text/Image-to-Video | Speed-optimized |
| `sora-2` | Image-to-Video | High-end quality |

See [references/video-api.md](references/video-api.md) for full parameter reference.

### 6. Text-to-Speech
Convert text to audio with 60+ voices.

```python
response = requests.post(
    "https://api.venice.ai/api/v1/audio/speech",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "input": "Hello, welcome to Venice.",
        "model": "tts-kokoro",
        "voice": "af_sky",
        "speed": 1.0,            # 0.25 to 4.0
        "response_format": "mp3"  # mp3, opus, aac, flac, wav, pcm
    }
)
with open("speech.mp3", "wb") as f:
    f.write(response.content)
```

**Voices:** `af_sky`, `af_nova`, `am_liam`, `bf_emma`, `zf_xiaobei`, `jm_kumo`, and 50+ more.
**Pricing:** $3.50 per 1M characters.

### 7. Speech-to-Text
Transcribe audio files.

```python
with open("audio.mp3", "rb") as f:
    response = requests.post(
        "https://api.venice.ai/api/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file": f},
        data={
            "model": "nvidia/parakeet-tdt-0.6b-v3",
            "response_format": "json",  # json or text
            "timestamps": "true"
        }
    )
```

**Formats:** WAV, FLAC, MP3, M4A, AAC, MP4.
**Pricing:** $0.0001 per audio second.

### 8. Embeddings
Generate vector embeddings for RAG and semantic search.

```python
response = requests.post(
    "https://api.venice.ai/api/v1/embeddings",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "text-embedding-bge-m3",
        "input": "Privacy-first AI infrastructure",
        "encoding_format": "float"  # or "base64"
    }
)
```

### 9. Vision (Multimodal)
Analyze images with vision-capable models.

```python
response = client.chat.completions.create(
    model="mistral-31-24b",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What is in this image?"},
            {"type": "image_url", "image_url": {"url": "https://..."}}
        ]
    }]
)
```

### 10. Function Calling
Define tools for the model to call.

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    }
}]

response = client.chat.completions.create(
    model="zai-org-glm-4.7",
    messages=[{"role": "user", "content": "Weather in SF?"}],
    tools=tools
)
```

### 11. Structured Outputs
Get guaranteed JSON schema responses.

```python
response = client.chat.completions.create(
    model="venice-uncensored",
    messages=[...],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "my_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False
            }
        }
    }
)
```

**Requirements:** `strict: true`, `additionalProperties: false`, all fields in `required`.

### 12. AI Characters
Interact with predefined AI personas.

```python
# List characters
characters = requests.get(
    "https://api.venice.ai/api/v1/characters",
    headers={"Authorization": f"Bearer {api_key}"},
    params={"categories": "philosophy", "limit": 50}
).json()

# Chat with a character
response = client.chat.completions.create(
    model="venice-uncensored",
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
    extra_body={
        "venice_parameters": {"character_slug": "alan-watts"}
    }
)
```

### 13. Model Discovery
Query available models and capabilities programmatically.

```python
# List models by type
models = requests.get(
    "https://api.venice.ai/api/v1/models",
    headers={"Authorization": f"Bearer {api_key}"},
    params={"type": "text"}  # text, image, audio, video, embedding
).json()

# Get model traits for auto-selection
traits = requests.get(
    "https://api.venice.ai/api/v1/models/traits",
    params={"type": "text"}
).json()
# e.g. {"default": "zai-org-glm-4.7", "fastest": "qwen3-4b", "uncensored": "venice-uncensored"}

# Use trait as model ID for automatic routing
response = client.chat.completions.create(
    model="fastest",  # Venice routes to the current fastest model
    messages=[...]
)
```

## Error Handling

### Error Codes

| Status | Error Code | Meaning | Action |
|--------|------------|---------|--------|
| 400 | `INVALID_REQUEST` | Bad parameters | Check payload schema |
| 401 | `AUTHENTICATION_FAILED` | Invalid API key | Verify key and balance |
| 402 | — | Insufficient balance | Add USD or stake VVV |
| 403 | — | Unauthorized access | Check key type (ADMIN vs INFERENCE) |
| 413 | — | Payload too large | Reduce request size |
| 415 | — | Invalid content type | Use `application/json` |
| 422 | — | Content policy violation | Modify prompt |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests | Backoff, wait for reset |
| 500 | `INFERENCE_FAILED` | Model error | Retry with backoff |
| 503 | — | Model at capacity | Retry later or switch model |
| 504 | — | Timeout | Use streaming for long responses |

### Abuse Protection
Sending >20 failed requests in 30 seconds triggers a 30-second IP block. Always implement backoff.

### Retry with Exponential Backoff (Python)

```python
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_venice_session():
    """Create a requests session with automatic retry and backoff."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,  # 1s, 2s, 4s
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST", "GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

session = create_venice_session()
response = session.post(url, json=payload, headers=headers)
```

### Retry with Exponential Backoff (JavaScript)

```javascript
async function veniceRequest(url, options, maxRetries = 3) {
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        const response = await fetch(url, options);

        if (response.ok) return response;

        if ([429, 500, 502, 503, 504].includes(response.status)) {
            if (attempt < maxRetries) {
                const delay = Math.pow(2, attempt) * 1000;
                console.log(`Retry ${attempt + 1} in ${delay}ms (status ${response.status})`);
                await new Promise(r => setTimeout(r, delay));
                continue;
            }
        }

        throw new Error(`Venice API error: ${response.status} ${response.statusText}`);
    }
}
```

### Rate Limit-Aware Client (Python)

```python
import time
import requests

class VeniceClient:
    """Wrapper that respects rate limits using response headers."""
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.venice.ai/api/v1"
        self.session = create_venice_session()
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def request(self, method, path, **kwargs):
        resp = self.session.request(
            method, f"{self.base_url}{path}",
            headers=self.headers, **kwargs
        )
        remaining = resp.headers.get("x-ratelimit-remaining-requests")
        if remaining and int(remaining) <= 1:
            reset = resp.headers.get("x-ratelimit-reset-requests")
            if reset:
                wait = max(0, float(reset) - time.time())
                time.sleep(wait)
        resp.raise_for_status()
        return resp
```

## Response Headers

Monitor these headers for production:
- `x-ratelimit-remaining-requests` — Requests left in window
- `x-ratelimit-remaining-tokens` — Tokens left in window
- `x-ratelimit-reset-requests` — Timestamp when request count resets
- `x-venice-balance-usd` — USD balance
- `x-venice-balance-diem` — DIEM balance
- `x-venice-is-blurred` — Image was blurred (safe mode)
- `x-venice-is-content-violation` — Content policy violation
- `x-venice-model-deprecation-warning` — Deprecation notice
- `x-venice-model-deprecation-date` — Sunset date
- `CF-RAY` — Request ID for support

## Rate Limits by Model Tier

**Text Models:**
| Tier | RPM | TPM | Example Models |
|------|-----|-----|----------------|
| XS | 500 | 1,000,000 | qwen3-4b, llama-3.2-3b |
| S | 75 | 750,000 | mistral-31-24b, venice-uncensored |
| M | 50 | 750,000 | llama-3.3-70b, qwen3-next-80b |
| L | 20 | 500,000 | zai-org-glm-4.7, deepseek-ai-DeepSeek-R1 |

**Other Endpoints:**
| Endpoint | RPM |
|----------|-----|
| Image Generation | 20 |
| Audio Synthesis | 60 |
| Audio Transcription | 60 |
| Embeddings | 500 |
| Video Queue | 40 |
| Video Retrieve | 120 |

## API Key Management

```bash
# Create key programmatically (requires ADMIN key)
curl -X POST https://api.venice.ai/api/v1/api_keys \
  -H "Authorization: Bearer $VENICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"apiKeyType": "INFERENCE", "description": "My App", "consumptionLimit": {"usd": 100}}'

# Check rate limits and balance
curl https://api.venice.ai/api/v1/api_keys/rate_limits \
  -H "Authorization: Bearer $VENICE_API_KEY"

# List keys
curl https://api.venice.ai/api/v1/api_keys \
  -H "Authorization: Bearer $VENICE_API_KEY"

# Delete key
curl -X DELETE "https://api.venice.ai/api/v1/api_keys?id={key_id}" \
  -H "Authorization: Bearer $VENICE_API_KEY"
```

## Reference Files

- [references/chat-completions.md](references/chat-completions.md) — Full chat API parameters
- [references/image-api.md](references/image-api.md) — Image generation, editing, upscaling details
- [references/video-api.md](references/video-api.md) — Video generation workflow and parameters
- [references/models.md](references/models.md) — Available models, tiers, pricing, and capabilities
