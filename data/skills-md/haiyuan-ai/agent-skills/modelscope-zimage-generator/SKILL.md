---
name: modelscope-zimage-generator
description: Generate images using ModelScope Z-Image models (Z-Image-Turbo, Z-Image-Base, Z-Image-Edit). Use when user asks to generate images, create artwork, or requests image generation functionality. Supports async generation with polling and optional LoRA configurations.
---

# ModelScope Z-Image Generator

Generate images using ModelScope's Z-Image series models.

## IMPORTANT: Response Format

After generating an image, you MUST:
1. Use the Python script to generate the image
2. Respond with ONLY a simple text message like: "Image saved to: /path/to/output.jpg"
3. DO NOT include the image URL in your response
4. DO NOT try to display or reference the image URL - this will cause errors with non-multimodal models

The user can view the generated image at the file path you provide.

## Prerequisites

Get your ModelScope API key from: https://modelscope.cn/my/myaccesstoken

The script will automatically prompt for your API key the first time you use it and offer to save it for future use.

**Optional: Manual Configuration**

You can also manually configure the API key:

**Config file:**
```bash
mkdir -p ~/.config/modelscope
cat > ~/.config/modelscope/config.json << EOF
{
  "api_key": "ms-your-api-key-here"
}
EOF
```

**Environment variable:**
```bash
export MODELSCOPE_API_KEY="ms-your-api-key-here"
```

## Quick Start

Use the Python script to generate images:

```bash
cd /Users/ningoo/.claude/skills/modelscope-image-generator/scripts
python generate_image.py "A golden cat" output.jpg
```

## Models

Available Z-Image models:

- `Tongyi-MAI/Z-Image-Turbo` (default, fast generation)
- `Tongyi-MAI/Z-Image-Base` (higher quality)
- `Tongyi-MAI/Z-Image-Edit` (image editing)

Specify a different model using the third argument:
```bash
python generate_image.py "A golden cat" output.jpg "Tongyi-MAI/Z-Image-Base"
```

## LoRA Support

Single LoRA:

```python
"loras": "<lora-repo-id>"
```

Multiple LoRAs (weights must sum to 1.0):

```python
"loras": {"<lora-id1>": 0.6, "<lora-id2>": 0.4}
```

## API Flow

1. Submit generation request with `X-ModelScope-Async-Mode: true`
2. Receive `task_id` in response
3. Poll `/v1/tasks/{task_id}` with `X-ModelScope-Task-Type: image_generation`
4. Wait for status `SUCCEED` or `FAILED`
5. Download image from `output_images[0]` URL
