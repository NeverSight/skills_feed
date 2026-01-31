---
name: image-generation
description: Generate images using FAL.ai nanobanana pro. Use when creating product shots, social graphics, brand assets, or any visual content. Integrates with automation system for direct asset generation in Claude Code.
---

# Image Generation Skill

## Overview

Image Generation uses FAL.ai nanobanana pro to create professional-quality images from text descriptions. This skill teaches you how to craft effective prompts and use the automation system to generate assets directly in Claude Code.

**Keywords**: image generation, nanobanana pro, prompt engineering, AI art, visual content creation, asset generation, automation

## Core Models

### nanobanana pro — Recommended
- **Quality**: Highest, most detailed
- **Speed**: 30-60 seconds
- **Best For**: Product photography, hero images, final assets
- **Use Case**: When quality matters most

### nanobanana pro
- **Quality**: High, good detail
- **Speed**: 5-15 seconds
- **Best For**: Testing, iterations, social media
- **Use Case**: When speed matters

### nanobanana pro
- **Quality**: Latest, improved
- **Speed**: 20-40 seconds
- **Best For**: Production work
- **Use Case**: When you want the latest model

## Prompt Engineering Framework

### The 5-Part Prompt Formula

Every effective prompt has 5 components:

**1. Subject** — What is the main thing?
```
"A luxury leather watch"
"A modern logo"
"An Instagram post graphic"
```

**2. Description** — What does it look like?
```
"with gold accents and brown leather strap"
"geometric style, minimalist design"
"vibrant colors, eye-catching composition"
```

**3. Style** — What's the artistic style?
```
"professional product photography"
"modern illustration"
"digital design"
"photorealistic"
```

**4. Technical Details** — Quality and format specs
```
"studio lighting, sharp focus, 4K, centered composition"
"high contrast, trending design, professional quality"
"detailed, well-lit, professional photography"
```

**5. Mood/Aesthetic** — What's the feeling?
```
"luxury and professional"
"energetic and modern"
"clean and minimalist"
"warm and inviting"
```

### Complete Prompt Example

```
A luxury leather watch with gold accents and brown strap, 
professional product photography, studio lighting with rim light, 
centered composition, sharp focus, 4K, luxury and professional mood
```

### Prompt Engineering Techniques

**Technique 1: Be Specific**
```
❌ Bad: "A watch"
✅ Good: "A luxury leather watch with gold accents on white background"
```

**Technique 2: Use Descriptive Adjectives**
```
❌ Bad: "A logo"
✅ Good: "A modern, geometric, minimalist logo in blue and white"
```

**Technique 3: Reference Styles**
```
❌ Bad: "A nice graphic"
✅ Good: "A graphic in the style of modern Instagram design trends"
```

**Technique 4: Specify Quality**
```
❌ Bad: "A photo"
✅ Good: "A professional 4K product photograph with studio lighting"
```

**Technique 5: Include Composition**
```
❌ Bad: "A person"
✅ Good: "A person in rule of thirds composition, natural lighting, centered"
```

## Claude Code Integration

### How to Use in Claude Code

Claude Code can directly generate images using the automation system:

```python
from claude_integration import generate_asset

# Generate a single image
result = generate_asset(
    category="product-photos",
    name="luxury-watch",
    prompt="A luxury leather watch with gold accents on white background, professional product photography, studio lighting, 4K, sharp focus",
    size="1024x1024",
    num_variations=1
)

print(f"Generated: {result['images']}")
```

### Setup for Claude Code

**Ensure these files are in your project:**
```
your-project/
├── vibe-creative-automation/
│   ├── fal_api.py
│   ├── creative_cli.py
│   ├── claude_integration.py
│   └── requirements.txt
└── assets/  (will be created automatically)
```

**Set environment variable:**
```bash
export FAL_API_KEY="your_key_here"
```

**Install dependencies:**
```bash
pip install requests
```

### Claude Code Workflow

When you ask Claude: **"Generate 3 variations of a product photo for my watch"**

Claude will:

1. **Read Image Generation skill** to understand prompting
2. **Read Creative Strategist** to get your style
3. **Craft the prompt** combining both
4. **Call automation system** with the prompt
5. **Generate 3 images** using FLUX model
6. **Save to folder** like `assets/product-photos/luxury-watch/`
7. **Show you results** with file paths

### Example: Claude Code Generates Product Photos

```python
from claude_integration import generate_asset

# Your Creative Strategist style (from your style guide)
YOUR_STYLE = {
    "primary_style": "photorealistic",
    "mood": "professional and luxurious",
    "lighting": "studio lighting with rim light",
    "composition": "centered"
}

# Generate product photo using your style
prompt = f"""
A luxury leather watch with gold accents,
{YOUR_STYLE['primary_style']},
{YOUR_STYLE['mood']},
{YOUR_STYLE['lighting']},
{YOUR_STYLE['composition']},
white background,
4K,
sharp focus,
professional product photography
"""

result = generate_asset(
    category="product-photography",
    name="luxury-watch",
    prompt=prompt,
    size="1024x1024",
    num_variations=3
)

for img_path in result['images']:
    print(f"✅ Generated: {img_path}")
```

### Batch Generation Example

