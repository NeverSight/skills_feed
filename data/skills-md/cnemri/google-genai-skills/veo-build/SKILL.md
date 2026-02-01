---
name: veo-build
description: Create and edit videos using Google's Veo 2 and Veo 3 models. Supports Text-to-Video, Image-to-Video, Inpainting, and Advanced Controls.
---

# Veo Video Generation and Editing

This skill provides comprehensive workflows for using Google's Veo models (Veo 2 and Veo 3) via the `google-genai` Python SDK.

## Quick Start Setup

All Veo operations require the `google-genai` library and an authenticated client with Vertex AI enabled.

```python
from google import genai
from google.genai import types
import os

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
```

## Reference Materials

- **[Generation (Veo 3)](references/generation.md)**: Text-to-Video, Image-to-Video.
- **[Editing (Veo 2)](references/editing.md)**: Inpainting, Masking.
- **[Advanced Controls](references/advanced.md)**: Frame Interpolation, Video Extension, Reference Images.
- **[Prompting Guide](references/prompting.md)**: Camera angles, visual styles, and best practices.
- **[Source Code](references/source_code.md)**: Deep inspection of SDK internals (`models.py`, `types.py`).

## Available Workflows

### 1. Video Generation (Veo 3)
Create new videos from text or image prompts.
- **Text-to-Video**: Create videos from detailed text descriptions.
- **Image-to-Video**: Animate static images.
- **Prompt Engineering**: Optimization keywords for camera, lighting, and style.

### 2. Video Editing (Veo 2)
Modify existing videos using masks (Inpainting).
- **Remove Objects**: Erase dynamic or static objects.
- **Insert Objects**: Add new elements into a scene.

### 3. Advanced Controls (Veo 3)
Specialized generation tasks for precise control.
- **Frame Interpolation**: Generate video bridging two images (first & last frame).
- **Video Extension**: Extend the duration of an existing video clip.
- **Reference-to-Video**: Use specific asset images (subjects, products) to guide generation.