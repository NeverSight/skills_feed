---
name: animation-performance
description: Provides React Native Reanimated, React Native Worklets, React Native Gesture Handler performance optimization guidelines for smooth animations. Applies to tasks involving shared values, worklets, frame callbacks, gesture handlers, animated styles, re-renders, or debugging animation jank and frame drops.
---

# Animation Performance Tips

## Overview

Performance optimization guide for React Native Reanimated animations, covering shared values, worklets, memoization, and rendering optimizations. These guidelines ensure buttery smooth animations at 60fps.

## When to Apply

Reference these guidelines when:
- Debugging janky or stuttering animations
- Optimizing animation performance (FPS drops)
- Working with shared values and worklets
- Implementing gesture handlers
- Optimizing animated lists and scroll handlers
- Reviewing Reanimated code for performance issues

## Priority-Ordered Guidelines

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Shared Values Usage | CRITICAL | `shared-values-*` |
| 2 | Re-renders | CRITICAL | `re-renders-*` |
| 3 | Memoization | HIGH | `memoization-*` |
| 4 | Animation Calculations | HIGH | `calculations-*` |
| 5 | Layout vs Transform | HIGH | `layout-*` |
| 6 | Reactions | HIGH | `reactions-*` |
| 7 | Hooks Selection | HIGH | `hooks-*` |
| 8 | Animation Lifecycle | MEDIUM | `animations-*` |
| 9 | Component Limits | MEDIUM | `limits-*` |
| 10 | Scroll Optimization | MEDIUM | `scroll-*` |

## Quick Reference

### Critical: Shared Values Usage

**Common mistakes:**
- Reading shared values on JS thread (causes thread blocking)
- Accessing shared values during render (violates Rules of React)
- Using component state for animation values (triggers re-renders)

**Quick fixes:**
- Read shared values only in worklets (`useAnimatedStyle`, `useDerivedValue`) - see `shared-values-read-in-worklets.md`
- Access shared values in `useEffect` or callbacks, not during render - see `shared-values-during-render.md`
- Use `useSharedValue` instead of `useState` for animation values - see `re-renders-use-shared-values.md`
- Track animation state with `useRef` instead of reading shared values - see `shared-values-track-state-with-ref.md`
- Initialize with simple values, compute complex ones in worklets - see `shared-values-initialization.md`

### Critical: Re-renders

**Common fixes:**
- Use shared values instead of component state for animations
- Memoize animation objects outside component or with constants
- Memoize frame callbacks with `useCallback`
- Memoize gesture objects with `useMemo`

### High: Animation Calculations

**Common fixes:**
- Use `useDerivedValue` for expensive calculations - see `calculations-use-derived-value.md`
- Avoid conditional logic in worklets - see `calculations-avoid-conditionals.md`
- Use `clamp` instead of manual Math.min/max - see `calculations-use-clamp.md`
- Batch updates with `scheduleOnUI` - see `calculations-batch-with-schedule-on-ui.md`
- Prefer transform properties over layout properties - see `layout-prefer-transform.md`
- Choose the right hook (`useAnimatedProps` vs `useAnimatedStyle`) - see `hooks-choose-animated-props.md`
- Optimize `useAnimatedReaction` dependencies - see `reactions-optimize-dependencies.md`
- Cancel animations properly before starting new ones - see `animations-cancel-properly.md`

## References

Full documentation with code examples in `references/`:

### Shared Values (`shared-values-*`)

| File | Impact | Description |
|------|--------|-------------|
| `shared-values-read-in-worklets.md` | CRITICAL | Read shared values only in worklets, not on JS thread |
| `shared-values-during-render.md` | CRITICAL | Don't read/modify shared values during render |
| `shared-values-track-state-with-ref.md` | HIGH | Track animation state with useRef instead of reading shared values |
| `shared-values-initialization.md` | HIGH | Avoid expensive initial values, use simple primitives |

### Re-renders (`re-renders-*`)

| File | Impact | Description |
|------|--------|-------------|
| `re-renders-use-shared-values.md` | CRITICAL | Use shared values instead of component state for animations |

### Memoization (`memoization-*`)

| File | Impact | Description |
|------|--------|-------------|
| `memoization-animations.md` | HIGH | Memoize animation objects to prevent recreation |
| `memoization-frame-callbacks.md` | HIGH | Memoize frame callbacks with useCallback |
| `memoization-gesture-objects.md` | HIGH | Memoize gesture objects with useMemo |

### Calculations (`calculations-*`)

| File | Impact | Description |
|------|--------|-------------|
| `calculations-use-derived-value.md` | HIGH | Use useDerivedValue to optimize useAnimatedStyle calculations |
| `calculations-avoid-conditionals.md` | HIGH | Minimize conditional logic in worklets, use useDerivedValue |
| `calculations-use-clamp.md` | HIGH | Use clamp instead of manual Math.min/max in worklets |
| `calculations-batch-with-schedule-on-ui.md` | HIGH | Batch shared value updates with scheduleOnUI |

### Layout (`layout-*`)

| File | Impact | Description |
|------|--------|-------------|
| `layout-prefer-transform.md` | HIGH | Prefer transform over layout properties |

### Reactions (`reactions-*`)

| File | Impact | Description |
|------|--------|-------------|
| `reactions-optimize-dependencies.md` | HIGH | Avoid unnecessary reactions, optimize dependency tracking |

### Hooks (`hooks-*`)

| File | Impact | Description |
|------|--------|-------------|
| `hooks-choose-animated-props.md` | HIGH | Choose useAnimatedProps vs useAnimatedStyle correctly |

### Animations (`animations-*`)

| File | Impact | Description |
|------|--------|-------------|
| `animations-cancel-properly.md` | MEDIUM | Cancel running animations before starting new ones |

### Limits (`limits-*`)

| File | Impact | Description |
|------|--------|-------------|
| `limits-animated-components.md` | MEDIUM | Limit number of simultaneously animated components |

### Scroll (`scroll-*`)

| File | Impact | Description |
|------|--------|-------------|
| `scroll-handlers-throttle.md` | MEDIUM | Optimize scroll handlers with throttling |

## Problem → Skill Mapping

| Problem | Start With |
|---------|------------|
| Animation feels janky/stuttering | `shared-values-read-in-worklets.md` → `re-renders-use-shared-values.md` |
| Reading shared value to determine toggle state | `shared-values-track-state-with-ref.md` |
| Too many re-renders during animation | `re-renders-use-shared-values.md` → `memoization-animations.md` |
| Expensive calculations every frame | `calculations-use-derived-value.md` → `calculations-avoid-conditionals.md` |
| Conditional logic in worklets causing jank | `calculations-avoid-conditionals.md` |
| Layout animations are slow | `layout-prefer-transform.md` |
| Multiple shared value updates cause jank | `calculations-batch-with-schedule-on-ui.md` |
| Clamping values inefficiently | `calculations-use-clamp.md` |
| Frame callback performance issues | `memoization-frame-callbacks.md` |
| Gesture handler reattaches frequently | `memoization-gesture-objects.md` |
| useAnimatedReaction causing performance issues | `reactions-optimize-dependencies.md` |
| Wrong hook choice (useAnimatedProps vs useAnimatedStyle) | `hooks-choose-animated-props.md` |
| Animations conflicting or not canceling | `animations-cancel-properly.md` |
| Shared value initialization is expensive | `shared-values-initialization.md` |
| Too many animated components | `limits-animated-components.md` |
| Scroll handler causes performance issues | `scroll-handlers-throttle.md` |

