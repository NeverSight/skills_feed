---
name: media-craft
description: >
  Generate, edit, transform, and enhance media using the obra CLI.
  Use when the user asks to create/generate/edit images, videos, music,
  or audio. Covers text-to-image, image-to-image, image editing,
  upscaling, background removal, text-to-video, image-to-video,
  video-to-video, motion control, AI avatars, music generation,
  lyrics, and music videos.
license: MIT
metadata:
  author: NanHeSam
  version: "1.0.0"
---

# Media Craft — obra CLI Skill

## Overview

`obra` is a unified CLI for AI media generation. It handles images, videos, and music through a consistent async-task workflow. Use this skill whenever the user asks to generate, create, edit, transform, upscale, or enhance any media.

## Prerequisites

```bash
npm install -g obra
obra config set kie.apiKey YOUR_API_KEY
```

## Core Workflow

Every obra command follows the same pattern:

1. **Preferred: synchronous with `--wait --json`** — blocks until the task completes and returns JSON with output URLs.
2. **Save output directly** — add `-o <path>` to download the result to a local file.
3. **Async fallback** — if `--wait` is not used, obra returns a task ID. Poll with `obra status <id> --wait --json`, then download with `obra download <id> -o <dir>`.

Always use `--wait --json` unless the user explicitly wants async behavior.

---

## Image Generation

Generate images from text prompts.

```bash
obra image generate "a serene mountain lake at sunset" --wait --json
```

### Key Flags

| Flag | Description |
|------|-------------|
| `--model <model>` | Model to use (default: `flux-2/pro-text-to-image`) |
| `--param <key=value>` | Model-specific parameter (repeatable) |
| `--params-json <json>` | JSON object of model parameters |
| `-o <path>` | Save output to file |

Model-specific parameters vary by model. Common ones include `aspect_ratio`, `seed`, `negative_prompt`, `width`, `height`. Use `obra image info <model>` to see available parameters for a specific model.

### Example: specific model and aspect ratio

```bash
obra image generate "cyberpunk cityscape" --model google/imagen4 --param aspect_ratio=16:9 --wait --json
```

### Available Image Models

Discover models with:

```bash
obra image list
obra image info <model-name>
```

Notable models: `flux-2/pro-text-to-image`, `google/imagen4`, `grok-imagine/text-to-image`, `gpt-image/1.5-text-to-image`, `seedream/4.5-text-to-image`, `qwen/text-to-image`, `ideogram/character`, `z-image`.

---

## Image Editing & Transformation

### Image-to-Image (Edit with Reference)

Provide an input image URL plus a prompt describing the edit. Use `--param image_urls=<url>` to pass the reference image (must be a URL, not a local path):

```bash
obra image generate "make it look like winter" --model seedream/4.5-edit --param image_urls=https://example.com/input.jpg --wait --json
```

Edit-capable models: `seedream/4.5-edit`, `bytedance/seedream-v4-edit`, `qwen/image-edit`, `grok-imagine/image-to-image`, `gpt-image/1.5-image-to-image`, `google/nano-banana-edit`, `google/pro-image-to-image`, `ideogram/character-edit`.

Use `obra image info <model>` to check the exact parameter names for each model.

### Upscaling

Some upscale models take a `task_id` from a previous generation task:

```bash
obra image generate "" --model grok-imagine/upscale --param task_id=<previous-task-id> --wait --json
```

Other upscale models accept image URLs directly:

```bash
obra image generate "upscale" --model topaz/image-upscale --param image_urls=https://example.com/low-res.jpg --wait --json
```

Upscale models: `grok-imagine/upscale`, `topaz/image-upscale`, `recraft/crisp-upscale`.

### Background Removal

```bash
obra image generate "" --model recraft/remove-background --param image_urls=https://example.com/photo.jpg --wait --json
```

### Reframing (Extend / Outpaint)

```bash
obra image generate "extend the scene" --model ideogram/v3-reframe --param image_urls=https://example.com/photo.jpg --wait --json
```

### Character Remix

```bash
obra image generate "character in a new style" --model ideogram/character-remix --param image_urls=https://example.com/character.jpg --wait --json
```

---

## Video Generation

Generate videos from text or images.

```bash
obra video generate "a cat playing piano" --wait --json
```

### Key Flags

| Flag | Description |
|------|-------------|
| `--model <model>` | Video model to use |
| `-i, --image <path>` | Input image for image-to-video |
| `--param <key=value>` | Model-specific parameter (repeatable) |
| `--params-json <json>` | JSON object of model parameters |
| `-o <path>` | Save output to file |

Model-specific parameters (aspect ratio, duration, etc.) vary by model. Use `obra video info <model>` to see available parameters.

### Image-to-Video

```bash
obra video generate "bring this scene to life" -i scene.jpg --wait --json
```

### Available Video Models

