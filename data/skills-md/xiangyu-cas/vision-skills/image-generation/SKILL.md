---
name: image-generation
description: Gemini image generation and editing skill for text-to-image, image-to-image edits, multi-reference composition, and Google Search grounding. Use when creating or modifying images via Gemini (default model gemini-3-pro-image-preview) with the Python SDK.
---

# Image Generation with Gemini

Use this skill when the user asks to generate or edit images with Gemini using the Python SDK. Default to `gemini-3-pro-image-preview`, and mention `gemini-2.5-flash-image` only as an optional faster/cheaper alternative.

## Workflow

1) Identify task type (text-to-image, edit, or multi-reference).
2) Ensure `GEMINI_API_KEY` is available (env or stored in `.env`), then use the Python SDK. This will make network requests to the Gemini API
3) Choose model + output (`response_modalities=["IMAGE"]` if image-only) and run. Generation can take ~30 seconds; allow 30–60 seconds before retrying.
4) Save returned images with `part.as_image()`; if none, report a clear error.

## Use these references

- `references/python.md` for Python SDK usage

## Response handling (Python SDK)

Use `part.as_image()` to access image outputs and save them. If no image parts are returned, surface a clear error and suggest checking the API key, model name, and response modalities.

## Timing note

Image generation may take around 30 seconds. When running commands via the shell tool, set a longer timeout (e.g., 60–120 seconds) to avoid premature timeouts.
