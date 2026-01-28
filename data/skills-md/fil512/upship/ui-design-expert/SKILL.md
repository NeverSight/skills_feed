---
name: ui-design-expert
description: Expert UI design guidance for polishing game interfaces. Use when reviewing screenshots, recommending CSS improvements, designing color schemes, improving typography, adding visual polish, or making the game look professional. Specializes in board game aesthetics with a steampunk/brass era theme.
---

# UI Design Expert Skill

## Overview

This skill provides expert guidance for reviewing game UI screenshots and recommending visual improvements. It covers color theory, typography, layout, shadows, animations, and CSS patterns that create a polished, professional board game experience.

The aesthetic targets a **steampunk/brass era** theme appropriate for UP SHIP!'s 1900-1937 Golden Age of Airships setting.

## Screenshot Review Workflow

When reviewing a screenshot, analyze in this order:

### 1. First Impressions (2 seconds)
- What draws the eye first? Is it the right thing?
- Does it feel cohesive or scattered?
- Is the theme immediately apparent?

### 2. Visual Hierarchy Check
- Are important elements (current action, player status) prominent?
- Is there clear distinction between interactive and static elements?
- Can you tell whose turn it is at a glance?

### 3. Color & Contrast Audit
- Are colors from the defined palette?
- Is text readable against backgrounds? (4.5:1 minimum contrast)
- Are accent colors used sparingly for emphasis?

### 4. Spacing & Alignment
- Is spacing consistent throughout?
- Are related elements grouped together?
- Is there enough breathing room (white space)?

### 5. Polish & Detail
- Do interactive elements have hover states?
- Are there appropriate shadows for depth?
- Do cards/components look tactile?

### 6. Recommendations
- Prioritize by impact: highest visual improvement per CSS change
- Provide specific CSS code snippets
- Reference the style guide sections below

---

## Color Palette: Steampunk Brass Era

### Primary Colors

```css
:root {
  /* Brass & Copper - The heart of steampunk */
  --brass-gold: #C08B51;
  --brass-light: #D4A76A;
  --copper: #A7623C;
  --copper-dark: #8B4D32;

  /* Deep Industrial - Backgrounds and panels */
  --slate-dark: #1a1a2e;
  --slate: #16213e;
  --charcoal: #2c2c3e;
  --iron: #3d3d4a;

  /* Accent - Teal/Patina (oxidized copper) */
  --patina: #34544F;
  --patina-light: #4a7a72;
  --patina-bright: #5fa093;

  /* Parchment & Cream - Text backgrounds, cards */
  --parchment: #F5DEB3;
  --cream: #DBCA9A;
  --ivory: #f5f0e6;
  --paper: #e8e0d0;
}
```

### Semantic Colors

```css
:root {
  /* Text */
  --text-dark: #2c2417;
  --text-medium: #5c5040;
  --text-light: #f5f0e6;
  --text-muted: #8a7f6a;

  /* Status Colors (keep muted to fit theme) */
  --success: #5a8a5a;        /* Muted green */
  --warning: #c4a035;        /* Amber/gold */
  --danger: #a85454;         /* Muted red */
  --info: #5a7a9a;           /* Steel blue */

  /* Interactive States */
  --highlight: #C08B51;      /* Brass for selection */
  --highlight-glow: rgba(192, 139, 81, 0.3);
  --focus-ring: #D4A76A;
}
```

### Faction Colors

```css
:root {
  /* Player/Faction Colors */
  --germany: #1a1a2e;        /* Deep slate/iron */
  --britain: #8B0000;        /* Deep crimson */
  --usa: #1e3a5f;            /* Navy blue */
  --italy: #2d5a3d;          /* Forest green */

  /* Lighter variants for backgrounds */
  --germany-light: #2c2c3e;
  --britain-light: #a83232;
  --usa-light: #2d5478;
  --italy-light: #3d7a52;
}
```

### Usage Guidelines

| Element | Color | Reason |
|---------|-------|--------|
| Backgrounds | `--slate-dark`, `--slate` | Dark creates drama, focus |
| Cards/Panels | `--parchment`, `--cream` | Warm, readable surfaces |
| Primary buttons | `--brass-gold` | Eye-catching, action-oriented |
| Secondary buttons | `--patina` | Distinct but muted |
| Text on dark | `--ivory`, `--cream` | High contrast |
| Text on light | `--text-dark` | Readable, warm |
| Accents/highlights | `--copper` | Period-appropriate gold |
| Borders | `--copper-dark`, `--iron` | Subtle definition |

---

## Typography

### Font Stack

```css
:root {
  /* Display/Headers - Period-appropriate serif */
  --font-display: 'Cinzel', 'Playfair Display', 'Georgia', serif;

  /* Body text - Clean, readable sans-serif */
  --font-body: 'Inter', 'Segoe UI', system-ui, sans-serif;

  /* Monospace - For numbers, stats */
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}
```

