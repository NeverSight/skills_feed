---
name: voiceover
description: |
  Generate high-quality voiceover audio with ElevenLabs. Includes word-level
  timestamps for video sync. Use when: creating demo narration, video voiceover,
  podcast intros, or any TTS need. Keywords: voiceover, TTS, text to speech,
  ElevenLabs, narration, audio, timestamps.
argument-hint: "[script text or file path]"
---

# Voiceover (ElevenLabs)

## What This Does
- Accept script text or file path.
- Preprocess for TTS: expand acronyms, normalize numbers.
- Generate via ElevenLabs API.
- Return audio + optional word timestamps.

## Prerequisites
- `ELEVENLABS_API_KEY` env var set.
- ElevenLabs Creator plan ~ $5/mo for ~100k chars.

## Usage
- `/voiceover "Welcome to Heartbeat..."`
- `/voiceover demo-script.md --timestamps --voice adam`

## Voices
- See `skills/voiceover/references/elevenlabs-voices.md`.
- Default: `adam` (clear, professional).

## Output
- `voiceover.mp3`
- `timestamps.json` (word-level timing when requested)

## Integration
- Used by `/demo-video` for narration sync.
