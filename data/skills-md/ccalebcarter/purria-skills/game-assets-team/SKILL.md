---
name: game-assets-team
description: Complete game asset design, creation, implementation, and optimization team. Use when creating visual assets, art direction, sprites, UI elements, icons, textures, animations specs, audio design, or any game visuals. Covers AI image generation (Gemini), asset pipelines, optimization for web/mobile, style guides, and performance tuning. Triggers on requests for game art, icons, backgrounds, character designs, UI assets, promotional materials, or asset troubleshooting.
---

# Game Assets Team

A virtual SME team for game asset design, creation, implementation, and optimization. Specialized for scalable web/mobile games with low-poly crystalline aesthetics.

## Team Roles & Expertise

| Role | Responsibilities |
|------|------------------|
| **Art Director** | Visual style, consistency, brand identity |
| **Concept Artist** | Initial designs, mood boards, style exploration |
| **UI/UX Designer** | Interface elements, iconography, HUD components |
| **Technical Artist** | Optimization, formats, performance, pipelines |
| **Motion Designer** | Animation specs, transitions, micro-interactions |
| **Audio Designer** | Sound direction, SFX specs, music briefs |

## Asset Creation Workflow

### 1. AI Image Generation (Primary Tool)

Use the `gemini-image-generator` skill for rapid asset creation:

```bash
# From the gemini-image-generator scripts directory:
python generate.py --prompt "[DETAILED PROMPT]" --output [filename].png
```

**Prompt Engineering for Game Assets:**

```
Structure: [Subject] + [Style] + [Composition] + [Technical] + [Mood]

Example for Farming in Purria Simulins:
"cute low-poly geometric bee game character, faceted crystalline wings,
big adorable eyes, bold yellow and gold with subtle gradients,
3/4 angle view, transparent background, phase 2 evolution,
developing features, partial crystalline wings"
```

### 2. Asset Categories & Specs

| Category | Formats | Sizes | Notes |
|----------|---------|-------|-------|
| UI Icons | PNG-24, SVG | 64x64, 128x128 | Transparent BG, 2px padding |
| Sprites | PNG-24, WebP | Power of 2 | Sprite sheets preferred |
| Backgrounds | WebP, AVIF | 1920x1080, 2560x1440 | Layered for parallax |
| Simulins | PNG-24 | 128/192/256px by phase | 3 evolution phases |
| Cards | PNG-24, SVG | 180x252 (2.5:3.5) | Print-ready at 300dpi |
| Particles | PNG-24 | 32x32, 64x64 | Additive blend ready |

### 3. Style Guide: Farming in Purria

**Visual Pillars:**
1. **Low-Poly Geometric** - Faceted shapes, clean edges, visible polygons
2. **Crystalline Accents** - Translucent gem-like wings, prismatic reflections
3. **Kawaii Charm** - Big expressive eyes, cute proportions, personality
4. **Bold Colors** - Vibrant palettes with subtle gradients

**Color Palette (Simulins):**
```
Spider:      #8B5CF6 (Purple)     #A78BFA (Light Purple)
Bee:         #F59E0B (Amber)      #FBBF24 (Yellow)
Ladybug:    #EF4444 (Red)        #1F2937 (Black)
Butterfly:  #EC4899 (Pink)       #8B5CF6 (Purple)
Grasshopper: #22C55E (Green)      #84CC16 (Lime)
Mole:        #92400E (Brown)      #D97706 (Orange)
```

**Typography:**
- Headers: Rounded, friendly sans-serif
- Body: Clean readability
- Numbers: Roboto Mono (Tabular for scores/currency)

## Optimization Standards

### Web/Mobile Performance

| Asset Type | Max Size | Format Priority | Lazy Load |
|------------|----------|-----------------|-----------|
| Hero Images | 200KB | AVIF > WebP > PNG | No |
| UI Sprites | 100KB | WebP > PNG | No |
| Backgrounds | 300KB | AVIF > WebP | Yes |
| Icons | 10KB each | SVG > WebP | No |
| Animations | 500KB | Lottie > GIF | Yes |

### Sprite Sheet Guidelines

```
Layout: Grid-based, power-of-2 dimensions
Padding: 2px between frames (prevents bleeding)
Naming: [simulin]_phase[1-3].[ext]
Atlas: Generate JSON metadata for programmatic access
```

### Responsive Asset Strategy

```
/assets
  /1x  (base - mobile)
  /2x  (retina - tablet/desktop)
  /3x  (high-DPI - optional)
```

Use `<picture>` element or CSS image-set() for delivery.

## Implementation Patterns

### React Integration

```tsx
// Optimized image component pattern
const GameAsset = ({ src, alt, priority = false }) => (
  <img
    src={src}
    alt={alt}
    loading={priority ? "eager" : "lazy"}
    decoding="async"
    className="crisp" // for low-poly art
  />
);
```

### CSS for Game Assets

```css
/* Crisp rendering for low-poly assets */
.crisp {
  image-rendering: crisp-edges;
  image-rendering: -webkit-optimize-contrast;
}

/* Smooth scaling for gradients */
.smooth {
  image-rendering: smooth;
  image-rendering: high-quality;
}

/* Sprite animation */
.sprite-animate {
  animation: sprite-play 0.8s steps(8) infinite;
}
```

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Blurry assets | Wrong resolution | Use 2x assets, check devicePixelRatio |
| Color banding | 8-bit limitation | Use PNG-24, add subtle dithering |
| Jagged edges | No anti-aliasing | Enable AA in source, or use SVG |
| Large file size | Unoptimized | Run through squoosh.app, use WebP |
| Animation stutter | Too many frames | Reduce to 12-24fps, use CSS transforms |
| Inconsistent style | No style guide | Reference art-direction.md, use AI consistently |

## Quality Checklist

Before shipping any asset:

- [ ] Correct dimensions and format
- [ ] Optimized file size (within limits above)
- [ ] Transparent background where needed
- [ ] Consistent with low-poly crystalline style
- [ ] Tested on 1x and 2x displays
- [ ] Named according to convention
- [ ] Metadata/atlas generated if sprite

## Reference Documents

- [Art Direction Deep Dive](references/art-direction.md) - Extended style guide, Simulin specs
- [Optimization Techniques](references/optimization.md) - Compression, formats, tools
- [Animation Specs](references/animation.md) - Timing, easing, Lottie workflows
