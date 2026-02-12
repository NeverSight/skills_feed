---
name: blitzreels-faceless
description: Faceless AI video generation workflows with BlitzReels (voices, visual styles, jobs, exports).
---

# BlitzReels Faceless Video Generation

Generate AI-powered faceless videos from a topic or script.

> **Cost Warning**: Faceless generation consumes AI credits (AI script writing, image generation, voiceover, video assembly). You MUST present a plan to the user and get approval before calling any expensive endpoint.

## Quick Start

```bash
# Full pipeline: topic → video
bash scripts/faceless.sh --topic "5 productivity tips" --duration 30 --voice rachel --style cinematic

# Dry run — show plan without executing
bash scripts/faceless.sh --topic "5 productivity tips" --dry-run

# From a user-provided script (paragraph breaks = scene breaks)
bash scripts/faceless.sh --script "First scene narration.\n\nSecond scene narration." --duration 60
```

## Required Workflow

**Always use plan mode.** Before generating, present this plan to the user for approval:

1. **Topic or script** — What the video is about
2. **Duration** — 10–120 seconds (drives scene count)
3. **Visual style** — See `references/visual-styles.md` or `GET /visual-styles`
4. **Voice** — See `references/voices.md` or `GET /voices`
5. **Image model** — See `references/models.md` (default: gemini-2.5-flash)
6. **Video model** — See `references/models.md` (default: kling-2.1)
7. **Output mode** — Full video, storyboard-only (images), or images + audio
8. **Captions** — Enabled by default; optionally pick a caption style
9. **Plan summary** — Present all choices + "this will consume AI credits" warning
10. **User approval** → Execute

### Input Modes

| Mode | Flag | Behavior |
|------|------|----------|
| Topic | `--topic "..."` | AI writes the script based on the topic |
| Script | `--script "..."` | User provides exact narration. Paragraph breaks (`\n\n`) become scene breaks. |

If both are provided, `--script` takes precedence.

## Scripts

### `scripts/faceless.sh`
Purpose-built end-to-end pipeline. Handles: create project → generate → poll → export → download URL.

```
faceless.sh --topic TEXT [--duration 30] [--voice rachel] [--style cinematic]
            [--image-model ID] [--video-model ID] [--video-duration SEC]
            [--storyboard-only] [--no-animated-video]
            [--aspect 9:16] [--captions true] [--caption-style ID]
            [--resolution 1080p] [--name TEXT] [--yes] [--dry-run]
```

Run `bash scripts/faceless.sh --help` for full usage.

### `scripts/blitzreels.sh`
Generic API helper for ad-hoc calls. Requires `BLITZREELS_ALLOW_EXPENSIVE=1` for expensive endpoints.

```bash
bash scripts/blitzreels.sh METHOD PATH [JSON_BODY]
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BLITZREELS_API_KEY` | Yes | API key for authentication |
| `BLITZREELS_API_BASE_URL` | No | Override base URL (default: `https://www.blitzreels.com/api/v1`) |
| `BLITZREELS_ALLOW_EXPENSIVE` | No | Set to `1` to allow expensive calls via `blitzreels.sh` |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects` | Create a new project |
| POST | `/projects/{id}/faceless` | Start faceless generation (expensive) |
| GET | `/jobs/{job_id}` | Poll job status |
| GET | `/projects/{id}/context?mode=timeline` | Inspect generated timeline |
| POST | `/projects/{id}/export` | Start export (expensive) |
| GET | `/exports/{export_id}` | Get export status + download URL |
| GET | `/voices` | List available voices |
| GET | `/visual-styles` | List available visual styles |
| GET | `/caption-styles` | List caption style presets |

## Faceless Request Body

```json
{
  "topic": "5 morning routine tips",
  "duration_seconds": 30,
  "visual_style": "cinematic",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "captions": true,
  "caption_style": "bold-center"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| topic | string | one of topic/script | AI generates script from this |
| script | string | one of topic/script | Exact narration text, paragraph breaks = scenes |
| duration_seconds | number | yes | 10–120 |
| visual_style | string | no | Style ID (default: cinematic) |
| voice_id | string | no | ElevenLabs voice ID (default: Rachel) |
| captions | boolean | no | Enable captions (default: true) |
| caption_style | string | no | Caption style preset |
| imageModelId | string | no | Image generation model (default: google-gemini-2.5-flash-image) |
| videoModel | string | no | Video generation model (default: kling-2.1) |
| videoDuration | number | no | Per-clip duration in seconds, 3–10 |
| storyboardOnly | boolean | no | Generate images only, skip video/audio (default: false) |
| generateAnimatedVideos | boolean | no | Set false to skip video animation (default: true) |

## Generation Modes

| Mode | Flag | What's Generated |
|------|------|-----------------|
| **Full video** (default) | — | Images → video clips → voiceover → music → captions |
| **Storyboard only** | `--storyboard-only` | Scene images only (no video, no audio). Cheapest option for previewing. |
| **Images + audio** | `--no-animated-video` | Scene images + voiceover + music (slideshow-style, no video animation) |

## References

- `references/models.md` — All image and video generation models with costs and capabilities
- `references/voices.md` — All available voice IDs, categories, and descriptions
- `references/visual-styles.md` — All available visual style IDs and descriptions

## Safety

- `faceless.sh` prompts for confirmation before calling expensive endpoints (bypass with `--yes`)
- `blitzreels.sh` requires `BLITZREELS_ALLOW_EXPENSIVE=1` for `/faceless` and `/export` paths
- Always present cost/plan to user before generation

## Notes

- Use `https://www.blitzreels.com/api/v1` as your base URL. `https://blitzreels.com` redirects to `www`, and some HTTP clients drop the `Authorization` header on redirects.
- `POST /projects/{id}/faceless` returns a `plan` and `input_warnings` to help you predict what will be generated.
- Full OpenAPI spec: `https://www.blitzreels.com/api/openapi.json`

## Rate Limits

| Plan | Requests/min |
|------|-------------|
| Free | 10 |
| Creator | 30 |
| Pro | 60 |
| Agency | 120 |
