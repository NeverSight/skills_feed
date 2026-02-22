---
name: pet-portrait-generation
description: Generate custom pet portraits using each::sense AI. Create realistic, artistic, and stylized pet portraits from photos - including cartoon, renaissance, watercolor, pop art, anime styles, and custom product mockups.
metadata:
  author: eachlabs
  version: "1.0"
---

# Pet Portrait Generation

Generate stunning custom pet portraits using each::sense. Transform your pet photos into beautiful artwork across various styles - from realistic portraits to whimsical cartoon illustrations, regal renaissance paintings, and personalized products.

## Features

- **Realistic Portraits**: Professional studio-quality pet photography
- **Cartoon/Illustrated**: Fun, colorful cartoon versions of pets
- **Renaissance/Royal**: Majestic portraits with historical costumes
- **Watercolor Paintings**: Artistic watercolor-style pet artwork
- **Pop Art**: Bold, vibrant pop art inspired portraits
- **Anime Style**: Japanese anime-style pet characters
- **Costume Portraits**: Pets in outfits, uniforms, and themed costumes
- **Multi-Pet Portraits**: Family portraits with multiple pets
- **Memorial Portraits**: Tribute artwork for beloved pets
- **Product Mockups**: Pet portraits on mugs, canvas, and merchandise

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a beautiful portrait of my golden retriever in a classic oil painting style",
    "image_urls": ["https://example.com/my-pet-photo.jpg"],
    "mode": "max"
  }'
```

## Use Case Examples

### 1. Realistic Pet Portrait

Create a professional studio-quality portrait that captures your pet's personality.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a realistic professional portrait of my cat. Studio lighting, soft bokeh background in warm earth tones. Capture the eyes beautifully with catchlights. High-end pet photography style.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "max"
  }'
```

### 2. Cartoon/Illustrated Pet Portrait

Transform your pet into a fun, colorful cartoon character.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform my dog into a cute cartoon illustration. Disney/Pixar style with big expressive eyes, playful pose. Vibrant colors, clean lines. Include a fun background with bones and toys.",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "mode": "max"
  }'
```

### 3. Renaissance/Royal Pet Portrait

Give your pet the royal treatment with a majestic historical portrait.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a renaissance-style royal portrait of my cat. Dress them as a noble king with a golden crown, velvet robe with ermine fur trim, and royal jewelry. Classical oil painting style, dramatic lighting, ornate gilded frame effect. Regal and majestic.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "max"
  }'
```

### 4. Watercolor Pet Painting

Create a beautiful watercolor artwork of your pet.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Paint my dog in a loose, expressive watercolor style. Soft edges, beautiful color bleeds and washes. Capture their personality with artistic brush strokes. Pastel background with splashes of color. Fine art watercolor painting look.",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "mode": "max"
  }'
```

### 5. Pop Art Pet Portrait

Create a bold, vibrant pop art portrait inspired by Andy Warhol.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a pop art portrait of my cat in Andy Warhol style. Bold, bright contrasting colors - hot pink, electric blue, yellow, orange. High contrast, graphic style with halftone dots. Create a 2x2 grid with different color variations.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "max"
  }'
```

### 6. Anime-Style Pet Portrait

Transform your pet into an adorable anime character.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime-style portrait of my dog. Japanese anime aesthetic with big sparkly eyes, soft shading, and cute kawaii expression. Include cherry blossoms in the background. Studio Ghibli inspired, warm and whimsical.",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "mode": "max"
  }'
```

### 7. Pet with Costume/Outfit

Dress up your pet in fun costumes and themed outfits.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a portrait of my cat as a space astronaut. Wearing a detailed NASA spacesuit with helmet, floating in space with Earth visible in the background. Stars and nebula. Realistic lighting, cinematic quality.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "max"
  }'
```

### 8. Multi-Pet Family Portrait

Create a beautiful portrait featuring multiple pets together.

```bash
# First request - provide all pet photos
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a family portrait with all three of my pets together. Classical portrait style with a warm, cozy living room background. Position them naturally as if they are posing together - the dog in the center, cats on either side. Soft, warm lighting, harmonious composition.",
    "image_urls": [
      "https://example.com/my-dog.jpg",
      "https://example.com/my-cat1.jpg",
      "https://example.com/my-cat2.jpg"
    ],
    "session_id": "pet-family-portrait",
    "mode": "max"
  }'

# Follow-up to adjust the portrait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Can you make the background a garden setting with flowers instead? Keep the same arrangement of the pets.",
    "session_id": "pet-family-portrait"
  }'
```

### 9. Memorial Pet Portrait

Create a touching tribute portrait for a beloved pet.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a memorial portrait for my beloved dog who passed away. Peaceful, serene setting with soft golden light. Include angel wings, subtle rainbow bridge elements in the background. Ethereal and comforting, celebrating their spirit. Beautiful tribute artwork.",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "mode": "max"
  }'
```

### 10. Pet Portrait on Products (Mug, Canvas)

Generate mockups of your pet portrait on merchandise and products.

```bash
# Pet portrait on a mug
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a product mockup of my cat portrait on a white ceramic coffee mug. The portrait should be a cute illustrated style. Show the mug on a wooden table with coffee, cozy morning setting. Professional product photography.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "session_id": "pet-products",
    "mode": "max"
  }'

# Same pet portrait on canvas
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a mockup of this same pet portrait as a canvas print hanging on a living room wall. Modern interior setting, natural lighting. Show it as wall art in context.",
    "session_id": "pet-products"
  }'
```

## Best Practices

### Photo Quality Tips
- **Clear photos**: Use well-lit, in-focus photos of your pet
- **Face visible**: Ensure the pet's face is clearly visible and not obscured
- **Multiple angles**: For best results, provide photos from different angles
- **Natural expressions**: Candid shots often produce the best portraits

### Prompt Tips
- **Be specific about style**: Mention specific art styles, artists, or references
- **Describe the mood**: Include emotional tone (playful, regal, peaceful)
- **Specify colors**: Request specific color palettes or schemes
- **Background details**: Describe the setting or background you want

### Example Prompt Structure

```
"Create a [style] portrait of my [pet type].
[Specific style details and references].
[Background/setting description].
[Mood and lighting].
[Any special elements or accessories]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & affordable, or maximum quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final portraits, gifts, prints | Slower | Highest |
| `eco` | Quick previews, style exploration | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to refine and iterate on portraits:

```bash
# Initial portrait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a renaissance portrait of my dog as a nobleman",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "session_id": "dog-portrait-project"
  }'

# Refine the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the costume more elaborate with gold embroidery and add a sword",
    "session_id": "dog-portrait-project"
  }'

# Try different variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different poses and backgrounds",
    "session_id": "dog-portrait-project"
  }'
```

## Style Exploration

Generate different styles to find the perfect look:

```bash
# Explore different styles with eco mode for speed
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create my cat portrait in oil painting style",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "eco"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create my cat portrait in minimalist line art style",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "eco"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create my cat portrait in stained glass window style",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Image not processing | Invalid or inaccessible image URL | Ensure image URL is publicly accessible |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Poor likeness | Low quality source photo | Use clear, well-lit photo with visible face |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - E-commerce product shots
- `image-generation` - General image generation
