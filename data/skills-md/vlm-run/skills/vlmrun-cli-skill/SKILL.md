---
name: vlmrun-cli-skill
description: "Use the VLM Run CLI (`vlmrun`) to interact with Orion visual AI agent. Process images, videos, and documents with natural language. Triggers: image understanding/generation, object detection, OCR, video summarization, document extraction, image generation, visual AI chat, 'generate an image/video', 'analyze this image/video', 'extract text from', 'summarize this video', 'process this PDF'."
---

# VLM Run CLI

Chat with VLM Run's Orion visual AI agent via CLI.

## Setup
```bash
uv venv && source .venv/bin/activate
uv pip install "vlmrun[cli]"
```

## Environment Variables

You must load the following variables in your environment so that the CLI can use them. You may load the [./env](./env) file to your environment.

| Variable | Type | Description |
|----------|------|-------------|
| `VLMRUN_API_KEY` | Required | Your VLM Run API key (required) |
| `VLMRUN_BASE_URL` | Optional | Base URL (default: `https://agent.vlm.run/v1`) |
| `VLMRUN_CACHE_DIR` | Optional | Cache directory (default: `~/.vlmrun/cache/artifacts/`) |

## Command

```bash
vlmrun chat "<prompt>" -i input.jpg [options]
```

## Options

| Flag | Description |
|------|-------------|
| `-p, --prompt` | Prompt text, file path, or `stdin` |
| `-i, --input` | Input file(s) - images, videos, docs (repeatable) |
| `-o, --output` | Artifact directory (default: `~/.vlmrun/cache/artifacts/`) |
| `-m, --model` | `vlmrun-orion-1:fast`, `vlmrun-orion-1:auto` (default), `vlmrun-orion-1:pro` |
| `-s, --session` | Optional session ID to continue a previous session |
| `-j, --json` | Raw JSON output |
| `-ns, --no-stream` | Disable streaming |
| `-nd, --no-download` | Skip artifact download |

## Examples

### Images
```bash
vlmrun chat "Describe what you see in this image in detail" -i photo.jpg
vlmrun chat "Detect and list all objects visible in this scene" -i scene.jpg
vlmrun chat "Extract all text and numbers from this document image" -i document.png
vlmrun chat "Compare these two images and describe the differences" -i before.jpg -i after.jpg
```

### Image Generation
```bash
vlmrun chat "Generate a photorealistic image of a cozy cabin in a snowy forest at sunset" -o ./generated
vlmrun chat "Remove the background from this product image and make it transparent" -i product.jpg -o ./output
```

### Video
```bash
vlmrun chat "Summarize the key points discussed in this meeting video" -i meeting.mp4
vlmrun chat "Find the top 3 highlight moments and create short clips from them" -i sports.mp4
vlmrun chat "Transcribe this lecture with timestamps for each section" -i lecture.mp4 --json
```

### Video Generation
```bash
vlmrun chat "Generate a 5-second video of ocean waves crashing on a rocky beach at golden hour" -o ./videos
vlmrun chat "Create a smooth slow-motion video from this image" -i ocean.jpg -o ./output
```

### Documents
```bash
vlmrun chat "Extract the vendor name, line items, and total amount" -i invoice.pdf --json
vlmrun chat "Summarize the key terms and obligations in this contract" -i contract.pdf
```

### Prompt Sources
```bash
# Direct prompt
vlmrun chat "What objects and people are visible in this image?" -i photo.jpg

# Prompt from file
vlmrun chat -p long_prompt.txt -i photo.jpg

# Prompt from stdin
echo "Describe this image in detail" | vlmrun chat - -i photo.jpg
```

### Continuing a previous session
If you want to keep the past conversation and generated artifacts in context, you can use the `-s` flag to continue a previous session using the session ID generated when you started the session.

```bash
# Start a new session of an image generation task where a new character is generated
vlmrun chat "Create an iconic scene of a ninja in a forest, practicing his skills with a katana?" -i photo.jpg

# Use the previous chat session in context to retain the same character and scene context (where the session ID is <session_id>)
vlmrun chat "Create a new scene with the same character meditating under a tree" -i photo.jpg -s <session_id>
```

### Skipping artifact download
If you want to skip the artifact download, you can use the `-nd` flag.
```bash
vlmrun chat "What objects and people are visible in this image?" -i photo.jpg -nd
```

## Notes

- Use `-o ./<directory>` to save generated artifacts (images, videos) relative to your current working directory
- Without `-o`, artifacts save to `~/.vlmrun/cache/artifacts/<session_id>/`
- Multiple input files upload concurrently
