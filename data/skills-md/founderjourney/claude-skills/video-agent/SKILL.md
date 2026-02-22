---
name: video-agent
description: AI content generation suite with 35+ models. Image generation, video creation, audio processing via FAL AI, Google Vertex AI, ElevenLabs. Pipeline orchestration and cost management.
original_source: https://github.com/donghaozhang/video-agent-claude-skill
author: donghaozhang
license: MIT
---

# Video Agent - AI Content Generation Suite

A comprehensive AI content generation package providing a unified interface across 35+ models for image, video, and audio creation.

## When to Use This Skill

- Text-to-image generation
- Image-to-image transformations
- Text-to-video creation
- Image-to-video animation
- Professional text-to-speech
- Multi-step content pipelines
- Batch content generation

## Supported Providers

### FAL AI
- FLUX models (text-to-image)
- Image transformations
- Fast inference

### Google Vertex AI
- Imagen 4 (text-to-image)
- Veo (text-to-video)
- High quality outputs

### ElevenLabs
- 20+ voice options
- Professional TTS
- Multiple languages

### OpenRouter
- Access to various LLMs
- Text generation
- Content writing

## Core Capabilities

### Image Generation

```
Generate image:
Prompt: "A serene Japanese garden at sunset"
Model: flux-pro
Size: 1024x1024
Style: photorealistic
```

**Available Models:**
- FLUX Pro/Dev (FAL)
- Imagen 4 (Google)
- Stable Diffusion variants

### Video Creation

```
Generate video:
Prompt: "Ocean waves crashing on rocky shore"
Model: veo
Duration: 5 seconds
Resolution: 1080p
```

**Available Models:**
- Google Veo
- MiniMax Hailuo
- Kling

### Image-to-Video

```
Animate image:
Source: /path/to/image.png
Motion: "gentle zoom out with particle effects"
Duration: 4 seconds
```

### Text-to-Speech

```
Generate audio:
Text: "Welcome to our product demo..."
Voice: professional-female-1
Speed: 1.0
Output: welcome.mp3
```

**Voice Options:**
- Professional male/female
- Casual conversational
- Narrator styles
- Multiple accents

## Pipeline Orchestration

### YAML Configuration

```yaml
pipeline: product-demo
steps:
  - name: generate-logo
    type: image
    model: flux-pro
    prompt: "Modern tech logo for AI startup"

  - name: create-intro
    type: video
    model: veo
    prompt: "Logo animation reveal"

  - name: add-voiceover
    type: audio
    model: elevenlabs
    text: "Introducing the future of AI..."
    voice: professional-male

  - name: combine
    type: merge
    inputs: [create-intro, add-voiceover]
```

### JSON Configuration

```json
{
  "pipeline": "social-content",
  "parallel": true,
  "steps": [
    {
      "type": "image",
      "variants": 4,
      "prompt": "Product hero shot"
    }
  ]
}
```

## Cost Management

### Real-time Estimation

```
Estimate cost for:
- 10 images (1024x1024)
- 2 videos (5 seconds)
- 1 audio (60 seconds)

Estimated: $2.45
```

### Budget Limits

```yaml
budget:
  max_per_job: $5.00
  max_daily: $50.00
  alert_threshold: 80%
```

## Performance Features

### Parallel Execution

```
Generate 10 image variants in parallel
Threads: 4
Expected speedup: 2-3x
```

### Caching

- Automatic prompt caching
- Reuse similar generations
- Reduce redundant API calls

## CLI Commands

```bash
# Image generation
video-agent image "prompt" --model flux-pro --size 1024

# Video generation
video-agent video "prompt" --model veo --duration 5

# Audio generation
video-agent audio "text" --voice professional-female

# Pipeline execution
video-agent pipeline config.yaml

# Cost check
video-agent cost --estimate
```

## Python API

```python
from video_agent import ImageGenerator, VideoGenerator

# Generate image
img = ImageGenerator(model="flux-pro")
result = img.generate("sunset over mountains")

# Generate video
vid = VideoGenerator(model="veo")
result = vid.generate("timelapse of clouds")
```

## Setup

### 1. Install Package
```bash
pip install video-agent-claude-skill
```

### 2. Configure API Keys
```bash
export FAL_API_KEY="your-key"
export GOOGLE_VERTEX_KEY="your-key"
export ELEVENLABS_API_KEY="your-key"
```

### 3. Verify Setup
```bash
video-agent status
```

## Use Cases

- **Marketing**: Product images, promo videos
- **Social Media**: Content at scale
- **Education**: Explainer videos, voiceovers
- **Prototyping**: Visual concepts, mockups
- **Automation**: Batch content pipelines

## Credits

Created by [donghaozhang](https://github.com/donghaozhang/video-agent-claude-skill). Licensed under MIT.
