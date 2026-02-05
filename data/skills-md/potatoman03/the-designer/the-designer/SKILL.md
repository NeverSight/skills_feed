---
name: the-designer
description: Create distinctive frontend interfaces with soul. Context-aware — applies different rules for marketing sites vs dashboards/apps. Marketing sites get dramatic typography, procedural visuals, and editorial layouts. Dashboards get high density, functional cards, and data-first design.
license: MIT
author: The Designer Collective
version: 5.0.0
---

# The Designer — Interfaces With Soul

This skill creates interfaces that feel **crafted by human hands**, not assembled from a kit. Every project gets its own personality. Every screen tells part of a story. The goal is memorable distinction, not safe consistency.

> **Philosophy**: Design is authorship. A great interface has a point of view — it makes decisions that lesser designers wouldn't dare. Safe choices produce forgettable work. Take a stand. Let the design have opinions.

> **Core Belief**: Users don't remember "clean" — they remember **feeling something**. Delight, intrigue, comfort, surprise. An interface should evoke emotion, not just display information.

---

## FIRST: Identify the Context

Before applying ANY rules, determine what you're building. The approach differs dramatically:

### Marketing Sites / Landing Pages
- **Goal**: Impress, convert, tell a story
- **Density**: Low (60%+ whitespace)
- **Typography**: Dramatic display sizes, emotional
- **Visual interest**: Procedural/generative backgrounds, texture, interactive elements
- **Cards**: AVOID — use editorial layouts, numbered lists
- **Hero sections**: Yes — big statements, atmosphere
- **Animation**: Expressive, scroll-driven reveals

### Dashboards / Admin Panels / Apps
- **Goal**: Inform, enable action, show data
- **Density**: High — information-rich, compact
- **Typography**: Functional, readable, restrained sizes
- **Visual interest**: Minimal — focus on data visualization, not decoration
- **Cards**: YES — cards are appropriate for dashboard widgets
- **Hero sections**: NO — get to the data immediately
- **Animation**: Minimal, functional transitions only
- **Whitespace**: 30-40%, not 60%+

### Key Differences

| Aspect | Marketing Site | Dashboard/App |
|--------|---------------|---------------|
| Hero section | Yes, dramatic | No, straight to content |
| Decorative visuals | Yes, generative/procedural | No, data viz only |
| Card grids | Never for features | Yes, for widgets |
| Display typography | Yes | Minimal, headers only |
| Information density | Low | High |
| Whitespace | 60%+ | 30-40% |
| Signature animation | Yes | Subtle indicators only |

**If building a dashboard**: Skip the Five Commitments, skip decorative visuals, use functional card layouts, prioritize data density and usability over emotional impact.

---

## The Five Commitments (Marketing Sites Only)

**Skip this for dashboards/apps** — go straight to building functional UI.

For marketing sites, before writing any code, make five binding decisions:

### 1. The Story
What narrative does this interface tell? Not features — *feeling*.
- "A calm library where thoughts settle into place"
- "A machine humming with quiet intelligence"
- "A letter from a friend who knows exactly what you need"

Write one sentence. Every design decision serves this story.

### 2. The Tension
Great design holds opposing forces in balance. Pick your spectrum:
- Playful ↔ Serious
- Dense ↔ Spacious
- Warm ↔ Cool
- Organic ↔ Geometric
- Loud ↔ Quiet

Where does this project sit? (e.g., "70% serious, 30% playful")

### 3. The Signature
The ONE element that makes this unmistakably *this*:
- A specific animation that appears nowhere else
- A color that burns into memory
- A typographic treatment that becomes the brand

If someone sees a screenshot with no logo, they should still know it's yours.

### 4. The Material
What is this interface *made of*? Physical metaphor drives texture:
- Paper and ink (soft, tactile, warm)
- Glass and light (transparency, refraction, glow)
- Stone and shadow (weight, depth, permanence)
- Metal and precision (sharp edges, industrial)

### 5. The Gesture
How does interaction feel in the hand?
- Snappy and immediate (arcade button)
- Smooth and continuous (silk ribbon)
- Weighted and deliberate (heavy door)
- Springy and alive (rubber ball)

---

## Layer 1: Typography — Voice, Not Just Text

