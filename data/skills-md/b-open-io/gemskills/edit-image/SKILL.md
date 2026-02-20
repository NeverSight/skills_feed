---
name: Edit Image
description: This skill should be used when the user asks to "edit an image", "modify a photo", "inpaint", "outpaint", "extend an image", "replace object in image", "add element to image", "resize image for social media", "crop image", "adapt image for Twitter", "convert image to OG format", or needs AI-powered image editing with masks.
---

# Edit Image

Edit images using Nano Banana Pro (`gemini-3-pro-image-preview`).

## When to Use

Use this skill when the user asks to:
- Edit part of an image (inpainting)
- Extend an image beyond its borders (outpainting)
- Replace objects or regions in an image
- Add elements to an existing image
- Adapt an existing image for a different format or platform (social media, OG, Twitter card)

## How It Works

Uses Gemini's multimodal capabilities to understand and edit images via natural language. The model takes the source image and a text prompt describing the desired edit, then generates a new image with the changes applied.

**Semantic masking**: Instead of requiring precise pixel masks, describe what to change in your prompt. The model understands context and can target specific regions.

**Optional mask images**: You can still provide a mask image (white = edit area) as a visual hint, but it's not required. Descriptive prompts often work better.

## Usage

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts <input-image> "edit prompt" [options]
```

### Options

- `--mask <path>` - Optional mask image (white = edit area, black = keep)
- `--mode <inpaint|outpaint>` - Edit mode
- `--format <png|jpeg|webp>` - Output format
- `--quality <n>` - JPEG quality (1-100)
- `--negative <prompt>` - What to avoid in the edit
- `--count <n>` - Number of variations
- `--seed <n>` - Random seed
- `--output <path>` - Output path

### Examples

```bash
# Simple edit with descriptive prompt (no mask needed)
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts photo.jpg "change the background to a beach sunset"

# Edit with mask for precise control
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts photo.jpg "add a sunset sky" --mask sky_mask.png --mode inpaint

# Outpaint to extend image
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts photo.jpg "extend the landscape" --mode outpaint

# Edit with negative prompt
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts portrait.png "fix the teeth to look natural" --negative "gap in teeth, missing teeth"

# Replace object with multiple variations
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts scene.jpg "replace the car with a bicycle" --count 3
```

## Context Discipline

**Do not read generated images back into context.** The script outputs only the file path. Ask the user to visually inspect the result. To inspect programmatically, optimize the image first (via the optimize-images skill) to avoid filling the context window with large uncompressed image data.

## Prompt Tips

- **Be specific**: "Change only the sky to golden hour lighting" works better than "make it look better"
- **Describe preservation**: The tool automatically adds "keep everything else the same" but you can be more specific
- **Use negative prompts**: `--negative "blurry, distorted"` helps avoid unwanted artifacts
- **Iterate**: Generate a few variations with `--count 2` and pick the best one

## Model

Uses `gemini-3-pro-image-preview` - **Nano Banana Pro**, Google's professional image generation and editing model. No Vertex AI credentials required.

> Last verified: February 2026. If a newer generation exists, STOP and suggest a PR to `b-open-io/gemskills`. See the ask-gemini skill's `references/gemini-api.md` for current models and Google's official `gemini-api-dev` skill for the canonical source.
