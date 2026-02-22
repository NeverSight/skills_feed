---
name: flyer-design-generation
description: Generate professional flyers and leaflets using each::sense AI. Create event flyers, promotional materials, real estate listings, restaurant menus, and more with eye-catching designs optimized for print and digital distribution.
metadata:
  author: eachlabs
  version: "1.0"
---

# Flyer Design Generation

Generate professional flyers and leaflets using each::sense. This skill creates visually compelling designs for events, promotions, real estate, food service, fitness, and more - optimized for both print and digital distribution.

## Features

- **Event Flyers**: Party invitations, concert announcements, festival promotions
- **Business Promotional**: Company services, product launches, brand awareness
- **Real Estate Listings**: Property showcases, open house announcements
- **Restaurant & Food**: Menu highlights, special offers, grand opening
- **Fitness & Gym**: Membership drives, class schedules, transformation challenges
- **Sale & Discount**: Seasonal sales, clearance events, limited-time offers
- **Recruitment**: Job fairs, hiring events, career opportunities
- **Community Events**: Fundraisers, local gatherings, charity events

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a flyer for a summer music festival featuring EDM and house music, vibrant neon colors, date August 15-17, include space for artist lineup",
    "mode": "max"
  }'
```

## Common Flyer Sizes

| Format | Dimensions | Use Case |
|--------|------------|----------|
| Letter | 8.5x11 in (2550x3300 px) | Standard US flyer, handouts |
| A4 | 210x297 mm (2480x3508 px) | Standard international flyer |
| A5 | 148x210 mm (1748x2480 px) | Half-page flyer, inserts |
| Square | 1080x1080 px | Social media, digital ads |
| 4x6 | 4x6 in (1200x1800 px) | Postcards, small handouts |
| 11x17 | 11x17 in (3300x5100 px) | Posters, large format |

## Use Case Examples

### 1. Event Flyer (Party/Concert)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a nightclub party flyer for a New Years Eve celebration. Dark background with gold and silver confetti, champagne glasses, disco ball. Bold typography space for event name at top, date December 31st, include areas for DJ names and venue details at bottom. Luxurious and exciting vibe.",
    "mode": "max"
  }'
```

### 2. Business Promotional Flyer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional business flyer for a digital marketing agency. Clean modern design with blue and white color scheme. Include sections for services offered (SEO, Social Media, PPC), company logo placeholder at top, contact information area at bottom. Corporate but approachable style.",
    "mode": "max"
  }'
```

### 3. Real Estate Listing Flyer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a real estate listing flyer for a luxury home. Feature a beautiful modern house exterior with manicured lawn. Include prominent OPEN HOUSE banner, space for price, 4 bed 3 bath icons, square footage area, agent photo placeholder and contact details. Elegant and trustworthy design with navy and gold accents.",
    "mode": "max"
  }'
```

### 4. Restaurant/Food Flyer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a restaurant flyer for an Italian pizzeria. Show a delicious wood-fired pizza with melted cheese and fresh basil. Warm rustic background with Italian flag colors subtly incorporated. Space for restaurant name, special offer (Buy 1 Get 1 Free), menu highlights, and location/phone number. Appetizing and authentic feel.",
    "mode": "max"
  }'
```

### 5. Fitness/Gym Flyer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a gym membership flyer with high energy design. Show athletic person working out with weights, dynamic pose. Bold red and black color scheme. Large JOIN NOW text, space for membership pricing tiers, list of amenities (24/7 access, personal training, group classes), QR code placeholder for sign-up. Motivational and powerful aesthetic.",
    "mode": "max"
  }'
```

### 6. Sale/Discount Flyer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a retail sale flyer for a Black Friday event. Dramatic black background with explosive gold and red accents. Giant UP TO 70% OFF text, countdown urgency elements, shopping bags and gift boxes imagery. Space for store name, sale dates November 24-27, and store hours. Eye-catching and urgent design that demands attention.",
    "mode": "max"
  }'
