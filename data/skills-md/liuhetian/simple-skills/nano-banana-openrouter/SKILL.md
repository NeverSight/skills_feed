---
name: nano-banana-openrouter
description: Generate or edit images via OpenRouter using Google's Gemini 3 Pro Image model. Use when the user wants to generate images using OpenRouter API instead of direct Google API.
metadata: {"openclaw":{"emoji":"🍌","requires":{"bins":["uv"],"env":["OPENROUTER_API_KEY"]},"primaryEnv":"OPENROUTER_API_KEY","install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Nano Banana OpenRouter

Generate or edit images via OpenRouter using Gemini 3 Pro Image model.

## Usage

### Generate
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "your image description" --filename "output.png"
```

### Edit
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "edit instructions" --filename "output.png" --input-image "/path/in.png"
```

## API Key

- `OPENROUTER_API_KEY` env var
- Or set `skills."nano-banana-openrouter".apiKey` / `skills."nano-banana-openrouter".env.OPENROUTER_API_KEY` in `~/.clawdbot/clawdbot.json`

## Notes
- Uses `google/gemini-3-pro-image-preview` model via OpenRouter
- Returns image as base64 data URL
- The script prints a `MEDIA:` line for Clawdbot to auto-attach on supported chat providers
- Do not read the image back; report the saved path only
