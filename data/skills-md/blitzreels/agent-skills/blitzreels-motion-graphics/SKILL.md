---
name: blitzreels-motion-graphics
description: Motion graphics composition creation via the BlitzReels Playground API (text, shapes, charts, animations, export).
---

# BlitzReels Motion Graphics (Playground API)

Create and edit motion graphics compositions via the Playground API. Build animated scenes with text, shapes, images, video, charts, code blocks, and more.

## Quick Start

```bash
# List available presets
bash scripts/playground.sh list-presets PROJECT_ID

# Create a composition from a JSON file
bash scripts/playground.sh create PROJECT_ID spec.json

# Create from inline JSON
bash scripts/playground.sh create PROJECT_ID '{"name":"Title Card","fps":30,"width":1920,"height":1080,"durationInFrames":90,"mode":"elements","elements":[{"id":"title","type":"text","content":"Hello World","style":{"fontSize":96,"fontWeight":"bold","color":"#fff","display":"flex","justifyContent":"center","alignItems":"center"}}]}'

# Get, update, delete
bash scripts/playground.sh get PROJECT_ID COMP_ID
bash scripts/playground.sh update PROJECT_ID COMP_ID updated-spec.json
bash scripts/playground.sh delete PROJECT_ID COMP_ID

# Export the project
bash scripts/playground.sh export PROJECT_ID --resolution 1080p
```

## Workflow

1. **Create a project** (or use an existing one)
2. **Browse presets** — `playground.sh list-presets` for inspiration
3. **Build composition spec** — JSON describing canvas, elements, and animations
4. **Create composition** — `playground.sh create`
5. **Iterate** — Update elements, adjust timing, add animations
6. **Export** — `playground.sh export`

## Scripts

### `scripts/playground.sh`
Purpose-built CRUD wrapper for playground compositions.

| Command | Usage |
|---------|-------|
| `list-presets` | `playground.sh list-presets <projectId>` |
| `list` | `playground.sh list <projectId>` |
| `create` | `playground.sh create <projectId> <spec.json\|-\|JSON>` |
| `get` | `playground.sh get <projectId> <compositionId>` |
| `update` | `playground.sh update <projectId> <compositionId> <spec>` |
| `delete` | `playground.sh delete <projectId> <compositionId>` |
| `export` | `playground.sh export <projectId> [--resolution 1080p]` |

Run `bash scripts/playground.sh --help` for full usage.

### `scripts/blitzreels.sh`
Generic API helper for ad-hoc calls.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BLITZREELS_API_KEY` | Yes | API key |
| `BLITZREELS_API_BASE_URL` | No | Override base URL |
| `BLITZREELS_ALLOW_EXPENSIVE` | No | Set to `1` for export calls via blitzreels.sh |

## API Endpoints

### Playground Compositions
| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects/{id}/playground/presets` | List preset templates |
| GET | `/projects/{id}/playground/compositions` | List compositions |
| POST | `/projects/{id}/playground/compositions` | Create composition |
| GET | `/projects/{id}/playground/compositions/{cid}` | Get composition |
| PATCH | `/projects/{id}/playground/compositions/{cid}` | Update composition |
| DELETE | `/projects/{id}/playground/compositions/{cid}` | Delete composition |

### Element-Level Operations
| Method | Path | Description |
|--------|------|-------------|
| PATCH | `/projects/{id}/playground/compositions/{cid}/elements/{eid}` | Update single element |
| DELETE | `/projects/{id}/playground/compositions/{cid}/elements/{eid}` | Delete element |

### Project Operations
| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects` | Create project |
| POST | `/projects/{id}/export` | Start export (expensive) |
| GET | `/exports/{export_id}` | Get export status + download URL |

## Composition Spec

The composition JSON spec defines the canvas, elements, and animations. See `references/composition-spec.md` for the full schema.

### Minimal Example
```json
{
  "name": "Title Card",
  "fps": 30,
  "width": 1920,
  "height": 1080,
  "durationInFrames": 150,
  "background": "#1a1a2e",
  "mode": "elements",
  "elements": [
    {
      "id": "title",
      "type": "text",
      "content": "Hello World",
      "from": 0,
      "durationInFrames": 150,
      "style": {
        "fontSize": 96,
        "fontWeight": "bold",
        "color": "#ffffff",
        "opacity": {
          "keyframes": [
            { "frame": 0, "value": 0 },
            { "frame": 30, "value": 1 }
          ]
        }
      }
    }
  ]
}
```

### Element Types
| Type | Description |
|------|-------------|
| `text` | Text with typewriter, highlight effects |
| `shape` | Rectangle, circle, ellipse, line, arrow, polygon, star |
| `image` | Static image with optional Ken Burns effect |
| `video` | Video clip with volume, loop, playback control |
| `audio` | Audio track |
| `chart` | Bar, pie, line, area, donut charts with animated reveal |
| `code` | Syntax-highlighted code with line-by-line reveal |
| `svg` | SVG with path draw/morph animations |
| `group` | Container for child elements (parallel or series) |
| `lottie` | Lottie animation from JSON or URL |

### Animation Options
- **Static values**: `"opacity": 1`
- **Keyframes**: Frame-by-frame with easing
- **Spring physics**: `smooth`, `snappy`, `bouncy`, `heavy`, `gentle` presets
- **Easing**: `linear`, `easeIn`, `easeOut`, `easeInOut`, elastic, bounce, bezier

### Scene Transitions (scenes mode)
`fade`, `slide`, `wipe`, `flip`, `clockWipe` — with directional variants.

## Timeline & Overlay Editing

For editing existing video projects (not playground compositions), use these endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects/{id}/context?mode=timeline` | Get project timeline |
| POST | `/projects/{id}/overlays` | Add text/image overlay |
| PATCH | `/projects/{id}/overlays/{oid}` | Update overlay |
| DELETE | `/projects/{id}/overlays/{oid}` | Remove overlay |
| POST | `/projects/{id}/captions` | Add/update captions |
| PATCH | `/projects/{id}/captions/style` | Update caption style |

## References

- `references/composition-spec.md` — Full composition JSON schema, element types, animation format, spring presets, transitions

## Notes

- Use `https://www.blitzreels.com/api/v1` as your base URL. `https://blitzreels.com` redirects to `www`, and some HTTP clients drop the `Authorization` header on redirects.
- When animating, prefer the smallest number of keyframes that communicates the motion (reduces jitter).
- Full OpenAPI spec: `https://www.blitzreels.com/api/openapi.json`

## Rate Limits

| Plan | Requests/min |
|------|-------------|
| Free | 10 |
| Creator | 30 |
| Pro | 60 |
| Agency | 120 |
