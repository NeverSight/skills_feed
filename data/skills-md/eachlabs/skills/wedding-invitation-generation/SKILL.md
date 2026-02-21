---
name: wedding-invitation-generation
description: Generate beautiful wedding invitations, save the dates, RSVP cards, and wedding programs using each::sense AI. Create classic, modern, floral, rustic, destination, and cultural wedding stationery designs.
metadata:
  author: eachlabs
  version: "1.0"
---

# Wedding Invitation Generation

Generate stunning wedding invitations and stationery using each::sense. This skill creates custom designs for all wedding paper goods including invitations, save the dates, RSVP cards, programs, and digital e-invitations across various styles and cultural traditions.

## Features

- **Classic Elegant**: Timeless formal designs with traditional typography
- **Modern Minimalist**: Clean, contemporary designs with sleek aesthetics
- **Floral & Botanical**: Garden-inspired designs with flowers and greenery
- **Rustic & Bohemian**: Natural, organic designs with earthy elements
- **Destination Wedding**: Beach, vineyard, and travel-themed designs
- **Cultural Designs**: Indian, Chinese, Jewish, and other traditional styles
- **Save the Dates**: Pre-invitation announcements
- **RSVP Cards**: Response cards matching invitation suites
- **Wedding Programs**: Ceremony guides and order of service
- **Digital Invitations**: E-invites optimized for screens and sharing

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an elegant wedding invitation for Sarah and Michael, getting married on June 15th, 2025 at The Grand Estate. Classic formal style with gold accents on cream background.",
    "mode": "max"
  }'
```

## Wedding Stationery Formats & Sizes

| Type | Standard Size | Aspect Ratio | Use Case |
|------|---------------|--------------|----------|
| Invitation | 5x7 inches | 5:7 | Main wedding invitation |
| Invitation | 4x6 inches | 2:3 | Budget-friendly option |
| Save the Date | 4x6 inches | 2:3 | Pre-announcement cards |
| RSVP Card | 3.5x5 inches | 7:10 | Response cards |
| Program | 5x7 inches | 5:7 | Ceremony order of service |
| Digital Invite | 1080x1920 | 9:16 | Mobile-optimized e-invite |
| Digital Invite | 1080x1080 | 1:1 | Social media square format |

## Use Case Examples

### 1. Classic Elegant Invitation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a classic elegant wedding invitation for Emma Rose Thompson and William James Harrison. Wedding date: Saturday, September 20th, 2025 at five o clock in the evening. Venue: The Ritz-Carlton Ballroom, New York City. Design style: Traditional formal with elegant script typography, gold foil accents on ivory paper, delicate filigree border, refined and timeless aesthetic. Size: 5x7 inches portrait orientation.",
    "mode": "max"
  }'
```

### 2. Modern Minimalist Invitation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern minimalist wedding invitation for Olivia Chen and James Park. Date: March 8, 2025. Venue: The Modern Art Museum, Los Angeles. Design: Ultra clean and contemporary, lots of white space, sans-serif typography, subtle geometric accents, black text on white background with a single thin gold line accent. Sophisticated and understated. 5x7 portrait format.",
    "mode": "max"
  }'
```

### 3. Floral & Botanical Invitation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a romantic floral wedding invitation for Isabella Martinez and David Wilson. Date: April 12, 2025 at 4 PM. Venue: Botanical Gardens, Charleston. Design: Lush watercolor flowers - peonies, roses, and eucalyptus in soft blush pink, dusty rose, and sage green. Romantic script font for names, elegant serif for details. Flowers framing the corners with a soft cream background. Garden party elegance. 5x7 portrait.",
    "mode": "max"
  }'
```

### 4. Rustic Bohemian Invitation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a rustic bohemian wedding invitation for Luna Rivers and Jack Morrison. Date: October 18, 2025 at 3 PM. Venue: Willow Creek Ranch, Colorado. Design: Earthy boho style with kraft paper texture background, wildflowers and dried pampas grass illustrations, warm terracotta and burnt orange tones with sage green accents. Hand-drawn style typography, dreamcatcher or feather subtle motifs. Natural and free-spirited vibe. 5x7 portrait.",
    "mode": "max"
  }'
```

### 5. Beach Destination Wedding Invitation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a destination beach wedding invitation for Sophia and Ryan. Date: January 25, 2025 at sunset. Venue: Four Seasons Resort, Maui, Hawaii. Design: Tropical paradise theme with soft watercolor ocean waves, palm fronds, and tropical flowers. Color palette of ocean blue, turquoise, coral, and sandy gold. Elegant but relaxed typography. Include small icons for flip flops or starfish. Vacation vibes meets wedding elegance. 5x7 portrait.",
    "mode": "max"
  }'
```

### 6. Indian Wedding Invitation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a traditional Indian wedding invitation for Priya Sharma and Raj Patel. Mehendi: December 12, Sangeet: December 13, Wedding: December 14, 2025. Venue: The Leela Palace, Jaipur. Design: Rich and ornate traditional Indian style with intricate mandala patterns, paisley motifs, and Ganesha symbol. Deep royal colors - maroon, gold, and emerald green. Ornate gold borders and traditional Indian decorative elements. Blend of Hindi and English text welcome. Luxurious and celebratory. 5x7 portrait.",
    "mode": "max"
  }'