### Type Scale

```css
:root {
  --text-xs: 0.75rem;    /* 12px - Labels, captions */
  --text-sm: 0.875rem;   /* 14px - Secondary text */
  --text-base: 1rem;     /* 16px - Body text (minimum!) */
  --text-lg: 1.125rem;   /* 18px - Emphasized body */
  --text-xl: 1.25rem;    /* 20px - Card titles */
  --text-2xl: 1.5rem;    /* 24px - Section headers */
  --text-3xl: 2rem;      /* 32px - Page titles */
  --text-4xl: 2.5rem;    /* 40px - Hero text */
}
```

### Typography Patterns

```css
/* Game title/logo */
.game-title {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: 700;
  color: var(--brass-gold);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* Section headers */
.section-header {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 600;
  color: var(--cream);
  border-bottom: 2px solid var(--copper);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

/* Card titles */
.card-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--text-dark);
}

/* Body text */
.body-text {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: 1.6;
  color: var(--text-dark);
}

/* Stats and numbers */
.stat-value {
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--brass-gold);
}

/* Labels */
.label {
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
}
```

---

## Layout & Spacing

### Spacing Scale

```css
:root {
  --space-1: 0.25rem;    /* 4px */
  --space-2: 0.5rem;     /* 8px */
  --space-3: 0.75rem;    /* 12px */
  --space-4: 1rem;       /* 16px */
  --space-5: 1.5rem;     /* 24px */
  --space-6: 2rem;       /* 32px */
  --space-8: 3rem;       /* 48px */
  --space-10: 4rem;      /* 64px */
}
```

### Layout Principles

1. **Group related elements** - Cards with their stats, buttons with their labels
2. **Use consistent gaps** - Pick 2-3 spacing values and stick to them
3. **Create breathing room** - Don't crowd the interface
4. **Align to grid** - Use CSS Grid or consistent flexbox patterns

```css
/* Panel layout with consistent spacing */
.panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-5);
}

/* Card grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--space-4);
}

/* Inline stats */
.stat-row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
```

---

## Cards & Panels

### Base Card Style

```css
.card {
  background: linear-gradient(135deg, var(--parchment) 0%, var(--cream) 100%);
  border: 2px solid var(--copper-dark);
  border-radius: 8px;
  padding: var(--space-4);
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.1),
    0 4px 8px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 4px 8px rgba(0, 0, 0, 0.15),
    0 8px 16px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.card.selected {
  border-color: var(--brass-gold);
  box-shadow:
    0 0 0 3px var(--highlight-glow),
    0 4px 8px rgba(0, 0, 0, 0.15);
}
```

### Dark Panel (for sidebars, overlays)

```css
.panel-dark {
  background: linear-gradient(180deg, var(--slate) 0%, var(--slate-dark) 100%);
  border: 1px solid var(--iron);
  border-radius: 8px;
  padding: var(--space-5);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.05),
    0 4px 16px rgba(0, 0, 0, 0.3);
}
```

### Tech/Upgrade Tile

```css
.tech-tile {
  background: var(--paper);
  border: 2px solid var(--copper);
  border-radius: 6px;
  padding: var(--space-3);
  position: relative;
  overflow: hidden;
}

/* Brass corner accents */
.tech-tile::before,
.tech-tile::after {
  content: '';
  position: absolute;
  width: 12px;
  height: 12px;
  background: var(--brass-gold);
  clip-path: polygon(0 0, 100% 0, 0 100%);
}

.tech-tile::before {
  top: 0;
  left: 0;
}

.tech-tile::after {
  bottom: 0;
  right: 0;
  transform: rotate(180deg);
}
```

### Playing Card Style

```css
.playing-card {
  width: 120px;
  height: 180px;
  background: var(--ivory);
  border: 1px solid var(--text-muted);
  border-radius: 8px;
  padding: var(--space-2);
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.12),
    0 2px 6px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

.playing-card .card-symbol {
  font-size: var(--text-3xl);
  text-align: center;
  color: var(--copper);
}

/* Card in hand - overlapping fan */
.hand .playing-card {
  margin-left: -40px;
  transition: transform 0.2s ease, margin 0.2s ease;
}

.hand .playing-card:first-child {
  margin-left: 0;
}

.hand .playing-card:hover {
  transform: translateY(-20px) scale(1.05);
  z-index: 10;
  margin-left: 0;
  margin-right: 40px;
}
```

---

## Buttons

### Primary Button (Brass)

