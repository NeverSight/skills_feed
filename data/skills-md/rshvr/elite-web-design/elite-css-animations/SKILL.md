---
name: elite-css-animations
description: |
  CSS-native animation techniques including Scroll-Driven Animations API, View Transitions, @property rule, and visual effects. Use when asked about: CSS animations, scroll-driven animations, CSS scroll timeline, view transitions, page transitions, @property, animating CSS variables, clip-path animations, backdrop-filter, mix-blend-mode, CSS masks, CSS-only animations, no-JavaScript animations, or when GSAP is not needed/wanted. Includes decision guide for CSS vs GSAP.
---

# Elite CSS Animations

Modern CSS animation capabilities - when JavaScript isn't needed.

## Quick Reference

| Topic | Reference File |
|-------|---------------|
| Scroll-Driven API | [scroll-driven-api.md](references/scroll-driven-api.md) |
| View Transitions | [view-transitions.md](references/view-transitions.md) |
| @property Rule | [property-rule.md](references/property-rule.md) |
| Visual Effects | [visual-effects.md](references/visual-effects.md) |

---

## CSS vs GSAP Decision Guide

### Use CSS When:

- Simple reveal/fade animations
- Progress indicators tied to scroll
- Hover/focus state transitions
- Performance is paramount (off-main-thread)
- Safari support isn't critical (for scroll-driven)
- You want to minimize JavaScript

### Use GSAP When:

- Complex multi-element sequences
- Pin/sticky behavior needed
- Horizontal scrolling sections
- Cross-browser consistency critical
- Fine-grained control (scrub with snap)
- Timeline orchestration

### Hybrid Approach

CSS for simple interactions, GSAP for complex sequences:

```css
/* CSS: Hover states, simple transitions */
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}
```

```javascript
// GSAP: Complex scroll-driven sequences
gsap.timeline({
  scrollTrigger: { trigger: '.section', scrub: 1 }
})
.from('.title', { opacity: 0, y: 50 })
.from('.content', { opacity: 0 }, '-=0.3');
```

---

## Browser Support (2026)

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Scroll-Driven Animations | ✓ 115+ | ✓ 132+ | ✗ (polyfill) | ✓ 115+ |
| View Transitions | ✓ 111+ | ✗ | ✓ 18+ | ✓ 111+ |
| @property | ✓ 85+ | ✓ 128+ | ✓ 15.4+ | ✓ 85+ |
| clip-path animations | ✓ | ✓ | ✓ | ✓ |
| backdrop-filter | ✓ | ✓ | ✓ | ✓ |

---

## Scroll-Driven Animations Quick Start

```css
/* Progress bar that fills as you scroll */
.progress-bar {
  transform-origin: left;
  transform: scaleX(0);
  animation: progress linear;
  animation-timeline: scroll();
}

@keyframes progress {
  to { transform: scaleX(1); }
}
```

```css
/* Element reveals as it enters viewport */
@media (prefers-reduced-motion: no-preference) {
  .reveal {
    animation: fadeIn linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 30%;
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Safari Polyfill

```html
<script src="https://flackr.github.io/scroll-timeline/dist/scroll-timeline.js"></script>
```

See [scroll-driven-api.md](references/scroll-driven-api.md) for complete patterns.

---

## View Transitions Quick Start

```javascript
// Simple page transition
document.startViewTransition(() => {
  // Update the DOM
  updateContent();
});
```

```css
/* Customize the transition */
::view-transition-old(root) {
  animation: fade-out 0.3s ease-out;
}

::view-transition-new(root) {
  animation: fade-in 0.3s ease-in;
}

@keyframes fade-out {
  to { opacity: 0; }
}

@keyframes fade-in {
  from { opacity: 0; }
}
```

See [view-transitions.md](references/view-transitions.md) for SPA integration.

---

## @property Quick Start

Animate CSS custom properties that previously couldn't animate:

```css
@property --progress {
  syntax: '<number>';
  initial-value: 0;
  inherits: false;
}

.progress-circle {
  --progress: 0;
  background: conic-gradient(
    var(--color-accent) calc(var(--progress) * 360deg),
    transparent 0
  );
  transition: --progress 1s ease-out;
}

.progress-circle.complete {
  --progress: 1;
}
```

See [property-rule.md](references/property-rule.md) for gradient animations and more.

---

## Visual Effects Quick Start

### Clip-Path Reveal

```css
.reveal {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.reveal.visible {
  clip-path: inset(0 0 0 0);
}
```

### Backdrop Filter

```css
.glass {
  backdrop-filter: blur(10px) saturate(180%);
  background: rgba(255, 255, 255, 0.7);
}
```

### Mix Blend Mode

```css
.text-overlay {
  mix-blend-mode: difference;
  color: white;
}
```

See [visual-effects.md](references/visual-effects.md) for creative patterns.

---

## prefers-reduced-motion

**Always wrap motion in preference checks:**

```css
/* Default: No animation */
.animated {
  opacity: 1;
  transform: none;
}

/* Only animate if user allows */
@media (prefers-reduced-motion: no-preference) {
  .animated {
    animation: fadeIn 0.6s ease-out;
  }
}
```

---

## Performance Best Practices

### Animate Only Compositor Properties

```css
/* GOOD - GPU accelerated */
.card {
  transition: transform 0.3s, opacity 0.3s;
}

.card:hover {
  transform: translateY(-4px) scale(1.02);
  opacity: 0.9;
}

/* BAD - Triggers layout/paint */
.card:hover {
  width: 110%;
  margin-left: -5%;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
```

### Use will-change Sparingly

```css
/* Apply only during animation */
.animating {
  will-change: transform, opacity;
}

/* Remove after animation */
.animation-complete {
  will-change: auto;
}
```

### Contain Property

```css
/* Isolate expensive effects */
.animated-section {
  contain: layout style paint;
}
```

---

## Common Patterns

### Smooth Hover Transitions

```css
.card {
  transition:
    transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}
```

### Staggered Entrance

```css
.item {
  opacity: 0;
  animation: fadeIn 0.5s ease forwards;
}

.item:nth-child(1) { animation-delay: 0.1s; }
.item:nth-child(2) { animation-delay: 0.2s; }
.item:nth-child(3) { animation-delay: 0.3s; }
/* ... or use CSS custom properties */

@keyframes fadeIn {
  to { opacity: 1; }
}
```

### Loading Spinner

```css
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## Resources

- [MDN: CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations)
- [MDN: Scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations)
- [Chrome: View Transitions](https://developer.chrome.com/docs/web-platform/view-transitions/)
- [Cubic Bezier Generator](https://cubic-bezier.com/)
