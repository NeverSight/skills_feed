---
name: image-resize
description: Resizes an image to specified dimensions. Use when you need to change image size, create thumbnails, or prepare images for specific display requirements.
---

# Image Resize

Resizes an image to a target width or height while optionally maintaining aspect ratio.

## Command

```bash
agent-media image resize --in <path> [options]
```

## Inputs

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input file path or URL |
| `--width` | No | Target width in pixels |
| `--height` | No | Target height in pixels |
| `--out` | No | Output path, filename or directory (default: ./) |
| `--provider` | No | Provider to use (default: auto-detect) |

At least one of `--width` or `--height` must be specified.

## Output

Returns a JSON object with the resized image path:

```json
{
  "ok": true,
  "media_type": "image",
  "action": "resize",
  "provider": "local",
  "output_path": "resized_123_abc.png",
  "mime": "image/png",
  "bytes": 45678
}
```

## Examples

Resize to 800px width:
```bash
agent-media image resize --in photo.jpg --width 800
```

Resize to exact dimensions:
```bash
agent-media image resize --in photo.jpg --width 1024 --height 768
```

Resize with custom output:
```bash
agent-media image resize --in image.png --width 500 --out ./resized
```

## Providers

- **local** (default) - Uses sharp library, no API key required
