---
name: image-extend
description: Extends an image canvas by adding padding on all sides with a solid background color. Use when you need to add borders, margins, or expand the canvas area around an image.
---

# Image Extend

Extends an image canvas by adding padding on all sides with a solid background color.

## Command

```bash
agent-media image extend --in <path> --padding <pixels> --color <hex> [options]
```

## Inputs

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input file path or URL |
| `--padding` | Yes | Padding size in pixels to add on all sides |
| `--color` | Yes | Background color for extended area (hex, e.g., "#FFFFFF"). Also flattens transparency. |
| `--dpi` | No | DPI/density for output image (default: 300) |
| `--out` | No | Output path, filename or directory (default: ./) |

## Output

Returns a JSON object with the extended image path:

```json
{
  "ok": true,
  "media_type": "image",
  "action": "extend",
  "provider": "local",
  "output_path": "extended_123_abc.png",
  "mime": "image/png",
  "bytes": 234567
}
```

## Examples

Add white padding around an image:
```bash
agent-media image extend --in photo.jpg --padding 50 --color "#FFFFFF"
```

Add colored border:
```bash
agent-media image extend --in artwork.png --padding 100 --color "#E4ECF8"
```

Extend with custom DPI:
```bash
agent-media image extend --in print-ready.jpg --padding 75 --color "#000000" --dpi 600
```

## Providers

This action uses local processing only:
- **local** - No API key required (uses Sharp)
