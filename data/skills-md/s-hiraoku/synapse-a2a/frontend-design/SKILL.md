---
name: frontend-design
description: >-
  Guide for creating distinctive, production-grade frontend interfaces. Covers
  visual design systems, typography, color, motion, spatial composition, and
  web interface standards. Use when designing UI, establishing design systems,
  or reviewing visual quality of frontend code.
---

# Frontend Design

Create interfaces with intentional aesthetics and professional execution. Avoid generic "template" looks.

## Design Process

Before writing code, answer these questions:

1. **Purpose** — What problem does this interface solve? Who uses it?
2. **Tone** — What aesthetic direction? (brutalist, luxury, playful, editorial, retro-futuristic, etc.)
3. **Constraints** — Device targets, accessibility requirements, performance budget
4. **Signature** — What single element makes this memorable?

Commit to a direction. Timid design is worse than bold design with flaws.

## Typography

### Font Selection

Avoid overused defaults. Choose typefaces that reinforce the interface's personality.

```css
/* BAD: Generic, seen everywhere */
font-family: 'Inter', 'Roboto', 'Arial', sans-serif;

/* GOOD: Distinctive and paired intentionally */
--font-display: 'Instrument Serif', serif;      /* headings */
--font-body: 'Satoshi', sans-serif;              /* body text */
--font-mono: 'Berkeley Mono', monospace;         /* code */
```

### Typographic Details

```css
/* Tabular numbers for aligned columns */
.data-cell { font-variant-numeric: tabular-nums; }

/* Balanced headings prevent widow words */
h1, h2, h3 { text-wrap: balance; }

/* Proper ellipsis character */
.truncate::after { content: '\2026'; } /* … not ... */
```

Handle text overflow deliberately:

```css
/* Single line truncation */
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* Multi-line clamping */
.clamp-3 { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }

/* Flex children need min-w-0 for truncation to work */
.flex-child { min-width: 0; }
```

## Color Systems

### Theme Architecture

Build on CSS custom properties with clear semantic naming.

```css
:root {
  /* Primitives */
  --gray-50: oklch(0.98 0.005 240);
  --gray-900: oklch(0.15 0.01 240);
  --accent: oklch(0.65 0.25 30);

  /* Semantic tokens */
  --color-bg: var(--gray-50);
  --color-text: var(--gray-900);
  --color-text-muted: oklch(0.55 0.01 240);
  --color-border: oklch(0.88 0.005 240);
  --color-accent: var(--accent);
  --color-accent-hover: oklch(0.58 0.28 30);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: var(--gray-900);
    --color-text: var(--gray-50);
    --color-text-muted: oklch(0.65 0.01 240);
    --color-border: oklch(0.28 0.005 240);
  }
}
```

### Color Principles

- **Commit to a palette** — 1 dominant + 1–2 accents. Avoid 5-color rainbows.
- **Use oklch** — Perceptually uniform, better than hex/hsl for programmatic palettes.
- **Contrast ratios** — 4.5:1 minimum for body text, 3:1 for large text (WCAG AA).

## Motion & Animation

### Rules

1. **Respect user preference**: Always honor `prefers-reduced-motion`
2. **Animate only `transform` and `opacity`**: These are GPU-composited, everything else triggers layout/paint
3. **Never use `transition: all`**: List specific properties
4. **Animations must be interruptible**: User actions should cancel running animations

```css
/* GOOD: Specific properties, respects user preference */
.card {
  transition: transform 200ms ease-out, opacity 150ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .card { transition: none; }
}
```

### High-Impact Moments

Focus animation budget on:

- **Page transitions** — Orchestrated staggered reveals
- **State changes** — Loading → content, collapsed → expanded
- **Feedback** — Button press, form submission confirmation

Skip: random hover effects on every element, scroll-jacking, decorative background animations.

## Spatial Composition

### Layout Principles

- **Asymmetry is interesting** — Perfectly centered grid layouts are predictable
- **Intentional negative space** — White space is a design element, not a mistake
- **Grid-breaking elements** — One element that overlaps or extends beyond the grid creates focus
- **Diagonal flow** — Eye movement along diagonals is more engaging than horizontal scan

### Responsive Strategy

```css
/* Fluid typography */
h1 { font-size: clamp(2rem, 5vw, 4rem); }

/* Container queries for component-level responsiveness */
.card-container { container-type: inline-size; }

@container (min-width: 400px) {
  .card { grid-template-columns: 200px 1fr; }
}
```

## Backgrounds & Atmosphere

Build visual depth through layered treatments:

```css
/* Noise texture overlay */
.surface::after {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/noise.svg');
  opacity: 0.03;
  pointer-events: none;
}

/* Gradient mesh */
.hero {
  background:
    radial-gradient(ellipse at 20% 50%, oklch(0.7 0.15 250 / 0.3), transparent 50%),
    radial-gradient(ellipse at 80% 20%, oklch(0.7 0.2 30 / 0.2), transparent 50%),
    var(--color-bg);
}
```

## Images & Media

```tsx
// Explicit dimensions prevent layout shift
<Image src={src} width={800} height={600} alt="Description" />

// Below-fold: lazy load
<Image src={src} loading="lazy" alt="..." />

// Above-fold: prioritize
<Image src={src} priority alt="..." />

// Decorative: empty alt
<Image src={pattern} alt="" aria-hidden="true" />
```

## Interactive States

Every interactive element needs 4 states:

| State | Treatment |
|-------|-----------|
| Default | Base appearance |
| Hover | Increased contrast or subtle shift |
| Focus | Visible ring via `:focus-visible` |
| Active/Pressed | Slight scale or color change |
| Disabled | Reduced opacity + `cursor: not-allowed` |

```css
.button {
  background: var(--color-accent);
  transition: background 150ms ease-out, transform 100ms ease-out;
}
.button:hover { background: var(--color-accent-hover); }
.button:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }
.button:active { transform: scale(0.98); }
```

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Inter/Roboto/Arial everywhere | Choose distinctive, project-appropriate typefaces |
| Purple gradient on white | Commit to a specific, cohesive palette |
| Uniform card grids | Vary sizes, add featured/hero cards |
| Shadows on everything | Use shadow purposefully for elevation hierarchy |
| `border-radius: 9999px` on all elements | Match radius to content type and context |
| Identical hover effects | Tailor interaction feedback to element function |
