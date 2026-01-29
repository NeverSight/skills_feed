---
name: remotion-ads
description: Instagram Reels & Carousel ad creation with Remotion. Use when creating vertical videos (9:16) for Instagram Reels/Stories or carousel posts (4:5). Includes safe zones, typography specs, voiceover integration, animations, and export settings.
---

# Remotion Ads - Instagram Video & Carousel Creation

Complete toolkit for creating professional Instagram Reels and Carousel ads with Remotion.

## Quick Setup

**Before creating any videos, configure your brand:**

1. Copy `rules/design-system-template.md` to `rules/design-system.md`
2. Fill in your brand colors, fonts, and asset paths
3. Generate backgrounds: `node scripts/generate-backgrounds.js`
4. Scan assets: `node scripts/scan-instagram-assets.js`

See [rules/setup.md](rules/setup.md) for complete project setup.

---

## Rule Files

### Core Documentation

| File | Description |
|------|-------------|
| [rules/setup.md](rules/setup.md) | Initial project setup, dependencies, folder structure |
| [rules/design-system-template.md](rules/design-system-template.md) | Template for your brand colors, fonts, and assets |
| [rules/formats.md](rules/formats.md) | Instagram display formats (9:16, 4:5, 1:1) and crop zones |

### Video Creation

| File | Description |
|------|-------------|
| [rules/voiceover.md](rules/voiceover.md) | ElevenLabs integration, scene JSON, timing sync |
| [rules/captions.md](rules/captions.md) | Animated captions with word-level timing and highlighting |
| [rules/animations.md](rules/animations.md) | Spring configs, transitions, animation components |
| [rules/components.md](rules/components.md) | Reusable template components for scenes |

### Assets & Carousels

| File | Description |
|------|-------------|
| [rules/local-assets.md](rules/local-assets.md) | Backgrounds, icons, illustrations management |
| [rules/carousels.md](rules/carousels.md) | Instagram carousel design specs, batch rendering |

---

## Core Dimensions

### Instagram Reels (9:16)

| Property | Value |
|----------|-------|
| Canvas | 1080×1920px (9:16 aspect ratio) |
| Resolution | Minimum 720p, optimal 1080p |
| Format | MP4 (H.264 codec) with AAC audio |
| Frame Rate | 30 FPS |
| Duration | 15-60 seconds (15s recommended for ads) |

### Instagram Carousels (4:5)

| Property | Value |
|----------|-------|
| Canvas | 1080×1350px (4:5 aspect ratio) |
| Slides | 2-10 images per carousel |
| Format | PNG or JPEG |

---

## Safe Zones (Critical)

### Reels Safe Zone Map (1080×1920)

```
┌─────────────────────────────────────┐ 0px
│          TOP DANGER ZONE            │
│   (username, "Reels" branding, UI)  │
│         250px buffer                │
├─────────────────────────────────────┤ ~285px
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │      OPTIMAL CONTENT        │    │
│  │         ZONE                │    │
│  │                             │    │
│  │    880×1350px centered      │    │
│  │    (middle 60% of screen)   │    │
│  │                             │    │
│  │   Place logos, key text,    │    │
│  │   faces, CTAs here          │    │
│  │                             │    │
│  └─────────────────────────────┘    │
│ ←80px                      120px→   │
├─────────────────────────────────────┤ ~1520px
│        BOTTOM DANGER ZONE           │
│  (captions, buttons, audio, CTA)    │
│         400px buffer                │
│     ⚠️ MOST CRITICAL ZONE ⚠️        │
└─────────────────────────────────────┘ 1920px
```

### Safe Zone Constants

```tsx
export const INSTAGRAM_REELS = {
  width: 1080,
  height: 1920,
  aspectRatio: "9:16",
  fps: 30,

  buffer: {
    top: 250,
    bottom: 400,
    left: 80,
    right: 120,
  },

  safeArea: {
    x: 80,
    y: 285,
    width: 880,
    height: 1235,
  },

  // Feed preview (4:5) crops
  feedPreview: {
    cropTop: 285,
    cropBottom: 285,
  },

  // Grid preview (1:1) crops
  gridPreview: {
    cropTop: 420,
    cropBottom: 420,
  },
};
```

