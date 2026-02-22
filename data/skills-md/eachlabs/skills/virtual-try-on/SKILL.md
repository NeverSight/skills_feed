---
name: Virtual Try-On
description: AI-powered virtual try-on for clothing, accessories, makeup, hairstyles, and more using each::sense API
metadata:
  category: fashion
  api: each::sense
  endpoint: https://sense.eachlabs.run/chat
  features:
    - clothing-try-on
    - accessories
    - makeup
    - hairstyles
    - glasses
    - jewelry
    - watches
    - shoes
---

# Virtual Try-On

AI-powered virtual try-on solution that allows users to visualize how clothing, accessories, makeup, and hairstyles look on them without physically trying items on.

## Overview

The Virtual Try-On skill leverages each::sense API to provide realistic visualization of:

- **Clothing Try-On**: Shirts, dresses, jackets, pants, and full outfits
- **Accessories**: Glasses, sunglasses, jewelry, watches, scarves, hats
- **Makeup**: Lipstick, eyeshadow, foundation, blush, complete makeup looks
- **Hairstyles**: Different haircuts, colors, and styling options
- **Shoes**: Sneakers, heels, boots, sandals
- **Jewelry**: Necklaces, earrings, bracelets, rings

## Quick Start

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Show me wearing this dress",
    "image_urls": [
      "https://example.com/person-photo.jpg",
      "https://example.com/dress-product.jpg"
    ],
    "mode": "max"
  }'
```

## Try-On Categories

| Category | Description | Example Items |
|----------|-------------|---------------|
| Clothing | Apparel and garments | Shirts, dresses, jackets, pants, coats |
| Shoes | Footwear | Sneakers, heels, boots, sandals, loafers |
| Glasses | Eyewear | Prescription glasses, sunglasses, reading glasses |
| Jewelry | Decorative accessories | Necklaces, earrings, bracelets, rings |
| Makeup | Cosmetic products | Lipstick, eyeshadow, foundation, blush |
| Hairstyles | Hair modifications | Haircuts, hair colors, styling |
| Watches | Wristwear | Analog watches, smartwatches, luxury watches |

## Use Case Examples

### 1. Clothing Try-On

Visualize how a specific clothing item looks on a person.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Show me wearing this blue blazer. Keep my face and body proportions accurate.",
    "image_urls": [
      "https://example.com/my-photo.jpg",
      "https://example.com/blue-blazer.jpg"
    ],
    "mode": "max"
  }'
```

### 2. Glasses/Eyewear Try-On

Try on different eyewear styles virtually.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Put these round tortoiseshell glasses on me. Make sure the fit looks natural on my face shape.",
    "image_urls": [
      "https://example.com/face-photo.jpg",
      "https://example.com/tortoiseshell-glasses.jpg"
    ],
    "mode": "max"
  }'
```

### 3. Jewelry Try-On

Visualize jewelry items like necklaces, earrings, or bracelets.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Show me wearing this gold necklace. Position it naturally on my neckline.",
    "image_urls": [
      "https://example.com/portrait-photo.jpg",
      "https://example.com/gold-necklace.jpg"
    ],
    "mode": "max"
  }'
```

### 4. Watch Try-On

Try on watches to see how they fit your wrist.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Put this luxury watch on my wrist. Show how it looks from a natural angle.",
    "image_urls": [
      "https://example.com/wrist-photo.jpg",
      "https://example.com/luxury-watch.jpg"
    ],
    "mode": "max"
  }'
```

### 5. Makeup Try-On

Apply virtual makeup looks or specific cosmetic products.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply this red lipstick shade to my lips. Keep the rest of my makeup natural.",
    "image_urls": [
      "https://example.com/face-closeup.jpg",
      "https://example.com/red-lipstick-product.jpg"
    ],
    "mode": "max"
  }'
```

### 6. Hairstyle Try-On

Experiment with different hairstyles and hair colors.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Give me this bob haircut style. Match the hair color to the reference image.",
    "image_urls": [
      "https://example.com/my-current-photo.jpg",
      "https://example.com/bob-hairstyle-reference.jpg"
    ],
    "mode": "max"
  }'
```

### 7. Shoes Try-On

Visualize how different footwear looks.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Show me wearing these white sneakers. Display a full body view.",
    "image_urls": [
      "https://example.com/full-body-photo.jpg",
      "https://example.com/white-sneakers.jpg"
    ],
    "mode": "max"
  }'
```

### 8. Full Outfit Styling

Create a complete look with multiple clothing items.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Style me in this complete outfit - the jacket, pants, and shoes together. Create a cohesive look.",
    "image_urls": [
      "https://example.com/my-photo.jpg",
      "https://example.com/leather-jacket.jpg",
      "https://example.com/black-jeans.jpg",
      "https://example.com/boots.jpg"
    ],
    "mode": "max"
  }'
```

### 9. Accessory Combination

Combine multiple accessories for a complete look.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Put these sunglasses and this scarf on me together. Make the accessories complement each other.",
    "image_urls": [
      "https://example.com/portrait.jpg",
      "https://example.com/aviator-sunglasses.jpg",
      "https://example.com/silk-scarf.jpg"
    ],
    "mode": "max"
  }'
```

