---
name: accessibility
description: Web accessibility (a11y) best practices for WCAG 2.1 AA compliance, ARIA attributes, keyboard navigation, screen reader support, and inclusive design. Use when auditing accessibility, implementing accessible features, fixing a11y issues, or when user mentions WCAG, accessibility, screen readers, or keyboard navigation.
---

# Web Accessibility (A11Y)

WCAG 2.1 AA compliance guidelines and implementation patterns.

## WCAG Principles (POUR)

1. **Perceivable** - Information must be presentable in ways users can perceive
2. **Operable** - Interface must be operable by all users
3. **Understandable** - Information and operation must be understandable
4. **Robust** - Content must be robust enough for assistive technologies

## Semantic HTML

### Use Correct Elements

```html
<!-- BAD: Div soup -->
<div class="header">
    <div class="nav">
        <div class="link" onclick="navigate()">Home</div>
    </div>
</div>

<!-- GOOD: Semantic elements -->
<header>
    <nav aria-label="Main navigation">
        <a href="/">Home</a>
    </nav>
</header>
```

### Headings Hierarchy

```html
<!-- BAD: Skipping heading levels -->
<h1>Page Title</h1>
<h3>Section</h3>  <!-- Skipped h2! -->

<!-- GOOD: Proper hierarchy -->
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

### Landmark Regions

```html
<header role="banner">
    <nav role="navigation" aria-label="Main">...</nav>
</header>

<main role="main">
    <article>...</article>
    <aside role="complementary">...</aside>
</main>

<footer role="contentinfo">...</footer>
```

## Images & Media

### Alternative Text

```html
<!-- Informative image -->
<img src="chart.png" alt="Sales increased 25% in Q4 2024">

<!-- Decorative image -->
<img src="divider.png" alt="" role="presentation">

<!-- Complex image -->
<figure>
    <img src="diagram.png" alt="System architecture diagram">
    <figcaption>
        Figure 1: The system consists of a web server,
        application server, and database server.
    </figcaption>
</figure>

<!-- Logo/link -->
<a href="/">
    <img src="logo.png" alt="Company Name - Home">
</a>
```

### Video & Audio

```html
<video controls>
    <source src="video.mp4" type="video/mp4">
    <track kind="captions" src="captions.vtt" srclang="en" label="English">
    <track kind="descriptions" src="descriptions.vtt" srclang="en" label="Audio descriptions">
</video>
```

## Forms

### Labels

```html
<!-- BAD: No label association -->
<input type="email" placeholder="Email">

<!-- GOOD: Explicit label -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" required>

<!-- GOOD: Implicit label -->
<label>
    Email address
    <input type="email" name="email" required>
</label>
```

### Error Messages

```html
<div class="form-group">
    <label for="email">Email address</label>
    <input
        type="email"
        id="email"
        name="email"
        aria-describedby="email-error email-hint"
        aria-invalid="true"
        required
    >
    <p id="email-hint" class="hint">We'll never share your email</p>
    <p id="email-error" class="error" role="alert">
        Please enter a valid email address
    </p>
</div>
```

### Fieldsets & Legends

```html
<fieldset>
    <legend>Shipping Address</legend>
    <label for="street">Street</label>
    <input type="text" id="street" name="street">
    <!-- More fields -->
</fieldset>

<fieldset>
    <legend>Preferred contact method</legend>
    <label>
        <input type="radio" name="contact" value="email"> Email
    </label>
    <label>
        <input type="radio" name="contact" value="phone"> Phone
    </label>
</fieldset>
```

## Keyboard Navigation

### Focus Management

```css
/* Never remove focus outline without replacement */
/* BAD */
*:focus { outline: none; }

/* GOOD: Custom focus styles */
:focus {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
}

/* Focus-visible for keyboard-only focus */
:focus:not(:focus-visible) {
    outline: none;
}

:focus-visible {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
}
```

### Tab Order

```html
<!-- Use natural tab order, avoid positive tabindex -->
<button>First</button>
<button>Second</button>
<button>Third</button>

<!-- Remove from tab order if visually hidden -->
<button tabindex="-1" aria-hidden="true">Skip</button>
```

### Skip Links

```html
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <header>...</header>
    <main id="main-content" tabindex="-1">...</main>
</body>

<style>
.skip-link {
    position: absolute;
    left: -9999px;
}
.skip-link:focus {
    left: 0;
    top: 0;
    padding: 1rem;
    background: #000;
    color: #fff;
    z-index: 9999;
}
</style>
```

## ARIA

### ARIA Roles

```html
<!-- Buttons that aren't <button> -->
<div role="button" tabindex="0" aria-pressed="false">Toggle</div>

