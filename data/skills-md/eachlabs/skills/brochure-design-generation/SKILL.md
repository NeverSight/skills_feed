---
name: brochure-design-generation
description: Generate professional brochure designs using each::sense AI. Create tri-fold, bi-fold, corporate, travel, product, real estate, healthcare, educational, event, and service brochures with print-ready layouts.
metadata:
  author: eachlabs
  version: "1.0"
---

# Brochure Design Generation

Generate professional brochure designs using each::sense. This skill creates visually appealing brochure layouts for various industries and purposes, from corporate communications to travel marketing.

## Features

- **Tri-Fold Brochures**: Classic three-panel designs for marketing materials
- **Bi-Fold Brochures**: Simple two-panel layouts for concise messaging
- **Corporate Brochures**: Professional designs for business communications
- **Travel/Tourism Brochures**: Inspiring visuals for destinations and tours
- **Product Catalogs**: Multi-page layouts showcasing product lines
- **Real Estate Brochures**: Property listings and development showcases
- **Healthcare Brochures**: Medical services and patient information
- **Educational Brochures**: School, course, and program materials
- **Event Programs**: Conference, wedding, and event schedules
- **Service Menus**: Restaurant, spa, and service pricing layouts

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tri-fold brochure design for a digital marketing agency. Modern, clean aesthetic with blue and white color scheme. Include sections for services, case studies, and contact information.",
    "mode": "max"
  }'
```

## Brochure Formats & Sizes

| Type | Dimensions (Flat) | Panels | Use Case |
|------|-------------------|--------|----------|
| Tri-Fold | 11" x 8.5" | 3 panels | Marketing, services overview |
| Bi-Fold | 11" x 8.5" | 2 panels | Simple messaging, menus |
| Z-Fold | 11" x 8.5" | 3 panels | Sequential information |
| Gate Fold | 17" x 11" | 4 panels | Premium presentations |
| Accordion | Variable | 4+ panels | Detailed catalogs |
| A4 Single | 8.27" x 11.69" | 1 panel | Flyers, single-page info |

## Use Case Examples

### 1. Tri-Fold Brochure (Marketing Agency)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tri-fold brochure design for a digital marketing agency called Vertex Digital. Modern minimalist design with navy blue and electric orange accents. Front panel: bold logo and tagline. Inside panels: services (SEO, PPC, Social Media), client testimonials, and case study highlights. Back panel: contact info and QR code placeholder. Professional photography style with geometric design elements.",
    "mode": "max"
  }'
```

### 2. Bi-Fold Brochure (Restaurant Menu)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a bi-fold brochure design for an Italian restaurant called Bella Notte. Elegant design with warm burgundy and cream colors. Front: restaurant name with appetizing pasta dish image. Inside spread: menu sections for antipasti, primi, secondi, and dolci with food photography. Back: location map placeholder, hours, and reservation info. Rustic Italian aesthetic with subtle texture.",
    "mode": "max"
  }'
```

### 3. Corporate Brochure (Company Profile)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate brochure design for a technology consulting firm called Nexus Solutions. Premium, sophisticated design with charcoal gray and gold accents. Include sections for: company overview, leadership team, service offerings, global presence, and client logos placeholder. Clean typography, professional business photography, and modern data visualization elements. Print-ready A4 format.",
    "mode": "max"
  }'
```

### 4. Travel/Tourism Brochure

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a travel brochure for exploring Santorini, Greece. Stunning visuals with white-washed buildings and blue domes. Tri-fold layout with: cover showing iconic sunset view, inside panels featuring top attractions (Oia, Fira, beaches), tour packages with pricing placeholders, and local dining recommendations. Vibrant Mediterranean color palette. Back panel with travel tips and booking information.",
    "mode": "max"
  }'
```

### 5. Product Catalog Brochure

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a product catalog brochure for a premium watch brand called Chronos. Luxury aesthetic with black background and silver accents. Showcase 6 different watch models with detailed product photography. Include: model names, key features, price placeholders, and specifications. Elegant typography with ample white space. Gate-fold format for premium presentation.",
    "mode": "max"
  }'
```

### 6. Real Estate Brochure

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a real estate brochure for a luxury condominium development called The Residences at Harbor View. Sophisticated design with deep teal and champagne gold colors. Include: hero image of building exterior, floor plan layouts, amenities section (pool, gym, concierge), neighborhood highlights, and pricing table placeholder. Premium photography showing interiors and waterfront views. Bi-fold format.",
    "mode": "max"
  }'
