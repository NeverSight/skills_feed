---
name: video-generation
description: Gemini video generation with Veo 3.1 via the Python SDK. Use when generating videos from text or images, using reference images, first/last frame interpolation, or video extension, and when tuning Veo parameters (aspect ratio, resolution, duration, negative prompts, personGeneration, seed).
---

# Video Generation with Gemini (Veo 3.1)

Use this skill when the user asks to generate or extend videos with Gemini using the Python SDK.
Default to `veo-3.1-fast-generate-preview`, `resolution="720p"`, and `duration_seconds=4`, unless the user asks otherwise or the task requires different settings (e.g., extension, interpolation, reference images, 1080p/4k).

## Workflow

1) Identify the task type: text-to-video, image-to-video, reference images, first/last frames (interpolation), or video extension.
2) Ensure `GEMINI_API_KEY` is available (env or local `.env`), then use the Python SDK.
3) When using images, pass `types.Image(imageBytes=..., mimeType=...)` (not `PIL.Image` or `types.Part`) to avoid input type errors.
4) Call `client.models.generate_videos(...)` with the correct inputs/config (see references).
5) Poll the operation until `done`, then download and save the video.
6) If no videos are returned, surface a clear error and suggest checking the API key, model, and config.

## Use these references (by task type)

- Common setup and workflow: `references/overview.md`
- Parameters and constraints: `references/parameters.md`
- Model versions and limits: `references/model-versions-and-limitations.md`
- Prompting guidance: `references/prompt-guide.md`

### Task types

- Text-to-video: `examples/text-to-video.md`
- Image-to-video: `examples/image-to-video.md`
- Reference images: `examples/reference-images.md`
- First/last frames (interpolation): `examples/first-last-frames.md`
- Video extension: `examples/video-extension.md`

### Tuning examples

- Aspect ratio: `examples/aspect-ratio.md`
- Resolution (4k): `examples/resolution.md`
- Negative prompt: `examples/negative-prompt.md`

## Defaults and notes

- Default model: `veo-3.1-fast-generate-preview`.
- Default output: 720p, 4 seconds.
- For image inputs, always provide `imageBytes` + `mimeType` via `types.Image` to prevent `INVALID_ARGUMENT` errors.
- 1080p/4k, reference images, interpolation, and video extension require `duration_seconds=8`.
- Video extension is limited to 720p inputs and requires a video from a previous Veo generation.
- Video generation can take minutes; allow longer timeouts when running commands.