```bash
obra video list
obra video info <model-name>
```

Notable models by provider:
- **xAI**: `grok-imagine/text-to-video`, `grok-imagine/image-to-video`
- **Kuaishou**: `kling-2.6/text-to-video`, `kling-2.6/image-to-video`, `kling/v2-1-master-text-to-video`
- **OpenAI**: `sora-2-text-to-video`, `sora-2-pro-text-to-video`, `sora-2-image-to-video`, `sora-2-pro-image-to-video`
- **Alibaba**: `wan/2-6-text-to-video`, `wan/2-6-image-to-video`
- **MiniMax**: `hailuo/02-text-to-video-pro`, `hailuo/2-3-image-to-video-pro`
- **Bytedance**: `bytedance/seedance-1.5-pro`, `bytedance/v1-pro-image-to-video`

---

## Video Editing & Transformation

### Video-to-Video

Transform an existing video with a new prompt:

```bash
obra video generate "convert to anime style" -i input.mp4 --model wan/2-6-video-to-video --wait --json
```

### Video Upscaling

```bash
obra video generate "upscale" -i low-res.mp4 --model topaz/video-upscale --wait --json
```

### Watermark Removal

```bash
obra video generate "remove watermark" -i watermarked.mp4 --model sora-watermark-remover --wait --json
```

### Motion Control

```bash
obra video generate "camera pan left" -i scene.jpg --model kling-2.6/motion-control --wait --json
```

### AI Avatars

Generate talking-head avatar videos:

```bash
obra video generate "introduce yourself as a tech reviewer" -i avatar.jpg --model kling/ai-avatar-pro --wait --json
```

Models: `kling/ai-avatar-standard`, `kling/ai-avatar-pro`.

### Speech-to-Video

```bash
obra video generate "speaking character" -i audio.wav --model wan/2-2-a14b-speech-to-video-turbo --wait --json
```

### Storyboard

```bash
obra video generate "scene 1: ...; scene 2: ..." --model sora-2-pro-storyboard --wait --json
```

---

## Music Generation

Generate music from text prompts.

```bash
obra music generate "upbeat electronic dance track" --wait --json
```

### Key Flags

| Flag | Description |
|------|-------------|
| `-m, --model <model>` | Model version: `V3_5`, `V4`, `V4_5`, `V4_5PLUS`, `V4_5ALL`, `V5` (default: `V4_5`) |
| `-i, --instrumental` | Generate without vocals |
| `-c, --custom-mode` | Enable custom mode (requires `--style` and `--title`) |
| `-s, --style <style>` | Music style/genre (requires `--custom-mode`) |
| `-t, --title <title>` | Track title (requires `--custom-mode`) |
| `--vocal-gender <gender>` | `m` or `f` |
| `--negative-tags <tags>` | Music styles to exclude |
| `--style-weight <n>` | Style adherence strength (0-1) |
| `--weirdness-constraint <n>` | Creative deviation control (0-1) |
| `--audio-weight <n>` | Audio feature balance (0-1) |
| `-o <path>` | Save output to file |

### Instrumental Track

```bash
obra music generate "calm lo-fi hip hop beat for studying" --instrumental --wait --json
```

### Custom Mode

```bash
obra music generate "lyrics here..." --custom-mode --style "indie folk" --title "Morning Light" --wait --json
```

---

## Lyrics Generation

Generate lyrics from a prompt (synchronous, no `--wait` needed):

```bash
obra music lyrics "a song about coding at 3am" --json
```

---

## Music Videos

Generate a music video from a completed music task:

```bash
obra music video <taskId> <audioId> --wait --json
```

The `taskId` and `audioId` come from the output of a prior `obra music generate` command.

---

## Synchronized Lyrics (Timestamps)

Get word-level timestamps for generated music:

```bash
obra music timestamps <taskId> <audioId> --json
```

---

## Model Discovery

List and inspect available models for any media type:

```bash
obra image list          # list image models
obra video list          # list video models
obra music list          # list music models

obra image info <model>  # detailed info about a specific model
obra video info <model>
```

---

## Task Management

```bash
obra status              # show all running tasks
obra status <id> --wait --json  # wait for a specific task
obra download <id> -o ./output  # download task results
obra history list        # list past tasks
obra history show <id>   # show details of a past task
```

---

## Best Practices

1. **Always use `--wait --json`** to get structured output with download URLs in a single call.
2. **Use `-o <path>`** to save files directly when the user wants a local file.
3. **Write detailed prompts** — more descriptive prompts produce better results across all media types.
4. **Chain workflows** — e.g., generate an image, then use it as input for image-to-video, then upscale the video.
5. **Check model availability** — run `obra <type> list` to see current models before specifying one.
6. **Parse JSON output** — when `--json` is used, parse the JSON to extract URLs, task IDs, and metadata for downstream use.
