---
name: web-accessibility
description: >-
  Web accessibility and interface standards guide. Covers WCAG compliance,
  semantic HTML, keyboard navigation, screen readers, forms, touch targets,
  and internationalization. Use when building, reviewing, or auditing web
  interfaces for accessibility and UX quality.
---

# Web Accessibility

Build interfaces that work for everyone. These are not optional enhancements — they are baseline quality.

## Semantic HTML

Use the right element for the job. Never simulate interactive elements with `<div>`.

```tsx
// BAD: div with click handler
<div onClick={handleClick} className="button">Submit</div>

// GOOD: semantic button
<button onClick={handleClick}>Submit</button>

// BAD: div as link
<div onClick={() => router.push('/about')}>About</div>

// GOOD: anchor/Link for navigation
<Link href="/about">About</Link>
```

### Element Selection Guide

| Purpose | Element | Not |
|---------|---------|-----|
| Action (submit, toggle, delete) | `<button>` | `<div onClick>` |
| Navigation to URL | `<a>` / `<Link>` | `<button onClick={navigate}>` |
| Form input | `<input>`, `<select>`, `<textarea>` | Custom div-based inputs |
| Section heading | `<h1>`–`<h6>` (sequential) | `<div className="heading">` |
| List of items | `<ul>` / `<ol>` + `<li>` | Repeated `<div>` |
| Navigation group | `<nav>` | `<div className="nav">` |
| Main content | `<main>` | `<div id="content">` |

## Keyboard Navigation

Every interactive element must be keyboard accessible.

### Focus Management

```css
/* NEVER remove focus indicators without replacement */
/* BAD */
*:focus { outline: none; }

/* GOOD: Visible focus only on keyboard navigation */
.interactive:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* Group focus for compound controls */
.input-group:focus-within {
  outline: 2px solid var(--color-accent);
}
```

### Keyboard Event Handling

```tsx
// Interactive custom elements need keyboard support
function CustomButton({ onClick, children }: { onClick: () => void; children: React.ReactNode }) {
  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
    >
      {children}
    </div>
  );
}
// Better: just use <button> and avoid all of the above
```

### Skip Links

Provide skip navigation for keyboard users.

```tsx
<a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50">
  Skip to main content
</a>
```

Headings used as scroll targets need offset for fixed headers:

```css
[id] { scroll-margin-top: 5rem; }
```

## ARIA Patterns

### Icon Buttons

```tsx
// Icon-only buttons MUST have aria-label
<button aria-label="Close dialog" onClick={onClose}>
  <XIcon aria-hidden="true" />
</button>

// Decorative icons are hidden from screen readers
<span aria-hidden="true">🔒</span> Secure connection
```

### Live Regions

Announce dynamic content changes to screen readers.

```tsx
// Toast notifications
<div role="status" aria-live="polite">
  {notification && <p>{notification.message}</p>}
</div>

// Error alerts
<div role="alert" aria-live="assertive">
  {error && <p>{error.message}</p>}
</div>
```

### Loading States

```tsx
<button disabled={isLoading} aria-busy={isLoading}>
  {isLoading ? 'Saving\u2026' : 'Save'}  {/* proper ellipsis character */}
</button>

// Skeleton screens
<div aria-busy="true" aria-label="Loading content">
  <Skeleton />
</div>
```

## Forms

### Labels

Every input must have an associated label.

```tsx
// GOOD: Explicit association
<label htmlFor="email">Email</label>
<input id="email" type="email" autoComplete="email" />

// GOOD: Wrapping (clickable label, no htmlFor needed)
<label>
  Email
  <input type="email" autoComplete="email" />
</label>

// GOOD: Visually hidden but accessible
<label htmlFor="search" className="sr-only">Search</label>
<input id="search" type="search" placeholder="Search..." />
```

### Input Types and Autocomplete

Use semantic input types to get the right mobile keyboard and browser behavior.

```tsx
<input type="email" autoComplete="email" />
<input type="tel" autoComplete="tel" />
<input type="url" autoComplete="url" />
<input type="password" autoComplete="current-password" />
<input type="password" autoComplete="new-password" />
```

### Validation and Errors

```tsx
<div>
  <label htmlFor="email">Email</label>
  <input
    id="email"
    type="email"
    aria-invalid={!!errors.email}
    aria-describedby={errors.email ? 'email-error' : undefined}
  />
  {errors.email && (
    <p id="email-error" role="alert" className="text-red-600">
      {errors.email}
    </p>
  )}
</div>
```

### Form Behavior Rules

- **Never prevent paste** on any input
- **Disable spellcheck** on emails and codes: `spellCheck={false}`
- **Submit button stays enabled** until request starts; show spinner during loading
- **Focus first error** on submit failure
- Checkboxes and radio buttons: single hit target, no dead zones between label and input

## Images and Media

```tsx
// Informative images: descriptive alt
<img src="chart.png" alt="Revenue grew 40% from Q1 to Q3 2025" />

// Decorative images: empty alt
<img src="divider.svg" alt="" />

// Prevent layout shift: always set dimensions
<img src="photo.jpg" width={800} height={600} alt="Team photo" />

// Below fold: lazy load
<img src="photo.jpg" loading="lazy" alt="..." />

// Critical: prioritize
<img src="hero.jpg" fetchPriority="high" alt="..." />
```

## Touch and Mobile

### Touch Targets

Minimum 44x44px for all interactive elements (WCAG 2.5.5).

```css
.touch-target {
  min-height: 44px;
  min-width: 44px;
}
```

### Safe Areas

Handle device notches and home indicators.

```css
.full-bleed {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

### Touch Behavior

```css
/* Prevent 300ms delay and highlight flash */
.interactive {
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

/* Prevent scroll chaining on modals */
.modal { overscroll-behavior: contain; }
```

## Internationalization

```tsx
// BAD: Hardcoded formats
const date = `${month}/${day}/${year}`;
const price = `$${amount.toFixed(2)}`;

// GOOD: Locale-aware formatting
const date = new Intl.DateTimeFormat(locale).format(new Date());
const price = new Intl.NumberFormat(locale, {
  style: 'currency',
  currency: 'USD',
}).format(amount);

// Detect language
const lang = request.headers.get('accept-language')?.split(',')[0] ?? 'en';
```

## Performance for Accessibility

- Lists > 50 items: virtualize
- Critical fonts: `<link rel="preload" as="font">` with `font-display: swap`
- Avoid layout reads during render (causes jank for screen reader users too)
- Uncontrolled inputs perform better than controlled for large forms

## Checklist

Use this for review:

- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible on `:focus-visible`
- [ ] Color contrast meets WCAG AA (4.5:1 body, 3:1 large text)
- [ ] Images have appropriate alt text
- [ ] Form inputs have labels
- [ ] Error messages are associated with inputs via `aria-describedby`
- [ ] Icon-only buttons have `aria-label`
- [ ] Dynamic content uses `aria-live` regions
- [ ] Touch targets are minimum 44x44px
- [ ] `prefers-reduced-motion` is respected
- [ ] No `outline: none` without replacement focus style
- [ ] Heading hierarchy is sequential (no skipped levels)
