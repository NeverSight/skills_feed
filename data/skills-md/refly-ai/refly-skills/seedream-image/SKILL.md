---
name: seedream-image
description: "Generate AI images using ByteDance Seedream 4.5. Use when you need to: (1) create images from text descriptions, (2) transform images with style transfer, or (3) generate high-quality artistic or realistic images."
version: 1.0.0
skillId: skp-pa4laqd42cze8sxl9r8dp416
workflowId: c-i51ssnvhcjdou7l0h3ote7d9
installationId: skpi-m56jo9am75xgijga62hd7t8g
category: file-generation
---

# Seedream Image

Generate AI images using ByteDance Seedream 4.5. Use when you need to: (1) create images from text descriptions, (2) transform images with style transfer, or (3) generate high-quality artistic or realistic images.

## Input

Provide input as JSON:

```json
{
  "prompt": "Text description of the image you want to generate or edit",
  "image_size": "Image size: square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9, auto_2K, auto_4K (default: auto_2K)",
  "num_images": "Number of images to generate (1-10, default: 1)",
  "reference_image": "<file-id>",
  "enable_safety_checker": "Enable safety checker (true/false, default: true)"
}
```

**Note on File Input:**
- `reference_image` is optional and requires a **file ID** (format: `df-xxxxx`) if provided
- **How to get file ID:**
  1. Upload your reference image to Refly using `refly file upload <file-path>`
  2. Copy the returned file ID from the upload response
  3. Use this file ID in the input JSON
- Omit `reference_image` for pure text-to-image generation
- Provide `reference_image` for image-to-image editing (supports up to 10 images)

## API Request Structure

This skill uses **Seedream 4.5 API** with the following structure:

### Text-to-Image
```json
{
  "prompt": "Your prompt here",
  "image_size": "auto_2K",
  "num_images": 1,
  "max_images": 1,
  "enable_safety_checker": true
}
```

### Image-to-Image (With Reference)
```json
{
  "prompt": "Edit instructions here",
  "image_size": "auto_4K",
  "num_images": 1,
  "max_images": 1,
  "enable_safety_checker": true,
  "image_urls": [
    "URL_of_reference_image_1",
    "URL_of_reference_image_2"
  ]
}
```

**Notes:**
- When `image_urls` is empty/not provided → **Text-to-Image** mode
- When `image_urls` is provided → **Image-to-Image** mode
- Supports up to 10 input images
- Total images (input + output) must not exceed 15
- `image_size` options: square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9, auto_2K, auto_4K

## Execution (Pattern A: File Generation)

### Step 0 (Optional): Upload Reference Image

```bash
# Upload a reference image for image-to-image generation
REF_RESULT=$(refly file upload /path/to/reference.jpg)
REF_FILE_ID=$(echo "$REF_RESULT" | jq -r '.payload.fileId')
echo "Reference image file ID: $REF_FILE_ID"
```

### Step 1: Run the Skill and Get Run ID

**Example 1: Text-to-Image**
```bash
RESULT=$(refly skill run --id skpi-m56jo9am75xgijga62hd7t8g --input '{
  "prompt": "A beautiful mountain landscape at sunset with vibrant colors",
  "image_size": "landscape_16_9",
  "num_images": 1,
  "enable_safety_checker": true
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

**Example 2: Image-to-Image Editing**
```bash
# Use the REF_FILE_ID from Step 0
RESULT=$(refly skill run --id skpi-m56jo9am75xgijga62hd7t8g --input '{
  "prompt": "Transform this into anime style with vibrant colors and dramatic lighting",
  "reference_image": "'"$REF_FILE_ID"'",
  "image_size": "auto_4K",
  "num_images": 1,
  "enable_safety_checker": true
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-i51ssnvhcjdou7l0h3ote7d9"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Download and Show Result

```bash
# Get files from this run
FILES=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.files[]')

# Download and open each file
echo "$FILES" | jq -c '.' | while read -r file; do
  FILE_ID=$(echo "$file" | jq -r '.fileId')
  FILE_NAME=$(echo "$file" | jq -r '.name')
  if [ -n "$FILE_ID" ] && [ "$FILE_ID" != "null" ]; then
    refly file download "$FILE_ID" -o "$HOME/Desktop/${FILE_NAME}"
    open "$HOME/Desktop/${FILE_NAME}"
  fi
done
```

## Expected Output

- **Type**: Image
- **Format**: .png/.jpg image file
- **Location**: `~/Desktop/`
- **Action**: Opens automatically to show user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
