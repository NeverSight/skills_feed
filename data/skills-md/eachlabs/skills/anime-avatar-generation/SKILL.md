---
name: anime-avatar-generation
description: Generate anime-style avatars and characters using each::sense AI. Transform photos into anime, create Ghibli-style portraits, manga characters, chibi avatars, and full character sheets with multiple angles.
metadata:
  author: eachlabs
  version: "1.0"
---

# Anime Avatar Generation

Generate stunning anime-style avatars and characters using each::sense. This skill transforms photos into anime art, creates original anime characters, and produces various anime styles from Ghibli to cyberpunk.

## Features

- **Photo to Anime**: Transform real photos into anime-style artwork
- **Ghibli Style**: Studio Ghibli-inspired soft, whimsical characters
- **Manga Style**: Black and white or toned manga character art
- **Cyberpunk Anime**: Neon-lit futuristic anime aesthetics
- **Chibi Avatars**: Cute, super-deformed character styles
- **Profile Pictures**: Optimized anime avatars for social media
- **Full Body Characters**: Complete character designs with outfits
- **Character Sheets**: Multiple angles for consistent character reference

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime avatar of a young woman with long blue hair and golden eyes, soft lighting, studio quality",
    "mode": "max"
  }'
```

## Anime Style Reference

| Style | Description | Best For |
|-------|-------------|----------|
| Ghibli | Soft colors, whimsical, hand-drawn feel | Warm, nostalgic portraits |
| Manga | Black/white, dynamic lines, expressive | Comic-style characters |
| Cyberpunk | Neon colors, futuristic, tech elements | Edgy profile pictures |
| Chibi | Super-deformed, cute, big head/small body | Mascots, emotes |
| Shonen | Bold, action-oriented, dramatic | Male characters, heroes |
| Shojo | Soft, romantic, sparkly effects | Female characters, idols |
| Seinen | Realistic proportions, mature style | Professional avatars |

## Use Case Examples

### 1. Photo to Anime Conversion

Transform a real photo into anime-style artwork.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this photo to anime style. Keep the facial features recognizable but transform it into a beautiful anime portrait with vibrant colors and soft shading.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

### 2. Ghibli Style Avatar

Create a Studio Ghibli-inspired character portrait.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Studio Ghibli style portrait of a young girl with short brown hair, wearing a simple blue dress. Soft watercolor aesthetic, gentle expression, surrounded by nature with small forest spirits in the background. Hayao Miyazaki inspired art style.",
    "mode": "max"
  }'
```

### 3. Manga Style Character

Generate a black and white manga-style character.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a manga-style character portrait in black and white. A confident male protagonist with spiky black hair, sharp eyes, wearing a school uniform. Dynamic pose, dramatic shading with screentones, shonen manga aesthetic.",
    "mode": "max"
  }'
```

### 4. Cyberpunk Anime Style

Create a futuristic neon-lit anime character.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cyberpunk anime character. A hacker girl with short neon pink hair with cyan highlights, cybernetic eye implants, wearing a leather jacket with glowing circuit patterns. Dark urban background with neon signs, rain, and holographic advertisements. Ghost in the Shell meets Akira aesthetic.",
    "mode": "max"
  }'
```

### 5. Chibi Style Avatar

Generate a cute super-deformed character.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a chibi anime avatar. A cute girl with big sparkly purple eyes, long wavy pink hair with star clips, wearing a magical girl outfit with ribbons and bows. Super deformed proportions with big head and small body, kawaii expression, pastel color palette, simple clean background.",
    "mode": "max"
  }'
```

### 6. Anime Profile Picture

Create an optimized avatar for social media profiles.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 square anime profile picture. A mysterious character with silver hair covering one eye, heterochromia (one blue eye, one red eye), wearing a high-collar black coat. Dramatic lighting from the side, dark elegant background. The composition should work well as a small avatar icon.",
    "mode": "max"
  }'
```

### 7. Full Body Anime Character

Design a complete character with outfit and pose.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a full body anime character design. A female warrior with long red hair in a ponytail, green eyes, wearing ornate silver armor with a flowing cape. She holds a glowing magical sword. Dynamic standing pose, fantasy setting with castle in the background. High detail anime illustration style.",
    "mode": "max"
  }'
