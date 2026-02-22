---
name: discord-graphics-generation
description: Generate Discord server graphics using each::sense AI. Create server icons, banners, role icons, welcome graphics, event banners, bot avatars, emojis, and more optimized for Discord's format requirements.
metadata:
  author: eachlabs
  version: "1.0"
---

# Discord Graphics Generation

Generate professional Discord server graphics using each::sense. This skill creates images optimized for Discord's various graphic placements, sizes, and best practices.

## Features

- **Server Icons**: Square icons for server identity (512x512)
- **Server Banners**: Wide banners for server profile (960x540)
- **Role Icons**: Small icons for role identification (64x64)
- **Welcome Graphics**: Channel headers for welcome areas
- **Rules Graphics**: Visual headers for rules channels
- **Announcement Banners**: Eye-catching announcement graphics
- **Event Banners**: Promotional graphics for server events
- **Bot Avatars**: Custom avatars for Discord bots
- **Emoji Packs**: Custom server emojis
- **Booster Badges**: Recognition graphics for server boosters

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Discord server icon for a gaming community called Pixel Warriors, featuring a pixel art sword and shield with purple and blue colors",
    "mode": "max"
  }'
```

## Discord Graphics Formats & Sizes

| Asset Type | Size | Aspect Ratio | Use Case |
|------------|------|--------------|----------|
| Server Icon | 512x512 | 1:1 | Server identity, appears everywhere |
| Server Banner | 960x540 | 16:9 | Server profile header (Nitro Level 2+) |
| Role Icon | 64x64 | 1:1 | Role badges next to usernames |
| Invite Splash | 1920x1080 | 16:9 | Server invite background (Nitro Level 1+) |
| Server Discovery | 1024x1024 | 1:1 | Server discovery listing |
| Custom Emoji | 128x128 | 1:1 | Server emojis (max 256KB) |
| Sticker | 320x320 | 1:1 | Custom stickers |

## Use Case Examples

### 1. Discord Server Icon

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 512x512 Discord server icon for a tech community called CodeHub. Feature a modern code bracket symbol with gradient from cyan to purple, dark background, clean minimal design that reads well at small sizes.",
    "mode": "max"
  }'
```

### 2. Server Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 960x540 Discord server banner for an anime discussion community. Show a stylish anime-inspired cityscape at night with neon lights, purple and pink color scheme. Leave the center area less busy for the server name overlay.",
    "mode": "max"
  }'
```

### 3. Role Icons Set

```bash
# Admin role icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 Discord role icon for Admin role. Gold crown symbol on dark background, simple and recognizable at small size. Clean vector-style design.",
    "session_id": "discord-roles-001"
  }'

# Moderator role icon (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 Discord role icon for Moderator role. Silver shield symbol, same style as the admin icon. Simple and recognizable.",
    "session_id": "discord-roles-001"
  }'

# VIP role icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 Discord role icon for VIP members. Purple diamond or star symbol, matching the style of previous role icons.",
    "session_id": "discord-roles-001"
  }'
```

### 4. Welcome Channel Graphic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a wide banner graphic for a Discord welcome channel. Friendly and inviting design with soft gradients in blue and purple. Include visual space for welcome text. Aspect ratio 16:9, dimensions 1200x675. Make it warm and community-focused.",
    "mode": "max"
  }'
```

### 5. Rules Channel Graphic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Discord rules channel header graphic. Professional and authoritative design with a scroll or document motif. Dark theme with gold accents. 1200x400 pixels. Include subtle gavel or scales of justice imagery. Clean and readable.",
    "mode": "max"
  }'
```

### 6. Announcement Graphics

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Discord announcement banner for a server update. Exciting and attention-grabbing with a megaphone or notification bell motif. Red and orange energy colors with dark background. 1200x600 pixels. Space for announcement text.",
    "mode": "max"
  }'
```

### 7. Event Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Discord event banner for a gaming tournament. Esports style with dynamic angles and energy effects. Team colors: red vs blue. 1200x675 pixels. Include space for event name, date, and prize info. Competitive and exciting mood.",
    "mode": "max"
  }'
```

### 8. Bot Avatar

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 512x512 Discord bot avatar for a music bot called BeatBot. Friendly robot face with headphones, musical notes floating around. Cyan and white color scheme on dark background. Cute but modern design, reads well as small circle.",
    "mode": "max"
  }'
```

