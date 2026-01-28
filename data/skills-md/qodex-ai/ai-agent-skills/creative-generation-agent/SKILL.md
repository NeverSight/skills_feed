---
name: creative-generation-agent
description: Build agents that generate creative content including music, memes, podcasts, and multimedia. Covers generative models, content synthesis, style transfer, and creative control. Use when building creative assistants, automated content creators, multimedia generators, or artistic AI systems.
---

# Creative Generation Agent

Build intelligent agents that generate original creative content across multiple modalities including text, music, images, memes, and podcasts.

## Overview

Creative generation combines:
- **Content Models**: Diffusion models, transformers, GANs
- **Prompt Engineering**: Guide creative output
- **Style Control**: Maintain artistic consistency
- **Quality Assessment**: Evaluate creative output
- **Iteration & Refinement**: Improve results

### Applications

- AI music composition and arrangement
- Automated meme generation
- Podcast script and audio generation
- Creative writing assistance
- Art and image generation
- Video content creation
- Game asset generation

## Quick Start

Extract the code examples and utilities from the directories:

- **Examples**: See [`examples/`](examples/) directory for complete implementations:
  - [`music_generation.py`](examples/music_generation.py) - Music generation and audio synthesis
  - [`meme_generator.py`](examples/meme_generator.py) - Image and text-based meme generation
  - [`podcast_producer.py`](examples/podcast_producer.py) - Podcast script and audio production
  - [`image_generation.py`](examples/image_generation.py) - Diffusion-based image generation
  - [`style_transfer.py`](examples/style_transfer.py) - Neural style transfer

- **Utilities**: See [`scripts/`](scripts/) directory for helper modules:
  - [`creative_quality_assessment.py`](scripts/creative_quality_assessment.py) - Quality evaluation
  - [`audio_effects.py`](scripts/audio_effects.py) - Audio effect processing
  - [`content_moderation.py`](scripts/content_moderation.py) - Safety and compliance filtering

## Music Generation

### 1. Symbolic Music Generation

Generate music as MIDI/musical notation. See [`examples/music_generation.py`](examples/music_generation.py).

**Key Classes:**
- `MusicGenerationAgent` - Generates melodies and full compositions
- Methods: `generate_melody()`, `generate_full_composition()`, `generate_harmony()`

**Usage:**
```python
from examples.music_generation import MusicGenerationAgent

agent = MusicGenerationAgent()
melody = agent.generate_melody(
    seed_notes=[("C4", 1), ("E4", 1), ("G4", 1)],
    length=32,
    temperature=0.8
)
composition = agent.generate_full_composition(style="classical", duration_bars=32)
```

### 2. Audio Synthesis

Generate audio waveforms directly. See [`examples/music_generation.py`](examples/music_generation.py).

**Key Classes:**
- `AudioSynthesisAgent` - Synthesizes audio from MIDI and applies effects

**Usage:**
```python
from examples.music_generation import AudioSynthesisAgent

synth = AudioSynthesisAgent(sample_rate=44100)
audio = synth.synthesize_from_midi(midi_data, duration_seconds=60)
audio = synth.add_effects(audio, effect_type="reverb")
synth.save_audio(audio, "output.wav")
```

## Meme Generation

See [`examples/meme_generator.py`](examples/meme_generator.py) for complete implementations.

### 1. Image-Based Meme Generator

Generate memes by applying captions to templates.

**Key Classes:**
- `MemeGenerationAgent` - Generates image-based memes with captions
- Methods: `generate_meme()`, `generate_caption()`, `apply_caption_to_template()`

**Usage:**
```python
from examples.meme_generator import MemeGenerationAgent

agent = MemeGenerationAgent()
meme = agent.generate_meme(topic="AI agents", meme_template="drake")
meme.save("output_meme.png")
```

### 2. Text-Based Meme Generator

Generate text-only memes in various formats.

**Key Classes:**
- `TextMemeGenerator` - Generates text-based memes
- Methods: `generate_text_meme()`, `generate_joke_meme()`, `generate_deep_meme()`

**Usage:**
```python
from examples.meme_generator import TextMemeGenerator

generator = TextMemeGenerator()
joke_meme = generator.generate_text_meme(topic="Python programming", format_type="joke")
deep_meme = generator.generate_text_meme(topic="AI", format_type="deep")
```

## Podcast Generation

See [`examples/podcast_producer.py`](examples/podcast_producer.py) for complete implementations.

### 1. Script Generation

Generate podcast scripts with structure and natural conversation flow.

**Key Classes:**
- `PodcastScriptGenerator` - Creates scripts from topics
- Methods: `generate_episode()`, `generate_script()`, `generate_content_segments()`, `generate_intro()`, `generate_outro()`

**Usage:**
```python
from examples.podcast_producer import PodcastScriptGenerator

generator = PodcastScriptGenerator()
episode = generator.generate_episode(
    topic="Future of AI",
    duration_minutes=30,
    num_hosts=2
)

print(episode["script"])
```

### 2. Audio Production

