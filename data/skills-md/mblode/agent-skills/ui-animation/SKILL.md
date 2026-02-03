---
name: ui-animation
description: Guidelines and examples for UI motion and animation. Use when designing, implementing, or reviewing motion, easing, timing, and reduced-motion behaviour.
---

# UI Animation

Use these core rules for consistent motion and animation decisions.

## Core rules
- Animate to clarify cause/effect or add deliberate delight.
- Keep interactions fast (200-300ms; up to 1s only for illustrative motion).
- Prefer CSS; use WAAPI or JS only when needed.
- Make animations interruptible and input-driven.
- Honor `prefers-reduced-motion` (reduce or disable).

## What to animate
- Only `transform` and `opacity`.
- Never animate layout properties; never use `transition: all`.
- Avoid blur > 20px.
- Disable transitions during theme switches.

## Spatial and sequencing
- Set `transform-origin` at the trigger point.
- For dialogs/menus, start around `scale(0.85-0.9)`; avoid `scale(0)`.
- Stagger reveals <= 50ms.

## Easing defaults
- Enter/hover: `cubic-bezier(0.22, 1, 0.36, 1)`.
- Move: `cubic-bezier(0.25, 1, 0.5, 1)`.
- Simple hover colour/opacity: `200ms ease`.

## Accessibility
- If `transform` is used, disable it in `prefers-reduced-motion`.

## Performance
- Pause looping animations off-screen.
- Toggle `will-change` only during heavy motion and only for `transform`/`opacity`.
- Prefer `transform` over positional props in animation libraries.

## Reference
- Snippets and practical tips: `examples.md`.

## Workflow
- Start with the core rules, then pick a reference snippet.
- Keep motion functional; honor `prefers-reduced-motion`.
- When reviewing, cite file paths and line numbers and propose concrete fixes.
