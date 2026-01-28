---
name: image-crop
description: Crops an image to specified dimensions around a focal point. Use when you need to extract a portion of an image, create thumbnails with custom positioning, or prepare images for specific aspect ratios.
---

# Image Crop

Crops an image to specified dimensions centered on a configurable focal point. The crop region is calculated to center on the focal point while staying within image bounds.

## Command

```bash
agent-media image crop --in <path> --width <px> --height <px> [options]
```

## Inputs

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input file path or URL |
| `--width` | Yes | Width of crop area in pixels |
| `--height` | Yes | Height of crop area in pixels |
| `--focus-x` | No | Focal point X position 0-100 (default: 50 = center) |
| `--focus-y` | No | Focal point Y position 0-100 (default: 50 = center) |
| `--dpi` | No | DPI/density for output (default: 300) |
| `--out` | No | Output path, filename or directory (default: ./) |
| `--provider` | No | Provider to use (default: local) |

## Output

Returns a JSON object with the cropped image path:

```json
{
  "ok": true,
  "media_type": "image",
  "action": "crop",
  "provider": "local",
  "output_path": "cropped_123_abc.png",
  "mime": "image/png",
  "bytes": 45678
}
```

## Examples

Crop to 800x600 centered (default focal point):
```bash
agent-media image crop --in photo.jpg --width 800 --height 600
```

Crop with focal point at top-left area (20% from left, 30% from top):
```bash
agent-media image crop --in photo.jpg --width 800 --height 600 --focus-x 20 --focus-y 30
```

Crop from URL with custom output:
```bash
agent-media image crop --in https://example.com/image.jpg --width 1024 --height 768 --out ./output
```

## Providers

- **local** (default) - Uses Sharp library, no API key required
