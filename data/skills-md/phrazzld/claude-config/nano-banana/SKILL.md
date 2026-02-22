---
name: nano-banana
description: AI image generation with curated prompt library. Use for creating images from text prompts, editing existing images, or browsing 6000+ professional prompt templates. Supports avatars, social media, product shots, logos, infographics, and more.
effort: high
---

# Nano Banana - Image Generation + Prompt Library

Generate images using Gemini API with access to 6000+ curated professional prompts.

## Quick Start

### Direct Generation
```bash
python scripts/generate_image.py "A cat wearing a wizard hat" output.png
```

### Search Prompts First
```bash
python scripts/search_prompts.py "avatar professional"
```

### Edit Existing Image
```bash
python scripts/edit_image.py input.png "Add rainbow background" output.png
```

## Workflow

### Step 0: Mode Detection

Classify user intent:

| Mode | Signal | Action |
|------|--------|--------|
| Direct | Clear prompt provided | Generate immediately |
| Exploration | Vague request, needs ideas | Search prompts first |
| Content-based | User provides article/context | Extract themes, then search |

### Step 1: Prompt Search (exploration mode)

Search by category:
- `avatars` - Headshots, portraits, profile pictures
- `social_media` - Instagram, Twitter, Facebook content (3800+)
- `product_marketing` - Ads, campaigns (1900+)
- `infographic` - Data visualization
- `thumbnails` - YouTube covers
- `comics` - Sequential art, storyboards
- `ecommerce` - Product photography
- `game_assets` - Sprites, characters
- `posters` - Events, announcements
- `web_design` - UI mockups

**Token optimization:** Use grep patterns, NEVER fully load reference files.

Present max 3 matching prompts with sample images when available.

### Step 2: Generation

| Source | Action |
|--------|--------|
| Curated prompt selected | Use EXACT prompt text |
| No match / user declines | Generate custom, label [AI-Generated] |

### Step 3: Refinement (optional)

Use multi-turn chat for iterative editing:
```bash
python scripts/multi_turn_chat.py
```

## Prompt Categories

| Category | Count | Best For |
|----------|-------|----------|
| Social Media | 3800+ | Instagram, Twitter, Facebook |
| Product Marketing | 1900+ | Ads, campaigns |
| Avatars | 700+ | Headshots, portraits |
| Infographic | 350+ | Data visualization |
| Posters | 300+ | Events, announcements |
| Comics | 200+ | Sequential art |
| E-commerce | 200+ | Product shots |
| Game Assets | 200+ | Sprites, characters |
| Thumbnails | 100+ | Video covers |
| Web Design | 100+ | UI mockups |

## Models

| Model | Resolution | Best For |
|-------|------------|----------|
| `gemini-2.5-flash-image` | 1024px | Speed, high-volume |
| `gemini-3-pro-image-preview` | Up to 4K | Professional assets, text rendering |

## Core API Pattern

All image generation uses the `generateContent` endpoint with `responseModalities: ["TEXT", "IMAGE"]`:

```python
import os
import base64
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["Your prompt here"],
)

for part in response.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = part.as_image()
        image.save("output.png")
```

## Image Configuration Options

Control output with `image_config`:

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
            image_size="2K"       # 1K, 2K, 4K (Pro only for 4K)
        ),
    )
)
```

## Editing Images

Pass existing images with text prompts:

```python
from PIL import Image

img = Image.open("input.png")
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["Add a sunset to this scene", img],
)
```

## Multi-Turn Refinement

Use chat for iterative editing:

```python
from google.genai import types

chat = client.chats.create(
    model="gemini-2.5-flash-image",
    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
)

response = chat.send_message("Create a logo for 'Acme Corp'")
# Save first image...

response = chat.send_message("Make the text bolder and add a blue gradient")
# Save refined image...
```

## Prompting Best Practices

### Photorealistic Scenes
Include camera details: lens type, lighting, angle, mood.
> "A photorealistic close-up portrait, 85mm lens, soft golden hour light, shallow depth of field"

### Stylized Art
Specify style explicitly:
> "A kawaii-style sticker of a happy red panda, bold outlines, cel-shading, white background"

### Text in Images
Be explicit about font style and placement. Use `gemini-3-pro-image-preview` for best results:
> "Create a logo with text 'Daily Grind' in clean sans-serif, black and white, coffee bean motif"

### Product Mockups
Describe lighting setup and surface:
> "Studio-lit product photo on polished concrete, three-point softbox setup, 45-degree angle"

## Advanced Features (Pro Model Only)

### Google Search Grounding
Generate images based on real-time data:

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Visualize today's weather in Tokyo as an infographic"],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        tools=[{"google_search": {}}]
    )
)
```

### Multiple Reference Images (Up to 14)
Combine elements from multiple sources:

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Create a group photo of these people in an office",
        Image.open("person1.png"),
        Image.open("person2.png"),
        Image.open("person3.png"),
    ],
)
```

## Environment

Requires `GEMINI_API_KEY` environment variable.

## Notes

- All generated images include SynthID watermarks
- Image-only mode (`responseModalities: ["IMAGE"]`) won't work with Google Search grounding
- For editing, describe changes conversationally—the model understands semantic masking
