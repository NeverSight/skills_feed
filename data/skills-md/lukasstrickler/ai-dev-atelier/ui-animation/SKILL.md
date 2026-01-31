---
name: ui-animation
description: "Guide tasteful UI animation with easing, springs, layout animations, gestures, and accessibility. Covers Tailwind and Motion patterns. Use when: (1) Implementing enter/exit animations, (2) Choosing easing curves, (3) Configuring springs, (4) Layout animations and shared elements, (5) Drag/swipe gestures, (6) Micro-interactions, (7) Ensuring prefers-reduced-motion accessibility. Triggers: animate, animation, easing, spring, transition, motion, layout, gesture, drag, swipe, reduced motion, framer motion."
metadata:
  author: ai-dev-atelier
  version: "1.0"
---

# UI Animation

Tasteful UI animation with proper timing, accessibility, and performance.

## Quick Start

**Technique Decision:**
- **Simple transition?** → CSS/Tailwind (`transition-*`, `animate-*`)
- **Enter/exit with unmount?** → Motion + `AnimatePresence`
- **Gesture-driven?** → Motion springs
- **Layout changes?** → Motion `layout` prop

**Default:** Start with Easing Decision Tree → Duration Guidelines → Implement → Add a11y → Verify

## Core Principles

1. **Natural Motion**: Mimic physics. Avoid linear easing - nothing moves at constant speed.
2. **Purposeful**: Every animation must add meaning. If you can't explain its benefit, remove it.
3. **Fast**: UI animations under 300ms. Hover effects under 150ms. Over 500ms feels sluggish.
4. **Interruptible**: Use springs for gesture-driven animations - they handle interruption gracefully.
5. **Accessible**: Always respect `prefers-reduced-motion`. Non-negotiable.

## Workflow

### Step 1: Classify Animation Type

| Type | Examples | Technique |
|------|----------|-----------|
| Micro-interaction | Button press, toggle, checkbox | CSS/Tailwind |
| Enter/Exit | Modal, toast, dropdown | Motion + AnimatePresence |
| Layout change | Accordion, reorder, expand | Motion `layout` prop |
| Shared element | Tab indicator, card expand | Motion `layoutId` |
| Gesture | Drag, swipe, pull-to-refresh | Motion springs |

### Step 2: Choose Timing

1. Use **Easing Decision Tree** below to select curve
2. Use **Duration Guidelines** to select timing
3. For gestures, use **Spring Animations** config

### Step 3: Implement

1. Check `references/recipes.md` for copy-paste patterns
2. Apply timing from Step 2
3. Wrap unmounting elements in `AnimatePresence`

Use `ui_to_artifact` when starting from a design screenshot or mockup. Use `ui_diff_check` to compare expected vs implemented UI.

### Step 4: Accessibility (Required)

1. Check `prefers-reduced-motion` with `useReducedMotion()` or `motion-safe:`
2. Simplify to opacity-only for reduced motion users
3. Verify focus timing (move focus AFTER animation starts)

### Step 5: Verify

- [ ] Exit animations run (not instant unmount)
- [ ] `opacity: 0` elements have `pointerEvents: none`
- [ ] Focus moves after animation starts, not before
- [ ] Only animating `transform` and `opacity`

## Easing

### Decision Tree

```text
What triggers the animation?
│
├─ User action (click, tap, open)?
│  └─ Use: ease-out (fast start, slow end = responsive)
│
├─ Element moving on-screen (tab switch, reorder)?
│  └─ Use: ease-in-out (accelerate then decelerate)
│
├─ Continuous/looping (spinner, marquee)?
│  └─ Use: linear (constant speed appropriate here)
│
├─ Gesture-based (drag, swipe, pull)?
│  └─ Use: Spring animation (physics-based, interruptible)
│
└─ Hover/focus effect?
   └─ Use: CSS ease, 150ms (subtle, immediate)
```

### Quick Reference

| Purpose | CSS | Tailwind | Duration |
|---------|-----|----------|----------|
| Modal/drawer enter | `cubic-bezier(0.32, 0.72, 0, 1)` | `ease-out duration-200` | 200ms |
| Modal/drawer exit | `cubic-bezier(0.32, 0.72, 0, 1)` | `ease-out duration-150` | 150ms |
| On-screen movement | `cubic-bezier(0.4, 0, 0.2, 1)` | `ease-in-out duration-200` | 200-300ms |
| Hover effect | `ease` | `ease duration-150` | 150ms |
| Button press | — | `active:scale-[0.97]` | instant |

### Pro Curves

