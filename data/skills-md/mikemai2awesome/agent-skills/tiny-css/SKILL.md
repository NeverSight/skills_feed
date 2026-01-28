---
name: tiny-css
description: Write minimal, efficient CSS by leveraging browser defaults and modern CSS features. Use when writing CSS, creating stylesheets, setting up base styles, or reviewing CSS for unnecessary declarations.
license: MIT
metadata:
  author: mikemai2awesome
  version: "1.0"
---

# Tiny CSS

Write as little CSS as possible. Leverage browser defaults and modern CSS features instead of overriding everything.

## Core Principles

1. **Trust the browser** — Don't reset what already works
2. **Use modern features** — Let CSS handle what JavaScript used to do
3. **Respect user preferences** — Honor system settings for motion, contrast, and color schemes
4. **Write resilient styles** — Use logical properties for internationalization

## Guidelines

### Don't Declare Base Font Size

Let the browser handle the base font size, which defaults to 100% (typically 16px). Users can adjust this in their browser settings for accessibility.

```css
/* Don't do this */
:root {
  font-size: 16px;
}
html {
  font-size: 100%;
}
body {
  font-size: 1rem;
}

/* Do nothing — the browser already handles this */
```

### Don't Declare Default Colors

Skip declaring color and background-color on the root. Browser defaults work and respect user preferences.

```css
/* Don't do this */
body {
  color: #000;
  background-color: #fff;
}

/* Do nothing — browser defaults are fine */
```

### Enable Light and Dark Modes

Use `color-scheme` to automatically support light and dark modes based on user system preferences.

```css
:root {
  color-scheme: light dark;
}
```

### Customize Interactive Element Colors

Use `accent-color` to change the color of checkboxes, radio buttons, range sliders, and progress bars.

```css
:root {
  accent-color: #0066cc; /* Replace with desired color */
}
```

### Match SVG Icons with Text Color

Make SVG icons inherit the current text color automatically.

```css
:where(svg) {
  fill: currentColor;
}
```

### Support Forced Colors Mode

Ensure buttons remain visible in Windows High Contrast Mode by adding explicit borders.

```css
@media (forced-colors: active) {
  :where(button) {
    border: 1px solid;
  }
}
```

### Handle Reduced Transparency

Only apply translucent or glassy effects when the user hasn't requested reduced transparency.

```css
@media (prefers-reduced-transparency: no-preference) {
  .glass-panel {
    background: oklch(100% 0 0 / 0.8);
    backdrop-filter: blur(1rem);
  }
}
```

### Use System Font with Better Glyphs

Enable distinct characters for uppercase I, lowercase l, and slashed zero in San Francisco font.

```css
:root {
  font-family: system-ui;
  font-feature-settings: "ss06";
}
```

### Improve Text Wrapping

Prevent widows and improve line breaks.

```css
:where(h1, h2, h3, h4, h5, h6) {
  text-wrap: balance;
}

:where(p) {
  text-wrap: pretty;
}
```

### Use Logical Properties

Write CSS that works across all languages and writing directions. Use logical properties instead of physical ones.

```css
/* Don't do this */
.card {
  margin-left: 1rem;
  margin-right: 1rem;
  padding-top: 2rem;
  padding-bottom: 2rem;
  width: 20rem;
  height: auto;
}

/* Do this */
.card {
  margin-inline: 1rem;
  padding-block: 2rem;
  inline-size: 20rem;
  block-size: auto;
}
```

### Make Media Embeds Responsive

Ensure images, videos, and iframes scale proportionally.

```css
:where(img, svg, video, iframe) {
  max-inline-size: 100%;
  block-size: auto;
}
```

### Add Pointer Cursors to Interactive Elements

Provide a baseline hover affordance for all clickable elements.

```css
:where(input:is([type="checkbox"], [type="radio"]), select, label, button) {
  cursor: pointer;
}
```

### Create Consistent Focus Outlines

Ensure all interactive elements have visible, high-contrast focus indicators.

```css
*:focus-visible {
  outline: 2px solid;
  outline-offset: 2px;
}
```

### Respect Reduced Motion Preferences

Only animate elements when the user hasn't requested reduced motion.

```css
@media (prefers-reduced-motion: no-preference) {
  .animated-element {
    transition: transform 0.3s ease;
  }
}
```

### Enable Smooth Scrolling Conditionally

Apply smooth scrolling only when the user hasn't requested reduced motion.

```css
@media (prefers-reduced-motion: no-preference) {
  :root {
    scroll-behavior: smooth;
  }
}
```

### Use ARIA Attributes as Styling Hooks

Style components based on their accessibility state rather than creating modifier classes.

```css
/* Don't do this */
.accordion-header--collapsed {
  /* collapsed styles */
}
.accordion-header--expanded {
  /* expanded styles */
}

/* Do this */
[aria-expanded="false"] {
  /* collapsed styles */
}
[aria-expanded="true"] {
  /* expanded styles */
}
```

More examples:

```css
/* Navigation states */
[aria-current="page"] {
  font-weight: bold;
}

/* Disabled states */
[aria-disabled="true"] {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Selected states */
[aria-selected="true"] {
  background-color: highlight;
}

/* Invalid form fields */
[aria-invalid="true"] {
  border-color: red;
}
```

## Minimal Base Stylesheet

Here's a complete minimal base that incorporates all guidelines:

```css
:root {
  color-scheme: light dark;
  accent-color: #0066cc;
  font-family: system-ui;
  font-feature-settings: "ss06";
}

*:focus-visible {
  outline: 2px solid;
  outline-offset: 2px;
}

:where(h1, h2, h3, h4, h5, h6) {
  text-wrap: balance;
}

:where(p) {
  text-wrap: pretty;
}

:where(img, svg, video, iframe) {
  max-inline-size: 100%;
  block-size: auto;
}

:where(svg) {
  fill: currentColor;
}

:where(input:is([type="checkbox"], [type="radio"]), select, label, button) {
  cursor: pointer;
}

@media (forced-colors: active) {
  :where(button) {
    border: 1px solid;
  }
}

@media (prefers-reduced-motion: no-preference) {
  :root {
    scroll-behavior: smooth;
  }
}
```
