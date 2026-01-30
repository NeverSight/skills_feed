---
name: semantic-css
description: Skill for building beautiful, accessible web interfaces with semantic CSS. Provides design tokens for colors, typography, spacing, and effects with a 6-theme system. Use this skill when styling web applications with scalable, meaningful CSS that prioritizes accessibility and theming.
---

# Semantic CSS with New UI

Crafted with care. Styled for impact.

New UI is a modern, semantic UI framework for building beautiful, accessible sites and apps. It provides the core design foundations you need—including colors, typography, spacing, sizing, layouts, and effects.

Designed to grow with you from your first launch to millions of users, it is thoughtfully made for makers, small teams, and anyone who values functional, scalable, and timeless design.

## Core Principles

- **Built to scale** — Core building blocks for modern interfaces that grow with your needs.
- **Themes that adapt** — Customizable default themes with cold and warm variants to match your brand.
- **Framework agnostic** — Works seamlessly with React, Vue, Svelte, or any framework you choose.
- **Accessibility first** — WCAG-compliant with built-in keyboard navigation and focus management.

---

## Getting Started

### Install

```bash
npm i -D @new-ui/foundations
```

> **Note:** This command installs all New UI foundation packages, which include reset, colors, effects, spacings, and typography.

### CDN Quick Start

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@new-ui/foundations@latest/dist/index.css" />
```

### Import

```scss
@use '@new-ui/foundations'; // Use `@import` for CSS
```

### Set the Theme

Set the theme by adding the `data-new-ui-theme` attribute to your HTML wrapper element:

```html
<html data-new-ui-theme="light"></html>
```

| Available Themes | Value         |
|------------------|---------------|
| Light (Default)  | `light`       |
| Light warm       | `light--warm` |
| Light cold       | `light--cold` |
| Dark (Default)   | `dark`        |
| Dark warm        | `dark--warm`  |
| Dark cold        | `dark--cold`  |

---

## Naming Convention

All classes associated with the New UI are prefixed with a global namespace followed by a hyphen: `nu-`

In addition to a global namespace, we added prefixes to each class to make it more apparent what job that class is doing using BEM syntax:

| Prefix  | Purpose                            |
|---------|------------------------------------|
| `nu-c-` | UI components                      |
| `nu-l-` | Layout-related styles              |
| `nu-u-` | Utilities                          |
| `is-`   | State-based classes                |
| `has-`  | State-based classes                |
| `js-`   | Targeting JavaScript functionality |

---

## Design Tokens

### Colors

| Background                        | Role                          |
|-----------------------------------|-------------------------------|
| **`--background`**                | Default app background        |
| **`--background-secondary`**      | Secondary app background      |
| **`--background-hover`**          | Background hover              |
| **`--background-selected`**       | UI element background         |
| **`--background-selected-hover`** | UI element background hovered |
| **`--background-high-contrast`**  | High contrast background      |

| Border                 | Role                           |
|------------------------|--------------------------------|
| **`--border-muted`**   | Muted strokes and separators   |
| **`--border`**         | Default strokes and separators |
| **`--border-strong`**  | Strong strokes and separators  |
| **`--border-inked`**   | Inked strokes and separators   |
| **`--border-inverse`** | Inverse strokes and separators |
| **`--border-focus`**   | Focus outline                  |

| Button                  | Role                       |
|-------------------------|----------------------------|
| **`--button`**          | Primary button background  |
| **`--button-hover`**    | Primary button hover       |
| **`--button-active`**   | Primary button active      |
| **`--button-disabled`** | Disabled button background |

| Link                 | Role                         |
|----------------------|------------------------------|
| **`--link`**         | Primary link                 |
| **`--link-hover`**   | Hover state for primary link |
| **`--link-subtle`**  | Secondary link               |
| **`--link-visited`** | Link visited                 |

| Support                 | Role        |
|-------------------------|-------------|
| **`--support-error`**   | Error       |
| **`--support-warning`** | Warning     |
| **`--support-success`** | Success     |
| **`--support-info`**    | Information |

| Content                       | Role                      |
|-------------------------------|---------------------------|
| **`--content-primary`**       | Primary body copy         |
| **`--content-secondary`**     | Secondary text color      |
| **`--content-secondary-alt`** | Secondary text color alt  |
| **`--content-placeholder`**   | Placeholder text color    |
| **`--content-on-color`**      | Text on interactive color |
| **`--content-error`**         | Error message             |
| **`--content-success`**       | Success message           |
| **`--content-inked`**         | Inked text                |

### Effects

| Shadows               | Role                                          |
|-----------------------|-----------------------------------------------|
| **`--dialog-strong`** | Modals, sidebar overlays, toasts              |
| **`--dialog`**        | Dropdown, tooltip, popover                    |
| **`--content`**       | Content area, buttons, controls, cards, pills |
| **`--canvas`**        | Background                                    |
| **`--keyboard-key`**  | Keyboard key component                        |

| Focus                 | Role          |
|-----------------------|---------------|
| **`--focus-default`** | Default focus |
| **`--focus-accent`**  | Accent focus  |
| **`--focus-inverse`** | Focus inverse |

| Radius           | Blur           |
|------------------|----------------|
| `--radius-xs`    | `--blur-xs`    |
| `--radius-sm`    | `--blur-sm`    |
| `--radius-md`    | `--blur-md`    |
| `--radius-lg`    | `--blur-lg`    |
| `--radius-xl`    | `--blur-xl`    |
| `--radius-2xl`   | `--blur-2xl`   |
| `--radius-3xl`   | `--blur-3xl`   |
| `--radius-4xl`   |                |

| Perspective              | Value      |
|--------------------------|------------|
| `--perspective-dramatic` | 6.25rem    |
| `--perspective-near`     | 18.75rem   |
| `--perspective-normal`   | 31.25rem   |
| `--perspective-midrange` | 50rem      |
| `--perspective-distant`  | 75rem      |

| Other               | Value |
|---------------------|-------|
| `--aspect-video`    | 16/9  |
| `--keyboard-key`    | Keyboard key component shadow |

### Spacings

| Token                | Source         | Size (px/rem) |
|----------------------|----------------|---------------|
| **`--spacing-zero`** | `--spacing-00` | 0 / 0         |
| **`--spacing-xs`**   | `--spacing-02` | 4 / 0.25      |
| **`--spacing-s`**    | `--spacing-04` | 8 / 0.5       |
| **`--spacing-m`**    | `--spacing-05` | 12 / 0.75     |
| **`--spacing-l`**    | `--spacing-06` | 16 / 1        |
| **`--spacing-xl`**   | `--spacing-08` | 24 / 1.5      |
| **`--spacing-xxl`**  | `--spacing-09` | 32 / 2        |
| **`--spacing-xxxl`** | `--spacing-11` | 48 / 3        |

### Sizing

| Token                         | Source         | Size (px/rem) |
|-------------------------------|----------------|---------------|
| **`--size-xs`**               | `--spacing-06` | 16 / 1        |
| **`--size-s`**                | `--spacing-08` | 24 / 1.5      |
| **`--size-m`**                | `--spacing-09` | 32 / 2        |
| **`--controls-size-default`** | `--spacing-09` | 32 / 2        |
| **`--controls-size-small`**   | `--spacing-08` | 24 / 1.5      |

### Typography

| Heading (Desktop)          | Heading (Mobile)          | Role       |
|----------------------------|---------------------------|------------|
| **`--desktop-heading-01`** | **`--mobile-heading-01`** | Heading 01 |
| **`--desktop-heading-02`** | **`--mobile-heading-02`** | Heading 02 |
| **`--desktop-heading-03`** | **`--mobile-heading-03`** | Heading 03 |
| **`--desktop-heading-04`** | **`--mobile-heading-04`** | Heading 04 |
| **`--desktop-heading-05`** | **`--mobile-heading-05`** | Heading 05 |
| **`--desktop-heading-06`** | **`--mobile-heading-06`** | Heading 06 |

| Body (Desktop)          | Body (Mobile)          | Role       |
|-------------------------|------------------------|------------|
| **`--desktop-body-xl`** | **`--mobile-body-xl`** | Body large |
| **`--desktop-body`**    | **`--mobile-body`**    | Body copy  |
| **`--desktop-body-sm`** | **`--mobile-body-sm`** | Body small |

| Utility (Desktop)           | Utility (Mobile)           | Role        |
|-----------------------------|----------------------------|-------------|
| **`--desktop-caption`**     | **`--mobile-caption`**     | Caption     |
| **`--desktop-helper-text`** | **`--mobile-helper-text`** | Helper text |
| **`--desktop-code`**        | **`--mobile-code`**        | Code        |

> **Note:** To set line height, simply add the prefix `--lh` to the font size variables. For instance, `--desktop-body-xl` becomes `--lh-desktop-body-xl`.

---

## Utility Classes

### Margin & Padding

Pattern: `nu-u-{property}-{size}`

| Property | Description      |
|----------|------------------|
| `m`      | margin           |
| `mt`     | margin-top       |
| `mb`     | margin-bottom    |
| `ms`     | margin-left      |
| `me`     | margin-right     |
| `mx`     | margin-inline    |
| `my`     | margin-block     |
| `p`      | padding          |
| `pt`     | padding-top      |
| `pb`     | padding-bottom   |
| `ps`     | padding-left     |
| `pe`     | padding-right    |
| `px`     | padding-inline   |
| `py`     | padding-block    |

Sizes: `zero`, `xs`, `s`, `m`, `l`, `xl`, `xxl`, `xxxl`

```html
<div class="nu-u-p-l">Padding large (16px)</div>
<div class="nu-u-mt-xl nu-u-mb-m">Margin top XL, bottom M</div>
<div class="nu-u-mx-auto">Centered horizontally</div>
```

### Spacer Components

```html
<div class="nu-c-spacer-xl"></div> <!-- 24px vertical space -->
```

### Typography Classes

```html
<h1 class="nu-c-h1">Heading 1</h1>
<h2 class="nu-c-h2">Heading 2</h2>
<p class="nu-c-fs-lead">Lead paragraph</p>
<p class="nu-c-fs-normal">Normal body text</p>
<p class="nu-c-fs-small">Small text</p>
<span class="nu-c-caption">CAPTION TEXT</span>
<span class="nu-c-helper-text">Helper text</span>
<code class="nu-c-code">Code text</code>
```

**Font weights:** `nu-u-fw-bold`, `nu-u-fw-semi-bold`, `nu-u-fw-normal`

**Text transform:** `nu-u-text--uppercase`, `nu-u-text--lowercase`, `nu-u-text--capitalize`

**Text align:** `nu-u-text--left`, `nu-u-text--right`, `nu-u-text--center`, `nu-u-text--justify`

**Font families:** `nu-u-serif`, `nu-u-sans-serif`, `nu-u-code`

### Background Classes

```html
<div class="nu-u-bg">Default background</div>
<div class="nu-u-bg-secondary">Secondary background</div>
<div class="nu-u-bg-selected">Selected state</div>
<div class="nu-u-bg-black">Black background</div>
<div class="nu-u-bg-white">White background</div>
```

### Text Color Classes

```html
<p class="nu-u-text--primary">Primary text</p>
<p class="nu-u-text--secondary">Secondary text</p>
<p class="nu-u-text--error">Error message</p>
<p class="nu-u-text--success">Success message</p>
<a class="nu-u-link">Link text</a>
```

### Border Classes

```html
<div class="nu-u-b">Default border color</div>
<div class="nu-u-b--muted">Muted border</div>
<div class="nu-u-b--strong">Strong border</div>
<div class="nu-u-b--focus">Focus border</div>
```

### Shadow Classes

```html
<div class="sh-dialog--strong">Modal shadow</div>
<div class="sh-dialog">Dropdown/tooltip shadow</div>
<div class="sh-content">Card/button shadow</div>
<div class="sh-canvas">Background shadow</div>
<div class="sh-default">Default focus ring</div>
<div class="sh-accent">Accent focus ring</div>
<div class="sh-inverse">Inverse focus ring</div>
```

---

## Usage Examples

### Themed Card Component

```html
<html data-new-ui-theme="light">
<body class="nu-u-bg">
  <article class="nu-u-p-xl nu-u-bg-secondary sh-content" 
           style="border-radius: var(--radius-lg);">
    <h2 class="nu-c-h3 nu-u-text--primary nu-u-mb-m">Card Title</h2>
    <p class="nu-c-fs-normal nu-u-text--secondary">
      Card description using semantic color tokens.
    </p>
    <div class="nu-c-spacer-l"></div>
    <button style="background: var(--button); color: var(--content-on-color); 
                   padding: var(--spacing-s) var(--spacing-l); 
                   border-radius: var(--radius-md);">
      Action
    </button>
  </article>
