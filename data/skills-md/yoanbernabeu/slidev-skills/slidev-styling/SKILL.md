---
name: slidev-styling
description: Style Slidev slides with UnoCSS and custom CSS. Use this skill for custom colors, typography, animations, and responsive designs.
---

# Styling in Slidev

This skill covers all styling options in Slidev, including UnoCSS utilities, custom CSS, scoped styles, and advanced styling techniques.

## When to Use This Skill

- Customizing slide appearance
- Adding custom colors and typography
- Creating reusable style patterns
- Implementing animations
- Building responsive layouts

## UnoCSS Basics

Slidev uses UnoCSS, an atomic CSS framework similar to Tailwind CSS.

### Inline Classes

```markdown
<div class="text-xl font-bold text-blue-500">
  Styled text
</div>
```

### Common Utilities

**Typography**:
```markdown
<span class="text-sm">Small</span>
<span class="text-base">Base</span>
<span class="text-lg">Large</span>
<span class="text-xl">Extra Large</span>
<span class="text-2xl">2XL</span>

<span class="font-bold">Bold</span>
<span class="font-semibold">Semibold</span>
<span class="italic">Italic</span>
<span class="underline">Underlined</span>
```

**Colors**:
```markdown
<span class="text-red-500">Red text</span>
<span class="text-blue-600">Blue text</span>
<span class="bg-green-100">Green background</span>
<span class="bg-yellow-200 text-yellow-800">Yellow combo</span>
```

**Spacing**:
```markdown
<div class="p-4">Padding 4</div>
<div class="m-2">Margin 2</div>
<div class="px-4 py-2">Horizontal/Vertical padding</div>
<div class="mt-8">Margin top 8</div>
```

**Layout**:
```markdown
<div class="flex items-center justify-between">
  <span>Left</span>
  <span>Right</span>
</div>

<div class="grid grid-cols-2 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
</div>
```

## Color System

### Default Colors

```markdown
<!-- Grays -->
<span class="text-gray-100">100</span>
<span class="text-gray-500">500</span>
<span class="text-gray-900">900</span>

<!-- Colors -->
<span class="text-red-500">Red</span>
<span class="text-orange-500">Orange</span>
<span class="text-yellow-500">Yellow</span>
<span class="text-green-500">Green</span>
<span class="text-blue-500">Blue</span>
<span class="text-purple-500">Purple</span>
<span class="text-pink-500">Pink</span>
```

### Custom Colors

In `uno.config.ts`:

```typescript
import { defineConfig } from 'unocss'

export default defineConfig({
  theme: {
    colors: {
      brand: {
        DEFAULT: '#5d8392',
        light: '#8bb4c4',
        dark: '#3d5a65',
      },
      accent: '#f59e0b',
    },
  },
})
```

Usage:
```markdown
<span class="text-brand">Brand color</span>
<span class="bg-brand-light">Light brand background</span>
<span class="text-accent">Accent color</span>
```

## Typography

### Font Sizes

```markdown
<p class="text-xs">Extra small (12px)</p>
<p class="text-sm">Small (14px)</p>
<p class="text-base">Base (16px)</p>
<p class="text-lg">Large (18px)</p>
<p class="text-xl">XL (20px)</p>
<p class="text-2xl">2XL (24px)</p>
<p class="text-3xl">3XL (30px)</p>
<p class="text-4xl">4XL (36px)</p>
<p class="text-5xl">5XL (48px)</p>
```

### Custom Fonts

In frontmatter:

```yaml
---
fonts:
  sans: 'Inter'
  serif: 'Merriweather'
  mono: 'Fira Code'
---
```

In `uno.config.ts`:

```typescript
export default defineConfig({
  theme: {
    fontFamily: {
      display: ['Inter', 'sans-serif'],
      body: ['Open Sans', 'sans-serif'],
    },
  },
})
```

Usage:
```markdown
<h1 class="font-display">Display heading</h1>
<p class="font-body">Body text</p>
```

### Google Fonts

```yaml
---
fonts:
  sans: 'Roboto'
  serif: 'Playfair Display'
  mono: 'JetBrains Mono'
  provider: 'google'
---
```

## Global Styles

### styles/index.css

```css
/* styles/index.css */

/* Root variables */
:root {
  --color-primary: #3b82f6;
  --color-secondary: #10b981;
  --font-size-base: 16px;
}

/* Global typography */
.slidev-layout h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary);
}

.slidev-layout h2 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--color-secondary);
}

/* Custom utility classes */
.highlight {
  background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
  padding: 0 0.25em;
}

.shadow-brand {
  box-shadow: 0 4px 14px 0 rgba(93, 131, 146, 0.39);
}

/* Animation classes */
.fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

## Scoped Styles

### Per-Slide Styles

Add `<style>` at the end of a slide:

```markdown
# My Styled Slide

<div class="custom-box">
  Special content
</div>

<style>
.custom-box {
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 1rem;
  color: white;
}