```css
.btn-primary {
  background: linear-gradient(180deg, var(--brass-light) 0%, var(--brass-gold) 100%);
  border: 2px solid var(--copper);
  border-radius: 6px;
  padding: var(--space-2) var(--space-4);
  color: var(--text-dark);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: linear-gradient(180deg, var(--brass-gold) 0%, var(--copper) 100%);
  transform: translateY(-2px);
  box-shadow:
    0 4px 8px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.2),
    inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-primary:disabled {
  background: var(--iron);
  border-color: var(--iron);
  color: var(--text-muted);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
```

### Secondary Button (Patina/Teal)

```css
.btn-secondary {
  background: transparent;
  border: 2px solid var(--patina);
  border-radius: 6px;
  padding: var(--space-2) var(--space-4);
  color: var(--patina-light);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: var(--patina);
  color: var(--ivory);
  border-color: var(--patina-light);
}
```

### Icon Button

```css
.btn-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--charcoal);
  border: 1px solid var(--iron);
  color: var(--cream);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background: var(--patina);
  border-color: var(--patina-light);
  transform: scale(1.1);
}
```

---

## Shadows & Depth

### Layered Shadow System

```css
:root {
  /* Elevation levels */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.1);

  --shadow-md:
    0 2px 4px rgba(0, 0, 0, 0.1),
    0 4px 8px rgba(0, 0, 0, 0.1);

  --shadow-lg:
    0 4px 8px rgba(0, 0, 0, 0.1),
    0 8px 16px rgba(0, 0, 0, 0.1),
    0 16px 32px rgba(0, 0, 0, 0.1);

  --shadow-xl:
    0 8px 16px rgba(0, 0, 0, 0.15),
    0 16px 32px rgba(0, 0, 0, 0.15),
    0 32px 64px rgba(0, 0, 0, 0.1);

  /* Glow effects */
  --glow-brass: 0 0 20px rgba(192, 139, 81, 0.4);
  --glow-patina: 0 0 20px rgba(52, 84, 79, 0.4);
}
```

### Inset/Recessed Effects

```css
/* Recessed input fields */
.input-field {
  background: var(--paper);
  border: 1px solid var(--copper-dark);
  border-radius: 4px;
  padding: var(--space-2) var(--space-3);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Pressed button state */
.btn-pressed {
  box-shadow:
    inset 0 2px 4px rgba(0, 0, 0, 0.2),
    inset 0 0 0 1px rgba(0, 0, 0, 0.1);
}

/* Engraved text effect */
.text-engraved {
  color: var(--iron);
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.3),
    0 -1px 0 rgba(0, 0, 0, 0.2);
}
```

---

## Icons & Symbols

### Icon Guidelines

1. **Consistency** - Use one icon set throughout (Lucide, Heroicons, or custom SVG)
2. **Size scale** - 16px (inline), 20px (buttons), 24px (standalone), 32px (feature)
3. **Color** - Icons inherit text color by default; use accent colors sparingly
4. **Stroke width** - Match to font weight (1.5-2px for regular text)

### Game-Specific Icons

```css
/* Icon sizing */
.icon-sm { width: 16px; height: 16px; }
.icon-md { width: 20px; height: 20px; }
.icon-lg { width: 24px; height: 24px; }
.icon-xl { width: 32px; height: 32px; }

/* Resource icons with color coding */
.icon-cash { color: var(--brass-gold); }
.icon-hydrogen { color: #5588cc; }  /* Blue gas */
.icon-helium { color: #cc8855; }    /* Orange/amber gas */
.icon-officers { color: var(--cream); }
.icon-engineers { color: var(--patina-light); }
```

### Symbol Reference

| Resource | Symbol | Color |
|----------|--------|-------|
| Cash | Pound sign / Coin | Brass gold |
| Hydrogen | Blue flame / H2 | Steel blue |
| Helium | Orange balloon / He | Amber |
| Officers | Person / Hat | Cream |
| Engineers | Wrench / Gear | Patina |
| Lift | Up arrow / Balloon | Light |
| Weight | Down arrow / Anchor | Dark |

---

## Animations & Transitions

### Base Transitions

```css
:root {
  --transition-fast: 150ms ease;
  --transition-normal: 200ms ease;
  --transition-slow: 300ms ease;

  /* Specific easing for different actions */
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Apply transitions thoughtfully */
.interactive {
  transition:
    transform var(--transition-normal),
    box-shadow var(--transition-normal),
    background-color var(--transition-fast);
}
```

### Hover & Selection Effects

```css
/* Lift on hover */
.hoverable:hover {
  transform: translateY(-4px);
}

/* Subtle pulse for attention */
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 0 0 var(--highlight-glow); }
  50% { box-shadow: 0 0 0 8px transparent; }
}

.attention {
  animation: pulse-glow 2s ease-in-out infinite;
}

/* Selection ring */
.selectable.selected {
  outline: 3px solid var(--brass-gold);
  outline-offset: 2px;
}
```

