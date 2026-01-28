---
name: ai-image
description: Generate AI images using OpenAI's gpt-image-1 model with customizable aspect ratios and artistic themes. Use when the user wants to create images, generate artwork, or mentions image generation with specific styles like Ghibli, futuristic, Pixar, oil painting, or Chinese painting.
---

# AI Image Generation Skill

Generate high-quality AI images using OpenAI's gpt-image-1 model with customizable styles and themes.

## When to Use This Skill

Use this skill when the user wants to:
- Generate images from text descriptions
- Create artwork with specific artistic styles
- Generate images with particular aspect ratios (vertical, horizontal, square)
- Apply themed visual styles (Studio Ghibli, futuristic, Pixar, oil painting, Chinese painting)

## Instructions

1. **Check for API Key**: Verify that the OPENAI_API_KEY environment variable is set
2. **Gather Requirements**: Ask the user for:
   - Image prompt (required)
   - Style/aspect ratio: vertical (1024x1536), horizontal (1536x1024), or square (1024x1024)
   - Theme: ghibli, futuristic, pixar, oil-paint, or chinese-paint (optional)
   - Output location (optional, defaults to ./generated_image.png)
3. **Run the CLI**: Execute the main.py script with the appropriate parameters
4. **Report Results**: Show the user where the image was saved and any relevant details

## Available Options

### Aspect Ratios (--style)
- `vertical`: 1024x1536 pixels (portrait orientation)
- `horizontal`: 1536x1024 pixels (landscape orientation)
- `square`: 1024x1024 pixels (default)

### Artistic Themes (--theme)
- `ghibli`: Studio Ghibli animation style with whimsical, dreamlike aesthetics
- `futuristic`: Sci-fi style with sleek designs and neon lights
- `pixar`: Vibrant 3D animation style with expressive characters
- `oil-paint`: Classical oil painting with rich textures and brushstrokes
- `chinese-paint`: Traditional Chinese ink painting with delicate brushwork

## Usage Examples

### Basic Usage
```bash
uv run main.py --prompt "a cat sitting on a tree"
```

### With Style and Theme
```bash
uv run main.py --prompt "a sunset over mountains" --style horizontal --theme oil-paint --output ./sunset.png
```

### Futuristic Portrait
```bash
uv run main.py --prompt "a robot in a city" --style vertical --theme futuristic --output ./robot.png
```

### Studio Ghibli Landscape
```bash
uv run main.py --prompt "a magical forest with spirits" --style horizontal --theme ghibli --output ./forest.png
```

## Setup Requirements

This skill requires an OpenAI API key with access to the gpt-image-1 model:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Note: Using gpt-image-1 requires organization verification on the OpenAI platform.

## Technical Details

- **Model**: OpenAI gpt-image-1 (released April 2025)
- **Response Format**: Base64 encoded images (b64_json)
- **Supported Sizes**: 1024x1024, 1024x1536, 1536x1024
- **Maximum Resolution**: Up to 4096x4096 pixels
- **Dependencies**: openai>=2.7.1

## Pricing Information

Usage is priced per token:
- Text tokens: $5 per million
- Image input tokens: $10 per million
- Image output tokens: $40 per million

Approximate costs per generated image:
- Low quality square: ~$0.02
- Medium quality square: ~$0.07
- High quality square: ~$0.19

## Troubleshooting

### API Key Not Set
If you see "Error: OPENAI_API_KEY environment variable not set", ensure your API key is exported in your shell session.

### Organization Not Verified
gpt-image-1 requires organization verification on platform.openai.com. Visit your OpenAI account settings to complete verification.

### Invalid Size Error
Ensure you're using one of the supported sizes: 1024x1024, 1024x1536, or 1536x1024.
