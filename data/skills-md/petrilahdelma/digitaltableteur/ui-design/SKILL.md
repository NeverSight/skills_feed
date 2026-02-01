---
name: ui-design
description: Expert UI design and visual design guidance for design systems, typography, color theory, layout, spacing, iconography, and component visual design. Use when designing interfaces, creating visual hierarchies, choosing colors, defining typography scales, creating design tokens, working with Figma, or building cohesive visual systems. Includes brand application and design-to-dev handoff.
---

# UI Design Expert

## Core UI Design Principles

When designing user interfaces, always follow these principles:

1. **Visual Hierarchy**: Guide attention through size, weight, color, contrast
2. **Consistency**: Use systematic patterns for predictability
3. **White Space**: Breathing room improves comprehension
4. **Contrast**: Ensure readability and focus
5. **Alignment**: Create order and visual connections
6. **Repetition**: Reinforce brand and structure

---

## Design System Foundation

### Design Tokens (Variables)

**Purpose**: Single source of truth for design decisions

**Token Categories**:

```css
/* Color Tokens */
--color-primary: #0066cc;
--color-secondary: #6c757d;
--color-success: #28a745;
--color-warning: #ffc107;
--color-danger: #dc3545;
--color-text: #212529;
--color-background: #ffffff;

/* Spacing Scale (8px base) */
--space-2: 0.125rem;   /* 2px */
--space-4: 0.25rem;    /* 4px */
--space-8: 0.5rem;     /* 8px */
--space-12: 0.75rem;   /* 12px */
--space-16: 1rem;      /* 16px */
--space-24: 1.5rem;    /* 24px */
--space-32: 2rem;      /* 32px */
--space-48: 3rem;      /* 48px */
--space-64: 4rem;      /* 64px */

/* Typography Scale (Modular 1.25 ratio) */
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.25rem;    /* 20px */
--font-size-xl: 1.5rem;     /* 24px */
--font-size-2xl: 2rem;      /* 32px */
--font-size-3xl: 2.5rem;    /* 40px */
--font-size-4xl: 3rem;      /* 48px */
--font-size-display: clamp(5rem, 10vw + 3rem, 8rem); /* 80-128px */

/* Font Weights */
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

/* Line Heights */
--line-height-tight: 1.2;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;

/* Border Radius */
--radius-sm: 0.25rem;   /* 4px */
--radius-md: 0.5rem;    /* 8px */
--radius-lg: 1rem;      /* 16px */
--radius-full: 9999px;  /* Circle */

/* Shadows */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

/* Z-Index Scale */
--z-dropdown: 1000;
--z-sticky: 1020;
--z-fixed: 1030;
--z-modal-backdrop: 1040;
--z-modal: 1050;
--z-popover: 1060;
--z-tooltip: 1070;
```

---

## Color System

### Color Theory for UI

**60-30-10 Rule**:
- **60%**: Dominant color (backgrounds, large areas)
- **30%**: Secondary color (sections, panels)
- **10%**: Accent color (CTAs, highlights)

### Semantic Color Palette

```
Primary (Brand):
├── primary-50:  #e6f2ff  (lightest - backgrounds)
├── primary-100: #b3d9ff
├── primary-200: #80c0ff
├── primary-300: #4da7ff
├── primary-400: #1a8eff
├── primary-500: #0066cc  ← Base
├── primary-600: #0052a3
├── primary-700: #003d7a
├── primary-800: #002952
└── primary-900: #001429  (darkest - text on light bg)

Success (Green):
├── Positive actions
├── Confirmation states
└── Valid inputs

Warning (Yellow/Orange):
├── Caution states
├── Important notices
└── Pending actions

Danger (Red):
├── Destructive actions
├── Error states
└── Invalid inputs

Neutral (Gray):
├── Text hierarchy
├── Borders
└── Disabled states
```

### Color Accessibility (WCAG)

