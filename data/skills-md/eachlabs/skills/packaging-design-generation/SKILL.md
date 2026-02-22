---
name: packaging-design-generation
description: Generate professional product packaging designs using each::sense AI. Create box designs, food packaging, cosmetic containers, beverage labels, supplement bottles, coffee bags, candle packaging, gift boxes, shopping bags, and product labels.
metadata:
  author: eachlabs
  version: "1.0"
---

# Packaging Design Generation

Generate professional product packaging designs using each::sense. This skill creates high-quality packaging mockups and designs for various product categories, from food and beverages to cosmetics and retail.

## Features

- **Product Box Design**: Electronics, toys, software, and general product boxes
- **Food Packaging**: Snacks, frozen foods, bakery items, and meal kits
- **Cosmetic/Beauty Packaging**: Skincare, makeup, haircare, and wellness products
- **Beverage Labels**: Wine, beer, juice, water, and soft drink labels
- **Supplement Packaging**: Vitamins, protein powders, and health supplements
- **Coffee Bag Design**: Specialty coffee, tea, and artisan beverage packaging
- **Candle Packaging**: Luxury candles, home fragrance, and gift sets
- **Gift Box Design**: Premium gift packaging and presentation boxes
- **Shopping Bags**: Retail bags, paper bags, and branded tote bags
- **Product Labels/Stickers**: Custom labels, stickers, and seal designs

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a premium coffee bag packaging design for an artisan roaster called Mountain Peak Coffee, featuring earthy tones and mountain imagery",
    "mode": "max"
  }'
```

## Packaging Design Categories

| Category | Common Sizes | Typical Style |
|----------|--------------|---------------|
| Product Box | Various | Clean, informative, brand-focused |
| Food Packaging | Standard retail | Appetizing, colorful, regulatory-compliant |
| Cosmetics | Compact, sleek | Elegant, minimalist, luxurious |
| Beverage Labels | 750ml, 330ml, etc. | Eye-catching, brand identity |
| Supplements | Bottle/pouch | Clean, trustworthy, health-focused |
| Coffee Bags | 250g, 500g, 1kg | Artisan, origin-focused, textural |
| Candles | Jar/box | Cozy, luxurious, gift-ready |
| Gift Boxes | Various | Premium, elegant, festive |
| Shopping Bags | Small/Medium/Large | Brand-forward, sustainable look |
| Labels/Stickers | Various | Versatile, clear messaging |

## Use Case Examples

### 1. Product Box Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a sleek product box design for premium wireless headphones. Modern tech aesthetic with dark matte finish, silver accents, and clean typography. Show the box at a 3/4 angle with the product visible through a window cutout. Brand name: SoundWave Pro.",
    "mode": "max"
  }'
```

### 2. Food Packaging Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a vibrant snack packaging for organic veggie chips. Colorful, playful design with hand-drawn vegetable illustrations. Kraft paper bag with a window to show the product. Brand: Crunch Garden. Flavors: Sea Salt & Herb. Include organic certification badge space.",
    "mode": "max"
  }'
```

### 3. Cosmetic/Beauty Packaging

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create luxury skincare packaging for a serum bottle and box set. Minimalist design with soft pink and rose gold accents. Frosted glass bottle with dropper, matching outer box. Brand: Lumina Beauty. Product: Renewal Face Serum. Elegant serif typography.",
    "mode": "max"
  }'
```

### 4. Beverage Label Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a craft beer label for an IPA. Vintage-inspired with modern twist, featuring hop illustrations and mountain scenery. Deep green and gold color palette. Brewery name: Summit Brewing Co. Beer name: Trail Blazer IPA. Include ABV space and tasting notes area.",
    "mode": "max"
  }'
```

### 5. Supplement/Vitamin Packaging

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a clean, trustworthy supplement bottle design for daily multivitamins. White bottle with blue and green accents suggesting health and vitality. Modern sans-serif typography. Brand: VitaCore. Product: Complete Daily Multivitamin. Show front label with dosage info area.",
    "mode": "max"
  }'
```

### 6. Coffee Bag Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design an artisan coffee bag for single-origin Ethiopian beans. Kraft paper bag with matte black label. Featuring Ethiopian landscape illustration in warm earth tones. Brand: Origin Story Coffee. Include space for roast date, flavor notes (blueberry, citrus, chocolate), and brewing recommendations.",
    "mode": "max"
  }'