Typography is the single most impactful decision. Type is **voice** — choose fonts that would sound right reading your content aloud.

### The Type Stack
Every project needs exactly THREE roles:

| Role | Purpose | Example Pairings |
|------|---------|------------------|
| **Voice** | Headlines, statements, personality | Newsreader, Cormorant, Playfair Display, Syne |
| **Work** | Body text, UI, readability | Outfit, Satoshi, General Sans, Geist |
| **Tech** | Code, data, precision | JetBrains Mono, Azeret Mono, Space Mono |

### Typography Rules

| Context | Size | Line Height | Letter Spacing |
|---------|------|-------------|----------------|
| Display | clamp(3rem, 8vw, 8rem) | 1.0–1.1 | -0.02em to -0.04em |
| Headings | 2rem–3rem | 1.1–1.2 | -0.01em |
| Body | 1rem–1.125rem | 1.6–1.7 | 0 |
| Captions | 0.75rem–0.875rem | 1.4 | 0.02em–0.05em |

### Text Measure (Line Length)
Body text MUST maintain readable line length:
- **Optimal**: 45–75 characters per line (65 is ideal)
- **Minimum width**: `max-w-prose` (65ch) or `max-w-2xl` (42rem/672px)
- **NEVER** constrain body text narrower than 20rem (320px)

If text wraps at 2–3 words per line, the container is too narrow. Always verify text measure visually.

### BANNED Fonts
Inter, Roboto, Arial, system-ui, Poppins, Open Sans, Montserrat — these signal "I didn't choose."

### Font Loading — Required Setup

Always load fonts in `index.html` head, NOT via CSS @import:

```html
<!-- index.html -->
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=YOUR_FONTS&display=swap" rel="stylesheet" />
</head>
```

Then reference in CSS:
```css
@theme {
  --font-voice: "Cormorant Garamond", "Times New Roman", serif;
  --font-work: "Outfit", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;
}
```

---

## Layer 2: Color — Emotion, Not Decoration

**Two colors. Maximum three.** Restraint creates sophistication.

### The Palette Formula
1. **One dominant** — 60% of the interface (your ground)
2. **One accent** — 10% or less, maximum impact (your spark)
3. **Derive everything else** — surfaces, text, borders from lightness/opacity variations

### Color Rules
- Never pure `#000` or `#FFF` — use near-blacks and near-whites with subtle hue
- Accent is sacred — use only on THE most important action per screen
- Dark mode is a different *mood*, not inverted math
- Interactions increase contrast — hover/focus states are MORE visible

### BANNED
- Gradients (all types — linear, radial, any)
- Purple-on-white (the AI aesthetic)
- Rainbow palettes without clear hierarchy
- Color as the only status indicator

---

## Layer 3: Space — Rhythm, Not Just Margins

**60% of any viewport should be nothing.** Empty space is the silence that makes the music.

### Spacing Scale
Use a consistent scale. Never arbitrary values.

| Token | Size | Use |
|-------|------|-----|
| xs | 0.25rem | Hairline gaps |
| sm | 0.5rem | Tight pairs |
| md | 1rem | Related elements |
| lg | 2rem | Grouped sections |
| xl | 4rem | Major breaks |
| 2xl | 8rem | Dramatic pauses |

### Key Rule
Section spacing = 3–5× element spacing. If cards have 1rem gaps, sections need 4–6rem padding.

### Layout Principles
- **Asymmetric grids** outperform symmetric ones
- **One grid-breaking element** per section creates tension
- **Let browser size things** — flex/grid over JS measurements
- **Optical alignment** — adjust ±1px when perception beats geometry

---

## Layer 4: Motion — Narrative, Not Decoration

Every animation must have a **named job**. If it doesn't fit a category, it shouldn't exist.

### Motion Taxonomy

| Type | Purpose | Timing |
|------|---------|--------|
| **Structural** | Scroll reveals, layout changes | Tied to scroll position |
| **Connective** | Page/state transitions | 400–800ms |
| **Communicative** | Hover, click, focus feedback | 100–200ms |
| **Atmospheric** | Idle animations, ambient life | 2000ms+ loops |

### Motion Rules
- **CSS first** — use JS libraries only when CSS can't achieve it
- **Compositor-friendly** — only animate `transform` and `opacity`
- **Never `transition: all`** — list specific properties
- **Honor `prefers-reduced-motion`** — always
- **One signature moment** — not animation on everything

