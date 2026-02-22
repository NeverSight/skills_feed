---
name: kling-video
description: "Generate AI videos using Kling video generation models. Use when you need to: (1) create videos from text prompts, (2) animate images into videos, (3) transform existing videos with AI, or (4) create AI avatar videos with speech."
tags:
  - ai-video
  - media-generation
version: 1.0.0
skillId: skp-d8eft4uduju18mhdv19pnpeb
workflowId: c-p3ydudm0cbdu13cmqodjqwhu
installationId: skpi-rzakvguz9m7memgp3o6dokta
triggers:
  - kling video
  - text to video
  - image to video
  - video generation
  - ai avatar
category: file-generation
---

# Kling Video

Generate AI videos using Kling video generation models. Use when you need to: (1) create videos from text prompts, (2) animate images into videos, (3) transform existing videos with AI, or (4) create AI avatar videos with speech.

## Input

Provide input as JSON:

```json
{
  "video_prompt": "Text description for the video you want to generate (e.g., 'A cat walking in a futuristic city at sunset')",
  "image_url": "<file-id>",
  "video_url": "<file-id>",
  "model_version": "Kling model to use: 'o1' for advanced reasoning or 'v2.6' for premium visuals",
  "duration": "Video duration in seconds (5-10s supported)",
  "aspect_ratio": "Video aspect ratio: '16:9' (landscape), '9:16' (portrait), or '1:1' (square)"
}
```

**Note on File Inputs:**
- `image_url` and `video_url` require a **file ID** (format: `df-xxxxx`)
- **How to get file ID:**
  1. Upload your file to Refly using `refly file upload <file-path>`
  2. Copy the returned file ID from the upload response
  3. Use this file ID in the input JSON
- For text-to-video mode, omit both `image_url` and `video_url`
- For image-to-video mode, provide `image_url`
- For video-to-video mode, provide `video_url`

## Execution (Pattern A: File Generation)

### Step 0 (Optional): Upload Files for Image/Video-to-Video Modes

```bash
# Upload an image for image-to-video
IMAGE_RESULT=$(refly file upload /path/to/your/image.jpg)
IMAGE_FILE_ID=$(echo "$IMAGE_RESULT" | jq -r '.payload.fileId')
echo "Image file ID: $IMAGE_FILE_ID"

# Or upload a video for video-to-video
VIDEO_RESULT=$(refly file upload /path/to/your/video.mp4)
VIDEO_FILE_ID=$(echo "$VIDEO_RESULT" | jq -r '.payload.fileId')
echo "Video file ID: $VIDEO_FILE_ID"
```

### Step 1: Run the Skill and Get Run ID

**Example 1: Text-to-Video**
```bash
RESULT=$(refly skill run --id skpi-rzakvguz9m7memgp3o6dokta --input '{
  "video_prompt": "A cat walking through a futuristic city at sunset",
  "duration": "5",
  "aspect_ratio": "16:9",
  "model_version": "v2.6"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

**Example 2: Image-to-Video**
```bash
# Use the IMAGE_FILE_ID from Step 0
RESULT=$(refly skill run --id skpi-rzakvguz9m7memgp3o6dokta --input '{
  "video_prompt": "Camera slowly zooms in on the scene",
  "image_url": "'"$IMAGE_FILE_ID"'",
  "duration": "5",
  "aspect_ratio": "16:9",
  "model_version": "v2.6"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-p3ydudm0cbdu13cmqodjqwhu"
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

- **Type**: Video
- **Format**: .mp4 video file
- **Location**: `~/Desktop/`
- **Action**: Opens automatically to show user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
