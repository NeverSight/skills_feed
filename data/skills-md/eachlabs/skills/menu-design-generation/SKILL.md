---
name: menu-design-generation
description: Generate professional restaurant, cafe, and bar menu designs using each::sense AI. Create print-ready menus, digital displays, QR code menus, and seasonal specials with stunning food photography and elegant typography layouts.
metadata:
  author: eachlabs
  version: "1.0"
---

# Menu Design Generation

Generate professional menu designs for restaurants, cafes, bars, and food service businesses using each::sense. This skill creates visually appealing menu layouts with food imagery, typography, and design elements optimized for various formats and dining experiences.

## Features

- **Full Page Menus**: Complete restaurant menus with sections and pricing
- **Digital Display Boards**: High-contrast menus for screens and digital signage
- **Cafe & Coffee Menus**: Cozy, artisanal designs for coffee shops
- **Bar & Cocktail Menus**: Sophisticated drink menus with elegant styling
- **Fast Food Boards**: Bold, eye-catching menu boards for quick service
- **Fine Dining Menus**: Luxurious, minimalist designs for upscale restaurants
- **Seasonal Specials**: Limited-time menu designs with festive themes
- **QR Code Menus**: Mobile-optimized designs for contactless ordering

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern restaurant menu design for an Italian trattoria with appetizers, pasta, mains, and desserts sections. Warm rustic aesthetic with elegant typography.",
    "mode": "max"
  }'
```

## Menu Formats & Sizes

| Menu Type | Aspect Ratio | Recommended Size | Use Case |
|-----------|--------------|------------------|----------|
| Print Menu (Letter) | 8.5:11 | 2550x3300 px | Traditional print menus |
| Print Menu (A4) | 1:1.414 | 2480x3508 px | International print format |
| Digital Display | 16:9 | 1920x1080 px | TV screens, monitors |
| Digital Display (Vertical) | 9:16 | 1080x1920 px | Vertical digital signage |
| Table Tent | 4:6 | 1200x1800 px | Table-top displays |
| QR Menu (Mobile) | 9:16 | 1080x1920 px | Mobile-optimized menus |
| Menu Board | 3:2 | 1800x1200 px | Wall-mounted boards |

## Use Case Examples

### 1. Restaurant Menu (Full Page)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a full-page restaurant menu design for a Mediterranean bistro. Include sections for Starters (hummus, falafel, calamari), Mains (grilled lamb, seafood platter, moussaka), and Desserts (baklava, tiramisu). Use warm earth tones, elegant serif typography, and include subtle olive branch decorative elements. Portrait orientation for print.",
    "mode": "max"
  }'
```

### 2. Cafe/Coffee Shop Menu

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a cozy coffee shop menu board for an artisan cafe. Include Hot Drinks (espresso, latte, cappuccino, mocha), Cold Drinks (iced coffee, cold brew, frappes), and Pastries (croissants, muffins, cookies). Rustic chalkboard aesthetic with hand-drawn style illustrations, warm brown and cream colors. Horizontal format for counter display.",
    "mode": "max"
  }'
```

### 3. Bar/Cocktail Menu

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an upscale cocktail bar menu design. Include Signature Cocktails (Old Fashioned, Negroni, Espresso Martini), Classic Cocktails, Wine by the Glass, and Premium Spirits sections. Dark moody aesthetic with gold accents, art deco styling, elegant script typography. Tall format suitable for leather menu holder.",
    "mode": "max"
  }'
```

### 4. Fast Food Menu Board

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a bold fast food menu board for a burger joint. Include Burgers (classic, bacon, veggie), Sides (fries, onion rings, nuggets), Drinks, and Combo Meals with large pricing. Bright colors (red, yellow, white), high contrast, appetizing burger photography, easy to read from distance. 16:9 landscape for overhead display.",
    "mode": "max"
  }'
```

### 5. Fine Dining Menu

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an elegant fine dining tasting menu design. Include 7-course tasting menu: Amuse-bouche, First Course, Fish Course, Palate Cleanser, Main Course, Pre-Dessert, Dessert. Minimalist luxury aesthetic with lots of white space, thin elegant fonts, subtle gold foil accents on cream paper texture. Portrait A4 format.",
    "mode": "max"
  }'
```

### 6. Brunch Menu

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a vibrant weekend brunch menu for a trendy cafe. Include Eggs & Benedicts, Pancakes & Waffles, Healthy Bowls, Bottomless Brunch Drinks (mimosas, bloody marys, bellinis). Fresh, light aesthetic with pastel colors, modern sans-serif typography, watercolor fruit illustrations. Portrait format for table menus.",
    "mode": "max"
  }'
