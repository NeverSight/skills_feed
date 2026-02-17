---
name: nanobanana
description: Use when "nanobanana", "generate image", "create image", "edit image", "AI drawing", "Gemini image", "image generation"
version: 1.0.0
---

# Nanobanana Image Generation

Generate and edit images using Google Gemini API.

---

## Prerequisites

| Requirement | Setup |
|-------------|-------|
| **API Key** | Export `GEMINI_API_KEY` or add to `~/.nanobanana.env` |
| **Dependencies** | `pip install google-genai Pillow python-dotenv` |
| **Script** | `${CLAUDE_PLUGIN_ROOT}/skills/core/nanobanana/nanobanana.py` |

---

## Basic Usage

| Task | Command |
|------|---------|
| **Generate image** | `python3 nanobanana.py --prompt "description" --output "file.png"` |
| **Edit image** | `python3 nanobanana.py --prompt "changes" --input source.png --output "edited.png"` |

---

## Aspect Ratios

| Size | Ratio | Use Case |
|------|-------|----------|
| `1024x1024` | 1:1 | Square, logos |
| `768x1344` | 9:16 | Portrait, stories (default) |
| `1344x768` | 16:9 | Landscape, wallpapers |
| `832x1248` | 2:3 | Portrait photos |
| `1248x832` | 3:2 | Landscape photos |
| `1536x672` | 21:9 | Ultra-wide |

Use `--size WIDTHxHEIGHT` to specify.

---

## Models

| Model | Trade-off |
|-------|-----------|
| `gemini-3-pro-image-preview` | Higher quality (default) |
| `gemini-2.5-flash-image` | Faster generation |

Use `--model MODEL` to specify.

---

## Resolution

| Resolution | Use Case |
|------------|----------|
| `1K` | Testing, drafts (default) |
| `2K` | Good quality |
| `4K` | Final output, print |

Use `--resolution RES` to specify.

---

## Best Practices

| Practice | Why |
|----------|-----|
| Be descriptive | Include style, mood, colors, composition |
| Use 1:1 for logos | Clean square format |
| Use 9:16 for stories | Standard mobile format |
| Use 16:9 for wallpapers | Standard widescreen |
| Start with 1K | Test before using higher resolution |
| Use flash model for iteration | Save time during drafting |

---

## Examples

**Generate landscape:**

```bash
python3 nanobanana.py --prompt "Mountain sunset with lake" --size 1344x768 --output "landscape.png"
```

**Generate logo:**

```bash
python3 nanobanana.py --prompt "Minimalist tech logo" --size 1024x1024 --output "logo.png"
```

**Edit existing image:**

```bash
python3 nanobanana.py --prompt "Add rainbow to sky" --input photo.png --output "edited.png"
```

**High quality output:**

```bash
python3 nanobanana.py --prompt "Professional portrait" --resolution 2K --output "portrait.png"
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Script fails | Check `GEMINI_API_KEY` is set |
| No image generated | Make prompt more specific |
| Can't read input | Verify file exists and is readable |
| Can't write output | Check directory is writable |
