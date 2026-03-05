---
name: motion-one
description: Use when implementing Disney's 12 animation principles with Motion One (modern, lightweight animation library)
---

# Motion One Animation Principles

Implement all 12 Disney animation principles using Motion One's performant Web Animations API wrapper.

## 1. Squash and Stretch

```javascript
import { animate } from "motion";

animate(".ball",
  { scaleX: [1, 1.2, 1], scaleY: [1, 0.8, 1] },
  { duration: 0.3, easing: "ease-in-out" }
);
```

## 2. Anticipation

```javascript
import { timeline } from "motion";

timeline([
  [".character", { y: 10, scaleY: 0.9 }, { duration: 0.2 }],
  [".character", { y: -200 }, { duration: 0.4, easing: "ease-out" }]
]);
```

## 3. Staging

```javascript
animate(".background", { filter: "blur(3px)", opacity: 0.6 });
animate(".hero", { scale: 1.1 });
```

## 4. Straight Ahead / Pose to Pose

```javascript
animate(".element", {
  x: [0, 100, 200, 300],
  y: [0, -50, 0, -30]
}, { duration: 1 });
```

## 5. Follow Through and Overlapping Action

```javascript
timeline([
  [".body", { x: 200 }, { duration: 0.5 }],
  [".hair", { x: 200 }, { duration: 0.5, at: "-0.45" }],
  [".cape", { x: 200 }, { duration: 0.6, at: "-0.5" }]
]);
```

## 6. Slow In and Slow Out

```javascript
animate(".element", { x: 300 }, {
  duration: 0.6,
  easing: [0.42, 0, 0.58, 1] // cubic-bezier ease-in-out
});
// Or: "ease-in", "ease-out", "ease-in-out"
// Or spring: { easing: spring({ stiffness: 100, damping: 15 }) }
```

## 7. Arc

```javascript
animate(".ball", {
  x: [0, 100, 200],
  y: [0, -100, 0]
}, { duration: 1, easing: "ease-in-out" });

// Or with offset path
animate(".element", {
  offsetDistance: ["0%", "100%"]
}, { duration: 1 });
// CSS: offset-path: path('M0,100 Q100,0 200,100');
```

## 8. Secondary Action

```javascript
const button = document.querySelector(".button");
button.addEventListener("mouseenter", () => {
  animate(button, { scale: 1.05 }, { duration: 0.2 });
  animate(".icon", { rotate: 15 }, { duration: 0.15 });
});
```

## 9. Timing

```javascript
import { spring } from "motion";

// Fast snap
animate(".fast", { x: 100 }, { duration: 0.15 });

// Spring physics
animate(".spring", { x: 100 }, {
  easing: spring({ stiffness: 300, damping: 20 })
});

// Slow dramatic
animate(".slow", { x: 100 }, { duration: 0.8, easing: "ease-out" });
```

## 10. Exaggeration

```javascript
import { spring } from "motion";

animate(".element", { scale: 1.5, rotate: 720 }, {
  easing: spring({ stiffness: 200, damping: 10 }) // overshoot
});
```

## 11. Solid Drawing

```javascript
animate(".box", {
  rotateX: 45,
  rotateY: 30
}, { duration: 0.5 });
// Set perspective in CSS: perspective: 1000px;
```

## 12. Appeal

```javascript
animate(".card", {
  scale: 1.02,
  boxShadow: "0 20px 40px rgba(0,0,0,0.2)"
}, { duration: 0.3, easing: "ease-out" });
```

## Stagger Animation

```javascript
import { stagger } from "motion";

animate(".item",
  { opacity: [0, 1], y: [20, 0] },
  { delay: stagger(0.1) }
);
```

## Scroll Animations

```javascript
import { scroll, animate } from "motion";

scroll(
  animate(".parallax", { y: [0, 100] }),
  { target: document.querySelector(".container") }
);
```

## In-View Animations

```javascript
import { inView } from "motion";

inView(".section", ({ target }) => {
  animate(target, { opacity: 1, y: 0 }, { duration: 0.5 });
});
```

## Key Motion One Features

- `animate()` - Single animation
- `timeline()` - Sequence with `at` positioning
- `stagger()` - Offset delays
- `spring()` - Physics-based easing
- `scroll()` - Scroll-linked animations
- `inView()` - Intersection observer wrapper
- Uses Web Animations API (hardware accelerated)
- Tiny bundle size (~3kb)
