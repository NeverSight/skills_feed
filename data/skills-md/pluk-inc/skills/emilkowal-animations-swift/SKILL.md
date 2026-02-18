---
name: emilkowal-animations-swift
description: SwiftUI and AppKit animation best practices for Apple platforms. Use when writing, reviewing, or implementing animations in SwiftUI (iOS 17+) or AppKit. Triggers on tasks involving transitions, easing, springs, gestures, matched geometry, phase animators, or motion.
---

# SwiftUI & AppKit Animation Best Practices

Comprehensive animation guide for Apple platform interfaces, adapted from Emil Kowalski's web animation principles and Framer Motion best practices. Contains 80 rules across 10 categories targeting iOS 17+, prioritized by impact.

## When to Apply

Reference these guidelines when:
- Adding animations to SwiftUI views
- Choosing easing curves, springs, or timing values
- Implementing gesture-based interactions (drag, tap, long press)
- Building transitions and navigation animations
- Using `matchedGeometryEffect` for shared element transitions
- Creating scroll-linked or parallax effects
- Using iOS 17+ `PhaseAnimator` or `KeyframeAnimator`
- Optimizing animation performance
- Ensuring animation accessibility with `accessibilityReduceMotion`
- Writing AppKit/macOS-specific animations

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Timing Curves & Easing | CRITICAL | `ease-` |
| 2 | Duration & Timing | CRITICAL | `timing-` |
| 3 | Animation Properties | HIGH | `props-` |
| 4 | Transforms & Effects | HIGH | `transform-` |
| 5 | Gesture & Interaction | HIGH | `gesture-` |
| 6 | Transitions & Navigation | MEDIUM-HIGH | `transition-` |
| 7 | Scroll & Parallax | MEDIUM | `scroll-` |
| 8 | Strategic Animation | MEDIUM | `strategy-` |
| 9 | Accessibility & Polish | MEDIUM | `polish-` |
| 10 | AppKit Specific | LOW-MEDIUM | `appkit-` |

## Quick Reference

### 1. Timing Curves & Easing (CRITICAL)

- [`ease-prefer-easeout`](references/ease-prefer-easeout.md) - Use easeOut as your default easing
- [`ease-avoid-linear`](references/ease-avoid-linear.md) - Avoid linear easing for UI animations
- [`ease-spring-default`](references/ease-spring-default.md) - Prefer springs for natural motion
- [`ease-spring-ios17`](references/ease-spring-ios17.md) - Use iOS 17 Spring struct with bounce/duration
- [`ease-custom-timing-curve`](references/ease-custom-timing-curve.md) - Create custom curves with timingCurve
- [`ease-ease-in-for-exits`](references/ease-ease-in-for-exits.md) - Use easeIn for exit animations
- [`ease-ease-inout-for-emphasis`](references/ease-ease-inout-for-emphasis.md) - Use easeInOut for emphasis motion
- [`ease-spring-response`](references/ease-spring-response.md) - Configure spring response for duration feel
- [`ease-spring-damping`](references/ease-spring-damping.md) - Configure spring damping for bounce
- [`ease-match-context`](references/ease-match-context.md) - Match easing to animation context

### 2. Duration & Timing (CRITICAL)

- [`timing-200ms-default`](references/timing-200ms-default.md) - Use 200ms as default UI animation duration
- [`timing-100ms-micro`](references/timing-100ms-micro.md) - Use 100ms for micro-interactions
- [`timing-300ms-emphasis`](references/timing-300ms-emphasis.md) - Keep emphasis animations under 300ms
- [`timing-stagger-children`](references/timing-stagger-children.md) - Stagger child animations for orchestration
- [`timing-delay-strategic`](references/timing-delay-strategic.md) - Use delay strategically for sequencing

### 3. Animation Properties (HIGH)

- [`props-opacity-scale`](references/props-opacity-scale.md) - Prefer opacity and scale for performance
- [`props-avoid-size-animate`](references/props-avoid-size-animate.md) - Avoid animating frame size directly
- [`props-transform-origin`](references/props-transform-origin.md) - Set anchor points for transforms
- [`props-drawing-group`](references/props-drawing-group.md) - Use drawingGroup for complex hierarchies
- [`props-animation-disable`](references/props-animation-disable.md) - Use animation(nil) to prevent animations
- [`props-explicit-animation`](references/props-explicit-animation.md) - Use withAnimation for explicit control
- [`props-implicit-animation`](references/props-implicit-animation.md) - Use .animation modifier for implicit animations

