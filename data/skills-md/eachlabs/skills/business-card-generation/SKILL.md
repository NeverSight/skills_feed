---
name: business-card-generation
description: Generate professional business cards using each::sense AI. Create corporate, creative, minimalist, luxury, and specialty business cards optimized for print at standard 3.5 x 2 inch size.
metadata:
  author: eachlabs
  version: "1.0"
---

# Business Card Generation

Generate professional business cards using each::sense. This skill creates print-ready business card designs for various industries, styles, and purposes at the standard 3.5 x 2 inch (1050 x 600 px) size.

## Features

- **Corporate Cards**: Professional designs for business executives and employees
- **Creative Cards**: Artistic designs for designers, artists, and creative professionals
- **Minimalist Cards**: Clean, simple designs with focus on typography
- **Luxury Cards**: Premium, elegant designs with sophisticated aesthetics
- **Industry-Specific Cards**: Tailored designs for real estate, photography, restaurants, tech, and more
- **Vertical Cards**: Portrait orientation for unique, standout designs
- **Double-Sided Cards**: Front and back designs with complementary layouts

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional business card for a marketing consultant, clean modern design with space for name, title, phone, email, and website",
    "mode": "max"
  }'
```

## Business Card Specifications

| Type | Dimensions | Pixels | Use Case |
|------|------------|--------|----------|
| Standard Horizontal | 3.5 x 2 inches | 1050 x 600 px | Most common format |
| Standard Vertical | 2 x 3.5 inches | 600 x 1050 px | Creative/unique presentations |
| European | 85 x 55 mm | 1004 x 650 px | International standard |
| Square | 2.5 x 2.5 inches | 750 x 750 px | Modern/creative businesses |

## Use Case Examples

### 1. Corporate Business Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate business card at 1050x600 pixels for a senior financial advisor. Navy blue and gold color scheme, professional and trustworthy feel. Include placeholder areas for: name, title (Senior Financial Advisor), company name, phone number, email, and office address. Add a subtle geometric pattern in the background. Clean sans-serif typography.",
    "mode": "max"
  }'
```

### 2. Creative/Designer Business Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an artistic business card at 1050x600 pixels for a graphic designer. Bold, creative design with vibrant gradient colors (purple to pink to orange). Abstract geometric shapes, modern and eye-catching. Include space for name, title (Creative Director), portfolio website, email, and Instagram handle. Make it memorable and showcase design skills.",
    "mode": "max"
  }'
```

### 3. Minimalist Business Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist business card at 1050x600 pixels. White background with black typography only. Elegant serif font for the name, clean sans-serif for contact details. Generous white space, sophisticated and refined. Include areas for: name, job title, email, phone, and a small logo placeholder in the corner. Less is more aesthetic.",
    "mode": "max"
  }'
```

### 4. Luxury/Premium Business Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a luxury business card at 1050x600 pixels for a high-end jewelry brand owner. Black background with gold foil effect elements. Elegant script font for the name, refined serif for details. Include subtle embossed texture effect, ornate border detail. Space for: name, title (Founder & Creative Director), brand name, phone, email, and boutique address. Premium, exclusive feel.",
    "mode": "max"
  }'
```

### 5. Tech Startup Business Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern tech startup business card at 1050x600 pixels. Dark theme with neon accent colors (electric blue or cyan). Futuristic, innovative aesthetic with subtle circuit board or data visualization patterns. Clean modern typography. Include space for: name, title (Co-Founder & CTO), company name, email, LinkedIn profile, and QR code placeholder. Tech-forward and cutting-edge vibe.",
    "mode": "max"
  }'
```

### 6. Real Estate Agent Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a real estate agent business card at 1050x600 pixels. Professional yet approachable design. Include a photo placeholder area on the left side. Color scheme: deep teal and white with gold accents. Include space for: agent name, title (Licensed Real Estate Agent), brokerage name, phone, email, website, and license number. Add a small house icon or property silhouette. Trustworthy and established feel.",
    "mode": "max"
  }'
```

### 7. Photographer Business Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photographer business card at 1050x600 pixels. Artistic design with a large image placeholder area showing a blurred/abstract photograph background. Camera aperture icon or lens element as design feature. Elegant typography in white over the image. Include space for: photographer name, specialty (Wedding & Portrait Photography), phone, email, Instagram, and website. Creative and visual storytelling aesthetic.",
    "mode": "max"
  }'
```

