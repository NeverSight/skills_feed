---
name: baoyu-image-gen
description: AI image generation with OpenAI, Google, DashScope and Replicate APIs. Supports text-to-image, reference images, aspect ratios. Sequential by default; parallel generation available on request. Use when user asks to generate, create, or draw images.
---

# Image Generation (AI SDK)

Official API-based image generation. Supports OpenAI, Google, DashScope (阿里通义万象), Replicate, and xheai (中转站) providers.

## Script Directory

**Agent Execution**:
1. `SKILL_DIR` = this SKILL.md file's directory
2. Script path = `${SKILL_DIR}/scripts/main.ts`

## Step 0: Load Preferences ⛔ BLOCKING

**CRITICAL**: This step MUST complete BEFORE any image generation. Do NOT skip or defer.

Check EXTEND.md existence (priority: project → user):

```bash
test -f .baoyu-skills/baoyu-image-gen/EXTEND.md && echo "project"
test -f "$HOME/.baoyu-skills/baoyu-image-gen/EXTEND.md" && echo "user"
```

| Result | Action |
|--------|--------|
| Found | Load, parse, apply settings. If `default_model.[provider]` is null → ask model only (Flow 2) |
| Not found | ⛔ Run first-time setup ([references/config/first-time-setup.md](references/config/first-time-setup.md)) → Save EXTEND.md → Then continue |

**CRITICAL**: If not found, complete the full setup (provider + model + quality + save location) using AskUserQuestion BEFORE generating any images. Generation is BLOCKED until EXTEND.md is created.

| Path | Location |
|------|----------|
| `.baoyu-skills/baoyu-image-gen/EXTEND.md` | Project directory |
| `$HOME/.baoyu-skills/baoyu-image-gen/EXTEND.md` | User home |

**EXTEND.md Supports**: Default provider | Default quality | Default aspect ratio | Default image size | Default models

Schema: `references/config/preferences-schema.md`

## Usage

```bash
# ⚠️ 长prompt用 --promptfiles 或双引号包裹，避免换行解析错误
# 推荐: npx -y bun "${SKILL_DIR}/scripts/main.ts" -p "长prompt" --image out.png
# 或:   npx -y bun ${SKILL_DIR}/scripts/main.ts --promptfiles prompt.txt --image out.png

# Basic
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image cat.png

# With aspect ratio
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A landscape" --image out.png --ar 16:9

# High quality
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png --quality 2k

# From prompt files
npx -y bun ${SKILL_DIR}/scripts/main.ts --promptfiles system.md content.md --image out.png

# With reference images (Google multimodal or OpenAI edits)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Make blue" --image out.png --ref source.png

# With reference images (explicit provider/model)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Make blue" --image out.png --provider google --model gemini-3-pro-image-preview --ref source.png

# Specific provider
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png --provider openai

# DashScope (阿里通义万象)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "一只可爱的猫" --image out.png --provider dashscope

# Replicate (google/nano-banana-pro)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png --provider replicate

# Replicate with specific model
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png --provider replicate --model google/nano-banana

# xheai (中转站 - 兼容 OpenAI 格式)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png --provider xheai

# xheai with nano-banana-2
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png --provider xheai --model nano-banana-2
```

## Options

