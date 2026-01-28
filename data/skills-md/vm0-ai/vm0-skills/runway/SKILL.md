---
name: runway
description: Runway AI API for video generation via curl. Use this skill to generate videos from images, text, or other videos.
vm0_secrets:
  - RUNWAY_API_KEY
---

# Runway API

Use the Runway API via direct `curl` calls to **generate AI videos** from images, text, or video inputs.

> Official docs: `https://docs.dev.runwayml.com/`

---

## When to Use

Use this skill when you need to:

- **Generate video from images** (image-to-video)
- **Generate video from text prompts** (text-to-video)
- **Transform existing videos** (video-to-video)
- **Generate images from text** (text-to-image)
- **Upscale video resolution** (4X upscale)
- **Generate sound effects or speech**

---

## Prerequisites

1. Sign up at [Runway Developer Portal](https://dev.runwayml.com/)
2. Purchase credits ($10 for 1000 credits)
3. Create an API key in the dashboard
4. Store it in the environment variable `RUNWAY_API_KEY`

```bash
export RUNWAY_API_KEY="your-api-key"
```

### Pricing

- Credits are consumed per generation
- ~25 credits per 5-second video

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume you have `RUNWAY_API_KEY` set.

Base URL: `https://api.dev.runwayml.com/v1`

**Required headers for all requests:**
- `Authorization: Bearer ${RUNWAY_API_KEY}`
- `X-Runway-Version: 2024-11-06`
- `Content-Type: application/json`

---

### 1. Check Organization Credits

Check your credit balance:

```bash
bash -c 'curl -s -X GET "https://api.dev.runwayml.com/v1/organization" --header "Authorization: Bearer ${RUNWAY_API_KEY}" --header "X-Runway-Version: 2024-11-06"'
```

---

### 2. Image to Video

Generate a video from an image:

Write to `/tmp/runway_request.json`:

```json
{
  "model": "gen4_turbo",
  "promptImage": "https://example.com/your-image.jpg",
  "promptText": "A timelapse of clouds moving across the sky",
  "ratio": "1280:720",
  "duration": 5
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.dev.runwayml.com/v1/image_to_video" --header "Authorization: Bearer ${RUNWAY_API_KEY}" --header "X-Runway-Version: 2024-11-06" --header "Content-Type: application/json" -d @/tmp/runway_request.json'
```

**Response:**
```json
{
  "id": "task-id-here"
}
```

---

### 3. Text to Video

Generate a video from text only:

> **Note:** Text-to-video only supports duration values of 4, 6, or 8 seconds (not arbitrary values like image-to-video).

Write to `/tmp/runway_request.json`:

```json
{
  "model": "veo3.1",
  "promptText": "A serene forest with sunlight filtering through the trees",
  "ratio": "1280:720",
  "duration": 6
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.dev.runwayml.com/v1/text_to_video" --header "Authorization: Bearer ${RUNWAY_API_KEY}" --header "X-Runway-Version: 2024-11-06" --header "Content-Type: application/json" -d @/tmp/runway_request.json'
```

---

### 4. Video to Video

Transform an existing video:

Write to `/tmp/runway_request.json`:

```json
{
  "model": "gen4_aleph",
  "videoUri": "https://example.com/source-video.mp4",
  "promptText": "Add magical sparkles and fairy dust effects",
  "ratio": "1280:720"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.dev.runwayml.com/v1/video_to_video" --header "Authorization: Bearer ${RUNWAY_API_KEY}" --header "X-Runway-Version: 2024-11-06" --header "Content-Type: application/json" -d @/tmp/runway_request.json'
```

---

### 5. Text to Image

Generate images from text:

Write to `/tmp/runway_request.json`:

```json
{
  "model": "gen4_image_turbo",
  "promptText": "A futuristic cityscape at sunset",
  "ratio": "1920:1080",
  "referenceImages": []
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.dev.runwayml.com/v1/text_to_image" --header "Authorization: Bearer ${RUNWAY_API_KEY}" --header "X-Runway-Version: 2024-11-06" --header "Content-Type: application/json" -d @/tmp/runway_request.json'
```

---

### 6. Check Task Status

Poll for task completion. Replace `<your-task-id>` with the actual task ID:

```bash
bash -c 'curl -s -X GET "https://api.dev.runwayml.com/v1/tasks/<your-task-id>" --header "Authorization: Bearer ${RUNWAY_API_KEY}" --header "X-Runway-Version: 2024-11-06"'
```

**Response when complete:**
```json
{
  "id": "task-id",
  "status": "SUCCEEDED",
  "output": ["https://cdn.runwayml.com/generated-video.mp4"]
}
```

**Possible statuses:** `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`

---

### 7. Cancel a Task

Cancel a running task. Replace `<your-task-id>` with the actual task ID:

```bash
bash -c 'curl -s -X DELETE "https://api.dev.runwayml.com/v1/tasks/<your-task-id>" --header "Authorization: Bearer ${RUNWAY_API_KEY}" --header "X-Runway-Version: 2024-11-06"'
```

---

### 8. Video Upscale (4X)

Upscale video resolution:

Write to `/tmp/runway_request.json`:

```json
{
  "model": "upscale_v1",
  "videoUri": "https://example.com/low-res-video.mp4"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.dev.runwayml.com/v1/video_upscale" --header "Authorization: Bearer ${RUNWAY_API_KEY}" --header "X-Runway-Version: 2024-11-06" --header "Content-Type: application/json" -d @/tmp/runway_request.json'
```

---

### 9. Generate Sound Effects

Generate audio from text:

Write to `/tmp/runway_request.json`:

```json
{
  "model": "eleven_text_to_sound_v2",
  "promptText": "Thunder rumbling in the distance"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.dev.runwayml.com/v1/sound_effect" --header "Authorization: Bearer ${RUNWAY_API_KEY}" --header "X-Runway-Version: 2024-11-06" --header "Content-Type: application/json" -d @/tmp/runway_request.json'
```

---

## Available Models

| Endpoint | Models |
|----------|--------|
| Image to Video | `gen4_turbo`, `gen3a_turbo`, `veo3.1`, `veo3` |
| Text to Video | `veo3.1`, `veo3.1_fast`, `veo3` |
| Video to Video | `gen4_aleph` |
| Text to Image | `gen4_image_turbo`, `gen4_image` |
| Video Upscale | `upscale_v1` |

---

## Aspect Ratios

Common ratios for video generation:
- `1280:720` (16:9 landscape)
- `720:1280` (9:16 portrait)
- `1024:1024` (1:1 square)

---

## Guidelines

1. **Poll for completion**: Video generation is async; poll `/tasks/{id}` until status is `SUCCEEDED`
2. **Use appropriate models**: `gen4_turbo` is faster, `gen4_aleph` for video-to-video
3. **Download promptly**: Output URLs may expire after some time
4. **Monitor credits**: Check `/organization` endpoint to track usage
5. **Handle rate limits**: API returns 429 when rate limited; add delays
