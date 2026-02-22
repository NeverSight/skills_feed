---
name: face-morphing
description: Morph, blend, and transform faces using each::sense AI. Create face morphs, celebrity blends, family resemblance predictions, gender swaps, and animated transitions between faces.
metadata:
  author: eachlabs
  version: "1.0"
---

# Face Morphing

Transform and blend faces using each::sense. This skill enables face morphing, blending two or more faces together, predicting family resemblances, creating gender swaps, and generating smooth morph animations.

## Features

- **Face Blending**: Seamlessly merge two faces into one
- **Celebrity Morphs**: Blend your face with celebrities
- **Family Prediction**: Generate what a child might look like from parent photos
- **Couple Face Merge**: Create a blended face from two partners
- **Family Resemblance**: Analyze and visualize genetic similarities
- **Morph Animation**: Create smooth video transitions between faces
- **Gender Swap**: Transform facial features between genders
- **Ethnicity Blend**: Create faces that blend multiple ethnicities
- **Historical Modernization**: Update historical figure faces to modern style
- **Average Face**: Generate an average face from multiple inputs

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Morph these two faces together into a seamless blend, 50% each",
    "image_urls": [
      "https://example.com/face1.jpg",
      "https://example.com/face2.jpg"
    ],
    "mode": "max"
  }'
```

## Use Case Examples

### 1. Morph Two Faces Together

Basic face morphing that blends two faces into one unified result.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Morph these two faces together. Create a seamless blend that takes facial structure from the first image and some features like eyes and nose from the second image. Make it look natural and realistic.",
    "image_urls": [
      "https://example.com/person-a.jpg",
      "https://example.com/person-b.jpg"
    ],
    "mode": "max"
  }'
```

### 2. Celebrity Face Blend

Blend a user photo with a celebrity face for fun transformations.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Blend my face with this celebrity photo. Create a 50/50 morph that combines my facial structure with their features. Keep the result looking like a real person, not artificial.",
    "image_urls": [
      "https://example.com/my-photo.jpg",
      "https://example.com/celebrity.jpg"
    ],
    "mode": "max"
  }'
```

### 3. Parent + Child Prediction

Generate what a child might look like based on two parent photos.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Based on these two parent photos, generate what their child might look like. Create a baby/toddler face that naturally combines features from both parents - take eye shape from the first parent, nose structure from the second, and blend skin tones appropriately. Make it look like a realistic child portrait.",
    "image_urls": [
      "https://example.com/parent1.jpg",
      "https://example.com/parent2.jpg"
    ],
    "mode": "max"
  }'
```

### 4. Couple Face Merge

Create a merged face from a couple's photos.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Merge these two faces from a couple into one face. The result should look like a single person who has balanced features from both individuals. Keep natural proportions and make it look like a genuine portrait photo.",
    "image_urls": [
      "https://example.com/partner1.jpg",
      "https://example.com/partner2.jpg"
    ],
    "mode": "max"
  }'
```

### 5. Family Resemblance Generator

Visualize genetic similarities across family members.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Analyze these family member photos and create a face that represents the family resemblance - the common features shared across all family members. Highlight the genetic similarities in bone structure, eye shape, and facial proportions.",
    "image_urls": [
      "https://example.com/family-member1.jpg",
      "https://example.com/family-member2.jpg",
      "https://example.com/family-member3.jpg"
    ],
    "mode": "max"
  }'
```

### 6. Gradual Morph Animation

Create a smooth video transition morphing from one face to another.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a gradual morph animation video that smoothly transitions from the first face to the second face over 3 seconds. The transformation should be fluid and show intermediate blended states between both faces. Output as a video.",
    "image_urls": [
      "https://example.com/start-face.jpg",
      "https://example.com/end-face.jpg"
    ],
    "mode": "max"
  }'
```

### 7. Gender Swap

Transform facial features to appear as a different gender.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this face to show how the person might look as a different gender. Adjust facial features like jawline, brow ridge, cheekbones, and add appropriate hair and makeup while maintaining recognizable features from the original person.",
    "image_urls": [
      "https://example.com/original-face.jpg"
    ],
    "mode": "max"
  }'
```

