---
name: Segment Image
description: This skill should be used when the user asks to "segment an image", "identify objects", "extract objects", "generate masks", "find objects in image", or needs AI-powered image segmentation.
---

# Segment Image

Segment and identify objects in images using Gemini's vision capabilities.

## When to Use

Use this skill when the user asks to:
- Identify objects in an image
- Generate masks for specific objects
- Segment an image into regions
- Extract objects from an image

## Usage

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/segment-image && bun run scripts/segment.ts <input-image> [options]
```

### Options

- `--prompt <text>` - Custom segmentation prompt
- `--output <dir>` - Output directory for mask files

### Examples

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/segment-image

# Segment all objects
bun run scripts/segment.ts photo.jpg

# Segment with custom prompt
bun run scripts/segment.ts photo.jpg --prompt "identify all people and vehicles"

# Save masks to directory
bun run scripts/segment.ts photo.jpg --output ./masks
```

## Model

Uses `gemini-3-pro-preview` for image segmentation.
