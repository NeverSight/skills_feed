---
name: flex-grid-flow
version: 3.0
description: Framework-agnostic design philosophy for fluid, responsive interfaces. Covers layout thinking, fluid typography/spacing math, adaptive colors, and hard rules. Equal coverage for SCSS and Tailwind.
---

# Design System Skill: Fluid Layout & Typography

A thinking framework for building responsive interfaces. This skill applies to any stack: React, Vue, Astro, Svelte, 11ty, plain HTML, Tailwind, SCSS, or vanilla CSS.

---

## Part I: Design Philosophy

### Think Before You Code

Before writing any CSS, ask these questions:

1. **What's the content hierarchy?**
   - What's the most important element?
   - What's secondary, tertiary?
   - What can be hidden on small screens?

2. **How does this flow on different screen sizes?**
   - Does the layout need to change at all?
   - What's the minimum viable layout?
   - Should items stack, wrap, or scroll horizontally?

3. **What's critical vs nice-to-have?**
   - On mobile, what must be visible immediately?
   - What can be revealed through interaction?

### Mobile Doesn't Mean "Center Everything"

Common misconception: mobile layouts should center all content. Reality:

- **Left-aligned content** often scans better (natural reading direction)
- **Asymmetric margins** create visual interest and hierarchy
- **Horizontal scroll** (reel pattern) sometimes beats stacking
- **Bottom navigation** often works better than hamburger menus
- **Tabs** can work on mobile if limited to 3-5 items

### Ask, Don't Assume

When implementing layouts:
- Ask what the priority is on small screens
- Ask if certain elements can be hidden/collapsed
- Ask about interaction patterns (swipe, tap, long-press)
- Don't invent solutions — present options

---

## Part II: Fluid Options

Not everything needs to be fluid. Choose based on the project:

```
Do you want fluid values?
├─ Typography only → fluid font sizes, fixed spacing
├─ Spacing only → fixed fonts, fluid gaps/padding
├─ Both → full fluid system
└─ Neither → breakpoint-based, explicit sizes
```

### When to Use Each

| Approach | Best For |
|----------|----------|
| **Fluid both** | Marketing sites, editorial, portfolios |
| **Fluid type only** | Apps with dense UI, data tables |
| **Fluid space only** | Apps with fixed type hierarchy |
| **Fixed both** | Precise control needed, legacy support |

### The Hybrid Approach

Most projects benefit from:
- Fluid typography for headings
- Fixed typography for body/UI text
- Fluid spacing for sections and large gaps
- Fixed spacing for component internals

---

## Part III: Type Scale Mathematics

### The Core Formula

Fluid values use CSS `clamp()` with linear interpolation:

```css
font-size: clamp(min, preferred, max);
```

Where the **preferred** value creates smooth scaling:

```
preferred = (slope × 100)vw + intercept

slope = (maxSize - minSize) / (maxViewport - minViewport)
intercept = minSize - (slope × minViewport)
```

### Example Calculation

Given:
- Min font: 16px at 320px viewport
- Max font: 20px at 1280px viewport

```
slope = (20 - 16) / (1280 - 320) = 4 / 960 = 0.00417
intercept = 16 - (0.00417 × 320) = 16 - 1.33 = 14.67px

preferred = 0.417vw + 14.67px
```

Result:
```css
font-size: clamp(1rem, 0.417vw + 0.917rem, 1.25rem);
```

### Type Scale Ratios

A type scale multiplies a base size by a ratio raised to a power:

```
fontSize = baseSize × ratio^step
```

| Ratio | Name | Character |
|-------|------|-----------|
| 1.067 | Minor Second | Very tight, technical |
| 1.125 | Major Second | Tight, compact UI |
| 1.200 | Minor Third | Balanced, versatile |
| 1.250 | Major Third | Comfortable reading |
| 1.333 | Perfect Fourth | Spacious, editorial |
| 1.414 | Augmented Fourth | Dramatic headlines |
| 1.500 | Perfect Fifth | Very dramatic |
| 1.618 | Golden Ratio | Classical proportion |

### Generating Steps

With base 16px and ratio 1.25 (Major Third):

| Step | Calculation | Size |
|------|-------------|------|
| -2 | 16 × 1.25^-2 | 10.24px |
| -1 | 16 × 1.25^-1 | 12.80px |
| 0 | 16 × 1.25^0 | 16.00px |
| 1 | 16 × 1.25^1 | 20.00px |
| 2 | 16 × 1.25^2 | 25.00px |
| 3 | 16 × 1.25^3 | 31.25px |
| 4 | 16 × 1.25^4 | 39.06px |
| 5 | 16 × 1.25^5 | 48.83px |

