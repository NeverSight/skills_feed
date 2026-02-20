---
name: daisyui
description: "CSS component library for Tailwind CSS 4 providing pre-built UI components with semantic class names. Use when building web interfaces with HTML/Tailwind that need: (1) Rapid UI development with consistent styling, (2) Accessible component patterns (buttons, forms, modals, etc.), (3) Theme-aware color systems that work across light/dark modes, (4) Responsive layouts with Tailwind utilities. Works with daisyUI v5+ which requires Tailwind CSS v4+."
---

# daisyUI 5

## Overview

daisyUI 5 is a CSS component library for Tailwind CSS 4 that provides class names for common UI components. Use it to rapidly build consistent, accessible, and theme-aware web interfaces.

## Installation

daisyUI 5 requires Tailwind CSS 4. The `tailwind.config.js` file is deprecated in Tailwind CSS v4.

Install via npm:

```bash
npm i -D daisyui@latest
```

Add to your CSS file:

```css
@import "tailwindcss";
@plugin "daisyui";
```

Or use CDN:

```html
<link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

## Configuration

### Basic Config

No config needed - use defaults:

```css
@plugin "daisyui";
```

### Light Theme Only

```css
@plugin "daisyui" {
  themes: light --default;
}
```

### With Dark Mode

```css
@plugin "daisyui" {
  themes: light --default, dark --prefersdark;
  root: ":root";
  include: ;
  exclude: ;
  prefix: ;
  logs: true;
}
```

### All Built-in Themes

```css
@plugin "daisyui" {
  themes: light, dark, cupcake, bumblebee --default, emerald, corporate, synthwave --prefersdark, retro, cyberpunk, valentine, halloween, garden, forest, aqua, lofi, pastel, fantasy, wireframe, black, luxury, dracula, cmyk, autumn, business, acid, lemonade, night, coffee, winter, dim, nord, sunset, caramellatte, abyss, silk;
  root: ":root";
  include: ;
  exclude: rootscrollgutter, checkbox;
  prefix: daisy-;
  logs: false;
}
```

Set theme on HTML element:

```html
<html data-theme="cupcake">
```

### Custom Theme

Use the theme generator at https://daisyui.com/theme-generator/ or create manually:

```css
@plugin "daisyui/theme" {
  name: "mytheme";
  default: true;
  prefersdark: false;
  color-scheme: light;

  --color-base-100: oklch(98% 0.02 240);
  --color-base-200: oklch(95% 0.03 240);
  --color-base-300: oklch(92% 0.04 240);
  --color-base-content: oklch(20% 0.05 240);
  --color-primary: oklch(55% 0.3 240);
  --color-primary-content: oklch(98% 0.01 240);
  --color-secondary: oklch(70% 0.25 200);
  --color-secondary-content: oklch(98% 0.01 200);
  --color-accent: oklch(65% 0.25 160);
  --color-accent-content: oklch(98% 0.01 160);
  --color-neutral: oklch(50% 0.05 240);
  --color-neutral-content: oklch(98% 0.01 240);
  --color-info: oklch(70% 0.2 220);
  --color-info-content: oklch(98% 0.01 220);
  --color-success: oklch(65% 0.25 140);
  --color-success-content: oklch(98% 0.01 140);
  --color-warning: oklch(80% 0.25 80);
  --color-warning-content: oklch(20% 0.05 80);
  --color-error: oklch(65% 0.3 30);
  --color-error-content: oklch(98% 0.01 30);

  --radius-selector: 1rem;
  --radius-field: 0.25rem;
  --radius-box: 0.5rem;
  --size-selector: 0.25rem;
  --size-field: 0.25rem;
  --border: 1px;
  --depth: 1;
  --noise: 0;
}
```

## Usage Rules

1. Add daisyUI class names to HTML elements (component + part + modifier classes)
2. Customize with Tailwind utilities (e.g., `btn px-10`)
3. Use `!` suffix for specificity issues as last resort (e.g., `bg-red-500!`)
4. If component doesn't exist, build with Tailwind utilities
5. Make layouts responsive with Tailwind prefixes (e.g., `sm:card-horizontal`)
6. Only use daisyUI class names or Tailwind utility classes
7. Ideally no custom CSS needed

### Additional Guidelines

- Use https://picsum.photos/{width}/{height} for placeholder images
- Don't add custom fonts unless necessary
- Don't add `bg-base-100 text-base-content` to body unless necessary
- For design decisions, follow Refactoring UI book best practices

## Class Name Categories

daisyUI class names fall into these categories (reference only, not used in code):

- `component` - Required component class (e.g., `btn`, `card`)
- `part` - Child part of component (e.g., `card-title`, `card-body`)
- `style` - Specific style (e.g., `btn-outline`, `alert-soft`)
- `behavior` - Changes behavior (e.g., `btn-active`, `btn-disabled`)
- `color` - Sets color (e.g., `btn-primary`, `alert-error`)
- `size` - Sets size (e.g., `btn-sm`, `input-lg`)
- `placement` - Sets placement (e.g., `dropdown-top`, `modal-middle`)
- `direction` - Sets direction (e.g., `tabs-horizontal`, `carousel-vertical`)
- `modifier` - Modifies component (e.g., `btn-wide`, `card-side`)
- `variant` - Utility prefixes with syntax `variant:utility-class` (e.g., `is-drawer-open:w-64`)

## Color System

### Semantic Color Names

- `primary` / `primary-content` - Main brand color
- `secondary` / `secondary-content` - Secondary brand color
- `accent` / `accent-content` - Accent color
- `neutral` / `neutral-content` - Neutral UI elements
- `base-100` - Base surface color (blank backgrounds)
- `base-200` - Darker shade for elevations
- `base-300` - Even darker shade for elevations
- `base-content` - Foreground content color
- `info` / `info-content` - Informational messages
- `success` / `success-content` - Success states
- `warning` / `warning-content` - Warning states
- `error` / `error-content` - Error states

### Color Rules

- daisyUI colors are theme-aware and change with theme
- No need for `dark:` prefix with daisyUI colors
- Tailwind colors like `red-500` stay same on all themes
- Avoid Tailwind text colors like `text-gray-800` - unreadable on dark themes
- `*-content` colors have good contrast on their associated colors
- Use `base-*` colors for majority of page
- Use `primary` color for important elements

## Common Components

### Button

```html
<button class="btn btn-primary">Click me</button>
<button class="btn btn-outline btn-secondary">Cancel</button>
<button class="btn btn-sm">Small</button>
<button class="btn btn-lg">Large</button>
```

### Input

```html
<input type="text" placeholder="Type here" class="input input-bordered" />
```

### Card

```html
<div class="card bg-base-100 shadow-sm">
  <figure><img src="https://picsum.photos/400/250" alt="Card image" /></figure>
  <div class="card-body">
    <h2 class="card-title">Title</h2>
    <p>Content</p>
    <div class="card-actions">
      <button class="btn btn-primary">Action</button>
    </div>
  </div>
