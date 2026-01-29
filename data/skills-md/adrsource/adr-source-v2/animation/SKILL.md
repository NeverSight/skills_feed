---
name: animation
description: Implement animations using the Motion library. Use when adding motion, transitions, gestures, scroll effects, or interactive animations to components. Triggered by implementation requests, not conceptual discussions.
allowed-tools: [Read, Edit, Grep, Glob, Bash, Write]
---

# Animation Implementation with Motion

Use the Motion library (https://motion.dev) for all animation work.

## Quick Start

**React (Primary):**

```jsx
import { motion } from "motion/react"

// Basic animation
<motion.div animate={{ opacity: 1, y: 0 }} />

// With transition config
<motion.div
  animate={{ x: 100 }}
  transition={{ type: "spring", stiffness: 100 }}
/>
```

## Core Patterns

### 1. Spring Physics (Preferred)

```jsx
<motion.div
  animate={{ scale: 1 }}
  transition={{
    type: 'spring',
    stiffness: 260,
    damping: 20,
  }}
/>
```

Spring presets:

- **Gentle**: `stiffness: 120, damping: 14`
- **Wobbly**: `stiffness: 180, damping: 12`
- **Stiff**: `stiffness: 300, damping: 20`

### 2. Gesture Interactions

```jsx
<motion.div
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  drag="x"
  dragConstraints={{ left: -100, right: 100 }}
/>
```

### 3. Layout Animations

```jsx
<motion.div layout>{/* Content that changes position/size */}</motion.div>
```

### 4. Scroll-Linked Effects

```jsx
import { useScroll, useTransform } from "motion/react"

const { scrollYProgress } = useScroll()
const opacity = useTransform(scrollYProgress, [0, 1], [1, 0])

<motion.div style={{ opacity }} />
```

### 5. Stagger Children

```jsx
<motion.ul
  variants={{
    visible: { transition: { staggerChildren: 0.07 } },
  }}
>
  {items.map((item) => (
    <motion.li
      key={item}
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 },
      }}
    />
  ))}
</motion.ul>
```

### 6. Enter/Exit Animations

```jsx
import { AnimatePresence } from 'motion/react';

<AnimatePresence>
  {show && <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />}
</AnimatePresence>;
```

## Animation Properties

**Transform** (GPU-accelerated, performant):

- `x, y, z` - Translate
- `scale, scaleX, scaleY` - Scale
- `rotate, rotateX, rotateY, rotateZ` - Rotation
- `skew, skewX, skewY` - Skew

**Visual** (use sparingly, can affect performance):

- `opacity`
- `background, backgroundColor`
- `color`
- `borderRadius`

**SVG-specific**:

- `pathLength` - For path drawing animations
- `pathOffset` - Offset the path
- `pathSpacing` - Spacing between dashes

## Accessibility

Always respect user preferences:

```jsx
<motion.div
  animate={{ x: 100 }}
  transition={{
    type: 'spring',
    // Disables animation if user prefers reduced motion
    duration: 0,
  }}
/>
```

Motion automatically handles `prefers-reduced-motion`. Springs become instant transitions.

## Performance Tips

1. **Animate transforms/opacity only** when possible (GPU-accelerated)
2. **Use `layout` prop** instead of animating width/height manually
3. **Avoid animating** during scroll when possible
4. **Use `will-change: transform`** for complex animations (Motion handles this)
5. **Limit simultaneous animations** - stagger instead of all-at-once

## Design Principles (Brief)

### When to Animate

- State transitions (loading → success)
- Spatial changes (entering/exiting view)
- Drawing attention (sparingly)
- Confirming user action

### When NOT to Animate

- Repeated actions after first occurrence
- Performance-critical paths
- User-controlled scrolling
- Every single interaction (restraint matters)

### Timing Guidelines

- **Micro-interactions**: 150-250ms
- **Panel/modal transitions**: 200-300ms
- **Page transitions**: 300-500ms
- **Springs**: Let physics determine duration

### Spring vs Duration

- **Use springs for**: Interactive elements, gestures, layout changes
- **Use duration for**: Intentional sequences, choreography, loaders

See `principles.md` for detailed animation philosophy.

## Common Patterns

**Loading state:**

```jsx
<motion.div
  animate={{ rotate: 360 }}
  transition={{
    repeat: Infinity,
    duration: 1,
    ease: 'linear',
  }}
/>
```

**Toast notification:**

```jsx
<motion.div
  initial={{ x: 400, opacity: 0 }}
  animate={{ x: 0, opacity: 1 }}
  exit={{ x: 400, opacity: 0 }}
  transition={{ type: 'spring', stiffness: 300, damping: 30 }}
/>
```

**Drawer:**

```jsx
<motion.div
  initial={{ x: '-100%' }}
  animate={{ x: 0 }}
  exit={{ x: '-100%' }}
  transition={{ type: 'spring', damping: 25 }}
/>
```

**Accordion:**

```jsx
<motion.div
  animate={{ height: isOpen ? 'auto' : 0 }}
  transition={{ type: 'spring', bounce: 0 }}
  style={{ overflow: 'hidden' }}
/>
```

## Resources

- **Motion Docs**: https://motion.dev/docs/react
- **Motion Examples**: https://motion.dev/examples (100+ free examples)
- **GitHub Repository**: https://github.com/motiondivision/motion
- **Extended resources**: See `resources.md` for curated animation.dev lessons and vault

## Quick Troubleshooting

**Animation not running?**

- Check if element is conditionally rendered (use AnimatePresence)
- Verify target values are different from initial values
- Check for CSS that might override (e.g., `!important`)

**Performance issues?**

- Stick to transforms and opacity
- Use `layout` prop instead of animating dimensions
- Check browser DevTools Performance tab

**Layout animations flickering?**

- Ensure parent has `position: relative`
- Add `layout` to both parent and child if needed
- Check for conflicting CSS transitions

## Notes

- Motion is MIT licensed, production-ready
- Hybrid engine: 120fps, GPU-accelerated
- TypeScript support built-in
- Tree-shakable for optimal bundle size
- Works with React 18+ (including Suspense)
