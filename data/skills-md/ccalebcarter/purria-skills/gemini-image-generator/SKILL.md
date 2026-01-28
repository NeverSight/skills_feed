---
name: gemini-image-generator
description: Generate images using Google Gemini AI with text prompts and reference images. Use when creating game assets, concept art, UI mockups, promotional images, or any visual content. Supports text-to-image, image-to-image with style transfer, and multiple output sizes. Requires GEMINI_API_KEY environment variable. Triggers on requests for AI image generation, concept art, visual assets, or Gemini images.
---

# Gemini Image Generator

Generate images using Google Gemini's image generation capabilities.

## Prerequisites

- Python 3.8+
- Google AI Studio API key
- Virtual environment with dependencies

## Setup

```bash
# Navigate to scripts directory
cd scripts

# Create virtual environment
python3 -m venv venv

# Install dependencies
./venv/bin/pip install -r requirements.txt  # Unix
# or
.\venv\Scripts\pip install -r requirements.txt  # Windows

# Set API key
export GEMINI_API_KEY="your-api-key"  # Unix
# or
$env:GEMINI_API_KEY = "your-api-key"  # PowerShell
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

## Usage

### Basic Text-to-Image

```bash
python generate.py --prompt "A serene mountain landscape at sunset" --output landscape.png
```

### With Reference Image (Style Transfer)

```bash
python generate.py --prompt "Same scene but in winter" --reference landscape.png --output winter.png
```

### Prompt Engineering Tips

For best results, structure prompts as:

```
[Subject] + [Style] + [Composition] + [Technical] + [Mood]
```

**Example for game assets:**
```
"A bio-mimetic robot with Art Nouveau brass gears and botanical vine patterns, 
centered composition on transparent background, flat vector style suitable for 
game sprite, warm golden hour lighting, whimsical and charming mood"
```

**Style keywords that work well:**
- Art styles: Art Nouveau, steampunk, Studio Ghibli, pixel art, vector illustration
- Technical: transparent background, game sprite, icon, UI element, seamless texture
- Mood: whimsical, dramatic, cozy, ethereal, vibrant

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--prompt` | Yes | Text description of desired image |
| `--output` | Yes | Output file path (.png) |
| `--reference` | No | Reference image for style guidance |

## Troubleshooting

| Error | Solution |
|-------|----------|
| API key not valid | Check GEMINI_API_KEY is set correctly |
| 403 Forbidden | API key may have IP restrictions |
| Model not found | Model names change; check Google AI docs |
| No image generated | Try simpler prompt, check API quota |

## Integration with Game Assets Team

This skill is the primary image generation tool for the `game-assets-team` skill. Use it for:

- Concept art exploration
- UI element generation
- Character/Simulin designs
- Background and environment art
- Promotional materials

Always follow the art direction guidelines in game-assets-team for consistent visual style.