```python
from claude_integration import batch_generate_assets

# Generate multiple assets at once
assets = [
    {
        "type": "custom",
        "category": "product-photos",
        "name": "watch",
        "prompt": "Luxury watch, professional photography, studio lighting, 4K"
    },
    {
        "type": "custom",
        "category": "product-photos",
        "name": "wallet",
        "prompt": "Premium leather wallet, professional photography, studio lighting, 4K"
    },
    {
        "type": "custom",
        "category": "product-photos",
        "name": "sunglasses",
        "prompt": "Designer sunglasses, professional photography, studio lighting, 4K"
    }
]

results = batch_generate_assets(assets)

for result in results:
    print(f"{result['asset_name']}: {result['images']}")
```

## Image Sizes

Choose the right size for your use case:

| Size | Use Case | Speed | Detail |
|------|----------|-------|--------|
| 512x512 | Testing, thumbnails | Fast | Good |
| 768x768 | Social media, web | Medium | Good |
| 1024x1024 | Product photos, hero images | Medium | Excellent |
| 1536x1536 | Large prints, high-res | Slow | Excellent |
| 2048x2048 | 4K, maximum detail | Very Slow | Maximum |

## Generation Parameters

### Guidance Scale (3.5 - 7.5)

Controls how strictly the model follows your prompt:

```
3.5 — More creative freedom, less literal
5.0 — Balanced (recommended)
7.5 — Strict adherence to prompt, more literal
```

**Example:**
```python
# More creative
result = generate_asset(..., guidance_scale=3.5)

# Balanced (default)
result = generate_asset(..., guidance_scale=5.0)

# Strict
result = generate_asset(..., guidance_scale=7.5)
```

### Inference Steps (20 - 50)

More steps = higher quality but slower:

```
20 — Fast, acceptable quality
28 — Balanced (default)
40 — High quality
50 — Maximum quality
```

**Example:**
```python
# Fast generation
result = generate_asset(..., inference_steps=20)

# Balanced (default)
result = generate_asset(..., inference_steps=28)

# High quality
result = generate_asset(..., inference_steps=40)
```

## Practical Prompt Examples

### Product Photography

```
A luxury leather watch with gold accents on white background, 
professional product photography, studio lighting with rim light, 
centered composition, sharp focus, 4K, highly detailed
```

### Social Media Graphic

```
Instagram post graphic for product launch, vibrant colors, 
eye-catching composition, modern design, 1080x1080 format, 
trending aesthetic, professional quality
```

### Logo Design

```
Modern tech company logo, geometric style, blue and white colors, 
minimalist design, scalable, professional, clean lines, 
suitable for all media
```

### Illustration

```
Colorful illustration of a person working at a computer, 
modern illustration style, bright colors, friendly mood, 
professional quality, trending design
```

### Hero Image

```
A futuristic tech workspace with multiple monitors, 
professional photography, modern aesthetic, blue and purple lighting, 
cinematic composition, 4K, highly detailed
```

## Integration with Other Skills

**Image Generation + Creative Strategist:**
- Use your style guide to craft better prompts
- Maintain consistency across all generated images

**Image Generation + Product Photography:**
- Generate product shots for e-commerce
- Create lifestyle product photos

**Image Generation + Social Graphics:**
- Generate graphics for social media
- Create platform-specific content

**Image Generation + Brand Asset:**
- Generate logos and icons
- Create brand illustrations

## Command Line Usage

You can also use the CLI directly:

```bash
# Generate custom asset
python creative_cli.py custom \
  --category "product-photos" \
  --name "luxury-watch" \
  --prompt "A luxury leather watch with gold accents on white background, professional product photography, studio lighting, 4K, sharp focus" \
  --size 1024x1024 \
  --num-images 3 \
  --model fal-ai/nano-banana-pro
```

## Troubleshooting

### Problem: Images don't match my style

**Solution:**
- Add more specific style descriptors to prompt
- Reference your Creative Strategist guide
- Test with different guidance scales
- Generate multiple variations

### Problem: Generation is too slow

**Solution:**
- Use `fal-ai/nano-banana-pro` model
- Reduce image size to 768x768
- Reduce inference steps to 20

### Problem: Images are too creative/not literal enough

**Solution:**
- Increase guidance scale to 7.5
- Be more specific in prompt
- Add more technical details

### Problem: API errors

**Solution:**
- Verify FAL_API_KEY is set correctly
- Check internet connection
- Verify API key is valid
- Try again after a moment

## Best Practices

1. **Start with Creative Strategist** — Define your style first
2. **Be Specific** — More details = better results
3. **Test Variations** — Generate multiple versions
4. **Iterate** — Refine based on results
5. **Use Consistent Prompts** — Similar prompts = consistent style
6. **Reference Your Style** — Include style descriptors in every prompt
7. **Batch Generate** — Generate multiple assets at once
8. **Organize Assets** — Keep generated images organized

## Next Steps

1. **Define Your Style** — Complete Creative Strategist first
2. **Craft Your Prompt** — Use the 5-part formula
3. **Test Generation** — Generate a test image
4. **Iterate** — Refine based on results
5. **Batch Generate** — Create multiple assets
6. **Use in Projects** — Integrate with other skills

---

**You now have the power to generate professional images with AI. Start creating! 🎨**
