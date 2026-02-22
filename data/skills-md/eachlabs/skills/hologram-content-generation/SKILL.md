---
name: hologram-content-generation
description: Generate hologram and 3D display content using each::sense AI. Create holographic product displays, presenters, 3D logos, interactive menus, event content, museum exhibits, retail displays, and trade show holograms.
metadata:
  author: eachlabs
  version: "1.0"
---

# Hologram Content Generation

Generate stunning hologram and 3D display content using each::sense. This skill creates images and videos optimized for holographic displays, 3D fans, LED pyramids, and other volumetric display technologies.

## Features

- **Product Holograms**: Floating 3D product visualizations for retail and showrooms
- **Holographic Presenters**: Virtual spokespersons and brand ambassadors
- **3D Logo Animation**: Animated brand logos for holographic displays
- **Interactive Menus**: Holographic interface and menu systems
- **Event Holograms**: Stage content for concerts, conferences, and launches
- **Museum Exhibits**: Educational holographic content for exhibits
- **Retail Displays**: Eye-catching holographic advertising
- **Trade Show Content**: Attention-grabbing booth holograms
- **Holographic Greetings**: Personalized 3D messages and invitations
- **Interactive Designs**: Touch-responsive holographic interfaces

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic product display showing a luxury watch floating and slowly rotating with particle effects and blue glow",
    "mode": "max"
  }'
```

## Hologram Display Formats

| Display Type | Aspect Ratio | Recommended | Use Case |
|--------------|--------------|-------------|----------|
| Hologram Fan | 1:1 | 1080x1080 | Retail, events, trade shows |
| LED Pyramid | 1:1 | 1080x1080 | Product displays, museums |
| Pepper's Ghost | 16:9 | 1920x1080 | Stage shows, large events |
| Holographic Box | 1:1 | 1080x1080 | Small product displays |
| Volumetric Display | 1:1 | 1080x1080 | High-end installations |
| Transparent OLED | 16:9 | 1920x1080 | Retail windows, exhibits |

## Use Case Examples

### 1. Holographic Product Display

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic product display for a premium perfume bottle. The bottle should float in the center, slowly rotating with a magical mist swirling around it. Add sparkle particles and a soft pink/purple glow. Black background for hologram fan display. 1:1 aspect ratio, 5 second loop.",
    "mode": "max"
  }'
```

### 2. Hologram Presenter/Spokesperson

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic presenter - a professional woman in business attire appearing as a blue-tinted hologram. She should be gesturing welcomingly as if greeting visitors. Add scan lines and digital glitch effects for authentic hologram look. Full body shot, black background, 16:9 aspect ratio.",
    "mode": "max"
  }'
```

### 3. 3D Logo Animation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D holographic logo animation. A futuristic tech company logo (abstract geometric shape) assembles from floating particles, rotates to reveal depth, then pulses with energy. Cyan and white color scheme with electric effects. Black background, 1:1 square format, 6 second seamless loop.",
    "mode": "max"
  }'
```

### 4. Holographic Menu/Interface

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic menu interface for a futuristic restaurant. Floating translucent panels showing food items with 3D dish previews. Sci-fi UI design with glowing borders, subtle animations. Blue and orange accent colors on dark background. 16:9 aspect ratio, interactive feel.",
    "mode": "max"
  }'
```

### 5. Event Hologram Content

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create holographic stage content for a product launch event. A smartphone emerging from an explosion of light particles, floating and rotating to show all angles. Dynamic camera movement, epic reveal moment with lens flares and energy waves. 16:9 cinematic format, 10 seconds.",
    "mode": "max"
  }'
```

### 6. Museum/Exhibit Hologram

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic museum exhibit showing a dinosaur (T-Rex) in educational display format. The dinosaur should appear as a detailed 3D hologram, slowly rotating with anatomical labels floating around it. Scientific visualization style with blue holographic effect. Black background, 1:1 format, 8 second loop.",
    "mode": "max"
  }'
```

### 7. Retail Hologram Display

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a retail holographic display for sneakers. The shoe floats and rotates showing all angles, with dynamic lighting highlighting materials and details. Add speed lines and energy effects suggesting performance. Price tag holographically appears. Attention-grabbing for store window. 1:1 square, 5 second loop.",
    "mode": "max"
  }'
```

