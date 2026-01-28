---
name: picasso
description: Generate visual assets (favicons, icons, logos, game sprites, UI elements) using fal.ai image generation. Triggers on "generate icon", "create favicon", "make logo", "create sprite", "generate asset", "picasso".
---

# Picasso

Generate production-ready visual assets via fal.ai API.

## Design Philosophy

Commit to a BOLD aesthetic direction—no generic AI slop:
- Choose distinctive, memorable visual concepts over safe defaults
- Use intentional, purposeful compositions that feel genuinely designed
- Avoid overused patterns: gradient text, neon-on-dark, glassmorphism clichés

## Prerequisites

```bash
command -v bun ffmpeg convert 2>/dev/null | xargs -I{} basename {} || echo "Missing deps"
```

Required: `bun`, `FAL_API_KEY` in `.env`. Optional: `ffmpeg` (video/gif), `convert` (ImageMagick).

## Quick Start

```bash
bun scripts/fal-generate.ts "minimalist letter A logo, flat design" --size square --out favicon.png
bun scripts/fal-generate.ts "mobile app icon, weather app" --num 4
bun scripts/fal-generate.ts "pixel art sword, transparent background" --format png
```

## Script Usage

```
Usage: bun fal-generate.ts <prompt> [options]

Options:
  --model <id>        fal.ai model endpoint (see Model Selection below)
  --size <size>       Size: square, landscape_4_3, portrait_4_3, etc.
  --num <n>           Number of images 1-4
  --format <fmt>      png, jpeg, webp
  --out <path>        Save first image to file
  --edit <url>        Image URL for editing (can be repeated)
  --resolution <res>  Edit output resolution: 1K, 2K, 4K
```

## Model Selection & Cost Efficiency

→ *Consult [models reference](reference/models.md) for discovery commands and selection criteria.*

### Strategy: Cheap iterations, quality finals

1. **Explore with fast/cheap models** — most generations get discarded
2. **Upgrade for final output only** — when quality is the deliverable
3. **Post-process instead of regenerate** — ImageMagick is free

```bash
# Discover available models
curl -s "https://api.fal.ai/v1/models?category=text-to-image&status=active" \
  -H "Authorization: Key $FAL_API_KEY" | jq '.models[] | {id: .endpoint_id, name: .metadata.display_name}'

# Search by capability
curl -s "https://api.fal.ai/v1/models?q=fast" -H "Authorization: Key $FAL_API_KEY"
```

### When to use what

| Phase | Model Tier | Why |
|-------|------------|-----|
| Concept exploration | Fast/cheap | Many iterations, most discarded |
| Sprites, icons, UI | Fast/cheap | Gets post-processed anyway |
| Final brand assets | Standard/Pro | Quality visible in deliverable |
| Print/marketing | Pro | Quality is the product |

Browse models: https://fal.ai/models

## Prompting Fundamentals

→ *Consult [image generation reference](reference/image-generation.md) for complete prompt engineering guide.*

**Prompt structure:** `Subject + Style/Medium + Lighting + Composition + Color/Mood`

```bash
# Well-structured prompt
bun scripts/fal-generate.ts "portrait of a barista, film photo, soft rim light, 50mm close-up, warm mood, teal-orange palette"
```

**DO**: Be specific about subject, lighting, camera, mood
**DON'T**: Use vague terms like "cool" or "nice"

## Image Editing

→ *Consult [image editing reference](reference/image-editing.md) for inpainting, outpainting, and compositing.*

Edit existing images with `--edit`. The script auto-selects appropriate edit endpoint.

```bash
# Inpainting (edit within image)
bun scripts/fal-generate.ts "replace the red car with a blue motorcycle" --edit photo.png

# Outpainting (extend image)
bun scripts/fal-generate.ts "extend to landscape, continue the forest background" --edit portrait.png

# Compositing (combine images)
bun scripts/fal-generate.ts "put the person from first image into the scene from second" \
  --edit person.png --edit background.png
```

**Edit tips:**
- Be specific about what to change AND what to preserve
- Describe spatial relationships: "add a cat sitting on the left"
- Reference image order matters: first = subject, second = context/style

## Mockups

→ *Consult [mockups reference](reference/mockups.md) for device, product, and presentation mockups.*