### Easing
- **Snappy UI**: `cubic-bezier(0.16, 1, 0.3, 1)`
- **Smooth decel**: `cubic-bezier(0.25, 1, 0.5, 1)`
- **Cinematic**: `cubic-bezier(0.76, 0, 0.24, 1)`

---

## Layer 5: Components — Characters, Not Widgets

Components have personality. They're not just reusable — they have opinions.

### Component Philosophy
- **Composition over configuration** — compound components over boolean props
- **Variants as a system** — not ad-hoc className strings
- **States are story beats** — empty, loading, error, success all designed
- **Cards are not the default** — most content doesn't need a box

### Buttons & Text on Backgrounds — CRITICAL

Text on colored backgrounds often fails to render when using only Tailwind utility classes. **Always create dedicated CSS classes with explicit colors and `!important`.**

#### Required: Create These Button Classes in index.css

```css
/* REQUIRED — Add to every project's index.css */
.btn-primary {
  display: inline-block;
  font-family: var(--font-work);
  font-size: 1rem;
  letter-spacing: 0.025em;
  padding: 1rem 2rem;
  background-color: var(--color-primary);
  color: var(--color-background) !important;
  transition: background-color 150ms ease;
}
.btn-primary:hover { background-color: var(--color-primary-hover); }

.btn-secondary {
  display: inline-block;
  font-family: var(--font-work);
  font-size: 1rem;
  letter-spacing: 0.025em;
  padding: 1rem 2rem;
  background-color: var(--color-background);
  color: var(--color-primary) !important;
  transition: background-color 150ms ease;
}

.btn-sm { font-size: 0.875rem; padding: 0.75rem 1.5rem; }
```

#### Why This Matters
- `a { color: inherit }` in CSS resets overrides utility classes
- Z-index stacking with overlays can hide text
- Tailwind utilities like `text-paper` don't use `!important`

#### Rules
1. **NEVER** use `bg-ink text-paper` utilities alone for buttons
2. **ALWAYS** use `.btn-primary`, `.btn-secondary` classes
3. **ALWAYS** include `!important` on color declarations
4. For any text on a colored background, use explicit CSS classes, not utilities

### When to Use Cards

**In Dashboards/Apps** — Cards are APPROPRIATE for:
- Stat widgets showing metrics
- Data summaries and KPIs
- Settings panels and sections
- List items that need visual grouping
- Any discrete, actionable content block

**In Marketing Sites** — Cards are appropriate for:
- Selectable/clickable items
- Content that will be manipulated (dragged, dismissed)
- Truly discrete items in a collection

### When NOT to Use Cards (Marketing Sites Only)
- Feature lists (use numbered lists or editorial text instead)
- Static marketing information
- "Wrapping things to look organized"

**Note**: The "feature card grid" ban applies to MARKETING SITES showing features as uniform icon+title+description cards. Dashboard stat cards and widget cards are completely different and encouraged.

---

## Layer 6: Texture — Touch, Not Flatness

Interfaces should feel **made of something**. Achieve texture through shadows, borders, and noise — not gradients.

### Material Treatments

| Material | Technique |
|----------|-----------|
| Paper | Subtle inset shadows, warm surface colors |
| Glass | `backdrop-filter: blur()`, translucent borders |
| Metal | Sharp inset highlights, hard shadows |
| Solid | Border + slight surface elevation |

### Grain
Subtle noise (2–4% opacity) adds analog warmth. Apply as a fixed overlay.

**CRITICAL**: When using CSS `::before` pseudo-elements for texture overlays, use `z-index: -1` (not positive values). Positive z-index will cover content and make text/buttons invisible.

### Shadows
Layered shadows (2–3 layers) feel more realistic than single-layer stock shadows.

---

## Layer 7: States — Every Moment Designed

Every state is a moment in the user's journey. Design them all.

| State | Character | Approach |
|-------|-----------|----------|
| **Empty** | The Beginning | Inviting, clear next step |
| **Loading** | Anticipation | Skeleton or simple text, never jarring |
| **Error** | The Setback | Helpful, shows the way out |
| **Success** | Victory | Celebratory but brief |