### Fluid Type Scale

Combine different ratios for mobile vs desktop:

```
Mobile: 1.125 (Major Second) — tighter hierarchy
Desktop: 1.25 (Major Third) — more dramatic hierarchy
```

Each step has a min (mobile) and max (desktop) value, then apply the clamp formula.

---

## Part IV: Spacing Scale

### Base Scale (T-Shirt Sizing)

```
3xs → 2xs → xs → sm → md → lg → xl → 2xl → 3xl
```

Use a ratio (commonly 1.5 Perfect Fifth) to generate values:

| Token | Calculation (ratio 1.5) | Value |
|-------|-------------------------|-------|
| size-3xs | base ÷ 1.5^3 | 4.7px |
| size-2xs | base ÷ 1.5^2 | 7.1px |
| size-xs | base ÷ 1.5^1 | 10.7px |
| size-sm | base | 16px |
| size-md | base × 1.5^1 | 24px |
| size-lg | base × 1.5^2 | 36px |
| size-xl | base × 1.5^3 | 54px |
| size-2xl | base × 1.5^4 | 81px |
| size-3xl | base × 1.5^5 | 121.5px |

### 1-Up Pairs (One Step Jump)

For responsive spacing that scales more dramatically:

```css
/* Min value from smaller step, max value from larger step */
--size-xs-sm: clamp(/* xs-min */, /* preferred */, /* sm-max */);
--size-sm-md: clamp(/* sm-min */, /* preferred */, /* md-max */);
--size-md-lg: clamp(/* md-min */, /* preferred */, /* lg-max */);
--size-lg-xl: clamp(/* lg-min */, /* preferred */, /* xl-max */);
--size-xl-2xl: clamp(/* xl-min */, /* preferred */, /* 2xl-max */);
```

Use for: section padding, large gaps, hero spacing

### 2-Up Pairs (Two Step Jump)

For even more dramatic responsive scaling:

```css
/* Skip a step for bigger difference */
--size-xs-md: clamp(/* xs-min */, /* preferred */, /* md-max */);
--size-sm-lg: clamp(/* sm-min */, /* preferred */, /* lg-max */);
--size-md-xl: clamp(/* md-min */, /* preferred */, /* xl-max */);
--size-lg-2xl: clamp(/* lg-min */, /* preferred */, /* 2xl-max */);
--size-xl-3xl: clamp(/* xl-min */, /* preferred */, /* 3xl-max */);
```

Use for: page margins, major section breaks, hero content

### Semantic Aliases

Map raw sizes to purpose:

```css
:root {
  --gap-tight: var(--size-xs);
  --gap: var(--size-sm);
  --gap-loose: var(--size-md);

  --section-padding: var(--size-lg-xl);  /* 1-up pair */
  --page-margin: var(--size-md-xl);      /* 2-up pair */
}
```

---

## Part V: Adaptive Color Tokens

### The Problem

Hardcoded colors don't adapt:
```css
/* This only works on white backgrounds */
.button:hover {
  background: rgba(0, 0, 0, 0.08);
}
```

### The Solution: currentColor + Transparency

Use `currentColor` so tokens inherit and adapt:

```css
:root {
  /* Transparency scale */
  --alpha-50: 4%;
  --alpha-100: 8%;
  --alpha-200: 12%;
  --alpha-300: 16%;
  --alpha-400: 24%;
  --alpha-500: 32%;
  --alpha-600: 48%;
  --alpha-700: 64%;
  --alpha-800: 80%;
  --alpha-900: 90%;
  --alpha-1000: 97%;
}
```

### Surface Tokens

```css
:root {
  /* Adapt to any foreground color */
  --surface-hover: color-mix(in srgb, currentColor var(--alpha-100), transparent);
  --surface-active: color-mix(in srgb, currentColor var(--alpha-200), transparent);
  --surface-selected: color-mix(in srgb, currentColor var(--alpha-300), transparent);
  --surface-disabled: color-mix(in srgb, currentColor var(--alpha-50), transparent);

  /* Borders that adapt */
  --border-subtle: color-mix(in srgb, currentColor var(--alpha-100), transparent);
  --border-default: color-mix(in srgb, currentColor var(--alpha-200), transparent);
  --border-strong: color-mix(in srgb, currentColor var(--alpha-400), transparent);
}
```

