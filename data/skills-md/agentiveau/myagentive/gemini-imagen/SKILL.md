---
name: gemini-imagen
description: Generate images from text prompts using Google's Gemini Imagen API. This skill should be used when the user requests image creation, generation, or visualization from text descriptions (e.g., "create an image of...", "generate a picture showing...", "make me an image for...").
---

# Gemini Imagen

## Overview

This skill enables image generation from text prompts using Google's Gemini Imagen API. It provides a reusable script that handles API authentication, request formatting, response processing, and automatic image saving with proper error handling.

## When to Use This Skill

Use this skill when the user requests:
- Creating or generating images from text descriptions
- Visualizing concepts, scenes, or objects through AI-generated imagery
- Producing multiple variations of an image concept
- Creating images with specific aspect ratios or quality levels

**Example requests:**
- "Generate an image of a sunset over mountains"
- "Create a logo concept showing a geometric bird"
- "Make me an image of a futuristic city at night in 16:9 ratio"
- "Generate 3 variations of a robot painting artwork"

## Configuration

### API Key Setup

The Gemini API requires an API key for authentication. Obtain a key from [Google AI Studio](https://ai.google.dev/).

**Recommended approach:** Store the API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Alternatively, pass the key directly when invoking the script (less secure for shared environments).

### Python Dependencies

The script requires these Python packages:
- `requests` - HTTP client for API calls
- `Pillow` - Image processing library

These are included in the project's shared virtual environment. Activate it before running:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Generating Images

### Basic Usage

To generate a single image with default settings:

```bash
python scripts/generate_image.py "your prompt here" --api-key $GEMINI_API_KEY
```

The script will:
1. Send the prompt to the Gemini Imagen API
2. Receive and decode the generated image(s)
3. Save images with timestamped filenames (e.g., `gemini_image_20231123_142530_1.png`)
4. Display progress and file paths

### Advanced Options

#### Model Selection

Choose from three quality/speed tiers:

```bash
# Fast generation (default) - quickest, good quality
--model imagen-4.0-fast-generate-001

# Standard generation - balanced speed and quality
--model imagen-4.0-generate-001

# Ultra generation - highest quality, slower
--model imagen-4.0-ultra-generate-001
```

#### Aspect Ratios

Generate images in different dimensions:

```bash
# Square (default)
--aspect-ratio 1:1

# Portrait orientations
--aspect-ratio 3:4
--aspect-ratio 9:16

# Landscape orientations
--aspect-ratio 4:3
--aspect-ratio 16:9
```

#### Multiple Images

Generate up to 4 variations in a single request:

```bash
--num 4
```

#### Output Directory

Specify where to save generated images:

```bash
--output ./generated_images
```

### Complete Examples

**Generate a high-quality landscape image:**
```bash
python scripts/generate_image.py \
  "Majestic mountain range at golden hour with dramatic clouds" \
  --api-key $GEMINI_API_KEY \
  --model imagen-4.0-ultra-generate-001 \
  --aspect-ratio 16:9 \
  --output ./landscapes
```

**Create multiple logo variations:**
```bash
python scripts/generate_image.py \
  "Minimalist geometric logo for tech startup, blue and white" \
  --api-key $GEMINI_API_KEY \
  --num 4 \
  --aspect-ratio 1:1 \
  --output ./logo_concepts
```

**Quick social media graphic:**
```bash
python scripts/generate_image.py \
  "Abstract colorful pattern for social media background" \
  --api-key $GEMINI_API_KEY \
  --aspect-ratio 9:16 \
  --output ./social_media
```

## Workflow Integration

When a user requests image generation:

1. **Extract the prompt** from the user's request
2. **Determine parameters** based on context:
   - Aspect ratio (square for logos, 16:9 for presentations, etc.)
   - Number of variations (if user wants options)
   - Quality tier (ultra for final outputs, fast for iteration)
3. **Invoke the script** with appropriate parameters
4. **Show the generated images** to the user and provide file paths
5. **Iterate if needed** with refined prompts or different parameters

## Best Practices

### Prompt Engineering

- **Be specific and descriptive:** Include details about style, lighting, composition, colors
- **Specify art style if desired:** "digital art", "oil painting", "photorealistic", "minimalist"
- **Mention important elements:** Objects, subjects, background, atmosphere
- **Include quality keywords:** "high detail", "professional", "award-winning"

**Example good prompt:**
> "A serene Japanese garden with cherry blossoms in full bloom, koi pond in foreground, traditional stone lantern, soft morning light, photorealistic style, high detail"

**Example basic prompt (works but less controlled):**
> "Japanese garden"

### Model Selection

- **Fast model:** Prototyping, iteration, quick previews, high-volume generation
- **Standard model:** General-purpose images, balanced quality and speed
- **Ultra model:** Final outputs, client presentations, high-stakes visuals

### Error Handling

The script handles common errors:
- Invalid API keys → Check API key configuration
- Network timeouts → Verify internet connection, retry request
- Rate limiting → Wait and retry, consider reducing simultaneous requests
- Invalid parameters → Review model name, aspect ratio, and num_images values

## Output Format

Generated images are saved as PNG files with:
- **Naming convention:** `gemini_image_YYYYMMDD_HHMMSS_N.png`
- **Timestamp:** Ensures unique filenames across runs
- **Sequential numbering:** When generating multiple images
- **SynthID watermark:** Automatically embedded by Imagen API

## Resources

### scripts/generate_image.py

The main image generation script that handles:
- API authentication and request formatting
- Base64 image decoding and PIL processing
- Automatic file saving with timestamps
- Comprehensive error handling and user feedback
- Command-line interface with all customization options

Invoke directly from the command line or integrate into larger workflows.
