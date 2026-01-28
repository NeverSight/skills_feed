---
name: nano-banana-pro
description: |
  Image generation and editing using Google Gemini's Nano Banana Pro (gemini-3-pro-image-preview) model.
  Use when user requests: "Generate an image", "Create an image", "Make me a picture", "Draw",
  "Edit that image", "Change the color", "Remove background", "Add transparency", "Modify this image",
  "Make it transparent", "Change the style", "Add text to image", or any image creation/manipulation task.
  Supports text-to-image generation, image editing, multi-turn conversations, and transparency extraction
  via difference matting technique.
---

# Nano Banana Pro Image Generation & Editing

Generate and edit images using Google's Gemini 3 Pro model with advanced transparency support.

## Prerequisites

1. **Dependencies**:
   ```bash
   pip install google-genai Pillow numpy python-dotenv
   ```

2. **API Key**: The script loads from `.env` automatically. Only ask the user if the script fails with "No API key found".

## CLI Usage (REQUIRED)

**ALWAYS use the CLI script. Do NOT write Python code or create .py files.**

Run `scripts/generate.py` directly:

```bash
# Basic generation
python scripts/generate.py "a cute banana sticker" -o banana.png

# With transparency (for game assets, stickers, icons)
python scripts/generate.py "pixel art sword" -o sword.png --transparent

# Custom size and aspect ratio
python scripts/generate.py "game logo" -o logo.png --size 4K --ratio 16:9
```

**Options:**
- `-o, --output` - Output filename (default: output.png)
- `--transparent` - Extract true alpha channel using difference matting
- `--size` - 1K, 2K, or 4K (default: 2K)
- `--ratio` - Aspect ratio: 1:1, 16:9, 9:16, etc. (default: 1:1)
- `--model` - Model override (default: gemini-3-pro-image-preview)

**Note:** The script loads the API key from `.env` automatically. Do not check for API keys manually or ask the user about them - just run the script and it will error with instructions if the key is missing.

## Intent Detection

Analyze user request to determine:

| Intent | Triggers | Action |
|--------|----------|--------|
| **Generate** | "create", "generate", "make", "draw", "design" | Text-to-image |
| **Edit** | "edit", "change", "modify", "update", "fix" | Image-to-image |
| **Transparency** | "transparent", "remove background", "alpha", "cutout", "PNG with transparency" | Use difference matting |
| **Text overlay** | "add text", "write on", "label", "caption" | Use Gemini 3 Pro for accurate text |

## Resolution Selection

Choose resolution based on use case:

| Resolution | Best For | Pixel Output |
|------------|----------|--------------|
| **1K** | Quick previews, thumbnails, web icons | ~1024px |
| **2K** | Social media, standard web images | ~2048px |
| **4K** | Print, professional assets, sprite sheets | ~4096px |

**Heuristics:**
- Sprite sheets, game assets, print materials → **4K**
- Social media, blog images, presentations → **2K**
- Quick tests, thumbnails, prototypes → **1K**

When uncertain, ask user or default to **2K**.

## Aspect Ratios

Available: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

**Selection guide:**
- Square content (icons, avatars, social posts) → `1:1`
- Portrait (mobile, vertical video) → `9:16` or `3:4`
- Landscape (desktop, presentations) → `16:9` or `3:2`
- Cinematic/ultrawide → `21:9`

## Core Implementation

### Basic Generation

```python
from google import genai
from google.genai import types
from PIL import Image
import io

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Your descriptive prompt here",
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",  # or other ratio
            image_size="2K"     # 1K, 2K, or 4K
        ),
    ),
)

# Extract image from response
for part in response.parts:
    if part.inline_data is not None:
        image = Image.open(io.BytesIO(part.inline_data.data))
        image.save("output.png")
        break
```

### Image Editing

```python
# Load existing image
input_image = Image.open("input.png")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        input_image,
        "Edit instruction: Change the background to sunset colors"
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
            image_size="2K"
        ),
    ),
)
```

### Multi-Turn Editing

Preserve context across edits using thought signatures:

```python
# First edit
response1 = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[image, "Add a red hat"],
    config=config,
)

# Continue editing (include previous response)
response2 = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        image,
        "Add a red hat",
        response1,  # Include for context preservation
        "Now make the hat blue instead"
    ],
    config=config,
)
```

## Transparency Extraction

When user needs transparent images, use **difference matting**. See `scripts/transparency.py`.

**When to use:**
- User explicitly asks for transparency
- Game sprites, icons, logos
- Assets that will be composited
- Cutouts and stickers

**Process:**
1. Generate image on pure white background (#FFFFFF)
2. Edit same image to pure black background (#000000)
3. Calculate alpha from pixel differences
4. Recover original colors

**Key insight:** Opaque pixels appear identical on both backgrounds (distance ≈ 0), transparent pixels show background color (max distance).

```python
from scripts.transparency import extract_alpha_difference_matting

# After generating white and black background versions
final_image = extract_alpha_difference_matting(img_on_white, img_on_black)
final_image.save("output.png")  # RGBA with true transparency
```

## Prompt Engineering

### Fundamental Principle

> "Describe the scene, don't just list keywords."

Narrative paragraphs outperform disconnected word lists.

### Effective Prompt Structure

```
[Style/Medium] of [Subject] in [Context/Setting], [Lighting], [Additional details]
```

**Examples:**

```
# Photorealistic
A professional studio photograph of a brass steampunk pocket watch,
shot with a 50mm lens, soft diffused lighting from the left,
shallow depth of field with bokeh background, 4K HDR quality.

# Illustration
A detailed digital illustration of a medieval blacksmith's forge,
isometric perspective, warm orange glow from the furnace,
dieselpunk aesthetic with exposed pipes and riveted metal plates.

# Product mockup
A product photography shot of a ceramic coffee mug on a marble surface,
natural window lighting, minimalist Scandinavian style, clean white background.
```

### Text in Images

For images containing text, use Gemini 3 Pro (not Imagen):
- Keep text to 25 characters or less per element
- Use 2-3 distinct text phrases maximum
- Specify font style generally (bold, elegant, handwritten)
- Indicate size (small, medium, large)

### Quality Modifiers

Add these for enhanced output:
- **Photography:** 4K, HDR, studio photo, professional lighting
- **Art:** detailed, by a professional, high-quality illustration
- **General:** high-fidelity, crisp details, polished finish

## Error Handling

```python
from google.genai import errors

def generate_with_retry(client, *, model, contents, config, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        try:
            return client.models.generate_content(
                model=model, contents=contents, config=config
            )
        except errors.APIError as e:
            code = getattr(e, "code", None) or getattr(e, "status", None)
            if code not in (429, 500, 502, 503, 504) or attempt >= max_attempts:
                raise
            delay = min(30, 2 ** (attempt - 1))
            time.sleep(delay)
```

## Model Selection

| Model | Use Case |
|-------|----------|
| `gemini-3-pro-image-preview` | Complex edits, text rendering, multi-turn, transparency workflows |
| `gemini-2.5-flash-image` | Quick generation, high volume, simple tasks |
| `imagen-4.0-generate-001` | Photorealistic images, no editing needed |

Default to **gemini-3-pro-image-preview** for most tasks.

## File References

- `scripts/generate.py` - CLI for image generation (use this instead of writing code)
- `scripts/transparency.py` - Difference matting implementation
- `references/prompts.md` - Extended prompt examples by category
