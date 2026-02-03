---
name: qwen3-tts-mlx
description: Local Qwen3-TTS speech synthesis on Apple Silicon via MLX. Use for offline narration, audiobooks, video voiceovers, and multilingual TTS.
metadata:
  author: agiseek
  version: "1.2.0"
---

# Qwen3-TTS MLX

Run Qwen3-TTS locally on Apple Silicon (M1/M2/M3/M4) using MLX. Supports 11 languages, 9 built-in voices, voice cloning, and voice design from text descriptions.

## When to Use

- Generate speech fully offline on a Mac
- Produce narration, audiobooks, podcasts, or video voiceovers
- Create multilingual TTS with controllable style and emotion
- Clone any voice from a short audio sample
- Design custom voices from text descriptions

## Quick Start

### Install

```bash
pip install mlx-audio
brew install ffmpeg
```

### Basic Usage

```bash
python scripts/run_tts.py custom-voice \
  --text "Hello, welcome to local text to speech." \
  --voice Ryan \
  --output output.wav
```

### With Style Control

```bash
python scripts/run_tts.py custom-voice \
  --text "Breaking news: local AI model achieves human-level speech." \
  --voice Uncle_Fu \
  --instruct "news anchor tone, calm and authoritative" \
  --output news.wav
```

## Model Variants

| Variant | Model | Size | Memory | Use Case |
|---------|-------|------|--------|----------|
| CustomVoice | `mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-4bit` | ~1GB | ~4GB | Built-in voices + style control (recommended) |
| VoiceDesign | `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-5bit` | ~2GB | ~5GB | Create voices from text descriptions |
| Base | `mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit` | ~1GB | ~4GB | Voice cloning from reference audio |

## Supported Languages

| Language | Code | Notes |
|----------|------|-------|
| Auto-detect | `auto` | Default, detects from text |
| Chinese | `Chinese` | Mandarin |
| English | `English` | |
| Japanese | `Japanese` | |
| Korean | `Korean` | |
| French | `French` | |
| German | `German` | |
| Spanish | `Spanish` | |
| Portuguese | `Portuguese` | |
| Italian | `Italian` | |
| Russian | `Russian` | |

## Built-in Voices

| Voice | Language | Character |
|-------|----------|-----------|
| Vivian | Chinese | Female, bright, young |
| Serena | Chinese | Female, gentle, soft |
| Uncle_Fu | Chinese | Male, authoritative, news anchor |
| Dylan | Chinese | Male, Beijing dialect |
| Eric | Chinese | Male, Sichuan dialect |
| Ryan | English | Male, energetic |
| Aiden | English | Male, clear, neutral |
| Ono_Anna | Japanese | Female |
| Sohee | Korean | Female |

**Voice Selection Guide:**

| Scenario | Recommended Voice |
|----------|-------------------|
| Chinese news/narration | Uncle_Fu |
| Chinese casual/lively | Eric |
| Chinese female, professional | Vivian |
| Chinese female, storytelling | Serena |
| English energetic content | Ryan |
| English neutral/educational | Aiden |
| Japanese content | Ono_Anna |
| Korean content | Sohee |

## Modes

### 1) CustomVoice

Use built-in voices with optional emotion/style control via `--instruct`.

```bash
python scripts/run_tts.py custom-voice \
  --text "This is amazing news!" \
  --voice Vivian \
  --instruct "excited and happy" \
  --output excited.wav
```

**Style instruction examples:**
- `"calm and warm"` - Soft, friendly delivery
- `"news anchor, authoritative"` - Professional broadcast style
- `"excited and energetic"` - High energy, enthusiastic
- `"sad and melancholic"` - Emotional, somber tone
- `"whispering, intimate"` - Quiet, close-mic feel

### 2) VoiceDesign

Create a completely new voice by describing it in natural language.

```bash
python scripts/run_tts.py voice-design \
  --text "Welcome to our podcast." \
  --instruct "warm, mature male narrator with low pitch and gentle tone" \
  --output podcast_intro.wav
```