### 10. Event-Ready Styling

Create looks for specific occasions.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Dress me for a formal wedding. Use this evening gown and add elegant jewelry to complete the look.",
    "image_urls": [
      "https://example.com/my-photo.jpg",
      "https://example.com/evening-gown.jpg",
      "https://example.com/pearl-earrings.jpg"
    ],
    "mode": "max"
  }'
```

## Using image_urls

The `image_urls` parameter accepts an array of image URLs for virtual try-on:

| Position | Purpose | Requirements |
|----------|---------|--------------|
| First image | Person photo | Clear, well-lit photo of the person |
| Second image | Product/item photo | Clear product image on neutral background |
| Additional images | Multiple products | For combining multiple items in one try-on |

### Image Guidelines

- **Person Photo**: Front-facing, good lighting, relevant body parts visible
- **Product Photo**: High resolution, clear product details, minimal background clutter
- **Supported Formats**: JPEG, PNG, WebP
- **Recommended Resolution**: 1024x1024 or higher for best results

## Best Practices

### Photo Quality

1. **Person Photo Requirements**:
   - Use well-lit, high-resolution images
   - Ensure the relevant body part is clearly visible (face for glasses, full body for clothing)
   - Avoid heavy filters or extreme angles
   - Front-facing photos work best for most try-ons

2. **Product Photo Requirements**:
   - Use official product images when available
   - Ensure the item is clearly visible and not obscured
   - White or neutral backgrounds work best
   - Multiple angles can improve accuracy

### Prompt Tips

- **Be Specific**: Describe exactly how you want the item positioned
- **Mention Fit**: Ask for natural fit and proportions
- **Reference Colors**: Specify if color matching is important
- **Include Context**: Mention the occasion or style goal

**Good Prompts**:
- "Show me wearing this navy blazer with natural shoulder fit"
- "Apply this eyeshadow palette for an evening look"
- "Put these glasses on me, adjusting for my face shape"

**Less Effective Prompts**:
- "Try this on" (too vague)
- "Put clothes" (no specific item reference)

## Mode Selection

| Mode | Description | Best For |
|------|-------------|----------|
| `max` | Highest quality, detailed rendering | Final visualizations, important decisions |
| `eco` | Faster processing, good quality | Quick previews, browsing multiple options |

```bash
# High quality for final decision
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Show me in this wedding dress with maximum detail",
    "image_urls": ["https://example.com/me.jpg", "https://example.com/dress.jpg"],
    "mode": "max"
  }'

# Quick preview mode
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Quick preview of this t-shirt on me",
    "image_urls": ["https://example.com/me.jpg", "https://example.com/tshirt.jpg"],
    "mode": "eco"
  }'
```

## Multi-Turn Sessions

Use `session_id` to try multiple items in a continuous session, maintaining context from previous interactions.

### Starting a Session

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This is my photo. I want to try on several outfits for a job interview.",
    "image_urls": ["https://example.com/my-photo.jpg"],
    "session_id": "tryon-session-12345",
    "mode": "max"
  }'
```

### Continuing the Session

```bash
# Try first outfit
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now show me in this navy suit",
    "image_urls": ["https://example.com/navy-suit.jpg"],
    "session_id": "tryon-session-12345",
    "mode": "max"
  }'

# Try second outfit
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "How about this charcoal blazer with khakis instead?",
    "image_urls": ["https://example.com/charcoal-blazer.jpg", "https://example.com/khakis.jpg"],
    "session_id": "tryon-session-12345",
    "mode": "max"
  }'

# Compare options
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Which outfit looked more professional on me?",
    "session_id": "tryon-session-12345",
    "mode": "max"
  }'
```

## Error Handling

### Common Issues and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Low quality result | Poor input image quality | Use higher resolution, well-lit photos |
| Incorrect placement | Unclear body positioning | Use front-facing photos with visible target area |
| Color mismatch | Product image has color cast | Use product images with accurate color representation |
| Item not visible | Product obscured in image | Use clear product images on neutral backgrounds |

### Handling API Errors

```bash
# Check response status and handle errors
response=$(curl -s -w "\n%{http_code}" -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Show me in this jacket",
    "image_urls": ["https://example.com/me.jpg", "https://example.com/jacket.jpg"],
    "mode": "max"
  }')

http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" -eq 200 ]; then
  echo "Success: $body"
elif [ "$http_code" -eq 401 ]; then
  echo "Error: Invalid API key"
elif [ "$http_code" -eq 400 ]; then
  echo "Error: Invalid request - check image URLs and parameters"
else
  echo "Error $http_code: $body"
fi
```

## Related Skills

- [Fashion AI](/skills/eachlabs-fashion-ai) - AI-powered fashion recommendations and styling
- [Image Edit](/skills/eachlabs-image-edit) - General image editing and manipulation
- [Image Generation](/skills/eachlabs-image-generation) - Generate fashion and product images
- [Product Visuals](/skills/eachlabs-product-visuals) - Create professional product photography
