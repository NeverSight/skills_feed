---
name: vtuber-avatar-generation
description: Generate VTuber avatars and character designs using each::sense AI. Create anime-style avatars, Live2D ready characters, expression sheets, full body designs, and accessories for virtual content creators.
metadata:
  author: eachlabs
  version: "1.0"
---

# VTuber Avatar Generation

Generate professional VTuber avatars and character designs using each::sense. This skill creates anime-style illustrations optimized for virtual YouTuber personas, Live2D rigging, and streaming overlays.

## Features

- **Anime VTuber Avatars**: High-quality anime-style character portraits
- **Live2D Ready Designs**: Clean linework and separated layers for rigging
- **Expression Sheets**: Multiple emotions and facial expressions in one sheet
- **Full Body Characters**: Complete character designs from head to toe
- **Chibi/Mascot Versions**: Cute simplified versions for emotes and overlays
- **Character Turnarounds**: Front, side, and back views for 3D modeling
- **Accessories & Props**: Matching items, pets, and stream elements
- **Style Variations**: Fantasy, cyberpunk, idol, casual, and more

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cute anime VTuber avatar, female character with pink hair and cat ears, cheerful expression, upper body portrait for streaming",
    "mode": "max"
  }'
```

## VTuber Design Specifications

| Asset Type | Recommended Size | Use Case |
|------------|------------------|----------|
| Portrait Avatar | 1:1 (1024x1024) | Stream overlay, profile picture |
| Half Body | 3:4 (768x1024) | Live2D model, stream layout |
| Full Body | 2:3 (682x1024) | Full character reveal, merchandise |
| Expression Sheet | 16:9 (1920x1080) | Multiple expressions, reference |
| Turnaround Sheet | 16:9 (1920x1080) | 3D modeling reference |
| Chibi/Emote | 1:1 (512x512) | Channel emotes, stickers |

## Use Case Examples

### 1. Anime VTuber Avatar Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a female anime VTuber avatar portrait. Character has long silver hair with blue highlights, heterochromia eyes (one blue, one gold), wearing a futuristic headset with holographic elements. Gentle smile, soft pastel color palette, clean anime art style suitable for Live2D. Upper body shot with simple gradient background.",
    "mode": "max"
  }'
```

### 2. Live2D Ready Character

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a Live2D ready VTuber character. Female, half body view facing forward. Red twintails hairstyle, large expressive purple eyes, wearing a magical girl outfit with frills and ribbons. Clean linework, flat colors with minimal shading, transparent background. Ensure hair, clothing, and accessories are clearly separated for easy rigging.",
    "mode": "max"
  }'
```

### 3. Multiple Expression Sheet

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an expression sheet for a VTuber character. Same character shown 6 times with different emotions: happy, sad, angry, surprised, smug, and blushing. Anime girl with short blue bob cut and fox ears. Arrange expressions in a 3x2 grid layout, consistent art style across all expressions, white background.",
    "mode": "max"
  }'
```

### 4. Full Body VTuber Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a full body VTuber character. Female idol-themed character with long gradient hair (pink to purple). Wearing an elaborate stage costume with a cropped jacket, pleated skirt, thigh-high boots, and star accessories. Dynamic pose showing personality, detailed outfit design, clean anime illustration style.",
    "mode": "max"
  }'
```

### 5. Chibi/Mascot Version

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a chibi mascot version of a VTuber. Super deformed style with large head and small body (2-3 head ratio). Dragon girl character with small horns, tail, and wings. Cute excited expression, holding a game controller. Transparent background, suitable for Twitch emotes and Discord stickers.",
    "mode": "max"
  }'
```

### 6. Male VTuber Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a male VTuber avatar. Handsome anime boy with messy dark green hair and sharp golden eyes. Wearing a modern streetwear outfit - oversized hoodie with tech patterns, chain accessories. Cool confident expression, upper body portrait, dark moody aesthetic with neon accent lighting.",
    "mode": "max"
  }'
```

### 7. Fantasy/Elf VTuber

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a fantasy elf VTuber character. Elegant female elf with very long flowing white hair and pointed ears. Emerald green eyes, wearing an intricate elven robe with gold embroidery and nature motifs. Serene wise expression, ethereal glowing particles around her, fantasy forest atmosphere in background.",
    "mode": "max"
  }'
```

