---
name: popmotion
description: Use when implementing Disney's 12 animation principles with Popmotion's functional animation library
---

# Popmotion Animation Principles

Implement all 12 Disney animation principles using Popmotion's composable animation functions.

## 1. Squash and Stretch

```javascript
import { animate } from "popmotion";

animate({
  from: { scaleX: 1, scaleY: 1 },
  to: { scaleX: 1.2, scaleY: 0.8 },
  duration: 150,
  onUpdate: ({ scaleX, scaleY }) => {
    element.style.transform = `scaleX(${scaleX}) scaleY(${scaleY})`;
  }
});
```

## 2. Anticipation

```javascript
// Wind up then action
animate({
  from: 0,
  to: 10,
  duration: 200,
  onUpdate: v => element.style.transform = `translateY(${v}px) scaleY(0.9)`,
  onComplete: () => {
    animate({
      from: 10,
      to: -200,
      duration: 400,
      ease: easeOut,
      onUpdate: v => element.style.transform = `translateY(${v}px)`
    });
  }
});
```

## 3. Staging

```javascript
animate({
  from: 1,
  to: 0.6,
  onUpdate: v => bg.style.opacity = v
});
animate({
  from: 1,
  to: 1.1,
  onUpdate: v => hero.style.transform = `scale(${v})`
});
```

## 4. Straight Ahead / Pose to Pose

```javascript
import { keyframes } from "popmotion";

keyframes({
  values: [
    { x: 0, y: 0 },
    { x: 100, y: -50 },
    { x: 200, y: 0 },
    { x: 300, y: -30 }
  ],
  duration: 1000,
  onUpdate: ({ x, y }) => {
    element.style.transform = `translate(${x}px, ${y}px)`;
  }
});
```

## 5. Follow Through and Overlapping Action

```javascript
animate({ from: 0, to: 200, duration: 500,
  onUpdate: v => body.style.transform = `translateX(${v}px)` });

animate({ from: 0, to: 200, duration: 500, elapsed: -50, // delay
  onUpdate: v => hair.style.transform = `translateX(${v}px)` });

animate({ from: 0, to: 200, duration: 600, elapsed: -100,
  onUpdate: v => cape.style.transform = `translateX(${v}px)` });
```

## 6. Slow In and Slow Out

```javascript
import { animate, easeInOut, easeIn, easeOut } from "popmotion";

animate({
  from: 0,
  to: 300,
  duration: 600,
  ease: easeInOut,
  onUpdate: v => element.style.transform = `translateX(${v}px)`
});
```

## 7. Arc

```javascript
keyframes({
  values: [
    { x: 0, y: 0 },
    { x: 100, y: -100 },
    { x: 200, y: 0 }
  ],
  duration: 1000,
  ease: easeInOut,
  onUpdate: ({ x, y }) => {
    element.style.transform = `translate(${x}px, ${y}px)`;
  }
});
```

## 8. Secondary Action

```javascript
// Primary action triggers secondary
animate({
  from: 1, to: 1.1, duration: 200,
  onUpdate: v => button.style.transform = `scale(${v})`,
  onComplete: () => {
    animate({
      from: 0, to: 15, duration: 150,
      onUpdate: v => icon.style.transform = `rotate(${v}deg)`
    });
  }
});
```

## 9. Timing

```javascript
import { spring } from "popmotion";

// Fast
animate({ from: 0, to: 100, duration: 150 });

// Spring physics
spring({
  from: 0,
  to: 100,
  stiffness: 300,
  damping: 20,
  onUpdate: v => element.style.transform = `translateX(${v}px)`
});

// Slow
animate({ from: 0, to: 100, duration: 800, ease: easeOut });
```

## 10. Exaggeration

```javascript
spring({
  from: { scale: 1, rotate: 0 },
  to: { scale: 1.5, rotate: 720 },
  stiffness: 200,
  damping: 10, // low = overshoot
  onUpdate: ({ scale, rotate }) => {
    element.style.transform = `scale(${scale}) rotate(${rotate}deg)`;
  }
});
```

## 11. Solid Drawing

```javascript
animate({
  from: { rotateX: 0, rotateY: 0 },
  to: { rotateX: 45, rotateY: 30 },
  duration: 500,
  onUpdate: ({ rotateX, rotateY }) => {
    box.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
  }
});
```

## 12. Appeal

```javascript
animate({
  from: 1,
  to: 1.02,
  duration: 300,
  ease: easeOut,
  onUpdate: v => {
    card.style.transform = `scale(${v})`;
    card.style.boxShadow = `0 ${20*v}px 40px rgba(0,0,0,${0.2*v})`;
  }
});
```

## Key Popmotion Features

- `animate()` - Tween animations
- `spring()` - Physics-based spring
- `keyframes()` - Multi-step animations
- `decay()` - Momentum/inertia
- `easeIn`, `easeOut`, `easeInOut` - Easing functions
- Composable functions - mix and pipe
- Framework agnostic
- Powers Framer Motion under the hood
