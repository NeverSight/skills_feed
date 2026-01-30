---
name: gemini-api
description: Delegate tasks to Google Gemini 3 series models via REST API. Use when tasks benefit from Gemini's multimodal capabilities - image generation (Nano Banana Pro), image editing (Nano Banana Pro), image understanding/vision (Gemini 3 Pro), or text tasks (Gemini 3 Pro). Always prioritize Pro models.
---

# Gemini API (REST)

Delegate tasks to Gemini 3 series models. Requires `GEMINI_API_KEY` environment variable.

## Models

| Model | Model ID | Best For |
|-------|----------|----------|
| **Gemini 3 Pro** | `gemini-3-pro-preview` | Text generation, vision/image understanding, OCR (DEFAULT for text output) |
| **Gemini 3 Flash** | `gemini-3-flash-preview` | Fast text/vision tasks (only when speed needed) |
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | Image generation, image editing (DEFAULT for image output) |
| **Nano Banana** | `gemini-2.5-flash-image` | Fast image generation (only when speed needed) |

**Defaults:**
- **Text output tasks** (text generation, vision, OCR): Use `gemini-3-pro-preview`
- **Image output tasks** (image generation, editing): Use `gemini-3-pro-image-preview`

## API Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}
```

## Request Structure

**For text models (with thinking):**
```json
{
  "contents": [{"parts": [{"text": "..."}]}],
  "generationConfig": {
    "thinkingConfig": {"thinkingLevel": "high"}
  }
}
```

**For image models (no thinking support):**
```json
{
  "contents": [{"parts": [{"text": "..."}]}],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

## Thinking Levels (Text models only)

| Level | Use Case |
|-------|----------|
| `low` | Simple tasks, minimal latency |
| `high` | Complex reasoning (default) |

**Note:** Image models (`gemini-3-pro-image-preview`, `gemini-2.5-flash-image`) do NOT support thinking levels.

---

## Examples

### 1. Text Generation (Gemini 3 Pro)

```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Explain quantum entanglement simply"}]}],
    "generationConfig": {"thinkingConfig": {"thinkingLevel": "high"}}
  }' | jq -r '.candidates[0].content.parts[0].text'
```

### 2. Image Understanding / Vision (Gemini 3 Pro)

Analyze an image - use Gemini 3 Pro for vision tasks (text output):

```bash
IMAGE_B64=$(base64 -i photo.jpg)

curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"inlineData": {"mimeType": "image/jpeg", "data": "'"${IMAGE_B64}"'"}},
        {"text": "Describe this image in detail. What objects, people, or text do you see?"}
      ]
    }],
    "generationConfig": {"thinkingConfig": {"thinkingLevel": "high"}}
  }' | jq -r '.candidates[0].content.parts[0].text'
```

### 3. Image Generation (Nano Banana Pro)

Generate images using Nano Banana Pro:

```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "A cozy coffee shop interior, warm lighting, watercolor style"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > coffee_shop.png
```

### 4. Image Editing (Nano Banana Pro)

Edit images using Nano Banana Pro:

```bash
IMAGE_B64=$(base64 -i input.jpg)

curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"inlineData": {"mimeType": "image/jpeg", "data": "'"${IMAGE_B64}"'"}},
        {"text": "Remove the background and make it transparent"}
      ]
    }],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > edited.png
```

### 5. Text in Images (Nano Banana Pro)

Nano Banana Pro excels at rendering text:

```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Create a professional business card for \"Jane Smith, CEO\" at \"TechCorp Inc\" with modern minimalist design"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > business_card.png
```

### 6. Fast Tasks (Flash models - only when speed needed)

```bash
# Fast text/vision (gemini-3-flash-preview)
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"contents": [{"parts": [{"text": "Quick summary"}]}]}' | jq -r '.candidates[0].content.parts[0].text'

# Fast image generation (gemini-2.5-flash-image)
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "A simple icon"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > icon.png
```

---

## When to Delegate to Gemini

| Task | Model |
|------|-------|
| Text generation | `gemini-3-pro-preview` (default) |
| Image understanding/vision | `gemini-3-pro-preview` (default) |
| OCR / text extraction | `gemini-3-pro-preview` (default) |
| Image generation | `gemini-3-pro-image-preview` (default) |
| Image editing | `gemini-3-pro-image-preview` (default) |
| Graphics with text/logos | `gemini-3-pro-image-preview` (default) |
| Fast text/vision (user requested) | `gemini-3-flash-preview` |
| Fast image tasks (user requested) | `gemini-2.5-flash-image` |

## Response Structure

**Text response:**
```json
{"candidates": [{"content": {"parts": [{"text": "..."}]}}]}
```

**Image response:**
```json
{"candidates": [{"content": {"parts": [
  {"text": "Here is your image..."},
  {"inlineData": {"mimeType": "image/png", "data": "<base64>"}}
]}}]}
```

## Python Script

Use `scripts/gemini_api.py` (prioritizes Pro models):

```bash
# Text generation (defaults to gemini-3-pro-preview)
python scripts/gemini_api.py text "Explain REST APIs"

# Image understanding (defaults to gemini-3-pro-preview)
python scripts/gemini_api.py vision photo.jpg "What's in this image?"

# Image generation (defaults to Nano Banana Pro)
python scripts/gemini_api.py generate "A sunset over mountains" -o sunset.png

# Image editing (defaults to Nano Banana Pro)
python scripts/gemini_api.py edit input.jpg "Add a rainbow" -o output.png

# Fast mode (only when user requests speed)
python scripts/gemini_api.py text "Quick question" --model flash
python scripts/gemini_api.py vision photo.jpg "Quick check" --model flash
python scripts/gemini_api.py generate "Simple icon" -o icon.png --model flash
```
