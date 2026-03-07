---
name: videoagent-video-studio
version: 2.1.0
author: pexoai
emoji: "🎬"
tags:
  - video
  - video-generation
  - text-to-video
  - image-to-video
  - veo
  - grok
  - kling
  - seedance
  - minimax
  - hunyuan
  - pixverse
description: >
  Generate short AI videos from text or images — text-to-video, image-to-video, and reference-based generation — with zero API key setup. Use when the user wants to create a video clip, animate an image, or generate video from a description.
metadata:
  openclaw:
    emoji: "🎬"
    install:
      - id: node
        kind: node
        label: "No dependencies needed — all calls go through the hosted proxy"
---

# 🎬 VideoAgent Video Studio

**Use when:** User asks to generate a video, create a video from text, animate an image, make a short clip, or produce AI video.

Generate short AI videos with 7 backends. This skill picks the right mode (text-to-video or image-to-video), enhances the prompt for best results, and returns the video URL.

---

## Quick Reference

| User Intent | Mode | Typical Duration |
|-------------|------|------------------|
| "Make a video of..." (no image) | `text-to-video` | 4–10 s |
| "Animate this image" / "Make this move" | `image-to-video` | 4–6 s |
| "Turn this into a video with..." | `image-to-video` | 4–6 s |
| Cinematic, story, ad | Prefer `text-to-video` with detailed prompt | 5–10 s |

### Generation Modes

| Mode | Description | Models |
|------|-------------|--------|
| **text-to-video** | Text prompt only → video | minimax, kling, veo, hunyuan, grok, seedance |
| **image-to-video** | Single image + prompt → animated clip | minimax, kling, veo, pixverse, grok, seedance |
| **reference-based** | Reference images/video → consistent output | minimax, kling, veo, hunyuan, grok, seedance |

### Models (use `--model <id>`)

| Model ID | T2V | I2V | Reference | Notes |
|----------|-----|-----|-----------|-------|
| `minimax` | ✅ | ✅ | ✅ | Subject reference image, character consistency |
| `kling` | ✅ | ✅ | ✅ | Multi-element / character / keyframe (O3) |
| `veo` | ✅ | ✅ | ✅ | Google Veo 3.1, multiple reference images |
| `hunyuan` | ✅ | — | ✅ | Video-to-video style transfer |
| `pixverse` | — | ✅ | — | Stylized image-to-video |
| `grok` | ✅ | ✅ | ✅ | Video editing via reference video |
| `seedance` | ✅ | ✅ | ✅ | Seedance 1.5 Pro, synchronized audio, 4–12 s |

Full model details and endpoint reference: [references/models.md](references/models.md).

---

## How to Generate a Video

### Step 1 — Choose mode and enhance the prompt

- **Text-to-video**: Expand with subject, action, camera movement, lighting, and style. Be specific about motion (e.g. "camera slowly zooms in", "character walks left to right").
- **Image-to-video**: Describe the motion to apply to the image (e.g. "gentle breeze in the hair", "camera pans across the scene"). See [references/prompt_guide.md](references/prompt_guide.md) for patterns.

### Step 2 — Run the script

**Text-to-video:**
```bash
node {baseDir}/tools/generate.js \
  --mode text-to-video \
  --prompt "<enhanced prompt>" \
  --duration <seconds> \
  --aspect-ratio <ratio>
```

**Image-to-video:**
```bash
node {baseDir}/tools/generate.js \
  --mode image-to-video \
  --prompt "<motion description>" \
  --image-url "<public image URL>" \
  --duration <seconds> \
  --aspect-ratio <ratio>
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--mode` | `text-to-video` | `text-to-video` or `image-to-video` |
| `--prompt` | *(required)* | Scene or motion description |
| `--image-url` | — | Required for `image-to-video`; public image URL |
| `--duration` | `5` | Length in seconds (typically 4–10) |
| `--aspect-ratio` | `16:9` | `16:9`, `9:16`, `1:1`, `4:3`, `3:4` |
| `--model` | `auto` | Model ID (e.g. `kling`, `veo`, `grok`, `seedance`); `auto` = proxy picks |

**Other commands:**

| Command | Description |
|---------|-------------|
| `node tools/generate.js --list-models` | List available models from the proxy |
| `node tools/generate.js --status --job-id <id>` | Check async job status |

### Step 3 — Return the result

The script returns JSON:

```json
{
  "success": true,
  "mode": "text-to-video",
  "videoUrl": "https://...",
  "duration": 5,
  "aspectRatio": "16:9"
}
```

Send `videoUrl` to the user.

---

## Example Conversations

**User:** "Generate a short video of a cat walking in the rain, cinematic."

```bash
node {baseDir}/tools/generate.js \
  --mode text-to-video \
  --prompt "A cat walking through rain, wet streets, neon reflections, cinematic lighting, slow motion, 4K" \
  --duration 5 \
  --aspect-ratio 16:9
```

---

**User:** "Animate this photo" *(user uploads a landscape)*

```bash
node {baseDir}/tools/generate.js \
  --mode image-to-video \
  --prompt "Gentle clouds moving across the sky, subtle grass movement, cinematic atmosphere" \
  --image-url "https://..." \
  --duration 5 \
  --aspect-ratio 16:9
```

---

**User:** "Make a 10-second vertical video of a coffee pour, slow motion."

```bash
node {baseDir}/tools/generate.js \
  --mode text-to-video \
  --prompt "Close-up of coffee pouring into a white cup, slow motion, steam rising, soft lighting, product shot" \
  --duration 10 \
  --aspect-ratio 9:16
```

---

**User:** "Use Google Veo for a cinematic shot."

```bash
node {baseDir}/tools/generate.js \
  --mode text-to-video \
  --model veo \
  --prompt "A dragon flying through cloudy skies, cinematic lighting, 8s" \
  --duration 8 \
  --aspect-ratio 16:9
```

---

**User:** "Animate this portrait."

```bash
node {baseDir}/tools/generate.js \
  --mode image-to-video \
  --model grok \
  --prompt "Gentle smile, subtle head turn" \
  --image-url "https://..." \
  --duration 5
```

---

## Setup

**Zero API keys by default.** Requests go through a hosted proxy. Set these for a custom proxy or token:

| Variable | Required | Description |
|----------|----------|-------------|
| `VIDEO_STUDIO_PROXY_URL` | No | Proxy base URL |
| `VIDEO_STUDIO_TOKEN` | No | Auth token if the proxy requires it |

---

## Knowledge Base

- **[references/prompt_guide.md](references/prompt_guide.md)** — Prompt patterns for text-to-video and image-to-video.
- **[references/models.md](references/models.md)** — Model list, capabilities, and selection guide.
- **[references/calling_guide.md](references/calling_guide.md)** — Per-model endpoint details, input parameters, and special handling.