**Contrast Ratios**:
- **AA Standard**: 4.5:1 for normal text, 3:1 for large text (18px+)
- **AAA Enhanced**: 7:1 for normal text, 4.5:1 for large text

**Test Colors**:
```bash
# Use WebAIM Contrast Checker
https://webaim.org/resources/contrastchecker/

# Or test in code
npm install wcag-color
```

**Example**:
```
✅ PASS: #0066cc text on #ffffff background (7.5:1)
❌ FAIL: #80c0ff text on #ffffff background (2.1:1)
```

### Dark Mode Strategy

**Approach**: Invert semantic colors, not direct colors

```css
/* Light Mode */
:root {
  --color-background: #ffffff;
  --color-surface: #f8f9fa;
  --color-text: #212529;
  --color-text-secondary: #6c757d;
  --color-border: #dee2e6;
}

/* Dark Mode */
[data-theme="dark"] {
  --color-background: #1a1a1a;
  --color-surface: #2d2d2d;
  --color-text: #f8f9fa;
  --color-text-secondary: #adb5bd;
  --color-border: #495057;

  /* Reduce saturation for less eye strain */
  --color-primary: #4da7ff;  /* Lighter than light mode */
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5); /* Deeper shadows */
}
```

---

## Typography

### Type Scale (Modular Scale)

**Formula**: `base × ratio^n`

**Common Ratios**:
- **1.125** (Major Second): Subtle, dense
- **1.25** (Major Third): Balanced ← Recommended
- **1.333** (Perfect Fourth): Dynamic
- **1.5** (Perfect Fifth): Dramatic

**Digitaltableteur Scale** (1.25 ratio):
```
Display: 80-128px (clamp)
H1: 48px
H2: 40px
H3: 32px
H4: 24px
H5: 20px
Body: 16px
Small: 14px
Caption: 12px
```

### Font Pairing

**Recommended Combinations**:

1. **Serif + Sans-Serif** (Classic)
   - Headings: Playfair Display (serif)
   - Body: Inter (sans-serif)

2. **Geometric + Humanist** (Modern)
   - Headings: Montserrat (geometric)
   - Body: Open Sans (humanist)

3. **Monospace + Sans** (Technical)
   - Code: Fira Code (monospace)
   - UI: Roboto (sans-serif)

**Digitaltableteur Stack**:
```css
--font-title: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'Fira Code', 'Courier New', monospace;
```

### Typographic Hierarchy

```css
/* Display (Hero Headlines) */
.display {
  font-size: var(--font-size-display);
  line-height: var(--line-height-tight);
  font-weight: var(--font-weight-bold);
  letter-spacing: -0.02em; /* Tighter for large sizes */
}

/* H1 (Page Title) */
h1 {
  font-size: var(--font-size-4xl);
  line-height: var(--line-height-tight);
  font-weight: var(--font-weight-bold);
}

/* H2 (Section Title) */
h2 {
  font-size: var(--font-size-3xl);
  line-height: var(--line-height-normal);
  font-weight: var(--font-weight-semibold);
}

/* Body (Paragraph) */
p {
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
  font-weight: var(--font-weight-normal);
  max-width: 65ch; /* Optimal reading width */
}

/* Small (Caption, Meta) */
small {
  font-size: var(--font-size-sm);
  line-height: var(--line-height-normal);
  color: var(--color-text-secondary);
}
```

### Readability Guidelines

- **Line Length**: 45-75 characters (optimal: 65ch)
- **Line Height**: 1.5× font size for body text
- **Paragraph Spacing**: 1.5× line height
- **Letter Spacing**: -0.02em for large text, 0em for body

---

## Layout & Spacing

### Grid System

**12-Column Grid** (flexible):

```css
.container {
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: var(--space-16);
}

.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-24);
}

/* 3-column layout */
.col-4 {
  grid-column: span 4;
}

/* Responsive */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
  .col-4 {
    grid-column: span 1;
  }
}
```

