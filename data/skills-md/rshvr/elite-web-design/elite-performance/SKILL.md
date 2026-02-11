---
name: elite-performance
description: |
  Performance optimization for premium animated websites. Use when asked about: animation performance, 60fps, Core Web Vitals, Vite setup, bundle optimization, lazy loading, will-change, GPU acceleration, layout thrashing, debugging jank, or performance budgets.
---

# Elite Performance

Maintain 60fps animations while hitting Core Web Vitals targets.

## Quick Reference

| Topic | Reference File |
|-------|---------------|
| Vite Setup | [vite-setup.md](references/vite-setup.md) |
| Animation Performance | [animation-performance.md](references/animation-performance.md) |
| Asset Optimization | [asset-optimization.md](references/asset-optimization.md) |
| Debugging | [debugging.md](references/debugging.md) |

---

## Performance Budget (2026)

### Core Web Vitals Targets

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |

### Animation Targets

| Metric | Target |
|--------|--------|
| Frame rate | 60fps (16.67ms/frame) |
| Frame budget | < 10ms for JS/layout |
| Animation start | < 100ms response |
| Scroll jank | 0 dropped frames |

### Bundle Targets

| Asset | Target |
|-------|--------|
| Initial JS | < 100KB (gzipped) |
| Initial CSS | < 50KB (gzipped) |
| GSAP core | ~25KB (gzipped) |
| Total initial | < 200KB (gzipped) |

---

## GPU-Accelerated Properties

### ONLY Animate These

```css
/* GPU composited - FAST */
transform: translateX() translateY() translateZ()
           scale() rotate() skew();
opacity: 0 to 1;
filter: blur() brightness() contrast();

/* Will trigger compositor layer */
will-change: transform, opacity;
```

### NEVER Animate These

```css
/* Triggers layout - SLOW */
width, height
top, right, bottom, left
margin, padding
font-size
border-width

/* Triggers paint - SLOW */
background-color, color
border-color
box-shadow
text-shadow
```

### Transform vs Position

```css
/* BAD - Triggers layout every frame */
.element {
  animation: moveLeft 1s;
}
@keyframes moveLeft {
  to { left: 100px; }
}

/* GOOD - GPU composited */
.element {
  animation: moveLeft 1s;
}
@keyframes moveLeft {
  to { transform: translateX(100px); }
}
```

---

## Quick Performance Wins

### 1. Lazy Load Below-Fold Content

```html
<!-- Native lazy loading -->
<img src="hero.jpg" alt="Hero" loading="eager">
<img src="feature.jpg" alt="Feature" loading="lazy">

<!-- Intersection Observer for components -->
<div class="lazy-section" data-component="heavy-animation">
  <!-- Loaded via JS when visible -->
</div>
```

### 2. Use content-visibility

```css
/* Skip rendering off-screen sections */
.section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;  /* Estimated height */
}
```

### 3. Contain Expensive Effects

```css
/* Isolate animated sections */
.animated-section {
  contain: layout style paint;
}

/* Full containment for cards */
.card {
  contain: strict;
}
```

### 4. Reduce Motion When Appropriate

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 5. Optimize Scroll Handlers

```javascript
// BAD - Fires on every scroll event
window.addEventListener('scroll', handleScroll);

// GOOD - Passive listener, no preventDefault
window.addEventListener('scroll', handleScroll, { passive: true });

// BETTER - Use ScrollTrigger (already optimized)
gsap.to('.element', {
  scrollTrigger: { /* ... */ }
});
```

---

## GSAP Performance

### Use gsap.context() for Cleanup

```javascript
// Prevents memory leaks
const ctx = gsap.context(() => {
  gsap.to('.element', { x: 100 });
  ScrollTrigger.create({ /* ... */ });
});

// On unmount
ctx.revert();
```

### Batch ScrollTrigger Updates

```javascript
// Process multiple items efficiently
ScrollTrigger.batch('.item', {
  onEnter: batch => gsap.to(batch, {
    opacity: 1,
    y: 0,
    stagger: 0.1
  })
});
```

### Use refreshPriority

```javascript
// Control refresh order
ScrollTrigger.create({
  trigger: '.section',
  refreshPriority: -1  // Refresh after others
});
```

### Lazy ScrollTriggers

```javascript
// Don't create all at once
const createTrigger = (element) => {
  ScrollTrigger.create({
    trigger: element,
    start: 'top 80%',
    onEnter: () => {
      // Create animation only when needed
      gsap.from(element, { opacity: 0, y: 50 });
    },
    once: true
  });
};

// Create triggers as needed
gsap.utils.toArray('.section').forEach(createTrigger);
```

---

## CSS Animation Performance

### Efficient Keyframes

```css
/* GOOD - Only compositor properties */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* BAD - Triggers layout */
@keyframes slideIn {
  from {
    opacity: 0;
    margin-top: 30px;
  }
  to {
    opacity: 1;
    margin-top: 0;
  }
}
```

### will-change Best Practices

