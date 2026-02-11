---
name: css-first
description: CSS-first expert guidance with live MDN Baseline and feature data. Use when asked about CSS implementations, modern CSS features, browser support, Baseline status, or when listing newly available web platform features.
license: MIT
---

# CSS First Agent Skill

An intelligent AI agent skill for providing context-aware, modern CSS-first solutions with semantic analysis and framework detection.

## Description

This skill transforms any AI agent into a CSS-first expert that enforces zero-JavaScript solutions using cutting-edge CSS features (2021-2026). The agent analyzes user intent, detects project context, and provides intelligently ranked CSS suggestions with implementation guidance.

**Core Capabilities**:

- **Semantic Intent Recognition**: Understands layout, animation, spacing, responsive, visual, interaction, stacking, and typography intents
- **Framework Detection**: Automatically detects React, Vue, Angular, Svelte, Tailwind, Bootstrap, etc.
- **Logical-First Approach**: Prioritizes writing-mode aware properties for internationalization
- **MDN Integration**: Pulls live browser support data and baseline status
- **Intelligent Ranking**: Scores suggestions by intent match, browser support, and framework compatibility

## When to Use This Skill

Use this skill when:

- User asks for UI implementation solutions
- User needs to center elements, create layouts, add animations
- User wants responsive design patterns
- User asks about CSS properties or browser support
- User needs modern CSS alternatives to JavaScript solutions

## Live MDN Fetch Workflow

Use the live fetch workflow defined in `references/live-mdn-fetch.md` whenever Baseline status, newly available features, or current MDN content is requested.

## Rules & Guidelines

All behavior rules are documented in `references/rules/`:

| Rule                     | File                                                                                                     | Summary                                        |
| ------------------------ | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| CSS-Only Enforcement     | [`references/rules/css-only-enforcement.md`](references/rules/css-only-enforcement.md)                   | Always prioritize CSS over JavaScript          |
| Logical Properties First | [`references/rules/logical-properties-first.md`](references/rules/logical-properties-first.md)           | Use `inline-size` over `width`, etc.           |
| Modern CSS Features      | [`references/rules/modern-css-features.md`](references/rules/modern-css-features.md)                     | Prioritize 2021-2025 features with baseline    |
| Semantic Intent Analysis | [`references/rules/semantic-intent-analysis.md`](references/rules/semantic-intent-analysis.md)           | Detect user intent before suggesting solutions |
| Framework Awareness      | [`references/rules/framework-awareness.md`](references/rules/framework-awareness.md)                     | Auto-detect and adapt to project frameworks    |
| Browser Support          | [`references/rules/browser-support-consideration.md`](references/rules/browser-support-consideration.md) | Always provide baseline status indicators      |
| Progressive Enhancement  | [`references/rules/progressive-enhancement.md`](references/rules/progressive-enhancement.md)             | Core functionality first, enhancements on top  |
| Browser Verification     | [`references/rules/browser-verification.md`](references/rules/browser-verification.md)                   | Use MCP servers / browser hooks to verify CSS  |

## CSS Demos

Production-ready CSS examples organized by category. See [`css-demos/INDEX.md`](css-demos/INDEX.md) for the full catalog with MDN links, baseline status, and browser support percentages.

## Browser Support Levels

- **🟢 Widely Available** (95%+): Safe for production use
- **🔵 Newly Available** (85-94%): Recently stable, verify target browsers
- **🟡 Limited Availability** (70-84%): Use with progressive enhancement
- **🟣 Experimental** (<70%): Cutting-edge features, use cautiously

## Quick Reference

