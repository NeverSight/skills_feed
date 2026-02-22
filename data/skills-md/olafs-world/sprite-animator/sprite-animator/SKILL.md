---
name: sprite-animator
description: Generate animated pixel art sprite GIFs from any image using AI (Gemini). Use when the user wants to create pixel art animations, sprite sheets, animated character GIFs, or convert photos/drawings into retro game-style animated sprites. Supports idle, wave, bounce, and dance animations.
license: MIT
metadata:
  author: Olafs-World
  version: "0.2.1"
---

# Sprite Animator

Turn any image into an animated pixel art sprite GIF. Uses Gemini image generation to create 16-frame sprite sheets, then assembles them into looping GIFs.

## Requirements

- `GEMINI_API_KEY` or `GOOGLE_API_KEY` env var must be set
- Install: `uv tool install sprite-animator` (or `uvx sprite-animator` for one-off runs)

## Quick Usage

```bash
# Best quality for photos — two-step converts to pixel art first, then animates
sprite-animator -i photo.png -o dance.gif -a dance --two-step -s 256 -r 2K

# From drawings or pixel art (single step is fine)
sprite-animator -i drawing.png -o idle.gif -a idle -s 256 -r 2K
```

## Animation Types

- `idle` — gentle breathing + blink (default)
- `wave` — arm raise → wave → return
- `bounce` — crouch → jump → land
- `dance` — lean, spin, jump — full party mode

## Key Options

| Flag | Description | Default |
|------|-------------|---------|
| `-i` | Input image path | required |
| `-o` | Output GIF path | required |
| `-a` | Animation type (idle/wave/bounce/dance) | idle |
| `-s` | Output sprite size in px | 128 |
| `-r` | Generation resolution (1K/2K) | 1K |
| `-d` | Frame duration in ms | 100 |
| `--two-step` | Pixelate first, then animate (better for photos) | off |
| `--keep-sheet` | Save raw sprite sheet | off |
| `--keep-frames` | Save individual frame PNGs | off |

## Tips

- Use `--two-step` for photos of real people — Gemini loses likeness otherwise
- Use `-r 2K` for noticeably better quality
- Use `-d 180` for more natural playback speed (default 100ms is fast)
- Save good base pixel art sprites and reuse them for different animations
- On Telegram, send GIFs as documents to avoid MP4 conversion

## Python API

```python
from pathlib import Path
from PIL import Image
from sprite_animator.cli import ANIMATION_PRESETS, generate_sprite_sheet, create_gif, call_gemini, get_api_key
from sprite_animator.template import create_template, extract_frames

api_key = get_api_key()
preset = ANIMATION_PRESETS["dance"]

# Create template and generate sprite sheet
template = create_template(cols=4, rows=4, labels=preset["labels"])
template.save("template.png")

generate_sprite_sheet(
    api_key=api_key,
    input_image=Image.open("input.png"),
    template_path=Path("template.png"),
    output_path=Path("sheet.png"),
    prompt=preset["prompt"],
    resolution="2K",
)

# Extract frames and build GIF
frames = extract_frames(Image.open("sheet.png"), cols=4, rows=4)
create_gif(frames, Path("output.gif"), frame_duration=180, size=256)
```