### Spacing System (8px Base)

**Concept**: All spacing uses multiples of 8px for visual consistency

```
2px:  Micro (icon padding)
4px:  Tiny (inline spacing)
8px:  Small (tight elements)
12px: Compact (related items)
16px: Base (default spacing)
24px: Medium (section padding)
32px: Large (cards, panels)
48px: XL (major sections)
64px: XXL (hero sections)
```

**Application**:
```css
/* Component Internal Spacing */
.card {
  padding: var(--space-24); /* 24px */
}

/* Component External Spacing */
.card + .card {
  margin-block-start: var(--space-16); /* 16px gap */
}

/* Section Spacing */
.section {
  padding-block: var(--space-64); /* 64px top/bottom */
}
```

### Whitespace Principles

**Law of Proximity**: Related items closer, unrelated farther

```
Bad Example:
┌─────────────┐
│ Title       │ ← 8px gap
│ Subtitle    │ ← 8px gap
│ Author      │ ← 8px gap (too uniform)
│ Date        │
└─────────────┘

Good Example:
┌─────────────┐
│ Title       │ ← 4px gap (related)
│ Subtitle    │ ← 24px gap (separate group)
│ Author      │ ← 4px gap (related)
│ Date        │
└─────────────┘
```

---

## Component Visual Design

### Button Anatomy

```
┌────────────────────────────┐
│  [Icon] Label [Icon]       │ ← Text: 14-16px, weight: 500-600
│  ↑      ↑       ↑          │
│  8px   12px    8px         │ ← Spacing
└────────────────────────────┘
  ↑                        ↑
  12px padding           12px padding

Height: 40-48px (min 44px for touch)
Border-radius: 8px
```

**Button Hierarchy**:

```css
/* Primary (High emphasis) */
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  font-weight: 600;
  box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
  background-color: var(--color-primary-600);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

/* Secondary (Medium emphasis) */
.btn-secondary {
  background-color: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

/* Tertiary (Low emphasis) */
.btn-tertiary {
  background-color: transparent;
  color: var(--color-primary);
  text-decoration: underline;
}
```

### Card Design

```css
.card {
  /* Structure */
  background-color: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-24);

  /* Depth */
  box-shadow: var(--shadow-md);

  /* Interaction */
  transition:
    transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 0.3s ease;
}

.card:hover {
  transform: scale(1.02);
  box-shadow: var(--shadow-xl);
}

/* Card Anatomy */
.card-header {
  margin-block-end: var(--space-16);
}

.card-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
}

.card-content {
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
  color: var(--color-text-secondary);
}

.card-footer {
  margin-block-start: var(--space-24);
  padding-block-start: var(--space-16);
  border-block-start: 1px solid var(--color-border);
}
```

### Form Input Design

```css
.input {
  /* Size */
  min-height: 48px;
  padding: 12px 16px;

  /* Typography */
  font-size: var(--font-size-base);
  line-height: 1.5;

  /* Visual */
  background-color: var(--color-background);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);

  /* Interaction */
  transition: all 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1); /* Focus ring */
}

.input:invalid {
  border-color: var(--color-danger);
}

.input:disabled {
  background-color: var(--color-surface);
  color: var(--color-text-secondary);
  cursor: not-allowed;
}

/* Label */
.label {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
  margin-block-end: var(--space-8);
}

/* Helper Text */
.help-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-block-start: var(--space-4);
}

/* Error Message */
.error-message {
  font-size: var(--font-size-sm);
  color: var(--color-danger);
  margin-block-start: var(--space-4);
  display: flex;
  align-items: center;
  gap: var(--space-4);
}
```

---

## Iconography

### Icon System Guidelines

**Size Scale**:
```
16px: Inline with text
20px: Buttons, inputs
24px: Navigation, cards
32px: Feature highlights
48px: Empty states, placeholders
```

