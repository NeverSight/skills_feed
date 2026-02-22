---
name: game-asset-generation
description: Generate game art assets using each::sense AI. Create 2D sprites, character sprite sheets, seamless textures, UI elements, icons, tilesets, loading screens, logos, and concept art for games.
metadata:
  author: eachlabs
  version: "1.0"
---

# Game Asset Generation

Generate professional game art assets using each::sense. This skill creates 2D sprites, textures, UI elements, icons, environments, and more optimized for game development workflows.

## Cost Savings

**60-80% cost reduction** compared to traditional game art production. AI-powered asset generation dramatically reduces time and budget for indie developers, studios, and game jams.

## Features

- **2D Sprites**: Pixel art characters, objects, and props
- **Sprite Sheets**: Animation-ready character sheets with multiple poses
- **Game Textures**: Seamless tileable textures for environments
- **UI Elements**: Buttons, frames, health bars, inventory slots
- **Game Icons**: Item icons, ability icons, achievement badges
- **Tilesets**: Environment tiles for platformers, RPGs, strategy games
- **Loading Screens**: Atmospheric loading and splash screens
- **Game Logos**: Title logos and branding assets
- **Concept Art**: Visual development and mood boards

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 32x32 pixel art sword icon for an RPG game, golden blade with ornate hilt, transparent background",
    "mode": "max"
  }'
```

## Common Game Art Sizes

| Asset Type | Common Sizes | Use Case |
|------------|--------------|----------|
| Pixel Art Icons | 16x16, 32x32, 64x64 | Inventory items, abilities |
| Character Sprites | 32x32, 64x64, 128x128 | Player/NPC characters |
| Sprite Sheets | 512x512, 1024x1024 | Animation frames |
| Textures | 256x256, 512x512, 1024x1024 | Environment surfaces |
| UI Elements | Various | Buttons, frames, bars |
| Loading Screens | 1920x1080, 2560x1440 | Full-screen displays |

## Use Case Examples

### 1. 2D Sprite Generation (Pixel Art)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 pixel art character sprite of a medieval knight with blue armor and silver sword. Retro 16-bit style, side view facing right, transparent background. Clean pixel edges, no anti-aliasing.",
    "mode": "max"
  }'
```

### 2. Character Sprite Sheet

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a character sprite sheet for a pixel art wizard character. Include 8 frames: 2 idle poses, 2 walking frames, 2 attack frames, 1 jump, 1 hurt pose. 32x32 per frame, arranged in a 4x2 grid (256x64 total). Purple robe, white beard, wooden staff.",
    "mode": "max"
  }'
```

### 3. Game Texture Generation (Seamless)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless tileable 512x512 stone dungeon floor texture. Dark gray cobblestones with moss growing between cracks, worn and weathered look. Must tile perfectly with no visible seams when repeated.",
    "mode": "max"
  }'
```

### 4. Game Icon Set

```bash
# First icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 pixel art health potion icon for an RPG. Red liquid in a glass flask with cork stopper, glowing effect, transparent background. Fantasy game style.",
    "session_id": "rpg-icons-set"
  }'

# Second icon (same session for style consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a mana potion icon in the same style. Blue liquid instead of red, same flask design, matching art style.",
    "session_id": "rpg-icons-set"
  }'

# Third icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a stamina potion icon. Green liquid, same consistent style as the health and mana potions.",
    "session_id": "rpg-icons-set"
  }'
```

### 5. UI Elements (Buttons, Frames, Bars)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a fantasy RPG UI kit containing: 1 rectangular button (200x50) with stone texture and gold border, 1 health bar frame (300x30) with ornate metal design, 1 inventory slot frame (64x64) with wooden texture and metal corners. Arrange on transparent background. Medieval fantasy style matching games like Diablo or Baldur'\''s Gate.",
    "mode": "max"
  }'
```

### 6. Environment/Tileset Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2D platformer tileset for a forest level. Include 16x16 pixel tiles: grass top, dirt fill, grass corner pieces (4 corners), tree trunk, leaves, flowers, rocks, wooden platform. Arrange in a tileset grid. Colorful cartoon style similar to classic platformers. 256x256 total sheet.",
    "mode": "max"
  }'
```