Generate realistic product presentations:

```bash
# Device mockup
bun scripts/fal-generate.ts "iPhone on wooden desk, app interface on screen, coffee shop setting, shallow depth of field"

# Product mockup
bun scripts/fal-generate.ts "t-shirt on hanger, front view, neutral background, soft studio lighting"

# Two-step for exact screen content
bun scripts/fal-generate.ts "phone mockup, blank screen, lifestyle setting" --out base.png
bun scripts/fal-generate.ts "place this screenshot on the phone screen" --edit base.png --edit my_screenshot.png
```

## Asset Type Quick Reference

| Asset Type | Key Prompt Elements | Reference |
|------------|---------------------|-----------|
| **General Images** | Subject + style + lighting + composition + mood | [reference/image-generation.md](reference/image-generation.md) |
| **Favicons & App Icons** | "flat design", "minimalist", "single object centered", "no text" | [reference/icons-favicons.md](reference/icons-favicons.md) |
| **Logos** | "vector style", "clean lines", "logo design", "monochrome" | [reference/brand-assets.md](reference/brand-assets.md) |
| **Game Sprites** | "pixel art", "transparent background", "32x32 style" | [reference/game-assets.md](reference/game-assets.md) |
| **Spritesheets** | Generate frames individually, combine with ImageMagick | [reference/game-assets.md](reference/game-assets.md) |
| **Tilesets** | "seamless", "tileable", "flat lighting" | [reference/game-assets.md](reference/game-assets.md) |
| **UI Icons** | "UI icon", "glyph", "outlined", "material design style" | [reference/icons-favicons.md](reference/icons-favicons.md) |
| **Marketing Images** | "hero image", style consistency via `--edit` | [reference/brand-assets.md](reference/brand-assets.md) |
| **Photo Edits** | Inpainting, outpainting, compositing, style transfer | [reference/image-editing.md](reference/image-editing.md) |
| **Mockups** | Device, product, presentation with environment context | [reference/mockups.md](reference/mockups.md) |

## Detailed Guides

**Core:**
- **[Image Generation](reference/image-generation.md)** - Prompt structure, lighting, composition, style
- **[Image Editing](reference/image-editing.md)** - Inpainting, outpainting, compositing
- **[Models](reference/models.md)** - Model discovery, selection criteria, cost/quality tradeoffs

**Asset-Specific:**
- **[Game Assets](reference/game-assets.md)** - Spritesheets, pixel art, tilesets, character rotations
- **[Icons & Favicons](reference/icons-favicons.md)** - Size requirements, platform guidelines
- **[Brand Assets](reference/brand-assets.md)** - Logos, marketing imagery, style consistency
- **[Mockups](reference/mockups.md)** - Device, product, and presentation mockups

## Post-Processing (ImageMagick)

```bash
# Resize for favicon
convert logo.png -resize 32x32 favicon.ico
convert logo.png -resize 180x180 apple-touch-icon.png

# Remove background
convert logo.png -fuzz 10% -transparent white transparent.png

# Create spritesheet from frames
montage frame*.png -tile 8x1 -geometry +0+0 -background none spritesheet.png

# Nearest-neighbor resize (pixel art)
convert sprite.png -filter point -resize 64x64 sprite_2x.png

# Batch uniform sizing
for f in frame*.png; do convert "$f" -gravity center -extent 64x64 "fixed_$f"; done
```

## Post-Processing (ffmpeg)

```bash
# PNG sequence to GIF
ffmpeg -framerate 10 -i frame_%03d.png -loop 0 animation.gif

# Video to GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1" output.gif
```

## Example Workflow

```bash
# 1. Discover suitable models
curl -s "https://api.fal.ai/v1/models?q=logo&category=text-to-image" \
  -H "Authorization: Key $FAL_API_KEY" | jq '.models[0:3] | .[].endpoint_id'

# 2. Generate logo concepts (use fast model for exploration)
bun scripts/fal-generate.ts "modern tech startup logo, geometric, blue" --num 4

# 3. Refine chosen concept
bun scripts/fal-generate.ts "minimalist geometric logo, blue" --size square --out logo.png

# 4. Create favicon set
convert logo.png -resize 32x32 favicon.ico
convert logo.png -resize 180x180 apple-touch-icon.png
```
