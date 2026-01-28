---
name: web-design-guidelines
description: UI/UX best practices and accessibility guidelines. Use when reviewing UI code, checking accessibility, auditing forms, or ensuring web interface best practices. Triggers on "review UI", "check accessibility", "audit design", "review UX", or "check best practices".
license: MIT
metadata:
  author: Web Accessibility Initiative (WAI)
  version: "1.0.0"
---

# Web Design Guidelines

Comprehensive UI/UX and accessibility guidelines for building inclusive, performant web interfaces. Contains 21 rules across 8 categories, prioritized by WCAG compliance and user impact.

## When to Apply

Reference these guidelines when:
- Reviewing UI code for accessibility
- Implementing forms and interactions
- Optimizing performance
- Ensuring cross-browser compatibility
- Improving user experience

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Accessibility - Semantic Structure | CRITICAL | `a11y-` |
| 2 | Accessibility - Keyboard & Focus | CRITICAL | `a11y-` |
| 3 | Accessibility - Visual & Color | CRITICAL | `a11y-` |
| 4 | Forms - Input & Validation | CRITICAL | `form-` |
| 5 | Forms - Error Handling | HIGH | `form-` |
| 6 | Forms - User Experience | MEDIUM | `form-` |
| 7 | Animation & Motion | CRITICAL | `motion-` |
| 8 | Performance & UX | MEDIUM | `perf-` |

## Quick Reference

### 1. Accessibility - Semantic Structure (CRITICAL)

- `a11y-semantic-html` - Use semantic HTML elements
- `a11y-heading-hierarchy` - Maintain proper heading hierarchy
- `a11y-screen-reader` - Optimize for screen reader compatibility
- `a11y-skip-links` - Provide skip links for navigation

### 2. Accessibility - Keyboard & Focus (CRITICAL)

- `a11y-keyboard-nav` - Ensure full keyboard navigation
- `a11y-focus-management` - Manage keyboard focus properly
- `a11y-aria-labels` - Add ARIA labels to interactive elements

### 3. Accessibility - Visual & Color (CRITICAL)

- `a11y-color-contrast` - Ensure sufficient color contrast
- `a11y-alt-text` - Provide meaningful alt text for images

### 4. Forms - Input & Validation (CRITICAL)

- `form-autocomplete` - Use autocomplete attributes for forms
- `form-input-types` - Use correct input types
- `form-labels` - Associate labels with form inputs

### 5. Forms - Error Handling (HIGH)

- `form-error-display` - Display form errors clearly
- `form-error-messages` - Provide accessible error messages
- `form-validation-ux` - Design user-friendly form validation

### 6. Forms - User Experience (MEDIUM)

- `form-inline-validation` - Implement smart inline validation
- `form-multi-step` - Design effective multi-step forms
- `form-placeholder-usage` - Use placeholders appropriately
- `form-submit-feedback` - Provide clear form submission feedback

### 7. Animation & Motion (CRITICAL)

- `motion-reduced` - Respect prefers-reduced-motion preference

### 8. Performance & UX (MEDIUM)

- Image optimization and layout stability patterns

## Essential Guidelines

### Semantic HTML

```tsx
// ❌ Div soup - no semantic meaning
<div className="header">
  <div className="nav">
    <div onClick={handleClick}>Home</div>
  </div>
</div>
<div className="content">
  <div className="title">Page Title</div>
  <div className="text">Content here...</div>
</div>

// ✅ Semantic HTML - accessible and meaningful
<header>
  <nav aria-label="Main navigation">
    <a href="/">Home</a>
  </nav>
</header>
<main>
  <article>
    <h1>Page Title</h1>
    <p>Content here...</p>
  </article>
</main>
```

### ARIA Labels

```tsx
// Interactive elements need accessible names
<button aria-label="Close dialog">
  <XIcon />
</button>

<button aria-label="Add to cart">
  <PlusIcon />
</button>

// Icon-only links
<a href="/settings" aria-label="Settings">
  <SettingsIcon />
</a>

// Decorative icons should be hidden
<span aria-hidden="true">🎉</span>
```

### Keyboard Navigation

