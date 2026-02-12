---
name: web-ui-best-practices
description: Opinionated constraints for building better user interfaces. Triggers on building or reviewing web components, pages, forms, modals, animations, or any frontend UI work. Covers accessibility, focus states, touch interactions, and performance.
---

# Web UI Best Practices

When invoked generally, apply these opinionated constraints for building better interfaces and for any UI work in this conversation.

When invoked with a file specified (i.e. `web-ui-best-practices <file>`), review the file against all constraints below and output:

1. violations (quote the exact line/snippet)
2. why it matters (1 short sentence)
3. a concrete fix (code-level suggestion)

## Stack

- MUST use Tailwind CSS defaults unless custom values already exist or are explicitly requested
- MUST use `motion/react` (formerly `framer-motion`) when JavaScript animation is required
- SHOULD use `tw-animate-css` for entrance and micro-animations in Tailwind CSS
- MUST use `cn` utility (`clsx` + `tailwind-merge`) for class logic

## Components

- MUST use accessible component primitives for anything with keyboard or focus behavior (`Base UI`, `Radix`, `React-Aria`)
- MUST use the project’s existing component primitives first
- NEVER mix primitive systems within the same interaction surface
- SHOULD prefer [`Base UI`](https://base-ui.com/react/components) for new primitives if compatible with the stack
- MUST add an `aria-label` to icon-only buttons
- NEVER rebuild keyboard or focus behavior by hand unless explicitly requested

## Interaction

- MUST use an `AlertDialog` for destructive or irreversible actions
- SHOULD use structural skeletons for loading states
- NEVER use `h-screen`, use `h-dvh`
- MUST show errors next to where the action happens
- NEVER block paste in `input` or `textarea` elements

## Navigation & State

- SHOULD reflect UI state in the URL (filters, tabs, pagination, expanded panels via query params)
- MUST use `<a>` / `<Link>` for navigation (Cmd/Ctrl+click and middle-click should work)
- SHOULD deep-link stateful UI (if it uses `useState`, consider URL sync via `nuqs` or similar)
- MUST require confirmation or undo window for destructive actions (never immediate)

## Touch & Interaction

- SHOULD set `touch-action: manipulation` on tappable controls (prevents double-tap zoom delay)
- SHOULD set `-webkit-tap-highlight-color` intentionally
- MUST use `overscroll-behavior: contain` in modals/drawers/sheets
- SHOULD during drag: disable text selection, `inert` on dragged elements
- SHOULD use `autoFocus` sparingly (desktop only, single primary input; avoid on mobile)

## Animation

- NEVER add animation unless it is explicitly requested
- MUST animate only compositor props (`transform`, `opacity`)
- NEVER animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`)
- SHOULD avoid animating paint properties (`background`, `color`) except for small, local UI (text, icons)
- SHOULD use `ease-out` on entrance
- NEVER exceed `200ms` for interaction feedback
- MUST pause looping animations when off-screen
- SHOULD respect `prefers-reduced-motion`
- NEVER introduce custom easing curves unless explicitly requested
- SHOULD avoid animating large images or full-screen surfaces
- SHOULD never `transition: all`—list properties explicitly
- SHOULD set correct `transform-origin`
- SHOULD have animations be interruptible—respond to user input mid-animation

## Typography

- MUST use `text-balance` for headings and `text-pretty` for body/paragraphs
- MUST use `tabular-nums` for data
- SHOULD use `truncate` or `line-clamp` for dense UI
- NEVER modify `letter-spacing` (`tracking-*`) unless explicitly requested
- SHOULD use `…` not `...`
- SHOULD use curly quotes `"` `"` not straight `"`
- SHOULD have non-breaking spaces: `10&nbsp;MB`, `⌘&nbsp;K`, brand names
- SHOULD have loading states end with `…`: `"Loading…"`, `"Saving…"`
- SHOULD use `font-variant-numeric: tabular-nums` for number columns/comparisons
- SHOULD have flex children need `min-w-0` to allow text truncation
- SHOULD handle empty states—don't render broken UI for empty strings/arrays
- SHOULD consider that user-generated input fields may have short, average, and very long inputs

## Layout

- MUST use a fixed `z-index` scale (no arbitrary `z-*`)
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

## Safe Areas & Layout

- MUST respect `env(safe-area-inset-*)` for full-bleed layouts and fixed elements on notched devices
- SHOULD avoid unwanted scrollbars (use `overflow-x-hidden` on containers and fix overflow at the source)
- SHOULD prefer flex/grid over JS measurement for layout

## Dark Mode & Theming

- MUST set `color-scheme: dark` on `<html>` for dark themes (fixes scrollbars and native inputs)
- SHOULD set `<meta name="theme-color">` to match the page background
- SHOULD set explicit `background-color` and `color` on native `<select>` (Windows dark mode)

## Locale & i18n

- MUST use `Intl.DateTimeFormat` (no hardcoded date/time formats)
- MUST use `Intl.NumberFormat` (no hardcoded number/currency formats)
- SHOULD detect language via `Accept-Language` / `navigator.languages`, not IP

## Hydration Safety

- MUST provide `onChange` for inputs with `value` (or use `defaultValue` for uncontrolled inputs)
- MUST guard date/time rendering against hydration mismatches (server vs client)
- SHOULD use `suppressHydrationWarning` only where truly needed

## Hover & Interactive States

- SHOULD provide `hover:` states for buttons/links (visual feedback)
- SHOULD increase contrast for interactive states (hover/active/focus more prominent than rest)

## Images

- MUST set explicit `width` and `height` on `<img>` (prevents CLS)
- SHOULD set `loading="lazy"` for below-fold images
- SHOULD set `priority` or `fetchpriority="high"` for above-fold critical images

## Performance

- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for anything that can be expressed as render logic
- SHOULD virtualize large lists (>50 items) (e.g. `virtua` or `content-visibility: auto` where appropriate)
- MUST avoid layout reads during render (`getBoundingClientRect`, `offsetHeight`, `offsetWidth`, `scrollTop`)
- SHOULD batch DOM reads/writes (avoid interleaving)
- SHOULD prefer uncontrolled inputs; controlled inputs must be cheap per keystroke
- SHOULD add `<link rel="preconnect">` for CDN/asset domains
- SHOULD preload critical fonts (`<link rel="preload" as="font">`) and use `font-display: swap`

## Design

- NEVER use gradients unless explicitly requested
- NEVER use purple or multicolor gradients
- NEVER use glow effects as primary affordances
- SHOULD use Tailwind CSS default shadow scale unless explicitly requested
- MUST give empty states one clear next action
- SHOULD limit accent color usage to one per view
- SHOULD use existing theme or Tailwind CSS color tokens before introducing new ones

## Design Direction (when aesthetics requested)

- MUST choose a clear aesthetic direction and execute consistently (e.g., brutally minimal, editorial, utilitarian, playful)
- SHOULD use deliberate typography (1 display + 1 body) and avoid accidental defaults; follow product font system when it exists
- SHOULD define theme/palette via CSS variables; use one dominant base + sharp accent
- SHOULD match implementation complexity to the aesthetic (minimal = restraint; maximal = elaborate but controlled)
- If motion is explicitly requested: prefer one cohesive high-impact sequence (load stagger, scroll reveal) over scattered micro-interactions
- SHOULD avoid cookie-cutter layout/component patterns; make 1-2 distinctive choices grounded in context

## Content & Copy

- SHOULD use active voice ("Install the CLI" not "The CLI will be installed")
- SHOULD use specific button labels ("Save API Key" not "Continue")
- SHOULD write error messages with a fix/next step, not just the problem
- SHOULD write in second person; avoid first person
- SHOULD use `&` over "and" where space-constrained

## Anti-patterns (flag these)

- `user-scalable=no` or `maximum-scale=1` disabling zoom
- `onPaste` with `preventDefault`
- `transition: all`
- `outline-none` without a `focus-visible` replacement
- Inline `onClick` navigation without `<a>` / `<Link>`
- `<div>` / `<span>` with click handlers (use `<button>`)
- Images without dimensions
- Large arrays `.map()` without virtualization
- Form inputs without labels
- Icon buttons without `aria-label`
- Hardcoded date/number formats (use `Intl.*`)
- `autoFocus` without clear justification

## Rules if not found in primitives

The below rules apply if the pattern is either explicitly requested or not found in the primitive itself already.

### Accessibility

- Icon-only buttons need `aria-label`
- Form controls need `<label>` or `aria-label`
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`)
- `<button>` for actions, `<a>`/`<Link>` for navigation (not `<div onClick>`)
- Images need `alt` (or `alt=""` if decorative)
- Decorative icons need `aria-hidden="true"`
- Async updates (toasts, validation) need `aria-live="polite"`
- Use semantic HTML (`<button>`, `<a>`, `<label>`, `<table>`) before ARIA
- Headings hierarchical `<h1>`–`<h6>`; include skip link for main content
- `scroll-margin-top` on heading anchors

### Focus States

- Interactive elements need visible focus: `focus-visible:ring-*` or equivalent
- Never `outline-none` / `outline: none` without focus replacement
- Use `:focus-visible` over `:focus` (avoid focus ring on click)
- Group focus with `:focus-within` for compound controls

### Forms

- Inputs need `autocomplete` and meaningful `name`
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`
- Never block paste (`onPaste` + `preventDefault`)
- Labels clickable (`htmlFor` or wrapping control)
- Disable spellcheck on emails, codes, usernames (`spellCheck={false}`)
- Checkboxes/radios: label + control share single hit target (no dead zones)
- Submit button stays enabled until request starts; spinner during request
- Errors inline next to fields; focus first error on submit
- Placeholders end with `…` and show example pattern
- `autocomplete="off"` on non-auth fields to avoid password manager triggers
- Warn before navigation with unsaved changes (`beforeunload` or router guard)
