---
name: meme-generation
description: Generate memes using each::sense AI. Create classic meme templates, custom memes, brand memes, reaction memes, comparison memes, trending formats, and more for social media, marketing, and entertainment.
metadata:
  author: eachlabs
  version: "1.0"
---

# Meme Generation

Generate viral-worthy memes using each::sense. This skill creates images optimized for social media sharing, brand marketing, workplace humor, and internet culture engagement.

## Features

- **Classic Templates**: Generate images in popular meme formats (Drake, Distracted Boyfriend, etc.)
- **Custom Memes**: Create original meme images from any prompt
- **Brand Memes**: Marketing-friendly memes that maintain brand voice
- **Reaction Memes**: Expressive images for social media responses
- **Comparison Memes**: Side-by-side or before/after formats
- **Trending Formats**: Current viral meme styles and formats
- **Text Overlay Memes**: Images with integrated meme text
- **Multi-Panel Memes**: Comic-strip style sequential panels
- **Corporate/Workplace Memes**: Office humor and professional satire
- **Industry-Specific Memes**: Niche humor for specific communities

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme about developers when the code works on the first try - shocked and suspicious expression",
    "mode": "max"
  }'
```

## Meme Formats & Styles

| Format | Description | Best For |
|--------|-------------|----------|
| Classic Template | Recognizable meme formats | Maximum shareability |
| Reaction Image | Expressive faces/situations | Social media replies |
| Comparison | Side-by-side panels | Before/after, expectations vs reality |
| Multi-Panel | 2-4 panel sequences | Storytelling, escalation humor |
| Text Overlay | Large impact text on image | Direct, punchy jokes |
| Surreal/Abstract | Absurdist imagery | Gen-Z humor, niche communities |

## Use Case Examples

### 1. Classic Meme Template Generation

Generate images in the style of popular meme templates.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme image in the style of the Drake meme format. Two panels vertically stacked. Top panel: a person looking away dismissively with hand up rejecting something. Bottom panel: same person smiling and pointing approvingly. Clean white background, expressive poses.",
    "mode": "max"
  }'
```

### 2. Custom Meme from Prompt

Create an original meme image from a creative concept.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme image of a cat sitting at a computer desk looking extremely confused at the screen, office setting, dramatic lighting from the monitor, the cat has reading glasses on. Funny and relatable vibe for when you receive a confusing email.",
    "mode": "max"
  }'
```

### 3. Brand Meme Marketing

Create memes suitable for brand social media accounts.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a clean, brand-safe meme image for a coffee company social media. Show a person dramatically hugging a giant coffee cup like it is their best friend. Office morning setting, humorous but professional enough for brand use. Warm, inviting colors.",
    "mode": "max"
  }'
```

### 4. Reaction Meme

Generate expressive images for social media reactions.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a reaction meme image of a person with an extremely exaggerated surprised face, eyes wide, jaw dropped, hands on cheeks. Simple background, highly expressive, perfect for replying to shocking news or announcements online.",
    "mode": "max"
  }'
```

### 5. Comparison Meme

Create side-by-side comparison format memes.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a two-panel comparison meme image. Left panel labeled area for expectation: a person confidently presenting at a meeting looking professional. Right panel labeled area for reality: the same person nervously fumbling with papers, coffee spilled, chaotic scene. Corporate office setting.",
    "mode": "max"
  }'
```

### 6. Trending Format Meme

Generate memes in currently popular viral styles.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme image in the style of the woman yelling at cat meme format. Left side: an angry woman pointing and yelling expressively at a dinner table. Right side: a confused white cat sitting at a table with a plate in front of it, looking bewildered. Split panel format.",
    "mode": "max"
  }'
```

### 7. Text Overlay Meme

Create images designed for bold text overlays.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme background image of a galaxy brain or expanding brain concept. Show a person in meditation pose with a glowing, oversized brain emanating light and energy. Cosmic background with stars. Leave clear space at top and bottom for impact font text overlay.",
    "mode": "max"
  }'
```

