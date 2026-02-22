---
name: media-generation
description: |
  Generate images and videos using x402-protected AI models at StableStudio.

  USE FOR:
  - Generating images from text prompts
  - Generating videos from text or images
  - Editing images with AI
  - Creating visual content

  TRIGGERS:
  - "generate image", "create image", "make a picture"
  - "generate video", "create video", "make a video"
  - "edit image", "modify image"
  - "stablestudio", "nano-banana", "sora", "veo"

  ALWAYS use `npx agentcash fetch` or `npx agentcash fetch-auth` for stablestudio.dev endpoints.
---

# Media Generation with StableStudio

Generate images and videos via x402 payments at `https://stablestudio.dev`.

## Setup

If the agentcash CLI is not yet installed, see [rules/getting-started.md](rules/getting-started.md) for installation and wallet setup.

## Quick Reference

| Task | Endpoint | Cost | Time |
|------|----------|------|------|
| Image (default) | `https://stablestudio.dev/api/generate/nano-banana-pro/generate` | $0.13-0.24 | ~10s |
| Image (budget) | `https://stablestudio.dev/api/generate/nano-banana/generate` | $0.039 | ~5s |
| Video (default) | `https://stablestudio.dev/api/generate/veo-3.1/generate` | $1.60-3.20 | 1-2min |
| Video (budget) | `https://stablestudio.dev/api/generate/wan-2.6/t2v` | $0.34-1.02 | 2-5min |
| Image edit | `https://stablestudio.dev/api/generate/nano-banana-pro/edit` | $0.13-0.24 | ~10s |

## Image Generation

**Recommended: nano-banana-pro** (best quality/cost)

```bash
npx agentcash fetch https://stablestudio.dev/api/generate/nano-banana-pro/generate -m POST -b '{
  "prompt": "a cat wearing a space helmet, photorealistic",
  "aspectRatio": "16:9",
  "imageSize": "2K"
}'
```

**Options:**
- `aspectRatio`: "1:1", "16:9", "9:16"
- `imageSize`: "1K", "2K", "4K" (nano-banana-pro only)

## Video Generation

**Recommended: veo-3.1** (best quality/cost)

```bash
npx agentcash fetch https://stablestudio.dev/api/generate/veo-3.1/generate -m POST -b '{
  "prompt": "a timelapse of clouds moving over mountains",
  "durationSeconds": "6",
  "aspectRatio": "16:9"
}'
```

**Options:**
- `durationSeconds`: "4", "6", "8"
- `aspectRatio`: "16:9", "9:16"

## Job Polling

Generation returns a `jobId`. Poll until complete:

```bash
npx agentcash fetch-auth https://stablestudio.dev/api/jobs/{jobId}
```

Poll images every 3s, videos every 10s. Result contains `imageUrl` or `videoUrl`.

## Image Editing

Requires uploading the source image first. See [rules/uploads.md](rules/uploads.md).

```bash
npx agentcash fetch https://stablestudio.dev/api/generate/nano-banana-pro/edit -m POST -b '{
  "prompt": "change the background to a beach sunset",
  "images": ["https://...blob-url..."]
}'
```

## Model Comparison

| Model | Type | Best For |
|-------|------|----------|
| nano-banana-pro | Image | General purpose, up to 4K |
| nano-banana | Image | Quick drafts, budget |
| gpt-image-1.5 | Image | Fast, variable quality |
| veo-3.1 | Video | High quality, 1080p |
| wan-2.6 | Video | Budget, text or image input |
| sora-2 | Video | Premium quality |
