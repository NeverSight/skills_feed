---
name: digital-twin-generation
description: Generate photorealistic digital twins and avatar clones using each::sense AI. Create AI-powered digital representations for video calls, corporate communications, customer service, and multilingual content.
metadata:
  author: eachlabs
  version: "1.0"
---

# Digital Twin Generation

Generate photorealistic digital twins and avatar clones using each::sense. This skill creates AI-powered digital representations of real people for video calls, corporate communications, customer service, and multilingual content delivery.

## Features

- **Photo-Based Digital Twins**: Create digital clones from reference photos
- **Photorealistic Avatars**: Generate lifelike avatar representations
- **Video Call Twins**: Digital twins optimized for virtual meetings
- **Corporate Spokespersons**: Professional digital representatives for brand communication
- **Customer Service Avatars**: Consistent AI representatives for support interactions
- **Multilingual Twins**: Digital twins that can speak multiple languages
- **Expressive Twins**: Avatars with natural facial expressions and emotions
- **Full-Body Twins**: Complete digital representations including body and gestures
- **Animated Videos**: Bring digital twins to life with video generation
- **Cross-Platform Consistency**: Maintain identical appearance across all platforms

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photorealistic digital twin from these reference photos. Generate a professional headshot suitable for corporate use.",
    "image_urls": ["https://example.com/person-photo1.jpg", "https://example.com/person-photo2.jpg"],
    "mode": "max"
  }'
```

## Digital Twin Use Cases

| Use Case | Description | Recommended Photos |
|----------|-------------|-------------------|
| Video Calls | Virtual meeting representation | 3-5 front-facing photos |
| Corporate Spokesperson | Brand communications | 5-10 professional photos |
| Customer Service | Support avatar | 3-5 neutral expression photos |
| Multilingual Content | Translated video content | 5+ varied angle photos |
| Social Media | Consistent online presence | 5-10 diverse photos |
| Training Videos | Educational content delivery | 5+ photos with expressions |

## Use Case Examples

### 1. Create Digital Twin from Photos

Generate a digital twin based on reference photographs for consistent identity representation.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin from these reference photos. The twin should capture the exact likeness, skin tone, and facial features. Generate a high-quality portrait with professional studio lighting on a neutral gray background.",
    "image_urls": [
      "https://example.com/reference-front.jpg",
      "https://example.com/reference-angle.jpg",
      "https://example.com/reference-side.jpg"
    ],
    "mode": "max"
  }'
```

### 2. Photorealistic Avatar Clone

Create a highly detailed photorealistic avatar for digital presence across platforms.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a photorealistic avatar clone from these photos. The avatar should be indistinguishable from a real photograph. Include fine details like skin texture, hair strands, and eye reflections. Output as a 1:1 square format suitable for profile pictures.",
    "image_urls": [
      "https://example.com/subject-photo1.jpg",
      "https://example.com/subject-photo2.jpg"
    ],
    "mode": "max"
  }'
```

### 3. Digital Twin for Video Calls

Create an optimized digital twin for virtual meeting environments.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin optimized for video calls. The twin should look natural in a home office setting with soft natural lighting. Include a subtle depth-of-field blur on the background. The person should have a friendly, approachable expression suitable for professional meetings.",
    "image_urls": [
      "https://example.com/ceo-headshot.jpg",
      "https://example.com/ceo-casual.jpg"
    ],
    "mode": "max",
    "session_id": "videocall-twin-001"
  }'
```

### 4. Corporate Spokesperson Twin

Generate a professional digital spokesperson for brand communications.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate spokesperson digital twin from these executive photos. The twin should appear authoritative yet approachable. Professional business attire, confident posture, clean corporate background with subtle brand colors (navy blue). Suitable for investor presentations and company announcements.",
    "image_urls": [
      "https://example.com/exec-professional.jpg",
      "https://example.com/exec-speaking.jpg",
      "https://example.com/exec-portrait.jpg"
    ],
    "mode": "max"
  }'
```

### 5. Customer Service Avatar

Create a consistent, friendly avatar for customer support interactions.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a customer service avatar digital twin. The avatar should have a warm, helpful expression with a genuine smile. Professional but approachable appearance. Clean, minimal background. The twin will be used for chat support and help desk interfaces, so it should feel trustworthy and friendly.",
    "image_urls": [
      "https://example.com/support-rep-photo.jpg"
    ],
    "mode": "max"
  }'
```

### 6. Multilingual Digital Twin

Create a digital twin designed for multilingual content delivery.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin for multilingual video content. Generate the twin with a neutral mouth position that works well for lip-sync dubbing. Include multiple angles: front-facing, slight left turn, and slight right turn. The lighting should be even and consistent to ensure seamless video dubbing across different languages.",
    "image_urls": [
      "https://example.com/presenter-front.jpg",
      "https://example.com/presenter-left.jpg",
      "https://example.com/presenter-right.jpg"
    ],
    "mode": "max",
    "session_id": "multilingual-twin-project"
  }'
