---
name: music-generator
description: "Generate AI music with ElevenLabs Music API. Use for: background music, soundtracks, jingles, theme songs, instrumental tracks, AI music composition."
---

# Music Generator

Generate custom AI music using ElevenLabs Music API with detailed composition control.

## Features

- **Simple Mode**: Generate music from a text prompt
- **Detailed Mode**: Create multi-section compositions with precise control over styles, moods, and transitions
- **Instrumental or Vocal**: Support for both instrumental and vocal tracks
- **Custom Duration**: Generate tracks from 15 seconds to 5 minutes

## Quick Start

```bash
cd ~/.claude/skills/music-generator/scripts

# Simple prompt-based generation
npx ts-node generate_music.ts \
  --prompt "Uplifting corporate music with electronic beats" \
  --duration 60 \
  --output /path/to/music.mp3

# List available styles
npx ts-node generate_music.ts --list-styles
```

## Composition Modes

### 1. Simple Mode (--prompt)

Generate music from a single text prompt:

```bash
npx ts-node generate_music.ts \
  --prompt "Energetic workout music with driving beats and motivational synths" \
  --duration 90 \
  --output workout.mp3
```

### 2. Detailed Mode (--composition)

Create multi-section compositions with JSON config:

```bash
npx ts-node generate_music.ts \
  --composition /path/to/composition.json \
  --output epic-track.mp3
```

**Composition JSON Format:**

```json
{
  "duration_ms": 80000,
  "instrumental": true,
  "positive_global_styles": ["corporate", "motivational", "electronic"],
  "negative_global_styles": ["sad", "aggressive", "heavy metal"],
  "sections": [
    {
      "section_name": "Intro",
      "duration_ms": 20000,
      "positive_local_styles": ["building momentum", "soft start"],
      "negative_local_styles": ["loud", "intense"],
      "lines": []
    },
    {
      "section_name": "Main Theme",
      "duration_ms": 40000,
      "positive_local_styles": ["energetic", "uplifting", "driving rhythm"],
      "negative_local_styles": ["slow", "mellow"],
      "lines": []
    },
    {
      "section_name": "Outro",
      "duration_ms": 20000,
      "positive_local_styles": ["triumphant", "resolution"],
      "negative_local_styles": ["abrupt ending"],
      "lines": []
    }
  ]
}
```

## Style Guide

### Positive Global Styles (Overall Track Feel)

**Moods:**
- uplifting, inspiring, motivational, peaceful, energetic
- dramatic, epic, emotional, nostalgic, mysterious
- playful, cheerful, romantic, melancholic

**Genres:**
- corporate, cinematic, electronic, ambient, orchestral
- pop, rock, jazz, classical, world music
- lo-fi, hip-hop, EDM, acoustic, folk

**Instruments:**
- piano, guitar, strings, synths, drums
- brass, woodwinds, percussion, bass

### Negative Global Styles (What to Avoid)

- aggressive, dark, scary, chaotic
- heavy metal, death metal, harsh noise
- explicit, profane

### Section-Specific Styles

Use `positive_local_styles` and `negative_local_styles` to control individual sections:

**Intro Styles:**
- soft opening, building momentum, atmospheric
- gentle start, mysterious intro

**Peak/Chorus Styles:**
- energetic peak, driving rhythm, powerful
- emotional climax, triumphant

**Outro Styles:**
- gentle fade, triumphant ending, resolution
- nostalgic close, hopeful conclusion

## Command Options

| Option | Short | Description |
|--------|-------|-------------|
| `--prompt` | `-p` | Text prompt for simple mode |
| `--composition` | `-c` | JSON file for detailed mode |
| `--duration` | `-d` | Duration in seconds (simple mode) |
| `--output` | `-o` | Output file path (required) |
| `--instrumental` | `-i` | Generate instrumental track |
| `--format` | `-f` | Output format (mp3_44100_192, mp3_44100_128) |
| `--list-styles` | | Show available styles |
| `--help` | `-h` | Show help |

## Examples

### Corporate Background Music

```bash
npx ts-node generate_music.ts \
  -p "Professional corporate background music, uplifting and modern, suitable for presentations" \
  -d 120 \
  -i \
  -o corporate-bg.mp3
```

### Podcast Intro

```bash
npx ts-node generate_music.ts \
  -p "Catchy podcast intro music, energetic and memorable, with electronic elements" \
  -d 15 \
  -o podcast-intro.mp3
```

### Video Game Theme

```bash
npx ts-node generate_music.ts \
  -p "Epic fantasy adventure theme with orchestral instruments and heroic melodies" \
  -d 180 \
  -i \
  -o game-theme.mp3
```

### Multi-Section Composition

Create a file `my-composition.json`:

```json
{
  "duration_ms": 120000,
  "instrumental": true,
  "positive_global_styles": ["cinematic", "epic", "orchestral"],
  "negative_global_styles": ["electronic", "modern"],
  "sections": [
    {
      "section_name": "Dawn",
      "duration_ms": 30000,
      "positive_local_styles": ["soft", "mysterious", "building anticipation"],
      "negative_local_styles": ["loud", "fast"],
      "lines": []
    },
    {
      "section_name": "Battle",
      "duration_ms": 50000,
      "positive_local_styles": ["intense", "driving", "heroic"],
      "negative_local_styles": ["peaceful", "slow"],
      "lines": []
    },
    {
      "section_name": "Victory",
      "duration_ms": 40000,
      "positive_local_styles": ["triumphant", "emotional", "uplifting"],
      "negative_local_styles": ["sad", "mellow"],
      "lines": []
    }
  ]
}
```

Then generate:

```bash
npx ts-node generate_music.ts \
  -c my-composition.json \
  -o epic-journey.mp3
```

## API Limits

- Maximum duration: 330 seconds (5.5 minutes)
- Minimum duration: 15 seconds
- Generation time: ~30-60 seconds per track
- Cost: ~$0.05-0.15 per generation (varies by duration)

## Troubleshooting

**"Invalid API key"**: Check `.env` file has valid `ELEVENLABS_API_KEY`

**"Duration too long"**: Maximum is 330 seconds (5.5 minutes)

**"Validation error"**: Ensure composition JSON has all required fields:
- `positive_global_styles` (array)
- `negative_global_styles` (array)
- `sections` with `section_name`, `duration_ms`, `positive_local_styles`, `negative_local_styles`, `lines`
