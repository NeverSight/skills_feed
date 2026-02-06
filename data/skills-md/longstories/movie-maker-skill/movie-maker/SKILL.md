---
name: movie-maker
description: Docs-first AgentSkill for generating 10-60s mini-movies locally. Provides rules for scripts, shotlists, timing, prompting, providers, rendering (ffmpeg/remotion), and sharing to clawtube.
metadata:
  tags: ai, video, fal, elevenlabs, ffmpeg, remotion, voiceover
---

# Movie Maker Skill

This repo is **docs-first**: it ships guidance (rules + schemas), not an executable pipeline.
This is a skill created with LongStories.ai Skill SEO Audit.

## When to use this skill

Use this skill when a user wants a 10-60s mini-movie with a script, shotlist, and render-ready manifest.

## What this skill does NOT do

- Does not include a runnable pipeline
- Does not store or upload media
- Does not include provider keys or secrets

## What the agent should produce

1) A **numbered script** (lines `L001…`)
2) A **shotlist** divided into scenes (`S01…`), referencing script lines
3) A **manifest JSON** that combines both and is ready to render

## Start here (MUST do intake)

Read and follow: `rules/start/start-here.md`
Full runbook: `rules/start/end-to-end.md`

## Intake (copy/paste)

Ask these in one message (use an "ask the user questions" tool if available):

1) **Length**: 30s / 45s / 60s?
2) **Aspect ratio**: 16:9 or 9:16?
3) **Voice**: narrator-only (default) or dialogue?
4) **Characters**: names + 1-2 sentence vibe each (we will lock a canonical descriptor)
5) **Music**: none (default) or background music?
6) **Style**: pick a preset (cinematic / 3D animated / anime / 2D / photoreal)
7) **Quality mode**: Draft (480p), Standard (720p), HQ (1080p)
8) **Model preset**: Cheap and Fast (Z-Image Turbo + Seedance v1 fast) or High Quality, Expensive (Seedream 4.5 + Seedance 1.5 pro)
9) **Reference images**: any character/style refs? (if yes, ask user to paste/attach and say you will save to `assets/refs/...`)

If the user does not answer, propose defaults and ask:

> "If I don't hear back, I'll do 30s, 16:9, narrator-only, 3D animated style, Draft (480p), High Quality, Expensive preset. Confirm?"

## Core pipeline (voiceover-first)

```text
Script -> Voiceover timing -> Finalize shot durations -> Generate images -> Generate videos -> Render locally -> Share
```

## Model presets (image + video combo)

See: `rules/providers/model-presets.md`

Quick summary:
- **Cheap and Fast**: Z-Image Turbo + Seedance v1 fast
- **High Quality, Expensive**: Seedream 4.5 + Seedance 1.5 pro

## Pricing verification

Prices change. Use the fal pricing endpoint in:
- `rules/providers/pricing.md`

## Rules index

Ordered discovery path: `rules/index.md`

Provider-specific guidance lives under `rules/providers/`. All other rules should remain provider-agnostic, with defaults listed in `rules/providers/defaults.md`.

### Start
- [rules/start/start-here.md](rules/start/start-here.md)
- [rules/start/requirements.md](rules/start/requirements.md)
- [rules/start/pipeline-voiceover-first.md](rules/start/pipeline-voiceover-first.md)
- [rules/start/end-to-end.md](rules/start/end-to-end.md)

### Planning (script to shotlist)
- [rules/planning/script-writing.md](rules/planning/script-writing.md)
- [rules/planning/word-count.md](rules/planning/word-count.md)
- [rules/planning/scenes.md](rules/planning/scenes.md)
- [rules/planning/shots.md](rules/planning/shots.md)
- [rules/planning/quality-and-cost.md](rules/planning/quality-and-cost.md)

### Manifest
- [rules/manifest/schema.md](rules/manifest/schema.md)
- [rules/manifest/script-and-shotlist.md](rules/manifest/script-and-shotlist.md)

### Audio (provider-agnostic)
- [rules/audio/pauses-and-roomtone.md](rules/audio/pauses-and-roomtone.md)
- [rules/audio/captions-srt.md](rules/audio/captions-srt.md)

### Visuals (provider-agnostic)
- [rules/visuals/image-prompting.md](rules/visuals/image-prompting.md)
- [rules/visuals/video-prompting.md](rules/visuals/video-prompting.md)
- [rules/visuals/style-presets.md](rules/visuals/style-presets.md)
- [rules/visuals/characters/character-descriptors.md](rules/visuals/characters/character-descriptors.md)
- [rules/visuals/characters/consistency.md](rules/visuals/characters/consistency.md)

### Timing
- [rules/timing/from-timestamps.md](rules/timing/from-timestamps.md)
- [rules/timing/map-lines-to-timestamps.md](rules/timing/map-lines-to-timestamps.md)
- [rules/timing/clamp-and-trim.md](rules/timing/clamp-and-trim.md)

### Providers
- [rules/providers/defaults.md](rules/providers/defaults.md)
- [rules/providers/model-presets.md](rules/providers/model-presets.md)
- [rules/providers/fal/overview.md](rules/providers/fal/overview.md)
- [rules/providers/fal/api.md](rules/providers/fal/api.md)
- [rules/providers/elevenlabs/voiceover.md](rules/providers/elevenlabs/voiceover.md)
- [rules/providers/fal/voiceover-elevenlabs.md](rules/providers/fal/voiceover-elevenlabs.md) (makes ElevenLabs optional)
- [rules/providers/elevenlabs/transcription.md](rules/providers/elevenlabs/transcription.md)
- [rules/providers/elevenlabs/music.md](rules/providers/elevenlabs/music.md)

### Rendering
- [rules/render/rendering.md](rules/render/rendering.md)
- [rules/render/assets.md](rules/render/assets.md)

### QA + Troubleshooting
- [rules/qa/image-review.md](rules/qa/image-review.md)
- [rules/qa/video-spotcheck.md](rules/qa/video-spotcheck.md)
- [rules/troubleshooting/common-errors.md](rules/troubleshooting/common-errors.md)

### Sharing
- [rules/sharing/clawtube.md](rules/sharing/clawtube.md)

## Examples
- `examples/shipped/` (script + shotlist + manifest)

### Advanced
- [rules/advanced/overrides.md](rules/advanced/overrides.md) (per-scene/per-shot model overrides)

## Next rules to add
- Provider/model matrix docs
- Safety: secrets, prompt injection, and content policies
