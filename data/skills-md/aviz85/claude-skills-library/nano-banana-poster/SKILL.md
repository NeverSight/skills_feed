---
name: nano-banana-poster
description: "Generate images and posters with Google Gemini. Use for: create image, generate visual, AI image generation, marketing poster."
version: "1.0.0"
author: aviz85
tags:
  - image-generation
  - ai
  - gemini
  - poster
  - visual
setup: "./SETUP.md"
---

# Nano Banana Poster Generator

Generate images using Google's Gemini model with optional reference assets.

## Quick Start

```bash
cd ~/.claude/skills/nano-banana-image/scripts

# Basic generation (default 3:2 horizontal)
npx ts-node generate_poster.ts "A futuristic city at sunset"

# With aspect ratio (3:2 horizontal, 2:3 vertical, 16:9 wide, 9:16 tall)
npx ts-node generate_poster.ts --aspect 3:2 "A wide landscape poster"
npx ts-node generate_poster.ts -a 9:16 "A vertical story format"

# With reference assets
npx ts-node generate_poster.ts --assets "my-logo" "Create banner with logo"

# Combined: aspect ratio + assets
npx ts-node generate_poster.ts --aspect 16:9 --assets "logo" "YouTube thumbnail"
```

## Aspect Ratio

**IMPORTANT:** Always use the default 3:2 aspect ratio unless the user explicitly requests a different format (like "vertical", "story", "square", etc.). Do NOT change the aspect ratio on your own.

Control image dimensions with `--aspect` or `-a`:

| Ratio | Use Case |
|-------|----------|
| `3:2` | Horizontal **(DEFAULT - use this unless user specifies otherwise)** |
| `1:1` | Square - Instagram, profile pics |
| `2:3` | Vertical - Pinterest, posters |
| `16:9` | Wide - YouTube thumbnails, headers |
| `9:16` | Tall - Stories, reels, TikTok |

```bash
npx ts-node generate_poster.ts --aspect 3:2 "Your prompt"
npx ts-node generate_poster.ts -a 16:9 "Your prompt"
```

## Adding Assets

Use `--assets` with full paths to include reference images:

```bash
# Single asset
npx ts-node generate_poster.ts --assets "/full/path/to/image.jpg" "Your prompt"

# Multiple assets (comma-separated)
npx ts-node generate_poster.ts --assets "/path/a.jpg,/path/b.png" "Use both images"
```

**Supported formats:** `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`

**IMPORTANT:** Assets are NOT automatically included. You must explicitly pass them via `--assets`.

## Save to Gallery

Save good results for future style reference:

```bash
npx ts-node generate_poster.ts --save-to-gallery "my-style" "prompt"
```

Creates `assets/gallery/my-style.jpg` + `.meta.json` with prompt info.

## API Configuration

Create `scripts/.env`:
```
GEMINI_API_KEY=your_api_key_here
```

## Hebrew/RTL Content

When generating images with Hebrew text:

**ALWAYS include in prompt:**
```
CRITICAL: All text must be in Hebrew.
CRITICAL: Layout direction is RTL (right-to-left).
Flow, reading order, and visual hierarchy must go from RIGHT to LEFT.
```

This ensures text renders correctly and visual flow matches Hebrew reading direction.

## Output

- Files saved as `poster_0.jpg`, `poster_1.jpg`, etc.
- Aspect ratio: Configurable via `--aspect` (default: 3:2)
- Quality: 1K (1024px on longest edge)
