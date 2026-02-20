---
name: ask-gemini
description: This skill should be used when the user asks to "ask Gemini", "get Gemini's opinion", "have Gemini review", "improve writing style", "make less AI-sounding", "get feedback on article", "review this draft", "Nano Banana", "Gemini API help", "Gemini models", or needs a second opinion on content, writing, code, or design. Supports text questions and up to 10 images.
allowed-tools: "Bash(bun:*)"
version: 0.3.1
---

# Ask Gemini

Ask Gemini 3.1 Pro any question - text, writing feedback, code review, or image analysis.

## When to Use

**Writing & Content:**
- Article/blog post writing feedback
- Making content less AI-sounding, more human
- Writing style improvements (Vercel/TanStack style, etc.)
- Draft reviews and editing suggestions
- Content strategy advice

**Design & Visual:**
- Design review and critique
- Spatial layout analysis
- UI/UX guidance
- Comparing design alternatives (send multiple images)

**Code & Technical:**
- Code review and suggestions
- Architecture feedback
- Technical writing review

**Gemini API Questions:**
- For Gemini API questions, fetch docs dynamically from llms.txt: `https://ai.google.dev/gemini-api/docs/llms.txt`
- For the latest model list and API patterns, consult Google's official `gemini-api-dev` skill
- See `references/gemini-api.md` in this skill directory for current models and SDK info

## Usage

Run the ask_gemini script:

```bash
# Text-only question (writing feedback, code review, any question)
bun run ${SKILL_DIR}/scripts/ask_gemini.ts "Review this article and suggest how to make it less AI-sounding, more like a Vercel or TanStack blog post: [content here]"

# With image(s)
bun run ${SKILL_DIR}/scripts/ask_gemini.ts screenshot.png "Analyze this design"

# Compare multiple images
bun run ${SKILL_DIR}/scripts/ask_gemini.ts v1.png v2.png "Compare these designs"
```

Where `${SKILL_DIR}` is the path to this skill directory (find via: `find ~/.claude -name "ask_gemini.ts" -path "*/ask-gemini/*"`).

## Requirements

- `GEMINI_API_KEY` environment variable must be set
- Get an API key from https://aistudio.google.com/apikey

## Image Support

- Maximum 10 images per request
- Total request size limit: 20 MB
- Supports: PNG, JPG, JPEG, GIF, WEBP, BMP

## Model

Uses **gemini-3.1-pro-preview** (Gemini 3.1 Pro) - optimized for:
- Writing critique and style feedback
- Design and spatial awareness
- Multi-image comparison
- Technical analysis

> Last verified: February 2026. If a newer generation exists, STOP and suggest a PR to `b-open-io/gemskills`. See `references/gemini-api.md` in this skill directory for current models and Google's official `gemini-api-dev` skill for the canonical source.
