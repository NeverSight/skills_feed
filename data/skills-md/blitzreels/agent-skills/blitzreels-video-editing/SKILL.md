---
name: blitzreels-video-editing
description: Video editing workflows with BlitzReels API — upload, transcribe, timeline editing, captions, overlays, backgrounds, and export.
---

# BlitzReels Video Editing

Edit videos via the BlitzReels API: upload media, transcribe, edit timeline, apply captions, add overlays and backgrounds, then export.

## Quick Start

```bash
# Upload a video from URL
bash scripts/editor.sh upload-url PROJECT_ID "https://example.com/video.mp4"

# Add to timeline and transcribe
bash scripts/editor.sh add-media PROJECT_ID MEDIA_ID
bash scripts/editor.sh transcribe PROJECT_ID MEDIA_ID

# Trim, caption, export
bash scripts/editor.sh trim PROJECT_ID ITEM_ID 1.0 -2.0
bash scripts/editor.sh captions PROJECT_ID viral-center
bash scripts/editor.sh export PROJECT_ID --resolution 1080p
```

## Primary Workflow

1. **Create project** — `POST /projects {"name":"...", "aspect_ratio":"9:16"}`
2. **Upload media** — `editor.sh upload-url` (URL import) or 2-step presigned upload
3. **Add to timeline** — `editor.sh add-media` places media on the timeline
4. **Transcribe** — `editor.sh transcribe` generates word-level captions
5. **Get context** — `editor.sh context` to see timeline state
6. **Edit timeline** — trim, split, delete, reorder, auto-remove silences
7. **Apply captions** — `editor.sh captions <presetId>` for styled subtitles
8. **Add overlays** — text overlays, motion code, motion graphics
9. **Add background** — fill layers (gradients, cinematic, patterns)
10. **Export** — `editor.sh export` renders final video with download URL

## Scripts

### `scripts/editor.sh`

Subcommand wrapper for common editing operations.

| Command | Usage | Description |
|---------|-------|-------------|
| `upload-url` | `<projectId> <url> [name]` | Upload media from URL |
| `transcribe` | `<projectId> <mediaId>` | Transcribe + poll until done |
| `context` | `<projectId> [mode]` | Get project context (default: timeline) |
| `timeline-at` | `<projectId> <seconds>` | Get items at timestamp |
| `trim` | `<projectId> <itemId> <startDelta> <endDelta>` | Trim item edges |
| `split` | `<projectId> <itemId> <atSeconds>` | Split item at time |
| `delete-item` | `<projectId> <itemId>` | Delete timeline item |
| `add-media` | `<projectId> <mediaId> [startSec]` | Add media to timeline |
| `add-broll` | `<projectId> <JSON>` | Add B-roll clip |
| `captions` | `<projectId> <presetId>` | Apply caption preset |
| `export` | `<projectId> [--resolution R]` | Export + poll + download URL |

Run `bash scripts/editor.sh --help` for full usage.

### `scripts/blitzreels.sh`

Generic API helper for direct endpoint calls. Use for overlays, effects, and advanced operations where `editor.sh` doesn't have a shortcut.

```bash
bash scripts/blitzreels.sh METHOD /path [JSON_BODY]
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BLITZREELS_API_KEY` | Yes | API key (`br_live_...`) |
| `BLITZREELS_API_BASE_URL` | No | Override base URL (default: `https://www.blitzreels.com/api/v1`) |
| `BLITZREELS_ALLOW_EXPENSIVE` | No | Set to `1` for export calls via `blitzreels.sh` |

## API Endpoint Index

### Projects

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects` | Create project |
| GET | `/projects/{id}` | Get project details |
| PATCH | `/projects/{id}` | Update project settings |
| DELETE | `/projects/{id}` | Delete project |
| GET | `/projects` | List projects |

### Media

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/media` | Import media from URL |
| POST | `/projects/{id}/upload/presigned` | Get presigned upload URL |
| POST | `/projects/{id}/upload/finalize` | Finalize presigned upload |

### Transcription

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/transcribe` | Start transcription job |
| GET | `/jobs/{jobId}` | Poll job status |
| GET | `/projects/{id}/context?mode=transcript` | Get transcript |
| POST | `/projects/{id}/captions/regenerate` | Re-transcribe media |

### Captions

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/captions` | Apply caption preset |
| GET | `/projects/{id}/captions/style` | Get current style |
| PATCH | `/projects/{id}/captions/style` | Update style settings |
| GET | `/projects/{id}/captions/presets` | List presets by category |
| PATCH | `/projects/{id}/captions/{captionId}` | Update caption words/timing |
| DELETE | `/projects/{id}/captions/{captionId}` | Delete caption |
| POST | `/projects/{id}/captions/words/emphasis` | Emphasize specific words |