### 7. Item/Weapon Icons

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a set of 6 weapon icons for a fantasy game, each 48x48 pixels: iron sword, wooden bow, fire staff, battle axe, throwing daggers, war hammer. Arrange in a 3x2 grid. Consistent hand-painted style with slight glow effects, transparent backgrounds. Top-down perspective for inventory display.",
    "mode": "max"
  }'
```

### 8. Loading Screen Art

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1920x1080 loading screen for a dark fantasy action RPG. Epic scene showing a lone warrior silhouette standing before a massive gothic castle on a cliff, stormy sky with lightning, dark moody atmosphere. Leave space at bottom center for a loading bar. Painterly digital art style.",
    "mode": "max"
  }'
```

### 9. Game Logo Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a game logo for a space shooter called \"NOVA STRIKE\". Bold metallic chrome letters with neon blue glow effects, slight 3D perspective, stars and energy particles around it. Sci-fi futuristic style. Transparent background, 1024x512 resolution. Suitable for title screen and marketing.",
    "mode": "max"
  }'
```

### 10. Concept Art for Games

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create concept art for a post-apocalyptic survival game. Show an abandoned city overgrown with vegetation, rusted vehicles, crumbling skyscrapers with trees growing through them, dramatic sunset lighting breaking through clouds. Painterly concept art style like The Last of Us or Horizon. 16:9 aspect ratio for presentation.",
    "mode": "max"
  }'
```

## Best Practices

### Sprite Art
- **Specify exact dimensions**: Always include pixel dimensions (32x32, 64x64)
- **Mention transparency**: Request transparent background for game integration
- **Define view angle**: Side view, top-down, isometric, front-facing
- **Art style clarity**: Pixel art, hand-painted, vector, retro 8-bit/16-bit

### Textures
- **Request seamless**: Always specify "seamless tileable" for repeating textures
- **Power of 2 sizes**: Use 256, 512, 1024 for optimal GPU performance
- **Material specifics**: Describe wear, weathering, age, condition

### Icon Sets
- **Use session_id**: Maintain consistent style across multiple icons
- **Grid arrangement**: Request organized layouts for sprite sheets
- **Consistent lighting**: Specify light direction for cohesive sets

### UI Elements
- **Leave safe zones**: Account for text and dynamic content
- **Scalability**: Consider how assets scale on different resolutions
- **State variations**: Request normal, hover, pressed states for buttons

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production assets, hero images, key art | Slower | Highest |
| `eco` | Quick iterations, concept exploration, prototyping | Faster | Good |

## Multi-Turn Asset Iteration

Use `session_id` to iterate and create consistent asset sets:

```bash
# Initial character design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a pixel art hero character for a platformer game, 64x64, knight with red cape",
    "session_id": "hero-character-project"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the same character but with a blue cape for player 2, matching style exactly",
    "session_id": "hero-character-project"
  }'

# Create matching enemy
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an enemy character in the same pixel art style - a skeleton warrior, same size and art direction",
    "session_id": "hero-character-project"
  }'
```

## Batch Asset Generation

Generate multiple variations efficiently:

```bash
# Style A - Pixel Art
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a treasure chest icon, 32x32, pixel art, closed position",
    "mode": "eco"
  }'

# Style B - Hand-painted
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a treasure chest icon, 64x64, hand-painted fantasy style, closed position",
    "mode": "eco"
  }'

# Style C - Modern Vector
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a treasure chest icon, 128x128, clean vector style with gradients, modern mobile game look",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to avoid violent/explicit content |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Prompt Tips for Game Assets

When creating game art, include these details in your prompt:

1. **Dimensions**: Exact pixel size (32x32, 512x512)
2. **Art Style**: Pixel art, hand-painted, vector, retro, modern
3. **Perspective**: Side view, top-down, isometric, 3/4 view
4. **Background**: Transparent, solid color, or contextual
5. **Color Palette**: Limited palette, vibrant, muted, specific colors
6. **Game Genre**: RPG, platformer, shooter, puzzle - affects style expectations
7. **Reference Style**: "Like Stardew Valley", "Zelda-inspired", etc.

### Example Prompt Structure

```
"Create a [dimensions] [art style] [asset type] for a [game genre].
[Visual description with colors, materials, details].
[Perspective/view angle]. [Background requirement].
[Additional technical requirements]."
```

## Related Skills

- `each-sense` - Core API documentation
- `product-visuals` - Product visualization
- `image-generation` - General image generation

## References

- [SSE Events Reference](./references/SSE-EVENTS.md) - Server-Sent Events documentation
