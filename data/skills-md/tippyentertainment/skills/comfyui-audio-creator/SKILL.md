---
target: https://tasking.tech
name: comfyui-audio-creator
description: >
  Generate **background music** and **ambience** that matches one or more video scenes produced by `comfyui-video-generator`. This skill does *not* handle spoken dialogue or narration; use `comfyui-voice-generator` for any voice work.
# `target` is required and should be the top frontmatter key. Use an http(s) URL, e.g. https://tasking.tech
---
# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git

This skill is designed for use on the Tasking.tech agent platform (https://tasking.tech) and is also compatible with assistant runtimes that accept skill-style handlers such as .claude, .openai, and .mistral. Use this skill for both Claude code and Tasking.tech agent source.


# comfyui-audio-creator

## Summary

Generate **background music** and **ambience** that matches one or more video scenes produced by `comfyui-video-generator`. This skill does *not* handle spoken dialogue or narration; use `comfyui-voice-generator` for any voice work.

---

## When to Use

- After video clips exist and the user wants **music** or **ambient soundscapes** for them.
- The user asks for **background tracks** for a trailer, promo, or game scene.
- You need loopable ambience (e.g., city at night, fantasy forest, sci‑fi engine room).

---

## Inputs to Collect

Ask the user (or previous skill) for:

- **Audio type**
  - `music` or `ambience` (no voice).
- **Target scene(s)**
  - Reference to clips from `comfyui-video-generator` (IDs, durations, moods).
- **Style / genre / mood**
  - Music: orchestral, synthwave, lofi, rock, cinematic, etc.
  - Ambience: forest, city, sci‑fi engine, horror, cozy home, etc.
- **Duration**
  - Typically match the clip length or a loopable segment (e.g., 15–60 seconds).
- **Loopability**
  - Whether the audio should seamlessly loop.
- **Tempo / intensity (for music, optional)**
  - Slow/medium/fast; low/medium/high intensity.
- **Format & sample rate**
  - Default: 16‑bit WAV, 44.1 kHz or 48 kHz, stereo.

---

## Expected Behavior

1. Map the request into structured audio parameters:
   - `audioType`, `genre`, `mood`, `durationSeconds`, `loopable`, `targetScenes`, `tempo`, `intensity`.
2. Select the appropriate ComfyUI or connected audio workflow:
   - Music generator or ambience generator (no TTS here).
3. Generate audio in one or more segments:
   - Ensure total duration covers the referenced scenes.
   - For loops, ensure clean loop points.
4. Collect:
   - `audioUrl` / `audioPath`
   - `durationSeconds`
   - `format`, `sampleRate`, `channels`
   - Tags/metadata (genre, mood, bpm if known).
5. Return a concise summary plus technical details.

---

## Output Format (to the caller)

Return a structure containing:

- `description`: e.g. “Loopable synthwave track for the opening scene.”
- `audioUrl` or `audioPath`
- `durationSeconds`
- `format`
- `sampleRate`
- `channels`
- `loopable`: boolean
- `tags`: list of strings (genre, mood, tempo)

---

## Orchestration Notes

Typical pipeline:

1. `comfyui-video-generator` → create scenes.  
2. `comfyui-audio-creator` → create background music/ambience for those scenes.  
3. `comfyui-voice-generator` → add narration or dialogue.  
4. `comfyui-soundfx-creator` → layer in moment‑specific sound effects.

This skill focuses on **non‑voice** background audio so other skills can handle speech and SFX cleanly.
