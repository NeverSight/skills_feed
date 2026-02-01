---
name: veo-use
description: "Create and edit videos using Google's Veo 2 and Veo 3 models. Supports Text-to-Video, Image-to-Video, Reference-to-Video, Inpainting, and Video Extension. Available parameters: prompt, image, mask, mode, duration, aspect-ratio. Always confirm parameters with the user or explicitly state defaults before running."
---

# Veo Use

Use this skill to generate and edit videos using Google's Veo models (`veo-3.1` and `veo-2.0`).

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

### 1. Text to Video

Generate a video purely from a text description.

```bash
uv run skills/veo-use/scripts/text_to_video.py "A cinematic drone shot of a futuristic city" --output city.mp4
```

### 2. Image to Video

Generate a video starting from a static image context.

```bash
uv run skills/veo-use/scripts/image_to_video.py "Zoom out from the flower" --image start.png --output flower.mp4
```

### 3. Reference to Video

Use specific asset images (subjects, products) to guide generation.

```bash
uv run skills/veo-use/scripts/reference_to_video.py "A man walking on the moon" --reference-image man.png --output moon_walk.mp4
```

### 4. Edit Video (Inpainting)

Modify existing videos using masks.

**Modes:**
-   `REMOVE`: Remove dynamic object.
-   `REMOVE_STATIC`: Remove static object (watermark).
-   `INSERT`: Insert new object (requires `--prompt`).

```bash
uv run skills/veo-use/scripts/edit_video.py --video input.mp4 --mask mask.png --mode INSERT --prompt "A flying car" --output edited.mp4
```

### 5. Extend Video

Extend the duration of an existing video clip.

```bash
uv run skills/veo-use/scripts/extend_video.py --video clip.mp4 --prompt "The car flies away into the sunset" --duration 6 --output extended.mp4
```

### Common Options

-   `--model`: Default `veo-3.1-generate-001`.
-   `--resolution`: `1080p` (default), `720p`, `4k`.
-   `--aspect-ratio`: `16:9` (default), `9:16`.
-   `--duration`: `6` (default), `4`, `8`.
