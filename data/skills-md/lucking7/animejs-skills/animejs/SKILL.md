---
name: animejs
description: "Use when creating JavaScript animations with Anime.js v4, implementing web animations, or when user mentions anime.js/animejs. Triggers on v3 code symptoms: anime() instead of animate(), translateX instead of x, easeOutExpo instead of outExpo, anime.timeline() instead of createTimeline(). Also triggers on: CSS animation, SVG animation, scroll-driven animation, drag interaction, text splitting, layout FLIP, spring physics, stagger patterns in JavaScript."
---

# Anime.js v4

Modern JavaScript animation library. V4 is a complete rewrite — `animate()` not `anime()`.

## Installation

```bash
npm install animejs
```
```javascript
import { animate, createTimeline, stagger, utils, onScroll, createDraggable, splitText, createScope, createLayout, waapi, svg, eases, cubicBezier, spring, engine } from 'animejs';
```

CDN: `<script src="https://cdn.jsdelivr.net/npm/animejs@4/dist/anime.min.js"></script>` → `const { animate } = anime;`

## V3 → V4 Migration (Critical)

**If you see ANY V3 pattern, the code MUST be migrated.**

| V3 (Wrong) | V4 (Correct) | Notes |
|------------|--------------|-------|
| `anime({ targets: '.el', ... })` | `animate('.el', { ... })` | Targets = first arg |
| `anime.timeline()` | `createTimeline()` | Named import |
| `anime.stagger(100)` | `stagger(100)` | Named import |
| `anime.set()` / `anime.get()` | `utils.set()` / `utils.get()` | On utils object |
| `anime.remove(targets)` | `utils.remove(targets)` | On utils object |
| `anime.random(0, 100)` | `utils.random(0, 100)` | On utils object |
| `translateX` / `translateY` / `translateZ` | `x` / `y` / `z` | Shorthand transforms |
| `easing: 'easeOutExpo'` | `ease: 'outExpo'` | Param renamed, drop "ease" prefix |
| `direction: 'alternate'` | `alternate: true` | Boolean property |
| `direction: 'reverse'` | `reversed: true` | Boolean property |
| `import anime from 'animejs'` | `import { animate } from 'animejs'` | Named imports only |
| Timeline `.add({ targets })` | `.add(targets, params, pos)` | Targets = first arg of `.add()` |
| `spring('mass:1')` | `spring({ mass: 1, stiffness: 200 })` | Object params, not string |
| `cubicBezier('0.7,0.1,0.5,0.9')` | `cubicBezier(.7, .1, .5, .9)` | Numeric args |

### V4 Easing Names

Drop the "ease" prefix: `easeOutExpo` → `outExpo`, `easeInOutQuad` → `inOutQuad`. `linear` unchanged. Full list → [references/easings.md](references/easings.md).

## API Reference

Load specific reference file for detailed params, methods, callbacks, and examples.

| Need | API | Reference |
|------|-----|-----------|
| Animate elements | `animate(targets, params)` | [animation.md](references/animation.md) |
| Reactive animatable values | `createAnimatable(targets, params)` | [animatable.md](references/animatable.md) |
| Sequence animations | `createTimeline(params)` | [timeline.md](references/timeline.md) |
| Frame loops / countdowns | `createTimer(params)` | [timer.md](references/timer.md) |
| Drag interactions | `createDraggable(targets, params)` | [draggable.md](references/draggable.md) |
| Scroll-driven animations | `onScroll(params)` | [events.md](references/events.md) |
| Scope, media queries, cleanup | `createScope(params)` | [scope.md](references/scope.md) |
| Text character/word splitting | `splitText(targets, params)` | [text.md](references/text.md) |
| FLIP layout animations | `createLayout(params)` | [layout.md](references/layout.md) |
| SVG morph / draw / motion path | `svg.morphTo()`, `svg.drawLine()` | [svg.md](references/svg.md) |
| Lightweight WAAPI (3KB) | `waapi.animate(targets, params)` | [web-animation-api.md](references/web-animation-api.md) |
| Easing functions, spring, bezier | `eases`, `spring()`, `cubicBezier()` | [easings.md](references/easings.md) |
| Stagger, get/set, math helpers | `utils`, `stagger()` | [utilities.md](references/utilities.md) |
| Global clock, fps, suspend | `engine` | [engine.md](references/engine.md) |
| Setup, React integration | Getting started guide | [getting-started.md](references/getting-started.md) |

## Common Patterns

### Staggered entrance

```javascript
import { animate, stagger } from 'animejs';
animate('.item', {
  y: [-20, 0], opacity: [0, 1],
  delay: stagger(80, { from: 'center' }),
  ease: 'outExpo', duration: 600,
});
```

### Timeline sequence

```javascript
import { createTimeline } from 'animejs';
const tl = createTimeline({ defaults: { duration: 750, ease: 'outExpo' } });
tl.add('.a', { x: '15rem' }, 0)
  .add('.b', { x: '15rem' }, '<')         // starts with previous
  .add('.c', { x: '15rem' }, '<-=500');    // 500ms before previous starts
```

Time positions: `0` (absolute ms), `'<'` (prev start), `'<<'` (prev end), `'>>'` (prev end), `'<+=200'` / `'<-=200'` (offset from prev start), `'>>=200'` (offset from prev end), `'label'` / `'label+=500'`.

### Scroll-linked animation

```javascript
import { animate, onScroll } from 'animejs';
animate('.progress', {
  scaleX: [0, 1],
  autoplay: onScroll({ target: '.content', enter: 'top bottom', leave: 'bottom top' })
});
```

## Red Flags — V3 Code Detected

Stop and migrate if you see ANY of these:

- `anime({` or `anime.timeline()` — V3 constructor
- `translateX`, `translateY`, `translateZ` — use `x`, `y`, `z`
- `easeIn*`, `easeOut*`, `easeInOut*` prefix — drop "ease"
- `anime.stagger()`, `anime.set()`, `anime.get()` — named imports / utils
- `direction: 'alternate'` / `direction: 'reverse'` — use booleans
- `easing:` parameter — V4 uses `ease:`
- `import anime from 'animejs'` — use named imports `{ animate }`
- `"anime is not a function"` / `"anime is not defined"` — V4 has no default export
- Animating `width`/`height` directly — use `scaleX`/`scaleY` or `x`/`y` for performance
- Missing `autoplay` for scroll — pass `autoplay: onScroll({...})`
- Not cleaning up in React — use `createScope()` + `.revert()` in cleanup
