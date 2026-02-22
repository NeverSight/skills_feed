---
name: emoji-sticker-generation
description: Generate custom emoji and sticker packs using each::sense AI. Create personalized emoji from photos, expression packs, animated stickers, and platform-specific emoji sets for Slack, Discord, WhatsApp, and more.
metadata:
  author: eachlabs
  version: "1.0"
---

# Emoji & Sticker Generation

Generate custom emoji and sticker packs using each::sense. This skill creates personalized emoji from photos, animated stickers, expression packs, and platform-optimized emoji sets for messaging apps and team collaboration tools.

## Features

- **Photo to Emoji**: Transform photos into cartoon-style emoji
- **Expression Packs**: Generate emotion sets from a single reference
- **Animated Stickers**: Create moving emoji and GIF stickers
- **Platform Optimization**: Sized for Slack, Discord, WhatsApp, Telegram
- **Brand Mascots**: Design consistent mascot emoji sets
- **Pet Emoji**: Turn pet photos into adorable stickers
- **Bitmoji-Style**: Avatar-based emoji with consistent character
- **Reaction Sets**: Common reaction emoji with custom style

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cute cartoon emoji from this photo, suitable for Slack",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

## Platform Sizes & Formats

| Platform | Size | Format | Notes |
|----------|------|--------|-------|
| Slack | 128x128 | PNG, GIF | Square, transparent background |
| Discord | 128x128 | PNG, GIF | Max 256KB for animated |
| WhatsApp | 512x512 | WebP | Sticker packs, transparent BG |
| Telegram | 512x512 | WebP, TGS | Static or animated |
| iMessage | 300x300 | PNG, GIF | Various sizes supported |
| Teams | 128x128 | PNG | Square format |

## Use Case Examples

### 1. Custom Emoji from Photo

Create a personalized emoji from a portrait photo.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this photo into a cute cartoon emoji. Make it expressive with big eyes and a friendly smile. Style should be like modern emoji with clean lines and vibrant colors. Output at 512x512 with transparent background.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait.jpg"]
  }'
```

### 2. Emoji Expression Pack

Generate a complete set of expressions from one reference.

```bash
# Initial emoji creation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cartoon character emoji from this photo. I want to use this as a base for an expression pack.",
    "mode": "max",
    "session_id": "emoji-pack-001",
    "image_urls": ["https://example.com/face.jpg"]
  }'

# Generate expression variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create 6 expression variations of this character: happy, sad, laughing, surprised, angry, and thinking. Keep the same style and character design consistent across all expressions.",
    "mode": "max",
    "session_id": "emoji-pack-001"
  }'
```

### 3. Animated Emoji/Sticker

Create moving stickers with simple animations.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an animated emoji sticker of a cute waving hand. Make it loop smoothly with a friendly wave motion. Cartoon style with bold outlines, bright skin tone. Output as a short looping animation suitable for messaging apps.",
    "mode": "max"
  }'
```

### 4. Slack/Discord Emoji Set

Generate a custom emoji set for team workspaces.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a set of 5 custom Slack emoji for a tech startup: 1) Ship it rocket, 2) LGTM thumbs up, 3) Coffee break mug, 4) Bug squash, 5) Celebration party. Modern flat design style with bold colors. 128x128 pixels each with transparent backgrounds.",
    "mode": "max",
    "session_id": "slack-emoji-set"
  }'

# Add more to the set
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add 3 more emoji to the set in the same style: 1) Thinking face with code brackets, 2) PR approved checkmark, 3) Deploy success. Keep the same flat design aesthetic.",
    "mode": "max",
    "session_id": "slack-emoji-set"
  }'
```

### 5. WhatsApp Sticker Pack

Create a sticker pack optimized for WhatsApp.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a WhatsApp sticker pack with a cute cat character. Generate 8 stickers showing: greeting, thank you, love, laughing, sleeping, eating, confused, and celebrating. Kawaii anime style with pastel colors. 512x512 pixels with transparent background for each sticker.",
    "mode": "max"
  }'
```

### 6. Bitmoji-Style Avatar Emoji

Create a personalized avatar emoji set in Bitmoji style.

```bash
# Create avatar base
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Bitmoji-style avatar from this photo. Cartoon character with recognizable features but stylized. Clean vector-like art style similar to Bitmoji/Snapchat avatars.",
    "mode": "max",
    "session_id": "my-avatar-emoji",
    "image_urls": ["https://example.com/my-selfie.jpg"]
  }'

# Generate situational stickers
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 5 stickers of my avatar in different situations: 1) Working on laptop, 2) Drinking coffee, 3) High-fiving, 4) Mind blown gesture, 5) Dancing celebration. Same Bitmoji art style, keep my avatar consistent.",
    "mode": "max",
    "session_id": "my-avatar-emoji"
  }'
```

### 7. Brand Mascot Emoji Pack

