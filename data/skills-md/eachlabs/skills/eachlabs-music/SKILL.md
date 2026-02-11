---
name: eachlabs-music
description: Generate songs, instrumentals, lyrics, and podcasts using EachLabs Mureka AI models. Also supports song extension, stem separation, and song recognition. Use when the user wants to create music, lyrics, or audio content.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Music

Generate songs, instrumentals, lyrics, podcasts, and more using Mureka AI models via the EachLabs Predictions API.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Available Capabilities

### Mureka Models

| Capability | Slug | Description |
|-----------|------|-------------|
| Generate Song | `mureka-generate-song` | Create a full song with vocals from a prompt |
| Generate Instrumental | `mureka-generate-instrumental` | Create instrumental tracks |
| Generate Lyrics | `mureka-generate-lyrics` | Generate lyrics from a prompt |
| Extend Lyrics | `mureka-extend-lyrics` | Continue/extend existing lyrics |
| Extend Song | `mureka-extend-song` | Continue an existing song |
| Create Speech | `mureka-create-speech` | Generate speech audio |
| Create Podcast | `mureka-create-podcast` | Generate multi-speaker podcast |
| Recognize Song | `mureka-recognize-song` | Identify a song from audio |
| Describe Song | `mureka-describe-song` | Analyze and describe a song |
| Stem Song | `mureka-stem-song` | Separate audio into stems |
| Upload File | `mureka-upload-file` | Upload audio for other operations |

### Minimax Music

| Capability | Slug | Description |
|-----------|------|-------------|
| Music v2 | `minimax-music-v2` | Latest Minimax music generation |
| Music v1.5 | `minimax-music-v1-5` | Stable Minimax music generation |

## Prediction Flow

1. **Check model** `GET https://api.eachlabs.ai/v1/model?slug=<slug>` — validates the model exists and returns the `request_schema` with exact input parameters. Always do this before creating a prediction to ensure correct inputs.
2. **POST** `https://api.eachlabs.ai/v1/prediction` with model slug, version `"0.0.1"`, and input matching the schema
3. **Poll** `GET https://api.eachlabs.ai/v1/prediction/{id}` until status is `"success"` or `"failed"`
4. **Extract** the output from the response

## Examples

### Generate a Song

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-generate-song",
    "version": "0.0.1",
    "input": {
      "prompt": "An upbeat indie pop song about summer road trips with catchy chorus",
      "duration": 120
    }
  }'
```

### Generate Instrumental

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-generate-instrumental",
    "version": "0.0.1",
    "input": {
      "prompt": "Lo-fi hip hop beat with jazzy piano chords and vinyl crackle, relaxing study music"
    }
  }'
```

### Generate Lyrics

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-generate-lyrics",
    "version": "0.0.1",
    "input": {
      "prompt": "Write lyrics for a heartfelt country ballad about coming home"
    }
  }'
```

### Create a Podcast

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-create-podcast",
    "version": "0.0.1",
    "input": {
      "prompt": "A 5-minute podcast discussion about the future of AI in music production",
      "speakers": ["Luna", "Jake"]
    }
  }'
```

### Extend an Existing Song

First upload the song, then extend it:

```bash
# Step 1: Upload the audio file
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-upload-file",
    "version": "0.0.1",
    "input": {
      "file": "https://example.com/my-song.mp3",
      "purpose": "audio"
    }
  }'

# Step 2: Use the upload ID to extend the song
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-extend-song",
    "version": "0.0.1",
    "input": {
      "upload_audio_id": "<upload-id-from-step-1>",
      "prompt": "Continue with an energetic guitar solo bridge"
    }
  }'
```

### Separate Audio Stems

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "mureka-stem-song",
    "version": "0.0.1",
    "input": {
      "url": "https://example.com/song.mp3"
    }
  }'
```

## Prompt Tips

- Specify genre: "indie pop", "lo-fi hip hop", "classical orchestral", "EDM"
- Include mood: "upbeat", "melancholic", "energetic", "relaxing"
- Mention instruments: "acoustic guitar", "piano", "synthesizer", "drums"
- Describe tempo: "slow ballad", "fast-paced", "medium tempo groove"
- For lyrics, mention theme and structure: "verse-chorus-verse about..."

## Parameter Reference

See [references/MODELS.md](references/MODELS.md) for complete parameter details for each model.
