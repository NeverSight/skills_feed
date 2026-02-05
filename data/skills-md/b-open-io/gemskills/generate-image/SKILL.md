---
name: Generate Image
description: This skill should be used when the user asks to "generate an image", "create a banner", "make artwork", "create an illustration", "generate a logo", "make a graphic", "design a header", "AI art", "img2img", or needs AI image generation. Handles prompt rewriting and Gemini 3 Pro image generation API calls.
---

# Generate Image

Generate images using Gemini 3 Pro image generation (`gemini-3-pro-image-preview`).

## When to Use

Use this skill when the user asks to:
- Generate an image from a text prompt
- Create artwork, illustrations, or graphics
- Generate variations of an existing image (img2img)
- Create scenes with multiple reference images (character + location + other characters)

## Gather Design Direction First

**Ask clarifying questions before rewriting prompts** to understand the user's intent:

1. **Purpose**: What is the image for? (banner, logo, social media, product shot, art piece)
2. **Style preference**: Photorealistic, illustrated, minimalist, abstract, specific art style?
3. **Color palette**: Any brand colors? Dark/light theme? Specific mood?
4. **Composition constraints**: Aspect ratio needs? Text overlay space? Full-bleed vs bordered?
5. **Key elements**: What must be included? What should be avoided?

Simple requests like "make a cat image" can proceed with sensible defaults. Complex requests like "create a banner for my app" require clarification to avoid iteration waste.

## Prompt Rewriting (Critical)

**Before generating any image, always rewrite the user's prompt** using the guide in `references/prompt-guide.md`.

The core principle: **"Describe the scene, don't just list keywords."**

### Rewriting Checklist

Transform simple prompts by adding:
1. **Subject details**: Specific appearance, clothing, expression, materials
2. **Environment/Setting**: Location, time of day, weather, indoor/outdoor
3. **Lighting**: Natural/artificial, direction, quality, color temperature
4. **Composition**: Camera angle, distance, framing, focal length
5. **Style/Aesthetic**: Photorealistic, illustration style, art movement
6. **Mood/Atmosphere**: Emotional tone, color palette mood
7. **Technical specs**: Aspect ratio, level of detail, textures

### Example Transformation

**User says**: "banner for my app"
**Rewritten prompt**: "A modern, full-bleed banner for a technology application. Dark gradient background transitioning from deep navy to black. Abstract geometric network visualization with glowing nodes connected by thin lines. Clean sans-serif typography positioned left of center. Professional, tech-forward aesthetic with no visible borders or edges - the design extends seamlessly to all edges. 16:9 aspect ratio."

**User says**: "a cat"
**Rewritten prompt**: "A fluffy orange tabby cat lounging on a sun-drenched windowsill, soft afternoon light creating a warm glow on its fur. The cat is in a relaxed pose with half-closed eyes, conveying contentment. Shot from a low angle with shallow depth of field, the background showing a blurred garden view. Photorealistic, warm color palette."

## Recommended Workflow

**Draft → Iterate → Final** approach saves time and API costs:

1. **Draft Phase (1K)**: Generate quickly at default resolution to test prompts
2. **Iteration Phase**: Refine prompts incrementally, creating new files each attempt
3. **Final Phase (4K)**: Only produce high-res output after prompt is validated

**Do not read the image back** - the script outputs only the file path. This allows efficient iteration without Claude loading large image data.

## Usage

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/generate-image && bun run scripts/generate.ts "prompt" [options]
```

### Options

- `--input <path>` - Reference image (can specify multiple times, up to 14 images)
- `--style <id>` - Apply style from the style library (see browsing-styles skill)
- `--size <1K|2K|4K>` - Image size (default: 1K for fast drafts)
- `--aspect <ratio>` - Aspect ratio: 1:1, 16:9, 9:16, 4:3, 3:4
- `--negative <prompt>` - Negative prompt (what to avoid)
- `--count <n>` - Number of images (1-4, default: 1)
- `--guidance <n>` - Guidance scale
- `--seed <n>` - Random seed for reproducibility
- `--output <path>` - Output path

### Examples

```bash
# Simple generation
bun run scripts/generate.ts "cyberpunk cityscape at night"

# With art style (100+ available, use short names or full IDs)
bun run scripts/generate.ts "mountain landscape" --style impressionism
bun run scripts/generate.ts "portrait" --style ukiy
bun run scripts/generate.ts "city street" --style noir

# High-res with specific aspect ratio
bun run scripts/generate.ts "mountain landscape" --size 4K --aspect 16:9

# With negative prompt
bun run scripts/generate.ts "portrait of a cat" --negative "low quality, blurry"

# Combine style with other options
bun run scripts/generate.ts "cat sleeping" --style wtrc --size 4K --aspect 1:1

# Generate multiple variations
bun run scripts/generate.ts "abstract art" --count 4

# Single reference image (img2img)
bun run scripts/generate.ts "make it look like a watercolor painting" --input photo.jpg

# Multiple reference images (character consistency, scene composition)
bun run scripts/generate.ts "King on throne in dramatic lighting" \
  --input character.png \
  --input throne-room.png \
  --aspect 16:9 --size 2K

# Multiple characters in a scene
bun run scripts/generate.ts "Two warriors facing each other in combat" \
  --input warrior1.png \
  --input warrior2.png \
  --input battlefield.png \
  --aspect 16:9
```

## Multiple Reference Images

Gemini supports up to 14 reference images per request:
- **6 objects** - Locations, items, environments
- **5 humans** - Character consistency across generations
- Use detailed prompts describing how reference images should be combined
- Reference images help maintain consistency across scene generations

## Available Styles

Use the `browsing-styles` skill to browse all 100+ styles:
- `bun run ../browsing-styles/scripts/preview_server.ts` - Interactive browser
- `bun run ../browsing-styles/scripts/list_styles.ts --table` - CLI list

Popular styles: `impr` (Impressionism), `ukiy` (Ukiyo-e), `cybr` (Cyberpunk), `pixl` (Pixel Art), `noir` (Film Noir), `anim` (Anime), `wtrc` (Watercolor)

## Model

Uses `gemini-3-pro-image-preview` (Gemini 3 Pro) for image generation.

## Reference Files

For detailed prompting strategies and techniques:
- **`references/prompt-guide.md`** - Comprehensive Gemini prompting guide with 7 strategies, example transformations, and best practices from Google's official documentation
