---
name: speak
description: Text-to-speech using edge-tts or macOS say. Use when user says "speak", "say", "read aloud", or wants text spoken.
---

# /speak - Text-to-Speech

Speak text using edge-tts (high-quality neural voices) with fallback to macOS `say`.

## Quick Start

```bash
/speak "Hello world"                    # Default English voice
/speak --thai "สวัสดีครับ"                # Thai voice
/speak --voice "en-GB-RyanNeural" "Hi"  # Specific voice
/speak --mac "Hello"                    # Force macOS say
```

## Options

| Option | Description |
|--------|-------------|
| `--thai` | Use Thai voice (th-TH-NiwatNeural) |
| `--female` | Use female voice |
| `--voice NAME` | Specific edge-tts voice |
| `--mac` | Force macOS say command |
| `--rate RATE` | Speech rate (edge-tts: +/-50%, mac: 100-300) |
| `--list` | List available voices |

## Default Voices

| Language | Voice |
|----------|-------|
| English | en-US-GuyNeural (male) |
| English | en-US-JennyNeural (female) |
| Thai | th-TH-NiwatNeural (male) |
| Thai | th-TH-PremwadeeNeural (female) |

## Scripts

Located in `src/skills/speak/scripts/`:

| Script | Purpose |
|--------|---------|
| `speak.ts` | Main TTS script |

### Run Script

```bash
cd src/skills/speak/scripts
bun speak.ts "Text to speak"
bun speak.ts --thai "ภาษาไทย"
bun speak.ts --list
```

## Requirements

- **edge-tts**: `pip install edge-tts` (optional, for high-quality voices)
- **macOS say**: Built-in (fallback)

## How It Works

1. Check if edge-tts is available
2. If yes: Use edge-tts with neural voice
3. If no: Fall back to macOS `say` command
4. Play audio through default output

## Examples

```bash
# Speak Gemini response
/speak "The answer is 42"

# Thai greeting
/speak --thai "สวัสดีครับ ยินดีต้อนรับ"

# British accent
/speak --voice "en-GB-RyanNeural" "Brilliant!"

# List all voices
/speak --list
```