### 4. Transforms & Effects (HIGH)

- [`transform-scale-subtle`](references/transform-scale-subtle.md) - Use subtle scale values (0.95-0.98)
- [`transform-rotation-purposeful`](references/transform-rotation-purposeful.md) - Apply rotation with purpose
- [`transform-translate-direction`](references/transform-translate-direction.md) - Translate in meaningful directions
- [`transform-3d-perspective`](references/transform-3d-perspective.md) - Use rotation3DEffect for depth
- [`transform-order-matters`](references/transform-order-matters.md) - Modifier order affects output
- [`transform-anchor-point`](references/transform-anchor-point.md) - Set anchor for rotation/scale origin
- [`transform-combine-effects`](references/transform-combine-effects.md) - Combine transforms purposefully

### 5. Gesture & Interaction (HIGH)

- [`gesture-tap-feedback`](references/gesture-tap-feedback.md) - Provide immediate tap feedback
- [`gesture-long-press`](references/gesture-long-press.md) - Animate long press states
- [`gesture-drag-basic`](references/gesture-drag-basic.md) - Implement smooth drag interactions
- [`gesture-drag-constraints`](references/gesture-drag-constraints.md) - Constrain drag within bounds
- [`gesture-drag-velocity`](references/gesture-drag-velocity.md) - Use velocity for momentum effects
- [`gesture-gesture-state`](references/gesture-gesture-state.md) - Use @GestureState for transient values
- [`gesture-updating-modifier`](references/gesture-updating-modifier.md) - Use .updating for live feedback
- [`gesture-simultaneous-vs-exclusive`](references/gesture-simultaneous-vs-exclusive.md) - Choose gesture composition
- [`gesture-magnify-gesture`](references/gesture-magnify-gesture.md) - Implement pinch-to-zoom
- [`gesture-rotation-gesture`](references/gesture-rotation-gesture.md) - Implement rotation gestures
- [`gesture-hover-macos`](references/gesture-hover-macos.md) - Handle hover on macOS
- [`gesture-sensory-feedback`](references/gesture-sensory-feedback.md) - Pair gestures with haptics
- [`gesture-spring-on-release`](references/gesture-spring-on-release.md) - Spring back on gesture end
- [`gesture-cancellation`](references/gesture-cancellation.md) - Handle gesture cancellation gracefully

### 6. Transitions & Navigation (MEDIUM-HIGH)

- [`transition-builtin-types`](references/transition-builtin-types.md) - Use built-in transition types
- [`transition-asymmetric`](references/transition-asymmetric.md) - Use asymmetric for different enter/exit
- [`transition-combined`](references/transition-combined.md) - Combine transitions for richer effects
- [`transition-custom-modifier`](references/transition-custom-modifier.md) - Create custom transition modifiers
- [`transition-matched-geometry`](references/transition-matched-geometry.md) - Use matchedGeometryEffect properly
- [`transition-namespace-scope`](references/transition-namespace-scope.md) - Manage @Namespace lifecycle
- [`transition-navigation-transitions`](references/transition-navigation-transitions.md) - Customize navigation transitions
- [`transition-sheet-presentations`](references/transition-sheet-presentations.md) - Animate sheet presentations
- [`transition-id-for-replacement`](references/transition-id-for-replacement.md) - Use .id() for view replacement
- [`transition-content-transition`](references/transition-content-transition.md) - Use contentTransition for text

### 7. Scroll & Parallax (MEDIUM)

- [`scroll-geometry-reader`](references/scroll-geometry-reader.md) - Use GeometryReader for scroll position
- [`scroll-preference-key`](references/scroll-preference-key.md) - Use PreferenceKey for scroll data
- [`scroll-parallax-effect`](references/scroll-parallax-effect.md) - Create parallax scroll effects
- [`scroll-sticky-header`](references/scroll-sticky-header.md) - Implement animated sticky headers
- [`scroll-scroll-transition`](references/scroll-scroll-transition.md) - Use iOS 17 scrollTransition modifier
- [`scroll-visual-effect`](references/scroll-visual-effect.md) - Use iOS 17 visualEffect modifier