### 8. Ethnicity Blend

Create a face that blends features from multiple ethnicities.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Blend these faces from different ethnic backgrounds into a single harmonious face. Create a natural-looking result that represents a mix of features from each source face - taking skin tone, eye shape, nose structure, and facial proportions from different inputs.",
    "image_urls": [
      "https://example.com/face-ethnicity1.jpg",
      "https://example.com/face-ethnicity2.jpg",
      "https://example.com/face-ethnicity3.jpg"
    ],
    "mode": "max"
  }'
```

### 9. Historical Figure Modernization

Transform a historical portrait to modern photographic style.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Take this historical portrait and modernize it. Transform the face to show how this historical figure would look in a modern photograph - update the lighting to contemporary photography style, adjust skin texture to look photorealistic, and give them a modern hairstyle while preserving their distinctive facial features.",
    "image_urls": [
      "https://example.com/historical-portrait.jpg"
    ],
    "mode": "max"
  }'
```

### 10. Create Average Face from Multiple Photos

Generate an average face that combines features from multiple input faces.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an average face from all these input photos. Blend the facial features mathematically to produce a single face that represents the statistical average of all inputs - averaged bone structure, feature placement, skin tone, and proportions.",
    "image_urls": [
      "https://example.com/face1.jpg",
      "https://example.com/face2.jpg",
      "https://example.com/face3.jpg",
      "https://example.com/face4.jpg",
      "https://example.com/face5.jpg"
    ],
    "mode": "max"
  }'
```

## Multi-Turn Creative Iteration

Use `session_id` to refine and iterate on face morphs:

```bash
# Initial morph
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Morph these two faces together with a 50/50 blend",
    "image_urls": [
      "https://example.com/face-a.jpg",
      "https://example.com/face-b.jpg"
    ],
    "session_id": "morph-project-001"
  }'

# Adjust the blend ratio
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Adjust the blend to be 70% first face and 30% second face",
    "session_id": "morph-project-001"
  }'

# Request specific feature adjustments
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Keep the eyes from the first face but use the jawline from the second face",
    "session_id": "morph-project-001"
  }'
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final morph outputs, detailed blends, animations | Slower | Highest |
| `eco` | Quick previews, testing different combinations | Faster | Good |

## Best Practices

### Input Image Quality
- **Resolution**: Use high-resolution face photos (at least 512x512)
- **Lighting**: Consistent lighting across input images produces better blends
- **Face Position**: Front-facing photos with similar angles work best
- **Background**: Clean backgrounds help isolate facial features

### Morph Quality Tips
- **Similar poses**: Input faces with similar head positions morph better
- **Clear features**: Avoid obscured faces (sunglasses, hands covering face)
- **Age consistency**: For family predictions, consider parent ages at time of photos
- **Multiple runs**: Try different prompts to find the best blend style

### Animation Considerations
- **Frame count**: More frames create smoother transitions
- **Duration**: 2-5 seconds is ideal for morph animations
- **Loop-friendly**: Request seamless loops for social media use

## Prompt Tips for Face Morphing

When creating face morphs, include these details in your prompt:

1. **Blend Ratio**: Specify the percentage blend (50/50, 70/30, etc.)
2. **Feature Focus**: Which features to take from which face
3. **Output Type**: Image or video animation
4. **Style**: Realistic, artistic, exaggerated, etc.
5. **Age Target**: For child predictions, specify desired age

### Example Prompt Structure

```
"[Action] these faces with [blend ratio].
Take [features] from the first face and [features] from the second.
Output as [image/video]. Make it look [style descriptor]."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| `No face detected` | Input image has no clear face | Use a clearer face photo |
| `Face alignment failed` | Faces too different in angle | Use photos with similar head positions |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `face-swap` - Swap faces between images
- `image-generation` - Generate faces from text descriptions
- `video-generation` - Create face animation videos
