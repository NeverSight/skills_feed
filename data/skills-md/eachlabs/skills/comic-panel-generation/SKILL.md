---
name: comic-panel-generation
description: Generate comic and manga panels, strips, and pages using each::sense AI. Create superhero comics, manga pages, webtoons, action sequences, and convert photos to comic art with consistent characters.
metadata:
  author: eachlabs
  version: "1.0"
---

# Comic Panel Generation

Generate professional comic and manga artwork using each::sense. This skill creates single panels, multi-panel strips, full page layouts, and complete comic sequences with consistent character designs.

## Features

- **Single Panels**: Individual comic panels with dynamic compositions
- **Multi-Panel Strips**: Traditional 3-4 panel comic strips
- **Manga Pages**: Japanese manga-style page layouts with reading flow
- **Superhero Comics**: Western comic book style with bold colors and action
- **Webtoon Format**: Vertical scrolling format for mobile viewing
- **Photo to Comic**: Convert photos into comic/manga art style
- **Speech Bubbles**: Generate panels with integrated dialogue bubbles
- **Action Sequences**: Dynamic action panels with motion lines and effects
- **Character Consistency**: Maintain character appearance across multiple panels
- **Cover Design**: Comic book and manga cover artwork

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a single comic panel of a superhero landing dramatically on a rooftop at night, cape billowing, city lights in background",
    "mode": "max"
  }'
```

## Comic Panel Formats & Sizes

| Format | Aspect Ratio | Recommended Size | Use Case |
|--------|--------------|------------------|----------|
| Single Panel | 1:1 | 1024x1024 | Social media, standalone art |
| Wide Panel | 16:9 | 1920x1080 | Cinematic moments, landscapes |
| Tall Panel | 9:16 | 1080x1920 | Dramatic reveals, webtoon |
| Comic Strip | 3:1 | 1500x500 | 3-4 panel horizontal strips |
| Manga Page | 2:3 | 1200x1800 | Traditional manga layout |
| Webtoon | 1:3+ | 800x2400+ | Vertical scroll format |
| Comic Cover | 2:3 | 1200x1800 | Book covers, thumbnails |

## Use Case Examples

### 1. Single Comic Panel

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a single comic panel showing a detective in a noir style examining clues in a dimly lit office. Heavy shadows, black and white with selective color on a red lamp. Include dramatic lighting from venetian blinds.",
    "mode": "max"
  }'
```

### 2. Multi-Panel Comic Strip

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4-panel horizontal comic strip. Panel 1: A cat staring at an empty food bowl. Panel 2: Cat meowing at its sleeping owner. Panel 3: Cat knocking items off a shelf. Panel 4: Owner finally awake and annoyed, cat looking innocent. Cute cartoon style, pastel colors.",
    "mode": "max"
  }'
```

### 3. Manga Page Layout

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a full manga page with 5-6 panels. Scene: A young samurai drawing his sword for the first time. Include dynamic panel sizes - one large panel for the dramatic sword draw moment, smaller panels for reaction shots. Black and white manga style with screentones, speed lines for action. Right-to-left reading flow.",
    "mode": "max"
  }'
```

### 4. Superhero Comic Style

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a superhero comic panel in classic Marvel/DC style. A female superhero with electric powers charging up, lightning crackling around her fists, dramatic low angle shot. Bold colors, heavy inks, dynamic pose, Kirby-style energy effects. Include a starburst background.",
    "mode": "max"
  }'
```

### 5. Webtoon Vertical Format

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a vertical webtoon-style comic segment with 3 connected scenes. Scene 1: A student walking into a mysterious antique shop. Scene 2: Close-up of a glowing amulet on a shelf. Scene 3: The shopkeeper appearing mysteriously behind them. Korean webtoon art style, soft colors, vertical scroll format optimized for mobile. 9:16 or taller aspect ratio.",
    "mode": "max"
  }'
```

### 6. Photo to Comic Conversion

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this photo into a comic book style illustration. Apply bold black outlines, halftone dots for shading, vibrant pop art colors. Make it look like a panel from a graphic novel. Keep the composition but stylize all elements.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait-photo.jpg"]
  }'
```

### 7. Speech Bubble Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a comic panel with two characters arguing. Include speech bubbles with placeholder text areas. Character 1 (angry businessman): large jagged speech bubble for shouting. Character 2 (calm woman): regular oval speech bubble for response. Also include a thought bubble above the woman showing she is unimpressed. Western comic style.",
    "mode": "max"
  }'
```

### 8. Action Sequence Panels

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3-panel action sequence showing a martial arts fight. Panel 1: Fighter A launching a flying kick (motion blur, speed lines). Panel 2: Impact moment with dramatic POW effect and motion burst. Panel 3: Fighter B crashing through wooden crates. Manga action style with heavy use of speed lines, impact effects, and dynamic camera angles.",
    "mode": "max"
  }'