| User Intent              | CSS Solution                    | Demo File                                              |
| ------------------------ | ------------------------------- | ------------------------------------------------------ |
| Center element           | Flexbox / Grid                  | `css-demos/layout/centering-logical.css`               |
| Spacing                  | Logical Properties              | `css-demos/layout/logical-spacing.css`                 |
| Aligned nested grids     | Subgrid                         | `css-demos/layout/subgrid.css`                         |
| Parent selection         | `:has()`                        | `css-demos/layout/has-selector.css`                    |
| Component styles         | CSS Nesting                     | `css-demos/layout/css-nesting.css`                     |
| Masonry layout           | Grid Lanes                      | `css-demos/layout/grid-lanes-masonry.css`              |
| z-index issues           | `isolation: isolate`            | `css-demos/layout/isolation-stacking.css`              |
| Fill width with margins  | `stretch`                       | `css-demos/layout/stretch-keyword.css`                 |
| Responsive layout        | Media queries (range syntax)    | `css-demos/responsive/media-queries.css`               |
| Feature detection        | `@supports`                     | `css-demos/responsive/supports-rule.css`               |
| Full-height sections     | Dynamic viewport units          | `css-demos/responsive/viewport-units.css`              |
| Container responsive     | Container size queries          | `css-demos/container/size-queries.css`                 |
| Component theming        | Container style queries         | `css-demos/container/style-queries.css`                |
| Sticky detection         | Scroll state queries            | `css-demos/container/scroll-state-queries.css`         |
| Tooltip arrow flip       | Anchored container queries      | `css-demos/container/anchored-queries.css`             |
| Page transitions         | View Transitions (+ nested)     | `css-demos/animation/view-transitions.css`             |
| Scroll effects           | Scroll-driven animations        | `css-demos/animation/scroll-driven.css`                |
| Scroll reveals           | Scroll-triggered animations     | `css-demos/animation/scroll-triggered.css`             |
| Entry/exit animation     | `@starting-style`               | `css-demos/animation/starting-style.css`               |
| Dark mode                | `light-dark()`                  | `css-demos/theming/light-dark-function.css`            |
| Tooltips                 | Anchor Positioning              | `css-demos/positioning/anchor-positioning.css`         |
| Carousel / Slider        | CSS Carousel                    | `css-demos/interaction/css-carousel.css`               |
| Tabs / Scroll spy        | CSS Carousel                    | `css-demos/interaction/css-carousel.css`               |
| Flip card / 3D tile      | `backface-visibility`           | `css-demos/interaction/flip-card.css`                  |
| 3D scenes / Cubes        | `perspective` + `preserve-3d`   | `css-demos/interaction/perspective-3d.css`              |
| Popovers / Dropdowns     | Popover API                     | `css-demos/interaction/popover.css`                    |
| Hover tooltips (no JS)   | Interest Invokers               | `css-demos/interaction/interest-invokers.css`          |
| Touch vs pointer         | Hover media queries             | `css-demos/interaction/hover-media-queries.css`        |
| Scroll chaining          | `overscroll-behavior`           | `css-demos/interaction/overscroll-behavior.css`        |
| Fixed nav anchor offset  | `scroll-margin` / `scroll-padding` | `css-demos/interaction/scroll-margin-padding.css`  |
| Highlight anchor target  | `:target` / `:focus-within`     | `css-demos/interaction/target-focus-within.css`        |
| Form validation          | `:user-valid`/`:user-invalid`   | `css-demos/visual/form-validation.css`                 |
| Color variations         | `color-mix()`                   | `css-demos/visual/color-mix.css`                       |
| Color conversion         | Relative color syntax           | `css-demos/visual/relative-colors.css`                 |
| Glassmorphism            | `backdrop-filter`               | `css-demos/visual/backdrop-filter.css`                 |
| Adaptive text on bg      | `mix-blend-mode`                | `css-demos/visual/mix-blend-mode.css`                  |
| Modern shapes            | `corner-shape`                  | `css-demos/visual/corner-shape.css`                    |
| Responsive clipping      | `clip-path: shape()`            | `css-demos/visual/clip-path-shape.css`                 |
| Gap separators           | `column-rule` / `row-rule`      | `css-demos/visual/gap-decorations.css`                 |
| Optical text centering   | `text-box-trim`                 | `css-demos/visual/text-box-trim.css`                   |
| Focus outlines clipped   | `overflow: clip` + clip-margin  | `css-demos/visual/overflow-clip-margin.css`            |
| Conditional values       | `if()`                          | `css-demos/functions/css-if-function.css`              |
| Reusable CSS logic       | `@function`                     | `css-demos/functions/custom-functions.css`             |
| Data-driven styles       | Advanced `attr()`               | `css-demos/functions/advanced-attr.css`                |
| Auto contrast text       | `contrast-color()`              | `css-demos/functions/contrast-color.css`               |
| Circular layout          | `sin()` / `cos()`               | `css-demos/functions/trigonometric-functions.css`       |
| Staggered animations     | `sibling-index()` / `sibling-count()` | `css-demos/functions/sibling-functions.css`       |
| Cascade control          | `@layer`                        | `css-demos/specificity/cascade-layers.css`             |
| Scoped styles            | `@scope`                        | `css-demos/specificity/scope-rule.css`                 |
| Custom select styling    | `appearance: base-select`       | `css-demos/native-customization/customizable-select.css` |
| Reduced motion           | `prefers-reduced-motion`        | `css-demos/accessibility/prefers-reduced-motion.css`     |
| High contrast            | `prefers-contrast`              | `css-demos/accessibility/prefers-reduced-motion.css`     |
| Forced colors (Win HC)   | `forced-colors`                 | `css-demos/accessibility/prefers-reduced-motion.css`     |

## See Also

- **MDN Web Docs**: https://developer.mozilla.org/en-US/docs/Web/CSS
- **CSS Baseline**: https://web.dev/baseline/
