---
name: ergon
description: AI media generation CLI tool using Google's Imagen 4, Veo 3.1, and Gemini TTS. Use when the user wants to (1) generate images from text prompts, (2) edit existing images with AI, (3) explain image contents, (4) generate videos from text or images, (5) create narration/voice audio with character settings. Triggers on requests like "generate an image of...", "create a video...", "make a voice that says...", "edit this image to...", "describe this image".
license: MIT
metadata:
  author: hirokidaichi
  version: 0.4.0
---

# ergon - AI Media Generation CLI

> **Note:** Run with `npx ergon` if not installed globally.

## Quick Reference

```bash
npx ergon image gen "<prompt>" -t <style> -a <ratio>   # Image generation
npx ergon image edit <file> "<instruction>"            # Image editing
npx ergon video gen "<prompt>" [-i <image>]            # Video with audio
npx ergon narration gen "<text>" -c "<character>"      # Voice generation
```

## Image Generation

```bash
npx ergon image gen [options] <theme>
```

### Style Selection Guide

| Use Case | Style (`-t`) | Aspect (`-a`) |
|----------|--------------|---------------|
| Product photo, landscape | `realistic` | 16:9, 4:3 |
| Character, mascot | `anime`, `illustration` | 1:1, 3:4 |
| Icon, logo | `flat`, `minimal` | 1:1 |
| Art, poster | `watercolor`, `oil-painting`, `pop-art` | varies |
| Game asset | `pixel-art`, `3d-render` | 1:1 |
| Business, presentation | `corporate` | 16:9 |
| Concept sketch | `sketch` | varies |

### Options

| Option | Values | Default |
|--------|--------|---------|
| `-t, --type` | realistic, illustration, flat, anime, watercolor, oil-painting, pixel-art, sketch, 3d-render, corporate, minimal, pop-art | flat |
| `-a, --aspect-ratio` | 16:9, 4:3, 1:1, 9:16, 3:4 | 16:9 |
| `-s, --size` | tiny, hd, fullhd, 2k, 4k | fullhd |
| `-e, --engine` | imagen4, imagen4-fast, imagen4-ultra | imagen4 |

**Examples:**
```bash
npx ergon image gen "cute cat mascot for tech startup" -t anime -a 1:1
npx ergon image gen "professional team meeting in modern office" -t corporate -a 16:9
npx ergon image gen "abstract geometric logo" -t minimal -a 1:1 -o logo.png
```

## Image Editing

```bash
npx ergon image edit [options] <file> <prompt>
```

Edit instructions in natural language:
- Background change: "change background to sunset beach"
- Style transfer: "make it look like watercolor painting"
- Object removal: "remove the person on the left"
- Color adjustment: "make colors more vibrant"

```bash
npx ergon image edit photo.jpg "change background to blue sky"
npx ergon image edit portrait.png "convert to anime style"
```

## Video Generation (with Audio)

Veo 3.1 generates videos **with synchronized audio**. Include audio/sound instructions directly in the prompt.

```bash
npx ergon video gen [options] <theme>
```

### Prompt Structure for Audio-Video

Include sound descriptions in your prompt:

```bash
# Sound effects included
npx ergon video gen "cat meowing and playing with a ball, soft purring sounds"

# Music/ambient audio
npx ergon video gen "sunset timelapse over ocean, with calming wave sounds and soft piano music"

# Dialogue/voice
npx ergon video gen "person saying 'welcome to our channel' with friendly tone, waving at camera"
```

### Image-to-Video

Animate a static image with motion and sound:

```bash
npx ergon video gen "character starts dancing to upbeat music" -i character.png
npx ergon video gen "logo reveals with whoosh sound effect" -i logo.png
```

### Options

| Option | Values | Default |
|--------|--------|---------|
| `-i, --input` | image file | - |
| `-d, --duration` | 5-8 seconds | 8 |
| `-a, --aspect-ratio` | 16:9, 9:16 | 16:9 |
| `--fast` | use Veo 3.1 Fast | false |

Vertical video for TikTok/Reels: `-a 9:16`

## Narration Generation

For voice-only audio without video, use narration command.

```bash
npx ergon narration gen [options] <text>
```

### Character and Acting Direction

Use `-c` (character) and `-d` (direction) for expressive voice:

```bash
# Character defines WHO is speaking
npx ergon narration gen "Let's go on an adventure!" -c "energetic young girl"

# Direction defines HOW they speak
npx ergon narration gen "The results are in..." -c "news anchor" -d "serious, building suspense"

# Combined for full expression
npx ergon narration gen "Yay! We did it!" -c "excited child" -d "jumping with joy, high energy"
```

### Voice Selection

| Voice | Character |
|-------|-----------|
| Kore | Female, versatile (default) |
| Aoede | Female, warm |
| Charon | Male, deep |
| Fenrir | Male, strong |
| Puck | Neutral, playful |

### Options

| Option | Values | Default |
|--------|--------|---------|
| `-v, --voice` | Kore, Aoede, Charon, Fenrir, Puck | Kore |
| `-c, --character` | character description | - |
| `-d, --direction` | acting direction | - |
| `--speed` | 0.25-4.0 | 1.0 |
| `-l, --lang` | ja, en, zh, ko, etc. | ja |

## Workflow Patterns

### Generate, then Edit
```bash
npx ergon image gen "product photo of headphones" -t realistic
npx ergon image edit headphones.png "add soft shadow, white background"
```

### Image to Animated Video
```bash
npx ergon image gen "mascot character standing" -t anime -a 1:1
npx ergon video gen "mascot waves and says hello cheerfully" -i mascot.png
```

### Preview Before Generation
```bash
npx ergon image gen "complex scene" --dry-run  # Check settings
npx ergon video gen "expensive render" --dry-run  # Verify before API call
```

## Common Options

All commands support:
- `--json` - JSON output for scripting
- `--dry-run` - Preview settings without API call
- `-o, --output <path>` - Specify output path