```

### 7. Digital Twin with Expressions

Generate a digital twin with various facial expressions for dynamic content.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin with multiple expressions from these reference photos. Generate 4 variations: 1) Neutral professional expression, 2) Warm genuine smile, 3) Thoughtful/listening expression, 4) Enthusiastic/excited expression. All variations should maintain perfect identity consistency.",
    "image_urls": [
      "https://example.com/person-neutral.jpg",
      "https://example.com/person-smiling.jpg",
      "https://example.com/person-serious.jpg"
    ],
    "mode": "max",
    "session_id": "expressive-twin-set"
  }'
```

### 8. Full-Body Digital Twin

Create a complete full-body digital representation including posture and gestures.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a full-body digital twin from these reference photos. Include accurate body proportions, clothing style, and natural standing posture. The twin should be shown in a professional presentation pose with hands visible. Full-length view suitable for virtual events and digital stage presentations.",
    "image_urls": [
      "https://example.com/fullbody-front.jpg",
      "https://example.com/fullbody-side.jpg",
      "https://example.com/headshot-detail.jpg"
    ],
    "mode": "max"
  }'
```

### 9. Animated Digital Twin Video

Generate an animated video featuring the digital twin speaking or presenting.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-second animated video of my digital twin. The twin should appear to be speaking naturally with subtle head movements and natural blinking. Professional office background with soft lighting. The animation should loop seamlessly for use as a video call placeholder.",
    "image_urls": [
      "https://example.com/my-photo-front.jpg",
      "https://example.com/my-photo-speaking.jpg"
    ],
    "mode": "max"
  }'
```

### 10. Consistent Twin Across Platforms

Create multiple format variations of a digital twin for cross-platform consistency.

```bash
# Initial twin creation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin master image from these photos. This will be the base for generating consistent avatars across multiple platforms. High resolution, neutral background, perfect lighting for easy adaptation.",
    "image_urls": [
      "https://example.com/master-photo1.jpg",
      "https://example.com/master-photo2.jpg",
      "https://example.com/master-photo3.jpg"
    ],
    "mode": "max",
    "session_id": "cross-platform-twin"
  }'

# LinkedIn format (1:1 square)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Using the digital twin we just created, generate a 1:1 square format version optimized for LinkedIn. Professional appearance with a subtle corporate background.",
    "session_id": "cross-platform-twin"
  }'

# Twitter/X format (circular crop friendly)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a circular-crop-friendly version of the twin for Twitter/X profile. Center the face with enough margin for circular cropping. Slightly more casual than LinkedIn.",
    "session_id": "cross-platform-twin"
  }'

# Video thumbnail format (16:9)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 16:9 landscape version of the twin suitable for YouTube thumbnails and video call backgrounds. Position the twin on the right third with space for text on the left.",
    "session_id": "cross-platform-twin"
  }'
```

## Best Practices

### Reference Photo Guidelines

- **Quantity**: Provide 3-10 reference photos for best results
- **Angles**: Include front, 3/4, and profile views when possible
- **Lighting**: Use well-lit photos without harsh shadows
- **Resolution**: Higher resolution photos produce better twins
- **Consistency**: Photos should show the same person at similar age
- **Expressions**: Include variety for expressive twin generation

### Quality Optimization

- **Mode Selection**: Use `max` for final assets, `eco` for rapid prototyping
- **Iterative Refinement**: Use `session_id` to refine twins across multiple requests
- **Specific Details**: Describe exact requirements for lighting, background, expression
- **Format Specification**: Always specify aspect ratio and intended use

### Identity Consistency

- **Session Continuity**: Use same `session_id` for all variations of one twin
- **Reference Anchoring**: Include original photos when requesting variations
- **Style Lock**: Describe consistent elements (lighting, background) across requests

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final digital twins, production assets | Slower | Highest |
| `eco` | Quick previews, concept exploration | Faster | Good |

## Multi-Turn Twin Development

Use `session_id` to iteratively develop and refine digital twins:

```bash
# Initial twin generation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin from these photos for corporate communications",
    "image_urls": ["https://example.com/ceo-photo1.jpg", "https://example.com/ceo-photo2.jpg"],
    "mode": "max",
    "session_id": "ceo-digital-twin"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the expression slightly more serious and add subtle rim lighting for more dimension",
    "session_id": "ceo-digital-twin"
  }'

# Generate variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 3 variations with different backgrounds: 1) Modern office, 2) Gradient blue, 3) Pure white",
    "session_id": "ceo-digital-twin"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Ensure photos have proper consent |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Low quality output | Poor reference photos | Provide higher quality, well-lit photos |

## Privacy & Consent

When creating digital twins, ensure:

- You have explicit consent from the person being cloned
- Digital twins are used only for authorized purposes
- Generated content complies with applicable laws and regulations
- Deepfake/synthetic media is clearly disclosed when required

## Related Skills

- `each-sense` - Core API documentation
- `face-swap` - Face replacement in existing images
- `video-generation` - Create videos from images
- `image-generation` - General image generation