h1 {
  color: #667eea;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
</style>
```

### Scoped vs Global

Styles in `<style>` are automatically scoped to the slide.

For global styles within a slide:
```markdown
<style>
:global(.slidev-layout) {
  /* Affects all slides */
}
</style>
```

## Layout Utilities

### Flexbox

```markdown
<div class="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<div class="flex items-center justify-center h-full">
  <p>Centered content</p>
</div>

<div class="flex flex-wrap gap-2">
  <span class="badge">Tag 1</span>
  <span class="badge">Tag 2</span>
</div>
```

### Grid

```markdown
<div class="grid grid-cols-3 gap-4">
  <div>1</div>
  <div>2</div>
  <div>3</div>
</div>

<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
  <!-- Responsive grid -->
</div>
```

### Positioning

```markdown
<div class="relative">
  <div class="absolute top-0 right-0">
    Top right corner
  </div>
</div>

<div class="fixed bottom-4 right-4">
  Fixed position
</div>
```

## Custom Shortcuts

### In uno.config.ts

```typescript
import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    'btn': 'px-4 py-2 rounded bg-blue-500 text-white hover:bg-blue-600',
    'btn-outline': 'px-4 py-2 rounded border border-blue-500 text-blue-500 hover:bg-blue-50',
    'card': 'p-4 rounded-lg shadow-md bg-white dark:bg-gray-800',
    'section-title': 'text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4',
    'badge': 'px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800',
  },
})
```

Usage:
```markdown
<button class="btn">Click me</button>
<div class="card">Card content</div>
<h2 class="section-title">Section</h2>
```

## Dark Mode Styling

### Dark Mode Classes

```markdown
<div class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
  Adapts to dark mode
</div>
```

### In Custom CSS

```css
.my-component {
  background: #ffffff;
  color: #1a1a1a;
}

.dark .my-component {
  background: #1a1a1a;
  color: #ffffff;
}
```

## Animations

### Transition Utilities

```markdown
<div class="transition-all duration-300 hover:scale-110">
  Scales on hover
</div>

<div class="transition-colors duration-200 hover:bg-blue-500">
  Color transition
</div>
```

### Custom Animations

```css
/* styles/index.css */
@keyframes slideInLeft {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.animate-slide-in-left {
  animation: slideInLeft 0.5s ease-out;
}
```

### Animation with v-motion

```markdown
<div
  v-motion
  :initial="{ opacity: 0, y: 50 }"
  :enter="{ opacity: 1, y: 0, transition: { duration: 500 } }"
>
  Animated content
</div>
```

## Responsive Design

### Breakpoints

```markdown
<div class="text-sm md:text-base lg:text-lg">
  Responsive text size
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  Responsive grid
</div>

<div class="hidden lg:block">
  Only visible on large screens
</div>
```

### Default Breakpoints

| Prefix | Width |
|--------|-------|
| `sm` | 640px |
| `md` | 768px |
| `lg` | 1024px |
| `xl` | 1280px |
| `2xl` | 1536px |

## Common Patterns

### Card Component

```markdown
<div class="p-6 rounded-xl bg-white dark:bg-gray-800 shadow-lg">
  <h3 class="text-lg font-semibold mb-2">Card Title</h3>
  <p class="text-gray-600 dark:text-gray-300">Card content</p>
</div>
```

### Badge

```markdown
<span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
  Active
</span>
```

### Alert Box

```markdown
<div class="p-4 rounded-lg bg-yellow-50 border-l-4 border-yellow-400">
  <p class="text-yellow-700">Warning message</p>
</div>
```

### Code Annotation

```markdown
<div class="relative">

```js
const x = 1 // [!code highlight]
```

<div class="absolute right-4 top-4 text-xs text-gray-500">
  Important line!
</div>
</div>
```

## Best Practices

### 1. Use Utilities First

```markdown
<!-- Prefer utilities -->
<div class="p-4 bg-blue-500 text-white rounded">
  Good
</div>

<!-- Custom CSS only when necessary -->
```

### 2. Create Shortcuts for Repeated Patterns

```typescript
shortcuts: {
  'btn-primary': 'px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600',
}
```

### 3. Maintain Consistency

Use the same spacing scale:
- `gap-4` everywhere, not mixing `gap-3` and `gap-5`

### 4. Support Dark Mode

Always provide dark mode variants for custom styles.

### 5. Test Export

Some CSS features don't export well to PDF:
- Complex gradients
- Some filters
- Animations (become static)

## Output Format

When styling slides:

```markdown
# [Slide Title]

<div class="[utility classes]">
  Content
</div>

<style>
/* Scoped styles if needed */
.custom-class {
  property: value;
}
</style>
```

**STYLE DECISIONS:**
- Colors: [primary, secondary]
- Typography: [font choices]
- Spacing: [consistent scale]
- Custom shortcuts: [list]

**FILES MODIFIED:**
- uno.config.ts (shortcuts, theme)
- styles/index.css (global styles)