### State Rules
- No dead ends — every screen offers a next step
- Loading states have minimum visible time (300–500ms) to avoid flicker
- Error messages tell users how to fix it, not just what went wrong

---

## Layer 8: Accessibility — Care, Not Compliance

Accessibility isn't a checklist — it's caring about every user.

### Non-Negotiables
- Visible focus rings (`:focus-visible`)
- 44px minimum touch targets
- Keyboard navigation for all flows
- Labels on all form inputs
- Color is never the only indicator
- `prefers-reduced-motion` respected

### Form Rules
- Don't pre-disable submit — let users discover what's wrong
- Don't block paste or input types
- Error messages next to fields, not just at top
- Mobile inputs ≥16px to prevent iOS zoom

---

## The AI Slop Hall of Shame

These patterns are **BANNED on marketing sites**. Dashboards have different rules.

### 1. The Feature Card Grid (Marketing Sites Only)
```
❌ NEVER ON MARKETING SITES:
┌───────────┐ ┌───────────┐ ┌───────────┐
│ (○ icon)  │ │ (○ icon)  │ │ (○ icon)  │
│ Heading   │ │ Heading   │ │ Heading   │
│ Desc text │ │ Desc text │ │ Desc text │
└───────────┘ └───────────┘ └───────────┘
```
Uniform rounded-corner cards with icon-in-circle, heading, description for FEATURES. Lazy marketing pattern.

**Instead on marketing sites**: Asymmetric layouts, text-only sections, editorial spreads, numbered lists.

**ON DASHBOARDS**: Card grids for stats/widgets are FINE and expected. This rule doesn't apply.

### 2. Icon-in-Circle
Icons inside colored circles or rounded squares. Visual shorthand for "I didn't think about this."

**Instead**: Icons inline with text, large illustrations, or no icons at all.

### 3. Gradients
Any use of `linear-gradient`, `radial-gradient`, or gradient backgrounds.

**Instead**: Solid colors, texture, layered surfaces.

### 4. Template Structure
Hero → Feature Cards → Testimonials → CTA. Every AI site ever.

**Instead**: Story-driven structure unique to this content.

### Complete Ban List

| Never | Instead |
|-------|---------|
| Feature card grids | Asymmetric layouts, text sections |
| Icons in circles | Inline icons or none |
| Gradients | Solid colors + texture |
| Uniform rounded corners | Mix sharp and rounded with intention |
| Symmetrical 3-column | Varied column widths, asymmetry |
| Animation on everything | One signature moment |
| Generic fonts | Distinctive typefaces |
| Pure black/white | Near-black/white with hue |
| Template layouts | Content-driven structure |
| Drop shadows on every card | Strategic elevation, most flat |

---

## Feature Presentation Without Slop

When you need to present features, use these approaches:

**Editorial Spread**: One large hero feature, smaller supporting details below.

**Numbered List**: Simple, scannable, no boxes.
```
01  Feature name — description flows naturally
02  Another feature — no icons in circles
03  Third feature — typography provides hierarchy
```

**Single Focus**: One thing, dramatically. Everything else secondary.

**Inline Flow**: Weave features into narrative prose.

**Comparison Table**: When actually comparing things.

---

## Tailwind v4 CSS Template — Use This Structure

Every project MUST use this index.css structure. Copy and adapt colors/fonts for each project.