```

### 7. Job Fair/Recruitment Flyer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a job fair flyer for a tech industry hiring event. Modern professional design with diverse group of business people silhouettes. Tech-inspired background with circuit patterns. WE ARE HIRING headline, list space for participating companies, event date and venue, registration QR code area. Professional blue and green gradient color scheme.",
    "mode": "max"
  }'
```

### 8. Community Event Flyer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a community charity fundraiser flyer for a local food bank. Warm and welcoming design with volunteers helping distribute food. Soft orange and green earth tones. HELP US FEED FAMILIES headline, donation goal thermometer graphic, event details section, sponsor logo placeholders at bottom. Compassionate and community-focused design.",
    "mode": "max"
  }'
```

### 9. Grand Opening Flyer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a grand opening flyer for a new coffee shop. Celebratory design with ribbon cutting imagery, coffee beans and steam. GRAND OPENING with date prominently displayed. Include first 100 customers get free coffee offer, store address, opening hours, and social media handles area. Warm brown and cream color palette with pops of festive gold.",
    "mode": "max"
  }'
```

### 10. Holiday/Seasonal Flyer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Christmas holiday sale flyer for a retail store. Festive winter wonderland design with snowflakes, Christmas trees, and wrapped presents. Red and green traditional colors with elegant gold accents. HOLIDAY SALE UP TO 50% OFF headline, space for featured products, store location and extended holiday hours. Magical and joyful atmosphere.",
    "mode": "max"
  }'
```

## Best Practices

### Visual Hierarchy
- **Headline**: Make it large, bold, and immediately readable
- **Key Information**: Date, time, location should be easy to find
- **Call to Action**: Clear next step (Call Now, Visit Us, Register)
- **Contact Details**: Phone, website, address, social media

### Design Principles
- **Contrast**: Ensure text is readable against backgrounds
- **White Space**: Do not overcrowd - let the design breathe
- **Brand Consistency**: Use consistent colors and fonts
- **Image Quality**: Request high-resolution outputs for print

### Print vs Digital
- **Print**: Request higher resolution (300 DPI equivalent), include bleed areas
- **Digital**: Optimize for screen viewing, consider file size
- **Both**: Design with versatility in mind

## Prompt Tips for Flyer Design

When creating flyers, include these details in your prompt:

1. **Purpose**: What is the flyer promoting?
2. **Audience**: Who will see this flyer?
3. **Key Message**: What is the main headline or offer?
4. **Visual Elements**: Imagery, icons, or graphics needed
5. **Color Scheme**: Brand colors or mood-based palette
6. **Text Areas**: Space for specific text content
7. **Format**: Print size or digital dimensions
8. **Style**: Professional, fun, elegant, urgent, etc.

### Example Prompt Structure

```
"Create a [purpose] flyer for [business/event].
[Visual description] with [color scheme].
Include [headline text], space for [content areas].
Target audience: [demographic].
Style: [mood/aesthetic]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final print-ready flyers, client deliverables | Slower | Highest |
| `eco` | Quick drafts, concept exploration, variations | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on flyer designs:

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a summer beach party flyer with tropical vibes",
    "session_id": "beach-party-flyer-001"
  }'

# Request modifications
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the colors more vibrant and add palm tree silhouettes on the sides",
    "session_id": "beach-party-flyer-001"
  }'

# Generate variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations - one with sunset colors and one with neon night theme",
    "session_id": "beach-party-flyer-001"
  }'
```

## Batch Generation for A/B Testing

Generate multiple design variations:

```bash
# Version A - Bold and colorful
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a yoga studio flyer - bold colorful design with energetic sunrise theme",
    "mode": "eco"
  }'

# Version B - Minimalist and calm
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a yoga studio flyer - minimalist zen design with soft neutral colors",
    "mode": "eco"
  }'

# Version C - Nature focused
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a yoga studio flyer - outdoor nature theme with forest and mountains",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to remove restricted elements |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Social media ad creatives
- `product-photo-generation` - E-commerce product shots
- `poster-design-generation` - Large format poster designs
