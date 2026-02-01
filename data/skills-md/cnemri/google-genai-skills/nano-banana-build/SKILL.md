---
name: nano-banana-build
description: Generate and edit high-quality images using Gemini 2.5 Flash Image and Gemini 3 Pro Image (Nano Banana). Supports Text-to-Image, Style Transfer, Virtual Try-On, and Character Consistency.
---

# Nano Banana Image Generation Skill

Use this skill to generate and edit images using the `google-genai` Python SDK with Gemini's specialized image models (Nano Banana).

## Quick Start Setup

```python
from google import genai
from google.genai import types
from PIL import Image
import io

client = genai.Client()
```

## Reference Materials

- **[Model Capabilities](references/model_capabilities.md)**: Comparison of Gemini 2.5 vs 3 Pro, resolutions, and token costs.
- **[Image Generation](references/image_generation.md)**: Text-to-Image, Interleaved Text/Image.
- **[Image Editing](references/image_editing.md)**: Subject Customization, Style Transfer, Multi-turn Editing.
- **[Thinking Process](references/thinking_process.md)**: Understanding thoughts and signatures (Gemini 3 Pro).
- **[Recipes](references/recipes.md)**: Extensive collection of examples (Logos, Stickers, Mockups, Comics, etc.).
- **[Source Code](references/source_code.md)**: Deep inspection of SDK internals.

## Available Models

- **`gemini-2.5-flash-image` (Nano Banana)**: Fast, high-quality generation and editing. Best for most use cases.
- **`gemini-3-pro-image-preview` (Nano Banana Pro)**: Highest fidelity, supports `2K` and `4K` resolution, complex prompt adherence, and grounding.

## Common Workflows

### 1. Fast Generation
```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A cute robot eating a banana',
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE']
    )
)
```

### 2. High-Quality Editing
```python
response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents=[
        types.Part.from_uri(file_uri='gs://.../shoe.jpg', mime_type='image/jpeg'),
        "Change the color of the shoe to neon green."
    ],
    config=types.GenerateContentConfig(response_modalities=['IMAGE'])
)
```
