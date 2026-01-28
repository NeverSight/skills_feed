---
name: nano-banana
description: Generate and edit images using Gemini's image generation API (Imagen 3). This skill should be used when creating images, illustrations, diagrams, editing existing images, or iteratively refining visual content through multi-turn conversations.
allowed-tools: Bash(python:*), Read, Write
---

# Nano Banana - Gemini Image Generation

This skill provides comprehensive access to Gemini's image generation capabilities, including text-to-image generation, image editing, multi-turn refinement, batch processing, and high-resolution output.

## Prerequisites

- API key set as `GOOGLE_API_KEY` or `GEMINI_API_KEY` environment variable
- The scripts include a bundled virtual environment (`.venv/`) with `google-genai` pre-installed
- Scripts can be called directly: `~/.claude/skills/nano-banana/scripts/generate_image.py`

## Available Models

| Model | ID | Best For |
|-------|----|----------|
| **Flash** | `gemini-2.5-flash-image` | Fast generation, high volume, low latency |
| **Pro** | `gemini-3-pro-image-preview` | Professional quality, 4K, advanced reasoning |

## Capabilities Overview

| Capability | Script | Description |
|------------|--------|-------------|
| Image Generation | `generate_image.py` | Create images from text prompts |
| Image Editing | `edit_image.py` | Modify existing images with instructions |
| Batch Generation | `batch_generate.py` | Generate multiple images in parallel |
| Multi-turn Editing | `chat_session.py` | Iterative refinement via conversation |

## Quick Start

### Generate a Single Image

```bash
python scripts/generate_image.py "a sunset over mountains" sunset.png
```

With options:
```bash
python scripts/generate_image.py "modern office" office.png --model pro --aspect 16:9 --size 4K
```

### Edit an Existing Image

```bash
python scripts/edit_image.py photo.png "remove the background" result.png
```

### Batch Generation

Create a prompts file (`prompts.json`):
```json
[
    {"prompt": "slide 1: intro graphic", "filename": "slide_01.png", "aspect": "16:9"},
    {"prompt": "slide 2: data visualization", "filename": "slide_02.png", "aspect": "16:9"}
]
```

Generate all:
```bash
python scripts/batch_generate.py prompts.json ./output/ --parallel 3
```

Or use a simple text file (one prompt per line):
```bash
python scripts/batch_generate.py prompts.txt ./output/ --aspect 16:9
```

### Multi-turn Editing Session

Start an interactive session:
```bash
python scripts/chat_session.py --output-dir ./images/
```

Resume a previous session:
```bash
python scripts/chat_session.py --session-file session.json
```

Send a single refinement:
```bash
python scripts/chat_session.py --session-file session.json --message "make it more vibrant"
```

## Script Reference

### generate_image.py

Generate a single image from a text prompt.

```
Usage: python scripts/generate_image.py "prompt" output.png [options]

Options:
  --model, -m    Model: flash (default) or pro
  --aspect, -a   Aspect ratio: 1:1 (default), 16:9, 9:16, 21:9, 4:3, 3:4
  --size, -s     Resolution (pro only): 1K, 2K, 4K
```

### edit_image.py

Edit an existing image using text instructions.

```
Usage: python scripts/edit_image.py input.png "instructions" output.png [options]

Options:
  --model, -m    Model: flash (default) or pro
```

### batch_generate.py

Generate multiple images from a prompts file.

```
Usage: python scripts/batch_generate.py prompts.json output_dir/ [options]

Options:
  --model, -m     Model: flash (default) or pro
  --aspect, -a    Default aspect ratio: 1:1 (default)
  --parallel, -p  Number of parallel workers: 1 (default)
  --json          Output results as JSON
```

### chat_session.py

Multi-turn image generation/editing session.

```
Usage: python scripts/chat_session.py [options]

Options:
  --model, -m        Model: flash (default) or pro
  --session-file, -s Path to session state file (JSON)
  --output-dir, -o   Directory for output images: . (default)
  --initial, -i      Initial prompt to start with
  --message          Send single message (non-interactive)
```

## Best Practices

### Prompting Tips

1. **Be specific**: "A red sports car on a mountain road at sunset" works better than "a car".
2. **Describe style**: Include art style, mood, lighting, and camera angle.
3. **Use negative space**: Describe what should NOT be in the image when needed.

### Editing Tips

1. **Target specific elements**: "Change only the sky to purple" is better than "make it purple".
2. **Reference the original**: "Keep the composition but change the color scheme".
3. **Iterative refinement**: Use multi-turn sessions for complex edits.

### Performance

- Use `flash` model for quick iterations and high volume.
- Use `pro` model for final production assets and 4K output.
- Use batch generation with `--parallel` for multiple images.

## Additional Resources

For detailed API documentation, see [references/gemini-api.md](references/gemini-api.md).
For prompting techniques, see [references/prompt-guide.md](references/prompt-guide.md).
For common editing patterns, see [references/editing-patterns.md](references/editing-patterns.md).
