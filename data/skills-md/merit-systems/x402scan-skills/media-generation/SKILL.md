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

  ALWAYS use mcp__x402__fetch for stablestudio.io endpoints.
---

# Media Generation with StableStudio

Generate images and videos via x402 payments at `https://stablestudio.io`.

## Quick Reference

| Task | Endpoint | Cost | Time |
|------|----------|------|------|
| Image (default) | `/api/x402/nano-banana-pro/generate` | $0.13-0.24 | ~10s |
| Image (budget) | `/api/x402/nano-banana/generate` | $0.039 | ~5s |
| Video (default) | `/api/x402/veo-3.1/generate` | $1.60-3.20 | 1-2min |
| Video (budget) | `/api/x402/wan-2.5/t2v` | $0.34-1.02 | 2-5min |
| Image edit | `/api/x402/nano-banana-pro/edit` | $0.13-0.24 | ~10s |

## Image Generation

**Recommended: nano-banana-pro** (best quality/cost)

```
mcp__x402__fetch(
  url="https://stablestudio.io/api/x402/nano-banana-pro/generate",
  method="POST",
  body={
    "prompt": "a cat wearing a space helmet, photorealistic",
    "aspectRatio": "16:9",
    "imageSize": "2K"
  }
)
```

**Options:**
- `aspectRatio`: "1:1", "16:9", "9:16"
- `imageSize`: "1K", "2K", "4K" (nano-banana-pro only)

## Video Generation

**Recommended: veo-3.1** (best quality/cost)

```
mcp__x402__fetch(
  url="https://stablestudio.io/api/x402/veo-3.1/generate",
  method="POST",
  body={
    "prompt": "a timelapse of clouds moving over mountains",
    "durationSeconds": "6",
    "aspectRatio": "16:9"
  }
)
```

**Options:**
- `durationSeconds`: "4", "6", "8"
- `aspectRatio`: "16:9", "9:16"

## Job Polling

Generation returns a `jobId`. Poll until complete:

```
mcp__x402__fetch_with_auth(
  url="https://stablestudio.io/api/x402/jobs/{jobId}"
)
```

Poll images every 3s, videos every 10s. Result contains `imageUrl` or `videoUrl`.

## Image Editing

Requires uploading the source image first. See [rules/uploads.md](rules/uploads.md).

```
mcp__x402__fetch(
  url="https://stablestudio.io/api/x402/nano-banana-pro/edit",
  method="POST",
  body={
    "prompt": "change the background to a beach sunset",
    "images": ["https://...blob-url..."]
  }
)
```

## Model Comparison

| Model | Type | Best For |
|-------|------|----------|
| nano-banana-pro | Image | General purpose, up to 4K |
| nano-banana | Image | Quick drafts, budget |
| gpt-image-1.5 | Image | Fast, variable quality |
| veo-3.1 | Video | High quality, 1080p |
| wan-2.5 | Video | Budget, text or image input |
| sora-2 | Video | Premium quality |