See [rules/formats.md](rules/formats.md) for detailed format specifications.

---

## Brand Configuration

### Design System Template

Create `rules/design-system.md` from the template:

```tsx
// TODO: Replace with your brand values
const COLORS = {
  primary: "#YOUR_PRIMARY_COLOR",
  secondary: "#YOUR_SECONDARY_COLOR",
  background: "#YOUR_BG_COLOR",
  foreground: "#YOUR_TEXT_COLOR",
  dark: "#YOUR_DARK_COLOR",
  accent: "#YOUR_ACCENT_COLOR",
};

// TODO: Import your brand fonts
import { loadFont } from "@remotion/google-fonts/YourHeadingFont";
import { loadFont as loadBodyFont } from "@remotion/google-fonts/YourBodyFont";

const { fontFamily: headingFont } = loadFont();
const { fontFamily: bodyFont } = loadBodyFont();

// TODO: Set your logo path
const LOGO_PATH = "your-logo.png";  // In public/ folder
```

See [rules/design-system-template.md](rules/design-system-template.md) for complete configuration.

---

## Ad Structure (4 Scenes)

### Recommended Scene Flow

| Scene | Purpose | Duration | Character |
|-------|---------|----------|-----------|
| **Scene 1: Hook** | Grab attention | 2-4s | `dramatic` |
| **Scene 2: Problem** | Establish pain point | 3-5s | `narrator` |
| **Scene 3: Solution** | Present answer | 3-5s | `expert` |
| **Scene 4: CTA** | Call to action | 2-4s | `calm` |

### Scene 1: Hook
- Large attention-grabbing icon (160-240px)
- Bold headline with keyword highlighted
- Empathetic subtitle
- Dark gradient background

### Scene 2: Problem
- Problem list with icons (55-75px)
- Staggered fade-in animation
- Optional section title
- Serious tone gradient

### Scene 3: Solution
- Large solution icon (140-180px)
- Solution highlight with accent color
- Reassuring subtitle
- Positive brand gradient

### Scene 4: CTA
- Brand logo prominently displayed
- Trust signals (ratings, badges)
- CTA button with arrow
- "Link in Bio" text
- Light background

---

## Voiceover Integration

### Quick Start

```bash
# Generate voiceover with timestamps
node tools/generate.js \
  --scenes remotion/instagram-ads/scenes/ad-example-scenes.json \
  --with-timestamps \
  --output-dir public/audio/instagram-ads/ad-example/

# With pronunciation dictionary for brand names
node tools/generate.js \
  --scenes remotion/instagram-ads/scenes/ad-example-scenes.json \
  --dictionary your-brand \
  --with-timestamps \
  --output-dir public/audio/instagram-ads/ad-example/
```

### Pronunciation Dictionaries

Create custom dictionaries in `dictionaries/` for correct brand name pronunciation:

```xml
<!-- dictionaries/your-brand.pls -->
<lexeme>
  <grapheme>YourBrand</grapheme>
  <alias>Jor Bränd</alias>
</lexeme>
```

See `dictionaries/template.pls` for full format.

### Scene JSON Format

```json
{
  "name": "ad-example",
  "voice": "YourVoiceName",
  "character": "narrator",
  "scenes": [
    {
      "id": "scene1",
      "text": "Hook text here.",
      "duration": 3.5,
      "character": "dramatic"
    },
    {
      "id": "scene2",
      "text": "Problem description.",
      "duration": 4.5
    },
    {
      "id": "scene3",
      "text": "Solution presentation.",
      "duration": 4.0,
      "character": "expert"
    },
    {
      "id": "scene4",
      "text": "Call to action. Brand Name.",
      "duration": 3.0,
      "character": "calm"
    }
  ]
}
```

### Character Presets

