---
name: nft-art-generation
description: Generate NFT artwork using each::sense AI. Create PFP collections, generative art, 1/1 pieces, pixel art, 3D renders, animated NFTs, and trait-based characters for Web3 projects.
metadata:
  author: eachlabs
  version: "1.0"
---

# NFT Art Generation

Generate stunning NFT artwork using each::sense. This skill creates images and videos optimized for NFT collections, marketplaces, and Web3 projects.

## Features

- **PFP Collections**: 10K style profile picture collections with consistent traits
- **Generative Art**: Algorithm-inspired abstract and geometric pieces
- **1/1 Unique Artwork**: High-quality single edition masterpieces
- **Pixel Art**: Retro-style pixelated NFT artwork
- **3D NFTs**: Rendered 3D characters and objects
- **Animated NFTs**: GIF and video NFTs with motion
- **AI Art Collections**: Distinctive AI-generated art series
- **Trait-Based Characters**: Characters with combinable attributes

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a PFP NFT of an ape character with cyberpunk style, neon colors, wearing futuristic sunglasses and a hoodie, dark background",
    "mode": "max"
  }'
```

## NFT Art Formats & Sizes

| Type | Aspect Ratio | Recommended Size | Use Case |
|------|--------------|------------------|----------|
| PFP Collection | 1:1 | 1024x1024 or 2048x2048 | Profile pictures, avatars |
| Generative Art | 1:1 | 2048x2048 or 4096x4096 | Art pieces, gallery display |
| 1/1 Artwork | Various | 2048x2048+ | High-value single editions |
| Pixel Art | 1:1 | 32x32 to 512x512 | Retro collections |
| 3D Render | 1:1 or 4:3 | 2048x2048 | 3D character NFTs |
| Animated GIF | 1:1 | 1024x1024 | Motion NFTs |
| Video NFT | 1:1 or 16:9 | 1080x1080 or 1920x1080 | Premium animated pieces |

## Use Case Examples

### 1. PFP Collection Style (10K Style)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 PFP NFT in the style of a 10K collection. An anthropomorphic fox character with purple fur, wearing a gold chain necklace and a backwards cap. Solid gradient background from teal to purple. Clean digital art style, bold outlines, vibrant colors.",
    "mode": "max"
  }'
```

### 2. Generative Art Piece

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a generative art piece inspired by algorithmic patterns. Abstract flowing lines and geometric shapes, inspired by Tyler Hobbs and Dmitri Cherniak. Use a limited color palette of deep blues, whites, and gold accents. Mathematical precision with organic flow. 1:1 aspect ratio.",
    "mode": "max"
  }'
```

### 3. 1/1 Unique Artwork

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a high-quality 1/1 NFT artwork. A surreal dreamscape with a floating island in a cosmic void, ancient ruins overgrown with bioluminescent plants, multiple moons in the sky, ethereal atmosphere. Ultra detailed, cinematic lighting, museum-quality digital painting.",
    "mode": "max"
  }'
```

### 4. Pixel Art NFT

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a pixel art NFT character. A retro-style warrior knight with glowing sword, 32x32 pixel style scaled up cleanly. Limited color palette, nostalgic 8-bit aesthetic, solid color background. CryptoPunks meets fantasy RPG vibe.",
    "mode": "max"
  }'
```

### 5. 3D NFT Artwork

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D rendered NFT character. A stylized robot head with chrome finish, glowing LED eyes, intricate mechanical details, floating in a dark studio environment with dramatic rim lighting. Octane render quality, subsurface scattering, 1:1 aspect ratio.",
    "mode": "max"
  }'
```

### 6. Animated NFT (GIF/Video)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an animated NFT, 3-5 seconds loop. A mystical crystal orb with swirling energy inside, particles floating around it, pulsing glow effect. Seamless loop, hypnotic motion, dark background with subtle ambient particles. 1:1 square format.",
    "mode": "max"
  }'
```

### 7. AI Art Collection

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AI art piece for a collection exploring digital consciousness. Abstract portrait merging human and digital elements, data streams flowing through a face, glitch art effects, neural network visualization overlay. Vaporwave color palette with pink, cyan, and purple. Unique artistic interpretation.",
    "mode": "max"
  }'
```

### 8. Trait-Based Character Generation

