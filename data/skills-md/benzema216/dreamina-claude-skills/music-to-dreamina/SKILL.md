---
name: music-to-dreamina
description: Generate Dreamina-compatible prompts from music analysis — per-section visual descriptions
user_invocable: true
---

# /music-to-dreamina — Music → Dreamina Prompts

Convert music analysis into Dreamina-compatible image/video generation prompts. Each song section gets a tailored Chinese and English prompt with style keywords, color palette, and energy level.

## Usage

```
/music-to-dreamina <audio_file_or_analysis_json>
```

Accepts either an audio file (runs analysis first) or a previously saved analysis JSON.

## Steps

1. Validate input (audio file or JSON)
2. Generate Dreamina prompts:

```bash
python3 -m music_analyzer dreamina "<input_path>"
```

3. Present per-section prompts:
   - **Section name** and time range
   - **Chinese prompt** (prompt_zh) — ready for Dreamina
   - **English prompt** (prompt_en)
   - **Style keywords** and **color palette**
   - **Energy level** (0-1)

4. Suggest using `/dreamina-gen-image` with the generated prompts to create actual images

## Mapping Logic

| Music Feature | Dreamina Parameter | Example |
|---------------|-------------------|---------|
| Emotion | Style keywords | happy → "明亮暖色调,活力" |
| Energy | Composition intensity | high → "动态构图,强对比" |
| BPM | Rhythm description | >140 → "激烈节奏" |
| Key/Mode | Brightness/darkness | major → "明亮基调" |
| Genre | Visual style | electronic → "赛博朋克,霓虹" |
| Section | Scene sequence | chorus → stronger visuals |

## Output Format

Each section produces:
```json
{
  "section": "chorus_1",
  "time_range": {"start": 45.2, "end": 72.8},
  "prompt_zh": "动态构图，明亮暖色调...",
  "prompt_en": "dynamic composition, bright warm tones...",
  "style_keywords": ["vibrant", "energetic"],
  "color_palette": ["#FFD700", "#FF6B35"],
  "energy_level": 0.85
}
```

## Integration with pull-film

The generated prompts can be directly used with `/dreamina-gen-image` from the pull-film plugin to create actual Dreamina images.
