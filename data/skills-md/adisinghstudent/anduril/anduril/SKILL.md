---
name: anduril
description: Opinionated constraints for building better interfaces with Anduril-style design.
---

# Anduril Design System

When invoked, apply these opinionated constraints for building better interfaces.

## How to use

- `/anduril` — Apply these constraints to any UI work in this conversation.
- `/anduril <file>` — Review the file against all constraints and output violations, why it matters, and a concrete fix.

---

## Design System: Anduril

### Colors

**Core Palette**
```css
/* Backgrounds */
--bg-black: #000000;        /* Pure black - dark mode primary */
--bg-dark: #1a1a1a;         /* Near black - dark mode secondary */
--bg-warm: #f5f3ef;         /* Warm off-white - light mode primary */
--bg-white: #ffffff;        /* Pure white - cards, inputs */

/* Text */
--text-primary: #010101;    /* Near black */
--text-inverse: #ffffff;    /* White on dark */
--text-muted: #666666;      /* Secondary text */
--text-subtle: #999999;     /* Tertiary text */

/* Brand Accent */
--accent-lime: #DFF140;     /* Anduril signature lime - primary accent */
--accent-lime-hover: #c8d93a;

/* Semantic */
--color-error: #FF3535;     /* Red - errors, destructive */
--color-error-bg: #fef2f2;
--color-success: #16a34a;   /* Green - success states */
--color-success-bg: #f0fdf4;
--color-info: #2563eb;      /* Blue - info, links */
--color-info-bg: #eff6ff;
--color-warning: #f59e0b;   /* Amber - warnings */
--color-warning-bg: #fffbeb;

/* Borders */
--border-light: #e5e5e5;
--border-default: #ddd;
--border-dark: #333333;
```

**Tailwind Config**
```js
colors: {
  anduril: {
    black: '#000000',
    dark: '#1a1a1a',
    warm: '#f5f3ef',
    lime: '#DFF140',
    'lime-hover': '#c8d93a',
  }
}
```

**Usage Guidelines**
- Use `--accent-lime` sparingly — one accent per view
- Dark mode: `--bg-black` background, `--accent-lime` for CTAs
- Light mode: `--bg-warm` background, `--text-primary` for CTAs
- NEVER use lime on light backgrounds (poor contrast)
- Reserve `--color-error` for destructive actions only

### Typography
- MUST use `'Helvetica Neue', Helvetica, Arial, sans-serif`
- Base font size: `15px`, weight: `400`, line-height: `1.5`
- Headers: `font-weight: 400` (never bold)
- Labels: `11px`, `uppercase`, `letter-spacing: 0.05em`, `color: var(--text-muted)`
- Hero headings: `48px`, `font-weight: 400`, `line-height: 1.1`
- Navigation/header text: `14px`, `uppercase`, `letter-spacing: 0.1em`

### Spacing
- Cards: `padding: 32px`
- Main content: `padding: 48px`, `max-width: 1200px`
- Header: `padding: 24px 48px`
- Form elements: `margin-top: 16px` between fields

### Components

**Cards**
- `background: #ffffff`
- `border: none` — NO borders
- `border-radius: 0` — sharp corners always
- NO shadows

**Buttons**
- `background: var(--text-primary)`
- `color: var(--text-inverse)`
- `border: 1px solid var(--text-primary)`
- `padding: 12px 24px`
- `border-radius: 0` — sharp corners
- `font-weight: 400`
- Hover: `opacity: 0.85`
- Disabled: `opacity: 0.5`

**Inputs**
- `padding: 10px 12px`
- `border: 1px solid #ddd`
- `border-radius: 0`
- Focus: `border-color: var(--text-primary)`, no outline

**Method badges**
- `font-family: monospace`
- `font-size: 11px`
- `text-transform: uppercase`
- `letter-spacing: 0.05em`
- `padding: 4px 8px`
- POST: `color: #2563eb; background: #eff6ff`
- GET: `color: #16a34a; background: #f0fdf4`

**Response/code blocks**
- `background: var(--bg-warm)`
- `font-family: monospace`
- `font-size: 12px`
- Error state: `background: #fef2f2; color: #dc2626`
- Success state: `background: #f0fdf4; color: #16a34a`

---

## Stack

- MUST use Tailwind CSS defaults unless custom values already exist
- MUST use `motion/react` when JavaScript animation is required
- SHOULD use `tw-animate-css` for entrance and micro-animations
- MUST use `cn` utility (`clsx` + `tailwind-merge`) for class logic

## Components

- MUST use accessible component primitives (`Base UI`, `React Aria`, `Radix`)
- MUST use the project's existing primitives first
- NEVER mix primitive systems within the same surface
- MUST add `aria-label` to icon-only buttons
- NEVER rebuild keyboard or focus behavior by hand

## Interaction

- MUST use `AlertDialog` for destructive actions
- SHOULD use structural skeletons for loading states
- NEVER use `h-screen`, use `h-dvh`
- MUST respect `safe-area-inset` for fixed elements
- MUST show errors next to where the action happens
- NEVER block paste in inputs

## Animation

- NEVER add animation unless explicitly requested
- MUST animate only compositor props (`transform`, `opacity`)
- NEVER animate layout props (`width`, `height`, `top`, `left`, `margin`, `padding`)
- SHOULD use `ease-out` on entrance
- NEVER exceed `200ms` for interaction feedback
- MUST pause looping animations when off-screen
- SHOULD respect `prefers-reduced-motion`

## Typography

- MUST use `text-balance` for headings, `text-pretty` for body
- MUST use `tabular-nums` for data
- SHOULD use `truncate` or `line-clamp` for dense UI
- NEVER modify `letter-spacing` unless explicitly requested

## Layout

- MUST use a fixed `z-index` scale (no arbitrary `z-*`)
- SHOULD use `size-*` for square elements

## Performance

- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for render logic

## Design — Anduril Style

**Shape & Surface**
- NEVER use border-radius — sharp corners only
- NEVER use shadows on cards
- NEVER use gradients
- NEVER use glow effects
- NEVER use purple or multicolor anything

**Color Usage**
- Light mode: `--bg-warm` (#f5f3ef) background, dark buttons
- Dark mode: `--bg-black` (#000000) background, lime accent CTAs
- MUST use `--accent-lime` (#DFF140) for primary actions in dark mode only
- NEVER use lime on light backgrounds — use near-black instead
- SHOULD limit accent color to ONE per view
- Use semantic colors (`--color-error`, `--color-success`) consistently

**Typography**
- MUST keep headers lightweight (`font-weight: 400`)
- MUST use uppercase + letter-spacing for labels and nav
- NEVER use bold for headings

**States**
- MUST give empty states one clear next action
- Error states: red text (#FF3535), light red background (#fef2f2)
- Success states: green text (#16a34a), light green background (#f0fdf4)
- Disabled: `opacity: 0.5`, `cursor: not-allowed`
