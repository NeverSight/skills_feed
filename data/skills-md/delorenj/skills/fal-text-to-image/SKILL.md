---
name: fal-text-to-image
description: Generate high-quality images from text prompts using fal.ai's text-to-image models. Supports intelligent model selection, style transfer, and professional-grade outputs.
---

# fal.ai Text-to-Image Generation Skill

Generate production-quality images from text prompts using fal.ai's state-of-the-art text-to-image models including FLUX, Recraft V3, Imagen4, and more.

## When to Use This Skill

Trigger when user:
- Requests image generation from text descriptions
- Wants to create images with specific styles (vector, realistic, typography)
- Needs high-resolution professional images (up to 2K)
- Wants to use a reference image for style transfer
- Mentions specific models like FLUX, Recraft, or Imagen
- Asks for logo, poster, or brand-style image generation

## Quick Start

### Basic Usage
```bash
uv run python fal-text-to-image "A cyberpunk city at sunset with neon lights"
```

### With Specific Model
```bash
uv run python fal-text-to-image -m flux-pro/v1.1-ultra "Professional headshot of a business executive"
```

### With Style Reference Image
```bash
uv run python fal-text-to-image -i reference.jpg "A mountain landscape" -m flux-2/lora/edit
```

## Model Selection Guide

The script intelligently selects the best model based on task context:

### **flux-pro/v1.1-ultra** (Default for High-Res)
- **Best for**: Professional photography, high-resolution outputs (up to 2K)
- **Strengths**: Photo realism, professional quality
- **Use when**: User needs publication-ready images
- **Endpoint**: `fal-ai/flux-pro/v1.1-ultra`

### **recraft/v3/text-to-image** (SOTA Quality)
- **Best for**: Typography, vector art, brand-style images, long text
- **Strengths**: Industry-leading benchmark scores, precise text rendering
- **Use when**: Creating logos, posters, or text-heavy designs
- **Endpoint**: `fal-ai/recraft/v3/text-to-image`

### **flux-2** (Best Balance)
- **Best for**: General-purpose image generation
- **Strengths**: Enhanced realism, crisp text, native editing
- **Use when**: Standard image generation needs
- **Endpoint**: `fal-ai/flux-2`

### **flux-2/lora** (Custom Styles)
- **Best for**: Domain-specific styles, fine-tuned variations
- **Strengths**: Custom style adaptation
- **Use when**: User wants specific artistic styles
- **Endpoint**: `fal-ai/flux-2/lora`

### **flux-2/lora/edit** (Style Transfer)
- **Best for**: Image-to-image editing with style references
- **Strengths**: Specialized style transfer
- **Use when**: User provides reference image with `-i` flag
- **Endpoint**: `fal-ai/flux-2/lora/edit`

### **imagen4/preview** (Google Quality)
- **Best for**: High-quality general images
- **Strengths**: Google's highest quality model
- **Use when**: User specifically requests Imagen or Google models
- **Endpoint**: `fal-ai/imagen4/preview`

### **stable-diffusion-v35-large** (Typography & Style)
- **Best for**: Complex prompts, typography, style control
- **Strengths**: Advanced prompt understanding, resource efficiency
- **Use when**: Complex multi-element compositions
- **Endpoint**: `fal-ai/stable-diffusion-v35-large`

### **ideogram/v2** (Typography Specialist)
- **Best for**: Posters, logos, text-heavy designs
- **Strengths**: Exceptional typography, realistic outputs
- **Use when**: Text accuracy is critical
- **Endpoint**: `fal-ai/ideogram/v2`

### **bria/text-to-image/3.2** (Commercial Safe)
- **Best for**: Commercial projects requiring licensed training data
- **Strengths**: Safe for commercial use, excellent text rendering
- **Use when**: Legal/licensing concerns matter
- **Endpoint**: `fal-ai/bria/text-to-image/3.2`

## Command-Line Interface