### 8. Restaurant/Chef Business Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a restaurant chef business card at 1050x600 pixels. Warm, inviting color palette - cream background with burgundy and copper accents. Include a chef hat or knife icon. Elegant typography mixing script and serif fonts. Subtle food-related pattern or texture. Include space for: chef name, title (Executive Chef), restaurant name, phone, email, and restaurant address. Culinary excellence and artistry feel.",
    "mode": "max"
  }'
```

### 9. Vertical Business Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a vertical business card at 600x1050 pixels (portrait orientation) for an architect. Modern architectural design with clean lines and geometric shapes. Black and white with one accent color (coral or mustard). Include building silhouette or blueprint element. Space for: name at top, title (Principal Architect), firm name, contact details stacked vertically - phone, email, website, office address. Contemporary and structural aesthetic.",
    "mode": "max"
  }'
```

### 10. Double-Sided Business Card (Front & Back)

```bash
# Front side
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the FRONT side of a double-sided business card at 1050x600 pixels for a law firm partner. Clean, prestigious design with navy blue background. Large centered logo placeholder area, firm name in elegant gold serif typography below. Established, authoritative, trustworthy aesthetic. This is the presentation side - minimal information, maximum impact.",
    "session_id": "lawfirm-card-001"
  }'

# Back side (same session for visual consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the BACK side of the same business card. White background with navy blue text to complement the front. Include all contact details: attorney name, title (Senior Partner), bar number, phone, fax, email, office address, and website. Clean layout with clear hierarchy. Add a thin gold accent line. Same typography style as front for consistency.",
    "session_id": "lawfirm-card-001"
  }'
```

## Best Practices

### Design Guidelines
- **Bleed Area**: Include 0.125 inch (3.75 px) bleed on all sides for printing
- **Safe Zone**: Keep important content 0.125 inch from the edge
- **Resolution**: Design at 300 DPI equivalent for crisp printing
- **Typography**: Use minimum 8pt font for readability
- **Contrast**: Ensure text is legible against background

### Content Hierarchy
1. **Name**: Most prominent element
2. **Title/Role**: Secondary prominence
3. **Company/Brand**: Supporting element
4. **Contact Info**: Clear and organized
5. **Logo**: Balanced with other elements

### Color Considerations
- Use CMYK-safe colors for print accuracy
- Limit palette to 2-3 colors for cohesion
- Consider metallic/foil effects for luxury cards
- Ensure sufficient contrast for readability

## Prompt Tips for Business Cards

When creating business cards, include these details in your prompt:

1. **Dimensions**: Specify pixel size (1050x600 for standard horizontal)
2. **Industry/Role**: What profession is this card for?
3. **Style**: Corporate, creative, minimalist, luxury, etc.
4. **Color Scheme**: Specific colors or general palette
5. **Information Fields**: What text areas to include
6. **Special Elements**: Icons, patterns, photo areas, QR codes
7. **Typography Style**: Serif, sans-serif, script, modern, classic

### Example Prompt Structure

```
"Create a [style] business card at [dimensions] for a [profession/industry].
[Color scheme description]. Include space for: [list of information fields].
[Design elements and aesthetic description].
[Additional requirements like icons, patterns, effects]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final print-ready designs, client presentations | Slower | Highest |
| `eco` | Quick concepts, draft iterations, bulk variations | Faster | Good |

## Multi-Turn Design Iteration

Use `session_id` to iterate on business card designs:

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a business card for a yoga instructor, calming natural aesthetic",
    "session_id": "yoga-card-project"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the colors warmer, add a lotus flower icon, and use a more elegant script font for the name",
    "session_id": "yoga-card-project"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different color palettes - one with sage green, one with dusty rose",
    "session_id": "yoga-card-project"
  }'
```

## Batch Generation for Teams

Generate consistent cards for team members:

```bash
# Template card
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate business card template for Acme Corporation. Blue and white color scheme with the company logo area in top left. Fields: employee name, job title, department, phone, email, office location.",
    "session_id": "acme-team-cards",
    "mode": "max"
  }'

# Generate variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Using the same design, create cards with these titles: CEO, CFO, VP of Marketing, Head of Engineering. Keep all other design elements consistent.",
    "session_id": "acme-team-cards"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt content |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Meta ad creatives
- `product-photo-generation` - Product photography
- `logo-generation` - Logo design
