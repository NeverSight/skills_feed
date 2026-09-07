---
name: codex-deepseek-vision
description: Use a configured third-party vision model to inspect local images and return grounded visual context that can be supplied to DeepSeek. Use this skill whenever a Codex + DeepSeek workflow needs image understanding, OCR, visual question answering, image description, or structured extraction from an image. Also use it when the agent recognizes it needs to view an image but the message delivers it as the placeholder `[Unsupported Image]` — treat that placeholder as the trigger to run the bridge on the attached image path or clipboard. Supports Qwen/DashScope and Gemini providers, provider selection through config.json, project-root .env API keys, configurable base URLs and model names, and optional thinking mode.
---

# Codex DeepSeek Vision

This project-level skill is a vision bridge for DeepSeek workflows. DeepSeek receives the text produced by a vision provider; it does not need to accept image bytes itself.

## Workflow

1. Read the project-level configuration at `.agents/skills/codex-deepseek-vision/config.json`.
2. Confirm `active_provider` is `qwen` or `gemini`. Keep provider credentials in the project-root `.env`; never put secret values in `config.json`, prompts, logs, or generated files.
3. Trigger recognition: If the user pasted or referenced an image but the conversation delivers it as `[Unsupported Image]` (the current model cannot consume image bytes), do not try to interpret the placeholder directly. Locate the image path — it is usually listed under "Files mentioned by the user" in the message, or in `local_images`/clipboard temp files. If no path is visible, the pasted image usually remains in the system clipboard; fall back to `--clipboard`.
4. If the user supplies a question with the image (in the message, filename context, or an accompanying attachment), use that question verbatim as the vision prompt. Do not replace it with a generic image-description prompt. Preserve the user's language and requested output format; only add a short instruction when needed to clarify that the answer must be grounded in the attached image.
5. Run `scripts/vision_bridge.py` with the image path (or `--clipboard`) and that prompt. Use an absolute image path when the working directory is uncertain. `--question` is an alias for `--prompt` when the input is explicitly a question.
6. Give the returned `text` to DeepSeek as visual context. Preserve the provider/model metadata when traceability matters.
7. If the image is unavailable, unreadable, too large, or the provider rejects the model, report the concrete error and ask for a corrected path or configuration. Do not invent visual observations.

Example (file path):

```bash
python3 .agents/skills/codex-deepseek-vision/scripts/vision_bridge.py \
  --image /absolute/path/chart.png \
  --question '图片中的销售额是多少？请只返回数字和单位。'
```

Example (clipboard — use when the image was pasted/screenshotted and no file path is known):

```bash
python3 .agents/skills/codex-deepseek-vision/scripts/vision_bridge.py \
  --clipboard \
  --question '这张截图里显示的报错是什么？'
```

`--image` and `--clipboard` are mutually exclusive; exactly one is required. The clipboard image is exported to a temporary file that the script deletes after the request, so no image bytes are ever written to a persistent upload location.

The script prints JSON to stdout. The `text` field is the vision answer to pass to DeepSeek. If neither `--question` nor `--prompt` is provided, the script uses `request.default_prompt` from `config.json`: a broad instruction to recognize and understand the image, including its contents, relationships, layout, visible text, data, and uncertainty. This is intentionally not an OCR-only prompt.

## Configuration

Edit `config.json` to choose the provider and model. The bundled defaults are:

| Provider | Default base URL | Default model | API key variable |
| --- | --- | --- | --- |
| `qwen` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen3.8-max` | `DASHSCOPE_API_KEY` |
| `gemini` | `https://generativelanguage.googleapis.com/v1beta` (official Gemini API) | `gemini-3.7-flash` | `GEMINI_API_KEY` |

These are the official model codes from the linked provider documentation. They are lowercase API identifiers, not the display names shown in product pages. If an account or gateway exposes a different identifier, edit only `base_url`, `endpoint`, or `model` in `config.json`; the bridge does not hard-code a catalog.

For Alibaba Cloud regional deployments, use the base URL format documented for the account, such as `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`, and replace `{WorkspaceId}` with the actual workspace ID. The public DashScope URL remains the default when the API key is provisioned for that endpoint.

`qwen3.8-max` uses the OpenAI-compatible Chat Completions shape with a multimodal `messages[].content` array. For local images, the bridge sends a Base64 Data URL in `image_url.url`, which the Qwen documentation explicitly supports. Gemini uses `POST <base_url>/models/<model>:generateContent`. With the current configuration, the final URL is `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.7-flash:generateContent`. The native request includes `contents[0].role: "user"`, a text `parts` entry, and an `inline_data` image `parts` entry. The bridge sends `x-goog-api-key` using `GEMINI_API_KEY`. For a compatible third-party gateway, override `base_url` (and, when necessary, `endpoint_style`) in `config.json`.

Thinking mode is only configurable for Qwen. It maps to an explicit `enable_thinking` boolean and an optional `thinking_budget`; this matters because `qwen3.8-max` defaults to thinking enabled. Gemini requests never include thinking fields.

## Image Inputs

The bridge accepts common local raster formats (`png`, `jpg`/`jpeg`, `webp`, `gif`, `bmp`, and `tif`/`tiff`). It converts the file to a data URL and sends it inline. Use `--mime-type` only when the file extension is missing or misleading. The image is never written to a temporary upload location by the bridge.

### Clipboard capture

`--clipboard` reads the image currently on the system clipboard instead of a file path. Platform support:

- **macOS** (default): read via `osascript`; screenshots (Cmd+Shift+4 / Cmd+Ctrl+Shift+4) work directly. PNG is preferred, TIFF is accepted as fallback.
- **Linux**: requires `xclip` (preferred) or `xsel` on the desktop session.
- **Windows**: reads via PowerShell (`System.Windows.Forms.Clipboard::GetImage`).

The captured image is written to a temp file, sent inline, and deleted after the request — even on failure. If the clipboard holds no image, the script fails with an explicit message instead of guessing.

## Provider-Specific Notes

Read [references/providers.md](references/providers.md) when changing request formats, endpoint paths, or thinking parameters. For routine use, the `config.json` values and the script are the source of truth.

## Failure Handling

- Missing `.env` key: stop with the variable name and a remediation message, without showing a secret.
- Non-2xx response: include HTTP status, sanitized response body, and available `x-request-id`, `x-client-request-id`, `cf-ray`, server, and content-type headers. These IDs are needed when a relay or Cloudflare returns a terse error.
- Malformed provider response: stop rather than passing an empty answer to DeepSeek.
- Retry only transient HTTP statuses (`408`, `429`, and `5xx`), with bounded exponential backoff. Do not retry authentication or schema errors.
