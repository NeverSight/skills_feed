---
name: google-image-gen
description: >
  Generate images using Google's Gemini API. Use this skill when the user wants
  to generate, create, or edit images with AI. Keywords: image generation,
  create image, generate picture, AI art, edit image, Gemini, icon, render,
  illustration.
allowed-tools: Bash, Read, Glob
---

# Google Image Generation Skill

Generate images from text prompts using Google's Gemini API.

## First-Time Setup (Once Per Context)

Run these commands once at the start of a session:

```bash
.claude/skills/google-image-gen/scripts/check_env.sh
cd .claude/skills/google-image-gen && uv sync && cd -
```

If the environment check fails, the user needs to create `.env` in the skill directory with their API key from https://aistudio.google.com/apikey

## Usage

**Important:** Run the script from the skill directory. Use `../../../` to save images to the project root.

```bash
cd .claude/skills/google-image-gen && uv run python main.py ../../../<output_path> "<prompt>" [options]
```

**Project root path:** `../../../` (relative to skill directory)

**Note:** If the user specifies a custom output path (e.g., `images/photo.png`), they likely mean relative to the project root. Always prepend `../../../` to such paths (e.g., `../../../images/photo.png`).

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--style` | `-s` | Style template (.md file with `{subject}` placeholder) |
| `--ref` | `-r` | Reference image for style (repeatable, max 14) |
| `--edit` | `-e` | Edit existing image instead of generating |
| `--aspect` | `-a` | Aspect ratio: `1:1`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` |

## Examples

All examples assume you run from the skill directory (`cd .claude/skills/google-image-gen`).

### Simple Generation (saves to project root)

```bash
cd .claude/skills/google-image-gen && uv run python main.py ../../../output.png "A red apple on a wooden table"
```

### Save to subdirectory in project root

```bash
cd .claude/skills/google-image-gen && uv run python main.py ../../../images/output.png "A red apple"
```

### With Aspect Ratio

```bash
cd .claude/skills/google-image-gen && uv run python main.py ../../../thumb.png "Mountain landscape" --aspect 16:9
```

### Edit Existing Image

```bash
cd .claude/skills/google-image-gen && uv run python main.py ../../../output.png "Change the sky to sunset" --edit ../../../input.png
```

### With Reference Image

```bash
cd .claude/skills/google-image-gen && uv run python main.py ../../../output.png "Same style but with a car" --ref ../../../reference.png
```

### Multiple Variations

Generates numbered outputs (output_1.png, output_2.png, etc.):

```bash
cd .claude/skills/google-image-gen && uv run python main.py ../../../output.png "cat" "dog" "bird"
```

## Workflow

1. First use in context: Run setup commands (check_env.sh + uv sync)
2. Generate images as needed
3. Report output paths to user

## Notes

- Paid API tier recommended (free tier has strict rate limits)
- Output directories are created automatically
- Default aspect ratio is 16:9