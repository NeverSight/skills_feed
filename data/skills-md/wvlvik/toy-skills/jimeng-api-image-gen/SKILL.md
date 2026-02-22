---
name: jimeng-api-image-gen
description: (project - Skill) Generate AI images using Volcengine Jimeng API 4.0. Use when users request image generation from text prompts, image-to-image editing, or batch image creation. Triggers include "generate image", "create picture", "AI image", "Jimeng", "Seedream", or any request involving AI-powered image creation from descriptions.
---

# Jimeng API Image Generation

Generate high-quality AI images using Volcengine's Jimeng 4.0 API with text prompts or image inputs.

## Configure Environment Variables

[Get Access Key/Secret Key](https://www.volcengine.com/docs/85621/1995636?lang=zh#3C9mCW9O)

```bash
# ~/.zshrc or ~/.zshenv
export VOLC_ACCESSKEY="your_access_key_id"
export VOLC_SECRETKEY="your_secret_access_key"
```

## Output Behavior (Important)

**After image generation succeeds, you MUST display the image directly to the user!**

When generation completes, output in the following format:

```markdown
![Generated Image](IMAGE_URL)

**Generation Info:**
- Prompt: [User's original prompt]
- Size: [Image dimensions]
- Save Path: [Local file path, if applicable]
```

### Example Output

```markdown
![Shiba Inu under cherry blossoms](https://example.com/image.png)

**Generation Info:**
- Prompt: Shiba Inu under cherry blossom tree, warm sunlight, healing art style
- Size: 2304 × 1728
- Save Path: /generated_images/[Generated Image] **important**
```

### Notes

1. **Prefer markdown image syntax** `![description](URL)` to display images directly
2. **Also provide the online link** for easy copying and sharing
3. **If saved locally**, display the local file path
4. **For multiple images**, display each one with numbered labels

## Quick Start

### Step 1: Run Generation

```bash
# Text-to-image
scripts/generate_image.py "A white Siamese cat sitting on a windowsill, sunlight streaming in"

# With specific size
scripts/generate_image.py "Mountain sunset landscape" --size 2K

# Image-to-image editing
scripts/generate_image.py "Change to watercolor style" --images https://example.com/input.jpg

# Save to file
scripts/generate_image.py "Serene lake at sunset" --output /generated_images/lake.png
```

## API Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Endpoint | `https://visual.volcengineapi.com` | API base URL |
| Submit Action | `CVSync2AsyncSubmitTask` | Submit async generation task |
| Query Action | `CVSync2AsyncGetResult` | Query task result |
| Version | `2022-08-31` | API version |
| Service | `cv` | Service name for signing |
| Region | `cn-north-1` | Region for signing |
| req_key | `jimeng_t2i_v40` | Jimeng AI 4.0 model identifier |

## Image Size Options

### Preset Resolutions

| Preset | Resolution | Pixels |
|--------|------------|--------|
| 1K | 1024×1024 | 1,048,576 |
| 2K | 2048×2048 | 4,194,304 (default) |
| 4K | 4096×4096 | 16,777,216 |

### Exact Dimensions

Use `--width` and `--height` together:

```bash
scripts/generate_image.py "prompt" --width 2560 --height 1440
```

**Recommended aspect ratios:**
- 1:1 (2048x2048) - Social media posts
- 4:3 (2304x1728) - Presentations  
- 16:9 (2560x1440) - Widescreen displays
- 9:16 (1440x2560) - Mobile vertical
- 3:2 (2496x1664) - Photography

**Constraints:**
- Width × Height must be in [1024×1024, 4096×4096]
- Aspect ratio (width/height) in [1/16, 16]
- Recommended: Use 2K+ for better quality

## Command-Line Options

```
scripts/generate_image.py PROMPT [OPTIONS]

Arguments:
  PROMPT              Text prompt for image generation (required, max 800 chars)

Options:
  --size SIZE         Image size: 1K, 2K, 4K or WxH (default: 2K)
  --width WIDTH       Exact width (requires --height)
  --height HEIGHT     Exact height (requires --width)
  --images URL [...]  Input image URLs for image-to-image (max 10)
  --watermark         Add "AI Generated" watermark
  --scale FLOAT       Text influence 0-1 (default: 0.5)
  --force-single      Force single image output
  --output PATH       Download image to file
  --json              Output raw JSON response

Environment Variables:
  VOLC_ACCESSKEY           Access Key ID (required)
  VOLC_SECRETKEY           Secret Access Key (required)
  JIMENG_API_URL           API endpoint (default: https://visual.volcengineapi.com)
  JIMENG_API_TIMEOUT       Request timeout seconds (default: 120)
  JIMENG_POLL_INTERVAL     Polling interval seconds (default: 2)
  JIMENG_MAX_POLL_ATTEMPTS Max polling attempts (default: 60)
```

## Authentication

This skill uses Volcengine IAM v4 signature authentication (HMAC-SHA256). The signing process:

1. Build canonical request with headers: `content-type;host;x-content-sha256;x-date`
2. Calculate SHA256 hash of canonical request
3. Derive signing key: secret_key → date → region → service → "request"
4. Sign the string-to-sign with derived key
5. Add `Authorization` header to request

Reference: [HTTP请求示例](https://www.volcengine.com/docs/6444/1390583)

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 10000 | Success | Request successful |
| 50411 | Pre Img Risk Not Pass | Input image failed content check |
| 50511 | Post Img Risk Not Pass | Output image failed content check |
| 50412 | Text Risk Not Pass | Input text failed content check |
| 50413 | Post Text Risk Not Pass | Input text contains sensitive words |
| 50429 | Request Has Reached API Limit | Rate limit exceeded, retry later |
| 50500 | Internal Error | Server error |
| timeout | Request timeout | Increase JIMENG_API_TIMEOUT |

## Input/Output Limits

**Input Images:**
- Format: JPEG, PNG only
- Max files: 10 images
- Max size: 15MB per image
- Max resolution: 4096×4096
- Aspect ratio (W/H): [1/3, 3]

**Output:**
- Max images: 15 - (input image count)
- Format: PNG
- URL validity: 24 hours

## Reference Documentation

- [Jimeng AI 4.0 API Documentation](https://www.volcengine.com/docs/85621/1817045)
- [HTTP Request Example](https://www.volcengine.com/docs/6444/1390583)
- [Volcengine Console](https://console.volcengine.com)
- [API Key Management](https://console.volcengine.com/iam/key_manage/)
