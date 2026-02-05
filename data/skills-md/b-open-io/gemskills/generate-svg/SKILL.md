---
name: Generate SVG
description: This skill should be used when the user asks to "generate SVG", "create SVG", "make a logo", "create vector graphics", "generate icon", "make vector illustration", or needs scalable vector graphics generated via AI.
---

# Generate SVG

Generate SVG graphics using Gemini 3.0 Pro Preview.

## When to Use

Use this skill when the user asks to:
- Create SVG graphics, logos, or icons
- Generate vector illustrations
- Create scalable graphics

## Usage

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/generate-svg && bun run scripts/generate.ts "prompt" [options]
```

### Options

- `--instructions <text>` - Custom system instructions
- `--output <path>` - Output path (default: output.svg)

### Examples

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/generate-svg

# Simple SVG generation
bun run scripts/generate.ts "minimalist mountain logo"

# With custom instructions
bun run scripts/generate.ts "geometric pattern" --instructions "Use only blue and green colors"

# Save to specific file
bun run scripts/generate.ts "company logo" --output logo.svg
```

## Model

Uses `gemini-3-pro-preview` for SVG generation.