```

### 9. Consistent Character Across Panels

```bash
# First panel - establish character
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a comic panel introducing a character: A teenage girl with short blue hair, large round glasses, wearing a yellow raincoat. She is looking up at the rain with wonder. Anime/manga style, soft colors. This is panel 1 of a series - I need to maintain her appearance in future panels.",
    "session_id": "comic-rainy-day-001",
    "mode": "max"
  }'

# Second panel - same character, different scene
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create panel 2 with the same blue-haired girl with glasses and yellow raincoat. Now she is jumping in a puddle, splashing water, with a big smile. Maintain the exact same character design and art style from panel 1.",
    "session_id": "comic-rainy-day-001",
    "mode": "max"
  }'

# Third panel - continue the story
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create panel 3: Same character discovers a small frog on a lily pad in the puddle. She kneels down, delighted. Keep her blue hair, round glasses, yellow raincoat consistent. Same manga art style.",
    "session_id": "comic-rainy-day-001",
    "mode": "max"
  }'
```

### 10. Comic Cover Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a comic book cover for issue #1 of SHADOW KNIGHTS. Feature a team of 4 heroes in dramatic poses - a knight with a glowing sword, an archer with shadow powers, a mage with fire magic, and a rogue with dual daggers. Dark fantasy style, dramatic lighting from below, epic composition. Leave space at the top for the title logo and bottom for issue number and barcode area. 2:3 aspect ratio.",
    "mode": "max"
  }'
```

## Comic Art Styles

| Style | Description | Best For |
|-------|-------------|----------|
| Western Comics | Bold lines, vibrant colors, dynamic poses | Superhero, action |
| Manga | Clean lines, screentones, expressive eyes | Drama, romance, action |
| Webtoon | Soft colors, detailed backgrounds, vertical flow | Romance, fantasy, slice of life |
| Noir | High contrast, shadows, limited palette | Detective, thriller |
| Cartoon | Simplified shapes, exaggerated expressions | Comedy, kids content |
| Graphic Novel | Detailed, realistic proportions | Mature themes, literary |
| Pop Art | Bold colors, halftones, stylized | Modern, artistic |

## Prompt Tips for Comic Generation

When creating comic panels, include these details in your prompt:

1. **Panel Layout**: Single panel, multi-panel strip, full page, or vertical scroll
2. **Art Style**: Manga, Western comic, webtoon, noir, cartoon, etc.
3. **Action/Scene**: What is happening in each panel
4. **Characters**: Describe appearance, expressions, poses
5. **Composition**: Camera angle, focal point, dramatic elements
6. **Effects**: Speed lines, impact effects, screentones, lighting
7. **Dialogue Space**: Request speech/thought bubbles if needed
8. **Reading Flow**: Left-to-right (Western) or right-to-left (manga)

### Example Prompt Structure

```
"Create a [panel count/layout] comic in [art style] style.
[Panel-by-panel description of action/scene].
Characters: [descriptions].
Include [effects: speed lines, speech bubbles, etc.].
[Color/mood]: [palette preferences]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final artwork, print-ready comics, detailed pages | Slower | Highest |
| `eco` | Quick drafts, storyboarding, concept exploration | Faster | Good |

## Multi-Turn Comic Creation

Use `session_id` to build a complete comic across multiple requests:

```bash
# Page 1 - Establish the story
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create page 1 of a sci-fi manga. A space bounty hunter enters a seedy alien bar. 4 panels: exterior shot of neon-lit bar, hunter walking in (silhouette), aliens turning to look, close-up of hunters determined eyes.",
    "session_id": "space-bounty-comic"
  }'

# Page 2 - Continue the narrative
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create page 2 continuing the scene. The hunter approaches a table of alien criminals. Include panels showing: the target alien recognizing danger, the hunters hand reaching for a weapon, tension building. Same art style as page 1.",
    "session_id": "space-bounty-comic"
  }'

# Request style adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Recreate page 2 but with more dramatic lighting - add more shadows and a red color accent from the bar neon signs. Keep all other elements the same.",
    "session_id": "space-bounty-comic"
  }'
```

## Batch Generation for Comic Projects

Generate multiple pages or variations efficiently:

```bash
# Cover variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a manga cover - a magical girl transformation scene, sparkles and ribbons, dramatic pose",
    "mode": "eco"
  }'

# Alternative cover style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the same magical girl cover but in darker, more mature art style - less sparkles, more dramatic shadows",
    "mode": "eco"
  }'

# Western comic adaptation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the magical girl transformation but in Western superhero comic style - bold colors, heavy inks, more muscular proportions",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to avoid violent/adult content |
| Timeout | Complex multi-panel generation | Set client timeout to minimum 10 minutes |
| Character inconsistency | New session or vague description | Use same session_id, provide detailed character descriptions |

## Related Skills

- `each-sense` - Core API documentation
- `photo-to-illustration` - Convert photos to various art styles
- `character-design-generation` - Create consistent character sheets
- `storyboard-generation` - Create visual storyboards for animation
