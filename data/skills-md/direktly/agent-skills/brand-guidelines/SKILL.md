---
name: brand-guidelines
description: Applies Direkt's official brand colors and typography to any artifact that should follow our look-and-feel. Use it when brand colors, typography, visual formatting, or design standards apply.
license: Complete terms in LICENSE.txt
---

# Direkt Brand Styling

## Overview

Use this skill to apply Direkt’s visual identity consistently across products, documents, presentations, UI mockups, and marketing assets.

**Keywords**: branding, corporate identity, visual identity, styling, brand colors, typography, Direkt brand, visual formatting, visual design, fintech branding

## Brand Guidelines

### Colors

**Base Colors (UI Foundation):**

- Dark Background: `#120018` — Primary dark mode background
- Light Background: `#FAFAFC` — Primary light mode background
- Mid Gray: `#B0B0B8` — Secondary UI elements, borders, icons
- Light Gray: `#E6E6ED` — Subtle backgrounds, cards, dividers

**Purple Palette (Core Brand Identity):**

- Grape: `#8A05BE` — Primary brand color, CTAs, main highlights  
- Violet: `#820AD1` — Secondary brand accent, links, hover states  
- Orchid: `#BD0FEA` — Vibrant highlight, gradients, special emphasis  
- Plum: `#4C0677` — Dark purple, headers, dark UI surfaces  
- Eggplant: `#2F0549` — Deepest tone, premium backgrounds, hero sections

**Text Colors:**
- Ink: `#000000` - Headings on light
- Ash: `#3C3C3C` - Body text on light
- Slate: `#999999` - Secondary text, placeholders
- Snow: `#FFFFFF` - Text on dark backgrounds

**Accent Palette (Signal Colors – Use Sparingly):**

- Lime: `#D6E303` — Success, attention, positive signals  
- Coral: `#FF7D6B` — Alerts, warnings, warm emphasis  
- Aqua: `#6FF5FF` — Info states, links, data visualization highlights  

---

### Typography

- **Headings**: Phonic (fallback: Arial, system-ui)
- **Body Text**: Martina Plantijn (fallback: Georgia, serif)
- **Note**: Fonts should be pre-installed in your environment for best visual consistency.

---

## Features

### Smart Font Application

- Applies Phonic font to headings (24pt and larger)
- Applies Martina Plantijn font to body text
- Automatically falls back to Arial/Georgia if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings (24pt+): Phonic font
- Body text: Martina Plantijn font
- Smart color selection based on background
- Preserves text hierarchy and formatting

### Shapes and Accent Colors

- Non-text shapes use accent colors
- Cycles through lime, coral, and aqua accents
- Maintains visual interest while staying on-brand

---

## Technical Details

### Font Management

- Uses system-installed Phonic and Martina Plantijn fonts when available
- Provides automatic fallback to Arial (headings) and Georgia (body)
- No font installation required - works with existing system fonts
- For best results, pre-install Phonic and Martina Plantijn fonts in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Convert to RGB/CMYK depending on platform needs
- Maintains color fidelity across different systems
