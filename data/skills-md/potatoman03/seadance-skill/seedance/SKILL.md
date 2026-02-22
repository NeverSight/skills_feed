---
name: seedance
description: Generate AI videos using BytePlus Seedance models. Activate when users want to create videos from text prompts or images, such as "generate a video of...", "create a video", "make a clip", or "seedance".
---

# Seedance Video Generation

Generate AI videos from text prompts or images using the `skills.sh` script bundled with this skill.

## Instructions

1. Read the user's request and determine:
   - The **prompt** (required) — a scene description for the video
   - The **mode** — text-to-video (default) or image-to-video (if an image path/URL is provided)
   - Any optional overrides: `--model`, `--ratio`, `--resolution`, `--duration`, `--camera-fixed`, `--output`, `--json-only`

2. Locate and run the CLI script via Bash. The script is `skills.sh` in this skill's directory:
   ```
   bash "<skill_directory>/skills.sh" --prompt "..." [--image PATH] [options]
   ```
   - The script auto-loads `ARK_API_KEY` from `.env` in the project root
   - Use a timeout of at least 600000ms for the Bash call (video generation takes minutes)
   - Always quote the prompt

3. Report the result:
   - On success, the script prints the downloaded file path to stdout. Show it to the user.
   - On failure, relay the error message and suggest fixes (check API key, model, parameters).

## Setup

Requires `ARK_API_KEY` in a `.env` file or exported in the shell. Get one at https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey

Python 3.7+ required. The Python SDK (`byteplus-python-sdk-v2`) installs automatically on first run.

## Defaults

| Option | Default |
|--------|---------|
| Model | `seedance-1-5-pro-251215` (switches to `seedance-2-0-260128` after 24 Feb 2026) |
| Ratio | `16:9` |
| Resolution | `720p` |
| Duration | `5` seconds |
| Camera fixed | `true` |
| Output dir | Current directory |

## Available Models

- `seedance-2-0-260128` — Seedance 2.0 (default after 24 Feb 2026 18:00)
- `seedance-1-5-pro-251215` — best quality + native audio
- `seedance-1-0-pro-250528` — best quality, no audio
- `seedance-1-0-pro-fast-251015` — 3x faster, good for drafts
- `seedance-1-0-lite-t2v-250428` — budget text-to-video only
- `seedance-1-0-lite-i2v-250428` — budget image-to-video only

## Prompting Tips

Structure prompts as: **Subject + Movement + Scene + Camera + Style**

Good: "A hawk slowly gliding downward over a misty canyon, wings spread, cinematic tracking shot"
Bad: "A bird flying"

For I2V: describe the **motion**, not the scene (the model can see the image).

The 1.5 Pro model supports native audio — describe sounds, music, or dialogue in the prompt.

## Example Commands

```bash
# Text-to-video, high quality
skills.sh --prompt "A lighthouse beam sweeping across a stormy sea at night, cinematic" --resolution 1080p --duration 8

# Image-to-video
skills.sh --prompt "The flower slowly blooms, petals unfurling" --image flower.jpg --duration 6

# Quick draft
skills.sh --prompt "A robot dancing in a disco" --model seedance-1-0-pro-fast-251015 --resolution 480p --duration 3
```