### 8. Strategic Animation (MEDIUM)

- [`strategy-purposeful-motion`](references/strategy-purposeful-motion.md) - Every animation needs purpose
- [`strategy-hierarchy-emphasis`](references/strategy-hierarchy-emphasis.md) - Use motion to show hierarchy
- [`strategy-state-communication`](references/strategy-state-communication.md) - Animate state changes clearly
- [`strategy-spatial-continuity`](references/strategy-spatial-continuity.md) - Maintain spatial relationships
- [`strategy-brand-expression`](references/strategy-brand-expression.md) - Express brand through motion

### 9. Accessibility & Polish (MEDIUM)

- [`polish-reduce-motion`](references/polish-reduce-motion.md) - Respect accessibilityReduceMotion
- [`polish-phase-animator`](references/polish-phase-animator.md) - Use PhaseAnimator for sequences
- [`polish-keyframe-animator`](references/polish-keyframe-animator.md) - Use KeyframeAnimator for complex paths
- [`polish-animation-completions`](references/polish-animation-completions.md) - Handle animation completion
- [`polish-interruptible-animations`](references/polish-interruptible-animations.md) - Make animations interruptible
- [`polish-animation-debugging`](references/polish-animation-debugging.md) - Debug animations effectively
- [`polish-performance-profiling`](references/polish-performance-profiling.md) - Profile animation performance
- [`polish-symbol-effects`](references/polish-symbol-effects.md) - Use SF Symbol effects
- [`polish-text-animations`](references/polish-text-animations.md) - Animate text with contentTransition
- [`polish-haptic-pairing`](references/polish-haptic-pairing.md) - Pair animations with haptic feedback

### 10. AppKit Specific (LOW-MEDIUM)

- [`appkit-nsanimation-context`](references/appkit-nsanimation-context.md) - Use NSAnimationContext for grouping
- [`appkit-core-animation`](references/appkit-core-animation.md) - Use Core Animation layers
- [`appkit-layer-backed-views`](references/appkit-layer-backed-views.md) - Enable layer backing for performance
- [`appkit-implicit-animations`](references/appkit-implicit-animations.md) - Leverage implicit layer animations
- [`appkit-spring-animation`](references/appkit-spring-animation.md) - Create spring animations in AppKit
- [`appkit-animator-proxy`](references/appkit-animator-proxy.md) - Use animator proxy for view animations

## Key Values Reference

| Value | Usage |
|-------|-------|
| `.spring(duration: 0.3, bounce: 0.2)` | Standard iOS 17 spring animation |
| `.spring(response: 0.3, dampingFraction: 0.7)` | Classic spring configuration |
| `.easeOut(duration: 0.2)` | Standard UI transition |
| `scaleEffect(0.97)` | Button press feedback |
| `scaleEffect(0.95)` | Minimum enter scale (never scale to 0) |
| `0.2` seconds | Default micro-interaction duration |
| `0.3` seconds | Maximum duration for UI animations |
| `0.5` seconds | Sheet/drawer animation duration |

## Concept Mapping (Web to SwiftUI)

| Web Concept | SwiftUI Equivalent |
|-------------|-------------------|
| `ease-out` | `.easeOut` or `Animation.easeOut(duration:)` |
| `cubic-bezier(a,b,c,d)` | `.timingCurve(a, b, c, d, duration:)` |
| Framer Motion spring | `.spring(duration:bounce:)` (iOS 17+) |
| `transform: scale(0.97)` | `.scaleEffect(0.97)` |
| `transform-origin` | `.scaleEffect(anchor: .topLeading)` |
| `useMotionValue` | `@State` / `@GestureState` |
| `AnimatePresence` | `.transition()` + `.id()` |
| `layoutId` | `.matchedGeometryEffect(id:in:)` |
| `useScroll` | `GeometryReader` + `PreferenceKey` |
| `whileHover/whileTap` | `.onHover {}` / gesture modifiers |
| `dragConstraints` | `DragGesture` with `onChange` bounds |
| `prefers-reduced-motion` | `@Environment(\.accessibilityReduceMotion)` |

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
