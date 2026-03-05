---
name: gsap-greensock
description: Use when implementing Disney's 12 animation principles with GSAP (GreenSock Animation Platform)
---

# GSAP Animation Principles

Implement all 12 Disney animation principles using GSAP's powerful timeline and tween system.

## 1. Squash and Stretch

```javascript
gsap.to(".ball", {
  scaleX: 1.2,
  scaleY: 0.8,
  yoyo: true,
  repeat: 1,
  duration: 0.15,
  ease: "power2.inOut"
});
```

## 2. Anticipation

```javascript
const tl = gsap.timeline();
tl.to(".character", { y: 20, scaleY: 0.9, duration: 0.2 }) // wind up
  .to(".character", { y: -200, duration: 0.4, ease: "power2.out" }); // action
```

## 3. Staging

```javascript
gsap.to(".background", { filter: "blur(3px)", opacity: 0.6 });
gsap.to(".hero", { scale: 1.1, zIndex: 10 });
```

## 4. Straight Ahead / Pose to Pose

```javascript
// Pose to pose with explicit keyframes
gsap.to(".sprite", {
  keyframes: [
    { x: 0, y: 0 },
    { x: 100, y: -50 },
    { x: 200, y: 0 },
    { x: 300, y: -30 }
  ],
  duration: 1
});
```

## 5. Follow Through and Overlapping Action

```javascript
const tl = gsap.timeline();
tl.to(".body", { x: 200, duration: 0.5 })
  .to(".hair", { x: 200, duration: 0.5 }, "-=0.4")  // overlaps
  .to(".cape", { x: 200, duration: 0.6 }, "-=0.45"); // more drag
```

## 6. Slow In and Slow Out

```javascript
gsap.to(".element", {
  x: 300,
  duration: 0.6,
  ease: "power2.inOut" // slow in and out
});
// Other eases: "power3.in", "power3.out", "elastic.out"
```

## 7. Arc

```javascript
gsap.to(".ball", {
  motionPath: {
    path: [{ x: 0, y: 0 }, { x: 100, y: -100 }, { x: 200, y: 0 }],
    curviness: 1.5
  },
  duration: 1
});
```

## 8. Secondary Action

```javascript
const tl = gsap.timeline();
tl.to(".button", { scale: 1.1, duration: 0.2 })
  .to(".icon", { rotation: 15, duration: 0.15 }, "<") // same time
  .to(".particles", { opacity: 1, stagger: 0.05 }, "<0.1");
```

## 9. Timing

```javascript
// Fast snap
gsap.to(".fast", { x: 100, duration: 0.15 });
// Gentle float
gsap.to(".slow", { y: -20, duration: 2, ease: "sine.inOut", yoyo: true, repeat: -1 });
```

## 10. Exaggeration

```javascript
gsap.to(".element", {
  scale: 1.5,        // exaggerated scale
  rotation: 720,     // multiple spins
  duration: 0.8,
  ease: "back.out(2)" // overshoot
});
```

## 11. Solid Drawing

```javascript
gsap.to(".box", {
  rotationX: 45,
  rotationY: 30,
  transformPerspective: 1000,
  duration: 0.5
});
```

## 12. Appeal

```javascript
gsap.to(".card", {
  scale: 1.02,
  boxShadow: "0 20px 40px rgba(0,0,0,0.2)",
  duration: 0.3,
  ease: "power1.out"
});
```

## GSAP Timeline Pattern

```javascript
const masterTL = gsap.timeline({ defaults: { ease: "power2.out" }});
masterTL
  .add(anticipation())
  .add(mainAction())
  .add(followThrough());
```

## Key GSAP Features

- `gsap.timeline()` - Sequence animations
- `ease` - 30+ built-in easing functions
- `stagger` - Offset multiple elements
- `motionPath` - Arc and path animations
- `yoyo` / `repeat` - Loop control
- `"<"` / `"-=0.2"` - Position parameter for overlap