```

### 7. Save the Date Card

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a save the date card for Amanda and Chris. Save the date: July 4th, 2025. Location: Napa Valley, California. Formal invitation to follow. Design: Wine country theme with subtle grapevine illustrations and vineyard landscape silhouette. Elegant purple and gold color scheme. The date should be prominently displayed. Include a placeholder area for a photo of the couple. Romantic and sophisticated. 4x6 landscape orientation.",
    "mode": "max",
    "session_id": "wedding-suite-amanda-chris"
  }'
```

### 8. RSVP Card Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching RSVP card for the same wedding suite. Include: Kindly respond by June 1st, 2025. Fields for: Name line, Number of guests attending, Meal choice checkboxes (Beef, Fish, Vegetarian), Song request line. Same wine country vineyard style with grapevine accents matching the save the date. 3.5x5 inches portrait orientation.",
    "mode": "max",
    "session_id": "wedding-suite-amanda-chris"
  }'
```

### 9. Wedding Program

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a wedding ceremony program for Katherine and Thomas. Date: August 23, 2025. Include sections for: Order of Ceremony (Processional, Welcome, Readings, Vows, Ring Exchange, Kiss, Recessional), Wedding Party (list bridesmaids and groomsmen names), Thank You message. Design: Classic elegant style with a monogram KT at the top, delicate border, cream and navy blue color scheme, traditional serif typography. 5x7 portrait, bifold style front cover.",
    "mode": "max"
  }'
```

### 10. Digital E-Invitation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital wedding e-invitation optimized for mobile sharing. Couple: Jessica and Daniel. Date: November 15, 2025 at 6 PM. Venue: The Glasshouse, Chicago. Design: Modern and animated-ready with elegant motion-friendly elements, sparkle and shimmer effects areas, bold readable typography for small screens. Black and champagne gold color scheme, art deco inspired geometric patterns. Format: 9:16 vertical for Instagram stories and WhatsApp. Include RSVP website URL placeholder at bottom.",
    "mode": "max"
  }'
```

## Best Practices

### Design Elements
- **Typography**: Use 2-3 complementary fonts maximum - script for names, serif/sans-serif for details
- **Hierarchy**: Names largest, date and venue prominent, additional details smaller
- **White Space**: Leave breathing room - avoid cluttered designs
- **Color Palette**: Stick to 2-4 colors that complement each other
- **Consistency**: Match all pieces in your stationery suite

### Text Content
- **Names**: Full formal names for traditional, first names only for casual
- **Date Format**: Spell out for formal (Saturday, the fifteenth of June), numeric for modern (06.15.2025)
- **Time**: Written out for formal (at five o'clock in the evening), numeric for modern (5:00 PM)
- **Venue**: Full name and city, detailed address on separate card

### Cultural Considerations
- **Religious Symbols**: Include appropriately (cross, Star of David, Ganesha, etc.)
- **Language**: Bilingual invitations for multicultural weddings
- **Traditions**: Incorporate cultural motifs and color symbolism
- **Multi-Event**: Indian weddings often have multiple events (Mehendi, Sangeet, etc.)

## Prompt Tips for Wedding Invitations

When creating wedding invitation designs, include these details:

1. **Couple Names**: Full names as they should appear
2. **Date & Time**: Complete date, day of week, and time
3. **Venue**: Full venue name and location
4. **Style**: Classic, modern, rustic, bohemian, etc.
5. **Color Palette**: Specific colors or general mood
6. **Motifs**: Flowers, geometric, cultural symbols
7. **Format**: Size and orientation (5x7 portrait, etc.)
8. **Stationery Type**: Invitation, save the date, RSVP, program

### Example Prompt Structure

```
"Create a [style] wedding [stationery type] for [names].
Date: [full date and time].
Venue: [venue name and location].
Design: [detailed description of colors, motifs, typography].
Format: [size and orientation]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final print-ready designs, professional quality | Slower | Highest |
| `eco` | Quick drafts, concept exploration, comparing styles | Faster | Good |

## Multi-Turn Design Iteration

Use `session_id` to iterate on designs or create matching suites:

```bash
# Initial invitation design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a romantic garden wedding invitation for Emily and Robert, June wedding at Rose Garden Estate. Soft pink and green floral design.",
    "session_id": "emily-robert-wedding"
  }'

# Request design revision
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I love it but can you make the flowers more prominent and add some gold accents to the text?",
    "session_id": "emily-robert-wedding"
  }'

# Create matching suite pieces
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching RSVP card and a details card with the same floral design style",
    "session_id": "emily-robert-wedding"
  }'
```

## Creating Complete Wedding Suites

Generate all matching stationery pieces:

```bash
# Save the Date
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create save the date for Nicole and Mark, December 2025 wedding in Aspen. Winter wonderland theme with snow and evergreens.",
    "mode": "max",
    "session_id": "nicole-mark-winter-wedding"
  }'

# Main Invitation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the main wedding invitation matching the save the date style. December 20, 2025 at 5 PM, The Little Nell, Aspen Colorado.",
    "mode": "max",
    "session_id": "nicole-mark-winter-wedding"
  }'

# RSVP Card
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create matching RSVP card with meal choices and song request.",
    "mode": "max",
    "session_id": "nicole-mark-winter-wedding"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product photography for wedding items
- `social-media-content-generation` - Wedding social media posts