**Voice description examples:**
- `"young cheerful female with high pitch"`
- `"elderly wise male with deep resonant voice"`
- `"professional female news anchor, clear articulation"`
- `"friendly young male, casual and relaxed"`

### 3) VoiceClone

Clone any voice from a reference audio sample (5-10 seconds recommended).

```bash
python scripts/run_tts.py voice-clone \
  --text "This is my cloned voice speaking new content." \
  --ref_audio reference.wav \
  --ref_text "The exact transcript of the reference audio" \
  --output cloned.wav
```

**Tips for voice cloning:**
- Use clean audio without background noise
- 5-10 seconds of speech works best
- Provide accurate transcript of the reference
- Reference and output language should match

## CLI Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--text` | Yes | - | Text to synthesize |
| `--voice` | No | Vivian | Built-in voice (CustomVoice only) |
| `--lang_code` | No | auto | Language code |
| `--instruct` | No | - | Style control or voice description |
| `--speed` | No | 1.0 | Speech speed multiplier |
| `--temperature` | No | 0.7 | Sampling temperature (higher = more variation) |
| `--model` | No | (per mode) | Override default model |
| `--output` | No | - | Output file path |
| `--out-dir` | No | ./outputs | Output directory when --output not set |
| `--ref_audio` | VoiceClone | - | Reference audio file |
| `--ref_text` | VoiceClone | - | Reference audio transcript |

## Python API

### Using generate_audio (recommended)

```python
from mlx_audio.tts.generate import generate_audio

# CustomVoice with style control
generate_audio(
    text="Hello from Qwen3-TTS!",
    model="mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-4bit",
    voice="Ryan",
    lang_code="english",
    instruct="friendly and warm",
    output_path=".",
    file_prefix="hello",
    audio_format="wav",
    join_audio=True,
    verbose=True,
)
```

### Using Model directly

```python
from mlx_audio.tts.utils import load
import soundfile as sf
import numpy as np

# Load model
model = load("mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-4bit")

# Generate audio (returns a generator)
audio_chunks = []
for chunk in model.generate_custom_voice(
    text="Hello from Qwen3-TTS.",
    speaker="Ryan",
    language="english",
    instruct="clear, steady delivery"
):
    if hasattr(chunk, 'audio') and chunk.audio is not None:
        audio_chunks.append(chunk.audio)

# Combine and save
audio = np.concatenate(audio_chunks)
sf.write("output.wav", audio, 24000)
```

### VoiceDesign

```python
from mlx_audio.tts.generate import generate_audio

generate_audio(
    text="Welcome to the show.",
    model="mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-5bit",
    instruct="warm, friendly female narrator with medium pitch",
    lang_code="english",
    output_path=".",
    file_prefix="voice_design",
    join_audio=True,
)
```

### VoiceClone

```python
from mlx_audio.tts.generate import generate_audio

generate_audio(
    text="New content in the cloned voice.",
    model="mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit",
    ref_audio="reference.wav",
    ref_text="Transcript of the reference audio",
    output_path=".",
    file_prefix="cloned",
    join_audio=True,
)
```

## Batch Processing

Use `scripts/batch_dubbing.py` for processing multiple lines:

```bash
python scripts/batch_dubbing.py \
  --input dubbing.json \
  --out-dir outputs
```

See `references/dubbing_format.md` for the JSON format.

## Performance

| Metric | Value |
|--------|-------|
| Sample rate | 24,000 Hz |
| Real-time factor | ~0.7x (faster than real-time) |
| Peak memory | ~4-6 GB |
| First run | Downloads model (~1-2GB) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow generation | Use 4-bit CustomVoice model |
| Unnatural pauses | Add punctuation, keep sentences short |
| Wrong language detected | Specify `--lang_code` explicitly |
| Voice cloning quality | Use cleaner reference audio, accurate transcript |
| Tokenizer warnings | Harmless, can be ignored |
| Out of memory | Close other apps, use 4-bit model |
