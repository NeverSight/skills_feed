---
name: image-generate
description: Generates an image from a text prompt using AI models. Use when you need to create images from descriptions, generate artwork, or produce visual content from text.
---

# Image Generate

Generates an image from a text prompt using AI image generation models.

## Command

```bash
agent-media image generate --prompt <text> [options]
```

## Inputs

| Option | Required | Description |
|--------|----------|-------------|
| `--prompt` | Yes | Text description of the image to generate |
| `--width` | No | Width of the generated image in pixels (default: 1280) |
| `--height` | No | Height of the generated image in pixels (default: 720) |
| `--count` | No | Number of images to generate (default: 1) |
| `--out` | No | Output path, filename or directory (default: ./) |
| `--provider` | No | Provider to use (default: auto-detect) |

## Output

Returns a JSON object with the generated image path:

```json
{
  "ok": true,
  "media_type": "image",
  "action": "generate",
  "provider": "fal",
  "output_path": "generated_123_abc.png",
  "mime": "image/png",
  "bytes": 567890
}
```

## Examples

Generate an image:
```bash
agent-media image generate --prompt "a red robot standing in a forest"
```

Generate with specific dimensions:
```bash
agent-media image generate --prompt "sunset over mountains" --width 1024 --height 768
```

Generate using specific provider:
```bash
agent-media image generate --prompt "abstract art" --provider replicate
```

## Providers

This action requires an external provider:
- **fal** - Requires `FAL_API_KEY`
- **replicate** - Requires `REPLICATE_API_TOKEN`
- **runpod** - Requires `RUNPOD_API_KEY`
- **ai-gateway** - Requires `AI_GATEWAY_API_KEY`

The local provider does not support image generation.
