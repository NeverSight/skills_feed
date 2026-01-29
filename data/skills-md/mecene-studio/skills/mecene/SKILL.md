---
name: mecene
description: Read and edit videos through the Mecene.ai API. Access transcripts, scenes, speakers via Video-as-Code format. Edit clips by manipulating timeline overlays. Use when working with Mecene videos, clips, overlays, captions, or Video-as-Code data.
---

# Mecene.ai Agent Skills

Mecene.ai transforms videos into a queryable knowledge base called "Video-as-Code". This skill teaches you how to read and edit videos through the Mecene API.

## What is Mecene?

Mecene is a video clip editing SaaS that:
- Analyzes videos to extract transcripts, speakers, scenes, and visual data
- Stores this as structured data (Video-as-Code format)
- Allows you to edit videos by manipulating timeline overlays
- Renders final clips with captions, cuts, and visual effects

## Capabilities

As an AI agent, you can:
1. **List videos** - See all videos in the user's account
2. **Read video data** - Access transcripts, scenes, speakers, and the TOON script
3. **Read clips** - See clip timeline with all overlays
4. **Edit overlays** - Modify, create, or delete timeline elements

## Authentication

See `rules/authentication.md` for how to discover and use the API token.

## API Endpoints

All endpoints require `Authorization: Bearer <token>` header.

### Video & Clip Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/videos` | GET | List all videos |
| `/api/videos/:id` | GET | Get video with Video-as-Code data |
| `/api/clips/:id` | GET | Get clip with all overlays |
| `/api/overlays/:clip_id` | GET | Get all overlays for a clip |

### Single Overlay Endpoints (Recommended)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/overlay/:overlay_id` | GET | Get single overlay |
| `/api/overlay/:overlay_id` | PATCH | Update single overlay |
| `/api/overlay/:overlay_id` | DELETE | Delete single overlay |
| `/api/clips/:clip_id/overlays` | POST | Create new overlay |

### Batch Operations (Advanced)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/overlays/:clip_id` | PATCH | Batch update/create/delete overlays |

## Quick Start

1. Check for token (see `rules/authentication.md`)
2. List videos: `GET /api/videos`
3. Get video details with transcript: `GET /api/videos/:id`
4. Get clip with overlays: `GET /api/clips/:id`
5. Edit single overlay: `PATCH /api/overlay/:overlay_id`

## Rules

- `rules/authentication.md` - Token discovery and usage
- `rules/video-as-code.md` - Understanding the TOON format
- `rules/list-videos.md` - How to list videos
- `rules/get-video-enhanced.md` - How to get video data
- `rules/get-clip.md` - How to get clip with overlays
- `rules/get-overlays.md` - How to get overlays only
- `rules/edit-overlays.md` - How to modify overlays
- `rules/overlay-types.md` - Overlay type schemas
