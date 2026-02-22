---
name: Food Photography Generation
description: Generate professional food photography using each::sense API for restaurant menus, food delivery apps, recipe blogs, and social media content
metadata:
  category: image-generation
  api: sense
  endpoint: https://sense.eachlabs.run/chat
  modes: [max, eco]
  features:
    - Professional food styling
    - Multiple photography angles
    - Appetizing presentation
    - Steam and action effects
    - Consistent menu series
---

# Food Photography Generation

Generate stunning, appetizing food photography using the each::sense API. Create professional-quality images for restaurant menus, food delivery platforms, recipe blogs, and social media food content.

## Overview

The each::sense API enables AI-powered food photography generation with:

- **Restaurant Menus**: High-quality dish presentations for print and digital menus
- **Food Delivery Apps**: Appetizing thumbnails that drive orders
- **Recipe Blogs**: Hero images and step-by-step visuals
- **Social Media Content**: Instagram-worthy food shots that engage audiences

## Quick Start

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a professional food photo of a gourmet burger with melted cheese, fresh lettuce, and crispy bacon on a rustic wooden board, warm lighting, shallow depth of field",
    "mode": "max"
  }'
```

## Food Photography Styles

| Style | Description | Best For |
|-------|-------------|----------|
| Overhead Flat Lay | Top-down 90-degree angle | Pizza, salads, spreads, ingredient layouts |
| 45-Degree Angle | Classic three-quarter view | Plated dishes, bowls, layered foods |
| Hero Shot | Eye-level dramatic presentation | Signature dishes, menu covers |
| Action Shot | Capturing movement (pouring, cutting, steam) | Dynamic social media content |
| Ingredient Spread | Raw ingredients artfully arranged | Recipe blogs, cooking tutorials |

## Use Case Examples

### Restaurant Menu Item

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional restaurant menu photo of grilled salmon fillet with lemon butter sauce, asparagus, and roasted potatoes on a white ceramic plate, elegant fine dining presentation, soft natural lighting, clean background",
    "mode": "max"
  }'
```

### Food Delivery App Listing

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Appetizing food delivery app photo of a loaded pepperoni pizza with stretchy melted mozzarella cheese, fresh basil leaves, in a pizza box, overhead angle, bright even lighting, looks delicious and ready to order",
    "mode": "max"
  }'
```

### Recipe Blog Hero Image

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Beautiful recipe blog hero image of homemade chocolate chip cookies, stack of warm cookies with melted chocolate chips visible, cookie crumbs scattered on marble surface, rustic kitchen background, cozy warm tones, food photography style",
    "mode": "max"
  }'
```

### Coffee and Beverage Shot

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional coffee shop photo of a latte with intricate leaf latte art in a ceramic cup on a wooden saucer, steam rising gently, coffee beans scattered nearby, morning light from window, cafe atmosphere",
    "mode": "max"
  }'
```

### Dessert Photography

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Elegant dessert photography of a layered tiramisu in a glass, visible coffee-soaked ladyfinger layers and mascarpone cream, dusted with cocoa powder, silver spoon beside it, dark moody background, dramatic lighting",
    "mode": "max"
  }'
```

### Action Shot with Movement

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Dynamic food action shot of maple syrup being poured over a stack of fluffy pancakes with fresh blueberries, syrup caught mid-pour creating a golden stream, steam rising, breakfast table setting, warm morning light",
    "mode": "max"
  }'
```

### Ingredient Flat Lay

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Overhead flat lay food photography of Italian pasta recipe ingredients: fresh tomatoes, basil leaves, garlic cloves, olive oil in a glass bottle, parmesan wedge, dried pasta, arranged artfully on a dark slate surface, natural lighting",
    "mode": "max"
  }'
```

### Table Setting and Spread

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Beautiful brunch table spread photography featuring avocado toast, fresh fruit bowl, croissants, orange juice glasses, and a French press coffee, rustic wooden table with linen napkins, overhead angle, bright natural daylight, lifestyle food photography",
    "mode": "max"
  }'
```

### Fast Food Product Shot

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Commercial fast food photography of crispy fried chicken bucket meal with golden brown pieces, seasoned fries in a red container, coleslaw cup, on a branded tray, clean studio lighting, appetizing and crave-worthy presentation",
    "mode": "max"
  }'
```