```css
/* Apply just before animation */
.card {
  transition: transform 0.3s, opacity 0.3s;
}

.card:hover {
  will-change: transform;
}

/* Remove after animation */
.card.animating {
  will-change: transform, opacity;
}

/* Never do this globally */
/* * { will-change: transform; } NEVER! */
```

### Composite Layers

```css
/* Force new layer when needed */
.animated-element {
  transform: translateZ(0);  /* or translate3d(0,0,0) */
}

/* Better: Use will-change temporarily */
.animating {
  will-change: transform;
}
```

---

## Loading Strategy

### Critical Path

```html
<head>
  <!-- Critical CSS inline -->
  <style>/* Above-fold styles */</style>

  <!-- Preload critical assets -->
  <link rel="preload" href="hero.webp" as="image">
  <link rel="preload" href="font.woff2" as="font" crossorigin>

  <!-- Async non-critical CSS -->
  <link rel="stylesheet" href="full.css" media="print" onload="this.media='all'">
</head>

<body>
  <!-- Above-fold content -->

  <!-- Defer heavy scripts -->
  <script src="gsap.min.js" defer></script>
  <script src="app.js" defer></script>
</body>
```

### Dynamic Imports

```javascript
// Load GSAP plugins only when needed
const loadScrollTrigger = async () => {
  const { ScrollTrigger } = await import('gsap/ScrollTrigger');
  gsap.registerPlugin(ScrollTrigger);
  return ScrollTrigger;
};

// Load on interaction or visibility
const section = document.querySelector('.scroll-section');
const observer = new IntersectionObserver(async ([entry]) => {
  if (entry.isIntersecting) {
    await loadScrollTrigger();
    initScrollAnimations();
    observer.disconnect();
  }
});
observer.observe(section);
```

### Progressive Enhancement

```javascript
// Check for animation support
const supportsAnimation = 'animate' in document.documentElement;
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (supportsAnimation && !prefersReducedMotion) {
  // Load animation library
  import('./animations.js');
} else {
  // Show final states immediately
  document.querySelectorAll('.animated').forEach(el => {
    el.classList.add('animation-complete');
  });
}
```

---

## Memory Management

### Clean Up Animations

```javascript
// Store references for cleanup
const animations = [];
const scrollTriggers = [];

function initAnimations() {
  animations.push(
    gsap.to('.element', { x: 100 })
  );

  scrollTriggers.push(
    ScrollTrigger.create({ trigger: '.section' })
  );
}

function cleanup() {
  animations.forEach(anim => anim.kill());
  scrollTriggers.forEach(st => st.kill());
  animations.length = 0;
  scrollTriggers.length = 0;
}

// Or use gsap.context()
const ctx = gsap.context(() => {
  // All animations here
});

// Cleanup
ctx.revert();
```

### SplitText Cleanup

```javascript
const splits = [];

function initTextAnimations() {
  document.querySelectorAll('.split-text').forEach(el => {
    const split = new SplitText(el, { type: 'chars' });
    splits.push(split);

    gsap.from(split.chars, {
      opacity: 0,
      y: 20,
      stagger: 0.02
    });
  });
}

function cleanup() {
  splits.forEach(split => split.revert());
  splits.length = 0;
}
```

### Event Listener Cleanup

```javascript
// Use AbortController for easy cleanup
const controller = new AbortController();

window.addEventListener('resize', handleResize, {
  signal: controller.signal
});

window.addEventListener('scroll', handleScroll, {
  passive: true,
  signal: controller.signal
});

// Cleanup all at once
function cleanup() {
  controller.abort();
}
```

---

## Debugging Checklist

### Performance Issues

1. **Dropped frames?**
   - Check DevTools Performance panel
   - Look for long tasks (> 50ms)
   - Verify only compositor properties animated

2. **Slow initial load?**
   - Check Network waterfall
   - Verify critical path optimized
   - Audit bundle sizes

3. **Memory leaks?**
   - Check Memory panel over time
   - Verify cleanup on navigation
   - Watch for detached DOM nodes

4. **Layout thrashing?**
   - Look for forced reflows in Performance
   - Batch DOM reads/writes
   - Use transform instead of position

### Quick Checks

```javascript
// Log animation frame rate
let lastTime = performance.now();
let frameCount = 0;

function measureFPS() {
  frameCount++;
  const now = performance.now();
  if (now - lastTime >= 1000) {
    console.log('FPS:', frameCount);
    frameCount = 0;
    lastTime = now;
  }
  requestAnimationFrame(measureFPS);
}
measureFPS();
```

```javascript
// Detect layout thrashing
const originalGetComputedStyle = window.getComputedStyle;
window.getComputedStyle = function(...args) {
  console.trace('getComputedStyle called');
  return originalGetComputedStyle.apply(this, args);
};
```

See [debugging.md](references/debugging.md) for comprehensive debugging techniques.

---

## Resources

- [web.dev Performance](https://web.dev/performance/)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [GSAP Performance Tips](https://gsap.com/docs/v3/GSAP/gsap.ticker())
- [CSS Triggers](https://csstriggers.com/) - What properties trigger layout/paint