### 8. Cyberpunk VTuber Style

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cyberpunk VTuber avatar. Female character with asymmetric neon pink and cyan hair, cybernetic eye implants with glowing HUD display. Wearing a tech-enhanced jacket with LED strips and holographic patches. Edgy confident smirk, urban night city reflections, heavy neon lighting in pink and blue.",
    "mode": "max"
  }'
```

### 9. Matching Accessories/Props

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design matching accessories for a witch-themed VTuber. Create a set including: a magical staff with crystal orb, a cute familiar (small black cat with purple eyes), a floating spellbook, and a cauldron prop. All items in cute anime style with purple and black color scheme, transparent background, arranged as item sheet.",
    "session_id": "witch-vtuber-001"
  }'
```

### 10. VTuber Model Turnaround Sheet

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a character turnaround reference sheet for a VTuber. Show the same character from front view, 3/4 view, side view, and back view. Female character with twin buns hairstyle in mint green, wearing a maid cafe uniform. Consistent proportions across all views, white background, label each angle. Suitable for 3D modeling reference.",
    "mode": "max"
  }'
```

## Best Practices

### Character Design
- **Silhouette**: Create distinctive shapes recognizable at small sizes
- **Color Palette**: Limit to 3-5 main colors for brand consistency
- **Readable Features**: Large expressive eyes, clear facial features
- **Signature Elements**: Include memorable accessories or traits

### Live2D Preparation
- **Clean Linework**: Crisp lines without sketchy edges
- **Flat Colors**: Minimize complex gradients for easier rigging
- **Separated Elements**: Hair, face, clothing clearly distinguishable
- **Front-Facing**: Standard neutral pose facing camera

### Expression Sheets
- **Consistency**: Same art style and proportions throughout
- **Range**: Include basic emotions plus character-specific expressions
- **Clear Differences**: Each expression should be instantly recognizable
- **Grid Layout**: Organized arrangement for easy reference

### Accessories & Props
- **Style Match**: Same art style as main character
- **Scale Reference**: Show items at appropriate size
- **Multiple Angles**: Different views if needed for animation
- **Transparent Background**: Easy to composite in streaming software

## Prompt Tips for VTuber Art

When creating VTuber designs, include these details in your prompt:

1. **Character Type**: Gender, species (human, kemonomimi, fantasy)
2. **Visual Features**: Hair, eyes, distinguishing traits
3. **Outfit Style**: Theme, specific clothing items, accessories
4. **Expression/Pose**: Mood, body language, camera angle
5. **Art Style**: Anime substyle, level of detail, coloring style
6. **Technical Specs**: Background, output format, intended use

### Example Prompt Structure

```
"Create a [view type] VTuber [character type].
[Physical description: hair, eyes, features].
Wearing [outfit description].
[Expression and pose].
[Art style specifications].
[Background and technical requirements]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final avatar designs, commission-quality work | Slower | Highest |
| `eco` | Quick concepts, style exploration, drafts | Faster | Good |

## Multi-Turn Character Development

Use `session_id` to iterate on character designs:

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a VTuber avatar concept: cozy streamer girl with autumn theme",
    "session_id": "autumn-vtuber-project"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I like the design! Add maple leaf hair accessories and make the sweater more oversized and cozy looking",
    "session_id": "autumn-vtuber-project"
  }'

# Create variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create an alternate outfit version - same character but in a Halloween costume",
    "session_id": "autumn-vtuber-project"
  }'
```

## Character Asset Pipeline

Generate a complete VTuber asset set:

```bash
# Step 1: Main Avatar
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create main VTuber avatar: space-themed girl with galaxy hair and astronaut-inspired outfit",
    "session_id": "space-vtuber-assets",
    "mode": "max"
  }'

# Step 2: Expression Sheet (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create an expression sheet for this character with 6 different emotions",
    "session_id": "space-vtuber-assets",
    "mode": "max"
  }'

# Step 3: Chibi Version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a chibi version of this character for emotes, super cute style",
    "session_id": "space-vtuber-assets",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `character-design` - General character illustration
- `anime-illustration` - Anime art generation
- `emote-generation` - Twitch/Discord emote creation