```css
@import "tailwindcss";

@theme {
  /* COLORS — Choose 2-3 colors appropriate to the project
     Examples:
     - Warm/friendly: cream backgrounds, deep brown primary, terracotta accent
     - Professional/serious: slate backgrounds, near-black primary, blue accent
     - Tech/modern: dark surfaces, white text, electric accent

     Always define primary, background, and ONE accent */
  --color-primary: /* dark text/UI color */;
  --color-primary-hover: /* slightly lighter */;
  --color-primary-muted: /* for secondary text */;
  --color-background: /* main surface */;
  --color-background-alt: /* cards, sections */;
  --color-accent: /* ONE accent for key actions */;

  /* FONTS — Choose fonts that match the project personality
     Load via Google Fonts in index.html, not CSS @import */
  --font-voice: /* display/headlines - serif or distinctive sans */;
  --font-work: /* body/UI - readable sans */;
  --font-mono: /* code/data - monospace */;

  /* TYPOGRAPHY — Safe to define */
  --font-size-display: clamp(3rem, 8vw, 6rem);
  --font-size-display-sm: clamp(2rem, 5vw, 3.5rem);
}

/* BASE STYLES */
html {
  font-family: var(--font-work);
  color: var(--color-primary);
  background-color: var(--color-background);
}

/* TYPOGRAPHY UTILITIES */
.font-voice { font-family: var(--font-voice); }
.font-work { font-family: var(--font-work); }
.text-display {
  font-family: var(--font-voice);
  font-size: var(--font-size-display);
  line-height: 1.0;
  letter-spacing: -0.03em;
}

/* REQUIRED BUTTON CLASSES */
.btn-primary {
  display: inline-block;
  font-family: var(--font-work);
  font-size: 1rem;
  padding: 1rem 2rem;
  background-color: var(--color-primary);
  color: var(--color-background) !important;
  transition: background-color 150ms ease;
}
.btn-primary:hover { background-color: var(--color-primary-hover); }

.btn-secondary {
  display: inline-block;
  font-family: var(--font-work);
  font-size: 1rem;
  padding: 1rem 2rem;
  background-color: var(--color-background);
  color: var(--color-primary) !important;
  transition: background-color 150ms ease;
}
.btn-secondary:hover { background-color: var(--color-background-alt); }

.btn-sm { font-size: 0.875rem; padding: 0.75rem 1.5rem; }

/* TEXTURE OVERLAY — z-index: -1 is critical */
.paper-texture { position: relative; }
.paper-texture::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* noise SVG */
  opacity: 0.03;
  pointer-events: none;
  z-index: -1; /* MUST be negative or it covers content */
}
```

### Critical @theme Rules

**NEVER** use these variable names — they conflict with Tailwind utilities:
- `--spacing-*` (breaks `max-w-md`, `max-w-xl`, `max-w-2xl`, etc.)
- `--container-*`
- `--text-sm`, `--text-lg`, etc. (use `--font-size-*` instead)

**SAFE prefixes**: `--color-*`, `--font-*`, `--font-size-*`, `--space-*`

---

## Decision Framework

When time is limited, invest in this order:

| Priority | Layer | Impact |
|----------|-------|--------|
| 1 | Typography | Highest impact — carries the entire design |
| 2 | Spacing | Separates professional from amateur |
| 3 | Color | 2 colors with intention beat 5 without |
| 4 | States | Empty, loading, error, success |
| 5 | Basic Motion | Hover states, scroll reveals |
| 6 | Texture | Shadows, grain, material feel |

---

## Implementation Checklist

### Setup (Every Project)

- [ ] Context identified? (Marketing site vs Dashboard/App)
- [ ] Google Fonts loaded in index.html with preconnect?
- [ ] Tailwind v4 @theme uses safe variable names? (No --spacing-*, no --container-*)
- [ ] Button classes (`.btn-primary`, `.btn-secondary`) defined with `!important` colors?

### Marketing Sites / Landing Pages

- [ ] Five Commitments documented? (Story, Tension, Signature, Material, Gesture)
- [ ] Only 2–3 colors?
- [ ] 60%+ viewport is empty space?
- [ ] No feature card grids? (Use numbered lists, editorial layouts)
- [ ] No gradients?
- [ ] No icons in circles?
- [ ] One signature visual/animation moment?
- [ ] Display typography for hero?

### Dashboards / Admin Panels / Apps

- [ ] High information density? (30-40% whitespace, not 60%)
- [ ] NO hero sections? (Get straight to data)
- [ ] NO decorative backgrounds? (No particles, generative art — they distract)
- [ ] Card grids for stats/widgets? (Cards ARE appropriate here)
- [ ] Functional, readable typography? (Not dramatic display sizes)
- [ ] Minimal animation? (Only functional transitions)
- [ ] Data-first layout? (Charts, tables, forms prominent)

### Both Contexts

- [ ] No banned fonts? (Inter, Roboto, Arial, Poppins, etc.)
- [ ] Body text 45–75 characters per line?
- [ ] All buttons use `.btn-*` classes?
- [ ] `prefers-reduced-motion` respected?

---

**Remember**: Safe is forgettable. The Designer creates interfaces that users *remember*.
