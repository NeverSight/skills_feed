---
name: speech-use
description: "Generate (TTS), Transcribe (STT), and Clone voices using Google's GenAI and Cloud Speech SDKs. Supports Gemini-TTS, Chirp 3, and Instant Custom Voice."
---

# Speech Use

Use this skill to perform Text-to-Speech (TTS), Speech-to-Text (STT), and Voice Cloning operations.

This skill uses portable Python scripts managed by `uv`.

## Prerequisites

1.  **Environment Variables**:
    *   `GOOGLE_API_KEY` (for TTS via Gemini)
    *   `GOOGLE_CLOUD_PROJECT` (Required for STT and Voice Cloning)
    *   `GOOGLE_APPLICATION_CREDENTIALS` (Recommended for STT/Voice Cloning)

2.  **APIs Enabled**:
    *   Text-to-Speech API (`texttospeech.googleapis.com`)
    *   Speech-to-Text API (`speech.googleapis.com`)

## Usage

### 1. Generate Speech (TTS)

Generate audio from text using Gemini-TTS.

**Standard Voice:**
```bash
uv run skills/speech-use/scripts/generate_speech.py "Hello world, this is a test." --voice Puck --output hello.wav
```

**Custom Voice (Cloned):**
```bash
uv run skills/speech-use/scripts/generate_speech.py "This is my custom voice speaking." --voice-cloning-key "YOUR_KEY_HERE" --output custom.wav
```

### 2. Create Custom Voice (Voice Cloning)

Generate a `voiceCloningKey` from a reference audio file and a consent file.

**Requirements:**
*   `reference.wav`: 10-30s of clear speech (the voice to clone).
*   `consent.wav`: The speaker saying: *"I am the owner of this voice and I consent to Google using this voice to create a synthetic voice model."*

```bash
uv run skills/speech-use/scripts/create_custom_voice.py --reference-audio reference.wav --consent-audio consent.wav
```
*Save the output key to use with `generate_speech.py`.*

### 3. Transcribe Audio (STT)

Transcribe audio files using Chirp 3.

```bash
uv run skills/speech-use/scripts/transcribe_audio.py audio.wav --language en-US --output transcript.txt
```

## Options

**generate_speech.py**
*   `--voice`: Prebuilt voice (e.g., `Kore`, `Puck`, `Fenrir`, `Aoede`).
*   `--voice-cloning-key`: Key from `create_custom_voice.py`.
*   `--model`: Default `gemini-2.5-flash-preview-tts`.

**transcribe_audio.py**
*   `--model`: Default `chirp_3`.
*   `--language`: Default `auto`.
*   `--location`: Cloud region (default `us`).