| Character | Style | Best For |
|-----------|-------|----------|
| `dramatic` | Intense, emotional | Hooks, problem statements |
| `narrator` | Professional, smooth | General content |
| `expert` | Authoritative | Solutions, legal content |
| `calm` | Soothing, reassuring | CTAs, trust-building |
| `salesperson` | Enthusiastic | Marketing, ads |

See [rules/voiceover.md](rules/voiceover.md) for complete integration guide.

---

## Captions

### TikTok-Style Captions

Generate word-level timestamps for animated captions:

```bash
node tools/generate.js \
  --scenes scenes.json \
  --with-timestamps \
  --output-dir public/audio/ad-example/
```

Key features:
- Word-by-word highlighting
- Page grouping (1-6 words per page)
- Entrance animations
- Text replacement (phonetic → display)

See [rules/captions.md](rules/captions.md) for implementation.

---

## Typography Specifications

### Font Sizes (1080×1920)

| Element | Size | Weight |
|---------|------|--------|
| Hero headline | 64-80px | 700 |
| Section headline | 52-64px | 600 |
| Body/subtitle | 44-52px | 500 |
| Bullet points | 40-48px | 500 |
| Captions | 48-56px | 400 |
| CTA button | 36-48px | 600 |
| Fine print | 24-28px | 400 |

### Text Formatting

```tsx
// High-contrast text (readable on any background)
const contrastTextStyle = {
  color: "#ffffff",
  textShadow: "0 2px 8px rgba(0,0,0,0.8), 0 0 20px rgba(0,0,0,0.5)",
};

// Highlighted word
<span style={{ color: COLORS.accent, fontWeight: 700 }}>
  keyword
</span>
```

---

## Animation Presets

### Spring Configurations

```tsx
// Smooth - professional, no bounce
const SPRING_SMOOTH = { damping: 200 };

// Quick - snappy transitions
const SPRING_QUICK = { damping: 15, stiffness: 100 };

// Bouncy - attention-grabbing
const SPRING_BOUNCY = { damping: 8, stiffness: 200 };
```

### Common Animations

| Animation | Use For |
|-----------|---------|
| Fade in + slide up | Text reveals |
| Scale pop | Icons, logos |
| Staggered list | Bullet points |
| Crossfade | Scene transitions |

See [rules/animations.md](rules/animations.md) for all animation patterns.

---

## Asset Structure

```
public/
├── images/
│   └── instagram-ads/
│       ├── backgrounds/          # 1080×1920 or 1080×1350
│       ├── icons/                # 64-256px elements
│       ├── illustrations/        # 256-800px graphics
│       │   └── ad-example/
│       │       └── final/        # Processed with transparency
│       └── overlays/             # Transparent overlays
├── audio/
│   └── instagram-ads/
│       └── ad-example/           # Per-ad voiceover files
│           ├── ad-example-combined.mp3
│           ├── ad-example-info.json
│           └── ad-example-captions.json
└── your-logo.png
```

See [rules/local-assets.md](rules/local-assets.md) for asset management.

---

## Export Settings

### Reels Export

```bash
npx remotion render AdExample out/reel.mp4 \
  --codec=h264 \
  --crf=18 \
  --audio-codec=aac \
  --audio-bitrate=192k
```

### Carousel Export

```bash
# Batch render all slides
for i in 1 2 3 4 5; do
  npx remotion still remotion/index.ts "Carousel-Slide$i" \
    "public/images/carousels/example/slide$i.png" --overwrite
done
```

---

## Complete Template

