---
name: qr-code-generation
description: Generate artistic and stylized QR codes using each::sense AI. Create branded QR codes, QR codes with logos, artistic designs, and custom themes that remain scannable while looking visually stunning.
metadata:
  author: eachlabs
  version: "1.0"
---

# QR Code Generation

Generate artistic, branded, and visually stunning QR codes using each::sense. This skill creates QR codes that combine functionality with beautiful design, perfect for marketing materials, business cards, menus, and more.

## Features

- **Stylized QR Codes**: Transform standard QR codes into artistic designs
- **Logo Integration**: Embed company logos in the center of QR codes
- **Branded Colors**: Create QR codes matching your brand identity
- **Artistic Themes**: Nature, geometric, abstract, and custom themes
- **Background Integration**: Blend QR codes with background images
- **Gradient Effects**: Colorful gradient fills for eye-catching designs
- **Industry-Specific**: Restaurant menus, business cards, social profiles

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a stylized QR code for https://mywebsite.com with a modern tech aesthetic",
    "mode": "max"
  }'
```

## QR Code Design Considerations

| Element | Best Practice | Impact on Scannability |
|---------|---------------|------------------------|
| Error Correction | High (30%) recommended for artistic QR | Allows more design freedom |
| Logo Size | Max 30% of QR area | Larger logos reduce reliability |
| Color Contrast | Dark modules on light background | Essential for scanning |
| Quiet Zone | Maintain white border | Required for reliable scanning |
| Module Style | Rounded, dots, or custom shapes | Minimal impact if consistent |

## Use Case Examples

### 1. Basic Stylized QR Code

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a stylized QR code for https://example.com. Use a modern, clean design with rounded corners on the modules. Keep it scannable with good contrast. Blue and white color scheme.",
    "mode": "max"
  }'
```

### 2. QR Code with Logo Center

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a QR code for https://mycompany.com with space in the center for a company logo. The QR should have a professional corporate look with dark blue modules. Make sure the center area is clean and square-shaped for logo placement.",
    "mode": "max",
    "image_urls": ["https://example.com/company-logo.png"]
  }'
```

### 3. Artistic QR Code (Nature Theme)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an artistic QR code for https://naturereserve.org with a nature theme. Incorporate organic shapes - the modules should look like leaves or natural elements. Use earthy green and brown tones. The overall design should feel like it belongs in nature while remaining fully scannable.",
    "mode": "max"
  }'
```

### 4. Branded QR Code (Company Colors)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a branded QR code for https://techstartup.io using brand colors: primary #FF6B35 (orange) and secondary #1A1A2E (dark navy). The design should feel innovative and tech-forward. Use geometric patterns around the QR code. Maintain high scannability.",
    "mode": "max"
  }'
```

### 5. QR Code with Background Image

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a QR code for https://beachresort.com that integrates with a tropical beach background. The QR modules should be semi-transparent or styled to blend naturally with the beach scene. Use sandy and ocean blue tones. The code must remain scannable despite the artistic integration.",
    "mode": "max"
  }'
```

### 6. Minimalist QR Code

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a minimalist QR code for https://minimal.design. Ultra-clean aesthetic with thin, precise modules. Pure black on white. No decorative elements - just elegant simplicity. The design should feel premium and high-end through restraint.",
    "mode": "max"
  }'
```

### 7. Colorful Gradient QR Code

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a vibrant gradient QR code for https://creativestudio.art. Apply a smooth gradient across the modules from pink (#FF6B9D) to purple (#C44569) to blue (#3D5A80). The gradient should flow diagonally. Make it eye-catching and artistic while remaining scannable.",
    "mode": "max"
  }'
```

### 8. QR Code for Restaurant Menu

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a QR code for a restaurant digital menu at https://restaurant.com/menu. Design should have an elegant dining theme - incorporate subtle fork and knife motifs or food-related design elements around the QR. Use warm, appetizing colors like burgundy and gold. Perfect for table tents.",
    "mode": "max"
  }'
```

### 9. QR Code for Business Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a professional QR code for a digital business card vCard at https://vcard.example.com/johndoe. The design should be compact and suitable for printing on a business card. Use a sophisticated charcoal gray color with subtle metallic accents. Include a small professional icon element.",
    "mode": "max"
  }'
```

### 10. QR Code for Social Media Profile

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a fun, social-media-ready QR code linking to https://linktr.ee/influencer. Design should feel young, trendy, and Instagram-worthy. Use a playful color palette with neon accents. Add decorative elements like stars or sparkles around the QR. Perfect for sharing on social platforms.",
    "mode": "max"
  }'
```

## Best Practices

### Design Guidelines
- **Contrast is Key**: Maintain strong contrast between modules and background
- **Test Scannability**: Always verify the generated QR code scans properly
- **Error Correction Level**: Higher levels allow more artistic freedom
- **Quiet Zone**: Preserve white space around the QR code
- **Module Clarity**: Keep modules distinct even with artistic styling

### Color Guidelines
- **Dark on Light**: Traditional contrast works best
- **Avoid Red/Green**: May cause issues for colorblind users
- **Consistent Styling**: Apply effects uniformly across all modules
- **Background Contrast**: Ensure sufficient contrast with placement surface

### Size Recommendations
| Use Case | Minimum Size | Recommended Size |
|----------|--------------|------------------|
| Business Card | 2cm x 2cm | 2.5cm x 2.5cm |
| Table Tent | 3cm x 3cm | 4cm x 4cm |
| Poster | 5cm x 5cm | 8cm x 8cm |
| Billboard | 15cm x 15cm | 20cm x 20cm |

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production QR codes, print materials, branded assets | Slower | Highest |
| `eco` | Quick previews, concept testing, multiple variations | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on QR code designs:

```bash
# Initial QR code design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a stylized QR code for https://mybrand.com with a modern tech aesthetic",
    "session_id": "qr-design-project"
  }'

# Refine the design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the corners more rounded and add a subtle glow effect around the QR code",
    "session_id": "qr-design-project"
  }'

# Request color variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a version with gold and black colors for our premium product line",
    "session_id": "qr-design-project"
  }'
```

## Batch Generation for Multiple URLs

Generate consistent QR codes for multiple destinations:

```bash
# Main website QR
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a branded QR code for https://company.com with blue gradient styling",
    "mode": "eco",
    "session_id": "company-qr-set"
  }'

# Product page QR
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching QR code for https://company.com/products in the same style",
    "mode": "eco",
    "session_id": "company-qr-set"
  }'

# Contact page QR
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching QR code for https://company.com/contact in the same style",
    "mode": "eco",
    "session_id": "company-qr-set"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content in URL | Use appropriate URLs |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| QR not scanning | Too artistic, low contrast | Request higher contrast, simpler design |

## Prompt Tips for QR Codes

When creating QR codes, include these details in your prompt:

1. **Target URL**: The exact URL the QR code should link to
2. **Style Theme**: Modern, minimalist, artistic, branded, etc.
3. **Colors**: Specific hex codes or color descriptions
4. **Use Case**: Business card, poster, menu, social media
5. **Logo Requirement**: Whether to include space for a logo
6. **Special Effects**: Gradients, shadows, glow, patterns

### Example Prompt Structure

```
"Create a [style] QR code for [URL].
Use [colors] with [design elements].
Intended use: [placement/medium].
[Additional requirements like logo space, specific themes, etc.]
Ensure it remains scannable."
```

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - E-commerce product shots
- `meta-ad-creative-generation` - Meta ad creatives
