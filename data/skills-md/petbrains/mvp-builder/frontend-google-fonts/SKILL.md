---
name: frontend-google-fonts
description: Typography setup with Google Fonts for Next.js + Tailwind projects. Use when choosing fonts, need font pairing recommendations (SaaS, editorial, corporate presets), or setting up optimized font loading. Includes ready-to-use configurations and performance best practices.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Google Fonts

Typography setup for web projects. Font pairings + performance optimization.

## When to Use

- Setting up project fonts
- Need font pairing recommendations
- Optimizing font loading

## Process

**SELECT → CONFIGURE → APPLY**

1. Choose fonts for project type
2. Configure in Next.js
3. Add to Tailwind

## Quick Start (Next.js)

```tsx
// lib/fonts.ts
import { Inter, Plus_Jakarta_Sans } from 'next/font/google'

export const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

export const jakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-jakarta',
})

// app/layout.tsx
<html className={`${inter.variable} ${jakarta.variable}`}>

// tailwind.config.ts
fontFamily: {
  sans: ['var(--font-inter)'],
  display: ['var(--font-jakarta)'],
}
```

## Font Pairing Presets

```yaml
Modern SaaS:
  Heading: Plus Jakarta Sans
  Body: Inter

Corporate:
  Heading: Source Sans 3
  Body: Source Serif 4

Editorial:
  Heading: Playfair Display
  Body: Lora

Tech/Dev:
  Heading: Geist
  Body: Inter
  Code: Geist Mono

Startup/Friendly:
  Heading: Outfit
  Body: Nunito
```

## Top Font Choices

| Font | Category | Best For |
|------|----------|----------|
| Inter | Sans | Universal default |
| Plus Jakarta Sans | Sans | Modern SaaS |
| DM Sans | Sans | Clean startups |
| Geist | Sans | Dev tools |
| Playfair Display | Serif | Elegant headlines |
| Lora | Serif | Long-form reading |
| JetBrains Mono | Mono | Code blocks |

## Performance Tips

```yaml
Variable fonts:     Use Inter, not Roboto with weight array
Subset:             Only 'latin' unless multilingual
Display swap:       Always set display: 'swap'
Self-host:          next/font auto self-hosts (no external requests)
```

## Typography Scale

```yaml
text-xs:   12px
text-sm:   14px
text-base: 16px
text-lg:   18px
text-xl:   20px
text-2xl:  24px
text-3xl:  30px
text-4xl:  36px
```

## Decision by Project Type

| Type | Heading | Body |
|------|---------|------|
| SaaS Dashboard | Inter | Inter |
| Marketing Site | Plus Jakarta | Inter |
| Blog | Playfair Display | Lora |
| Dev Docs | Geist | Inter |
| Enterprise | Source Sans | Source Serif |

**Resources:**
- https://fonts.google.com
- https://www.fontpair.co
- https://typescale.com
