---
name: css-styling
description: Write modern, maintainable CSS using best practices for layouts, responsive design, animations, and CSS architecture. Use when styling websites, fixing CSS issues, or implementing designs.
---

# CSS Styling Skill

## Instructions

When writing CSS:

### 1. Modern CSS Reset

```css
*, *::before, *::after {
  box-sizing: border-box;
}

* {
  margin: 0;
  padding: 0;
}

html {
  -webkit-text-size-adjust: none;
  text-size-adjust: none;
}

body {
  min-height: 100vh;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

input, button, textarea, select {
  font: inherit;
}

p, h1, h2, h3, h4, h5, h6 {
  overflow-wrap: break-word;
}
```

### 2. CSS Custom Properties (Variables)

```css
:root {
  /* Colors */
  --color-primary: #2563eb;
  --color-primary-dark: #1d4ed8;
  --color-secondary: #64748b;
  --color-success: #22c55e;
  --color-error: #ef4444;

  /* Typography */
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: ui-monospace, monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;

  /* Borders */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 300ms ease;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #0f172a;
    --color-text: #f1f5f9;
  }
}
```

### 3. Flexbox Layouts

```css
/* Center anything */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Space between */
.space-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Stack vertically */
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* Wrap items */
.flex-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}
```

### 4. Grid Layouts

```css
/* Auto-fit responsive grid */
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-6);
}

/* Fixed columns */
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

/* Sidebar layout */
.with-sidebar {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: var(--space-8);
}

/* Holy grail layout */
.holy-grail {
  display: grid;
  grid-template:
    "header header header" auto
    "nav main aside" 1fr
    "footer footer footer" auto
    / 200px 1fr 200px;
  min-height: 100vh;
}
```

### 5. Responsive Design

```css
/* Mobile-first breakpoints */
/* Base: Mobile */

@media (min-width: 640px) {
  /* Tablet */
}

@media (min-width: 1024px) {
  /* Desktop */
}

@media (min-width: 1280px) {
  /* Large desktop */
}

/* Container queries */
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: flex;
  }
}

/* Clamp for fluid typography */
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
}
```

### 6. Common Components

**Buttons:**
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  font-weight: 500;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-dark);
}

.btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

**Cards:**
```css
.card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.card-body {
  padding: var(--space-6);
}

.card-title {
  font-size: var(--text-xl);
  font-weight: 600;
  margin-bottom: var(--space-2);
}
```

**Forms:**
```css
.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid #e2e8f0;
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  transition: border-color var(--transition-fast);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.input:invalid {
  border-color: var(--color-error);
}
```

### 7. Animations

```css
/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in {
  animation: fadeIn var(--transition-normal) ease-out;
}

/* Slide up */
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
  animation: slideUp var(--transition-normal) ease-out;
}

/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 8. Utility Classes

```css
/* Visually hidden (accessible) */
.visually-hidden {
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

/* Truncate text */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Line clamp */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

### 9. Best Practices

- Use CSS custom properties for theming
- Mobile-first responsive approach
- Avoid !important
- Use logical properties (margin-inline, padding-block)
- Prefer classes over IDs for styling
- Use BEM or similar naming convention
- Minimize nesting depth
- Group related properties

### 10. Performance Tips

- Avoid expensive selectors
- Use `will-change` sparingly
- Prefer `transform` and `opacity` for animations
- Use `contain` for isolated components
- Lazy load non-critical CSS

---

## WordPress-Specific CSS

### 11. Enqueueing Styles Properly

```php
// In functions.php or plugin file
function theme_enqueue_styles() {
    // Main stylesheet
    wp_enqueue_style(
        'theme-style',
        get_stylesheet_uri(),
        array(),
        wp_get_theme()->get('Version')
    );

    // Additional CSS
    wp_enqueue_style(
        'theme-custom',
        get_template_directory_uri() . '/assets/css/custom.css',
        array('theme-style'),
        '1.0.0'
    );
}
add_action('wp_enqueue_scripts', 'theme_enqueue_styles');

// Admin styles
function theme_admin_styles() {
    wp_enqueue_style(
        'theme-admin',
        get_template_directory_uri() . '/assets/css/admin.css',
        array(),
        '1.0.0'
    );
}
add_action('admin_enqueue_scripts', 'theme_admin_styles');
```

### 12. RTL Support

```php
// Register RTL stylesheet
wp_enqueue_style('theme-style', get_stylesheet_uri());
wp_style_add_data('theme-style', 'rtl', 'replace');

// Or with suffix
wp_style_add_data('theme-style', 'rtl', get_template_directory_uri() . '/assets/css/style-rtl.css');
```

```css
/* Use logical properties for automatic RTL */
.element {
    margin-inline-start: 1rem;  /* margin-left in LTR, margin-right in RTL */
    padding-inline-end: 1rem;   /* padding-right in LTR, padding-left in RTL */
    text-align: start;          /* left in LTR, right in RTL */
}

/* Or use [dir] attribute */
[dir="rtl"] .element {
    margin-left: 0;
    margin-right: 1rem;
}
```

### 13. Block Editor (Gutenberg) Styles

```php
// Editor styles
function theme_editor_styles() {
    add_theme_support('editor-styles');
    add_editor_style('assets/css/editor-style.css');
}
add_action('after_setup_theme', 'theme_editor_styles');

// Block styles
function theme_block_styles() {
    wp_enqueue_block_style('core/button', array(
        'handle' => 'theme-button-style',
        'src'    => get_template_directory_uri() . '/assets/css/blocks/button.css',
    ));
}
add_action('init', 'theme_block_styles');
```

### 14. theme.json Integration

```json
{
    "version": 2,
    "settings": {
        "color": {
            "palette": [
                { "slug": "primary", "color": "#2563eb", "name": "Primary" },
                { "slug": "secondary", "color": "#64748b", "name": "Secondary" }
            ]
        },
        "spacing": {
            "units": ["px", "rem", "%"],
            "spacingScale": { "steps": 7 }
        },
        "typography": {
            "fontFamilies": [
                { "slug": "system", "fontFamily": "system-ui, sans-serif", "name": "System" }
            ]
        }
    }
}
```

```css
/* Use WordPress CSS variables from theme.json */
.element {
    color: var(--wp--preset--color--primary);
    font-family: var(--wp--preset--font-family--system);
    padding: var(--wp--preset--spacing--40);
}
```

### 15. WordPress Admin Compatibility

```css
/* Match WordPress admin colors */
.wp-admin .my-plugin-box {
    background: #f0f0f1;
    border: 1px solid #c3c4c7;
    border-radius: 4px;
}

/* Use admin color scheme variables */
.wp-admin .my-button {
    background: var(--wp-admin-theme-color, #2271b1);
    color: var(--wp-admin-theme-color-darker-10, #135e96);
}

/* Responsive admin */
@media screen and (max-width: 782px) {
    .wp-admin .my-plugin-box {
        padding: 12px;
    }
}
```

### 16. WordPress CSS Best Practices

- **Prefix classes** with theme/plugin slug to avoid conflicts
- **Use `wp_add_inline_style()`** for dynamic CSS
- **Avoid !important** - use specificity instead
- **Support RTL** with logical properties or RTL stylesheet
- **Test in Gutenberg** editor view
- **Use theme.json** for design tokens when possible
- **Minify for production** using build tools