| Name | Value | Use Case |
|------|-------|----------|
| **Vaul (buttery)** | `cubic-bezier(0.32, 0.72, 0, 1)` | Sheets, drawers, modals |
| **Emphasized** | `cubic-bezier(0.2, 0, 0, 1)` | Material Design 3 |
| **Snappy** | `cubic-bezier(0.25, 1, 0.5, 1)` | Fast UI transitions |

**Avoid**: Built-in `ease-in`—starts slow, feels sluggish.

## Duration Guidelines

| Type | Duration | Notes |
|------|----------|-------|
| Micro-feedback | 100-150ms | Button press, toggle, checkbox |
| Small transition | 150-250ms | Tooltip, icon morph |
| Medium transition | 200-300ms | Modal, popover, dropdown |
| Large transition | 300-400ms | Page transition, complex layout |
| **Maximum** | <500ms | Exceptions: onboarding, data viz |

**Key Rules**:
- **Exit faster than enter**: 200ms enter → 150ms exit
- **Hover = fast**: Under 150ms
- **High-frequency = instant**: Keyboard nav, scrolling—<100ms or none

## Spring Animations

### Duration-based (Recommended)

Easier to compose with other timed animations. Use `visualDuration` (time to visually reach target) and `bounce` (0 = no bounce, 1 = very bouncy).

| Feel | Config | Use Case |
|------|--------|----------|
| **Snappy** | `{ duration: 0.3, bounce: 0.15 }` | Tabs, buttons, quick feedback |
| **Standard** | `{ duration: 0.4, bounce: 0.2 }` | Modals, menus, general UI |
| **Gentle** | `{ duration: 0.5, bounce: 0.25 }` | Smooth, human-like flow |

### Physics-based (Legacy/Advanced)

Use when integrating with physics libraries or when precise control over spring dynamics is needed.

| Feel | Config | Use Case |
|------|--------|----------|
| **Snappy** | `{ stiffness: 400, damping: 30 }` | High-frequency interactions |
| **Standard** | `{ stiffness: 300, damping: 20 }` | Framer Handshake convention |
| **Gentle** | `{ stiffness: 120, damping: 14 }` | react-motion preset |

> **Gotcha**: `stiffness`/`damping`/`mass` overrides `duration`/`bounce`. Pick one approach—don't mix.

## Layout Animations

### The `layout` Prop

Add `layout` to animate position/size changes automatically. Use `layout="position"` for text (prevents distortion).

| Prop Value | Effect | Use Case |
|------------|--------|----------|
| `layout={true}` | Animates position AND size | Default for flexible elements |
| `layout="position"` | Animates only translation | Text/icons that shouldn't stretch |
| `layout="size"` | Animates only dimensions | Fixed-position expanding panels |

### Shared Element Transitions (`layoutId`)

Elements with matching `layoutId` animate between each other when entering/exiting.

**Critical Trap**: Duplicate `layoutId` values cause elements to **teleport across the page**. Use unique IDs per context or wrap in `<LayoutGroup id="...">`.

### Layout Gotchas

- **Text distortion**: Apply `layout="position"` to text elements
- **Border radius**: Can warp during scale—Motion auto-corrects, but test it
- **SVG elements**: `layout` doesn't work on `<path>`—use manual morphing

## Gesture Gotchas

| Problem | Solution |
|---------|----------|
| Touch scroll conflicts | `dragPropagation={false}` |
| Element snaps back | Check `dragConstraints` + `dragElastic` |
| Momentum feels wrong | `dragMomentum={false}` for precise UIs |
| One-direction only | `dragElastic={{ top: 0, bottom: 0.5 }}` |

**Swipe dismiss**: Check BOTH distance AND velocity—users expect flicks to work.

## Accessibility

### prefers-reduced-motion (REQUIRED)

```tsx
import { useReducedMotion } from "motion/react"

const shouldReduce = useReducedMotion()
const variants = shouldReduce 
  ? { opacity: 1 }                    // Fade only
  : { opacity: 1, scale: 1, y: 0 }    // Full animation
```

Tailwind: `motion-safe:animate-pulse` / `motion-reduce:transition-none`

**Best practice**: Don't disable—simplify. Remove spatial movement, keep opacity.

### Focus Management

- Move focus AFTER animation starts: `requestAnimationFrame(() => ref.focus())`
- Restore focus to trigger on close
- Don't animate inside `aria-live` regions

### Touch Targets

| Standard | Size | Tailwind | Physical |
|----------|------|----------|----------|
| **Material Design** | 48×48 dp | `min-h-12 min-w-12` | ~9mm (recommended) |
| **Apple HIG** | 44×44 pt | `min-h-11 min-w-11` | ~7mm |
| **WCAG 2.2 (AA)** | 24×24 px | `min-h-6 min-w-6` | ~5mm (minimum) |

