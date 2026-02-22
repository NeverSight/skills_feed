---
name: speech-to-text
description: Transcribe audio to text using Sarvam AI's Saarika model. Use when the user needs to convert speech to text, transcribe audio files, build voice interfaces, or process Indian language audio. Supports 11 Indian languages plus English with automatic language detection, code-mixing, speaker diarization, and word-level timestamps.
license: Apache-2.0
metadata:
  author: sarvam-ai
  version: "1.0"
  model: saarika:v2.5
---

# Speech-to-Text with Saarika

Saarika is Sarvam AI's speech recognition model optimized for Indian languages with support for code-mixing (Hindi-English etc.) and multi-speaker scenarios.

## Installation

```bash
pip install sarvamai
```

## Quick Start

```python
from sarvamai import SarvamAI

client = SarvamAI()

response = client.speech_to_text.transcribe(
    file=open("audio.wav",
"rb"),
    model="saarika:v2.5",
    language_code="hi-IN"
)

print(response.transcript)
```

## Supported Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| `hi-IN` | Hindi | `ta-IN` | Tamil |
| `bn-IN` | Bengali | `te-IN` | Telugu |
| `kn-IN` | Kannada | `ml-IN` | Malayalam |
| `mr-IN` | Marathi | `gu-IN` | Gujarati |
| `pa-IN` | Punjabi | `or-IN` | Odia |
| `en-IN` | English (Indian) | `auto` | Auto-detect |

## API Options

### REST API (≤30 seconds)

For short audio clips:

```python
response = client.speech_to_text.transcribe(
    file=open("short_clip.wav",
"rb"),
    model="saarika:v2.5",
    language_code="auto",           # Auto-detect language
    with_timestamps=True,           # Word-level timestamps
    with_diarisation=True           # Speaker identification
)

print(response.transcript)
print(response.language_code)       # Detected language
print(response.words)               # Timestamped words
print(response.speaker_segments)    # Speaker turns
```

### Batch API (≤1 hour)

For long recordings:

```python
response = client.speech_to_text.transcribe_batch(
    file=open("long_recording.mp3",
"rb"),
    model="saarika:v2.5",
    language_code="hi-IN"
)
```

### WebSocket Streaming (Real-time)

For live transcription. Audio must be sent as **base64-encoded strings**.

```python
import asyncio
import base64
from sarvamai import AsyncSarvamAI

async def stream_audio():
    client = AsyncSarvamAI()

    async with client.speech_to_text_streaming.connect(
        language_code="hi-IN",
        model="saarika:v2.5",
        high_vad_sensitivity=True
    ) as ws:
        # Read and encode audio to base64
        with open("audio.wav",
"rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode("utf-8")

        # Send base64 encoded audio
        await ws.transcribe(
            audio=audio_base64,
            encoding="audio/wav",
            sample_rate=16000
        )

        # Receive transcription
        response = await ws.recv()
        print(response)

asyncio.run(stream_audio())
```

**WebSocket supported formats:** `wav`, `pcm_s16le`, `pcm_l16`, `pcm_raw` only. MP3/AAC/OGG not supported for streaming.

## JavaScript

```javascript
import { SarvamAI
} from "sarvamai";
import fs from "fs";

const client = new SarvamAI();

const response = await client.speechToText.transcribe({
  file: fs.createReadStream("audio.wav"),
  model: "saarika:v2.5",
  languageCode: "hi-IN",
  withTimestamps: true
});

console.log(response.transcript);
```

## cURL

```bash
curl -X POST "https://api.sarvam.ai/speech-to-text" \
  -H "api-subscription-key: $SARVAM_API_KEY" \
  -F "file=@audio.wav" \
  -F "model=saarika:v2.5" \
  -F "language_code=hi-IN"
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | Audio file (wav, mp3, flac, ogg, webm) |
| `model` | string | Yes | `saarika:v2.5` or `saarika:v2` |
| `language_code` | string | Yes | BCP-47 code or `auto` |
| `with_timestamps` | bool | No | Return word timestamps |
| `with_diarisation` | bool | No | Enable speaker identification |

## Response

```json
{
    "request_id": "abc123",
    "transcript": "नमस्ते, आप कैसे हैं?",
    "language_code": "hi-IN",
    "words": [
        {
            "word": "नमस्ते",
            "start": 0.0,
            "end": 0.5
        },
        {
            "word": "आप",
            "start": 0.6,
            "end": 0.8
        }
    ],
    "speaker_segments": [
        {
            "speaker": "SPEAKER_00",
            "start": 0.0,
            "end": 2.5
        }
    ]
}
```

See [references/streaming.md
](references/streaming.md) for detailed WebSocket documentation.

