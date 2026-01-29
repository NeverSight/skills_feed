---
name: web-features-summary
description: This skill should be used when the user is performing "frontend development", working with "HTML" or "CSS", or writing "JavaScript" (including "server-side JS", "Node.js", or "JS scripting"). It provides guidance on modern web features that have recently reached cross-browser Baseline status.
version: 1.0.0
---

# Web Features Summary (Baseline 2023-2026)

This skill summarizes web platform features that achieved Baseline status (available in all major browsers: Chrome, Firefox, Safari) between January 2023 and early 2026. Use this to ensure recommended APIs are widely available without polyfills.

## High-Impact Modern Features (Quick Reference)

### JavaScript & Web APIs
- **Array & Collections:**
  - `toSorted()`, `toReversed()`, `toSpliced()`, `with()` (Immutable array updates)
  - `Object.groupBy()`, `Map.groupBy()` (Data grouping)
  - `Set` methods: `intersection()`, `union()`, `difference()`, `symmetricDifference()`
- **Async & Control Flow:**
  - `Promise.withResolvers()` (External promise resolution)
  - `Promise.try()` (Wrap sync/async functions in a Promise)
  - `AbortSignal.any()` (Combine multiple abort signals)
  - `Array.fromAsync()` (Consume async iterables)
- **Utilities:**
  - `URL.canParse()` (Safe URL validation)
  - `Intl.Segmenter` (Locale-sensitive text segmentation)
  - `Intl.DurationFormat` (Duration string formatting)
  - `RegExp.escape()` (Escape special characters in regex strings)

### CSS
- **Layout & Scoping:**
  - **Subgrid:** (`grid-template-columns: subgrid`) Align nested grids to parent tracks.
  - **Container Queries:** (`@container`) Style based on parent size, not viewport.
  - **@scope:** (`@scope (.card) to (.content)`) True style scoping without BEM/Modules.
  - **Nesting:** Native CSS nesting (similar to Sass).
- **Colors & Theming:**
  - `light-dark()`: native light/dark mode color switching.
  - `color-mix()`: Mix colors in any space (e.g., `color-mix(in srgb, red, blue)`).
  - `Relative colors`: Derive colors from others (`rgb(from var(--bg) r g b / 50%)`).
- **Typography & Math:**
  - `text-wrap: balance` (Titles) & `text-wrap: pretty` (Body text).
  - Math functions: `pow()`, `sqrt()`, `hypot()`, `log()`, `exp()`, `round()`, `mod()`, `rem()`, `abs()`, `sign()`.
- **UI & Interaction:**
  - `scrollbar-color` / `scrollbar-width` (Standardized scrollbar styling).
  - `@starting-style` (Entry animations for `display: none` elements).
  - `view-transitions` (Native page/element transitions).

### HTML & DOM
- **Interactivity:**
  - `popover` API (Native overlays/tooltips without z-index wars).
  - `<dialog>` element (now with `requestClose()` for safe closing).
  - `inert` attribute (Disable interaction for parts of the DOM).
- **Semantics & Loading:**
  - `<search>` element (Semantic wrapper for search forms).
  - `<link rel="modulepreload">` (Preload ES modules).
  - `fetchpriority` (Hint resource priority to browser).

## Chrome-Supported Modern Features (Limited Availability)
These features are usable in modern Chrome/Edge (Chromium) but lack full cross-browser support. **Use with caution** and always provide fallbacks.

### CSS & UI
- **Anchor Positioning:** (`position-anchor`, `anchor()`)
  - *Status:* Chrome 125+. No Firefox/Safari support.
  - *Use Case:* Tying tooltips/menus to trigger elements without JS.
  - *Interop:* Requires polyfill or JS fallback (e.g., Floating UI) for other browsers.
- **Scroll-Driven Animations:** (`animation-timeline: scroll()`)
  - *Status:* Chrome 115+. No stable Firefox/Safari.
  - *Use Case:* Parallax effects, reading progress bars linked to scroll position.
  - *Interop:* Graceful degradation (animation just doesn't play).
- **@scope:**
  - *Status:* Chrome 118+, Safari 17.4+. Firefox pending.
  - *Use Case:* True component-level styling isolation.
  - *Interop:* Use BEM/Modules as fallback for Firefox.
- **Container Style Queries:** (`@container style(...)`)
  - *Status:* Chrome 111+. No Firefox/Safari.
  - *Use Case:* Styling children based on parent's *computed values* (e.g., color).
  - *Interop:* Highly experimental.

### Web Capabilities (Fugu)
- **File System Access API:** (`window.showOpenFilePicker()`)
  - *Status:* Chrome 86+, Safari (Origin Private FS only). Firefox (Origin Private FS only).
  - *Use Case:* Reading/Writing local user files directly.
  - *Interop:* Progressive enhancement only.
- **View Transitions (Cross-Document):** (`@view-transition { navigation: auto; }`)
  - *Status:* Chrome 126+. Safari 18+. Firefox pending.
  - *Use Case:* Morphing animations between multi-page navigations.
  - *Interop:* Graceful degradation (instant navigation).
  - **Web Hardware APIs:** Chrome-only. Firefox/Safari unlikely to implement.

## Modern Best Practices & Discarded Idioms

### Adopt These Idioms
- **Immutable Arrays:** Use `toSorted()`, `toSpliced()`, and `with()` instead of mutation.
- **Native Grouping:** Use `Object.groupBy()` instead of `reduce()` patterns.
- **Parent Selectors:** Use `:has()` instead of JS-based class toggling for parent state.
- **Component-First Responsive:** Use `@container` instead of `@media` for internal component layout.
- **Native Overlays:** Use `<dialog>` and `popover` instead of custom modal/tooltip logic.
- **Native Nesting:** Use CSS nesting directly; reduce reliance on preprocessors for basic nesting.

### Discard These Patterns
- **Mutation-in-place:** Stop using `sort()` or `reverse()` on original arrays when state management is involved.
- **Viewport-Only Design:** Stop assuming component layout is tied strictly to screen size.
- **JS-Heavy UI:** Stop using JavaScript for focus trapping, z-index management, and simple "click-outside" logic that `<dialog>` and `popover` handle natively.

## Procedural Guidance

### Verify Feature Availability
1. Check the feature name against the list in `references/baseline_2023_2026.md`.
2. Check `references/modern_idioms.md` for recommended coding patterns.
3. Verify the "Baseline Status" and date.

## Additional Resources

### Reference Files
- **`references/baseline_2023_2026.md`** - Comprehensive list of 100+ web features reaching Baseline status.
- **`references/modern_idioms.md`** - Detailed comparison of legacy vs. modern coding patterns.


### Source Data
Information derived from the [web-features](https://www.npmjs.com/package/web-features) project.
