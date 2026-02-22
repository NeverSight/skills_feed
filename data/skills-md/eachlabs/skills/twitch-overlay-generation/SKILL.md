---
name: twitch-overlay-generation
description: Generate Twitch and streaming overlays using each::sense AI. Create webcam frames, starting soon screens, BRB screens, alerts, chat boxes, panels, emotes, subscriber badges, and channel banners optimized for streaming platforms.
metadata:
  author: eachlabs
  version: "1.0"
---

# Twitch Overlay Generation

Generate professional streaming overlays and graphics using each::sense. This skill creates images optimized for Twitch, YouTube Gaming, and other streaming platforms.

## Features

- **Webcam Frames**: Custom borders and frames for webcam placement
- **Starting Soon Screens**: Countdown and pre-stream graphics
- **BRB Screens**: Be right back intermission graphics
- **Stream Ending Screens**: Outro and ending sequence graphics
- **Alert Graphics**: Follow, subscribe, donation, and raid alerts
- **Chat Box Frames**: Styled chat overlay containers
- **Twitch Panels**: Channel panel graphics for about, schedule, rules, etc.
- **Emotes**: Custom Twitch emotes for channel subscribers
- **Subscriber Badges**: Tiered loyalty badges for subscribers
- **Channel Banners**: Profile banners and offline screens

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cyberpunk themed webcam frame with neon purple and blue colors, futuristic tech elements, transparent center for the webcam",
    "mode": "max"
  }'
```

## Streaming Overlay Formats & Sizes

| Asset Type | Size | Format | Use Case |
|------------|------|--------|----------|
| Webcam Frame | 1920x1080 | PNG (transparent) | Overlay on stream layout |
| Starting Soon | 1920x1080 | PNG/MP4 | Pre-stream display |
| BRB Screen | 1920x1080 | PNG/MP4 | Break screen |
| Stream Ending | 1920x1080 | PNG/MP4 | End of stream |
| Alert Graphics | 400x400 | PNG (transparent) | On-screen notifications |
| Chat Box Frame | 400x600 | PNG (transparent) | Chat overlay container |
| Twitch Panel | 320x160 | PNG | Channel info panels |
| Emote | 112x112, 56x56, 28x28 | PNG (transparent) | Chat emotes |
| Sub Badge | 72x72, 36x36, 18x18 | PNG (transparent) | Subscriber badges |
| Channel Banner | 1200x480 | PNG | Profile banner |
| Offline Screen | 1920x1080 | PNG | When stream is offline |

## Use Case Examples

### 1. Stream Overlay with Webcam Frame

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1920x1080 stream overlay with a webcam frame in the bottom right corner. Gaming theme with dark purple and gold accents. Include decorative borders, transparent center for webcam, and space for recent events on the left side. Modern esports aesthetic.",
    "mode": "max"
  }'
```

### 2. Starting Soon Screen

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1920x1080 Starting Soon screen for a gaming stream. Neon synthwave theme with retro grid, glowing text area for STARTING SOON, animated feel with light rays and particles. Include space for social media handles at the bottom. Pink, purple, and cyan color scheme.",
    "mode": "max"
  }'
```

### 3. BRB (Be Right Back) Screen

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1920x1080 BRB screen for Twitch. Cozy lo-fi aesthetic with warm colors, include a cute animated coffee cup or snack visual. Text space for BE RIGHT BACK in stylized font. Soft lighting, relaxing vibes. Include subtle chat reminder at bottom.",
    "mode": "max"
  }'
```

### 4. Stream Ending Screen

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1920x1080 stream ending screen. Thanks for watching theme with space for STREAM ENDED or THANKS FOR WATCHING text. Include areas for social media icons/handles, next stream schedule, and a follow reminder. Dark elegant theme with gold accents and particle effects.",
    "mode": "max"
  }'
```

### 5. Alert Graphics (Follow, Sub, Donation)

```bash
# Follow Alert
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 400x400 transparent PNG follow alert graphic for Twitch. Cute anime-style character celebrating with confetti and sparkles. Include a heart icon and space for NEW FOLLOWER text. Vibrant colors, kawaii aesthetic.",
    "session_id": "alert-set-001",
    "mode": "max"
  }'

# Subscribe Alert (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching 400x400 subscribe alert. Same style as the follow alert but with a star icon and more elaborate celebration effects. Space for NEW SUB text.",
    "session_id": "alert-set-001",
    "mode": "max"
  }'

# Donation Alert
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching 400x400 donation/tip alert. Same style with coin or money effects, extra sparkle and celebration. Space for donation amount text.",
    "session_id": "alert-set-001",
    "mode": "max"
  }'
```

### 6. Chat Box Frame

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 400x600 transparent chat box frame overlay. Cyberpunk tech theme with glowing border edges, circuit board patterns. Mostly transparent center where chat will display. Include a small CHAT header area at top. Neon green and black color scheme.",
    "mode": "max"
  }'
```

### 7. Twitch Panel Graphics

```bash
# About Panel
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 320x160 Twitch panel graphic for an ABOUT ME section. Clean modern design with the text ABOUT ME. Dark background with gradient accent, gaming controller or headset icon. Professional streamer aesthetic.",
    "session_id": "panel-set-001",
    "mode": "max"
  }'

# Schedule Panel
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching 320x160 SCHEDULE panel. Same style as previous with calendar icon. Text says SCHEDULE.",
    "session_id": "panel-set-001",
    "mode": "max"
  }'

# Rules Panel
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching 320x160 RULES panel. Same style with a book or list icon.",
    "session_id": "panel-set-001",
    "mode": "max"
  }'
```

