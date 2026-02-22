---
name: certificate-generation
description: Generate professional certificates, diplomas, and awards using each::sense AI. Create course completion certificates, achievement awards, professional certifications, academic diplomas, and custom branded certificates.
metadata:
  author: eachlabs
  version: "1.0"
---

# Certificate Generation

Generate professional certificates, diplomas, and awards using each::sense. This skill creates high-quality certificate images for educational institutions, corporate training, professional development, and recognition programs.

## Features

- **Course Completion Certificates**: Online courses, workshops, bootcamps
- **Achievement Certificates**: Milestones, goals, competitions
- **Award Certificates**: Recognition, excellence, outstanding performance
- **Professional Certifications**: Industry credentials, qualifications
- **Academic Diplomas**: Degrees, graduation, academic achievements
- **Training Certificates**: Corporate training, compliance, skill development
- **Appreciation Certificates**: Thank you, volunteer recognition, service awards
- **Participation Certificates**: Events, conferences, programs
- **Employee Recognition**: Employee of the month, years of service
- **Custom Branded Certificates**: Company-specific designs with logos and branding

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional course completion certificate for a web development bootcamp. Include placeholder text for recipient name, course name, completion date, and instructor signature.",
    "mode": "max"
  }'
```

## Certificate Design Elements

| Element | Description | Placement |
|---------|-------------|-----------|
| Border/Frame | Decorative borders, ornamental frames | Outer edges |
| Header | Organization name, logo placeholder | Top center |
| Title | Certificate type (Certificate of Completion, etc.) | Upper center |
| Recipient Name | Large, prominent placeholder | Center |
| Description | Achievement details, course name | Below name |
| Date | Completion/issue date | Lower section |
| Signatures | Authority signatures with titles | Bottom section |
| Seal/Badge | Official seal, emblem, or badge | Corner or center-bottom |
| Certificate ID | Unique identifier placeholder | Bottom corner |

## Use Case Examples

### 1. Course Completion Certificate

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an elegant course completion certificate for an online learning platform. Modern design with navy blue and gold accents. Include sections for: recipient name, course title, completion date, instructor signature, and platform logo placeholder. Add a decorative border and official seal.",
    "mode": "max"
  }'
```

### 2. Achievement Certificate

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design an achievement certificate for a sales team. Celebratory design with star motifs and ribbon accents. Include fields for: employee name, achievement description (e.g., exceeded quarterly target by 150%), date, and manager signature. Corporate professional style with red and silver color scheme.",
    "mode": "max"
  }'
```

### 3. Award Certificate

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an award certificate for a science fair competition. First place winner design with trophy imagery and laurel wreath elements. Include: winner name, project title, competition name, date, and judges signatures. Premium golden design with white background.",
    "mode": "max"
  }'
```

### 4. Professional Certification

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a professional certification certificate for a project management credential. Formal corporate style with clean lines. Include: certified professional name, certification title (Certified Project Manager), issue date, expiration date, certification ID number, and certifying authority signature. Use dark blue and white color scheme with embossed seal look.",
    "mode": "max"
  }'
```

### 5. Academic Diploma

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a traditional academic diploma for a university. Classic formal design with ornate border and calligraphic elements. Include: graduate name, degree title (Bachelor of Science in Computer Science), university name, graduation date, university seal placeholder, and signatures for dean and president. Ivory background with dark green and gold accents.",
    "mode": "max"
  }'
```

### 6. Training Certificate

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a corporate training certificate for workplace safety compliance. Professional and official design. Include: employee name, training program name, training hours completed, completion date, trainer signature, and HR manager signature. Add company logo placeholder and compliance badge. Blue and gray corporate colors.",
    "mode": "max"
  }'
```

### 7. Appreciation Certificate

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a certificate of appreciation for volunteer work. Warm and heartfelt design with soft colors. Include: volunteer name, organization name, description of service, hours contributed, date, and director signature. Add decorative elements like hands or hearts. Use teal and coral color palette.",
    "mode": "max"
  }'
```

