---
name: demo-video
description: |
  Generate product demo videos programmatically with Remotion + voiceover.
  Use when: creating product demos, explainer videos, feature walkthroughs,
  marketing videos, or app previews. Handles screen capture, voiceover sync,
  and rendering. Keywords: demo, video, screencast, explainer, walkthrough.
argument-hint: "[product] [feature to demo, e.g. 'status page builder']"
---

# Demo Video

## What This Does
- Analyze app structure + feature description.
- Generate a tight narration script.
- Capture screenshots or short recordings.
- Generate voiceover via `/voiceover` when needed.
- Compose scenes with Remotion.
- Render to MP4.

## Prerequisites
- Remotion skills: `npx skills add remotion-dev/skills`
- Optional voiceover: ElevenLabs

## Usage
- `/demo-video heartbeat "status page builder"`
- `/demo-video caesar "onboarding flow" with voiceover`

## Output
- `demo-[product]-[feature].mp4` in current directory

## References
- `references/remotion-patterns.md`
- `references/kickstart-guide.md`