```bash
uv run python fal-text-to-image [OPTIONS] PROMPT

Arguments:
  PROMPT                    Text description of the image to generate

Options:
  -m, --model TEXT         Model to use (see model list above)
  -i, --image TEXT         Path or URL to reference image for style transfer
  -o, --output TEXT        Output filename (default: generated_image.png)
  -s, --size TEXT          Image size (e.g., "1024x1024", "landscape_16_9")
  --seed INTEGER           Random seed for reproducibility
  --steps INTEGER          Number of inference steps (model-dependent)
  --guidance FLOAT         Guidance scale (higher = more prompt adherence)
  --help                   Show this message and exit
```

## Authentication Setup

Before first use, set your fal.ai API key:

```bash
export FAL_KEY="your-api-key-here"
```

Or create a `.env` file in the skill directory:
```env
FAL_KEY=your-api-key-here
```

Get your API key from: https://fal.ai/dashboard/keys

## Advanced Examples

### High-Resolution Professional Photo
```bash
uv run python fal-text-to-image \
  -m flux-pro/v1.1-ultra \
  "Professional headshot of a business executive in modern office" \
  -s 2048x2048
```

### Logo/Typography Design
```bash
uv run python fal-text-to-image \
  -m recraft/v3/text-to-image \
  "Modern tech startup logo with text 'AI Labs' in minimalist style"
```

### Style Transfer from Reference
```bash
uv run python fal-text-to-image \
  -m flux-2/lora/edit \
  -i artistic_style.jpg \
  "Portrait of a woman in a garden"
```

### Reproducible Generation
```bash
uv run python fal-text-to-image \
  -m flux-2 \
  --seed 42 \
  "Futuristic cityscape with flying cars"
```

## Model Selection Logic

The script automatically selects the best model when `-m` is not specified:

1. **If `-i` provided**: Uses `flux-2/lora/edit` for style transfer
2. **If prompt contains typography keywords** (logo, text, poster, sign): Uses `recraft/v3/text-to-image`
3. **If prompt suggests high-res needs** (professional, portrait, headshot): Uses `flux-pro/v1.1-ultra`
4. **If prompt mentions vector/brand**: Uses `recraft/v3/text-to-image`
5. **Default**: Uses `flux-2` for general purpose

## Output Format

Generated images are saved with metadata:
- Filename includes timestamp and model name
- EXIF data stores prompt, model, and parameters
- Console displays generation time and cost estimate

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `FAL_KEY not set` | Export FAL_KEY environment variable or create .env file |
| `Model not found` | Check model name against supported list |
| `Image reference fails` | Ensure image path/URL is accessible |
| `Generation timeout` | Some models take longer; wait or try faster model |
| `Rate limit error` | Check fal.ai dashboard for usage limits |

## Cost Optimization

- **Free tier**: FLUX.2 offers 100 free requests (expires Dec 25, 2025)
- **Pay per use**: FLUX Pro charges per megapixel
- **Budget option**: Use `flux-2` or `stable-diffusion-v35-large` for general use
- **Premium**: Use `flux-pro/v1.1-ultra` only when high-res is required

## File Structure

```
fal-text-to-image/
├── SKILL.md                    # This file
├── pyproject.toml              # Dependencies (uv)
├── fal-text-to-image           # Main executable script
├── references/
│   └── model-comparison.md     # Detailed model benchmarks
└── outputs/                    # Generated images (created on first run)
```

## Dependencies

Managed via `uv`:
- `fal-client`: Official fal.ai Python SDK
- `python-dotenv`: Environment variable management
- `pillow`: Image handling and EXIF metadata
- `click`: CLI interface

## Best Practices

1. **Model Selection**: Let the script auto-select unless you have specific needs
2. **Reference Images**: Use high-quality references for best style transfer results
3. **Prompt Engineering**: Be specific and descriptive for better outputs
4. **Cost Awareness**: Monitor usage on fal.ai dashboard
5. **Reproducibility**: Use `--seed` for consistent results during iteration

## Resources

- fal.ai Documentation: https://docs.fal.ai/
- Model Playground: https://fal.ai/explore/search
- API Keys: https://fal.ai/dashboard/keys
- Pricing: https://fal.ai/pricing

## Limitations

- Requires active fal.ai API key
- Subject to fal.ai rate limits and quotas
- Internet connection required
- Some models have usage costs (check pricing)
- Image reference features limited to specific models