```

### 8. Anime Couple/Group

Generate multiple characters in one scene.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime illustration of a couple. A tall guy with messy black hair and glasses wearing a casual hoodie, and a shorter girl with twin-tail blonde hair wearing a sundress. They are standing together at a summer festival, holding hands, with fireworks in the night sky behind them. Romantic shojo anime style.",
    "mode": "max"
  }'
```

### 9. Anime with Specific Hair/Eye Colors

Create a character with precise color specifications.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime character with very specific colors: gradient hair that transitions from deep purple at the roots to lavender at the tips, bright amber eyes with a subtle golden glow, pale skin with a slight blush. The character should have an elegant hairstyle with braids and loose strands. Portrait shot, soft dreamy lighting, flower petals floating around.",
    "mode": "max"
  }'
```

### 10. Anime Character Sheet (Multiple Angles)

Generate a reference sheet with multiple views for consistency.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime character reference sheet with multiple angles. The character is a young male mage with medium-length teal hair and bright orange eyes, wearing a wizard robe with gold trim. Show front view, side view (profile), 3/4 view, and back view on a clean white background. Include close-up details of the face and any accessories. Professional character design sheet format.",
    "mode": "max"
  }'
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final avatars, profile pictures, character designs | Slower | Highest |
| `eco` | Quick drafts, exploring styles, iteration | Faster | Good |

## Multi-Turn Character Refinement

Use `session_id` to iterate on character designs:

```bash
# Initial character concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime character - a mysterious ninja with dark clothing",
    "session_id": "ninja-character-design"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I like it but make the character female, add a red scarf, and give her white hair",
    "session_id": "ninja-character-design"
  }'

# Request style variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create the same character but in chibi style",
    "session_id": "ninja-character-design"
  }'
```

## Style Consistency Across Multiple Characters

Create multiple characters with consistent art style:

```bash
# First character
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime hero character - a young man with spiky orange hair and determined expression, wearing a battle-worn jacket",
    "session_id": "anime-team-project"
  }'

# Second character (same session for style consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create his rival - a calm, cool character with slicked-back blue hair, wearing a formal coat. Keep the same art style as the previous character.",
    "session_id": "anime-team-project"
  }'
```

## Best Practices

### Character Description Tips

- **Hair**: Specify color, length, style (spiky, wavy, straight, twin-tails, ponytail)
- **Eyes**: Describe color, shape, and expression (sharp, soft, sparkly)
- **Clothing**: Detail the outfit style, colors, and any accessories
- **Expression**: Define the mood (happy, mysterious, fierce, gentle)
- **Pose**: Describe the body position and any gestures

### Style Specification

- Reference specific anime/manga for style guidance
- Mention lighting preferences (soft, dramatic, backlit)
- Specify background complexity (simple, detailed, gradient)
- Include color palette preferences (pastel, vibrant, dark)

### Technical Considerations

- For profile pictures, request 1:1 aspect ratio
- For character sheets, request landscape orientation
- For full body, ensure the composition includes head to feet
- For detailed faces, request close-up portrait composition

## Prompt Tips for Anime Avatars

When creating anime characters, include these details:

1. **Character Gender/Age**: Young girl, adult man, teenage boy, etc.
2. **Hair Details**: Color, length, style, accessories (ribbons, clips)
3. **Eye Details**: Color, shape, expression, any special features
4. **Outfit**: Clothing type, style, colors, accessories
5. **Pose/Composition**: Portrait, full body, action pose, etc.
6. **Art Style**: Ghibli, manga, cyberpunk, chibi, etc.
7. **Mood/Atmosphere**: Cheerful, mysterious, dramatic, romantic
8. **Background**: Simple, detailed, specific setting

### Example Prompt Structure

```
"Create a [style] anime [character type] with [hair details] and [eye details].
They are wearing [outfit description].
[Pose/composition]. [Background/setting].
[Mood/atmosphere] feeling. [Additional details]."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Inconsistent character | Session not maintained | Use same `session_id` for related requests |

## Related Skills

- `each-sense` - Core API documentation
- `photo-to-illustration` - General illustration styles
- `character-design` - Non-anime character creation
- `profile-picture-generation` - General avatar creation
