---
name: image-remove-background
description: Removes the background from an image, leaving the foreground subject with transparency. Use when you need to isolate subjects, create cutouts, or prepare images for compositing.
---

# Image Remove Background

Removes the background from an image, leaving only the foreground subject with transparency.

## Command

```bash
agent-media image remove-background --in <path> [options]
```

## Inputs

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input file path or URL |
| `--out` | No | Output path, filename or directory (default: ./) |
| `--provider` | No | Provider to use (local, fal, replicate) |

## Output

Returns a JSON object with the processed image path:

```json
{
  "ok": true,
  "media_type": "image",
  "action": "remove-background",
  "provider": "fal",
  "output_path": "nobg_123_abc.png",
  "mime": "image/png",
  "bytes": 34567
}
```

## Examples

Remove background from local file:
```bash
agent-media image remove-background --in portrait.jpg
```

Remove background using specific provider:
```bash
agent-media image remove-background --in portrait.jpg --provider replicate
```

## Providers

### local

Runs locally on CPU using [Transformers.js](https://huggingface.co/docs/transformers.js), no API key required.

- Uses `Xenova/modnet` model
- Models downloaded on first use (~25MB)
- You may see a `mutex lock failed` error — ignore it, the output is correct if `"ok": true`

```bash
agent-media image remove-background --in portrait.jpg --provider local
```

### fal

- Requires `FAL_API_KEY`
- Uses `birefnet/v2` model

### replicate

- Requires `REPLICATE_API_TOKEN`
- Uses `birefnet` model
