---
name: eachlabs-video-edit
description: Edit, transform, extend, upscale, and enhance videos using EachLabs AI models. Supports lip sync, video translation, subtitle generation, audio merging, style transfer, and video extension. Use when the user wants to edit or transform existing video content.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Video Edit

Edit, transform, and enhance existing videos using 25+ AI models via the EachLabs Predictions API.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Model Selection Guide

### Video Extension

| Model | Slug | Best For |
|-------|------|----------|
| Veo 3.1 Extend | `veo3-1-extend-video` | Best quality extension |
| Veo 3.1 Fast Extend | `veo3-1-fast-extend-video` | Fast extension |
| PixVerse v5 Extend | `pixverse-v5-extend` | PixVerse extension |
| PixVerse v4.5 Extend | `pixverse-v4-5-extend` | Older PixVerse extension |

### Lip Sync & Talking Head

| Model | Slug | Best For |
|-------|------|----------|
| Sync Lipsync v2 Pro | `sync-lipsync-v2-pro` | Best lip sync quality |
| PixVerse Lip Sync | `pixverse-lip-sync` | PixVerse lip sync |
| LatentSync | `latentsync` | Open-source lip sync |
| Video Retalking | `video-retalking` | Audio-based lip sync |

### Video Transformation

| Model | Slug | Best For |
|-------|------|----------|
| Runway Gen4 Aleph | `runway-gen4-aleph` | Video transformation |
| Kling O1 Video Edit | `kling-o1-video-to-video-edit` | AI video editing |
| Kling O1 V2V Reference | `kling-o1-video-to-video-reference` | Reference-based edit |
| ByteDance Video Stylize | `bytedance-video-stylize` | Style transfer |
| Wan v2.2 Animate Move | `wan-v2-2-14b-animate-move` | Motion animation |
| Wan v2.2 Animate Replace | `wan-v2-2-14b-animate-replace` | Object replacement |

### Video Upscaling & Enhancement

| Model | Slug | Best For |
|-------|------|----------|
| Topaz Upscale Video | `topaz-upscale-video` | Best quality upscale |
| Luma Ray 2 Video Reframe | `luma-dream-machine-ray-2-video-reframe` | Video reframing |
| Luma Ray 2 Flash Reframe | `luma-dream-machine-ray-2-flash-video-reframe` | Fast reframing |

### Audio & Subtitles

| Model | Slug | Best For |
|-------|------|----------|
| FFmpeg Merge Audio Video | `ffmpeg-api-merge-audio-video` | Merge audio track |
| MMAudio V2 | `mm-audio-v-2` | Add audio to video |
| MMAudio | `mmaudio` | Add audio to video |
| Auto Subtitle | `auto-subtitle` | Generate subtitles |
| Merge Videos | `merge-videos` | Concatenate videos |

### Video Translation

| Model | Slug | Best For |
|-------|------|----------|
| Heygen Video Translate | `heygen-video-translate` | Translate video speech |

### Motion Transfer

| Model | Slug | Best For |
|-------|------|----------|
| Motion Fast | `motion-fast` | Fast motion transfer |
| Infinitalk V2V | `infinitalk-video-to-video` | Talking head from video |

### Face Swap (Video)

| Model | Slug | Best For |
|-------|------|----------|
| Faceswap Video | `faceswap-video` | Swap face in video |

## Prediction Flow

1. **Check model** `GET https://api.eachlabs.ai/v1/model?slug=<slug>` — validates the model exists and returns the `request_schema` with exact input parameters. Always do this before creating a prediction to ensure correct inputs.
2. **POST** `https://api.eachlabs.ai/v1/prediction` with model slug, version `"0.0.1"`, and input matching the schema
3. **Poll** `GET https://api.eachlabs.ai/v1/prediction/{id}` until status is `"success"` or `"failed"`
4. **Extract** the output video URL from the response

## Examples

### Extend a Video with Veo 3.1

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "veo3-1-extend-video",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/video.mp4",
      "prompt": "Continue the scene with the camera slowly pulling back"
    }
  }'
```

### Lip Sync with Sync v2 Pro

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "sync-lipsync-v2-pro",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/talking-head.mp4",
      "audio_url": "https://example.com/new-audio.mp3"
    }
  }'
```

### Add Subtitles

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "auto-subtitle",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/video.mp4"
    }
  }'
```

### Merge Audio with Video

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "ffmpeg-api-merge-audio-video",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/video.mp4",
      "audio_url": "https://example.com/music.mp3",
      "start_offset": 0
    }
  }'
```

### Upscale Video with Topaz

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "topaz-upscale-video",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/low-res-video.mp4"
    }
  }'
```

## Parameter Reference

See [references/MODELS.md](references/MODELS.md) for complete parameter details for each model.