### Usage

```css
.button {
  background: transparent;
  border: 1px solid var(--border-default);
}

.button:hover {
  background: var(--surface-hover);
}

.button:active {
  background: var(--surface-active);
}

/* Works on ANY background color */
```

### White/Black Transparency (Fixed)

When you need consistent overlay regardless of context:

```css
:root {
  /* White overlays */
  --white-a100: color-mix(in srgb, white var(--alpha-100), transparent);
  --white-a200: color-mix(in srgb, white var(--alpha-200), transparent);
  --white-a300: color-mix(in srgb, white var(--alpha-300), transparent);

  /* Black overlays */
  --black-a100: color-mix(in srgb, black var(--alpha-100), transparent);
  --black-a200: color-mix(in srgb, black var(--alpha-200), transparent);
  --black-a300: color-mix(in srgb, black var(--alpha-300), transparent);
}
```

---

## Part VI: Hard Rules

These are non-negotiable defaults. Only break them with explicit justification.

### 1. Icons in 1:1 Containers (Always)

```css
.icon {
  display: grid;
  place-items: center;
  aspect-ratio: 1;
  width: var(--icon-size, 1.5rem);
}

/* Or inline */
.icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 1;
  width: 1em;
  height: 1em;
}
```

**Why:** Icons misalign when not in square containers. The 1:1 ratio ensures consistent alignment with text and other elements.

### 2. Logical Properties (Always)

```css
/* YES */
.element {
  padding-block: var(--size-md);
  padding-inline: var(--size-lg);
  margin-block-start: var(--size-sm);
  border-inline-end: 1px solid var(--border-default);
}

/* NO */
.element {
  padding-top: var(--size-md);
  padding-bottom: var(--size-md);
  padding-left: var(--size-lg);
  padding-right: var(--size-lg);
}
```

**Why:** Logical properties support RTL languages and writing modes automatically.

### 3. Gap on Containers, Not Margins on Children

```css
/* YES */
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}

/* NO */
.stack > * + * {
  margin-top: 1rem;
}
```

**Why:** Gap is more maintainable, doesn't require lobotomized owl selectors, and works with flex/grid.

### 4. No Hardcoded Values

```css
/* YES */
.card {
  padding: var(--size-md);
  border-radius: var(--radius-md);
  gap: var(--size-sm);
}

/* NO */
.card {
  padding: 24px;
  border-radius: 8px;
  gap: 16px;
}
```

**Why:** Tokens create consistency and make global changes trivial.

### 5. Display Grid or Flex on Every Wrapper

Every container that holds multiple children should declare layout:

```css
/* YES */
.card {
  display: grid;
  gap: var(--size-sm);
}

/* NO - implicit block layout */
.card {
  /* children use default block flow */
}
```

**Why:** Explicit layout prevents surprises and makes gap work.

---

## Part VII: Layout Patterns

### Decision Tree: Grid vs Flex

```
Need explicit 2D control (rows AND columns)?
├─ YES → Grid
└─ NO → Need items to wrap?
    ├─ YES → Flex with flex-wrap
    └─ NO → Single axis alignment?
        ├─ YES → Flex
        └─ NO → Need stacking/overlay?
            ├─ YES → Grid (grid-area trick)
            └─ NO → Default to Flex
```

### Grid: Template Areas (Explicit Layout)

For complex, named layouts:

```css
.page {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav    main   aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 250px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header { grid-area: header; }
.nav { grid-area: nav; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }

/* Mobile: stack everything */
@media (max-width: 768px) {
  .page {
    grid-template-areas:
      "header"
      "main"
      "aside"
      "nav"
      "footer";
    grid-template-columns: 1fr;
  }
}
```

### Grid: Template Columns/Rows (Structured)

For repetitive but controlled layouts:

```css
/* Fixed columns */
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--size-md);
}

/* Mixed fixed and flexible */
.sidebar-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: var(--size-lg);
}

/* Responsive with explicit breakpoint */
.grid-responsive {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--size-md);
}

@media (min-width: 640px) {
  .grid-responsive {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid-responsive {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Grid: Auto-fit/Auto-fill (Intrinsic)

For grids that figure themselves out:

```css
/* Auto-fit: columns collapse when empty */
.grid-auto-fit {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
  gap: var(--size-md);
}

