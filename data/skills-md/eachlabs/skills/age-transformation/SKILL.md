---
name: age-transformation
description: Transform faces across ages using each::sense AI. Create age progressions, de-aging effects, baby-to-adult predictions, and aging simulations for entertainment, forensics, and visual effects.
metadata:
  author: eachlabs
  version: "1.0"
---

# Age Transformation

Transform faces across different ages using each::sense. This skill enables realistic age progression (aging) and age regression (de-aging) effects on photos, useful for entertainment, film/video production, forensic visualization, and creative projects.

## Features

- **Age Progression**: Make subjects appear older (10, 20, 40+ years)
- **Age Regression**: De-age subjects to look younger
- **Baby to Adult**: Predict how a baby/child might look as an adult
- **Teenage Version**: Transform to teenage appearance
- **Senior/Elderly**: Create realistic elderly versions
- **Middle-Aged**: Transform to middle-age appearance
- **Subtle Aging**: Minor age changes (5-10 years)
- **Dramatic Aging**: Major age transformations (30-50 years)
- **De-aging for Film**: Professional de-aging for video/film production
- **Age Timeline**: Generate multiple ages in sequence

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Age this person to look 70 years old while maintaining their recognizable features",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

## Use Case Examples

### 1. Age Progression (Make Older)

Transform a young adult to appear significantly older with natural aging characteristics.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Age this person by 30 years. Add realistic aging features like wrinkles, slight sagging, gray hair, and age spots while keeping their identity clearly recognizable.",
    "image_urls": ["https://example.com/young-adult.jpg"],
    "mode": "max"
  }'
```

### 2. Age Regression (Make Younger)

De-age an older subject to appear younger with smoother skin and youthful features.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "De-age this person by 25 years. Make them look younger with smoother skin, fuller hair, tighter facial features, but keep their identity intact. Natural and realistic result.",
    "image_urls": ["https://example.com/middle-aged-person.jpg"],
    "mode": "max"
  }'
```

### 3. Baby to Adult Prediction

Predict how a baby or young child might look as an adult.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this baby photo to show how they might look as a 30-year-old adult. Maintain key facial features like eye shape, nose structure, and overall face shape. Make it realistic and believable.",
    "image_urls": ["https://example.com/baby-photo.jpg"],
    "mode": "max"
  }'
```

### 4. Teenage Version

Transform a child or adult to their teenage appearance.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this person to look like a 16-year-old teenager. Adjust facial features to teenage proportions while preserving their recognizable identity. Natural skin, youthful energy.",
    "image_urls": ["https://example.com/adult-portrait.jpg"],
    "mode": "max"
  }'
```

### 5. Senior/Elderly Version

Create a realistic elderly version with natural aging characteristics.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Age this person to 80 years old. Add deep wrinkles, age spots, white/gray hair, thinner skin, and natural elderly features. The result should look like a dignified senior while still being recognizable as the same person.",
    "image_urls": ["https://example.com/young-person.jpg"],
    "mode": "max"
  }'
```

### 6. Middle-Aged Version

Transform to a realistic middle-aged appearance.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this young adult to appear 45-50 years old. Add subtle wrinkles, slight gray at the temples, mature skin texture, and natural middle-age characteristics while maintaining their identity.",
    "image_urls": ["https://example.com/25-year-old.jpg"],
    "mode": "max"
  }'
```

### 7. Subtle Aging (10 Years)

Apply minor, realistic aging for a 10-year progression.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Age this person by exactly 10 years. Apply subtle, realistic aging: fine lines around eyes and mouth, slightly less elastic skin, minimal gray hair starting to show. Keep changes believable and natural.",
    "image_urls": ["https://example.com/current-photo.jpg"],
    "mode": "max"
  }'
```

### 8. Dramatic Aging (40 Years)

Apply significant aging transformation spanning 40 years.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Age this 25-year-old by 40 years to look 65. Apply dramatic but realistic aging: significant wrinkles, sagging skin, gray/white hair, age spots, thinning hair, jowls. Result should be photorealistic and the person should still be recognizable.",
    "image_urls": ["https://example.com/young-adult-25.jpg"],
    "mode": "max"
  }'
```

