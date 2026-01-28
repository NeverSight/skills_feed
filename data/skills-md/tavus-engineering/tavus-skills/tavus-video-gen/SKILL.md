---
name: tavus-video-gen
description: Generate AI videos with Tavus replicas. Use when creating personalized videos from scripts or audio, adding custom backgrounds, watermarks, or generating videos at scale. Covers the video generation API, not real-time conversations.
---

# Tavus Video Generation Skill

Generate personalized AI videos with replicas speaking your script.

## Quick Start

```bash
curl -X POST https://tavusapi.com/v2/videos \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "replica_id": "rfe12d8b9597",
    "script": "Hey there! Welcome to our product demo."
  }'
```

Response:
```json
{
  "video_id": "1e30440cf9",
  "status": "queued"
}
```

## Full API Options

```bash
curl -X POST https://tavusapi.com/v2/videos \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "replica_id": "rfe12d8b9597",
    "script": "Your script text here",
    "video_name": "Product Demo v1",
    "callback_url": "https://your-webhook.com/video-ready",
    "background_url": "https://example.com/landing-page",
    "background_source_url": "https://s3.../background.mp4",
    "watermark_url": "https://s3.../logo.png",
    "fast": false,
    "transparent_background": false
  }'
```

### Parameters

| Param | Description |
|-------|-------------|
| `replica_id` | Required. Stock or custom replica ID |
| `script` | Text for replica to speak (use this OR audio_url) |
| `audio_url` | Pre-recorded audio (.wav/.mp3) for replica to lip-sync |
| `video_name` | Display name |
| `callback_url` | Webhook for completion/error |
| `background_url` | Website URL to record as background |
| `background_source_url` | Video file URL for background |
| `watermark_url` | PNG/JPEG logo overlay |
| `fast` | Quick render (disables some features) |
| `transparent_background` | WebM with alpha (requires `fast: true`) |

## Using Audio Instead of Script

```json
{
  "replica_id": "rfe12d8b9597",
  "audio_url": "https://s3.../narration.mp3"
}
```

Supported formats: `.wav`, `.mp3`

## Background Options

### Website Background
Records a scrolling website as the background:
```json
{
  "background_url": "https://example.com/landing-page"
}
```

### Video Background
Uses a video file:
```json
{
  "background_source_url": "https://s3.../promo-bg.mp4"
}
```

### Transparent Background
For compositing in video editors:
```json
{
  "fast": true,
  "transparent_background": true
}
```
Outputs `.webm` with alpha channel.

## Check Video Status

```bash
curl https://tavusapi.com/v2/videos/{video_id} \
  -H "x-api-key: YOUR_API_KEY"
```

Status values: `queued`, `generating`, `ready`, `error`, `deleted`

When ready:
```json
{
  "status": "ready",
  "hosted_url": "https://videos.tavus.io/video/xxx",
  "download_url": "https://stream.mux.com/.../high.mp4",
  "stream_url": "https://stream.mux.com/xxx.m3u8"
}
```

## Webhook Callback

On completion:
```json
{
  "video_id": "1e30440cf9",
  "status": "ready",
  "hosted_url": "https://videos.tavus.io/video/1e30440cf9",
  "download_url": "...",
  "stream_url": "..."
}
```

On error:
```json
{
  "video_id": "xxx",
  "status": "error",
  "status_details": "Error message here"
}
```

## Scripting Best Practices

- Keep under 5 minutes for quality/engagement
- Write conversationally (speak out loud to test)
- Use punctuation to indicate pauses
- Clear structure: intro → body → CTA
- Break long content into multiple videos

## List & Delete Videos

```bash
# List all videos
curl https://tavusapi.com/v2/videos -H "x-api-key: YOUR_API_KEY"

# Delete video
curl -X DELETE https://tavusapi.com/v2/videos/{video_id} \
  -H "x-api-key: YOUR_API_KEY"
```
