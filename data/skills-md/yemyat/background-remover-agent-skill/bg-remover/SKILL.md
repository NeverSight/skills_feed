---
name: bg-remover
description: Remove backgrounds from images using FAL.ai's BiRefNet model. Use when users ask to remove background, make transparent PNG, extract subject from image, or create cutouts. Trigger phrases include "remove background", "transparent background", "cut out", "extract subject", or any background removal request.
---

# Background Remover Skill

Remove backgrounds from images using FAL.ai's BiRefNet v2 model. Uses Bun for fast TypeScript execution with inline scripts.

## Prerequisites

This skill requires:
- **Bun** - Fast JavaScript runtime
- **FAL_KEY** - FAL.ai API key set as environment variable

### Checking for Bun

Before running scripts, verify Bun is installed:

```bash
which bun
```

If Bun is not installed, **ask the user for permission** before installing:

```bash
npm install -g bun
```

### Setting up FAL.ai

1. Get an API key from https://fal.ai/dashboard/keys
2. Set the environment variable: `export FAL_KEY="your-key-here"`

## Basic Usage

Remove background from an image using a heredoc script:

```bash
bun run - << 'EOF'
import { fal } from "@fal-ai/client";
import { readFileSync, writeFileSync } from "fs";
import { basename, dirname, join } from "path";

const imagePath = "INPUT_IMAGE_PATH";
const imageBuffer = readFileSync(imagePath);
const fileName = basename(imagePath);
const mimeType = imagePath.endsWith(".png") ? "image/png" : "image/jpeg";

// Upload to FAL storage
const file = new File([imageBuffer], fileName, { type: mimeType });
const imageUrl = await fal.storage.upload(file);
console.log("Uploaded:", imageUrl);

// Remove background
const result = await fal.subscribe("fal-ai/birefnet/v2", {
  input: {
    image_url: imageUrl,
    model: "General Use (Light)",
    operating_resolution: "1024x1024",
    output_format: "png"
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS" && update.logs) {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  },
});

// Download and save result
const outputUrl = result.data.image.url;
const response = await fetch(outputUrl);
const buffer = Buffer.from(await response.arrayBuffer());

const dir = dirname(imagePath);
const nameWithoutExt = basename(imagePath, basename(imagePath).match(/\.[^.]+$/)?.[0] || "");
const outputPath = join(dir, `${nameWithoutExt}-nobg.png`);

writeFileSync(outputPath, buffer);
console.log("Saved:", outputPath);
EOF
```

Replace `INPUT_IMAGE_PATH` with the actual path to the image.

## Model Options

The BiRefNet model supports different configurations:

### Model Variants
- `"General Use (Light)"` - Fast, good for most images (default)
- `"General Use (Heavy)"` - Higher quality, slower processing
- `"Portrait"` - Optimized for human subjects
- `"Matting"` - Best for complex edges like hair

### Operating Resolutions
- `"1024x1024"` - Standard quality (default)
- `"2048x2048"` - Higher detail for large images

### Additional Options
- `refine_foreground: true` - Improve edge quality
- `output_format: "png"` - Always use PNG for transparency

## Configuration Example

For high-quality portrait extraction:

```bash
bun run - << 'EOF'
import { fal } from "@fal-ai/client";
import { readFileSync, writeFileSync } from "fs";
import { basename, dirname, join } from "path";

const imagePath = "INPUT_IMAGE_PATH";
const imageBuffer = readFileSync(imagePath);
const fileName = basename(imagePath);
const mimeType = imagePath.endsWith(".png") ? "image/png" : "image/jpeg";

const file = new File([imageBuffer], fileName, { type: mimeType });
const imageUrl = await fal.storage.upload(file);

const result = await fal.subscribe("fal-ai/birefnet/v2", {
  input: {
    image_url: imageUrl,
    model: "Portrait",
    operating_resolution: "2048x2048",
    refine_foreground: true,
    output_format: "png"
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS" && update.logs) {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  },
});

const response = await fetch(result.data.image.url);
const buffer = Buffer.from(await response.arrayBuffer());

const dir = dirname(imagePath);
const nameWithoutExt = basename(imagePath, basename(imagePath).match(/\.[^.]+$/)?.[0] || "");
const outputPath = join(dir, `${nameWithoutExt}-nobg.png`);

writeFileSync(outputPath, buffer);
console.log("Saved:", outputPath);
EOF
```

## Key Principles

1. **Check prerequisites**: Always verify Bun is installed before running
2. **Ask before installing**: Get user permission before `npm install -g bun`
3. **Use heredocs**: Run inline scripts for one-off operations
4. **Preserve location**: Save output next to input with `-nobg` suffix
5. **Always PNG**: Output format must be PNG for transparency

## Workflow

1. **Verify Bun** is installed (offer to install if not)
2. **Verify FAL_KEY** is set
3. **Run the script** with the input image path
4. **Check the output** - view the saved PNG with transparent background

## Error Recovery

If a script fails:
1. Check FAL_KEY is set: `echo $FAL_KEY`
2. Verify image path exists and is readable
3. Check FAL.ai dashboard for quota/billing issues
4. Try a smaller image if upload fails

## API Response Format

The BiRefNet model returns:

```json
{
  "image": {
    "url": "https://...",
    "width": 1024,
    "height": 1024,
    "content_type": "image/png",
    "file_name": "birefnet-output.png"
  }
}
```

## Advanced Usage

For batch processing, URL-based inputs, or integration with other tools, see `references/guide.md`.
