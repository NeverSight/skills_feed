---
name: multimodal-models
description: Use when "CLIP", "Whisper", "Stable Diffusion", "SDXL", "speech-to-text", "text-to-image", "image generation", "transcription", "zero-shot classification", "image-text similarity", "inpainting", "ControlNet"
version: 1.0.0
---

# Multimodal Models

Pre-trained models for vision, audio, and cross-modal tasks.

---

## Model Overview

| Model | Modality | Task |
|-------|----------|------|
| **CLIP** | Image + Text | Zero-shot classification, similarity |
| **Whisper** | Audio → Text | Transcription, translation |
| **Stable Diffusion** | Text → Image | Image generation, editing |

---

## CLIP (Vision-Language)

Zero-shot image classification without training on specific labels.

### CLIP Use Cases

| Task | How |
|------|-----|
| Zero-shot classification | Compare image to text label embeddings |
| Image search | Find images matching text query |
| Content moderation | Classify against safety categories |
| Image similarity | Compare image embeddings |

### CLIP Models

| Model | Parameters | Trade-off |
|-------|------------|-----------|
| ViT-B/32 | 151M | Recommended balance |
| ViT-L/14 | 428M | Best quality, slower |
| RN50 | 102M | Fastest, lower quality |

### CLIP Concepts

| Concept | Description |
|---------|-------------|
| **Dual encoder** | Separate encoders for image and text |
| **Contrastive learning** | Trained to match image-text pairs |
| **Normalization** | Always normalize embeddings before similarity |
| **Descriptive labels** | Better labels = better zero-shot accuracy |

**Key concept**: CLIP embeds images and text in same space. Classification = find nearest text embedding.

### CLIP Limitations

- Not for fine-grained classification
- No spatial understanding (whole image only)
- May reflect training data biases

---

## Whisper (Speech Recognition)

Robust multilingual transcription supporting 99 languages.

### Whisper Use Cases

| Task | Configuration |
|------|---------------|
| Transcription | Default `transcribe` task |
| Translation to English | `task="translate"` |
| Subtitles | Output format SRT/VTT |
| Word timestamps | `word_timestamps=True` |

### Whisper Models

| Model | Size | Speed | Recommendation |
|-------|------|-------|----------------|
| turbo | 809M | Fast | **Recommended** |
| large | 1550M | Slow | Maximum quality |
| small | 244M | Medium | Good balance |
| base | 74M | Fast | Quick tests |
| tiny | 39M | Fastest | Prototyping only |

### Whisper Concepts

| Concept | Description |
|---------|-------------|
| **Language detection** | Auto-detects, or specify for speed |
| **Initial prompt** | Improves technical terms accuracy |
| **Timestamps** | Segment-level or word-level |
| **faster-whisper** | 4× faster alternative implementation |

**Key concept**: Specify language when known—auto-detection adds latency.

### Whisper Limitations

- May hallucinate on silence/noise
- No speaker diarization (who said what)
- Accuracy degrades on >30 min audio
- Not suitable for real-time captioning

---

## Stable Diffusion (Image Generation)

Text-to-image generation with various control methods.

### SD Use Cases

| Task | Pipeline |
|------|----------|
| Text-to-image | `DiffusionPipeline` |
| Style transfer | `Image2Image` |
| Fill regions | `Inpainting` |
| Guided generation | `ControlNet` |
| Custom styles | LoRA adapters |

### SD Models

| Model | Resolution | Quality |
|-------|------------|---------|
| SDXL | 1024×1024 | Best |
| SD 1.5 | 512×512 | Good, faster |
| SD 2.1 | 768×768 | Middle ground |

### Key Parameters

| Parameter | Effect | Typical Value |
|-----------|--------|---------------|
| **num_inference_steps** | Quality vs speed | 20-50 |
| **guidance_scale** | Prompt adherence | 7-12 |
| **negative_prompt** | Avoid artifacts | "blurry, low quality" |
| **strength** (img2img) | How much to change | 0.5-0.8 |
| **seed** | Reproducibility | Fixed number |

### Control Methods

| Method | Input | Use Case |
|--------|-------|----------|
| **ControlNet** | Edge/depth/pose | Structural guidance |
| **LoRA** | Trained weights | Custom styles |
| **Img2Img** | Source image | Style transfer |
| **Inpainting** | Image + mask | Fill regions |

### Memory Optimization

| Technique | Effect |
|-----------|--------|
| CPU offload | Reduces VRAM usage |
| Attention slicing | Trades speed for memory |
| VAE tiling | Large image support |
| xFormers | Faster attention |
| DPM scheduler | Fewer steps needed |

**Key concept**: Use SDXL for quality, SD 1.5 for speed. Always use negative prompts.

### SD Limitations

- GPU strongly recommended (CPU very slow)
- Large VRAM requirements for SDXL
- May generate anatomical errors
- Prompt engineering matters

---

## Common Patterns

### Embedding and Similarity

All three models use embeddings:

- CLIP: Image/text embeddings for similarity
- Whisper: Audio embeddings for transcription
- SD: Text embeddings for image conditioning

### GPU Acceleration

| Model | VRAM Needed |
|-------|-------------|
| CLIP ViT-B/32 | ~2 GB |
| Whisper turbo | ~6 GB |
| SD 1.5 | ~6 GB |
| SDXL | ~10 GB |

### Best Practices

| Practice | Why |
|----------|-----|
| Use recommended model sizes | Best quality/speed balance |
| Cache embeddings (CLIP) | Expensive to recompute |
| Specify language (Whisper) | Faster than auto-detect |
| Use negative prompts (SD) | Avoid common artifacts |
| Set seeds for reproducibility | Consistent results |

## Resources

- CLIP: <https://github.com/openai/CLIP>
- Whisper: <https://github.com/openai/whisper>
- Diffusers: <https://huggingface.co/docs/diffusers>
