---
name: pitolandia-visual-identity
description: Visual identity system for Pitolandia, a consent-first date planning service. Use when generating images, illustrations, or visual content for Pitolandia brand materials. Triggers include requests for venue illustrations, food/drink specimen plates, desert landscapes, or any visual asset in the "Sonoran Gothic Surrealism" aesthetic—19th-century copperplate engravings with hand-tinted watercolor washes. Also use when transforming source photographs into the Pitolandia style for fair-use purposes, or when crafting AI image generation prompts for Pitolandia content.
---

# Pitolandia Visual Identity

**Sonoran Gothic Surrealism:** 19th-century intaglio engravings documenting 21st-century Arizona courtship.

## Brand Philosophy

Pitolandia facilitates modern, equitable romantic connections—values associated with fluidity and minimalism. Yet we adopt a Victorian visual language: rigid, authoritative, codified. This tension is our most potent asset.

**The Resolution:** Victorian authority provides structure for safety. Surrealist collage provides absurdity for joy. A date planned through Pitolandia is a "Treaty of Connection"—codified with the gravity of a steel engraving, yet unburdened by the stifling norms of the past.

**Mottos:**
- External/Tagline: *Gravitas with a Wink.*
- Internal/Philosophy: *Structure for Safety. Absurdity for Freedom.*

---

## Core Aesthetic

- **Medium:** Copperplate engraving / steel etching / wood engraving (1840-1910 style)
- **Shading:** Cross-hatching and stippling only—no gradients, no solid fills
- **Color:** Hand-tinted watercolor washes sitting behind/over black linework
- **Ground:** Aged vellum (#F5F0E6), never pure white (#FFFFFF)
- **Imperfection:** Slight wobble, ink spread at intersections, plate wear

---

## Unified Color Palette (Strict)

### Foundation — Dark Mode & Linework
| Color | Hex | Role |
|-------|-----|------|
| Obsidian | #171103 | Canyon shadow depth. Primary dark mode. |
| Charcoal | #463928 | Desert at dusk. Secondary dark, borders. |
| Midnight | #1E2832 | Night sky. Deep shadow in illustrations (never food). |

### Heat & Energy — Accents
| Color | Hex | Role | Apply To |
|-------|-----|------|----------|
| Oxblood | #722F37 | HEAT | Rare meat, red wine, brick, leather, chiles, passion |
| Ember Gold | #C9A227 | ENERGY | Light sources, beer, cheese, bread, warmth, CTAs |
| Sonoran Copper | #B87333 | TEXTURE | Roasted/fried foods, metal, adobe, rust, craft |

### Life & Action
| Color | Hex | Role | Apply To |
|-------|-----|------|----------|
| Saguaro | #4A5D4A | LIFE | Foliage, salads, herbs, oxidized copper, landscape |
| Monsoon Teal | #407D6C | ACTION | Interactive UI states, links, palo verde after rain |

### Structure & Ground
| Color | Hex | Role | Apply To |
|-------|-----|------|----------|
| Bone | #DCD0C0 | STRUCTURE | Plates, napkins, concrete, limestone, stucco |
| Aged Vellum | #F5F0E6 | GROUND | Primary paper ground for illustrations |
| Parchment | #FCF5E5 | SURFACE | Light mode UI surfaces, cards, long-form reading |

**Rule:** Maximum 3 palette colors per image plus black linework and paper ground.

---

## Quick Prompt Framework

```
[STYLE]: 19th-century copperplate engraving
[TECHNIQUE]: Variable-weight linework, cross-hatching, stippling, hand-tinted washes
[PALETTE]: [2-3 colors from Material Palette] as transparent washes
[GROUND]: Aged vellum (#F5F0E6)
[REFERENCE]: Gustave Doré, Harper's Weekly, Victorian scientific plates
```

**Negative prompt (always include):**
```
photorealistic, 3D render, digital art, vector, smooth gradients, airbrushed, glossy, neon glow, drop shadow, modern illustration, cartoon, anime, minimalist, pure white background, saturated colors
```

---

## Subject Treatments

- **Venues:** 1890s travelogue/architectural lithograph style
- **Food/Drink:** Victorian specimen plate, encyclopedic precision
- **Landscape:** Survey expedition illustration, botanical accuracy for flora
- **Modern Objects:** Halftone/grain overlay ("Wondermark anachronism")

---

## Full Reference

For complete specifications including:
- Detailed linework and shading parameters
- Typography guidelines (UI and in-image)
- Composition frameworks
- Food texture rendering charts
- Desert flora guide
- Source image transformation protocol
- Voice and verbal identity
- Quality checklist
- CSS design tokens

**Read:** [references/visual-identity-directive.md](references/visual-identity-directive.md)