### 9. De-aging for Video/Film

Professional de-aging suitable for film and video production.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "De-age this actor to look 25 years younger for a film flashback scene. Remove wrinkles, tighten facial features, restore hair color and volume, create smooth youthful skin. Result must be cinematic quality, photorealistic, and maintain perfect identity consistency.",
    "image_urls": ["https://example.com/actor-current.jpg"],
    "mode": "max"
  }'
```

### 10. Age Progression Timeline (Multiple Ages)

Generate multiple age versions using session continuity.

```bash
# First request - Age to 40
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This is a 20-year-old. Create an age progression showing them at 40 years old. Maintain identity throughout.",
    "image_urls": ["https://example.com/person-age-20.jpg"],
    "session_id": "age-timeline-project-001",
    "mode": "max"
  }'

# Second request - Age to 60 (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now show the same person at 60 years old. Continue the aging progression naturally from the 40-year-old version.",
    "session_id": "age-timeline-project-001",
    "mode": "max"
  }'

# Third request - Age to 80 (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Finally, show them at 80 years old. Complete the age timeline with realistic elderly features.",
    "session_id": "age-timeline-project-001",
    "mode": "max"
  }'
```

## Best Practices

### For Realistic Results
- **High-quality source photos**: Use clear, well-lit frontal portraits
- **Specify exact age**: "Age to 65" is better than "make older"
- **Mention identity preservation**: Always request maintaining recognizable features
- **Describe aging features**: Guide the transformation with specific details

### Input Photo Guidelines
- **Resolution**: Higher resolution photos produce better results
- **Lighting**: Even, neutral lighting works best
- **Angle**: Front-facing portraits are ideal
- **Expression**: Neutral expressions transform most naturally
- **Obstruction**: Avoid sunglasses, heavy makeup, or face coverings

### Prompt Tips

When requesting age transformations, include:

1. **Current age** (if known): "This 30-year-old..."
2. **Target age**: "...to look 70 years old"
3. **Aging features**: "Add wrinkles, gray hair, age spots..."
4. **Identity note**: "...while keeping them recognizable"
5. **Quality requirement**: "Photorealistic result"

### Example Prompt Structure

```
"Transform this [current age]-year-old to look [target age] years old.
Add [specific aging/de-aging features].
Maintain their identity and recognizable features.
[Additional requirements like lighting, style, etc.]"
```

## Mode Selection

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final outputs, professional work, film/video | Slower | Highest |
| `eco` | Quick previews, testing, iterations | Faster | Good |

**Recommendation**: Use `eco` mode to test and refine your prompts, then switch to `max` for final high-quality outputs.

## Multi-Turn Refinement

Use `session_id` to iteratively refine age transformations:

```bash
# Initial transformation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Age this person to 70 years old",
    "image_urls": ["https://example.com/portrait.jpg"],
    "session_id": "age-refinement-001"
  }'

# Refine the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more prominent wrinkles and make the hair completely white",
    "session_id": "age-refinement-001"
  }'

# Further adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Keep the aging but make the expression warmer, add smile lines",
    "session_id": "age-refinement-001"
  }'
```

## Common Use Cases

| Use Case | Recommended Approach |
|----------|---------------------|
| Entertainment/Fun | Quick age-ups/de-aging with `eco` mode |
| Film/Video VFX | De-aging actors with `max` mode, detailed prompts |
| Missing Persons | Age progression from childhood, preserve key features |
| Family Projects | "What will I look like at 80?" type queries |
| Forensic Visualization | Professional age progression with identity focus |
| Before/After Concepts | Subtle aging for skincare/health visualizations |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Poor identity preservation | Vague prompt | Be specific about maintaining features |
| Unrealistic aging | Missing aging details | Describe specific aging characteristics |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `face-swap` - Face swapping capabilities
- `image-edit` - General image editing
- `portrait-generation` - Creating portraits from scratch