/* Auto-fill: keeps empty column tracks */
.grid-auto-fill {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(18rem, 100%), 1fr));
  gap: var(--size-md);
}
```

**When to use:**
- `auto-fit`: Card grids, galleries, when you want items to stretch
- `auto-fill`: When you want consistent column widths even with few items

### Grid: Stacking (Overlay)

Replace `position: absolute` for overlays:

```css
.stack-container {
  display: grid;
  grid-template-areas: "stack";
}

.stack-container > * {
  grid-area: stack;
}

/* Position children with alignment */
.stack-container > .overlay {
  align-self: end;
  justify-self: start;
  padding: var(--size-md);
}
```

### Flex: Stack (Vertical)

```css
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
}

/* Variants */
.stack[data-gap="tight"] { gap: var(--size-xs); }
.stack[data-gap="loose"] { gap: var(--size-lg); }
.stack[data-align="center"] { align-items: center; }
.stack[data-align="end"] { align-items: flex-end; }
```

### Flex: Cluster (Horizontal Wrap)

```css
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--size-xs);
  align-items: center;
}

/* Variants */
.cluster[data-justify="between"] { justify-content: space-between; }
.cluster[data-justify="end"] { justify-content: flex-end; }
```

### Flex: Switcher (Responsive Row/Column)

```css
.switcher {
  display: flex;
  flex-wrap: wrap;
  gap: var(--size-md);
}

.switcher > * {
  flex-grow: 1;
  flex-basis: calc((30rem - 100%) * 999);
}
```

**How it works:** When container is wider than 30rem, items stay in a row. Below that, they stack.

### Flex: Sidebar

```css
.with-sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--size-lg);
}

.with-sidebar > :first-child {
  flex-basis: 250px;
  flex-grow: 1;
}

.with-sidebar > :last-child {
  flex-basis: 0;
  flex-grow: 999;
  min-width: 60%;
}
```

### Reel (Horizontal Scroll)

```css
.reel {
  display: flex;
  gap: var(--size-sm);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-padding-inline: var(--size-md);
  padding-block: var(--size-xs); /* space for focus rings */
}

.reel > * {
  flex-shrink: 0;
  scroll-snap-align: start;
}

/* Hide scrollbar but keep functionality */
.reel {
  scrollbar-width: none;
}
.reel::-webkit-scrollbar {
  display: none;
}
```

---

## Part VIII: Container Queries

When a component should respond to its container, not the viewport:

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: grid;
  gap: var(--size-sm);
}

@container card (min-width: 400px) {
  .card {
    grid-template-columns: 150px 1fr;
    gap: var(--size-md);
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 200px 1fr;
  }
}
```

### When to Use Container vs Viewport Queries

| Use Container Query | Use Viewport Query |
|---------------------|-------------------|
| Cards in varying contexts | Page-level layout |
| Reusable components | Navigation changes |
| Sidebar content | Global typography |
| Widgets/embeds | Section layouts |

---

## Part IX: SCSS Implementation

### Core Functions

```scss
// Convert px to rem
@function rem($px) {
  @return calc($px / 16 * 1rem);
}

// Generate fluid clamp value
@function fluid-clamp($min-px, $max-px, $min-vw: 320, $max-vw: 1280) {
  $min-rem: rem($min-px);
  $max-rem: rem($max-px);

  $slope: calc(($max-px - $min-px) / ($max-vw - $min-vw));
  $intercept: $min-px - ($slope * $min-vw);

  $slope-vw: calc($slope * 100);
  $intercept-rem: rem($intercept);

  @return clamp(#{$min-rem}, #{$slope-vw}vw + #{$intercept-rem}, #{$max-rem});
}

// Calculate type step size
@function type-step($step, $base: 16, $ratio: 1.25) {
  @return $base * pow($ratio, $step);
}

// Generate fluid type step
@function fluid-type-step($step, $min-base: 16, $max-base: 16, $min-ratio: 1.125, $max-ratio: 1.25, $min-vw: 320, $max-vw: 1280) {
  $min-size: type-step($step, $min-base, $min-ratio);
  $max-size: type-step($step, $max-base, $max-ratio);

  @return fluid-clamp($min-size, $max-size, $min-vw, $max-vw);
}

// Calculate spacing step
@function space-step($step, $base: 16, $ratio: 1.5) {
  @return $base * pow($ratio, $step);
}

// Generate fluid space step
@function fluid-space-step($step, $base: 16, $ratio: 1.5, $min-vw: 320, $max-vw: 1280) {
  $min-size: space-step($step, $base, $ratio) * 0.75; // 75% at mobile
  $max-size: space-step($step, $base, $ratio);

  @return fluid-clamp($min-size, $max-size, $min-vw, $max-vw);
}

// Pow function (for older Sass versions)
@function pow($base, $exp) {
  $result: 1;
  @if $exp > 0 {
    @for $i from 1 through $exp {
      $result: $result * $base;
    }
  } @else if $exp < 0 {
    @for $i from 1 through (-$exp) {
      $result: calc($result / $base);
    }
  }
  @return $result;
}
```