Generate a consistent mascot emoji set for brand communications.

```bash
# Define mascot
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a brand mascot emoji: a friendly robot character with rounded features, blue and white color scheme, expressive LED eyes. This will be used for our tech company Slack and social media. Start with a neutral happy expression.",
    "mode": "max",
    "session_id": "brand-mascot-emoji"
  }'

# Generate mascot pack
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a complete emoji pack with this robot mascot showing: thumbs up, thinking, celebrating, waving hello, error/oops face, loading/processing, success checkmark pose, and question mark confused. Maintain exact same character design and brand colors.",
    "mode": "max",
    "session_id": "brand-mascot-emoji"
  }'
```

### 8. Reaction Emoji Set

Create custom reaction emoji for team or community use.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a set of 10 reaction emoji in a consistent playful illustrated style: 1) Fire/lit, 2) 100 percent, 3) Eyes looking, 4) Chef kiss, 5) Mind blown explosion, 6) Facepalm, 7) Clapping hands, 8) Raising hands celebration, 9) Laughing crying, 10) Heart eyes. Bold colors, clean outlines, 128x128 transparent PNG style.",
    "mode": "max"
  }'
```

### 9. Pet Emoji from Photo

Transform pet photos into adorable emoji stickers.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Turn this photo of my dog into a cute cartoon emoji sticker. Capture the personality and distinctive features. Kawaii style with big sparkly eyes and adorable expression. Create it as a 512x512 sticker with transparent background.",
    "mode": "max",
    "image_urls": ["https://example.com/my-dog.jpg"]
  }'

# Create pet expression pack
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 6 emoji variations of this dog: happy with tongue out, sleepy, begging for treats, playful with ball, confused head tilt, and excited jumping. Keep the same cartoon style consistent.",
    "mode": "max",
    "session_id": "pet-emoji-pack",
    "image_urls": ["https://example.com/my-dog.jpg"]
  }'
```

### 10. Text-Based Emoji Design

Create custom text and typography-based emoji.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create custom text emoji stickers for common team reactions: 1) NICE in rainbow gradient bubble letters, 2) SHIP IT with rocket trail effect, 3) WFH in cozy style with house icon, 4) BRB with clock elements, 5) TY in heart shape, 6) GG in gaming style. Each should be readable at 128x128 with transparent background, bold fun typography.",
    "mode": "max"
  }'
```

## Best Practices

### Emoji Design
- **Simplicity**: Keep designs simple and readable at small sizes
- **Bold Outlines**: Use thick outlines for clarity
- **Limited Colors**: Stick to 3-5 colors per emoji
- **Expressions**: Exaggerate facial expressions for impact
- **Consistency**: Maintain style across a pack

### Platform Optimization
- **Transparent Backgrounds**: Always use for best compatibility
- **Square Format**: Most platforms expect 1:1 aspect ratio
- **File Size**: Keep under 256KB for animated emoji
- **Test Small**: Preview at 32x32 to ensure readability

### Animation Tips
- **Loop Seamlessly**: Ensure animations loop smoothly
- **Keep it Short**: 1-3 seconds is ideal
- **Simple Motion**: Single motion reads better than complex
- **Frame Rate**: 10-15 FPS works well for emoji

## Prompt Tips for Emoji

When creating emoji, include these details:

1. **Style**: Cartoon, kawaii, flat design, 3D, etc.
2. **Expression/Emotion**: What feeling should it convey?
3. **Size**: Specify output dimensions
4. **Background**: Request transparent background
5. **Platform**: Mention target platform for optimization
6. **Consistency**: Reference previous generations for packs

### Example Prompt Structure

```
"Create a [style] emoji of [subject/expression].
[Visual details and characteristics].
Output at [size] with transparent background.
Target platform: [Slack/Discord/WhatsApp/etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final sticker packs, brand emoji | Slower | Highest |
| `eco` | Quick concepts, testing ideas, drafts | Faster | Good |

## Multi-Turn Pack Creation

Use `session_id` to build cohesive emoji packs:

```bash
# Start with character design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a cute mascot character for my emoji pack - a happy cloud with a face",
    "session_id": "cloud-emoji-project"
  }'

# Add expressions
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create this cloud with a rainy sad expression",
    "session_id": "cloud-emoji-project"
  }'

# Continue building the pack
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now make a sunny happy version with rainbow",
    "session_id": "cloud-emoji-project"
  }'
```

## Batch Generation for Packs

Generate complete packs efficiently:

```bash
# Generate full expression set in one request
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a complete emoji pack of 8 food emoji: pizza slice, hamburger, sushi, taco, ice cream cone, donut, coffee cup, and avocado. All in the same cute kawaii style with happy faces, consistent line weight and color palette. 128x128 each with transparent backgrounds.",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Inconsistent style | New session | Use same `session_id` for pack consistency |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product imagery
- `meta-ad-creative-generation` - Social media creatives
