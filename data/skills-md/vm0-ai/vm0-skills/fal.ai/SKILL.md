---
name: fal.ai
description: fal.ai AI image generation. Use this skill when you need to use fal, fal.ai, or generate images from text prompts using AI text-to-image models.
vm0_secrets:
  - FAL_KEY
---

# fal.ai Image Generator

Use the fal.ai API to **generate images from text prompts**.

> Official docs: `https://fal.ai/docs`

---

## When to Use

Use this skill when you need to:

- **Generate images from text descriptions**
- **Create illustrations or visual content**
- **Generate blog headers, thumbnails, or social media images**

---

## Prerequisites

1. Sign up at [fal.ai](https://fal.ai/)
2. Get your API key from the dashboard

```bash
export FAL_KEY="your-api-key"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

### 1. Generate Image (nano-banana-pro - fast)

Write to `/tmp/fal_request.json`:

```json
{
  "prompt": "A futuristic city at sunset, cyberpunk style"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://fal.run/fal-ai/nano-banana-pro" --header "Authorization: Key ${FAL_KEY}" --header "Content-Type: application/json" -d @/tmp/fal_request.json' | jq -r '.images[0].url'
```

### 2. Generate Image (flux/schnell - fast)

Write to `/tmp/fal_request.json`:

```json
{
  "prompt": "A cute cat eating a cookie"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://fal.run/fal-ai/flux/schnell" --header "Authorization: Key ${FAL_KEY}" --header "Content-Type: application/json" -d @/tmp/fal_request.json' | jq -r '.images[0].url'
```

### 3. Generate Image (recraft-v3 - high quality)

Write to `/tmp/fal_request.json`:

```json
{
  "prompt": "Abstract art, vibrant colors"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://fal.run/fal-ai/recraft-v3" --header "Authorization: Key ${FAL_KEY}" --header "Content-Type: application/json" -d @/tmp/fal_request.json' | jq -r '.images[0].url'
```

### 4. Generate with Custom Size

Write to `/tmp/fal_request.json`:

```json
{
  "prompt": "Mountain landscape",
  "image_size": "landscape_16_9"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://fal.run/fal-ai/nano-banana-pro" --header "Authorization: Key ${FAL_KEY}" --header "Content-Type: application/json" -d @/tmp/fal_request.json' | jq -r '.images[0].url'
```

### 5. Download Generated Image

Write to `/tmp/fal_request.json`:

```json
{
  "prompt": "A minimalist workspace"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://fal.run/fal-ai/nano-banana-pro" --header "Authorization: Key ${FAL_KEY}" --header "Content-Type: application/json" -d @/tmp/fal_request.json' | jq -r '.images[0].url' | xargs curl -sL -o /tmp/image.png
```

### 6. Pipe Prompt from Echo (JSON escaped)

```bash
echo "A dragon breathing fire, epic fantasy art" | jq -Rs '{prompt: .}' > /tmp/fal_request.json
bash -c 'curl -s -X POST "https://fal.run/fal-ai/nano-banana-pro" --header "Authorization: Key ${FAL_KEY}" --header "Content-Type: application/json" -d @/tmp/fal_request.json' | jq -r '.images[0].url'
```

### 7. Pipe Prompt from File (JSON escaped)

```bash
cat /tmp/prompt.txt | jq -Rs '{prompt: .}' > /tmp/fal_request.json
bash -c 'curl -s -X POST "https://fal.run/fal-ai/nano-banana-pro" --header "Authorization: Key ${FAL_KEY}" --header "Content-Type: application/json" -d @/tmp/fal_request.json' | jq -r '.images[0].url'
```

### 8. Pipe with Additional Parameters

```bash
echo "Neon city at night" | jq -Rs '{prompt: ., image_size: "landscape_16_9"}' > /tmp/fal_request.json
bash -c 'curl -s -X POST "https://fal.run/fal-ai/nano-banana-pro" --header "Authorization: Key ${FAL_KEY}" --header "Content-Type: application/json" -d @/tmp/fal_request.json' | jq -r '.images[0].url'
```

---

## Available Models

| Model | Description |
|-------|-------------|
| `nano-banana-pro` | Fast, good quality (recommended) |
| `flux/schnell` | Fast generation |
| `flux-pro` | High quality |
| `recraft-v3` | High quality vector/illustration |

See more at: https://fal.ai/models

---

## Image Sizes

| Size | Aspect Ratio |
|------|--------------|
| `square` | 1:1 |
| `square_hd` | 1:1 (high res) |
| `portrait_4_3` | 4:3 |
| `portrait_16_9` | 16:9 |
| `landscape_4_3` | 3:4 |
| `landscape_16_9` | 9:16 |

---

## Prompt Guidelines

For best results:

1. **Be specific** - Describe the subject clearly
2. **Add style hints** - "modern", "minimalist", "photorealistic", "digital art", "cinematic"
3. **Specify colors/mood** - "blue and purple gradient", "warm tones", "dark and moody"
4. **Keep it concise** - Clear and focused descriptions work better