### 8. Multi-Panel Meme

Generate comic-strip style sequential memes.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4-panel meme comic strip. Panel 1: person calmly saying they will just check one email. Panel 2: person still at computer, slightly concerned. Panel 3: person surrounded by multiple screens, stressed. Panel 4: person collapsed at desk, it is now nighttime. Office setting, escalating chaos.",
    "mode": "max",
    "session_id": "multi-panel-meme-001"
  }'
```

### 9. Corporate/Workplace Meme

Create office humor memes for professional contexts.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a workplace meme image. Scene: a meeting room with a person presenting a very simple obvious solution on a whiteboard while everyone else at the table looks shocked and amazed as if it is genius. Exaggerated reactions, corporate office setting, humorous take on overthinking simple problems.",
    "mode": "max"
  }'
```

### 10. Industry-Specific Meme

Generate memes for niche professional communities.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a programmer/developer meme image. A developer sitting at a desk surrounded by multiple monitors showing code, but they are intensely focused on a tiny bug that is literally represented as a small cartoon bug on the screen. The bug is tiny but the developer is using a magnifying glass. Dramatic lighting, humorous debugging scene.",
    "mode": "max"
  }'
```

## Best Practices

### Creating Shareable Memes

- **Clear Composition**: Keep the main subject prominent and uncluttered
- **Expressive Faces**: Exaggerated expressions work best for reaction memes
- **Text Space**: Leave room for impact font overlays when needed
- **Universal Humor**: Aim for broadly relatable situations
- **High Contrast**: Ensure the image reads well at small sizes (mobile feeds)

### Brand Meme Guidelines

- **Stay On-Brand**: Humor should align with brand voice
- **Avoid Controversy**: Steer clear of divisive topics
- **Timely but Timeless**: Balance trending formats with lasting appeal
- **Quality Over Quantity**: One great meme beats ten mediocre ones
- **Know Your Audience**: Different platforms have different humor styles

### Technical Tips

- **Square Format (1:1)**: Best for Instagram, Twitter, Facebook
- **Vertical (4:5 or 9:16)**: Better for Stories, TikTok, mobile feeds
- **Resolution**: Aim for at least 1080px on the shortest side
- **File Size**: Keep reasonable for fast loading

## Prompt Tips for Memes

When creating meme images, include these details:

1. **Format**: Specify panel layout (single, two-panel, four-panel, etc.)
2. **Expression**: Describe the emotional expression clearly
3. **Setting**: Where does the scene take place?
4. **Style**: Realistic, cartoon, surreal, etc.
5. **Text Space**: Request areas for text overlay if needed
6. **Context**: What situation is this meme depicting?

### Example Prompt Structure

```
"Create a [format] meme image. [Scene description] with [expression/action].
[Setting details]. [Style preferences].
[Text space requirements if any]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final memes, high-engagement posts, brand content | Slower | Highest |
| `eco` | Quick drafts, A/B testing concepts, bulk generation | Faster | Good |

## Multi-Turn Meme Iteration

Use `session_id` to iterate on meme concepts:

```bash
# Initial meme concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme of a dog at a computer looking frustrated",
    "session_id": "meme-project-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the dog expression more dramatic, add coffee cup for extra relatability",
    "session_id": "meme-project-001"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cat version of the same meme for comparison",
    "session_id": "meme-project-001"
  }'
```

## Meme Series Generation

Generate multiple related memes for a campaign:

```bash
# Meme 1 - Monday mood
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a weekday mood meme - Monday: exhausted office worker barely awake at desk",
    "mode": "eco",
    "session_id": "weekday-series"
  }'

# Meme 2 - Friday mood (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Same style but Friday: the same worker now energetic and celebrating, leaving the office",
    "mode": "eco",
    "session_id": "weekday-series"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt - avoid offensive, harmful, or inappropriate content |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `image-generation` - General image generation
- `product-visuals` - Product photography and marketing visuals
- `meta-ad-creative-generation` - Social media ad creatives