### Generate Tokens

```scss
:root {
  // Type scale
  @for $i from -2 through 5 {
    --font-#{$i}: #{fluid-type-step($i)};
  }

  // Spacing scale
  $space-names: ('3xs': -3, '2xs': -2, 'xs': -1, 'sm': 0, 'md': 1, 'lg': 2, 'xl': 3, '2xl': 4, '3xl': 5);

  @each $name, $step in $space-names {
    --size-#{$name}: #{fluid-space-step($step)};
  }

  // 1-up pairs
  --size-xs-sm: #{fluid-clamp(space-step(-1) * 0.75, space-step(0))};
  --size-sm-md: #{fluid-clamp(space-step(0) * 0.75, space-step(1))};
  --size-md-lg: #{fluid-clamp(space-step(1) * 0.75, space-step(2))};
  --size-lg-xl: #{fluid-clamp(space-step(2) * 0.75, space-step(3))};
  --size-xl-2xl: #{fluid-clamp(space-step(3) * 0.75, space-step(4))};

  // 2-up pairs
  --size-xs-md: #{fluid-clamp(space-step(-1) * 0.75, space-step(1))};
  --size-sm-lg: #{fluid-clamp(space-step(0) * 0.75, space-step(2))};
  --size-md-xl: #{fluid-clamp(space-step(1) * 0.75, space-step(3))};
  --size-lg-2xl: #{fluid-clamp(space-step(2) * 0.75, space-step(4))};
  --size-xl-3xl: #{fluid-clamp(space-step(3) * 0.75, space-step(5))};
}
```

---

## Part X: Tailwind Implementation

### Tailwind v4 @theme Configuration

```css
@import "tailwindcss";

:root {
  /* Fluid spacing - define raw values */
  --size-3xs: clamp(0.25rem, 0.23rem + 0.1vw, 0.31rem);
  --size-2xs: clamp(0.5rem, 0.46rem + 0.2vw, 0.63rem);
  --size-xs: clamp(0.75rem, 0.68rem + 0.3vw, 0.94rem);
  --size-sm: clamp(1rem, 0.91rem + 0.4vw, 1.25rem);
  --size-md: clamp(1.5rem, 1.37rem + 0.6vw, 1.88rem);
  --size-lg: clamp(2rem, 1.83rem + 0.8vw, 2.5rem);
  --size-xl: clamp(3rem, 2.74rem + 1.2vw, 3.75rem);
  --size-2xl: clamp(4rem, 3.65rem + 1.6vw, 5rem);
  --size-3xl: clamp(6rem, 5.48rem + 2.4vw, 7.5rem);

  /* 1-up pairs */
  --size-sm-md: clamp(1rem, 0.8rem + 1vw, 1.88rem);
  --size-md-lg: clamp(1.5rem, 1.2rem + 1.5vw, 2.5rem);
  --size-lg-xl: clamp(2rem, 1.5rem + 2.5vw, 3.75rem);

  /* 2-up pairs */
  --size-sm-lg: clamp(1rem, 0.6rem + 2vw, 2.5rem);
  --size-md-xl: clamp(1.5rem, 0.9rem + 3vw, 3.75rem);

  /* Fluid type */
  --font-xs: clamp(0.75rem, 0.7rem + 0.2vw, 0.875rem);
  --font-sm: clamp(0.875rem, 0.8rem + 0.3vw, 1rem);
  --font-base: clamp(1rem, 0.9rem + 0.4vw, 1.125rem);
  --font-lg: clamp(1.125rem, 1rem + 0.5vw, 1.25rem);
  --font-xl: clamp(1.25rem, 1.1rem + 0.7vw, 1.5rem);
  --font-2xl: clamp(1.5rem, 1.3rem + 1vw, 2rem);
  --font-3xl: clamp(1.875rem, 1.5rem + 1.5vw, 2.5rem);
  --font-4xl: clamp(2.25rem, 1.8rem + 2vw, 3rem);
  --font-5xl: clamp(3rem, 2.2rem + 3vw, 4rem);

  /* Adaptive colors */
  --surface-hover: color-mix(in srgb, currentColor 8%, transparent);
  --surface-active: color-mix(in srgb, currentColor 12%, transparent);
  --surface-selected: color-mix(in srgb, currentColor 16%, transparent);
  --border-subtle: color-mix(in srgb, currentColor 8%, transparent);
  --border-default: color-mix(in srgb, currentColor 16%, transparent);
}

@theme {
  /* Map to Tailwind utilities */
  --spacing-3xs: var(--size-3xs);
  --spacing-2xs: var(--size-2xs);
  --spacing-xs: var(--size-xs);
  --spacing-sm: var(--size-sm);
  --spacing-md: var(--size-md);
  --spacing-lg: var(--size-lg);
  --spacing-xl: var(--size-xl);
  --spacing-2xl: var(--size-2xl);
  --spacing-3xl: var(--size-3xl);

  /* Pairs */
  --spacing-sm-md: var(--size-sm-md);
  --spacing-md-lg: var(--size-md-lg);
  --spacing-lg-xl: var(--size-lg-xl);
  --spacing-sm-lg: var(--size-sm-lg);
  --spacing-md-xl: var(--size-md-xl);

  /* Font sizes */
  --font-size-xs: var(--font-xs);
  --font-size-sm: var(--font-sm);
  --font-size-base: var(--font-base);
  --font-size-lg: var(--font-lg);
  --font-size-xl: var(--font-xl);
  --font-size-2xl: var(--font-2xl);
  --font-size-3xl: var(--font-3xl);
  --font-size-4xl: var(--font-4xl);
  --font-size-5xl: var(--font-5xl);

  /* Colors */
  --color-surface-hover: var(--surface-hover);
  --color-surface-active: var(--surface-active);
  --color-surface-selected: var(--surface-selected);
  --color-border-subtle: var(--border-subtle);
  --color-border-default: var(--border-default);
}
```