**Style**:
- **Stroke width**: 2px (consistent across set)
- **Corner radius**: 2px (rounded, friendly)
- **Grid**: 24×24px with 2px padding

**Usage**:
```tsx
import { MagnifyingGlass, User, XCircle } from '@phosphor-icons/react';

// Default size (24px)
<MagnifyingGlass />

// Custom size
<MagnifyingGlass size={32} weight="bold" />

// With color
<User color="var(--color-primary)" />
```

**Accessibility**:
```tsx
// Decorative icon (hidden from screen readers)
<MagnifyingGlass aria-hidden="true" />

// Functional icon (needs label)
<button aria-label="Search">
  <MagnifyingGlass />
</button>
```

---

## Animation & Motion

### Animation Principles

1. **Purposeful**: Motion guides attention or provides feedback
2. **Subtle**: Enhance, don't distract (200-400ms)
3. **Natural**: Use easing curves, not linear
4. **Respectful**: Honor `prefers-reduced-motion`

### Easing Functions

```css
/* Material Design Easing */
--ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1);  /* Default */
--ease-decelerate: cubic-bezier(0.0, 0.0, 0.2, 1); /* Enter screen */
--ease-accelerate: cubic-bezier(0.4, 0.0, 1, 1);   /* Exit screen */

/* Elastic (playful) */
--ease-elastic: cubic-bezier(0.34, 1.56, 0.64, 1);

/* Usage */
.button {
  transition: transform 0.3s var(--ease-standard);
}

.button:hover {
  transform: scale(1.05);
}
```

### Common Animations

**Fade In**:
```css
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation: fadeIn 0.3s var(--ease-standard);
}
```

**Slide Up**:
```css
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-up {
  animation: slideUp 0.4s var(--ease-decelerate);
}
```

**Gradient Flow** (Digitaltableteur):
```css
@keyframes gradient-move {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.gradient-text {
  background: linear-gradient(120deg, #667eea, #764ba2, #f093fb);
  background-size: 200% 200%;
  animation: gradient-move 4s ease-in-out infinite;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### Reduced Motion

```css
/* Respect user preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Responsive Design

### Breakpoints

```css
/* Mobile First Approach */

/* Small (mobile) - default, no media query */
.container {
  padding: var(--space-16);
}

/* Medium (tablet) - 768px+ */
@media (min-width: 768px) {
  .container {
    padding: var(--space-24);
  }
}

/* Large (desktop) - 1024px+ */
@media (min-width: 1024px) {
  .container {
    padding: var(--space-32);
    max-width: 1200px;
  }
}

/* Extra Large (wide desktop) - 1440px+ */
@media (min-width: 1440px) {
  .container {
    max-width: 1400px;
  }
}
```

### Fluid Typography

```css
/* Scales smoothly between breakpoints */
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
  /* Min: 32px, Ideal: 5vw+16px, Max: 64px */
}

p {
  font-size: clamp(1rem, 1vw + 0.75rem, 1.25rem);
  /* Min: 16px, Ideal: 1vw+12px, Max: 20px */
}
```

---

## Design-to-Dev Handoff (Figma)

### Figma Best Practices

**Layer Naming**:
```
✅ Good: button-primary-large
❌ Bad: Rectangle 23
```

**Component Organization**:
```
Components/
├── Foundations/
│   ├── Colors
│   ├── Typography
│   └── Spacing
├── Atoms/
│   ├── Button
│   ├── Input
│   └── Icon
├── Molecules/
│   ├── Card
│   └── Form Field
└── Organisms/
    ├── Header
    └── Footer