### 9. Emoji Pack Generation

```bash
# Generate consistent emoji set
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 128x128 Discord emoji of a happy pepe-style frog giving thumbs up. Simple, clean design with thick outlines for visibility at small sizes. Green frog, expressive eyes.",
    "session_id": "emoji-pack-001"
  }'

# Sad emoji
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 128x128 Discord emoji of the same frog character but sad with a single tear. Same art style as before, consistent design.",
    "session_id": "emoji-pack-001"
  }'

# Laughing emoji
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 128x128 Discord emoji of the same frog character laughing hard with tears of joy. Consistent style with previous emojis.",
    "session_id": "emoji-pack-001"
  }'
```

### 10. Server Booster Badge

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 Discord role icon for Server Boosters. Premium feel with Discord Nitro pink/purple gradient colors. Lightning bolt or rocket symbol to represent boost. Shiny metallic effect, stands out from other role icons.",
    "mode": "max"
  }'
```

## Best Practices

### Server Icons
- **Simplicity**: Design should be recognizable at 32x32 pixels
- **Contrast**: Use high contrast colors for visibility
- **Centered**: Keep main element centered (displays as circle)
- **No text**: Avoid text - it won't be readable at small sizes
- **Brand colors**: Use consistent brand/community colors

### Role Icons
- **64x64 max**: Discord caps role icons at 64x64
- **Simple shapes**: Complex details get lost at small sizes
- **Color coding**: Use distinct colors for different role levels
- **Consistency**: Create a cohesive set with matching styles
- **Transparency**: Use transparent backgrounds

### Banners & Headers
- **Safe zones**: Keep important elements away from edges
- **Text space**: Leave room for overlay text
- **Mobile friendly**: Test how it looks on mobile
- **File size**: Keep under 10MB for banners

### Emojis
- **128x128**: Standard Discord emoji size
- **256KB limit**: Keep file size under limit
- **Thick outlines**: Helps visibility at small sizes
- **Transparent BG**: Use transparency for versatility
- **Expression focus**: Emphasize the emotion/action

## Prompt Tips for Discord Graphics

When creating Discord graphics, include these details in your prompt:

1. **Exact size**: Specify dimensions (512x512, 960x540, 64x64, etc.)
2. **Asset type**: Server icon, banner, role icon, emoji, etc.
3. **Theme/Style**: Gaming, anime, professional, minimalist, etc.
4. **Colors**: Specific colors or let AI choose based on theme
5. **Key elements**: Symbols, mascots, or imagery to include
6. **Readability**: Mention if it needs to work at small sizes
7. **Text space**: Note if you need room for text overlays

### Example Prompt Structure

```
"Create a [size] Discord [asset type] for [community type/name].
Feature [key visual elements] with [color scheme].
Style: [aesthetic description].
[Additional requirements like small-size readability, text space, etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final assets, server branding, public-facing graphics | Slower | Highest |
| `eco` | Quick drafts, concept exploration, bulk emoji generation | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on Discord graphics:

```bash
# Initial server icon concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 512x512 Discord server icon for a space exploration gaming community",
    "session_id": "space-server-branding"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the planet more prominent and add some stars in the background. Keep the same color scheme.",
    "session_id": "space-server-branding"
  }'

# Create matching banner
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching 960x540 server banner with the same space theme and color palette",
    "session_id": "space-server-branding"
  }'
```

## Complete Server Branding Set

Generate a cohesive branding package:

```bash
# 1. Server icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 512x512 Discord server icon for a creative art community called ArtVault. Modern abstract paint splash design, vibrant rainbow colors on dark background.",
    "session_id": "artvault-branding",
    "mode": "max"
  }'

# 2. Server banner
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching 960x540 server banner. Extend the paint splash theme across a wider canvas. Same colors and style.",
    "session_id": "artvault-branding",
    "mode": "max"
  }'

# 3. Role icons
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 3 role icons (64x64 each) for Artist, Moderator, and VIP roles. Use paintbrush for Artist (blue), palette for Mod (orange), and star for VIP (gold). Same art style as the server icon.",
    "session_id": "artvault-branding",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with Discord community guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Image too large | File size exceeds limit | Request smaller dimensions or simpler design |

## Related Skills

- `each-sense` - Core API documentation
- `social-media-graphics` - Social media assets
- `logo-generation` - Brand logo creation
- `character-design` - Mascot and character creation