### Healthy Meal Prep

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Clean healthy meal prep photography showing glass containers with grilled chicken breast, quinoa, roasted vegetables including broccoli and sweet potato, colorful and nutritious, organized kitchen counter, bright lighting, fitness lifestyle aesthetic",
    "mode": "max"
  }'
```

## Best Practices for Food Photography

### Make Food Look Appetizing

- **Steam and Heat**: Include visible steam for hot dishes to convey freshness
- **Moisture and Shine**: Add gleaming sauces, melted cheese, or oil glazes for appeal
- **Color Contrast**: Combine colorful ingredients for visual interest
- **Texture Details**: Highlight crispy, creamy, or crunchy textures

### Styling and Props

- **Garnishes**: Fresh herbs, citrus zests, or edible flowers add finishing touches
- **Backgrounds**: Use complementary surfaces like wood, marble, or slate
- **Utensils**: Include silverware, napkins, or serving boards for context
- **Negative Space**: Leave room for text overlay if used in marketing

### Lighting Guidelines

- **Natural Light**: Soft daylight creates warm, inviting images
- **Side Lighting**: Emphasizes texture and creates depth
- **Avoid Harsh Shadows**: Use diffused lighting for even exposure
- **Warm Tones**: Enhances appetizing appearance of food

## Prompt Tips

Effective food photography prompts should include:

1. **Food Description**: Specific dish name and key ingredients
2. **Presentation Style**: Plating, garnishes, and arrangement
3. **Camera Angle**: Overhead, 45-degree, eye-level, or close-up
4. **Lighting**: Natural, studio, warm, dramatic, or soft
5. **Props and Surface**: Plates, utensils, background materials
6. **Mood**: Cozy, elegant, rustic, modern, or commercial

Example structure:
```
"[Photography style] of [dish name] with [key ingredients/toppings],
[presentation details], [surface/background], [lighting description],
[mood/aesthetic]"
```

## Mode Selection

| Mode | Description | Best For |
|------|-------------|----------|
| `max` | Highest quality, detailed rendering | Menu covers, hero images, print materials |
| `eco` | Faster generation, good quality | Social media posts, quick iterations, testing |

## Multi-Turn Sessions for Menu Consistency

Use `session_id` to maintain consistent styling across a menu series:

```bash
# First dish in menu series
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional restaurant menu photo of beef tenderloin steak with red wine reduction, roasted garlic mashed potatoes, and grilled asparagus on a white plate, elegant fine dining style, soft lighting, dark wood table background",
    "session_id": "menu-series-001",
    "mode": "max"
  }'

# Second dish maintaining consistent style
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching menu photo of pan-seared duck breast with cherry glaze, wild rice pilaf, and sauteed spinach, same elegant fine dining style and plating",
    "session_id": "menu-series-001",
    "mode": "max"
  }'

# Third dish in the series
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Continue with a dessert photo in the same style: chocolate lava cake with vanilla ice cream and raspberry coulis, elegant presentation matching the previous dishes",
    "session_id": "menu-series-001",
    "mode": "max"
  }'
```

## Error Handling

| Error Code | Description | Solution |
|------------|-------------|----------|
| 401 | Invalid API key | Verify your `EACHLABS_API_KEY` is correct |
| 400 | Invalid request | Check JSON format and required parameters |
| 429 | Rate limit exceeded | Implement exponential backoff |
| 500 | Server error | Retry with exponential backoff |

Example with error handling:

```bash
response=$(curl -s -w "\n%{http_code}" -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional food photo of a sushi platter with various nigiri and maki rolls, fresh wasabi and pickled ginger, elegant Japanese presentation on a black lacquer tray",
    "mode": "max"
  }')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 200 ]; then
  echo "Success: $body"
else
  echo "Error $http_code: $body"
fi
```

## Related Skills

- [Image Generation](/skills/eachlabs-image-generation) - General image generation capabilities
- [Product Visuals](/skills/eachlabs-product-visuals) - Product photography and visualization
- [Image Edit](/skills/eachlabs-image-edit) - Edit and enhance existing food photos
