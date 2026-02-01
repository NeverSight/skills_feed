---
name: speech-build
description: Generate and transcribe speech using Google's Gemini-TTS and Chirp 3 models. Supports Text-to-Speech (Single/Multi-speaker), Instant Custom Voice, and Speech-to-Text (Transcription/Diarization).
---

# Speech Skill (TTS & STT)

Use this skill to implement audio generation and transcription workflows using the `google-genai` and `google-cloud-speech` SDKs.

## Quick Start Setup

```python
from google import genai
from google.genai import types
# For STT: from google.cloud import speech_v2

client = genai.Client()
```

## Reference Materials

- **[Text-to-Speech (TTS)](references/tts.md)**: Gemini-TTS, Chirp 3 HD, Instant Custom Voice.
- **[Speech-to-Text (STT)](references/stt.md)**: Chirp 3 Transcription, Diarization, Streaming.
- **[Voices & Locales](references/voices.md)**: Available voices (`Aoede`, `Puck`...) and languages.
- **[Prompting Guide](references/prompting.md)**: How to control style, accent, and pacing in Gemini-TTS.
- **[Source Code](references/source_code.md)**: Deep inspection of SDK internals.

## Common Workflows

### 1. Generate Speech (Gemini-TTS)
```python
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents="Hello, world!",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
            )
        )
    )
)
```

### 2. Transcribe Audio (Chirp 3)
```python
# Requires google-cloud-speech
from google.cloud import speech_v2
# ... (See stt.md for full setup)
response = speech_client.recognize(...)
```