</div>
```

### Modal

```html
<button onclick="my_modal.showModal()">Open</button>
<dialog id="my_modal" class="modal">
  <div class="modal-box">
    <h3 class="font-bold">Title</h3>
    <p>Content</p>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn">Close</button>
      </form>
    </div>
  </div>
</dialog>
```

### Alert

```html
<div role="alert" class="alert alert-error">
  <svg class="w-6 h-6" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
  <span>Error message</span>
</div>
```

### Navbar

```html
<div class="navbar bg-base-200">
  <div class="navbar-start">Logo</div>
  <div class="navbar-center">Title</div>
  <div class="navbar-end">Menu</div>
</div>
```

### Drawer

```html
<div class="drawer lg:drawer-open">
  <input id="my-drawer" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content">
    <label for="my-drawer" class="btn drawer-button lg:hidden">Open drawer</label>
    <!-- Page content -->
  </div>
  <div class="drawer-side">
    <label for="my-drawer" class="drawer-overlay"></label>
    <ul class="menu bg-base-200 min-h-full w-80 p-4">
      <li><a>Item 1</a></li>
      <li><a>Item 2</a></li>
    </ul>
  </div>
</div>
```

## Resources

### references/

Component documentation and detailed examples:

- **components.md** - Complete component reference with all class names, syntax, and usage rules for every daisyUI component (accordion, alert, avatar, badge, breadcrumbs, button, calendar, card, carousel, chat, checkbox, collapse, countdown, diff, divider, dock, drawer, dropdown, fab, fieldset, file-input, filter, footer, hero, hover-3d, hover-gallery, indicator, input, join, kbd, label, link, list, loading, mask, menu, mockup-browser, mockup-code, mockup-phone, mockup-window, modal, navbar, pagination, progress, radial-progress, radio, range, rating, select, skeleton, stack, stat, status, steps, swap, tab, table, text-rotate, textarea, theme-controller, timeline, toast, toggle, validator)

When working with a specific component, read components.md and search for that component's section.
