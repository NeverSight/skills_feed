---
name: eachlabs-video-generation
description: Generate new videos from text prompts, images, or reference inputs using EachLabs AI models. Supports text-to-video, image-to-video, transitions, motion control, talking head, and avatar generation. Use when the user wants to create new video content. For editing existing videos, see eachlabs-video-edit.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Video Generation

Generate new videos from text prompts, images, or reference inputs using 165+ AI models via the EachLabs Predictions API. For editing existing videos (upscaling, lip sync, extension, subtitles), see the `eachlabs-video-edit` skill.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable or pass it directly. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Quick Start

### 1. Create a Prediction

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "pixverse-v5-6-text-to-video",
    "version": "0.0.1",
    "input": {
      "prompt": "A golden retriever running through a meadow at sunset, cinematic slow motion",
      "resolution": "720p",
      "duration": "5",
      "aspect_ratio": "16:9"
    }
  }'
```

### 2. Poll for Result

```bash
curl https://api.eachlabs.ai/v1/prediction/{prediction_id} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

Poll until `status` is `"success"` or `"failed"`. The output video URL is in the response.

## Model Selection Guide

### Text-to-Video

| Model | Slug | Best For |
|-------|------|----------|
| Pixverse v5.6 | `pixverse-v5-6-text-to-video` | General purpose, audio generation |
| XAI Grok Imagine | `xai-grok-imagine-text-to-video` | Fast creative |
| Kandinsky 5 Pro | `kandinsky5-pro-text-to-video` | Artistic, high quality |
| Seedance v1.5 Pro | `seedance-v1-5-pro-text-to-video` | Cinematic quality |
| Wan v2.6 | `wan-v2-6-text-to-video` | Long/narrative content |
| Kling v2.6 Pro | `kling-v2-6-pro-text-to-video` | Motion control |
| Pika v2.2 | `pika-v2-2-text-to-video` | Stylized, effects |
| Minimax Hailuo V2.3 Pro | `minimax-hailuo-v2-3-pro-text-to-video` | High fidelity |
| Sora 2 Pro | `sora-2-text-to-video-pro` | Premium quality |
| Veo 3 | `veo-3` | Google's best quality |
| Veo 3.1 | `veo3-1-text-to-video` | Latest Google model |
| LTX v2 Fast | `ltx-v-2-text-to-video-fast` | Fastest generation |
| Moonvalley Marey | `moonvalley-marey-text-to-video` | Cinematic style |
| Ovi | `ovi-text-to-video` | General purpose |

### Image-to-Video

| Model | Slug | Best For |
|-------|------|----------|
| Pixverse v5.6 | `pixverse-v5-6-image-to-video` | General purpose |
| XAI Grok Imagine | `xai-grok-imagine-image-to-video` | Creative edits |
| Wan v2.6 Flash | `wan-v2-6-image-to-video-flash` | Fastest |
| Wan v2.6 | `wan-v2-6-image-to-video` | High quality |
| Seedance v1.5 Pro | `seedance-v1-5-pro-image-to-video` | Cinematic |
| Kandinsky 5 Pro | `kandinsky5-pro-image-to-video` | Artistic |
| Kling v2.6 Pro I2V | `kling-v2-6-pro-image-to-video` | Best Kling quality |
| Kling O1 | `kling-o1-image-to-video` | Latest Kling model |
| Pika v2.2 I2V | `pika-v2-2-image-to-video` | Effects, PikaScenes |
| Minimax Hailuo V2.3 Pro | `minimax-hailuo-v2-3-pro-image-to-video` | High fidelity |
| Sora 2 I2V | `sora-2-image-to-video` | Premium quality |
| Veo 3.1 I2V | `veo3-1-image-to-video` | Google's latest |
| Runway Gen4 Turbo | `gen4-turbo` | Fast, film quality |
| Veed Fabric 1.0 | `veed-fabric-1-0` | Social media |

### Transitions & Effects

