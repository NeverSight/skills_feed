---
name: Pixel Avatar
description: This skill should be used when the user asks to "create a pixel art avatar", "generate pixel portrait", "make a pixel character", "convert photo to pixel art", "team member avatar", "Amiga-style portrait", or needs pixel art profile images that retain likeness to a source photo.
---

# Pixel Avatar

Generate pixel art avatars from reference photos using Gemini image generation, maintaining recognizable likeness while achieving a stylized pixel aesthetic.

## When to Use

Use this skill when the user asks to:
- Create pixel art avatars from photos
- Generate team member profile images in pixel art style
- Convert headshots to Amiga-era pixel portraits
- Create consistent pixel art characters that resemble real people

## Core Principles

### Balance Likeness and Style

The critical challenge is achieving BOTH:
1. **Recognizable likeness** - Must look like the source person
2. **Pixel art aesthetic** - Stylized, not photorealistic

Common failures:
- Too photorealistic = pixelated photo filter effect
- Too stylized = loses resemblance to source person

### Single Source Input

Use ONLY the subject's photo as input. Never use another person's image as a style reference - this causes face blending and loss of likeness.

## Prompt Template

```
Generate a pixel art avatar from the reference photo.

## INPUT IMAGE
[path to subject's photo] - USE ONLY THIS IMAGE

## CRITICAL: LIKENESS PRESERVATION
Capture the subject's EXACT features from the photo:
- Face shape and jawline
- Eye shape, spacing, and expression
- Nose shape and size
- Mouth/smile characteristics
- Hair texture, color, and style
- Facial hair pattern and coverage (if applicable)
The result must be RECOGNIZABLE as this specific person.

## STYLE REQUIREMENTS
- Amiga-era pixel art (16-bit) with smooth gradients
- Visible pixels but NOT a pixelated photo filter
- Clean lines, rich colors, consistent shading
- Stylized but maintains individual features
- NOT photorealistic, NOT overly cartoonish

## APPEARANCE
- [Describe clothing from photo or as specified]
- [Describe expression]
- [Describe any accessories]

## BACKGROUND
- [Describe background style and colors]
- Pixel art style matching the character

## TECHNICAL
- NO TEXT on the image
- 512x512 output
- Portrait orientation, head and shoulders
- Square format

## OUTPUT
Save to: [output path]
```

## Example: Individual Avatar

For a team member named Dan with a reference photo showing short dark hair, beard, black v-neck:

```
Generate a pixel art avatar from the reference photo.

## INPUT IMAGE
/path/to/dan-photo.png - USE ONLY THIS IMAGE

## CRITICAL: LIKENESS PRESERVATION
Capture Dan's EXACT features from the photo:
- His specific face shape and jawline
- His eye shape and expression
- His nose shape
- His smile characteristics
- Short dark hair - exact texture and style from photo
- Full dark beard - exact pattern and coverage
The result must be RECOGNIZABLE as Dan.

## STYLE REQUIREMENTS
- Amiga-era pixel art (16-bit) with smooth gradients
- Visible pixels but NOT a pixelated photo filter
- Clean lines, rich colors, consistent shading
- Stylized but maintains individual features

## APPEARANCE
- Black v-neck shirt
- Warm smile showing teeth
- Friendly, approachable expression

## BACKGROUND
- California sunset cityscape
- Warm oranges, pinks, teals
- Pixel art style matching the character

## TECHNICAL
- NO TEXT on the image
- 512x512 output
- Portrait orientation, head and shoulders

## OUTPUT
Save to: /path/to/output/dan-pixel.png
```

## Context Discipline

**Do not read generated avatar images back into context.** The script outputs only the file path. Ask the user to visually inspect the result and provide feedback for iteration. To inspect programmatically, optimize the image first (via the optimize-images skill).

## Iteration Workflow

1. **First attempt**: Generate with detailed prompt
2. **Review**: Check both likeness AND style
3. **Adjust if needed**:
   - If too photorealistic: Emphasize "stylized pixel art character"
   - If likeness lost: Strengthen feature descriptions from source
   - If wrong features: Be more specific about what to capture

## Common Issues

### Face doesn't match source
- Ensure ONLY the subject's photo is used as input
- Add more specific feature descriptions
- Reference exact details visible in the photo

### Too photorealistic
- Emphasize "pixel art character" not "pixelated photo"
- Request "stylized" and "illustrated feel"
- Mention "Amiga-era" or "16-bit" aesthetic

### Too cartoonish / loses likeness
- Strengthen the likeness preservation section
- List specific features to capture
- Emphasize "RECOGNIZABLE as this person"

## Reference Files

For background style references:
- **`references/background-styles.md`** - Common background approaches for avatars