### 8. Twitch Emote Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 112x112 Twitch emote. A cute cat face with heart eyes, chibi/kawaii style. Expressive, bold lines, vibrant colors that pop against dark backgrounds. Transparent background. The emote should be readable at small sizes.",
    "mode": "max"
  }'

# Emote variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a set of 3 Twitch emotes at 112x112 each: 1) Pog/excited face, 2) Sad/cry face, 3) Laugh/LUL face. All featuring a cute frog character, consistent style across all three. Bold outlines, expressive features, transparent backgrounds.",
    "mode": "max"
  }'
```

### 9. Subscriber Badges

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a set of 6 Twitch subscriber badges at 72x72 pixels each, tiered progression for 1 month, 3 months, 6 months, 1 year, 2 years, and 3 years. Theme: crystal/gem progression from small rough gem to elaborate crown jewel. Each tier more detailed and prestigious. Transparent backgrounds, clear at small sizes.",
    "mode": "max"
  }'

# Alternative badge style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 6 subscriber loyalty badges, 72x72 pixels. Military rank progression theme: bronze star (1mo), silver star (3mo), gold star (6mo), bronze medal (1yr), silver medal (2yr), gold medal with laurels (3yr). Clear iconography, readable at 18x18 size, transparent backgrounds.",
    "mode": "max"
  }'
```

### 10. Channel Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1200x480 Twitch channel banner. Epic gaming scene with dramatic lighting, mountain landscape with fantasy elements. Space on the right side for channel name text. Color scheme: deep blues and purples with orange accent lighting. Cinematic, high quality.",
    "mode": "max"
  }'

# Offline Screen
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1920x1080 Twitch offline screen. Cozy nighttime scene with a gaming setup, monitors off, ambient lighting from RGB peripherals. Text space for CURRENTLY OFFLINE and social media handles. Moody atmospheric lighting, lo-fi aesthetic.",
    "mode": "max"
  }'
```

## Best Practices

### Overlay Design
- **Transparency**: Request PNG with transparent backgrounds for overlays
- **Safe Zones**: Keep important elements away from edges (Twitch UI covers corners)
- **Readability**: Ensure text is readable on various game backgrounds
- **Consistency**: Use session_id to maintain style across overlay sets
- **Color Contrast**: Use colors that stand out but do not distract from gameplay

### Emotes & Badges
- **Bold Lines**: Use thick outlines for visibility at small sizes
- **Simple Designs**: Less detail works better at 28x28 and 18x18 sizes
- **Test Sizes**: Request all size variants or design for the smallest size
- **Expression First**: Emotes should convey emotion instantly

### Screen Graphics
- **Brand Consistency**: Maintain colors and style across all screens
- **Text Hierarchy**: Make primary text (Starting Soon, BRB) most prominent
- **Social Integration**: Include space for social media handles
- **Animation-Ready**: Design with potential animation in mind

## Prompt Tips for Streaming Graphics

When creating streaming overlays, include these details:

1. **Dimensions**: Specify exact pixel dimensions
2. **Theme**: Gaming genre, aesthetic (cyberpunk, cozy, anime, etc.)
3. **Colors**: Primary and accent colors that match your brand
4. **Transparency**: Specify if you need transparent background
5. **Text Space**: Where text/logos will be placed
6. **Style Reference**: Esports, cozy, retro, minimal, etc.
7. **Platform**: Twitch, YouTube, or multi-platform

### Example Prompt Structure

```
"Create a [dimensions] [asset type] for [platform].
[Theme/aesthetic] with [color scheme].
Include [specific elements] and space for [text/overlays].
[Transparency requirements]. [Style reference]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production overlays, emote sets, brand assets | Slower | Highest |
| `eco` | Quick concepts, drafts, style exploration | Faster | Good |

## Multi-Turn Overlay Set Creation

Use `session_id` to create cohesive overlay packages:

```bash
# Create base style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a webcam frame with a Japanese cherry blossom theme, soft pink and white colors, elegant minimal design",
    "session_id": "sakura-overlay-set"
  }'

# Create matching starting soon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching Starting Soon screen in the same cherry blossom style",
    "session_id": "sakura-overlay-set"
  }'

# Create matching BRB screen
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching BRB screen, same aesthetic with falling petals",
    "session_id": "sakura-overlay-set"
  }'

# Create matching alerts
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create follow and subscribe alerts matching this cherry blossom theme",
    "session_id": "sakura-overlay-set"
  }'
```

## Complete Overlay Package Example

Generate a full streaming package in one session:

```bash
# Initialize the package style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I am creating a complete Twitch overlay package. Theme: Cyberpunk Neon City. Colors: Hot pink, electric blue, purple. Style: Futuristic, glowing edges, holographic elements. Start with the main webcam overlay frame at 1920x1080.",
    "session_id": "cyberpunk-package",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with platform guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Inconsistent style | No session_id | Use session_id for multi-asset generation |

## Related Skills

- `each-sense` - Core API documentation
- `emote-generation` - Specialized emote creation
- `brand-kit-generation` - Complete brand identity packages
- `animated-overlay-generation` - Animated/video overlays
