---
name: mux-video
displayName: Mux Video
description: "Upload, manage, and embed videos via Mux. Covers direct uploads, API asset management, webhook event flow, playback embedding, and the Mux CLI. Use when uploading video, creating assets, checking encoding status, embedding playback, or handling Mux webhook events."
version: 0.1.0
author: joel
tags:
  - video
  - mux
  - media
  - webhooks
---

# Mux Video

Upload, manage, and embed videos through Mux's API and CLI. Integrates with joelclaw's webhook infrastructure and Inngest event pipeline.

## When to Use

Triggers on: "upload video to mux", "create mux asset", "embed mux video", "check video status", "mux playback", "direct upload", "video encoding", "mux webhook", or any task involving video hosting via Mux.

## Credentials

Stored in agent-secrets:
- `mux_token_id` — API token ID
- `mux_token_secret` — API token secret
- `mux_signing_key_id` — URL signing key ID
- `mux_signing_secret` — webhook signing secret (per-endpoint, HMAC)

Lease credentials:
```bash
secrets lease mux_token_id
secrets lease mux_token_secret
```

Or use env vars `MUX_TOKEN_ID` and `MUX_TOKEN_SECRET`.

## Core Operations

### Create Asset from URL

Ingest a video from a public URL:
```bash
curl https://api.mux.com/video/v1/assets \
  -X POST \
  -H "Content-Type: application/json" \
  -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET} \
  -d '{
    "input": [{"url": "https://example.com/video.mp4"}],
    "playback_policy": ["public"],
    "video_quality": "plus"
  }'
```

Video quality tiers: `basic` (fastest/cheapest), `plus` (default, good quality), `premium` (highest).

### Direct Upload (browser/client-side)

Two-step process:

**Step 1: Create authenticated upload URL (server-side)**
```bash
curl https://api.mux.com/video/v1/uploads \
  -X POST \
  -H "Content-Type: application/json" \
  -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET} \
  -d '{
    "new_asset_settings": {
      "playback_policies": ["public"],
      "video_quality": "plus"
    },
    "cors_origin": "*"
  }'
```

Response includes `data.url` (resumable upload endpoint) and `data.id` (upload ID).

**Step 2: PUT the file to the URL (client-side)**
```bash
curl -X PUT "${UPLOAD_URL}" \
  -H "Content-Type: video/mp4" \
  --data-binary @video.mp4
```

The URL is resumable — large files can be uploaded in chunks. Use [UpChunk](https://github.com/muxinc/upchunk) for browser uploads.

### List Assets
```bash
curl https://api.mux.com/video/v1/assets \
  -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET}
```

### Get Asset Details
```bash
curl https://api.mux.com/video/v1/assets/${ASSET_ID} \
  -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET}
```

### Delete Asset
```bash
curl -X DELETE https://api.mux.com/video/v1/assets/${ASSET_ID} \
  -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET}
```

### Auto-Generated Captions
```bash
curl https://api.mux.com/video/v1/assets \
  -X POST \
  -H "Content-Type: application/json" \
  -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET} \
  -d '{
    "input": [{"url": "https://example.com/video.mp4"}],
    "playback_policy": ["public"],
    "auto_generated_captions": [{"language": "en"}]
  }'
```

## Playback

### Embed URL
Once an asset is ready and has a playback ID:
```
https://stream.mux.com/${PLAYBACK_ID}.m3u8
```

### Thumbnail/Poster
```
https://image.mux.com/${PLAYBACK_ID}/thumbnail.jpg
https://image.mux.com/${PLAYBACK_ID}/thumbnail.jpg?time=10
https://image.mux.com/${PLAYBACK_ID}/animated.gif?start=5&end=10
```

### Mux Player (Web Component)
```html
<mux-player
  playback-id="${PLAYBACK_ID}"
  metadata-video-title="My Video"
  accent-color="#FF0000"
></mux-player>
```

Install: `npm install @mux/mux-player-react` for React, or use the web component directly.

### React Component
```tsx
import MuxPlayer from "@mux/mux-player-react";

<MuxPlayer
  playbackId={playbackId}
  metadata={{ video_title: "My Video" }}
  accentColor="#FF0000"
/>
```

## Webhook Events

Mux webhooks are registered at: `https://panda.tail7af24.ts.net/webhooks/mux`

The webhook provider (`packages/system-bus/src/webhooks/providers/mux.ts`) handles HMAC-SHA256 verification and normalizes events into the Inngest pipeline.

### Key Events

| Mux Event | Inngest Event | When |
|-----------|---------------|------|
| `video.asset.created` | `mux/asset.created` | Asset record created |
| `video.asset.ready` | `mux/asset.ready` | Encoding complete, playable |
| `video.asset.errored` | `mux/asset.errored` | Encoding failed |
| `video.upload.created` | `mux/upload.created` | Direct upload URL created |
| `video.upload.asset_created` | `mux/upload.asset_created` | Upload completed, asset created |
| `video.upload.cancelled` | `mux/upload.cancelled` | Upload cancelled or timed out |
| `video.asset.live_stream_completed` | `mux/asset.live_stream_completed` | Live stream recording ready |

### Event Payload Structure
```json
{
  "type": "video.asset.ready",
  "data": {
    "id": "asset_id",
    "playback_ids": [{"id": "playback_id", "policy": "public"}],
    "status": "ready",
    "duration": 120.5,
    "passthrough": "your_custom_id",
    "tracks": [...]
  }
}
```

The `passthrough` field carries your custom identifier through the entire pipeline — use it to correlate uploads with your application records.

### Building Inngest Functions for Mux Events

```typescript
// Example: Notify when video is ready
const onVideoReady = inngest.createFunction(
  { id: "mux-video-ready", name: "Mux Video Ready" },
  { event: "mux/asset.ready" },
  async ({ event, step }) => {
    const { data } = event;
    const playbackId = data.playback_ids?.[0]?.id;
    const duration = data.duration;

    // Your logic here — update DB, notify user, etc.
    await step.run("notify", async () => {
      // ...
    });
  }
);
```

## passthrough Pattern

Always set `passthrough` when creating assets or uploads. This is your correlation ID that flows through all webhook events:

```bash
curl https://api.mux.com/video/v1/assets \
  -X POST \
  -H "Content-Type: application/json" \
  -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET} \
  -d '{
    "input": [{"url": "https://example.com/video.mp4"}],
    "playback_policy": ["public"],
    "passthrough": "my-unique-correlation-id"
  }'
```

## Rules

- **Always use `passthrough`** for tracking — it's your only way to correlate webhooks back to your records.
- **Don't poll for status** in production — use webhooks. Mux has rate limits.
- **Webhook signing secret is per-endpoint** — it's the secret you get when registering the webhook URL in the Mux dashboard, NOT the API token secret or signing key.
- **Video quality tiers affect cost** — `basic` for drafts/previews, `plus` for production, `premium` only when needed.
- **Direct upload URLs expire** — default 1 hour timeout. Create them on-demand, not ahead of time.
- **Playback IDs are stable** — once an asset is ready, the playback ID doesn't change. Safe to cache/store.