### 8. Participation Certificate

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a participation certificate for a hackathon event. Modern tech-inspired design with geometric patterns. Include: participant name, event name, event dates, category/track participated in, and organizer signature. Use vibrant purple and electric blue colors with clean sans-serif typography.",
    "mode": "max"
  }'
```

### 9. Employee of the Month

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an Employee of the Month certificate. Prestigious and motivating design with star and spotlight elements. Include: employee name, month and year, department, reason for recognition, CEO signature, and company logo placeholder. Premium gold and black design with elegant typography.",
    "mode": "max"
  }'
```

### 10. Custom Branded Certificate

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a certificate template for a tech company named TechForward. Minimalist modern design that matches tech startup aesthetics. Include: recipient name, certificate title (flexible), achievement description, date, and dual signature lines. Use clean white background with gradient accent in purple to blue. Include prominent logo placeholder area and QR code placeholder for verification.",
    "mode": "max"
  }'
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final certificates, official documents | Slower | Highest |
| `eco` | Quick drafts, template exploration | Faster | Good |

## Multi-Turn Certificate Design

Use `session_id` to iterate on certificate designs:

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a certificate of completion for a coding bootcamp",
    "session_id": "cert-bootcamp-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the design more modern with darker colors and add a tech-inspired geometric border",
    "session_id": "cert-bootcamp-001"
  }'

# Add specific elements
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a QR code placeholder in the bottom right corner and include space for a holographic seal",
    "session_id": "cert-bootcamp-001"
  }'
```

## Certificate Series Generation

Generate consistent certificates for different levels:

```bash
# Bronze level certificate
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Bronze level achievement certificate for a learning platform. Use bronze/copper metallic accents. Include level badge prominently.",
    "session_id": "cert-levels-001"
  }'

# Silver level certificate (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the Silver level version of this certificate. Same layout but with silver metallic accents.",
    "session_id": "cert-levels-001"
  }'

# Gold level certificate
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the Gold level version. Same layout but with gold metallic accents and more ornate details.",
    "session_id": "cert-levels-001"
  }'
```

## Best Practices

### Design Guidelines
- **Typography**: Use elegant, readable fonts; script fonts for names, clean sans-serif for body text
- **Hierarchy**: Make recipient name the most prominent element
- **Balance**: Symmetrical layouts work best for formal certificates
- **Whitespace**: Leave adequate breathing room around elements
- **Color**: Use 2-3 colors maximum; gold/navy/burgundy convey prestige

### Content Recommendations
- **Clear Title**: State the certificate type prominently
- **Specific Achievement**: Include what was accomplished
- **Authority**: Add signatures and official seals
- **Verification**: Include certificate ID or QR code placeholder
- **Dates**: Always include issue date, expiration if applicable

### Technical Considerations
- **Resolution**: Request high resolution for print-quality output
- **Aspect Ratio**: Standard certificate ratios are landscape 4:3 or letter size
- **Text Placeholders**: Use clear placeholder text like "[Recipient Name]"
- **Logo Space**: Always include designated areas for organization logos

## Prompt Tips for Certificates

When creating certificates, include these details in your prompt:

1. **Certificate Type**: Completion, achievement, award, diploma, etc.
2. **Occasion/Purpose**: What is being recognized or certified
3. **Style**: Formal, modern, traditional, playful
4. **Color Scheme**: Specific colors or general palette
5. **Required Elements**: Name, date, signatures, seals, logos
6. **Organization Context**: Industry, formality level
7. **Special Features**: QR codes, security elements, badges

### Example Prompt Structure

```
"Create a [certificate type] certificate for [organization/purpose].
Style: [formal/modern/traditional].
Color scheme: [colors].
Include: [list of required elements].
Special features: [QR code, seal, badge, etc.]."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product and branding imagery
- `logo-generation` - Logo creation for certificates
