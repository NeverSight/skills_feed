---
name: nano-banana-use
description: "Generate, edit, and compose images using Gemini Nano Banana models via portable Python scripts. Handles authentication via API Key or Vertex AI environment variables. Available parameters: prompt, model, aspect-ratio, safety-filter-level. Always confirm parameters with the user or explicitly state defaults before running."
---

# Nano Banana Use

Use this skill to generate, edit, and compose images using Gemini's Nano Banana models (`gemini-2.5-flash-image` and `gemini-3-pro-image-preview`).

This skill uses portable Python scripts managed by `uv`.

## Prerequisites

Ensure you have one of the following authentication methods configured in your environment:

1.  **API Key**:
    -   `GOOGLE_API_KEY` or `GEMINI_API_KEY`

2.  **Vertex AI**:
    -   `GOOGLE_CLOUD_PROJECT`
    -   `GOOGLE_CLOUD_LOCATION`
    -   `GOOGLE_GENAI_USE_VERTEXAI=1`

## Usage

### Generate an Image

**Step 1: Confirm Parameters**
Before running the script, confirm the following parameters with the user or state the defaults you will use:
-   **Prompt**: The image description.
-   **Model**: Default is `gemini-3-pro-image-preview`.
-   **Aspect Ratio**: Default is `1:1`.
-   **Safety Filter**: Default is `BLOCK_MEDIUM_AND_ABOVE`.

**Step 2: Run the Script**
Run the python script using `uv`:

```bash
uv run skills/nano-banana-use/scripts/generate_image.py "A futuristic banana city" --output city.png
```

### Edit an Image

Modify an existing image based on a text prompt.

```bash
uv run skills/nano-banana-use/scripts/edit_image.py original.png "Make the sky purple" --output edited.png
```

### Compose Images

Generate a new image based on multiple input images and a prompt.

```bash
uv run skills/nano-banana-use/scripts/compose_image.py --image style.png --image subject.jpg "A painting of the subject in the style of the first image" --output composition.png
```

### Options

-   `prompt`: The text description of the image.
-   `--model`: The model to use. Defaults to `gemini-3-pro-image-preview`.
-   `--output`: The filename for the saved image. Defaults to `generated_image.png`.
-   `--aspect-ratio`: The aspect ratio of the generated image. Defaults to `1:1`. Supported: `1:1`, `16:9`, `4:3`, `3:4`, `9:16`.
-   `--safety-filter-level`: Safety filter threshold. Defaults to `BLOCK_MEDIUM_AND_ABOVE`.
