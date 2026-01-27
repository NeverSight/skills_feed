---
name: openai-image-gen
description: Generate images using OpenAI's DALL-E 3 API. Use when needing to create graphics, icons, backgrounds, or any visual assets. Requires OPENAI_API_KEY in environment.
---

# OpenAI Image Generation (DALL-E 3)

Generate images using OpenAI's DALL-E 3 API via command line.

## Quick Usage

```bash
# Generate an image with a prompt
~/.claude/skills/openai-image-gen/generate.sh "your prompt here" output.png

# Generate with specific size
~/.claude/skills/openai-image-gen/generate.sh "your prompt here" output.png 1792x1024

# Generate with quality setting
~/.claude/skills/openai-image-gen/generate.sh "your prompt here" output.png 1024x1024 hd
```

## Parameters

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| prompt | any text | required | The image description |
| output | filepath | required | Where to save the image |
| size | 1024x1024, 1792x1024, 1024x1792 | 1024x1024 | Image dimensions |
| quality | standard, hd | standard | Image quality (hd = more detail) |

## Size Guide

- **1024x1024** - Square, good for icons, avatars, general use
- **1792x1024** - Landscape/wide, good for headers, banners, hero images
- **1024x1792** - Portrait/tall, good for mobile backgrounds, vertical banners

## Gothic Cathedral Presets

Pre-made prompts for the 0xbigboss.github.io site:

### Backgrounds

```bash
# Dark stone texture
~/.claude/skills/openai-image-gen/generate.sh "Dark cathedral stone wall texture, seamless tileable pattern, deep charcoal gray with subtle purple undertones, weathered medieval masonry, dramatic shadows, gothic architecture, 4k texture, dark moody atmosphere" stone-bg.png 1024x1024

# Vaulted ceiling
~/.claude/skills/openai-image-gen/generate.sh "Gothic cathedral ribbed vault ceiling view from below, deep blue-black with gold leaf accent lines on ribs, dramatic perspective, medieval architecture, dim candlelit glow, ornate stone carvings fading into darkness, atmospheric fog, 4k" vault-ceiling.png 1792x1024
```

### Hero Images

```bash
# Homepage - Light rays
~/.claude/skills/openai-image-gen/generate.sh "Divine light rays streaming through gothic cathedral rose window, deep purple and blue stained glass, golden light beams cutting through darkness, dust particles floating in light, medieval stone interior, dramatic chiaroscuro, cinematic lighting, 4k" hero-home.png 1792x1024 hd

# Projects - Craftsman workshop
~/.claude/skills/openai-image-gen/generate.sh "Medieval craftsman's workshop, golden tools on dark wood workbench, gothic arched window in background, warm candlelight, scrolls and blueprints, brass instruments, artisan craftsmanship aesthetic, dramatic shadows, cinematic still life" hero-projects.png 1792x1024 hd

# Posts - Scriptorium
~/.claude/skills/openai-image-gen/generate.sh "Ancient scriptorium desk with illuminated manuscript, quill pen and gold ink pot, gothic window with blue light, leather-bound journals stacked, medieval monastery aesthetic, dramatic rim lighting, warm golden candlelight against cool window light" hero-posts.png 1792x1024 hd

# Contact - Cathedral door
~/.claude/skills/openai-image-gen/generate.sh "Gothic cathedral door slightly ajar with divine light streaming through crack, ornate iron hinges and handles, carved stone archway frame, welcoming yet mysterious, invitation to enter, dramatic lighting, medieval aesthetic" hero-contact.png 1792x1024 hd
```

### Stained Glass Windows

```bash
# Projects window
~/.claude/skills/openai-image-gen/generate.sh "Gothic stained glass window design, geometric pattern, deep purple and blue glass with gold leading, hammer and gear symbols, craftsman iconography, backlit with divine rays, ornate pointed arch frame, dark background, digital art" window-projects.png 1024x1024 hd

# Posts window
~/.claude/skills/openai-image-gen/generate.sh "Gothic stained glass window design, open book and quill symbols, deep blue and purple glass with gold leading, medieval manuscript aesthetic, backlit glow, pointed arch frame, ornate tracery pattern, dark background, digital art" window-posts.png 1024x1024 hd

# Contact window
~/.claude/skills/openai-image-gen/generate.sh "Gothic stained glass window design, dove and reaching hand symbols, deep purple and gold glass, connection iconography, divine light streaming through, pointed arch frame, ornate leading pattern, dark background, digital art" window-contact.png 1024x1024 hd
```

### Decorative Elements

```bash
# Logo monogram
~/.claude/skills/openai-image-gen/generate.sh "Medieval illuminated manuscript style monogram letters AE, gold leaf with deep blue and purple accents, ornate flourishes and Celtic knotwork, gothic calligraphy style, intricate detail, dark background, luxury heraldic aesthetic" logo-ae.png 1024x1024 hd

# Divider
~/.claude/skills/openai-image-gen/generate.sh "Medieval ornate horizontal divider, gold filigree on dark background, gothic scrollwork pattern, symmetrical design, thin elegant line with central medallion, Celtic knotwork accents, digital art, isolated element" divider.png 1792x1024

# Light ray overlay
~/.claude/skills/openai-image-gen/generate.sh "Divine light rays streaming from top, volumetric god rays, dust particles floating, golden warm light on pure black background, cathedral lighting effect, subtle and ethereal, digital art" light-overlay.png 1792x1024
```

## Batch Generation

Generate all Gothic presets at once:

```bash
cd ~/path/to/your/project/public/images
~/.claude/skills/openai-image-gen/batch-gothic.sh
```

## Tips for Better Results

1. **Be specific** - More detail = better results
2. **Include style keywords** - "4k", "cinematic", "digital art", "photorealistic"
3. **Specify lighting** - "dramatic shadows", "rim lighting", "candlelit"
4. **Mention perspective** - "from below", "bird's eye view", "close-up"
5. **Use quality=hd** for hero images and important assets

## Troubleshooting

**"Invalid API key"** - Check `echo $OPENAI_API_KEY` is set

**"Content policy violation"** - Rephrase prompt to avoid flagged content

**Image looks wrong** - DALL-E interprets prompts creatively; try multiple generations or refine prompt

## Cost Reference

DALL-E 3 pricing (as of 2024):
- Standard 1024x1024: ~$0.04/image
- Standard 1792x1024 or 1024x1792: ~$0.08/image
- HD 1024x1024: ~$0.08/image
- HD 1792x1024 or 1024x1792: ~$0.12/image