| Option | Description |
|--------|-------------|
| `--prompt <text>`, `-p` | Prompt text |
| `--promptfiles <files...>` | Read prompt from files (concatenated) |
| `--image <path>` | Output image path (required) |
| `--provider google\|openai\|dashscope\|replicate\|xheai` | Force provider (default: auto-detect) |
| `--model <id>`, `-m` | Model ID (Google: `gemini-3-pro-image-preview`, `gemini-3.1-flash-image-preview`; OpenAI: `gpt-image-1.5`; xheai: `gemini-3.1-flash-image-preview`, `nano-banana-2`) |
| `--ar <ratio>` | Aspect ratio (e.g., `16:9`, `1:1`, `4:3`) |
| `--size <WxH>` | Size (e.g., `1024x1024`) |
| `--quality normal\|2k` | Quality preset (default: 2k) |
| `--imageSize 1K\|2K\|4K` | Image size for Google (default: from quality) |
| `--ref <files...>` | Reference images. Supported by Google multimodal (`gemini-3-pro-image-preview`, `gemini-3-flash-preview`, `gemini-3.1-flash-image-preview`) and OpenAI edits (GPT Image models). If provider omitted: Google first, then OpenAI |
| `--n <count>` | Number of images |
| `--json` | JSON output |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key (also used for xheai when OPENAI_BASE_URL points to xheai.cc) |
| `GOOGLE_API_KEY` | Google API key |
| `DASHSCOPE_API_KEY` | DashScope API key (阿里云) |
| `REPLICATE_API_TOKEN` | Replicate API token |
| `OPENAI_IMAGE_MODEL` | OpenAI/xheai model override |
| `GOOGLE_IMAGE_MODEL` | Google model override |
| `DASHSCOPE_IMAGE_MODEL` | DashScope model override (default: z-image-turbo) |
| `REPLICATE_IMAGE_MODEL` | Replicate model override (default: google/nano-banana-pro) |
| `OPENAI_BASE_URL` | Custom OpenAI endpoint (set to https://api.xheai.cc for xheai) |
| `GOOGLE_BASE_URL` | Custom Google endpoint |
| `DASHSCOPE_BASE_URL` | Custom DashScope endpoint |
| `REPLICATE_BASE_URL` | Custom Replicate endpoint |
| `DEBUG_ENV` | Set to `1` to enable debug output for env loading and provider detection |

**Load Priority**: CLI args > EXTEND.md > env vars > `<cwd>/.baoyu-skills/.env` > `~/.baoyu-skills/.env`

**Cross-Platform Paths**: `~/.baoyu-skills/.env` automatically resolves to:
- Windows: `C:\Users\<username>\.baoyu-skills\.env`
- macOS: `/Users/<username>/.baoyu-skills/.env`
- Linux: `/home/<username>/.baoyu-skills/.env`

**Debug Mode**: Set `DEBUG_ENV=1` to see which .env files are loaded and which API keys are detected:
```bash
DEBUG_ENV=1 npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image cat.png
```

## Model Resolution

Model priority (highest → lowest), applies to all providers:

1. CLI flag: `--model <id>`
2. EXTEND.md: `default_model.[provider]`
3. Env var: `<PROVIDER>_IMAGE_MODEL` (e.g., `GOOGLE_IMAGE_MODEL`)
4. Built-in default

**EXTEND.md overrides env vars**. If both EXTEND.md `default_model.google: "gemini-3-pro-image-preview"` and env var `GOOGLE_IMAGE_MODEL=gemini-3.1-flash-image-preview` exist, EXTEND.md wins.

**Agent MUST display model info** before each generation:
- Show: `Using [provider] / [model]`
- Show switch hint: `Switch model: --model <id> | EXTEND.md default_model.[provider] | env <PROVIDER>_IMAGE_MODEL`

### Replicate Models

Supported model formats:

- `owner/name` (recommended for official models), e.g. `google/nano-banana-pro`
- `owner/name:version` (community models by version), e.g. `stability-ai/sdxl:<version>`

Examples:

```bash
# Use Replicate default model
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png --provider replicate

# Override model explicitly
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png --provider replicate --model google/nano-banana
```

## Provider Selection

1. `--ref` provided + no `--provider` → auto-select Google first, then OpenAI, then Replicate
2. `--provider` specified → use it (if `--ref`, must be `google`, `openai`, or `replicate`)
3. Only one API key available → use that provider
4. Multiple available → default to Google

## Quality Presets

| Preset | Google imageSize | OpenAI Size | Use Case |
|--------|------------------|-------------|----------|
| `normal` | 1K | 1024px | Quick previews |
| `2k` (default) | 2K | 2048px | Covers, illustrations, infographics |

**Google imageSize**: Can be overridden with `--imageSize 1K|2K|4K`

## Aspect Ratios

Supported: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `2.35:1`

- Google multimodal: uses `imageConfig.aspectRatio`
- Google Imagen: uses `aspectRatio` parameter
- OpenAI: maps to closest supported size

## Generation Mode

**Default**: Sequential generation (one image at a time). This ensures stable output and easier debugging.

**Parallel Generation**: Only use when user explicitly requests parallel/concurrent generation.

| Mode | When to Use |
|------|-------------|
| Sequential (default) | Normal usage, single images, small batches |
| Parallel | User explicitly requests, large batches (10+) |

**Parallel Settings** (when requested):

| Setting | Value |
|---------|-------|
| Recommended concurrency | 4 subagents |
| Max concurrency | 8 subagents |
| Use case | Large batch generation when user requests parallel |

**Agent Implementation** (parallel mode only):
```
# Launch multiple generations in parallel using Task tool
# Each Task runs as background subagent with run_in_background=true
# Collect results via TaskOutput when all complete
```

## Error Handling

- Missing API key → error with setup instructions
- Generation failure → auto-retry once
- Invalid aspect ratio → warning, proceed with default
- Reference images with unsupported provider/model → error with fix hint (switch to Google multimodal: `gemini-3-pro-image-preview`, `gemini-3.1-flash-image-preview`; or OpenAI GPT Image edits)

## Extension Support

Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options.