```

### 7. Dessert Menu

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a decadent dessert menu for a patisserie. Include Cakes (chocolate lava, cheesecake, tiramisu), Pastries (eclairs, macarons, tarts), Ice Cream & Sorbets, and Specialty Coffee Pairings. Luxurious aesthetic with rich colors (burgundy, gold, chocolate brown), elegant cursive headers, beautiful dessert photography. Square format.",
    "mode": "max"
  }'
```

### 8. Digital Menu for Display

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a digital menu display for a sushi restaurant TV screen. Include Sashimi, Nigiri, Maki Rolls, Special Rolls with prices. Modern Japanese aesthetic with dark background for screen display, high contrast white and red text, clean grid layout, subtle wave patterns. 16:9 HD format optimized for digital signage.",
    "mode": "max"
  }'
```

### 9. QR Code Menu Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a mobile-optimized QR code menu design for a taco restaurant. Include Tacos (carnitas, al pastor, fish), Burritos, Sides (rice, beans, guacamole), and Drinks. Scrollable single-column layout, large touch-friendly sections, vibrant Mexican colors (orange, green, pink), playful typography. 9:16 mobile portrait format with clear section headers.",
    "mode": "max"
  }'
```

### 10. Seasonal/Special Menu

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a winter holiday special menu for a restaurant. Include Holiday Appetizers, Seasonal Mains (roast turkey, prime rib, glazed ham), Festive Desserts (pumpkin pie, yule log, gingerbread), and Holiday Cocktails. Elegant winter theme with deep greens, gold, and cream colors, snowflake accents, festive but sophisticated typography. Portrait format for table insert.",
    "mode": "max"
  }'
```

## Best Practices

### Design Principles
- **Hierarchy**: Use clear visual hierarchy with section headers, item names, and prices
- **Readability**: Ensure text is readable at intended viewing distance
- **White Space**: Don't overcrowd - let items breathe
- **Consistency**: Maintain consistent styling throughout all sections
- **Brand Alignment**: Match the restaurant's overall brand and ambiance

### Typography Tips
- **Headers**: Use decorative or serif fonts for section headers
- **Body**: Use clean, readable fonts for item descriptions
- **Prices**: Align prices consistently (right-aligned or with dot leaders)
- **Size**: Menu item names should be larger than descriptions

### Color Guidelines
- **Fine Dining**: Neutral colors, black/white, gold accents
- **Casual Dining**: Warm, inviting colors matching cuisine theme
- **Fast Food**: Bold, high-contrast colors (red, yellow, orange)
- **Cafes**: Earthy tones, pastels, natural colors
- **Bars**: Dark backgrounds with metallic accents

### Format Considerations
- **Print Menus**: High resolution (300 DPI), CMYK color consideration
- **Digital Displays**: RGB colors, high contrast for visibility
- **Mobile Menus**: Large tap targets, scrollable sections
- **Menu Boards**: Readable from 10+ feet away

## Prompt Tips for Menu Design

When creating menu designs, include these details in your prompt:

1. **Restaurant Type**: Italian, Mexican, Japanese, Fine Dining, etc.
2. **Menu Sections**: List specific categories and example items
3. **Aesthetic Style**: Modern, rustic, elegant, playful, minimal
4. **Color Palette**: Specific colors or mood (warm, cool, vibrant)
5. **Format**: Print, digital display, mobile, specific dimensions
6. **Typography Style**: Elegant, bold, handwritten, modern
7. **Special Elements**: Decorative elements, photography style, borders

### Example Prompt Structure

```
"Create a [format] menu design for a [restaurant type].
Include sections for [menu sections with example items].
[Aesthetic style] with [color palette], [typography style].
[Special elements or requirements].
[Dimensions/orientation] for [intended use]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final print-ready menus, client presentations | Slower | Highest |
| `eco` | Quick drafts, concept exploration, layout testing | Faster | Good |

## Multi-Turn Menu Iteration

Use `session_id` to iterate on menu designs:

```bash
# Initial menu design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a menu design for a modern Asian fusion restaurant with appetizers, mains, and drinks",
    "session_id": "menu-project-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the background darker and add more gold accents. Also add a dessert section.",
    "session_id": "menu-project-001"
  }'

# Request format variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a digital display version of this menu in 16:9 landscape format",
    "session_id": "menu-project-001"
  }'
```

## Menu Set Generation

Generate a complete set of matching menus:

```bash
# Main dinner menu
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a dinner menu for an upscale steakhouse with elegant dark theme, gold accents",
    "session_id": "steakhouse-brand"
  }'

# Matching wine menu
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching wine list menu in the same style - include Reds, Whites, and Champagne sections",
    "session_id": "steakhouse-brand"
  }'

# Matching dessert menu
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching dessert menu in the same brand style",
    "session_id": "steakhouse-brand"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Food photography for menus
- `meta-ad-creative-generation` - Restaurant advertising creatives
- `google-ad-creative-generation` - Restaurant Google Ads