### Usage Examples

```html
<!-- Spacing -->
<div class="p-md gap-sm-md">
  <h2 class="text-3xl">Title</h2>
  <p class="text-base">Content</p>
</div>

<!-- Adaptive hover -->
<button class="hover:bg-surface-hover active:bg-surface-active border border-border-default">
  Click me
</button>

<!-- Layout -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(min(18rem,100%),1fr))] gap-md">
  <div class="p-sm">Card 1</div>
  <div class="p-sm">Card 2</div>
</div>

<!-- Icon (always 1:1) -->
<span class="inline-grid place-items-center aspect-square w-[1.5em]">
  <svg>...</svg>
</span>
```

---

## Part XI: Accessibility

### Focus States (Required)

```css
:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
}

/* Never remove outline without replacement */
button:focus {
  outline: none; /* BAD */
}

button:focus-visible {
  outline: 2px solid var(--color-focus); /* GOOD */
}
```

### Reduced Motion (Required)

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Color Contrast

- Normal text: 4.5:1 minimum
- Large text (18px+ or 14px+ bold): 3:1 minimum
- UI components: 3:1 minimum

### Touch Targets

```css
button,
a,
input,
select {
  min-height: 44px;
  min-width: 44px;
}
```

---

## Part XII: Checklist

Before finalizing any layout/component:

### Structure
- [ ] Every wrapper has `display: grid` or `display: flex`
- [ ] Gap used on containers (not margins on children)
- [ ] Logical properties used throughout
- [ ] Semantic HTML where appropriate

### Tokens
- [ ] No hardcoded px/rem values
- [ ] Spacing uses size tokens
- [ ] Typography uses font tokens
- [ ] Colors use adaptive tokens where possible

### Icons
- [ ] All icons in 1:1 aspect-ratio containers
- [ ] Icon size controlled via token or em

### Responsive
- [ ] Asked about mobile priorities
- [ ] Considered if layout needs to change at all
- [ ] Used appropriate pattern (grid areas, auto-fit, flex-wrap)
- [ ] Mobile isn't just "center everything"

### Accessibility
- [ ] Focus states visible
- [ ] Reduced motion respected
- [ ] Touch targets adequate (44px minimum)
- [ ] Color contrast sufficient

### Before Making Changes
- [ ] Checked design_master.md for existing decisions
- [ ] Asked when uncertain (didn't invent)
- [ ] Logged new decisions to design_master.md