```

### 7. Candle Packaging

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create luxury candle packaging for a home fragrance brand. Amber glass jar with minimalist white label, housed in a elegant black box with gold foil details. Brand: Maison Lumiere. Scent: Fireside & Vanilla. Cozy, sophisticated aesthetic suitable for gifting.",
    "mode": "max"
  }'
```

### 8. Gift Box Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a premium gift box for a chocolate assortment. Rich burgundy exterior with embossed gold pattern, satin ribbon closure. Interior with velvet-textured compartments visible. Brand: Artisan Chocolatier. Luxurious, festive design suitable for holidays and special occasions.",
    "mode": "max"
  }'
```

### 9. Shopping Bag Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a retail shopping bag design for a boutique fashion store. Thick paper bag with rope handles. Minimalist design with large logo placement, matte white with black typography. Brand: Atelier Mode. Sustainable, premium feel that customers would reuse.",
    "mode": "max"
  }'
```

### 10. Product Label/Sticker Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a product label for artisan honey jars. Circular label with honeycomb pattern border, featuring bee illustration. Warm amber and golden tones. Brand: Wild Meadow Apiary. Include space for honey type, weight, and harvest date. Rustic yet refined aesthetic.",
    "mode": "max"
  }'
```

## Best Practices

### Design Elements
- **Brand Consistency**: Maintain logo placement, color palette, and typography across packaging
- **Hierarchy**: Establish clear visual hierarchy with brand name, product name, and key information
- **Whitespace**: Use negative space effectively for premium feel
- **Materials**: Consider how design translates to different materials (matte, gloss, kraft, metallic)

### Technical Considerations
- **Bleed Areas**: Account for printing bleed in design requests
- **Die-Cut Windows**: Specify if product should be visible through packaging
- **Structural Design**: Describe box/container shape and dimensions
- **Print Finishes**: Mention desired finishes (foil stamping, embossing, spot UV)

### Industry Standards
- **Food Packaging**: Include space for nutrition facts, ingredients, allergens
- **Cosmetics**: Plan for ingredients list, usage instructions, warnings
- **Beverages**: Account for bottle shape and label wrap-around
- **Supplements**: Include supplement facts panel and FDA disclaimer space

## Prompt Tips for Packaging Design

When creating packaging designs, include these details in your prompt:

1. **Product Type**: What is being packaged (food, cosmetic, tech, etc.)
2. **Brand Name**: The brand identity to feature
3. **Product Name**: Specific product or variant name
4. **Design Style**: Minimalist, luxurious, playful, vintage, modern, etc.
5. **Color Palette**: Specific colors or mood (earthy, vibrant, monochromatic)
6. **Materials**: Kraft paper, glass, matte cardboard, metallic accents
7. **View Angle**: Front view, 3/4 angle, flat lay, mockup style
8. **Special Elements**: Windows, foil stamping, embossing, ribbons

### Example Prompt Structure

```
"Create a [style] packaging design for [product type].
[Material/container type] with [color palette] colors.
Brand: [name]. Product: [name].
[Special features like windows, finishes, or structural details].
[View angle and presentation style]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final packaging designs, client presentations, print-ready concepts | Slower | Highest |
| `eco` | Quick drafts, concept exploration, initial ideation | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on packaging designs:

```bash
# Initial design concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a protein powder packaging design, modern fitness aesthetic, bold typography",
    "session_id": "protein-packaging-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more premium looking with matte black finish and gold accents. Add a resealable pouch mockup.",
    "session_id": "protein-packaging-001"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 flavor variants: Chocolate and Vanilla, keeping the same design language",
    "session_id": "protein-packaging-001"
  }'
```

## Product Line Consistency

Generate cohesive packaging across product variants:

```bash
# First product in line
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create skincare packaging for a cleanser. Minimalist white with sage green accents. Brand: Pure Botanics. Establish the design system for the entire product line.",
    "session_id": "pure-botanics-line"
  }'

# Second product (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create the toner packaging in the same design language. Same brand identity but different bottle shape.",
    "session_id": "pure-botanics-line"
  }'

# Third product
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the moisturizer jar packaging. Continue the Pure Botanics design system with consistent typography and color palette.",
    "session_id": "pure-botanics-line"
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
- `product-photo-generation` - E-commerce product shots
- `meta-ad-creative-generation` - Meta advertising creatives
- `google-ad-creative-generation` - Google Ads creatives