Convert scripts to audio with text-to-speech and effects.

**Key Classes:**
- `PodcastAudioProducer` - Produces audio from podcast scripts
- Methods: `produce_podcast()`, `text_to_speech()`, `add_background_music()`, `add_transitions()`

**Usage:**
```python
from examples.podcast_producer import PodcastAudioProducer

producer = PodcastAudioProducer()
audio = producer.produce_podcast(script_text)
```

## Image and Art Generation

See [`examples/image_generation.py`](examples/image_generation.py) and [`examples/style_transfer.py`](examples/style_transfer.py).

### 1. Diffusion Model Integration

Generate images from text prompts using Stable Diffusion or similar models.

**Key Classes:**
- `ImageGenerationAgent` - Generates images from text prompts
- Methods: `generate_image()`, `enhance_prompt()`, `generate_variations()`

**Usage:**
```python
from examples.image_generation import ImageGenerationAgent

agent = ImageGenerationAgent()
image = agent.generate_image(
    prompt="A futuristic city with neon lights",
    style="cyberpunk",
    num_inference_steps=50
)
image.save("generated_image.png")

variations = agent.generate_variations(image, num_variations=4)
```

### 2. Style Transfer

Transfer artistic style from one image to another.

**Key Classes:**
- `StyleTransferAgent` - Applies style transfer between images
- Methods: `transfer_style()`, `preprocess_image()`, `postprocess_image()`

**Usage:**
```python
from examples.style_transfer import StyleTransferAgent

agent = StyleTransferAgent()
stylized = agent.transfer_style(
    content_image="photo.jpg",
    style_image="monet_painting.jpg"
)
```

## Quality Assessment

See [`scripts/creative_quality_assessment.py`](scripts/creative_quality_assessment.py) for complete implementations.

### 1. Creative Quality Metrics

Evaluate generated content across multiple quality dimensions.

**Key Classes:**
- `CreativeQualityAssessor` - Assesses quality of all content types
- Methods: `assess_content_quality()`, `assess_music_quality()`, `assess_meme_quality()`, `assess_image_quality()`

**Usage:**
```python
from scripts.creative_quality_assessment import CreativeQualityAssessor

assessor = CreativeQualityAssessor()

# Assess music quality
music_assessment = assessor.assess_content_quality(audio, content_type="music")
print(f"Overall score: {music_assessment['overall_score']}")
print(f"Metrics: {music_assessment['metrics']}")

# Assess meme quality
meme_assessment = assessor.assess_content_quality(meme, content_type="meme")

# Assess image quality
image_assessment = assessor.assess_content_quality(image, content_type="image")
```

## Best Practices

### Content Generation
- ✓ Start with clear style/mood specifications
- ✓ Use temperature wisely (0.7-0.9 for creativity, 0.3-0.5 for consistency)
- ✓ Implement iterative refinement
- ✓ Maintain seed values for reproducibility
- ✓ Test with diverse prompts

### Quality Control
- ✓ Assess generated content systematically (see [`creative_quality_assessment.py`](scripts/creative_quality_assessment.py))
- ✓ Implement human review loops
- ✓ Track quality metrics over time
- ✓ Use feedback to refine models
- ✓ Version different creative styles

### Audio Processing
- ✓ Use audio effects wisely (see [`audio_effects.py`](scripts/audio_effects.py))
  - Reverb for spatial depth
  - Compression for dynamic control
  - EQ for frequency balance
  - Fade in/out for smooth transitions
- ✓ Monitor audio levels to prevent clipping
- ✓ Mix multiple tracks appropriately

### Content Moderation
- ✓ Filter inappropriate content (see [`content_moderation.py`](scripts/content_moderation.py))
- ✓ Ensure copyright compliance
- ✓ Validate factual accuracy
- ✓ Check for bias in generation
- ✓ Implement safety guidelines
- ✓ Use strict mode for sensitive applications

## Implementation Checklist

- [ ] Choose content modality (music, images, text, etc.)
- [ ] Select generation model/framework
- [ ] Implement prompt engineering
- [ ] Set up quality assessment metrics
- [ ] Create iterative refinement loop
- [ ] Build content moderation system
- [ ] Test generation across diverse inputs
- [ ] Optimize for speed/quality tradeoff
- [ ] Implement version control for outputs
- [ ] Document prompting strategies

## Resources

### Music Generation
- **Music Transformer**: https://magenta.tensorflow.org/
- **MuseNet**: https://openai.com/blog/musenet/
- **music21**: https://web.mit.edu/music21/

### Image Generation
- **Stable Diffusion**: https://huggingface.co/runwayml/stable-diffusion-v1-5
- **DALL-E**: https://openai.com/dall-e/
- **Midjourney**: https://www.midjourney.com/

### Audio Synthesis
- **Jukebox**: https://openai.com/research/jukebox
- **Chirp**: https://deepmind.google/discover/blog/chirp-universal-speech-model/

### Video Generation
- **Runway**: https://runwayml.com/
- **Pika**: https://pika.art/