```tsx
// All interactive elements must be keyboard accessible
function Dialog({ isOpen, onClose, children }) {
  // Trap focus inside dialog
  const dialogRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (isOpen) {
      dialogRef.current?.focus()
    }
  }, [isOpen])

  // Handle Escape key
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose()
    }
  }

  return (
    <div
      ref={dialogRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={handleKeyDown}
    >
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  )
}
```

### Focus Styles

```tsx
// ✅ Always visible focus styles
<button className="
  focus:outline-none
  focus-visible:ring-2
  focus-visible:ring-blue-500
  focus-visible:ring-offset-2
">
  Button
</button>

// ❌ Never remove focus outlines without replacement
<button className="outline-none focus:outline-none">
  Inaccessible
</button>
```

### Form Accessibility

```tsx
// ✅ Properly labeled form
<form>
  <div>
    <label htmlFor="email">
      Email address
      <span aria-hidden="true" className="text-red-500">*</span>
    </label>
    <input
      id="email"
      type="email"
      name="email"
      required
      aria-required="true"
      aria-describedby="email-hint email-error"
      autoComplete="email"
    />
    <p id="email-hint" className="text-gray-500 text-sm">
      We'll never share your email.
    </p>
    {error && (
      <p id="email-error" role="alert" className="text-red-500 text-sm">
        {error}
      </p>
    )}
  </div>

  <button type="submit">Subscribe</button>
</form>
```

### Respect Reduced Motion

```tsx
// CSS
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

// Tailwind
<div className="
  transition-transform duration-300
  hover:scale-105
  motion-reduce:transition-none
  motion-reduce:hover:transform-none
">
  Card
</div>

// JavaScript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches

function animate() {
  if (prefersReducedMotion) {
    // Skip or simplify animation
    return
  }
  // Full animation
}
```

### Image Handling

```tsx
// ✅ Proper image implementation
<img
  src="/hero.webp"
  alt="Team collaborating around a whiteboard"
  width={1200}
  height={600}
  loading="lazy"
  decoding="async"
/>

// ✅ Decorative images
<img src="/pattern.svg" alt="" aria-hidden="true" />

// ✅ Responsive images
<picture>
  <source
    srcSet="/hero-mobile.webp"
    media="(max-width: 768px)"
    type="image/webp"
  />
  <source srcSet="/hero.webp" type="image/webp" />
  <img src="/hero.jpg" alt="Hero description" width={1200} height={600} />
</picture>
```

### Touch Targets

```tsx
// ✅ Minimum 44x44px touch targets
<button className="min-h-[44px] min-w-[44px] p-2">
  <Icon className="w-6 h-6" />
</button>

// ✅ Adequate spacing between touch targets
<nav className="flex gap-2">
  <a href="/" className="p-3">Home</a>
  <a href="/about" className="p-3">About</a>
</nav>
```

### Color Contrast

```css
/* WCAG AA requires 4.5:1 for normal text, 3:1 for large text */

/* ❌ Insufficient contrast */
.low-contrast {
  color: #999999;        /* Gray on white: ~2.8:1 */
  background: white;
}

/* ✅ Sufficient contrast */
.good-contrast {
  color: #595959;        /* Darker gray: ~7:1 */
  background: white;
}

/* ✅ Don't rely on color alone */
.error {
  color: #dc2626;
  border-left: 4px solid #dc2626;  /* Visual indicator */
}
```

### Live Regions

```tsx
// Announce dynamic content to screen readers
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
  className="sr-only"
>
  {message}
</div>

// Toast notifications
function Toast({ message }: { message: string }) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      className="fixed bottom-4 right-4 bg-gray-900 text-white p-4 rounded"
    >
      {message}
    </div>
  )
}
```

## Output Format

When auditing code, output findings in this format:

```
file:line - [category] Description of issue
```

Example:
```
src/components/Button.tsx:15 - [a11y] Missing aria-label on icon-only button
src/pages/Home.tsx:42 - [perf] Image missing width/height attributes
src/components/Form.tsx:28 - [form] Input missing associated label
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/a11y-semantic-html.md
rules/form-autocomplete.md
rules/motion-reduced.md
rules/_sections.md
```

Each rule file contains:
- YAML frontmatter with metadata (title, impact, tags)
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and WCAG references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
