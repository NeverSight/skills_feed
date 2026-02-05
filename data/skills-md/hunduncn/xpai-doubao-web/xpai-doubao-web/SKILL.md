---
name: xpai-doubao-web
description: Generate images and text via Doubao Web using browser cookies and Playwright UI automation. Use when a user asks for Doubao Web image generation, prompt-to-image automation, text replies, preset aspect ratios (e.g. 小红书封面), or session-based multi-turn workflows.
---

# XPAI Doubao Web

## Overview

Use this skill to generate images or text from Doubao Web by reusing browser login cookies. It provides a CLI wrapper with prompt files, optional reference images, presets, sessions, and JSON output.

## Script Directory

All scripts are located in the `scripts/` subdirectory of this skill.

Script reference:
- `scripts/main.ts`: CLI entry point (image/text)
- `scripts/doubao-webapi/*`: TypeScript client and helpers

## Consent Check (required before first use)

This skill relies on reverse-engineered web behavior and will access/store your Doubao Web cookies.
Obtain explicit user consent before running automation.

Consent file locations:
- macOS: `~/Library/Application Support/xpai-skills/doubao-web/consent.json`
- Linux: `~/.local/share/xpai-skills/doubao-web/consent.json`
- Windows: `%APPDATA%\\xpai-skills\\doubao-web\\consent.json`

Consent file format:
`{"version":1,"accepted":true,"acceptedAt":"<ISO>","disclaimerVersion":"1.0"}`

## Preferences (EXTEND.md)

Check for optional EXTEND.md overrides in this order:

```bash
# Project-level first
test -f .xpai-skills/xpai-doubao-web/EXTEND.md && echo "project"

# Then user-level
test -f "$HOME/.xpai-skills/xpai-doubao-web/EXTEND.md" && echo "user"
```

Supported settings (if you add parsing for them): default model, proxy settings, custom data directory.

## Usage

```bash
# Text-to-image
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts "Your prompt"

# Text-only
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts --mode text --prompt "Summarize this article"

# Specify model
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts --prompt "Your prompt" --model doubao-default

# Generate an image file
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts --prompt "A cute cat" --image out.png

# Prompt from files
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts --promptfiles system.md content.md --image out.png

# Vision input (reference images)
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts --prompt "Create variation" --reference a.png --image out.png

# Preset (aspect ratio via prompt prefix/suffix)
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts --preset xiaohongshu_cover --prompt "Minimalist poster" --image out.png

# List presets
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts --list-presets

# Multi-turn sessions
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts "Remember: 42" --sessionId session-abc
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts "What number?" --sessionId session-abc

# JSON output
npx -y bun /Users/aqxp/Aicodingmac/test2/xpai-doubao-web/scripts/main.ts "Hello" --json
```

## Options

- `--prompt`, `-p`: Prompt text
- `--promptfiles`: Read prompt from files (concatenated)
- `--model`, `-m`: Model string (pass-through)
- `--mode`: `image` (default) or `text`
- `--preset`: Preset name (applies prompt prefix/suffix; default `xiaohongshu_cover`)
- `--image [path]`: Generate image (default: `generated.png`)
- `--reference`, `--ref`: Reference images for vision input
- `--sessionId`: Session ID for multi-turn conversation
- `--list-sessions`: List saved sessions
- `--list-presets`: List preset names and config paths
- `--json`: Output as JSON
- `--login`: Refresh cookies, then exit
- `--cookie-path`: Custom cookie file path
- `--profile-dir`: Chrome profile directory

## Authentication

Login uses browser cookies. The CLI supports:
- `--login` to trigger a browser-based refresh (implemented with Playwright).
- `--cookie-path` or `DOUBAO_WEB_COOKIE_PATH` to point at an exported cookie file.

Flow notes:
- `--login` opens a visible browser window and saves cookies.
- Image/text generation runs headless by default (no window). Set `DOUBAO_WEB_HEADLESS=0` to show the browser.
- If a cookies file already exists, generation proceeds without opening a browser.
- To force a fresh login, delete the cookies file or run `--login` again.

For `--login` and image generation, install Playwright and its browsers:

```bash
npm i -D playwright
npx playwright install
```

Supported browsers (Playwright): Chromium/Chrome/Edge.
Override browser path via `DOUBAO_WEB_CHROME_PATH`. If you pass `--profile-dir`, it is used as a Playwright user data directory.

## Presets

Preset config path priority:
1. `DOUBAO_WEB_PRESETS_PATH`
2. `.xpai-skills/xpai-doubao-web/presets.json` (project)
3. `$HOME/.xpai-skills/xpai-doubao-web/presets.json` (user)

Format:
```json
{
  "default": "xiaohongshu_cover",
  "presets": {
    "xiaohongshu_cover": { "prefix": "...", "suffix": "..." }
  }
}
```

Example file: `references/presets.example.json`

## Environment Variables

- `DOUBAO_WEB_DATA_DIR`: Data directory
- `DOUBAO_WEB_COOKIE_PATH`: Cookie file path
- `DOUBAO_WEB_HEADLESS`: Set to `0` to run browser in headed mode (default: headless)
- `DOUBAO_WEB_MAX_IMAGES`: Max images to save (default: `1`)
- `DOUBAO_WEB_LOGIN_URL`: Login URL to open in the browser (default: `https://www.doubao.com/`)
- `DOUBAO_WEB_COOKIE_DOMAIN`: Filter cookies by domain (default: `doubao.com`)
- `DOUBAO_WEB_PRESETS_PATH`: Preset config file path
- `DOUBAO_WEB_INPUT_SELECTOR`: Custom input selector for the prompt box
- `DOUBAO_WEB_OUTPUT_SELECTOR`: Custom selector for the latest assistant message
- `DOUBAO_WEB_CHROME_PROFILE_DIR`: Chrome profile directory
- `DOUBAO_WEB_CHROME_PATH`: Chrome executable path
- `HTTP_PROXY`, `HTTPS_PROXY`: Proxy for web access

## Sessions

Session files are stored in the data directory under `sessions/<id>.json`.

Contains: `id`, `conversationUrl`, `messages`, timestamps. When `--sessionId` is set, a persistent Playwright profile is stored under `profiles/<id>/` to keep login state.