```

### 7. Healthcare/Medical Brochure

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a healthcare brochure for a family medical clinic called Wellness First Medical Center. Calming design with soft blue and green colors. Tri-fold format with: services offered (primary care, pediatrics, lab services), doctor profiles section, patient resources, insurance information, and location with hours. Friendly, approachable imagery of diverse patients and healthcare providers. Clean, easy-to-read layout.",
    "mode": "max"
  }'
```

### 8. Educational Brochure (University)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an educational brochure for a university business school MBA program. Professional yet inspiring design with maroon and white school colors. Include: program overview, curriculum highlights, faculty showcase, career outcomes statistics, campus life images, and application deadlines. Feature diverse students in academic and professional settings. Tri-fold format with clear call-to-action for applications.",
    "mode": "max"
  }'
```

### 9. Event Program Brochure

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an event program brochure for a tech conference called Innovation Summit 2024. Dynamic design with gradient purple to blue colors and tech-inspired geometric patterns. Include: event schedule over 2 days, keynote speaker profiles, workshop sessions, sponsor logos placeholder, venue map, and networking event details. Modern, energetic aesthetic. Bi-fold format for easy reference.",
    "mode": "max"
  }'
```

### 10. Service Menu Brochure (Spa)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a service menu brochure for a luxury spa called Serenity Wellness Spa. Zen-inspired design with soft sage green, cream, and natural wood tones. Tri-fold format with: massage services and pricing, facial treatments, body treatments, packages and specials, and booking information. Peaceful imagery with natural elements like stones, bamboo, and orchids. Elegant serif typography with generous spacing.",
    "mode": "max"
  }'
```

## Multi-Turn Creative Iteration

Use `session_id` to iterate on brochure designs:

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tri-fold brochure for an eco-friendly cleaning company. Green and natural aesthetic.",
    "session_id": "eco-brochure-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the design more modern with less leaf imagery. Add icons for each service type and include a pricing table.",
    "session_id": "eco-brochure-001"
  }'

# Request additional panels
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create the back panel design with contact information, social media icons, and an eco-certification badge.",
    "session_id": "eco-brochure-001"
  }'
```

## Brochure Series Generation

Generate multiple related brochures for a brand:

```bash
# Main services brochure
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tri-fold brochure for a law firm called Sterling & Associates. Navy and gold color scheme, professional photography, services overview.",
    "session_id": "law-firm-brochures"
  }'

# Practice area specific brochure
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching brochure specifically for the Corporate Law practice area. Maintain the same brand identity and color scheme.",
    "session_id": "law-firm-brochures"
  }'

# Client testimonial brochure
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a client success stories brochure in the same style. Feature 3-4 case study placeholders with outcome statistics.",
    "session_id": "law-firm-brochures"
  }'
```

## Best Practices

### Layout & Design
- **Visual Hierarchy**: Guide the reader's eye with clear heading structure
- **White Space**: Avoid overcrowding - let content breathe
- **Fold Awareness**: Place key content considering how the brochure unfolds
- **Bleed Areas**: Include 3mm bleed for professional printing
- **Safe Zones**: Keep important text 5mm from fold lines

### Typography
- **Font Pairing**: Use maximum 2-3 font families
- **Readability**: Body text should be 9-12pt minimum
- **Headlines**: Make them bold and scannable
- **Contrast**: Ensure text is readable against backgrounds

### Imagery
- **High Resolution**: Use 300 DPI for print-ready output
- **Consistent Style**: Maintain visual cohesion across panels
- **Brand Colors**: Apply consistent color palette
- **Photo Quality**: Use professional or high-quality stock imagery

### Content Structure
- **Cover Appeal**: Front panel should create immediate interest
- **Logical Flow**: Information should progress naturally
- **Call-to-Action**: Include clear next steps
- **Contact Info**: Always include ways to reach you

## Prompt Tips for Brochure Design

When creating brochure designs, include these details in your prompt:

1. **Format**: Specify brochure type (tri-fold, bi-fold, etc.)
2. **Industry/Purpose**: What is the brochure for?
3. **Brand Identity**: Colors, style, company name
4. **Content Sections**: What information to include
5. **Imagery Style**: Photography style, illustrations, icons
6. **Target Audience**: Who will read this brochure?
7. **Print Specifications**: Size, orientation if specific

### Example Prompt Structure

```
"Create a [brochure type] brochure for [company/purpose].
[Brand colors and style preferences].
Include sections for: [content areas].
Target audience: [demographic].
[Additional requirements like imagery style, special elements, etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final print-ready designs, client presentations | Slower | Highest |
| `eco` | Quick drafts, concept exploration, layout testing | Faster | Good |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Social media ad creatives
- `product-photo-generation` - E-commerce product shots
- `presentation-design-generation` - Slide deck designs