| Model | Slug | Best For |
|-------|------|----------|
| Pixverse v5.6 Transition | `pixverse-v5-6-transition` | Smooth transitions |
| Pika v2.2 PikaScenes | `pika-v2-2-pikascenes` | Scene effects |
| Pixverse v4.5 Effect | `pixverse-v4-5-effect` | Video effects |
| Veo 3.1 First Last Frame | `veo3-1-first-last-frame-to-video` | Interpolation |

### Motion Control & Animation

| Model | Slug | Best For |
|-------|------|----------|
| Kling v2.6 Pro Motion | `kling-v2-6-pro-motion-control` | Pro motion control |
| Kling v2.6 Standard Motion | `kling-v2-6-standard-motion-control` | Standard motion |
| Motion Fast | `motion-fast` | Fast motion transfer |
| Motion Video 14B | `motion-video-14b` | High quality motion |
| Wan v2.6 R2V | `wan-v2-6-reference-to-video` | Reference-based |
| Kling O1 Reference I2V | `kling-o1-reference-image-to-video` | Reference-based |

### Talking Head & Lip Sync

| Model | Slug | Best For |
|-------|------|----------|
| Bytedance Omnihuman v1.5 | `bytedance-omnihuman-v1-5` | Full body animation |
| Creatify Aurora | `creatify-aurora` | Audio-driven avatar |
| Infinitalk I2V | `infinitalk-image-to-video` | Image talking head |
| Infinitalk V2V | `infinitalk-video-to-video` | Video talking head |
| Sync Lipsync v2 Pro | `sync-lipsync-v2-pro` | Lip sync |
| Kling Avatar v2 Pro | `kling-avatar-v2-pro` | Pro avatar |
| Kling Avatar v2 Standard | `kling-avatar-v2-standard` | Standard avatar |
| Echomimic V3 | `echomimic-v3` | Face animation |
| Stable Avatar | `stable-avatar` | Stable talking head |

## Prediction Flow

1. **Check model** `GET https://api.eachlabs.ai/v1/model?slug=<slug>` — validates the model exists and returns the `request_schema` with exact input parameters. Always do this before creating a prediction to ensure correct inputs.
2. **POST** `https://api.eachlabs.ai/v1/prediction` with model slug, version `"0.0.1"`, and input parameters matching the schema
3. **Poll** `GET https://api.eachlabs.ai/v1/prediction/{id}` until status is `"success"` or `"failed"`
4. **Extract** the output video URL from the response

## Examples

### Image-to-Video with Wan v2.6 Flash

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "wan-v2-6-image-to-video-flash",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/photo.jpg",
      "prompt": "The person turns to face the camera and smiles",
      "duration": "5",
      "resolution": "1080p"
    }
  }'
```

### Video Transition with Pixverse

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "pixverse-v5-6-transition",
    "version": "0.0.1",
    "input": {
      "prompt": "Smooth morphing transition between the two images",
      "first_image_url": "https://example.com/start.jpg",
      "end_image_url": "https://example.com/end.jpg",
      "duration": "5",
      "resolution": "720p"
    }
  }'
```

### Motion Control with Kling v2.6

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "kling-v2-6-pro-motion-control",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/character.jpg",
      "video_url": "https://example.com/dance-reference.mp4",
      "character_orientation": "video"
    }
  }'
```

### Talking Head with Omnihuman

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "bytedance-omnihuman-v1-5",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/portrait.jpg",
      "audio_url": "https://example.com/speech.mp3",
      "resolution": "1080p"
    }
  }'
```

## Prompt Tips

- Be specific about motion: "camera slowly pans left" rather than "nice camera movement"
- Include style keywords: "cinematic", "anime", "3D animation", "cyberpunk"
- Describe timing: "slow motion", "time-lapse", "fast-paced"
- For image-to-video, describe what should change from the static image
- Use negative prompts to avoid unwanted elements (where supported)

## Parameter Reference

See [references/MODELS.md](references/MODELS.md) for complete parameter details for each model.
