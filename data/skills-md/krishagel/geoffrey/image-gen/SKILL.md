---
name: image-gen
description: Generate images using Google's Nano Banana Pro (Gemini 3 Pro Image) with workflow-based prompting
triggers:
  - "create image"
  - "generate image"
  - "make infographic"
  - "create infographic"
  - "generate diagram"
  - "make diagram"
  - "design visual"
  - "create visual"
allowed-tools: Read, Write, Bash
version: 0.1.0
---

# Image Generation Skill

Generate professional images, infographics, and diagrams using Google's Nano Banana Pro model (gemini-3-pro-image-preview).

## Model Capabilities

**Nano Banana Pro** (released November 20, 2025):
- **Text rendering** - Accurate, legible text in images
- **Google Search grounding** - Real-time data (weather, stocks, etc.)
- **Multi-turn conversation** - Iterative refinement
- **Up to 14 reference images** - For composition and style transfer
- **Resolutions**: 1K, 2K, 4K
- **Aspect ratios**: 1:1, 2:3, 3:2, 4:3, 16:9, 21:9

## Scripts

All scripts use Python via `uv run` with inline dependencies.

### generate.py - Text to Image
```bash
uv run scripts/generate.py "prompt" output.png [aspect_ratio] [size]
```

**Examples:**
```bash
# Basic image
uv run scripts/generate.py "A cozy coffee shop in autumn" coffee.png

# Infographic with specific aspect ratio
uv run scripts/generate.py "Infographic explaining how neural networks work" nn.png 16:9 2K

# 4K professional image
uv run scripts/generate.py "Professional headshot, studio lighting" headshot.png 3:2 4K
```

### edit.py - Image Editing
```bash
uv run scripts/edit.py input.png "edit instructions" output.png
```

**Examples:**
```bash
# Edit existing image
uv run scripts/edit.py photo.png "Change the background to a beach sunset" edited.png
```

### compose.py - Multi-Image Composition
```bash
uv run scripts/compose.py "prompt" output.png --refs image1.png image2.png
```

**Examples:**
```bash
# Combine styles from multiple images
uv run scripts/compose.py "Combine these styles into a logo" logo.png --refs style1.png style2.png
```

## Workflows

Workflows provide structured approaches for specific visual types. Each workflow follows the PAI 6-step editorial process:

1. **Extract narrative** - Understand the complete story/concept
2. **Derive visual concept** - Single metaphor with 2-3 physical objects
3. **Apply aesthetic** - Define style, colors, mood
4. **Construct prompt** - Build detailed generation instructions
5. **Generate** - Execute via script
6. **Validate** - Check against criteria, regenerate if needed

### Available Workflows

- **infographic.md** - Data visualization, statistics, explainers
- **diagram.md** - Technical diagrams, flowcharts, architecture

## Workflow Usage

When generating images, follow the appropriate workflow:

### For Infographics
```markdown
1. What data/concept needs visualization?
2. What's the key insight or takeaway?
3. Aspect ratio: 16:9 (landscape) recommended
4. Include: clear hierarchy, minimal text, supporting icons
5. Generate at 2K minimum for text clarity
```

### For Diagrams
```markdown
1. What system/process is being illustrated?
2. What are the key components and relationships?
3. Style: flat colors, clean lines, minimal detail
4. Generate at 2K for label clarity
```

## Environment Setup

Requires `GEMINI_API_KEY` environment variable. This should be set from Geoffrey's secrets:

```bash
source ~/Library/Mobile\ Documents/com~apple~CloudDocs/Geoffrey/secrets/.env
```

## Best Practices

### Infographics
- Use simple, direct prompts: "Infographic explaining how X works"
- Model auto-includes relevant icons/logos
- 16:9 aspect ratio works best
- Generate at 2K+ for readable text

### General
- Multi-turn refinement: generate, then ask for specific changes
- Reference images improve consistency
- Be specific about style, mood, lighting
- SynthID watermark is automatic (Google provenance)

## Output Location

By default, save images to `/tmp/` or user-specified paths. For persistent storage, use:
```
~/Library/Mobile Documents/com~apple~CloudDocs/Geoffrey/images/
```

## ⚠️ CRITICAL: Never Read Generated Images

**DO NOT use the Read tool on generated images.**

Why:
- 4K images (3840x2160) are within the 8000px limit
- 2K images (2560x1440) are also safe
- BUT: Do not Read them - they're for user consumption, not analysis
- For edits, use edit.py script, not Read tool

Workflow:
1. Generate image with script
2. Return file path to user
3. User views the high-quality output

## Limitations

- No photorealistic humans (safety filter)
- No copyrighted characters
- Maximum 14 reference images for composition
- 4K only available with Nano Banana Pro

## Pricing

| Size | Cost per Image |
|------|---------------|
| 1K | Free tier / $0.04 |
| 2K | $0.134 |
| 4K | $0.24 |
