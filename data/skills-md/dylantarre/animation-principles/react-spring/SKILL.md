---
name: react-spring
description: Use when implementing Disney's 12 animation principles with React Spring's physics-based animations
---

# React Spring Animation Principles

Implement all 12 Disney animation principles using React Spring's spring physics system.

## 1. Squash and Stretch

```jsx
const [springs, api] = useSpring(() => ({
  scaleX: 1,
  scaleY: 1,
  config: { tension: 300, friction: 10 }
}));

api.start({ scaleX: 1.2, scaleY: 0.8 });
<animated.div style={springs} />
```

## 2. Anticipation

```jsx
const [props, api] = useSpring(() => ({ y: 0, scaleY: 1 }));

const jump = async () => {
  await api.start({ y: 10, scaleY: 0.9 }); // wind up
  api.start({ y: -200, config: { tension: 200 } }); // action
};
```

## 3. Staging

```jsx
const bgSpring = useSpring({ filter: 'blur(3px)', opacity: 0.6 });
const heroSpring = useSpring({ scale: 1.1, zIndex: 10 });
```

## 4. Straight Ahead / Pose to Pose

```jsx
const [props] = useSpring(() => ({
  from: { x: 0, y: 0 },
  to: [
    { x: 100, y: -50 },
    { x: 200, y: 0 },
    { x: 300, y: -30 }
  ]
}));
```

## 5. Follow Through and Overlapping Action

```jsx
const bodySpring = useSpring({ x: 200 });
const hairSpring = useSpring({ x: 200, delay: 50 });
const capeSpring = useSpring({ x: 200, delay: 100, config: { friction: 15 } });
```

## 6. Slow In and Slow Out

```jsx
const spring = useSpring({
  x: 300,
  config: {
    tension: 170,
    friction: 26 // balanced = smooth in/out
  }
});
// High tension + low friction = fast
// Low tension + high friction = slow
```

## 7. Arc

```jsx
const [props] = useSpring(() => ({
  to: async (next) => {
    await next({ x: 100, y: -100 });
    await next({ x: 200, y: 0 });
  },
  config: { tension: 200, friction: 20 }
}));
```

## 8. Secondary Action

```jsx
const buttonSpring = useSpring({ scale: hover ? 1.05 : 1 });
const iconSpring = useSpring({
  rotate: hover ? 15 : 0,
  delay: 50
});
```

## 9. Timing

```jsx
const configs = {
  fast: { tension: 400, friction: 30 },
  normal: { tension: 170, friction: 26 },
  slow: { tension: 100, friction: 40 },
  wobbly: { tension: 180, friction: 12 }
};
// Or use presets: config.gentle, config.stiff, config.slow
```

## 10. Exaggeration

```jsx
const spring = useSpring({
  scale: 1.5,
  rotate: 720,
  config: { tension: 200, friction: 8 } // low friction = overshoot
});
```

## 11. Solid Drawing

```jsx
const spring = useSpring({
  transform: 'perspective(1000px) rotateX(45deg) rotateY(30deg)'
});
```

## 12. Appeal

```jsx
const cardSpring = useSpring({
  scale: hover ? 1.02 : 1,
  boxShadow: hover
    ? '0 20px 40px rgba(0,0,0,0.2)'
    : '0 5px 15px rgba(0,0,0,0.1)',
  config: config.gentle
});
```

## useTrail for Stagger

```jsx
const trail = useTrail(items.length, {
  opacity: show ? 1 : 0,
  y: show ? 0 : 20,
  config: { tension: 200, friction: 20 }
});

trail.map((props, i) => <animated.div style={props}>{items[i]}</animated.div>)
```

## Key React Spring Features

- `useSpring` - Single animation
- `useSprings` - Multiple springs
- `useTrail` - Staggered animations
- `useChain` - Sequence animations
- `useTransition` - Mount/unmount animations
- `config` presets - `gentle`, `stiff`, `slow`, `molasses`
- Physics-based: `tension`, `friction`, `mass`, `velocity`