<!-- Tab interface -->
<div role="tablist">
    <button role="tab" aria-selected="true" aria-controls="panel1">Tab 1</button>
    <button role="tab" aria-selected="false" aria-controls="panel2">Tab 2</button>
</div>
<div role="tabpanel" id="panel1">Content 1</div>
<div role="tabpanel" id="panel2" hidden>Content 2</div>

<!-- Alert for dynamic content -->
<div role="alert" aria-live="assertive">Form submitted successfully</div>
```

### ARIA States & Properties

```html
<!-- Expanded/collapsed -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu" hidden>...</ul>

<!-- Current page -->
<nav>
    <a href="/" aria-current="page">Home</a>
    <a href="/about">About</a>
</nav>

<!-- Disabled -->
<button aria-disabled="true">Submit</button>

<!-- Loading -->
<button aria-busy="true">
    <span class="spinner" aria-hidden="true"></span>
    Loading...
</button>
```

### Live Regions

```html
<!-- Polite announcements (wait for pause) -->
<div aria-live="polite" aria-atomic="true">
    3 items in cart
</div>

<!-- Assertive announcements (immediate) -->
<div role="alert" aria-live="assertive">
    Error: Payment failed
</div>

<!-- Status updates -->
<div role="status" aria-live="polite">
    Showing results 1-10 of 100
</div>
```

## Color & Contrast

### Contrast Requirements

- **Normal text**: 4.5:1 minimum
- **Large text** (18pt+ or 14pt+ bold): 3:1 minimum
- **UI components**: 3:1 minimum

```css
/* BAD: Low contrast */
.light-text {
    color: #999; /* On white: 2.85:1 - FAIL */
}

/* GOOD: Sufficient contrast */
.text {
    color: #595959; /* On white: 7:1 - PASS */
}
```

### Don't Rely on Color Alone

```html
<!-- BAD: Color only -->
<span class="error" style="color: red;">Invalid</span>

<!-- GOOD: Color + icon + text -->
<span class="error">
    <svg aria-hidden="true"><!-- Error icon --></svg>
    Error: Invalid email address
</span>
```

## Testing

### Automated Tools

```bash
# axe-core
npx @axe-core/cli https://example.com

# Lighthouse
npx lighthouse https://example.com --only-categories=accessibility

# Pa11y
npx pa11y https://example.com
```

### Manual Testing Checklist

1. **Keyboard-only navigation**
   - Tab through all interactive elements
   - Ensure visible focus indicator
   - Check logical tab order
   - Test all functionality without mouse

2. **Screen reader testing**
   - VoiceOver (macOS): Cmd + F5
   - NVDA (Windows): Free download
   - Test headings, links, forms, dynamic content

3. **Zoom testing**
   - Zoom to 200%, check layout
   - Zoom to 400%, check readability

4. **Color/contrast**
   - Use browser dev tools contrast checker
   - Test with color blindness simulators

### React Accessibility

```jsx
// Focus management
const inputRef = useRef(null);

useEffect(() => {
    if (showError) {
        inputRef.current?.focus();
    }
}, [showError]);

// Accessible component
function Modal({ isOpen, onClose, title, children }) {
    const modalRef = useRef(null);

    useEffect(() => {
        if (isOpen) {
            modalRef.current?.focus();
            document.body.style.overflow = 'hidden';
        }
        return () => {
            document.body.style.overflow = '';
        };
    }, [isOpen]);

    if (!isOpen) return null;

    return (
        <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            ref={modalRef}
            tabIndex={-1}
        >
            <h2 id="modal-title">{title}</h2>
            {children}
            <button onClick={onClose}>Close</button>
        </div>
    );
}
```

## Common Issues & Fixes

| Issue | Impact | Fix |
|-------|--------|-----|
| Missing alt text | Screen readers can't describe images | Add descriptive alt or alt="" for decorative |
| Missing form labels | Users don't know field purpose | Add `<label for="">` |
| Low color contrast | Hard to read for low vision | Increase contrast to 4.5:1 |
| No focus indicator | Keyboard users can't see focus | Add visible `:focus` styles |
| Mouse-only interactions | Keyboard users can't access | Add keyboard event handlers |
| Auto-playing media | Disorienting, hard to stop | Add controls, don't autoplay |
| Missing page title | Users don't know page context | Add unique `<title>` |
| Missing language | Screen readers mispronounce | Add `<html lang="en">` |