</body>
</html>
```

### Dark Theme Toggle

```javascript
function toggleTheme() {
  const html = document.documentElement;
  const current = html.dataset.newUiTheme;
  html.dataset.newUiTheme = current === 'light' ? 'dark' : 'light';
}
```

---

## Best Practices

### Using New UI Tokens

1. **Use semantic tokens** — Prefer `--content-primary` over `--grey10` for automatic theme support.
2. **Leverage utility classes** — Use `nu-u-*` classes for consistent spacing and typography.
3. **Set themes at root** — Apply `data-new-ui-theme` on `<html>` for full page theming.
4. **Responsive typography** — Heading and body classes automatically scale for mobile.
5. **Accessible colors** — OKLCH color system ensures perceptual consistency across themes.

### Focus States

- Interactive elements need visible focus: use `--focus-default`, `--focus-accent`, or `--border-focus`
- Apply focus with `box-shadow: var(--focus-default)` or the `.sh-default` utility class
- Never use `outline: none` without providing a focus replacement
- Use `:focus-visible` over `:focus` (avoids focus ring on click)
- Group focus with `:focus-within` for compound controls

### Forms

- Inputs need `autocomplete` and meaningful `name` attributes
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`
- Labels must be clickable (`for` attribute or wrapping control)
- Errors displayed inline next to fields; focus first error on submit
- Placeholders should show example patterns and end with `…`

