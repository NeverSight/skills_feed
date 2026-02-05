---
name: vap-media
description: AI image, video, and music generation. Flux, Veo 3.1, Suno V5.
homepage: https://vapagent.com
---

# VAP Media - AI Media Generation

Generate images, videos, and music via the VAP API.

## Mode Selection

Check if VAP_API_KEY is set:
- VAP_API_KEY not set → Use Free Mode (images only, 3/day)
- VAP_API_KEY set → Use Full Mode (image, video, music, unlimited)

---

## Free Mode (No API Key)

Generate images for free. No signup required. 3 per day.

### Generate Image

```bash
curl -s -X POST https://api.vapagent.com/v3/trial/generate \
  -H "Content-Type: application/json" \
  -d '{"description":"a serene mountain lake at sunset"}'
```

Returns `{"task_id":"UUID","status":"pending","remaining":2}`.

### Poll Result

```bash
curl -s https://api.vapagent.com/v3/trial/status/TASK_ID
```

Returns `{"status":"completed","image_url":"https://..."}` when done.

### Free Mode Errors

- 429 → Daily limit reached. Suggest upgrading: `export VAP_API_KEY=vape_xxx`
- 503 → Trial service temporarily unavailable.

---

## Full Mode (With API Key)

Unlimited images, video, and music generation.

### Create Task

```bash
curl -s -X POST https://api.vapagent.com/v3/tasks \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "description": "a futuristic cityscape at night",
    "aspect_ratio": "16:9"
  }'
```

Returns `{"task_id":"UUID","status":"pending","estimated_cost":"0.1800"}`.

### Poll Result

```bash
curl -s https://api.vapagent.com/v3/tasks/TASK_ID \
  -H "Authorization: Bearer $VAP_API_KEY"
```

Returns `{"status":"completed","result":{"output_url":"https://..."}}` when done.

### Task Types

| Type   | Model   | Params                                        |
|--------|---------|-----------------------------------------------|
| image  | Flux    | description, aspect_ratio (1:1, 16:9, 9:16)   |
| video  | Veo 3.1 | description, duration (4/6/8), aspect_ratio, generate_audio (bool) |
| music  | Suno V5 | description, duration (30-480), instrumental (bool) |

### Full Mode Errors

- 401 → Invalid API key.
- 402 → Insufficient balance. Top up at https://vapagent.com/dashboard/signup.html

---

## Instructions

When a user asks to create/generate/make an image, video, or music:

1. Improve the prompt - Add style, lighting, composition, mood details
2. Check mode - Is VAP_API_KEY set?
3. Call the appropriate endpoint - Free or Full mode
4. Poll for result - Check task status until completed
5. Return the media URL to the user

If free mode limit is hit, tell the user: "You've used your 3 free generations today. For unlimited access, get an API key at https://vapagent.com/dashboard/signup.html"

---

## Free Mode Example

```bash
# Create (no auth needed)
curl -s -X POST https://api.vapagent.com/v3/trial/generate \
  -H "Content-Type: application/json" \
  -d '{"description":"a golden retriever puppy playing in a field"}'
# → {"task_id":"abc123","status":"pending","remaining":2}

# Poll every 2-3 seconds
curl -s https://api.vapagent.com/v3/trial/status/abc123
# → {"status":"completed","image_url":"https://cdn.vapagent.com/abc123.png"}
```

## Full Mode Examples

```bash
# Image
curl -s -X POST https://api.vapagent.com/v3/tasks \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"image","description":"cyberpunk street at night, neon lights","aspect_ratio":"16:9"}'

# Video
curl -s -X POST https://api.vapagent.com/v3/tasks \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"video","description":"ocean waves crashing on beach","duration":6,"generate_audio":true}'

# Music
curl -s -X POST https://api.vapagent.com/v3/tasks \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"music","description":"upbeat electronic dance music","duration":120,"instrumental":false}'
```

---

## Prompt Tips

- Style: "oil painting", "3D render", "watercolor", "photograph", "flat illustration"
- Lighting: "golden hour", "neon lights", "soft diffused light", "dramatic shadows"
- Composition: "close-up", "aerial view", "wide angle", "rule of thirds"
- Mood: "serene", "energetic", "mysterious", "whimsical"

---

## Setup (Optional - for Full Mode)

1. Sign up: https://vapagent.com/dashboard/signup.html
2. Get API key from dashboard
3. Set: `export VAP_API_KEY=vape_xxxxxxxxxxxxxxxxxxxx`

---

## Links

- [Try Free](https://vapagent.com/try)
- [API Docs](https://api.vapagent.com/docs)
- [GitHub](https://github.com/vapagentmedia/vap-showcase)
