---
name: eachlabs-voice-audio
description: Text-to-speech, speech-to-text, voice conversion, and audio processing using EachLabs AI models. Supports ElevenLabs TTS, Whisper transcription with diarization, and RVC voice conversion. Use when the user needs TTS, transcription, or voice conversion.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Voice & Audio

Text-to-speech, speech-to-text transcription, voice conversion, and audio utilities via the EachLabs Predictions API.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Available Models

### Text-to-Speech

| Model | Slug | Best For |
|-------|------|----------|
| ElevenLabs TTS | `elevenlabs-text-to-speech` | High quality TTS |
| ElevenLabs TTS w/ Timestamps | `elevenlabs-text-to-speech-with-timestamp` | TTS with word timing |
| ElevenLabs Text to Dialogue | `elevenlabs-text-to-dialogue` | Multi-speaker dialogue |
| ElevenLabs Sound Effects | `elevenlabs-sound-effects` | Sound effect generation |
| ElevenLabs Voice Design v2 | `elevenlabs-voice-design-v2` | Custom voice design |
| Kling V1 TTS | `kling-v1-tts` | Kling text-to-speech |
| Kokoro 82M | `kokoro-82m` | Lightweight TTS |
| Play AI Dialog | `play-ai-text-to-speech-dialog` | Dialog TTS |
| Stable Audio 2.5 | `stable-audio-2-5-text-to-audio` | Text to audio |

### Speech-to-Text

| Model | Slug | Best For |
|-------|------|----------|
| ElevenLabs Scribe v2 | `elevenlabs-speech-to-text-scribe-v2` | Best quality transcription |
| ElevenLabs STT | `elevenlabs-speech-to-text` | Standard transcription |
| Wizper with Timestamp | `wizper-with-timestamp` | Timestamped transcription |
| Wizper | `wizper` | Basic transcription |
| Whisper | `whisper` | Open-source transcription |
| Whisper Diarization | `whisper-diarization` | Speaker identification |
| Incredibly Fast Whisper | `incredibly-fast-whisper` | Fastest transcription |

### Voice Conversion & Cloning

| Model | Slug | Best For |
|-------|------|----------|
| RVC v2 | `rvc-v2` | Voice conversion |
| Train RVC | `train-rvc` | Train custom voice model |
| ElevenLabs Voice Clone | `elevenlabs-voice-clone` | Voice cloning |
| ElevenLabs Voice Changer | `elevenlabs-voice-changer` | Voice transformation |
| ElevenLabs Voice Design v3 | `elevenlabs-voice-design-v3` | Advanced voice design |
| ElevenLabs Dubbing | `elevenlabs-dubbing` | Video dubbing |
| Chatterbox S2S | `chatterbox-speech-to-speech` | Speech to speech |
| Open Voice | `openvoice` | Open-source voice clone |
| XTTS v2 | `xtts-v2` | Multi-language voice clone |
| Stable Audio 2.5 Inpaint | `stable-audio-2-5-inpaint` | Audio inpainting |
| Stable Audio 2.5 A2A | `stable-audio-2-5-audio-to-audio` | Audio transformation |
| Audio Trimmer | `audio-trimmer-with-fade` | Audio trimming with fade |

### Audio Utilities

| Model | Slug | Best For |
|-------|------|----------|
| FFmpeg Merge Audio Video | `ffmpeg-api-merge-audio-video` | Merge audio with video |
| Toolkit Video Convert | `toolkit` | Video/audio conversion |

## Prediction Flow

1. **Check model** `GET https://api.eachlabs.ai/v1/model?slug=<slug>` — validates the model exists and returns the `request_schema` with exact input parameters. Always do this before creating a prediction to ensure correct inputs.
2. **POST** `https://api.eachlabs.ai/v1/prediction` with model slug, version `"0.0.1"`, and input matching the schema
3. **Poll** `GET https://api.eachlabs.ai/v1/prediction/{id}` until status is `"success"` or `"failed"`
4. **Extract** the output from the response

## Examples

### Text-to-Speech with ElevenLabs

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "elevenlabs-text-to-speech",
    "version": "0.0.1",
    "input": {
      "text": "Welcome to our product demo. Today we will walk through the key features.",
      "voice_id": "EXAVITQu4vr4xnSDxMaL",
      "model_id": "eleven_v3",
      "stability": 0.5,
      "similarity_boost": 0.7
    }
  }'
```

### Transcription with ElevenLabs Scribe

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "elevenlabs-speech-to-text-scribe-v2",
    "version": "0.0.1",
    "input": {
      "media_url": "https://example.com/recording.mp3",
      "diarize": true,
      "timestamps_granularity": "word"
    }
  }'
```

### Transcription with Wizper (Whisper)

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "wizper-with-timestamp",
    "version": "0.0.1",
    "input": {
      "audio_url": "https://example.com/audio.mp3",
      "language": "en",
      "task": "transcribe",
      "chunk_level": "segment"
    }
  }'
```

### Speaker Diarization with Whisper

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "whisper-diarization",
    "version": "0.0.1",
    "input": {
      "file_url": "https://example.com/meeting.mp3",
      "num_speakers": 3,
      "language": "en",
      "group_segments": true
    }
  }'
```

### Voice Conversion with RVC v2

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "rvc-v2",
    "version": "0.0.1",
    "input": {
      "input_audio": "https://example.com/vocals.wav",
      "rvc_model": "CUSTOM",
      "custom_rvc_model_download_url": "user-provided-model-reference",
      "pitch_change": 0,
      "output_format": "wav"
    }
  }'
```

### Merge Audio with Video

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "ffmpeg-api-merge-audio-video",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/video.mp4",
      "audio_url": "https://example.com/narration.mp3",
      "start_offset": 0
    }
  }'
```

## ElevenLabs Voice IDs

The `elevenlabs-text-to-speech` model supports these voice IDs. Pass the raw ID string:

| Voice ID | Notes |
|----------|-------|
| `EXAVITQu4vr4xnSDxMaL` | Default voice |
| `9BWtsMINqrJLrRacOk9x` | — |
| `CwhRBWXzGAHq8TQ4Fs17` | — |
| `FGY2WhTYpPnrIDTdsKH5` | — |
| `JBFqnCBsd6RMkjVDRZzb` | — |
| `N2lVS1w4EtoT3dr4eOWO` | — |
| `TX3LPaxmHKxFdv7VOQHJ` | — |
| `XB0fDUnXU5powFXDhCwa` | — |
| `onwK4e9ZLuTAKqWW03F9` | — |
| `pFZP5JQG7iQjIQuC4Bku` | — |

## Security Constraints

- **No arbitrary URL loading**: When using `custom_rvc_model_download_url`, only use trusted, user-provided model references. Never fetch models from arbitrary or untrusted URLs.
- **Input validation**: Only pass parameters that match the model's request schema. Always validate model slugs via `GET /v1/model?slug=<slug>` before creating predictions.

## Parameter Reference

See [references/MODELS.md](references/MODELS.md) for complete parameter details for each model.