```bash
# First character with base traits
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a trait-based NFT character for a collection. Base: Cat humanoid. Traits: Background=Sunset Orange, Fur=Calico pattern, Eyes=Laser red, Accessory=Pirate eyepatch, Clothing=Leather jacket, Headwear=None. Consistent flat illustration style suitable for a 10K PFP collection.",
    "session_id": "nft-collection-cats-001"
  }'

# Second character variation (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another character with different traits. Same style as before. Traits: Background=Deep Space, Fur=White, Eyes=Diamond blue, Accessory=Monocle, Clothing=Tuxedo, Headwear=Top hat. Maintain the exact same art style.",
    "session_id": "nft-collection-cats-001"
  }'
```

### 9. Abstract Generative Art

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an abstract generative art NFT. Inspired by Art Blocks aesthetic - recursive geometric patterns, flow fields, mathematical beauty. Colors emerge from chaos into order. Black background with vibrant color accents in orange, pink, and electric blue. Crisp vector-like precision. 1:1 format.",
    "mode": "max"
  }'
```

### 10. Cyberpunk/Futuristic NFT

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cyberpunk NFT artwork. A futuristic street samurai character with cybernetic augmentations, neon-lit visor, holographic HUD elements, rain-soaked environment reflected on surfaces. Blade Runner meets anime aesthetic. Neon pink and cyan color scheme, dark atmospheric mood. Premium collectible quality.",
    "mode": "max"
  }'
```

## Best Practices

### Collection Consistency
- **Art Style**: Maintain consistent style across collection pieces
- **Color Palette**: Define and stick to a cohesive palette
- **Trait System**: Plan traits with clear categories (background, body, accessories, etc.)
- **Resolution**: Use consistent resolution across all pieces
- **Session ID**: Use same session_id for related pieces to maintain consistency

### Technical Quality
- **High Resolution**: Generate at 2048x2048+ for quality display
- **Clean Edges**: Request clean outlines for PFP collections
- **Proper Format**: Use PNG for static, MP4/GIF for animated
- **Marketplace Ready**: Ensure output meets OpenSea, Foundation, etc. requirements

### NFT-Specific Considerations
- **Rarity Planning**: Design rare traits distinctively
- **Scalability**: Ensure art looks good at small sizes (profile thumbnails)
- **Uniqueness**: Each piece should be visually distinct
- **Metadata Ready**: Generate with clear trait descriptions

## Prompt Tips for NFT Art

When creating NFT artwork, include these details in your prompt:

1. **Collection Type**: PFP, generative, 1/1, pixel art, etc.
2. **Art Style**: Describe the visual style (flat, 3D, pixel, painterly)
3. **Subject**: What is the main subject (character, abstract, landscape)
4. **Traits/Attributes**: List specific features if trait-based
5. **Color Palette**: Specify colors or mood
6. **Background**: Solid color, gradient, or detailed
7. **Quality Level**: Mention if premium/museum quality needed

### Example Prompt Structure

```
"Create a [collection type] NFT.
[Subject description] with [traits/attributes].
Style: [art style].
Colors: [color palette].
Background: [background description].
[Additional quality/format requirements]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final collection pieces, 1/1 artwork, premium drops | Slower | Highest |
| `eco` | Concept exploration, trait testing, draft iterations | Faster | Good |

## Multi-Turn Collection Development

Use `session_id` to develop collections iteratively:

```bash
# Establish collection style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a base character for my NFT collection. A stylized bear with streetwear fashion, bold flat colors, minimalist background.",
    "session_id": "bear-nft-project"
  }'

# Request trait variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the same bear character but with different accessories - add sunglasses and a gold chain. Keep the exact same art style.",
    "session_id": "bear-nft-project"
  }'

# Request rare variant
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a rare legendary variant - same bear but with cosmic/galaxy fur pattern, glowing eyes, and a crown. This is the 1/1 rare for the collection.",
    "session_id": "bear-nft-project"
  }'
```

## Batch Generation for Collections

Generate multiple variations efficiently:

```bash
# Variation 1 - Common trait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create PFP NFT: Robot character, silver body, blue LED eyes, plain gray background, minimal style",
    "mode": "eco"
  }'

# Variation 2 - Uncommon trait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create PFP NFT: Robot character, gold body, green LED eyes, gradient purple background, minimal style",
    "mode": "eco"
  }'

# Variation 3 - Rare trait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create PFP NFT: Robot character, holographic rainbow body, laser red eyes, cosmic space background, minimal style",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Style inconsistency | New session | Use same `session_id` for collection pieces |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product imagery
- `meta-ad-creative-generation` - Social media creatives