### State Change Animations

```css
/* Value change highlight */
@keyframes value-change {
  0% { background: var(--highlight-glow); }
  100% { background: transparent; }
}

.stat-changed {
  animation: value-change 0.5s ease-out;
}

/* Income popup */
@keyframes float-up {
  0% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-30px); }
}

.income-popup {
  animation: float-up 1s ease-out forwards;
  color: var(--success);
  font-weight: bold;
}
```

### Card Flip

```css
.card-flipper {
  perspective: 1000px;
}

.card-inner {
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.card-flipper.flipped .card-inner {
  transform: rotateY(180deg);
}

.card-front, .card-back {
  backface-visibility: hidden;
  position: absolute;
  width: 100%;
  height: 100%;
}

.card-back {
  transform: rotateY(180deg);
}
```

---

## Accessibility

### Contrast Requirements

| Text Type | Minimum Ratio | Our Colors |
|-----------|---------------|------------|
| Body text | 4.5:1 | `--text-dark` on `--parchment` = 9.2:1 |
| Large text (24px+) | 3:1 | `--cream` on `--slate-dark` = 8.1:1 |
| UI components | 3:1 | `--brass-gold` on `--slate` = 4.8:1 |

### Focus States

```css
/* Visible focus for keyboard users */
:focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 2px;
}

/* Remove default outline only when custom is applied */
button:focus:not(:focus-visible) {
  outline: none;
}
```

### Motion Preferences

```css
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

### Screen Reader Support

```css
/* Visually hidden but accessible */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Common UI Patterns

### Resource Display

```css
.resource-bar {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-3);
  background: var(--charcoal);
  border-radius: 6px;
  border: 1px solid var(--iron);
}

.resource-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.resource-icon {
  width: 24px;
  height: 24px;
}

.resource-value {
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--cream);
}
```

### Turn Indicator

```css
.turn-indicator {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--slate);
  border-left: 4px solid var(--brass-gold);
  border-radius: 0 6px 6px 0;
}

.turn-indicator.my-turn {
  background: linear-gradient(90deg, rgba(192, 139, 81, 0.2) 0%, transparent 100%);
  animation: pulse-glow 2s ease-in-out infinite;
}
```

### Tooltip

```css
.tooltip {
  position: absolute;
  background: var(--slate-dark);
  border: 1px solid var(--copper-dark);
  border-radius: 6px;
  padding: var(--space-3);
  max-width: 250px;
  box-shadow: var(--shadow-lg);
  z-index: 1000;
  pointer-events: none;
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 0.2s, transform 0.2s;
}

.tooltip.visible {
  opacity: 1;
  transform: translateY(0);
}

.tooltip-arrow {
  position: absolute;
  width: 8px;
  height: 8px;
  background: var(--slate-dark);
  border-left: 1px solid var(--copper-dark);
  border-top: 1px solid var(--copper-dark);
  transform: rotate(45deg);
  top: -5px;
  left: 20px;
}
```

### Modal/Dialog

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: linear-gradient(180deg, var(--cream) 0%, var(--parchment) 100%);
  border: 3px solid var(--copper);
  border-radius: 12px;
  padding: var(--space-6);
  max-width: 500px;
  width: 90%;
  box-shadow: var(--shadow-xl);
}

.modal-header {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  color: var(--text-dark);
  border-bottom: 2px solid var(--copper);
  padding-bottom: var(--space-3);
  margin-bottom: var(--space-4);
}
```

---

## Checklist: Before Shipping

Use this checklist when reviewing the final UI:

### Visual Polish
- [ ] All colors from the defined palette
- [ ] Consistent spacing using the scale
- [ ] Cards/panels have appropriate shadows
- [ ] Interactive elements have hover states
- [ ] Selected states are clearly visible
- [ ] Typography hierarchy is clear

### Usability
- [ ] Current player/turn is obvious
- [ ] Available actions are highlighted
- [ ] Disabled elements look disabled
- [ ] Loading states exist where needed
- [ ] Error states are styled

### Accessibility
- [ ] Text has 4.5:1 contrast minimum
- [ ] Focus states are visible
- [ ] Interactive elements are keyboard accessible
- [ ] Motion respects user preferences

### Theme Consistency
- [ ] Brass/copper accents for primary actions
- [ ] Parchment/cream for content cards
- [ ] Dark slate for backgrounds/panels
- [ ] Patina/teal for secondary elements
- [ ] Period-appropriate typography

---

## When This Skill Activates

Use this skill when:
- Reviewing UI screenshots for improvements
- Recommending CSS changes for visual polish
- Designing color schemes or typography
- Creating new UI components
- Fixing visual inconsistencies
- Adding animations or transitions
- Improving accessibility
- Making the game look more professional
