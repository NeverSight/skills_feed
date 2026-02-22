---
name: logo-generation
description: Generate professional logos using each::sense AI. Create wordmarks, icon logos, combination marks, monograms, mascots, emblems, and abstract logos for brands, startups, and businesses.
metadata:
  author: eachlabs
  version: "1.0"
---

# Logo Generation

Generate professional, creative logos using each::sense. This skill creates various logo styles including wordmarks, icon logos, combination marks, monograms, mascots, emblems, and abstract designs for brands of all sizes.

## Features

- **Wordmark Logos**: Text-based logos with custom typography
- **Icon/Symbol Logos**: Standalone graphic marks
- **Combination Logos**: Icon + text integrated designs
- **Monogram Logos**: Initials-based logos (letter marks)
- **Mascot Logos**: Character-based brand identities
- **Abstract Logos**: Geometric and conceptual marks
- **Emblem/Badge Logos**: Enclosed crests and seals
- **Minimalist Logos**: Clean, simple, modern designs
- **Logo Variations**: Color, black & white, icon-only versions
- **Transparent Backgrounds**: Export-ready logos for any use

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern minimalist logo for a tech startup called Nexus. Clean lines, professional look.",
    "mode": "max"
  }'
```

## Logo Styles & Use Cases

| Style | Best For | Characteristics |
|-------|----------|-----------------|
| Wordmark | Unique brand names, startups | Typography-focused, readable |
| Icon/Symbol | App icons, favicons, social media | Scalable, memorable |
| Combination | Full branding, websites | Versatile, complete identity |
| Monogram | Luxury brands, law firms | Elegant, compact |
| Mascot | Sports teams, food brands, gaming | Friendly, memorable |
| Abstract | Tech companies, innovation | Modern, unique |
| Emblem | Universities, government, heritage brands | Traditional, authoritative |
| Minimalist | Modern brands, apps | Clean, versatile |

## Use Case Examples

### 1. Text-Based Logo (Wordmark)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a wordmark logo for a coffee brand called BREW HAVEN. Use elegant serif typography with a warm, artisanal feel. Rich brown and cream colors. The text should be the main focus with subtle coffee-inspired styling.",
    "mode": "max"
  }'
```

### 2. Icon/Symbol Logo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an icon logo for a fitness app. Design a bold, dynamic symbol that represents strength and movement. Use a single striking icon without any text. Electric blue and white colors. Must work well as an app icon at small sizes.",
    "mode": "max"
  }'
```

### 3. Combination Logo (Icon + Text)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a combination logo for an eco-friendly cleaning company called GreenClean. Include a leaf icon integrated with the company name. Fresh green and white color scheme. Modern sans-serif font. The icon should work standalone but also pair well with the text.",
    "mode": "max"
  }'
```

### 4. Monogram Logo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a monogram logo for a luxury fashion brand with initials JM (James Morrison). Interlock the letters elegantly. Gold on black background. High-end, sophisticated feel. Classic with a modern twist.",
    "mode": "max"
  }'
```

### 5. Mascot Logo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a mascot logo for a gaming company called Thunder Wolves. Design a fierce but friendly wolf character with lightning bolt elements. Bold colors - purple, electric blue, white. The wolf should have personality and attitude. Suitable for esports branding.",
    "mode": "max"
  }'
```

### 6. Abstract Logo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an abstract logo for a fintech startup called Quantum Finance. Use geometric shapes that suggest growth, security, and innovation. Gradient from deep blue to teal. No literal imagery - focus on abstract forms that feel professional and cutting-edge.",
    "mode": "max"
  }'
```

### 7. Emblem/Badge Logo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an emblem logo for a craft brewery called Mountain Peak Brewing, established 2015. Design a circular badge with mountain imagery, hops, and the company name. Vintage Americana style. Navy blue, gold, and cream colors. Should look great on bottle labels and merchandise.",
    "mode": "max"
  }'
```

### 8. Minimalist Logo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an ultra-minimalist logo for a design studio called FORM. Single color, black on white. Reduce the concept to its absolute essence - clean lines, perfect proportions, no unnecessary elements. Should work at any size from favicon to billboard.",
    "mode": "max"
  }'
```

### 9. Logo Variations (Multi-Turn)

Use `session_id` to create consistent logo variations:

```bash
# Create the primary logo
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern logo for a sustainable fashion brand called Earthwear. Combine a stylized leaf with elegant typography. Earth tones - forest green and warm brown.",
    "session_id": "earthwear-logo-project",
    "mode": "max"
  }'

# Create black and white version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a black and white version of this logo. Pure black on white background, maintaining all the visual impact.",
    "session_id": "earthwear-logo-project",
    "mode": "max"
  }'

# Create icon-only version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an icon-only version - just the leaf symbol without any text. This will be used for app icons and social media profile pictures.",
    "session_id": "earthwear-logo-project",
    "mode": "max"
  }'
```

### 10. Logo with Transparent Background

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a logo for a photography studio called Aperture Arts. Modern camera aperture icon with elegant text. Create it with a transparent background (PNG format) so it can be placed on any color background. Black logo that will work on light backgrounds.",
    "mode": "max"
  }'
```

## Best Practices

### Design Principles
- **Simplicity**: Great logos are simple and memorable
- **Scalability**: Must work from favicon (16px) to billboard
- **Versatility**: Should work in color, B&W, and reversed
- **Timelessness**: Avoid trendy elements that will date quickly
- **Relevance**: Should reflect the brand's industry and values

### Prompt Tips

When requesting logos, include these details:

1. **Brand Name**: Exact spelling and capitalization
2. **Industry/Type**: What does the business do?
3. **Style Preference**: Modern, classic, playful, professional, etc.
4. **Color Preferences**: Specific colors or color feelings
5. **Imagery Ideas**: Any symbols or concepts to incorporate
6. **Usage Context**: Where will the logo be used most?
7. **What to Avoid**: Any styles or elements to stay away from

### Example Prompt Structure

```
"Create a [style] logo for [brand name], a [industry/description].
[Visual elements and concept].
Colors: [color preferences].
Style: [modern/classic/playful/etc].
The logo should [key requirements]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final logo designs, client presentations | Slower | Highest |
| `eco` | Quick concepts, brainstorming, exploration | Faster | Good |

## Multi-Turn Logo Development

Use `session_id` for iterative logo design:

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a logo for a tech company called Nova Labs. Modern, innovative feel.",
    "session_id": "nova-labs-branding"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I like the concept but make it more bold and add a gradient from purple to blue.",
    "session_id": "nova-labs-branding"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 3 more variations with different icon styles but keep the same color scheme.",
    "session_id": "nova-labs-branding"
  }'
```

## Batch Logo Exploration

Generate multiple concepts quickly:

```bash
# Concept A - Minimalist
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist logo for Horizon Analytics - clean geometric shapes, single color",
    "mode": "eco"
  }'

# Concept B - Bold
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a bold logo for Horizon Analytics - strong typography, gradient colors",
    "mode": "eco"
  }'

# Concept C - Abstract
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an abstract logo for Horizon Analytics - flowing shapes suggesting data and insight",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product photography
- `meta-ad-creative-generation` - Social media ad creatives