**Why?** Average adult finger pad is ~9mm. Targets below 7mm cause "fat finger" errors. Use Material's 48dp for cross-platform; Apple's 44pt is iOS-specific minimum.

## Performance

### Golden Rules

1. **Only animate `transform` and `opacity`**—GPU-accelerated
2. **Never animate**: `width`, `height`, `top`, `left`, `margin`, `padding`
3. **`will-change` sparingly**—only during animation, remove after
4. **Blur thresholds**:
   - ≤10px: Safe for animation
   - 11-20px: May cause jank on mobile/4K—test thoroughly
   - >20px: Avoid for real-time effects; use pre-blurred images instead
5. **Prefer CSS over JS** for simple transitions

### Key Traps

- **Height animation**: Use `layout` prop, not `animate={{ height }}`
- **Invisible but clickable**: `opacity: 0` still receives clicks—add `pointerEvents: "none"`
- **will-change everywhere**: Causes layer explosion, mobile crashes

See `references/recipes.md` for detailed examples.

## Examples

Copy-paste patterns organized by category in `references/recipes.md`:

- **Common UI Patterns**: Button press, modal enter/exit, error shake, staggered lists, accordion
- **Touch & Interaction**: Accessible touch targets, hover on touch devices, instant tooltips
- **Layout Animations**: `layout` prop, `layoutId` shared elements, collision fixes
- **Radix UI Integration**: `forceMount` pattern, `asChild`, origin-aware popovers
- **Accessibility**: Focus timing, focus restoration, reduced motion variants
- **Performance**: Height animation (use `layout`), invisible-but-clickable fix, `will-change`
- **Exit Patterns**: `popLayout` with `forwardRef`, SSR hydration (`initial={false}`)
- **Gestures**: Swipe dismiss with velocity check, elastic drag boundaries

## AnimatePresence

| Mode | Behavior | Use Case |
|------|----------|----------|
| `sync` (default) | Simultaneous enter/exit | Crossfades, overlays |
| `wait` | Exit completes before enter | Page transitions, tabs |
| `popLayout` | Exiting elements leave flow | List removals (with `layout`) |

### Exit Animation Trap

Exit animations require `AnimatePresence`—without it, unmount is instant:

```tsx
// ❌ Exit never runs
{isOpen && <motion.div exit={{ opacity: 0 }}>...</motion.div>}

// ✅ Wrap in AnimatePresence
<AnimatePresence>
  {isOpen && <motion.div exit={{ opacity: 0 }}>...</motion.div>}
</AnimatePresence>
```

**SSR**: Use `<AnimatePresence initial={false}>` to prevent animation on page load.

## Anti-patterns

| Don't | Do Instead | Why |
|-------|------------|-----|
| `scale(0)` start | `scale(0.9)` or higher | Avoids "popping" effect |
| `linear` for UI | `ease-out` or springs | Linear feels robotic |
| Animations >500ms | Keep under 300ms | Feels sluggish |
| Same tooltip delay | First: 400ms, subsequent: 0ms | User mental model |
| Skip reduced-motion | Always `motion-safe:` | Accessibility |
| Animate layout props | Use `transform: scale()` | Performance |
| Excessive bounce | `bounce: 0-0.2` | Unprofessional |

## tailwindcss-animate

> **Tailwind v4**: Define keyframes via `@theme` in CSS, not config.

| Category | Classes |
|----------|---------|
| Enter | `animate-in fade-in zoom-in-95 slide-in-from-top` |
| Exit | `animate-out fade-out zoom-out-95 slide-out-to-top` |
| Timing | `delay-150 duration-500` |
| Fill Mode | `fill-mode-forwards fill-mode-backwards` |

## Integration with Other Skills

| When | Skill | Why |
|------|-------|-----|
| After implementing | `code-quality` | Ensure code passes checks |
| Reusable patterns | `docs-write` | Document component API |
| Before committing | `git-commit` | Use `feat(ui):` or `style:` |
| Integration issues | `search` | Look up latest patterns |

## Output

- **Artifacts**: Code changes only (no `.ada/` outputs)
- **Modifications**: Component animations, CSS/Tailwind styles, Motion configs
- **Type**: Workflow skill (guidance only, no scripts)

## References

### Internal

- [`references/recipes.md`](references/recipes.md) - Copy-paste patterns, integration examples, detailed traps

### External

- [Motion Documentation](https://motion.dev/docs)
- [Material Design 3 Motion](https://m3.material.io/styles/motion)
- [Apple HIG - Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- [tailwindcss-animate](https://github.com/jamiebuilds/tailwindcss-animate)
- [easings.net](https://easings.net) - Easing function cheat sheet
