---
name: bootstrap-icons
description: This skill should be used when the user asks about Bootstrap Icons, Bootstrap icon library, how to install Bootstrap Icons, how to use Bootstrap Icons, Bootstrap icon fonts, Bootstrap icon SVGs, Bootstrap icon sprites, Bootstrap Icons CDN, Bootstrap Icons npm, Bootstrap Icons Composer, PHP Bootstrap Icons, Laravel icons, external image icons, img tag icons, CSS background icons, CSS mask icons, how to style Bootstrap icons, Bootstrap icon sizing, Bootstrap icon colors, Bootstrap icon accessibility, or needs help using icons in Bootstrap projects.
---

# Bootstrap Icons

Bootstrap Icons is an official open-source icon library with over 2,000 icons designed to work with Bootstrap components and documentation.

**Current Version**: 1.13.x (check <https://icons.getbootstrap.com> for latest)

## Installation Methods

### CDN (Quickest)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css" integrity="sha384-CK2SzKma4jA5H/MXDUU7i1TqZlCFaD4T01vtyDFvPlD97JQyS+IsSh1nI2EFbpyk" crossorigin="anonymous">
```

### npm

```bash
npm install bootstrap-icons
```

Then import:
```scss
// In SCSS
@import "bootstrap-icons/font/bootstrap-icons.css";
```

```javascript
// In JavaScript
import 'bootstrap-icons/font/bootstrap-icons.css';
```

### Download

Download from <https://icons.getbootstrap.com> and include files locally.

### Composer (PHP)

For PHP projects using Composer:

```bash
composer require twbs/bootstrap-icons
```

Then reference icons from the vendor directory:

```php
// Laravel Blade example
<img src="{{ asset('vendor/twbs/bootstrap-icons/icons/heart.svg') }}" alt="Heart">

// Symfony Twig example
<img src="{{ asset('bundles/bootstrap-icons/icons/heart.svg') }}" alt="Heart">
```

## Usage Methods

### Icon Fonts (Recommended for Most Cases)

Icon fonts are the simplest method for most projects:

- **Easy syntax**: Just add `<i class="bi bi-*"></i>`
- **Automatic sizing**: Icons scale with surrounding text
- **Color inheritance**: Icons use the parent's `color` property
- **Single dependency**: One CSS file provides all icons

For advanced use cases (color gradients, animation, or offline/email), consider SVG methods instead.

```html
<!-- Basic usage -->
<i class="bi bi-alarm"></i>
<i class="bi bi-heart-fill"></i>
<i class="bi bi-check-circle"></i>

<!-- Sizing with font-size -->
<i class="bi bi-alarm" style="font-size: 2rem;"></i>

<!-- Sizing with Bootstrap utilities -->
<i class="bi bi-alarm fs-1"></i>
<i class="bi bi-alarm fs-3"></i>

<!-- Coloring -->
<i class="bi bi-heart-fill text-danger"></i>
<i class="bi bi-check-circle text-success"></i>
<i class="bi bi-star-fill text-warning"></i>
```

### Embedded SVG

Copy SVG code directly from the website:

```html
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
  <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
</svg>
```

**Benefits of embedded SVG:**
- No external dependencies
- Full CSS control
- Can be manipulated with JavaScript
- `currentColor` inherits text color

### SVG Sprite

Include sprite once, reference icons:

```html
<!-- Include sprite (in body or inline) -->
<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
  <symbol id="heart" viewBox="0 0 16 16">
    <path d="m8 2.748-.717-.737C5.6.281..."/>
  </symbol>
  <symbol id="star" viewBox="0 0 16 16">
    <path d="M2.866 14.85c-.078.444..."/>
  </symbol>
</svg>

<!-- Use icons -->
<svg class="bi" width="32" height="32" fill="currentColor">
  <use xlink:href="#heart"/>
</svg>
```

Or reference external sprite file:

```html
<svg class="bi" width="32" height="32" fill="currentColor">
  <use xlink:href="bootstrap-icons.svg#heart"/>
</svg>
```

### External Image

Reference icon SVG files directly via `<img>` element:

```html
<!-- Via CDN -->
<img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/icons/heart.svg" alt="Heart" width="32" height="32">

<!-- Local file -->
<img src="/assets/icons/heart.svg" alt="Heart" width="32" height="32">
```

**When to use:**

- Email templates (no CSS/font dependencies)
- Simple static pages
- Content management systems
- When caching individual icons

**Trade-offs:**

- Cannot inherit text color (use CSS method for that)
- Each icon is a separate HTTP request (unless using HTTP/2)
- Requires explicit width/height attributes

### CSS Method

Include icons via CSS background-image or mask:

```css
/* Background-image approach (fixed color) */
.icon-heart {
  display: inline-block;
  width: 1em;
  height: 1em;
  background-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/icons/heart.svg");
  background-size: contain;
  background-repeat: no-repeat;
}

/* Mask approach (inherits currentColor) */
.icon-heart-mask {
  display: inline-block;
  width: 1em;
  height: 1em;
  background-color: currentColor;
  mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/icons/heart.svg");
  mask-size: contain;
  mask-repeat: no-repeat;
  -webkit-mask-image: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/icons/heart.svg");
  -webkit-mask-size: contain;
  -webkit-mask-repeat: no-repeat;
}
```

**When to use:**

- Decorative icons applied via CSS classes
- Icons that need to inherit text color (use mask approach)
- Avoiding markup changes

**Trade-offs:**

- Background-image: Cannot change color dynamically
- Mask approach: Requires vendor prefixes for Safari (`-webkit-mask-*`)
- Both: Not accessible without additional ARIA markup

## Styling Icons

### Sizing

```html
<!-- With inline styles -->
<i class="bi bi-heart" style="font-size: 24px;"></i>
<i class="bi bi-heart" style="font-size: 2rem;"></i>

<!-- With Bootstrap font-size utilities -->
<i class="bi bi-heart fs-1"></i>  <!-- 2.5rem -->
<i class="bi bi-heart fs-2"></i>  <!-- 2rem -->
<i class="bi bi-heart fs-3"></i>  <!-- 1.75rem -->
<i class="bi bi-heart fs-4"></i>  <!-- 1.5rem -->
<i class="bi bi-heart fs-5"></i>  <!-- 1.25rem -->
<i class="bi bi-heart fs-6"></i>  <!-- 1rem -->

<!-- With custom CSS class -->
<style>
  .icon-lg { font-size: 3rem; }
  .icon-md { font-size: 1.5rem; }
  .icon-sm { font-size: 0.875rem; }
</style>
<i class="bi bi-heart icon-lg"></i>

<!-- SVG sizing with width/height -->
<svg class="bi" width="48" height="48">...</svg>
```

### Coloring

```html
<!-- Bootstrap text utilities -->
<i class="bi bi-heart text-primary"></i>
<i class="bi bi-heart text-danger"></i>
<i class="bi bi-heart text-success"></i>
<i class="bi bi-heart text-warning"></i>
<i class="bi bi-heart text-info"></i>

<!-- Inline color -->
<i class="bi bi-heart" style="color: #ff6b6b;"></i>

<!-- SVG with fill -->
<svg class="bi" fill="#ff6b6b">...</svg>

<!-- SVG with currentColor (inherits parent color) -->
<div style="color: red;">
  <svg class="bi" fill="currentColor">...</svg>
</div>
```

### Vertical Alignment

```html
<!-- Align with text -->
<i class="bi bi-heart" style="vertical-align: middle;"></i>

<!-- Or use Bootstrap alignment -->
<i class="bi bi-heart align-middle"></i>

<!-- Common fix for vertical centering -->
<style>
  .bi {
    vertical-align: -.125em;
  }
</style>
```

## Accessibility

### Icons with Meaning

When icons convey meaning, provide accessible text:

```html
<!-- Option 1: Visually hidden text -->
<button class="btn btn-danger">
  <i class="bi bi-trash" aria-hidden="true"></i>
  <span class="visually-hidden">Delete</span>
</button>

<!-- Option 2: aria-label on parent -->
<button class="btn btn-danger" aria-label="Delete">
  <i class="bi bi-trash" aria-hidden="true"></i>
</button>

<!-- Option 3: title attribute (tooltip) -->
<i class="bi bi-info-circle" title="More information" role="img" aria-label="More information"></i>
```

### Decorative Icons

Hide purely decorative icons from screen readers:

```html
<i class="bi bi-star-fill" aria-hidden="true"></i>
```

### Icon with Visible Text

When text is visible, hide icon from screen readers:

```html
<button class="btn btn-primary">
  <i class="bi bi-download" aria-hidden="true"></i> Download
</button>
```

## Common Patterns

### Button with Icon

```html
<!-- Icon before text -->
<button class="btn btn-primary">
  <i class="bi bi-download me-1"></i> Download
</button>

<!-- Icon after text -->
<button class="btn btn-primary">
  Next <i class="bi bi-arrow-right ms-1"></i>
</button>

<!-- Icon only -->
<button class="btn btn-outline-secondary" aria-label="Settings">
  <i class="bi bi-gear-fill"></i>
</button>
```

### Navigation with Icons

```html
<ul class="nav nav-pills">
  <li class="nav-item">
    <a class="nav-link active" href="#">
      <i class="bi bi-house-fill me-1"></i> Home
    </a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#">
      <i class="bi bi-person me-1"></i> Profile
    </a>
  </li>
</ul>
```

### List with Icons

```html
<ul class="list-unstyled">
  <li><i class="bi bi-check-circle text-success me-2"></i>Feature one</li>
  <li><i class="bi bi-check-circle text-success me-2"></i>Feature two</li>
  <li><i class="bi bi-x-circle text-danger me-2"></i>Not included</li>
</ul>
```

### Social Icons

```html
<div class="d-flex gap-3 fs-4">
  <a href="#" class="text-decoration-none">
    <i class="bi bi-facebook text-primary"></i>
  </a>
  <a href="#" class="text-decoration-none">
    <i class="bi bi-twitter-x text-dark"></i>
  </a>
  <a href="#" class="text-decoration-none">
    <i class="bi bi-instagram text-danger"></i>
  </a>
  <a href="#" class="text-decoration-none">
    <i class="bi bi-linkedin text-primary"></i>
  </a>
  <a href="#" class="text-decoration-none">
    <i class="bi bi-github text-dark"></i>
  </a>
</div>
```

### Icon Badges

```html
<button class="btn btn-primary position-relative">
  <i class="bi bi-envelope"></i>
  <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
    99+
    <span class="visually-hidden">unread messages</span>
  </span>
</button>
```

## Popular Icon Names

### Actions

`bi-plus`, `bi-dash`, `bi-x`, `bi-check`, `bi-pencil`, `bi-trash`, `bi-download`, `bi-upload`, `bi-search`, `bi-filter`

### Navigation

`bi-arrow-left`, `bi-arrow-right`, `bi-arrow-up`, `bi-arrow-down`, `bi-chevron-left`, `bi-chevron-right`, `bi-house`, `bi-list`, `bi-grid`

### UI Elements

`bi-bell`, `bi-gear`, `bi-sliders`, `bi-three-dots`, `bi-three-dots-vertical`, `bi-person`, `bi-people`, `bi-envelope`, `bi-chat`

### Status

`bi-check-circle`, `bi-x-circle`, `bi-exclamation-circle`, `bi-info-circle`, `bi-question-circle`

### Files

`bi-file`, `bi-folder`, `bi-image`, `bi-film`, `bi-music-note`, `bi-file-pdf`, `bi-file-word`, `bi-file-excel`

### Social

`bi-facebook`, `bi-twitter-x`, `bi-instagram`, `bi-linkedin`, `bi-github`, `bi-youtube`, `bi-discord`, `bi-slack`

## Additional Resources

### Reference Files

- `references/icon-categories.md` - Full icon list organized by category (Actions, Navigation, UI Elements, Status, Files, Media, Social, Devices, Weather, E-commerce, Development)
- `references/sass-integration.md` - Sass variables, bundler configuration (Vite, Parcel, Webpack), integration with Bootstrap Sass, and troubleshooting
- `references/rails-integration.md` - Rails 8 Propshaft setup, cssbundling-rails, dartsass-rails, bootstrap-icons gem, and troubleshooting

### Example Files

- `examples/icon-methods-styling-patterns.html` - Icon fonts, embedded SVG, SVG sprites, sizing, coloring, and vertical alignment techniques
- `examples/icon-ui-accessibility-patterns.html` - Buttons, navigation, lists, social icons, badges, and accessibility patterns
