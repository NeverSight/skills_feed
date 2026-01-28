---
name: video-generate
description: Generates video from text prompts or animates static images. Use when you need to create videos from descriptions, animate images, or produce video content using AI.
---

# Video Generate

Generates a video from a text prompt using AI video generation models. Supports both text-to-video and image-to-video (animating a static image).

## Command

```bash
agent-media video generate --prompt <text> [options]
```

## Inputs

| Option | Required | Description |
|--------|----------|-------------|
| `--prompt` | Yes | Text description of the video to generate |
| `--in` | No | Input image path or URL for image-to-video |
| `--duration` | No | Duration in seconds (6, 8, 10, 12, 14, 16, 18, 20; default: 6) |
| `--resolution` | No | Video resolution (720p, 1080p, 1440p, 2160p; default: 720p) |
| `--fps` | No | Frame rate (25 or 50; default: 25) |
| `--audio` | No | Generate audio track |
| `--out` | No | Output path, filename or directory (default: ./) |
| `--provider` | No | Provider to use (default: auto-detect) |
| `--model` | No | Model to use (overrides provider default) |

## Output

Returns a JSON object with the generated video path:

```json
{
  "ok": true,
  "media_type": "video",
  "action": "video-generate",
  "provider": "fal",
  "output_path": "generated_abc123.mp4",
  "mime": "video/mp4",
  "bytes": 12345678
}
```

## Examples

Generate a video from text:
```bash
agent-media video generate --prompt "a cat walking in a garden"
```

Generate a longer video with higher resolution:
```bash
agent-media video generate --prompt "ocean waves crashing on a beach" --duration 10 --resolution 1080p
```

Animate an existing image (image-to-video):
```bash
agent-media video generate --in portrait.png --prompt "the person waves hello and smiles"
```

Generate with audio:
```bash
agent-media video generate --prompt "fireworks exploding in the night sky" --audio
```

Use a specific provider:
```bash
agent-media video generate --prompt "a rocket launching" --provider replicate
```

## Providers

This action requires an external provider:
- **fal** - Requires `FAL_API_KEY` (uses LTX-2 model)
- **replicate** - Requires `REPLICATE_API_TOKEN` (uses lightricks/ltx-video model)

The local provider does not support video generation.
