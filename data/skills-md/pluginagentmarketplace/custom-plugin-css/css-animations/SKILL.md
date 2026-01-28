---
name: css-animations
description: Create performant CSS animations, transitions, and motion design
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-12-30"
bonded_agent: 03-css-animations
bond_type: PRIMARY_BOND
---

# CSS Animations Skill

Create performant, accessible CSS animations and transitions with proper timing and motion design.

## Overview

This skill provides atomic, focused guidance on CSS animations with performance optimization and accessibility considerations built-in.

## Skill Metadata

| Property | Value |
|----------|-------|
| **Category** | Motion |
| **Complexity** | Intermediate to Expert |
| **Dependencies** | css-fundamentals |
| **Bonded Agent** | 03-css-animations |

## Usage

```
Skill("css-animations")
```

## Parameter Schema

```yaml
parameters:
  animation_type:
    type: string
    required: true
    enum: [transition, keyframe, transform, timing]
    description: Type of animation to create

  effect:
    type: string
    required: false
    enum: [fade, slide, scale, rotate, bounce, shake, pulse]
    description: Predefined animation effect

  performance_mode:
    type: boolean
    required: false
    default: true
    description: Optimize for 60fps performance

  accessible:
    type: boolean
    required: false
    default: true
    description: Include reduced-motion alternatives

validation:
  - rule: animation_type_required
    message: "animation_type parameter is required"
  - rule: valid_effect
    message: "effect must be a recognized animation effect"
```

## Topics Covered

### Transitions
- Property, duration, timing-function, delay
- Transitionable vs non-transitionable properties
- Multi-property transitions

### Keyframe Animations
- @keyframes syntax
- Animation properties (name, duration, iteration, direction)
- Fill modes and play states

### Transforms
- 2D: translate, rotate, scale, skew
- 3D: perspective, rotateX/Y/Z, translateZ
- Transform origin and composition

### Timing Functions
- Built-in: ease, linear, ease-in, ease-out, ease-in-out
- cubic-bezier() custom curves
- steps() for frame-by-frame

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff_type: exponential
  initial_delay_ms: 1000
  max_delay_ms: 10000
```

## Logging & Observability

```yaml
logging:
  entry_point: skill_invoked
  exit_point: skill_completed
  metrics:
    - invocation_count
    - effect_usage
    - performance_mode_ratio
```

## Quick Reference

### Transition Template

```css
.element {
  transition: property duration timing-function delay;
  transition: transform 0.3s ease-out;
  transition: opacity 0.2s, transform 0.3s ease-out;
}
```

### Keyframe Template

```css
@keyframes animation-name {
  0% { /* start state */ }
  50% { /* midpoint state */ }
  100% { /* end state */ }
}

.element {
  animation: name duration timing-function delay iteration-count direction fill-mode;
  animation: slide-in 0.5s ease-out forwards;
}
```

### Performance Rules

```
SAFE (Compositor-only):
├─ transform
└─ opacity

AVOID (Trigger repaint/reflow):
├─ width, height
├─ top, left, right, bottom
├─ margin, padding
└─ background-color
```

## Common Effects

### Fade In

```css
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in {
  animation: fade-in 0.3s ease-out forwards;
}
```

### Slide Up

```css
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-up {
  animation: slide-up 0.4s ease-out forwards;
}
```

### Pulse

```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}
```

### Accessibility Template

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

## Timing Function Reference

```
cubic-bezier(x1, y1, x2, y2)

ease:        (0.25, 0.1, 0.25, 1.0)
ease-in:     (0.42, 0, 1.0, 1.0)
ease-out:    (0, 0, 0.58, 1.0)
ease-in-out: (0.42, 0, 0.58, 1.0)

Custom:
Bounce:      (0.68, -0.55, 0.265, 1.55)
Snap:        (0.5, 0, 0.75, 0)
Smooth:      (0.4, 0, 0.2, 1)
```

## Test Template

```javascript
describe('CSS Animations Skill', () => {
  test('validates animation_type parameter', () => {
    expect(() => skill({ animation_type: 'invalid' }))
      .toThrow('animation_type must be one of: transition, keyframe...');
  });

  test('returns accessible version when flag is true', () => {
    const result = skill({
      animation_type: 'keyframe',
      effect: 'fade',
      accessible: true
    });
    expect(result).toContain('prefers-reduced-motion');
  });

  test('uses compositor-only properties in performance mode', () => {
    const result = skill({
      animation_type: 'transform',
      performance_mode: true
    });
    expect(result).not.toContain('left:');
    expect(result).not.toContain('top:');
  });
});
```

## Error Handling

| Error Code | Cause | Recovery |
|------------|-------|----------|
| INVALID_ANIMATION_TYPE | Unknown animation type | Show valid options |
| PERFORMANCE_WARNING | Using layout-triggering properties | Suggest transform alternative |
| ACCESSIBILITY_MISSING | No reduced-motion fallback | Add default accessible version |

## Related Skills

- css-fundamentals (prerequisite)
- css-performance (animation optimization)
- css-modern (scroll-driven animations)
