---
name: music-analyze
description: Full music analysis — extracts rhythm, emotion, timbre, tonality, lyrics and outputs structured JSON
user_invocable: true
---

# /music-analyze — Full Music Analysis

Analyze a local audio file and output a comprehensive structured JSON containing rhythm, emotion, timbre, tonality, lyrics, onset, and color palette data.

## Usage

```
/music-analyze <audio_file_path>
```

## Accepted Formats
MP3, WAV, FLAC, OGG, M4A, AAC, WMA

## Steps

1. Validate the audio file path exists and is a supported format
2. Run the full analysis pipeline:

```bash
python3 -m music_analyzer analyze "<audio_file_path>"
```

3. Parse the JSON output and present a structured summary to the user:
   - **Rhythm**: BPM, time signature, song structure sections
   - **Emotion**: Primary mood, energy level, valence, genre
   - **Timbre**: Brightness, warmth, dynamic range, MFCC summary
   - **Tonality**: Key, mode, chord progression highlights
   - **Lyrics**: Whether vocals detected, language, transcription preview
   - **Onsets**: Onset rate (for visual sync reference)
   - **Color Palette**: Suggested colors based on mood

4. If the user wants to generate Dreamina prompts or storyboards, suggest:
   - `/music-to-dreamina` for Dreamina image/video generation prompts
   - `/music-to-storyboard` for shot-by-shot storyboard
   - `/music-color-palette` for detailed color scheme

## Options

- Add `--no-cache` to force re-analysis (skip cached results)
- Add `--no-separation` to skip Demucs source separation (faster)
- Add `--output <path>` to save JSON to a specific file

## Output

The analysis JSON follows the `MusicAnalysisResult` schema and can be saved and reused as input for the formatter commands (dreamina, storyboard, color-palette).

## Error Handling

- If librosa is not installed, instruct user: `pip install -e ~/.claude/plugins/music-analyzer/src/`
- If optional features are missing, the tool will degrade gracefully and note which tier is active (lite/standard/full)
