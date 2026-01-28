---
name: nano-banana
description: Generate images from text prompts using Google Nano Banana (Gemini image generation) via eng0 data API. Use when user asks to generate, create, or make images, pictures, illustrations, or artwork from descriptions. Triggers include "generate image", "create image", "make a picture", "draw", "illustrate", "image of", "picture of", "nano banana". Do NOT use for image editing or manipulation of existing images.
---

# Nano Banana - Image Generation API

Generate images from text prompts using Google Nano Banana (Gemini's native image generation).

## Base URL

```
https://api.eng0.ai/api/data
```

## Models

| Model | ID | Best For | Max Resolution |
|-------|-----|----------|----------------|
| **Flash** | `flash` | Fast generation, high-volume tasks | 1024px |
| **Pro** | `pro` | Professional quality, complex prompts | 4K |

---

## Generate Image

Create an image from a text description.

```bash
curl -X POST https://api.eng0.ai/api/data/images/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic cityscape at sunset with flying cars",
    "model": "flash",
    "aspectRatio": "16:9"
  }'
```

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Text description of the image to generate |
| `model` | string | No | `flash` | `flash` (fast, 1024px) or `pro` (high-quality, up to 4K) |
| `aspectRatio` | string | No | `1:1` | Output aspect ratio |
| `imageSize` | string | No | `1K` | `1K`, `2K`, or `4K` (4K only with `pro` model) |

**Aspect Ratios:**

| Ratio | Use Case |
|-------|----------|
| `1:1` | Square (social media, icons) |
| `16:9` | Landscape (presentations, banners) |
| `9:16` | Portrait (mobile, stories) |
| `4:3` | Standard landscape |
| `3:4` | Standard portrait |
| `21:9` | Ultra-wide (cinematic) |
| `2:3`, `3:2`, `4:5`, `5:4` | Various formats |

**Response:**

```json
{
  "image": {
    "base64": "iVBORw0KGgoAAAANSUhEUgAA...",
    "mimeType": "image/png",
    "dataUrl": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  },
  "description": "A vibrant futuristic cityscape..."
}
```

**Response Fields:**

| Field | Description |
|-------|-------------|
| `image.base64` | Base64-encoded image data |
| `image.mimeType` | Image MIME type (typically `image/png`) |
| `image.dataUrl` | Ready-to-use data URL for HTML/CSS |
| `description` | Model's description of the generated image |

---

## Common Workflows

### Generate a Simple Image

```bash
curl -X POST https://api.eng0.ai/api/data/images/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cute robot holding a cup of coffee"
  }'
```

### Generate High-Quality 4K Image

```bash
curl -X POST https://api.eng0.ai/api/data/images/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Professional product photo of a sleek smartphone on marble surface",
    "model": "pro",
    "imageSize": "4K",
    "aspectRatio": "4:3"
  }'
```

### Generate Social Media Banner

```bash
curl -X POST https://api.eng0.ai/api/data/images/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Abstract gradient background with geometric shapes in blue and purple",
    "aspectRatio": "16:9"
  }'
```

### Generate Mobile Story Image

```bash
curl -X POST https://api.eng0.ai/api/data/images/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Cozy coffee shop interior with warm lighting",
    "aspectRatio": "9:16"
  }'
```

---

## Using with Python

```python
import requests
import base64
from pathlib import Path

BASE_URL = "https://api.eng0.ai/api/data"

def generate_image(
    prompt: str,
    model: str = "flash",
    aspect_ratio: str = "1:1",
    image_size: str = "1K"
) -> dict:
    """Generate an image from a text prompt."""
    response = requests.post(
        f"{BASE_URL}/images/generate",
        json={
            "prompt": prompt,
            "model": model,
            "aspectRatio": aspect_ratio,
            "imageSize": image_size
        }
    )
    return response.json()

def save_image(result: dict, filepath: str) -> None:
    """Save generated image to a file."""
    if "image" in result:
        image_data = base64.b64decode(result["image"]["base64"])
        Path(filepath).write_bytes(image_data)
        print(f"Saved to {filepath}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")

# Example: Generate and save an image
result = generate_image(
    prompt="A serene mountain landscape at dawn with mist in the valley",
    aspect_ratio="16:9"
)
save_image(result, "landscape.png")

# Example: Generate high-quality product image
result = generate_image(
    prompt="Minimalist tech gadget on white background, studio lighting",
    model="pro",
    image_size="4K"
)
save_image(result, "product.png")
```

---

## Using with Node.js

```javascript
const fs = require('fs');

const BASE_URL = 'https://api.eng0.ai/api/data';

async function generateImage(prompt, options = {}) {
  const response = await fetch(`${BASE_URL}/images/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt,
      model: options.model || 'flash',
      aspectRatio: options.aspectRatio || '1:1',
      imageSize: options.imageSize || '1K'
    })
  });
  return response.json();
}

function saveImage(result, filepath) {
  if (result.image) {
    const buffer = Buffer.from(result.image.base64, 'base64');
    fs.writeFileSync(filepath, buffer);
    console.log(`Saved to ${filepath}`);
  } else {
    console.error('Error:', result.error || 'Unknown error');
  }
}

// Example usage
(async () => {
  const result = await generateImage(
    'A neon-lit cyberpunk street scene at night',
    { aspectRatio: '21:9' }
  );
  saveImage(result, 'cyberpunk.png');
})();
```

---

## Prompt Tips

### Be Specific
```
Bad:  "A dog"
Good: "A golden retriever puppy playing in autumn leaves, warm sunlight"
```

### Include Style
```
"Oil painting style portrait of a woman in Renaissance clothing"
"Minimalist vector illustration of a mountain range"
"Photorealistic close-up of a dewdrop on a leaf"
```

### Specify Lighting
```
"... with dramatic side lighting"
"... golden hour sunlight"
"... soft diffused studio lighting"
```

### Add Context
```
"... in the style of Studio Ghibli"
"... professional product photography"
"... vintage 1970s film aesthetic"
```

---

## Model Comparison

| Feature | Flash | Pro |
|---------|-------|-----|
| Speed | Fast | Slower |
| Max Resolution | 1024px | 4K |
| Complex Prompts | Good | Excellent |
| Text Rendering | Good | Sharp |
| Best For | Quick iterations, previews | Final assets, print |

**When to use Flash:**
- Rapid prototyping
- Social media content
- High-volume generation
- When speed matters

**When to use Pro:**
- Professional/commercial use
- Print materials
- Complex compositions
- When quality matters

---

## Error Handling

**No Image Generated:**
```json
{
  "error": "No image generated",
  "message": "SAFETY"
}
```
This occurs when the prompt triggers content safety filters.

**Invalid Parameters:**
```json
{
  "error": "Invalid parameters",
  "message": "Missing required parameter: prompt"
}
```

---

## Important Notes

- All generated images include invisible **SynthID watermarking**
- Images are generated server-side; base64 responses can be large
- The `pro` model takes longer but produces higher quality
- 4K resolution is only available with the `pro` model
- Content safety filters may block certain prompts

---

## Combining with Other Skills

This skill provides **image generation**. Combine with:

- **deep-research** - Generate illustrations for research reports
- **market-data** - Create visualizations of financial data

**Example workflow:**
1. Research a topic (deep-research)
2. Generate relevant illustrations (this skill)
3. Compile into a report
