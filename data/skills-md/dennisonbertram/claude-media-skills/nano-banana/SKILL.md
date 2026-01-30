---
name: nano-banana
description: Generate images using Google's Nano-Banana (Gemini 2.5 Flash Image) model. Use when the user asks to generate, create, or make an image, picture, or illustration.
allowed-tools: Read, Bash
---

# Nano-Banana Image Generation

Generate images using Google's Gemini Image models.

## IMPORTANT: Enhance User Prompts

Before generating, **always enhance the user's prompt** using the techniques in [PROMPTING.md](PROMPTING.md).

### Quick Enhancement Formula
`[Subject] + [Style] + [Lighting] + [Composition] + [Quality]`

### Example Enhancement
- User says: "a cat"
- Enhanced: "A fluffy orange tabby cat with bright green eyes, photorealistic, soft natural window lighting, shallow depth of field, rule of thirds composition"

For detailed prompting techniques, templates, and style keywords, see [PROMPTING.md](PROMPTING.md).

## Quick Start

```bash
~/.claude/skills/nano-banana/scripts/generate.sh "your prompt here"
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output PATH` | Save to specific file | `~/Pictures/nano-banana/<timestamp>.png` |
| `--size SIZE` | Resolution: 1K, 2K, 4K | 1K |
| `--aspect RATIO` | Aspect ratio | 1:1 |
| `--flash` | Use Flash model (faster, lower quality) | Pro |

### Aspect Ratios
`1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`

### Resolutions
- **1K** - Standard (default, fast)
- **2K** - High resolution (requires Pro model)
- **4K** - Maximum resolution (requires Pro model)

## Interpreting User Requests

Parse the user's request and map to script options:

| User says | Script call |
|-----------|-------------|
| "Generate a cat" | `generate.sh "a cat"` |
| "Create a 4K image of mountains" | `generate.sh "mountains" --size 4K` |
| "Make a landscape wallpaper" | `generate.sh "landscape" --aspect 16:9` |
| "High quality portrait of a robot" | `generate.sh "portrait of a robot" --pro --aspect 3:4` |
| "Generate a sunset, save to desktop" | `generate.sh "a sunset" --output ~/Desktop/sunset.png` |
| "4K widescreen cyberpunk city" | `generate.sh "cyberpunk city" --size 4K --aspect 16:9` |

### Keywords to watch for:
- **Resolution**: "4K", "high res", "high resolution", "2K", "large" → use `--size`
- **Quality**: "high quality", "detailed", "professional" → use `--pro`
- **Orientation**: "landscape", "widescreen", "wallpaper" → `--aspect 16:9`
- **Orientation**: "portrait", "vertical", "phone wallpaper" → `--aspect 9:16`
- **Save location**: "save to", "put it in", "output to" → `--output`

## Behavior

- Runs in **background** (won't block Claude)
- Sends **macOS notification** when complete
- **Auto-opens** the image when done
- Images saved to `~/Pictures/nano-banana/` by default

## Troubleshooting

Check the error log:
```bash
cat ~/.claude/skills/nano-banana/last-error.log
```

Verify API key:
```bash
security find-generic-password -a "$USER" -s "GEMINI_API_KEY" -w | head -c 10
```
