---
name: frontend-aesthetics
description: Prevents generic AI-generated designs by guiding typography, color, motion, and background choices. Use when creating frontend designs, landing pages, dashboards, or any UI/UX work. Helps avoid the "AI slop" aesthetic.
---

# Frontend Aesthetics Skill

Based on Anthropic's formula for improving frontend design through steerability.

## The Problem

LLMs converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic - Inter fonts, purple gradients on white backgrounds, and minimal animations.

## Instructions

Make creative, distinctive frontends that surprise and delight. Focus on these four dimensions:

### Typography

Choose fonts that are beautiful, unique, and interesting.

**Never use**: Inter, Roboto, Open Sans, Lato, Arial, default system fonts

**Good choices**:
- Code aesthetic: JetBrains Mono, Fira Code, Space Grotesk
- Editorial: Playfair Display, Crimson Pro, Newsreader
- Technical: IBM Plex family, Source Sans 3
- Distinctive: Bricolage Grotesque, Syne, Outfit, Plus Jakarta Sans
- Premium: Cabinet Grotesk, Satoshi, General Sans, Clash Display

**Pairing principle**: High contrast = interesting. Display + monospace, serif + geometric sans, variable font across weights.

**Use extremes**: 100/200 weight vs 800/900, not 400 vs 600. Size jumps of 3x+, not 1.5x.

Pick one distinctive font, use it decisively. Load from Google Fonts.

### Color & Theme

Commit to a cohesive aesthetic. Use CSS variables for consistency.

**Dominant colors with sharp accents** outperform timid, evenly-distributed palettes.

Draw inspiration from:
- IDE themes (Dracula, Nord, One Dark, Catppuccin, Tokyo Night)
- Cultural aesthetics (Japanese minimalism, Scandinavian design, Brutalism)
- Industry-specific palettes (Finance: navy/gold, Health: teal/white, Gaming: neon/dark)

**Avoid**: Purple gradients on white backgrounds (the ultimate AI slop indicator)

### Motion

Use animations for effects and micro-interactions.

- Prioritize CSS-only solutions for HTML
- Use Motion library for React when available
- Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions

### Backgrounds

Create atmosphere and depth rather than defaulting to solid colors.

- Layer CSS gradients (radial + linear combinations)
- Use geometric patterns or grids
- Add contextual effects that match the overall aesthetic
- Consider noise textures, grain, or subtle animations

## Tailwind CSS v4 Compatibility

**CRITICAL**: Tailwind v4 has breaking changes. Follow these rules:

### Spacing
- **Never use**: `space-x-*`, `space-y-*` (removed in v4)
- **Always use**: `gap-*` with flex/grid containers instead

```tsx
// WRONG (Tailwind v3 only)
<div className="flex space-x-4">

// CORRECT (Tailwind v4 compatible)
<div className="flex gap-4">
```

### Config Loading
- Tailwind v4 doesn't auto-load `tailwind.config.ts`
- Add `@config "../tailwind.config.ts"` to your CSS file if using a config

```css
/* app/globals.css */
@import "tailwindcss";
@config "../tailwind.config.ts";
```

### CSS Reset Conflicts
- Don't add custom `* { margin: 0 }` resets - they break `mx-auto`, `my-*` utilities
- Let Tailwind's preflight handle resets

### Package.json
- Add `"type": "module"` to avoid Node.js ESM warnings

## What to Avoid

- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (purple gradients on white)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character
- Space Grotesk (even this is becoming overused)
- `space-x-*` and `space-y-*` utilities (use `gap-*` instead)

## Key Principle

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics.

You still tend to converge on common choices across generations. Avoid this: it is critical that you think outside the box!

## Example: Theme Ideas

Instead of the default "tech purple":

1. **Obsidian Terminal**: Deep black (#0a0a0a), electric green (#00ff9f), JetBrains Mono
2. **Editorial Luxury**: Cream (#faf9f6), deep navy (#1a1a2e), Playfair Display + Source Sans
3. **Neon Brutalist**: Pure white, bold black, hot pink accent (#ff006e), IBM Plex Mono
4. **Nordic Minimal**: Cool gray (#e5e5e5), slate blue (#475569), Outfit
5. **Retro Computing**: Amber on dark (#ffb000 on #1a1a1a), VT323 or IBM Plex Mono