### Animation

- Honor `prefers-reduced-motion` (provide reduced variant or disable)
- Animate `transform` and `opacity` only (compositor-friendly)
- Never use `transition: all`—list properties explicitly
- Use `--default-transition-duration` and `--default-transition-timing-function`

### Typography

- Use `…` not `...` (ellipsis character)
- Use curly quotes `"` `"` not straight `"`
- Non-breaking spaces for units: `10 MB`, `⌘ K`
- Loading states end with `…`: `"Loading…"`, `"Saving…"`
- Use `font-variant-numeric: tabular-nums` for number columns
- Use `text-wrap: balance` on headings (prevents widows)

### Images

- Always provide explicit `width` and `height` (prevents CLS)
- Below-fold images: `loading="lazy"`
- Above-fold critical images: `fetchpriority="high"`

### Dark Mode & Theming

- Set theme using `data-new-ui-theme` attribute on `<html>`
- Use `color-scheme: dark` on `<html>` for dark themes (fixes native scrollbar, inputs)
- `<meta name="theme-color">` should match `--background` token
- Native `<select>`: use `--background` and `--content-primary` for consistent theming
- Always use semantic tokens (`--content-primary`, `--background`) for automatic theme adaptation

### Content Handling

- Text containers must handle long content: `truncate`, `line-clamp`, or `overflow-wrap: break-word`
- Flex children need `min-width: 0` to allow text truncation
- Always handle empty states—don't render broken UI

### Accessibility

- Form inputs must have associated labels
- Icon buttons need `aria-label`
- Never disable zoom: avoid `user-scalable=no` or `maximum-scale=1`
- Use semantic HTML elements (`<button>`, `<a>`, `<nav>`, `<main>`, `<article>`)

---

## Anti-Patterns to Avoid

- `outline: none` without focus-visible replacement
- `transition: all` (list properties explicitly)
- `<div>` or `<span>` with click handlers (use `<button>`)
- Images without dimensions
- Form inputs without labels
- Icon buttons without `aria-label`
- Hardcoded date/number formats (use `Intl.*`)
- Inline `onClick` navigation without `<a>` or `<Link>`

---

## Learn More

- [New UI Documentation](https://new-ui.com/docs)
- [Colors Guide](https://new-ui.com/docs/foundations/colors)
- [Typography Guide](https://new-ui.com/docs/foundations/typography)
- [Spacings Guide](https://new-ui.com/docs/foundations/spacings)
- [Effects Guide](https://new-ui.com/docs/foundations/effects)

