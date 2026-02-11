---
name: music-lyrics
description: Extract lyrics — timestamped transcription using faster-whisper
user_invocable: true
---

# /music-lyrics — Lyrics Transcription

Transcribe lyrics from audio with timestamps using faster-whisper (when available).

## Usage

```
/music-lyrics <audio_file_path>
```

## Steps

1. Validate the audio file path
2. Run lyrics extraction:

```bash
python3 -m music_analyzer lyrics "<audio_file_path>"
```

Optionally specify model size: `--model-size base` (tiny/base/small/medium/large-v2)

3. Present results:
   - **Has Vocals**: Whether vocals were detected
   - **Language**: Detected language
   - **Lyrics**: Timestamped segments with text
   - **Full Text**: Complete concatenated lyrics

## Requirements

- **Full tier**: faster-whisper must be installed for actual transcription
- **Lite tier**: Only vocal detection heuristic (no transcription)

Install full dependencies:
```bash
pip install -e "~/.claude/plugins/music-analyzer/src/[full]"
```

## Output Fields

| Field | Description |
|-------|-------------|
| `segments` | Array of {start, end, text, confidence} |
| `full_text` | Complete lyrics text |
| `language` | Detected language code |
| `has_vocals` | Boolean — vocals detected |
| `method` | "whisper" or "none" |
