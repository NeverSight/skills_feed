---
name: music-emotion
description: Analyze emotion — mood classification, energy, valence, genre detection
user_invocable: true
---

# /music-emotion — Emotion & Style Analysis

Classify the emotional content of an audio file: primary mood, energy level, emotional valence, arousal, genre, and mood tags.

## Usage

```
/music-emotion <audio_file_path>
```

## Steps

1. Validate the audio file path
2. Run emotion analysis:

```bash
python3 -m music_analyzer emotion "<audio_file_path>"
```

3. Present results:
   - **Primary Emotion**: Dominant mood (happy, sad, calm, energetic, etc.)
   - **Energy Level**: 0-1 scale with curve across song segments
   - **Valence**: -1 (negative) to 1 (positive)
   - **Genre**: Detected genre
   - **Mood Tags**: Descriptive mood keywords

## Detection Methods

- **CLAP (full tier)**: AI-based emotion/genre classification using CLAP model
- **Heuristic (lite tier)**: Spectral features + rhythm + tonality-based rules

The method used is noted in the `method` field of the output.

## Output Fields

| Field | Description |
|-------|-------------|
| `primary_emotion` | Dominant emotion label |
| `secondary_emotions` | Additional emotion tags |
| `overall_energy` | Energy level 0-1 |
| `energy_curve` | Energy values per segment |
| `valence` | Emotional valence -1 to 1 |
| `arousal` | Arousal level 0-1 |
| `genre` | Detected genre |
| `mood_tags` | Mood descriptor keywords |
