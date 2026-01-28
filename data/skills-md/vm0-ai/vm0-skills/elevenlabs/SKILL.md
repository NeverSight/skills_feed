---
name: elevenlabs
description: ElevenLabs AI voice generation API via curl. Use this skill to convert text to speech with realistic AI voices.
vm0_secrets:
  - ELEVENLABS_API_KEY
---

# ElevenLabs API

Use the ElevenLabs API via direct `curl` calls to generate **realistic AI speech** from text.

> Official docs: `https://elevenlabs.io/docs/api-reference`

---

## When to Use

Use this skill when you need to:

- **Convert text to speech** with high-quality AI voices
- **List available voices** to find the right voice for your use case
- **Stream audio output** for real-time playback
- **Generate voiceovers** for videos, podcasts, or accessibility

---

## Prerequisites

1. Sign up at [ElevenLabs](https://elevenlabs.io/) and create an account
2. Go to your profile settings and generate an API key
3. Store your API key in the environment variable `ELEVENLABS_API_KEY`

```bash
export ELEVENLABS_API_KEY="your-api-key"
```

### API Limits

- Free tier: limited characters per month
- API key is passed via the `xi-api-key` header

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

All examples below assume you have `ELEVENLABS_API_KEY` set.

The base URL for the ElevenLabs API is:

- `https://api.elevenlabs.io/v1`

---

### 1. List Available Voices

Get all voices available to your account:

```bash
bash -c 'curl -s -X GET "https://api.elevenlabs.io/v1/voices" --header "xi-api-key: ${ELEVENLABS_API_KEY}"' | jq '.voices[] | {voice_id, name, category}'
```

This returns voice IDs needed for text-to-speech. Common voice categories:
- `premade`: ElevenLabs default voices
- `cloned`: Your cloned voices
- `generated`: AI-designed voices

---

### 2. Get Voice Details

Get detailed information about a specific voice. Replace `<your-voice-id>` with an actual voice ID:

```bash
bash -c 'curl -s -X GET "https://api.elevenlabs.io/v1/voices/<your-voice-id>" --header "xi-api-key: ${ELEVENLABS_API_KEY}"'
```

---

### 3. List Available Models

Get all available TTS models:

```bash
bash -c 'curl -s -X GET "https://api.elevenlabs.io/v1/models" --header "xi-api-key: ${ELEVENLABS_API_KEY}"' | jq '.[] | {model_id, name, can_do_text_to_speech}'
```

Common models:
- `eleven_multilingual_v2`: Best quality, supports 29 languages
- `eleven_flash_v2_5`: Low latency, good for real-time
- `eleven_v3`: Latest model (alpha)

---

### 4. Text to Speech (Save to File)

Convert text to speech and save as MP3. Replace `<your-voice-id>` with an actual voice ID from the list voices endpoint:

Write to `/tmp/elevenlabs_request.json`:

```json
{
  "text": "Hello! This is a test of the ElevenLabs text to speech API.",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}
```

Then run:

```bash
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/<your-voice-id>" --header "xi-api-key: ${ELEVENLABS_API_KEY}" --header "Content-Type: application/json" --header "Accept: audio/mpeg" -d @/tmp/elevenlabs_request.json --output speech.mp3
```

**Voice settings:**

- `stability` (0.0-1.0): Higher = more consistent, lower = more expressive
- `similarity_boost` (0.0-1.0): Higher = closer to original voice

---

### 5. Text to Speech with Streaming

Stream audio for real-time playback. Replace `<your-voice-id>` with an actual voice ID:

Write to `/tmp/elevenlabs_request.json`:

```json
{
  "text": "This audio is being streamed in real-time.",
  "model_id": "eleven_flash_v2_5"
}
```

Then run:

```bash
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/<your-voice-id>/stream" --header "xi-api-key: ${ELEVENLABS_API_KEY}" --header "Content-Type: application/json" --header "Accept: audio/mpeg" -d @/tmp/elevenlabs_request.json --output streamed.mp3
```

---

### 6. Get User Subscription Info

Check your usage and character limits:

```bash
bash -c 'curl -s -X GET "https://api.elevenlabs.io/v1/user/subscription" --header "xi-api-key: ${ELEVENLABS_API_KEY}"' | jq '{character_count, character_limit, tier}'
```

---

## Output Formats

You can specify different output formats via the `output_format` query parameter. Replace `<your-voice-id>` with an actual voice ID:

Write to `/tmp/elevenlabs_request.json`:

```json
{
  "text": "Hello world",
  "model_id": "eleven_multilingual_v2"
}
```

Then run:

```bash
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/<your-voice-id>?output_format=pcm_16000" --header "xi-api-key: ${ELEVENLABS_API_KEY}" --header "Content-Type: application/json" -d @/tmp/elevenlabs_request.json --output speech.pcm
```

Available formats:
- `mp3_44100_192` (default): MP3 at 44.1kHz, 192kbps
- `mp3_44100_128`: MP3 at 44.1kHz, 128kbps
- `pcm_16000`: PCM at 16kHz
- `pcm_22050`: PCM at 22.05kHz
- `pcm_24000`: PCM at 24kHz

---

## Guidelines

1. **Choose the right model**: Use `eleven_flash_v2_5` for low latency, `eleven_multilingual_v2` for best quality
2. **Monitor usage**: Check subscription endpoint to avoid exceeding character limits
3. **Experiment with voice settings**: Adjust stability and similarity_boost for different effects
4. **Use streaming for long text**: Stream endpoint is better for real-time applications
5. **Cache voice IDs**: Store frequently used voice IDs to avoid repeated API calls
