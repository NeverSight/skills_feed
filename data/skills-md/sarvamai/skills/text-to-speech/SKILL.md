---
name: text-to-speech
description: Convert text to natural speech using Sarvam AI's Bulbul model. Use when the user needs to generate audio from text, create voiceovers, build voice interfaces, or synthesize Indian language speech. Supports 11 Indian languages with multiple voices, controllable pitch/pace/loudness, and real-time streaming. Returns base64-encoded audio.
license: Apache-2.0
metadata:
  author: sarvam-ai
  version: "1.0"
  model: bulbul:v2
---

# Text-to-Speech with Bulbul

Bulbul is Sarvam AI's text-to-speech model that generates natural-sounding speech in Indian languages with support for voice customization and streaming.

## Installation

```bash
pip install sarvamai
```

## Quick Start

```python
from sarvamai import SarvamAI
from sarvamai.play import save

client = SarvamAI()

response = client.text_to_speech.convert(
    text="नमस्ते, आप कैसे हैं?",
    target_language_code="hi-IN",
    model="bulbul:v2",
    speaker="anushka"
)

# Response contains base64-encoded audio
save(response,
"output.wav")
```

## Base64 Audio Response

The API returns audio as **base64-encoded strings** in the `audios` array:

```json
{
    "request_id": "abc123",
    "audios": [
        "UklGRiQAAABXQVZFZm10IBAAAAABAAEA..."
    ]
}
```

### Decode Manually

```python
import base64

response = client.text_to_speech.convert(
    text="Hello world",
    target_language_code="en-IN",
    model="bulbul:v2",
    speaker="anushka"
)

# Decode base64 to bytes
audio_bytes = base64.b64decode(response.audios[
    0
])

# Save to file
with open("output.wav",
"wb") as f:
    f.write(audio_bytes)
```

## Supported Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| `hi-IN` | Hindi | `ta-IN` | Tamil |
| `bn-IN` | Bengali | `te-IN` | Telugu |
| `kn-IN` | Kannada | `ml-IN` | Malayalam |
| `mr-IN` | Marathi | `gu-IN` | Gujarati |
| `pa-IN` | Punjabi | `or-IN` | Odia |
| `en-IN` | English (Indian) | | |

## Available Voices

| Voice | Type | Best For |
|-------|------|----------|
| `anushka` | Female | General, warm tone |
| `manisha` | Female | Professional, clear |
| `vidya` | Female | Friendly, conversational |
| `arjun` | Male | Authoritative, news |
| `amol` | Male | Casual, storytelling |
| `amartya` | Male | Deep, formal |

## Voice Control

Customize pitch, pace, and loudness:

```python
response = client.text_to_speech.convert(
    text="यह एक परीक्षण है।",
    target_language_code="hi-IN",
    model="bulbul:v2",
    speaker="anushka",
    pitch=0.2,          # -1.0 to 1.0 (higher = higher pitch)
    pace=1.2,           # 0.5 to 2.0 (higher = faster)
    loudness=1.5        # 0.5 to 2.0 (higher = louder)
)
```

## Audio Formats

Set output format with `output_audio_codec`:

| Format | Description |
|--------|-------------|
| `wav` | Uncompressed (default) |
| `mp3` | MPEG Layer-3 |
| `aac` | Advanced Audio Coding |
| `opus` | Optimized for speech |
| `flac` | Lossless |
| `linear16` | Raw PCM |
| `mulaw` | Telephony (8-bit) |
| `alaw` | Telephony (8-bit) |

```python
response = client.text_to_speech.convert(
    text="Hello",
    target_language_code="en-IN",
    model="bulbul:v2",
    speaker="anushka",
    output_audio_codec="mp3"
)
```

## Sample Rates

| Rate | Use Case |
|------|----------|
| `8000` | Telephony |
| `16000` | Voice assistants |
| `22050` | Standard audio |
| `24000` | High quality (default) |

```python
response = client.text_to_speech.convert(
    text="Hello",
    target_language_code="en-IN",
    model="bulbul:v2",
    speaker="anushka",
    sample_rate=8000  # For phone systems
)
```

## JavaScript

```javascript
import { SarvamAI
} from "sarvamai";
import fs from "fs";

const client = new SarvamAI();

const response = await client.textToSpeech.convert({
  text: "नमस्ते",
  targetLanguageCode: "hi-IN",
  model: "bulbul:v2",
  speaker: "anushka"
});

// Decode base64 and save
const audioBuffer = Buffer.from(response.audios[
    0
],
"base64");
fs.writeFileSync("output.wav", audioBuffer);
```

## cURL

```bash
curl -X POST "https://api.sarvam.ai/text-to-speech" \
  -H "api-subscription-key: $SARVAM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
        "नमस्ते, कैसे हो?"
    ],
    "target_language_code": "hi-IN",
    "model": "bulbul:v2",
    "speaker": "anushka"
}'
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` / `inputs` | string/array | Yes | Text to synthesize |
| `target_language_code` | string | Yes | BCP-47 language code |
| `model` | string | Yes | `bulbul:v2` or `bulbul:v1` |
| `speaker` | string | Yes | Voice name |
| `pitch` | float | No | -1.0 to 1.0 |
| `pace` | float | No | 0.5 to 2.0 |
| `loudness` | float | No | 0.5 to 2.0 |
| `output_audio_codec` | string | No | Audio format |
| `sample_rate` | int | No | Output sample rate |

## Response

```json
{
    "request_id": "20241115_abc123",
    "audios": [
        "UklGRiQAAABXQVZFZm10IBAAAAABAAEA..."
    ]
}
```

See [references/voices.md
](references/voices.md) for voice samples and recommendations.