```tsx
import React from "react";
import {
  AbsoluteFill,
  Audio,
  Series,
  staticFile,
  useVideoConfig,
} from "remotion";

// TODO: Import from your design-system.md
const COLORS = {
  primary: "#YOUR_PRIMARY",
  secondary: "#YOUR_SECONDARY",
  background: "#YOUR_BG",
  dark: "#YOUR_DARK",
  accent: "#YOUR_ACCENT",
};

export const AdTemplate: React.FC = () => {
  const { fps } = useVideoConfig();

  // Durations from voiceover info.json (actualDuration values)
  const SCENE_DURATIONS = {
    scene1: 3.5,
    scene2: 4.5,
    scene3: 4.0,
    scene4: 3.0,
  };

  const paddingFrames = 5;
  const scene1Frames = Math.round(SCENE_DURATIONS.scene1 * fps) + paddingFrames;
  const scene2Frames = Math.round(SCENE_DURATIONS.scene2 * fps) + paddingFrames;
  const scene3Frames = Math.round(SCENE_DURATIONS.scene3 * fps) + paddingFrames;
  const totalTargetFrames = Math.round(15 * fps);
  const scene4Frames = totalTargetFrames - scene1Frames - scene2Frames - scene3Frames;

  return (
    <AbsoluteFill>
      <Audio src={staticFile("audio/instagram-ads/ad-example/ad-example-combined.mp3")} />

      <Series>
        <Series.Sequence durationInFrames={scene1Frames}>
          <Scene1Hook />
        </Series.Sequence>
        <Series.Sequence durationInFrames={scene2Frames}>
          <Scene2Problem />
        </Series.Sequence>
        <Series.Sequence durationInFrames={scene3Frames}>
          <Scene3Solution />
        </Series.Sequence>
        <Series.Sequence durationInFrames={scene4Frames}>
          <Scene4CTA />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
```

See [rules/components.md](rules/components.md) for scene template components.

---

## Pre-Upload Checklist

### Reels
- [ ] Resolution is 1080×1920 (9:16)
- [ ] All text within safe zones (80px+ from edges)
- [ ] No critical content in top 285px
- [ ] No critical content in bottom 400px
- [ ] Text minimum 40px font size
- [ ] Logo visible in center 1080×1080 (grid thumbnail)
- [ ] Tested 4:5 feed preview (y = 285-1635)
- [ ] Tested 1:1 grid preview (y = 420-1500)
- [ ] Voiceover synced with visuals
- [ ] Captions readable and properly timed
- [ ] Total duration ~15 seconds
- [ ] Tested on actual mobile device

### Carousels
- [ ] Resolution is 1080×1350 (4:5)
- [ ] All text within 80px padding
- [ ] First slide is attention-grabbing
- [ ] CTA with button on final slide
- [ ] Brand logo visible
- [ ] 5-10 slides total
- [ ] Swipe indicators on slides 1-4

---

## Workflow Summary

```bash
# 1. Setup (one time)
cp rules/design-system-template.md rules/design-system.md
# Edit design-system.md with your brand values
cp dictionaries/template.pls dictionaries/your-brand.pls
# Edit your-brand.pls with brand pronunciations
node scripts/generate-backgrounds.js
node scripts/scan-instagram-assets.js

# 2. Create scenes JSON
vim remotion/instagram-ads/scenes/ad-new-scenes.json

# 3. Generate voiceover (with optional dictionary)
node tools/generate.js \
  --scenes remotion/instagram-ads/scenes/ad-new-scenes.json \
  --dictionary your-brand \
  --with-timestamps \
  --output-dir public/audio/instagram-ads/ad-new/

# 4. Create composition
# Use actualDuration values from ad-new-info.json

# 5. Preview
npx remotion studio

# 6. Render
npx remotion render AdNew out/ad-new.mp4 --codec=h264 --crf=18

# 7. Test on mobile before uploading
```

---

## File Structure

```
remotion-ads/
├── SKILL.md                        # This file
├── README.md                       # Quick start guide
├── tools/
│   └── generate.js                 # ElevenLabs voiceover generator
├── dictionaries/
│   ├── template.pls                # Dictionary template
│   └── example.pls                 # Example dictionary
└── rules/
    ├── setup.md
    ├── voiceover.md                # Voiceover & dictionary docs
    ├── captions.md
    ├── animations.md
    ├── components.md
    ├── formats.md
    ├── local-assets.md
    ├── carousels.md
    └── design-system-template.md
```