### Timeline Editing

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/timeline/media` | Add media to timeline |
| POST | `/projects/{id}/timeline/trim` | Trim item by deltas |
| POST | `/projects/{id}/timeline/split` | Split item at timestamp |
| DELETE | `/projects/{id}/timeline/items/{itemId}` | Delete item |
| PATCH | `/projects/{id}/timeline/items/{itemId}` | Update item |
| POST | `/projects/{id}/timeline/items/batch-update` | Batch update items |
| PATCH | `/projects/{id}/timeline/items/{itemId}/volume` | Set volume |
| PATCH | `/projects/{id}/timeline/items/{itemId}/transform` | Set transform |
| POST | `/projects/{id}/timeline/pack-clips` | Remove gaps |
| POST | `/projects/{id}/timeline/silence-detection` | Detect silences |
| POST | `/projects/{id}/timeline/mistake-detection` | AI mistake detection |
| POST | `/projects/{id}/timeline/caption-recut` | Caption-based recut plan |

### Overlays — Text, Motion Code, Motion Graphics

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/text-overlays` | Add text overlay |
| PATCH | `/projects/{id}/text-overlays/{oid}` | Update text overlay |
| DELETE | `/projects/{id}/text-overlays/{oid}` | Remove text overlay |
| POST | `/projects/{id}/motion-code` | Add animated code block |
| PATCH | `/projects/{id}/motion-code/{cid}` | Update code block |
| POST | `/projects/{id}/motion-graphics` | Add motion graphic |
| PATCH | `/projects/{id}/motion-graphics/{gid}` | Update motion graphic |

### Backgrounds

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/fill-layers` | Add fill layer |
| PATCH | `/projects/{id}/fill-layers/{lid}` | Update fill layer |

### Context & State

| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects/{id}/context?mode=...` | Get project context |
| GET | `/projects/{id}/timeline/at?time_seconds=X` | Items at timestamp |
| POST | `/projects/{id}/timeline/undo` | Undo last action |

### Export & Jobs

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/export` | Start export (expensive) |
| GET | `/exports/{exportId}` | Export status + download URL |
| GET | `/projects/{id}/exports` | Export history |
| DELETE | `/projects/{id}/exports` | Delete all exports |
| GET | `/jobs/{jobId}` | Generic job polling |

### Effects & Keyframes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/timeline/effects/zoom` | Add zoom effect |
| POST | `/projects/{id}/timeline/effects/mask` | Add mask effect |
| POST | `/projects/{id}/timeline/effects/color-grade` | Add color grade |
| POST | `/projects/{id}/timeline/items/{itemId}/keyframes` | Create keyframe |

---

## Context Modes

Use `?mode=` to control what data the context endpoint returns:

| Mode | Returns |
|------|---------|
| `summary` | Project metadata, duration, media count |
| `assets` | All media assets with metadata |
| `timeline` | Full timeline with items, layers, timing |
| `transcript` | Word-level transcript from transcription |
| `full` | Everything combined |

Default: `timeline`

```bash
bash scripts/editor.sh context PROJECT_ID timeline
bash scripts/editor.sh context PROJECT_ID full
```

## Upload Modes

### URL Import (Simpler)
```bash
bash scripts/editor.sh upload-url PROJECT_ID "https://example.com/video.mp4"
```

### Presigned 2-Step (For Local Files)
```bash
# Step 1: Get presigned URL
PRESIGNED=$(bash scripts/blitzreels.sh POST /projects/PROJECT_ID/upload/presigned \
  '{"fileName":"video.mp4","contentType":"video/mp4"}')

# Step 2: Upload to presigned URL
curl -X PUT "$(echo $PRESIGNED | jq -r '.url')" \
  -H "Content-Type: video/mp4" \
  --data-binary @video.mp4

# Step 3: Finalize
bash scripts/blitzreels.sh POST /projects/PROJECT_ID/upload/finalize \
  "{\"storageKey\":\"$(echo $PRESIGNED | jq -r '.key')\"}"
```

## Quick Reference

- **Caption presets**: 30+ presets across 6 categories — see `references/caption-styles.md`
- **Active word animations**: highlight, scale, glow, lift, bounce, punch, slam, elastic, shake, none
- **Motion code themes**: github-dark, one-dark, dracula, nord, monokai, tokyo-night
- **Fill layer presets**: 38+ across 7 categories — see `references/fill-layers.md`
- **Timeline layer order**: caption(0) → effect(1) → image(2) → video(3) → audio(4) → background(5)

## References

- `references/caption-styles.md` — All 30+ presets, CaptionStyleSettings schema, animations
- `references/overlays.md` — Text overlays, motion code, motion graphics schemas
- `references/fill-layers.md` — 38+ background presets, FillLayerSettings schema
- `references/timeline-ops.md` — Timeline endpoints, AI features, keyframes, effects
- `references/export-settings.md` — Export params, codecs, polling pattern
- `examples/edit-uploaded-video.md` — Full upload→edit→export walkthrough
- `examples/enhance-with-overlays.md` — Adding graphics to existing project

## Safety & Notes

- Use `https://www.blitzreels.com/api/v1` as base URL (avoid redirect from non-www)
- Export and B-roll generation are **expensive** — require `BLITZREELS_ALLOW_EXPENSIVE=1`
- `editor.sh export` sets this automatically; `blitzreels.sh` requires explicit opt-in
- Download URLs are temporary (24h TTL)
- Full OpenAPI spec: `https://www.blitzreels.com/api/openapi.json`

## Rate Limits

| Plan | Requests/min | Requests/day |
|------|-------------|-------------|
| Free | 10 | 100 |
| Lite | 30 | 1,000 |
| Creator | 60 | 5,000 |
| Agency | 120 | 20,000 |
