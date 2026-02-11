---
name: music-rhythm
description: Analyze rhythm — BPM, beats, time signature, and song structure sections
user_invocable: true
---

# /music-rhythm — Rhythm & Structure Analysis

Extract rhythm and structural information from an audio file: tempo (BPM), beat positions, time signature, and song structure segmentation (intro/verse/chorus/bridge/outro).

## Usage

```
/music-rhythm <audio_file_path>
```

## Steps

1. Validate the audio file path
2. Run rhythm analysis:

```bash
python3 -m music_analyzer rhythm "<audio_file_path>"
```

3. Present results:
   - **BPM**: Estimated tempo with confidence
   - **Time Signature**: 4/4 or 3/4
   - **Song Structure**: Table of sections with start/end times
   - **Beat Count**: Total beats detected

## Output Fields

| Field | Description |
|-------|-------------|
| `bpm` | Estimated tempo in BPM |
| `bpm_confidence` | Confidence score 0-1 |
| `time_signature` | Estimated time signature |
| `beats` | Array of beat positions with strength |
| `downbeats` | Downbeat times |
| `sections` | Song structure segments with labels and times |
| `duration` | Total duration in seconds |