```

**Auto Layout** (Flexbox equivalent):
- Use for all components
- Set spacing, padding explicitly
- Configure resizing behavior

**Variants** (Component states):
```
Button:
├── Variant: Primary, Secondary, Tertiary
├── Size: Small, Medium, Large
├── State: Default, Hover, Active, Disabled
└── Icon: Left, Right, None
```

### Handoff Checklist

- [ ] All text layers use shared text styles
- [ ] All colors reference design tokens (not hex values)
- [ ] Spacing uses 8px grid
- [ ] Components use Auto Layout
- [ ] All states documented (hover, active, disabled)
- [ ] Responsive behavior specified
- [ ] Accessibility notes added (alt text, ARIA labels)
- [ ] Interactive prototype for complex flows
- [ ] Developer mode enabled (CSS code snippets)

---

## Visual Hierarchy Techniques

### Size & Scale

```
Largest:   Display Headlines (guide attention immediately)
↓
Large:     Page Titles (establish context)
↓
Medium:    Section Headings (organize content)
↓
Base:      Body Text (readable, comfortable)
↓
Small:     Captions, Meta (supporting info)
```

### Weight & Contrast

```
Boldest:   CTAs, Primary Actions (demand action)
↓
Bold:      Headings (structure)
↓
Semibold:  Subheadings, Labels (clarity)
↓
Regular:   Body (readability)
↓
Light:     De-emphasized Text (background info)
```

### Color Emphasis

```
High Contrast:    Black on White (critical info)
Medium Contrast:  Gray on White (secondary info)
Low Contrast:     Light Gray on White (tertiary info)
Accent Color:     Brand Color (CTAs, highlights)
```

---

## Brand Application (Digitaltableteur)

### Brand Colors

```css
--accent-pink: #ff006e;
--accent-purple: #8338ec;
--accent-cyan: #00d9ff;
--accent-teal: #06ffa5;
--accent-yellow: #ffbe0b;
--accent-violet: #7209b7;

/* Gradient (Signature) */
--home-gradient: linear-gradient(120deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
```

### Section Accent Pattern

```tsx
// Rotate accent colors for visual rhythm
<section className={styles.sectionAccentPink}>
  {/* Content */}
</section>

<section className={styles.sectionAccentCyan}>
  {/* Content */}
</section>

<section className={styles.sectionAccentYellow}>
  {/* Content */}
</section>
```

### Gradient Text (CTAs)

```css
.gradientText {
  background: var(--home-gradient);
  background-size: 200% 200%;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient-move 4s ease-in-out infinite;
}
```

---

## Micro-Interactions (Visual Feedback)

### Button States

```css
.button {
  /* Idle */
  background-color: var(--color-primary);
  transform: scale(1);
  transition: all 0.2s ease;
}

.button:hover {
  /* Hover */
  background-color: var(--color-primary-600);
  transform: scale(1.05);
  box-shadow: var(--shadow-lg);
}

.button:active {
  /* Active (pressed) */
  transform: scale(0.98);
  box-shadow: var(--shadow-sm);
}

.button:focus-visible {
  /* Focus (keyboard) */
  outline: 4px solid rgba(0, 102, 204, 0.3);
  outline-offset: 2px;
}

.button:disabled {
  /* Disabled */
  background-color: var(--color-surface);
  color: var(--color-text-secondary);
  cursor: not-allowed;
  transform: scale(1);
}
```

### Loading States

```tsx
// Skeleton loader
<div className={styles.skeleton} />

/* CSS */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface) 0%,
    var(--color-border) 50%,
    var(--color-surface) 100%
  );
  background-size: 200% 100%;
  animation: loading 1.5s ease-in-out infinite;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
```

---

## When to Use This Skill

Activate this skill when:
- Designing UI components or patterns
- Creating design systems or style guides
- Choosing colors, typography, or spacing
- Building visual hierarchies
- Designing for accessibility (color contrast)
- Creating design tokens or CSS variables
- Working with Figma or design tools
- Defining animation and motion
- Designing responsive layouts
- Creating brand application guidelines
- Designing micro-interactions
- Conducting design QA or reviews
- Handing off designs to developers

**Remember**: Consistency and accessibility are non-negotiable. Always test designs with real users and assistive technologies.
