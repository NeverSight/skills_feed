---
name: elevenlabs-tts
description: Generate realistic audio from text using ElevenLabs Text-to-Speech API. Use when the user needs to convert text to speech, create voiceovers, generate narration, or produce audio content. Triggers include "generate audio", "text to speech", "TTS", "voiceover", "narration", "ElevenLabs", "audio from text", "read this text aloud"
---

# ElevenLabs Text-to-Speech

Generate high-quality audio from text using the ElevenLabs API.

## Prerequisites

1. **ElevenLabs API Key**: Must be set as environment variable `ELEVEN_API_KEY`
   - The API key should already be configured in your environment
   - If not set, get your API key from: https://elevenlabs.io/app/settings/api-keys

2. **Python requests library**: Install if needed with `pip install requests --break-system-packages`

## Quick Start

Use the provided script to generate audio with your default voice:

```bash
python scripts/generate_audio.py "Your text here" output.mp3
```

The script is pre-configured to use your preferred voice (ID: `dq5fzy66iCKSIQWm5YMU`).

## Using a Different Voice

If you need to use a different voice, specify it with the `--voice` parameter:

```bash
python scripts/generate_audio.py "Hello world" output.mp3 --voice "voice_id_here"
```

## Common Workflows

### Voiceover for Videos

1. Prepare your script text
2. Choose appropriate voice for your content
3. Generate the audio file
4. Use the audio in your video editing software

Example:

```bash
# Read script from file and generate audio
python scripts/generate_audio.py "$(cat video_script.txt)" voiceover.mp3
```

### Multiple Segments

For longer content or different scenes, generate separate audio files:

```bash
# Intro
python scripts/generate_audio.py "Welcome to our channel" intro.mp3

# Main content
python scripts/generate_audio.py "$(cat main_script.txt)" main.mp3

# Outro
python scripts/generate_audio.py "Thanks for watching" outro.mp3
```

### From Markdown or Text Files

Convert documents to audio:

```bash
# Extract text from markdown (remove formatting)
python scripts/generate_audio.py "$(cat article.md | sed 's/#//g')" article.mp3
```

## Advanced Usage

### Custom Voice ID

If you have access to custom voices or want to use a specific voice ID:

```bash
python scripts/generate_audio.py "Text" output.mp3 --voice "your_voice_id_here"
```

### Providing API Key Directly

Instead of setting environment variable:

```bash
python scripts/generate_audio.py "Text" output.mp3 --api-key "your_api_key"
```

## Script Parameters

The `generate_audio.py` script accepts:

- **text** (required): The text to convert to speech
- **output** (required): Output file path (e.g., `output.mp3`)
- **--voice** (optional): Custom voice ID (default: dq5fzy66iCKSIQWm5YMU)
- **--api-key** (optional): API key (overrides ELEVEN_API_KEY env var)

## Best Practices

1. **Text Length**: Keep individual requests under 2,500 characters for best results
2. **Character Limits**: Monitor your monthly character quota to avoid interruptions
3. **File Naming**: Use descriptive names (e.g., `intro_v2.mp3`, `scene1_narration.mp3`)
4. **Testing**: Generate a short sample first to verify quality before processing long texts
5. **Punctuation**: Use proper punctuation to improve natural speech rhythm and pauses

## Troubleshooting

**API Key Error**: Ensure ELEVEN_API_KEY is set correctly:
```bash
echo $ELEVEN_API_KEY  # Should display your key
```

**Module Not Found**: Install requests:
```bash
pip install requests --break-system-packages
```

**Rate Limiting**: Free tier has usage limits. Space out requests or upgrade plan.

**Poor Audio Quality**: Try different voices or adjust the text (add punctuation, break into shorter sentences).

## Resources

- ElevenLabs Dashboard: https://elevenlabs.io/app
- API Documentation: https://elevenlabs.io/docs/api-reference
- Voice Library: https://elevenlabs.io/voice-library
- Pricing: https://elevenlabs.io/pricing
