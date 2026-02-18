---
name: fonts
description: Reference for selecting distinctive typography. Includes font recommendations by vibe, category, archetype, and pairing guidelines for Next.js projects.
---

# Skill: Fonts

Reference for selecting distinctive typography. Avoid overused fonts (Helvetica, Arial, Roboto, Open Sans, Montserrat, Playfair Display, Poppins, Lato).

All fonts below are **free via Google Fonts** and work with `next/font/google`.

---

## By Vibe

| Vibe | Fonts |
|------|-------|
| Editorial/Literary | Newsreader, Lora, EB Garamond, Cormorant, Spectral |
| Luxury/Fashion | Cormorant Garamond, Bodoni Moda, Libre Bodoni, Fraunces |
| Modern Clean | Space Grotesk, DM Sans, Plus Jakarta Sans, Manrope |
| Bold/Impact | Bricolage Grotesque, League Spartan, Syne, Outfit |
| Playful | Rubik, Nunito, Comfortaa, Quicksand |
| Technical/Future | Space Mono, JetBrains Mono, Fira Code, IBM Plex Mono |
| Understated | Mulish, Chivo, Proza Libre, Work Sans |

---

## Serif

| Font | Use Case |
|------|----------|
| Cormorant | High-contrast elegance, editorial headers, luxury feel |
| Cormorant Garamond | Sophisticated authority, refined editorial |
| Lora | Elegant body text, blog content, readable at small sizes |
| EB Garamond | Classic book typography, long-form reading |
| Newsreader | Magazine/editorial layouts, journalistic feel |
| Spectral | Balanced body text with character |
| Fraunces | Modern variable serif with personality, 9 weights |
| Bodoni Moda | Didone-style headlines, fashion/luxury |
| Libre Bodoni | Clean Bodoni alternative, display use |
| Libre Baskerville | Literary feel (Mrs Eaves alternative) |
| Young Serif | Contemporary headlines with warmth |
| Instrument Serif | Modern refined serif, editorial |
| Alegreya | Distinctive letterforms, sophisticated portfolios |
| BioRhyme | Slab serif for editorial layouts, 7 weights |

---

## Sans Serif

| Font | Use Case |
|------|----------|
| Space Grotesk | Contemporary branding, geometric personality |
| DM Sans | Humanist design, Futura alternative, distinctive "G" |
| Plus Jakarta Sans | Modern UI, distinctive character |
| Manrope | Clean geometric sans, 7 weights |
| Outfit | Geometric humanist, modern portfolios |
| Bricolage Grotesque | Bold headlines, expressive with personality |
| Syne | Tactile uniqueness, creative portfolios |
| Chivo | Versatile workhorse, 9 weights |
| Work Sans | Screen-optimized, friendly professional |
| Mulish | Humanist-geometric hybrid, variable font |
| Epilogue | Geometric with warmth |
| Proza Libre | Understated sophistication, editorial |
| League Spartan | Condensed geometric, impactful headers |
| Inter | UI-focused, excellent legibility (use sparingly - becoming common) |

---

## Display

| Font | Use Case |
|------|----------|
| Bricolage Grotesque | Expressive headlines, bold personality |
| Fraunces | Variable serif with dramatic weight range |
| Instrument Serif | Modern editorial headlines |
| Young Serif | Warm contemporary headers |
| Abril Fatface | Bold Didone-style display |
| Rubik Glitch | Experimental/tech aesthetic |
| Silkscreen | Retro pixel/terminal aesthetic |
| Aboreto | Distinctive display style |
| Red Rose | Expressive headlines |

---

## Monospace

| Font | Use Case |
|------|----------|
| Space Mono | Developer portfolios, distinctive style |
| JetBrains Mono | Code display, excellent legibility |
| Fira Code | Programming with ligatures |
| IBM Plex Mono | Technical documentation, professional |
| Inconsolata | Classic code aesthetic |
| Source Code Pro | Clean, versatile monospace |

---

## By Archetype

| Person | Direction |
|--------|-----------|
| Writer/Editor | Newsreader, Lora, EB Garamond, Spectral |
| Designer | Space Grotesk, Bricolage Grotesque, Fraunces |
| Developer | Space Mono, JetBrains Mono, IBM Plex Mono |
| Strategist | Cormorant Garamond, Chivo, DM Sans |
| Artist | Syne, Rubik, Instrument Serif |
| Luxury/Fashion | Bodoni Moda, Cormorant, Libre Bodoni |

---

## Recommended Pairings

| Style | Display + Body |
|-------|----------------|
| Editorial | Instrument Serif + DM Sans |
| Modern | Bricolage Grotesque + Space Grotesk |
| Literary | Cormorant + Spectral |
| Tech | Space Mono + Inter |
| Luxury | Bodoni Moda + Manrope |
| Creative | Fraunces + Work Sans |
| Minimal | Young Serif + Plus Jakarta Sans |

---

## Usage in Next.js

```tsx
import { Space_Grotesk, Newsreader } from 'next/font/google';

const heading = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-heading'
});

const body = Newsreader({
  subsets: ['latin'],
  variable: '--font-body'
});
```

---

## Pairing Rules

- Contrast categories: serif display + sans body (or reverse)
- One dominant, one supporting (never compete for attention)
- Match x-heights when possible for visual harmony
- Limit to 3 fonts maximum per site