### 8. Trade Show Hologram

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an attention-grabbing trade show booth hologram. A futuristic robot mascot waving and beckoning visitors, surrounded by floating company info graphics and product highlights. High energy, playful but professional. Include particle effects and holographic glitches. 1:1 format, 10 second loop.",
    "mode": "max"
  }'
```

### 9. Holographic Greeting

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic birthday greeting. A magical 3D birthday cake with floating candles, sparkles swirling around it, and the text HAPPY BIRTHDAY appearing in glowing 3D letters above. Warm golden and pink colors with festive particle effects. Black background, 1:1 square format, 6 seconds.",
    "mode": "max"
  }'
```

### 10. Interactive Hologram Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an interactive holographic globe interface. A 3D Earth slowly rotating with data points lighting up across continents, connection lines between cities, and floating info panels that appear. Sci-fi command center aesthetic. Blue and cyan tones on black background. 1:1 format, 8 second loop.",
    "mode": "max"
  }'
```

## Best Practices

### Hologram Design Principles
- **Black Background**: Essential for hologram fans and most display types - content appears to float
- **High Contrast**: Use bright, glowing elements against dark backgrounds
- **Center Focus**: Keep main content centered for 3D fan displays
- **Smooth Motion**: Avoid jerky movements - smooth rotations and transitions work best
- **Loop Seamlessly**: Create content that loops perfectly for continuous display

### Visual Effects for Authenticity
- **Scan Lines**: Horizontal lines add retro-futuristic hologram feel
- **Glitch Effects**: Subtle digital artifacts enhance realism
- **Particle Effects**: Floating particles add depth and magic
- **Glow/Bloom**: Soft glow around elements enhances 3D appearance
- **Transparency**: Semi-transparent elements look more holographic

### Color Considerations
- **Cyan/Blue**: Classic hologram color, high tech feel
- **White/Silver**: Clean, premium appearance
- **Purple/Pink**: Magical, entertainment oriented
- **Green**: Matrix-style, data visualization
- **Orange/Gold**: Warm, luxury products

### Technical Requirements
- **Frame Rate**: 30fps minimum, 60fps for smooth rotation
- **Resolution**: Match your display - typically 1080x1080 for fans
- **Duration**: 5-15 seconds for loops, longer for narratives
- **File Format**: MP4 with H.264/H.265 codec

## Prompt Tips for Hologram Content

When creating holographic content, include these details:

1. **Display Type**: Specify hologram fan, pyramid, stage, etc.
2. **Aspect Ratio**: 1:1 for fans/pyramids, 16:9 for stages
3. **Subject**: What should be displayed (product, person, logo)
4. **Motion**: Rotation, floating, assembly animation
5. **Effects**: Particles, glow, scan lines, glitches
6. **Color Scheme**: Specify hologram colors
7. **Background**: Almost always black for proper display
8. **Duration**: Loop length and seamless looping requirement

### Example Prompt Structure

```
"Create a holographic [content type] for [display type].
Show [subject] with [motion/animation].
Add [effects] with [color scheme].
Black background, [aspect ratio] format, [duration] second loop."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast drafts or production quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production content, client deliverables | Slower | Highest |
| `eco` | Quick concepts, iterations, testing ideas | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on hologram content:

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic car display for an auto showroom, the car floating and rotating",
    "session_id": "car-hologram-001"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more dramatic - add energy lines tracing the car body, and have parts explode outward to show the engine",
    "session_id": "car-hologram-001"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a version with different color scheme - red and orange energy effects instead of blue",
    "session_id": "car-hologram-001"
  }'
```

## Industry Applications

### Retail & E-commerce
- In-store product displays
- Window displays
- Pop-up experiences
- Product launches

### Events & Entertainment
- Concert visuals
- Conference stages
- Award ceremonies
- Theme park attractions

### Museums & Education
- Historical recreations
- Scientific visualizations
- Interactive exhibits
- Visitor information

### Corporate & Marketing
- Lobby displays
- Trade show booths
- Brand activations
- Executive presentations

### Hospitality
- Restaurant menus
- Hotel concierge
- Wayfinding systems
- Entertainment venues

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product photography
- `video-generation` - General video content
- `3d-animation` - 3D animated content
