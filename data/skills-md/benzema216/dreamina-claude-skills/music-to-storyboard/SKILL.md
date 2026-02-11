---
name: music-to-storyboard
description: Generate storyboard from music analysis — shot-by-shot with camera movements
user_invocable: true
---

# /music-to-storyboard — Music → Storyboard

Generate a shot-by-shot storyboard from music analysis, with shot types, camera movements, visual descriptions, mood, and transitions. Output is compatible with pull-film's storyboard-generator format.

## Usage

```
/music-to-storyboard <audio_file_or_analysis_json>
```

Accepts either an audio file (runs analysis first) or a previously saved analysis JSON.

## Steps

1. Validate input (audio file or JSON)
2. Generate storyboard:

```bash
python3 -m music_analyzer storyboard "<input_path>"
```

3. Present storyboard as a table or sequence:
   - **Shot #** with section label and time range
   - **Shot type**: wide, medium, close-up, etc.
   - **Camera movement**: static, dolly, orbit, etc.
   - **Visual description** (Chinese + English)
   - **Transition** to next shot: cut, dissolve, fade
   - **Energy level** and mood

4. Suggest using `/storyboard-generator` from pull-film to create the visual storyboard

## Section → Shot Mapping

| Section | Default Shot | Camera | Visual Treatment |
|---------|-------------|--------|-----------------|
| Intro | Wide → Medium | Slow dolly in | Environment establishing |
| Verse | Medium, Close-up | Static, slow pan | Narrative focus |
| Chorus | Wide, Close-up | Orbit, fast push | Visual climax |
| Bridge | Close-up, Wide | Slow dolly out | Contrast, reflection |
| Outro | Wide | Slow pull-out | Closure, fade |

## Output Format

Compatible with pull-film's storyboard-generator:
```json
{
  "song_title": "example.mp3",
  "total_duration": 240.5,
  "bpm": 128.0,
  "shots": [
    {
      "shot_number": 1,
      "section": "intro",
      "time_range": {"start": 0, "end": 15.5},
      "shot_type": "wide",
      "camera_movement": "slow dolly in",
      "visual_description_zh": "...",
      "visual_description_en": "...",
      "transition": "fade",
      "energy_level": 0.3
    }
  ]
}
```
