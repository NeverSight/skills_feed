---
name: music-tonality
description: Analyze tonality — key detection, chord progression, melody contour
user_invocable: true
---

# /music-tonality — Tonality & Harmony Analysis

Detect musical key, mode, chord progression, and melody pitch contour.

## Usage

```
/music-tonality <audio_file_path>
```

## Steps

1. Validate the audio file path
2. Run tonality analysis:

```bash
python3 -m music_analyzer tonality "<audio_file_path>"
```

3. Present results:
   - **Key**: Detected key and mode (e.g. "C major", "A minor")
   - **Confidence**: Key detection confidence
   - **Chord Progression**: Sequence of chords with timestamps
   - **Melody Contour**: Simplified pitch contour (sampled Hz values)

## Detection Methods

- **Essentia (standard/full tier)**: Uses essentia's KeyExtractor and ChordsDetection
- **Librosa (lite tier)**: Krumhansl-Schmuckler key profiles + template-based chord matching

## Output Fields

| Field | Description |
|-------|-------------|
| `key` | Estimated key (e.g. "C major") |
| `key_confidence` | Confidence 0-1 |
| `mode` | "major" or "minor" |
| `chords` | Chord events with time, duration, label |
| `melody_contour` | Sampled pitch values in Hz |
