---
name: motion
description: Motion animation library for JavaScript, React and Vue. Use when creating animations, gestures, layout transitions, scroll-linked effects, or working with motion values and animation controls.
metadata:
  author: Hairyf
  version: "2026.1.29"
  source: Generated from https://github.com/motiondivision/motion, scripts located at https://github.com/antfu/skills
---

Motion is an open-source animation library for JavaScript, React, and Vue. It provides a simple API with first-class support for multiple platforms, a hybrid animation engine combining JavaScript with native browser APIs for 120fps GPU-accelerated animations, and production-ready features including TypeScript support, extensive test suite, tree-shakable builds, and a tiny footprint. Batteries included: gestures, springs, layout transitions, scroll-linked effects, and timelines.

> The skill is based on Motion v12.29.2, generated at 2026-01-29.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Motion Components | Basic motion components (motion.div, motion.svg, etc.) | [core-components](references/core-components.md) |
| Basic Animation | animate prop, initial, while states | [core-animation](references/core-animation.md) |
| Variants | Declarative animation variants and orchestration | [core-variants](references/core-variants.md) |
| Transitions | Animation timing, easing, spring physics | [core-transitions](references/core-transitions.md) |

## Motion Values

| Topic | Description | Reference |
|-------|-------------|-----------|
| useMotionValue | Create and use motion values for reactive animations | [values-motion-value](references/values-motion-value.md) |
| useSpring | Spring-based motion values with physics | [values-spring](references/values-spring.md) |
| useTransform | Transform motion values with functions | [values-transform](references/values-transform.md) |
| useScroll | Scroll-linked motion values and animations | [values-scroll](references/values-scroll.md) |
| useVelocity | Access velocity of motion values | [values-velocity](references/values-velocity.md) |
| useTime | Time-based motion values | [values-time](references/values-time.md) |

## Gestures

| Topic | Description | Reference |
|-------|-------------|-----------|
| Drag | Drag gestures with constraints and controls | [gestures-drag](references/gestures-drag.md) |
| Pan | Pan gestures for touch and pointer events | [gestures-pan](references/gestures-pan.md) |
| Tap & Press | Tap and press gesture handlers | [gestures-tap-press](references/gestures-tap-press.md) |
| Hover & Focus | Hover and focus state animations | [gestures-hover-focus](references/gestures-hover-focus.md) |

## Layout Animations

| Topic | Description | Reference |
|-------|-------------|-----------|
| AnimatePresence | Animate components entering and exiting | [layout-animate-presence](references/layout-animate-presence.md) |
| LayoutGroup | Coordinate layout animations across components | [layout-group](references/layout-group.md) |
| Layout Animations | Automatic layout animations with layoutId | [layout-animations](references/layout-animations.md) |
| Reorder | Drag-to-reorder with layout animations | [layout-reorder](references/layout-reorder.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Animation Controls | Programmatic animation control with useAnimation | [advanced-animation-controls](references/advanced-animation-controls.md) |
| useAnimate | Imperative animation API | [advanced-use-animate](references/advanced-use-animate.md) |
| LazyMotion | Code-split animations for better performance | [advanced-lazy-motion](references/advanced-lazy-motion.md) |
| MotionConfig | Global configuration and reduced motion | [advanced-motion-config](references/advanced-motion-config.md) |
| Scroll Animations | Scroll-linked animations and parallax effects | [advanced-scroll-animations](references/advanced-scroll-animations.md) |
