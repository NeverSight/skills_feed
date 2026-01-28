---
name: swiftui-animations
description: Use when building, debugging, or refining animations in SwiftUI iOS/macOS apps. Covers implicit/explicit animations, transitions, gesture-driven interactions, and modern iOS 17+ APIs like PhaseAnimator and KeyframeAnimator.
---

You are an expert in SwiftUI animations. Help developers create smooth, performant, and accessible animations following Apple's best practices.

## Core Principles

### How SwiftUI Animation Works

1. **Animations are driven by state changes** – SwiftUI animates the *difference* between old and new state
2. **Transactions propagate down** – When you wrap a state change in `withAnimation`, a transaction flows through the view hierarchy
3. **Only animatable data animates** – Types must conform to `Animatable` (most built-in types do: CGFloat, Color, CGSize, etc.)
4. **Animation is declarative** – You describe what the end state looks like, SwiftUI figures out the interpolation

### Mental Model

```
State Change → Transaction Created → View Diffed → Animatable Properties Interpolated → Frames Rendered
```

Think of animations as *automatic interpolation between two snapshots of your view*. Your job is to:
1. Define the two states clearly
2. Tell SwiftUI which timing curve to use
3. Ensure the properties you want animated are `Animatable`

## Implicit Animations

The easiest way to animate – attach an `.animation()` modifier or wrap state changes in `withAnimation`.

### withAnimation (Recommended)

Wraps a state change so all resulting view updates animate:

```swift
withAnimation(.spring(duration: 0.4, bounce: 0.3)) {
    isExpanded.toggle()
}
```

**When to use:** When you control the state change (button taps, gestures, responses).

### .animation() Modifier

Animates whenever the observed value changes:

```swift
Circle()
    .scaleEffect(isActive ? 1.2 : 1.0)
    .animation(.easeInOut(duration: 0.3), value: isActive)
```

**When to use:** When state changes outside your control (bindings, parent state).

**Critical:** Always use `value:` parameter. The old `.animation(.default)` without value is deprecated and causes unpredictable behavior.

### Timing Curves

| Curve | Use Case |
|-------|----------|
| `.linear` | Mechanical, constant motion (progress bars) |
| `.easeIn` | Objects entering from user action |
| `.easeOut` | Objects settling into place |
| `.easeInOut` | General UI, symmetrical movement |
| `.spring(duration:bounce:)` | **Default choice for iOS** – natural feel |
| `.spring(response:dampingFraction:)` | Fine-tuned spring physics |
| `.interactiveSpring` | Gesture-driven, snappy response |

**Rule of thumb:** Use `.spring()` unless you have a reason not to. Apple's HIG recommends spring animations for most interactions.

## Explicit Animations

For custom types and complex animations where implicit animation isn't enough.

### The Animatable Protocol

Any type can animate if it provides an `animatableData` property:

```swift
struct AnimatableGradient: View, Animatable {
    var progress: CGFloat

    var animatableData: CGFloat {
        get { progress }
        set { progress = newValue }
    }

    var body: some View {
        // Use progress (0→1) to interpolate colors, positions, etc.
    }
}
```

SwiftUI calls the setter repeatedly with interpolated values between old and new state.

### AnimatableModifier

For reusable animated effects:

```swift
struct CountingModifier: AnimatableModifier {
    var value: Double

    var animatableData: Double {
        get { value }
        set { value = newValue }
    }

    func body(content: Content) -> some View {
        content.overlay(Text("\(Int(value))"))
    }
}

// Usage: Text counts from 0 to 100
Text("Score").modifier(CountingModifier(value: score))
```

### Animating Shapes

Shapes animate via their `animatableData`. For multiple values, use `AnimatablePair`:

```swift
struct Wedge: Shape {
    var startAngle: Double
    var endAngle: Double

    var animatableData: AnimatablePair<Double, Double> {
        get { AnimatablePair(startAngle, endAngle) }
        set {
            startAngle = newValue.first
            endAngle = newValue.second
        }
    }

    func path(in rect: CGRect) -> Path { /* ... */ }
}
```

**Nested pairs** for 3+ values: `AnimatablePair<CGFloat, AnimatablePair<CGFloat, CGFloat>>`

## Transitions

Transitions animate views entering and leaving the view hierarchy. They only apply when views are inserted/removed (via `if`, `switch`, `ForEach` changes).

### Built-in Transitions

```swift
if showDetail {
    DetailView()
        .transition(.slide)
}
```

| Transition | Effect |
|------------|--------|
| `.opacity` | Fade in/out |
| `.slide` | Slide from leading edge |
| `.move(edge:)` | Slide from specified edge |
| `.scale` | Grow from center |
| `.scale(anchor:)` | Grow from anchor point |
| `.push(from:)` | Push in, old view pushed out |
| `.offset(x:y:)` | Animate from offset position |

### Combining Transitions

```swift
.transition(.scale.combined(with: .opacity))

// Or use extension for reusability:
extension AnyTransition {
    static var scaleAndFade: AnyTransition {
        .scale(scale: 0.8).combined(with: .opacity)
    }
}
```

### Asymmetric Transitions

Different animations for insertion vs removal:

```swift
.transition(.asymmetric(
    insertion: .move(edge: .trailing).combined(with: .opacity),
    removal: .move(edge: .leading).combined(with: .opacity)
))
```

### Custom Transitions

Build from any `ViewModifier`:

```swift
struct SlideAndBlur: ViewModifier {
    let active: Bool

    func body(content: Content) -> some View {
        content
            .offset(x: active ? 200 : 0)
            .blur(radius: active ? 10 : 0)
    }
}

extension AnyTransition {
    static var slideBlur: AnyTransition {
        .modifier(
            active: SlideAndBlur(active: true),
            identity: SlideAndBlur(active: false)
        )
    }
}
```

**Key gotcha:** Transitions require `withAnimation` around the state change that adds/removes the view. The `.animation()` modifier on the view itself won't trigger transitions.

## Gesture-Driven Animations

Interactive animations that respond to user touch in real-time.

### Basic Drag with Spring Release

```swift
@State private var offset: CGSize = .zero

var body: some View {
    Circle()
        .offset(offset)
        .gesture(
            DragGesture()
                .onChanged { offset = $0.translation }
                .onEnded { _ in
                    withAnimation(.spring(response: 0.4, dampingFraction: 0.6)) {
                        offset = .zero
                    }
                }
        )
}
```

### GestureState for Auto-Reset

`@GestureState` automatically resets when gesture ends – perfect for temporary states:

```swift
@GestureState private var dragOffset: CGSize = .zero

var body: some View {
    Card()
        .offset(dragOffset)
        .animation(.interactiveSpring, value: dragOffset)
        .gesture(
            DragGesture()
                .updating($dragOffset) { value, state, _ in
                    state = value.translation
                }
        )
}
```

### Velocity-Aware Animations

Use gesture velocity for natural-feeling releases:

```swift
.onEnded { gesture in
    let velocity = CGVector(
        dx: gesture.velocity.width / 300,
        dy: gesture.velocity.height / 300
    )
    withAnimation(.spring(response: 0.4, dampingFraction: 0.7, blendDuration: 0.25).speed(1)) {
        // Factor velocity into final position
    }
}
```

### Tracking Animation Progress

Use `GeometryReader` + `PreferenceKey` or iOS 17's `onGeometryChange` to read animated values for coordinated effects.

### Spring Parameters for Gestures

| Context | Recommended Spring |
|---------|-------------------|
| Dragging (live) | `.interactiveSpring` or no animation |
| Release to origin | `.spring(response: 0.4, dampingFraction: 0.7)` |
| Release to target | `.spring(response: 0.5, dampingFraction: 0.8)` |
| Snap to position | `.spring(response: 0.3, dampingFraction: 0.9)` |

## Modern APIs (iOS 17+)

iOS 17 introduced powerful declarative animation APIs that simplify complex sequences.

### PhaseAnimator

Cycles through discrete phases automatically – perfect for looping or multi-step animations:

```swift
enum BouncePhase: CaseIterable {
    case initial, compress, stretch, settle

    var scale: CGSize {
        switch self {
        case .initial: CGSize(width: 1, height: 1)
        case .compress: CGSize(width: 1.1, height: 0.9)
        case .stretch: CGSize(width: 0.9, height: 1.1)
        case .settle: CGSize(width: 1, height: 1)
        }
    }
}

PhaseAnimator(BouncePhase.allCases) { phase in
    Circle()
        .scaleEffect(phase.scale)
} animation: { phase in
    switch phase {
    case .initial: .spring(duration: 0.2, bounce: 0.5)
    default: .spring(duration: 0.25, bounce: 0.3)
    }
}
```

**Trigger-based:** Add `trigger:` parameter to run on value change instead of looping:

```swift
PhaseAnimator(phases, trigger: triggerValue) { phase in ... }
```

### KeyframeAnimator

Fine-grained control with keyframes on multiple properties:

```swift
KeyframeAnimator(initialValue: AnimationState()) { state in
    Circle()
        .offset(x: state.xOffset)
        .scaleEffect(state.scale)
        .opacity(state.opacity)
} keyframes: { _ in
    KeyframeTrack(\.xOffset) {
        LinearKeyframe(0, duration: 0.1)
        SpringKeyframe(100, duration: 0.4, spring: .bouncy)
        SpringKeyframe(0, duration: 0.3)
    }
    KeyframeTrack(\.scale) {
        LinearKeyframe(1.0, duration: 0.1)
        CubicKeyframe(1.3, duration: 0.2)
        CubicKeyframe(1.0, duration: 0.4)
    }
}
```

**Keyframe types:**
- `LinearKeyframe` – Constant velocity
- `CubicKeyframe` – Bezier easing
- `SpringKeyframe` – Physics-based
- `MoveKeyframe` – Instant jump (no interpolation)

### New Spring Syntax

iOS 17 simplified spring parameters:

```swift
// Old (still works)
.spring(response: 0.5, dampingFraction: 0.7)

// New – more intuitive
.spring(duration: 0.5, bounce: 0.3)  // bounce: 0 = no bounce, 1 = max bounce

// Presets
.spring(.smooth)    // No bounce
.spring(.snappy)    // Slight bounce
.spring(.bouncy)    // Pronounced bounce
```

### When to Use What

| Scenario | API |
|----------|-----|
| Single state change | `withAnimation` |
| Looping/cycling animation | `PhaseAnimator` |
| Complex multi-property choreography | `KeyframeAnimator` |
| User-triggered sequence | `PhaseAnimator` with `trigger:` |
| Fine-tuned timing control | `KeyframeAnimator` |

## Critical Rules

### DO:

- **Always use `value:` parameter** with `.animation()` modifier – the valueless version is deprecated and buggy
- **Prefer `withAnimation` over `.animation()`** – more explicit control over what triggers animation
- **Use springs as default** – they feel more natural than linear/ease curves
- **Respect reduced motion** – check `accessibilityReduceMotion` (see Accessibility section)
- **Animate layout, not frames** – use `.offset()`, `.scaleEffect()`, `.opacity()` rather than changing `frame` directly
- **Keep animations under 400ms** for UI responses – longer feels sluggish
- **Test on device** – Simulator timing differs from real hardware

### DO NOT:

- **Don't animate inside `body` computation** – body should be pure; trigger animations from state changes
- **Don't use `.animation()` without `value:`** – causes unpredictable cascading animations
- **Don't fight the framework** – if an animation is hard to achieve, reconsider the approach
- **Don't animate too many properties simultaneously** – pick 2-3 max for clarity
- **Don't use `DispatchQueue.main.asyncAfter` for sequencing** – use `PhaseAnimator` or completion-based APIs
- **Don't nest `withAnimation` blocks** – the innermost wins, outer is ignored
- **Don't assume animation completion** – SwiftUI doesn't guarantee completion callbacks; use `Transaction` for critical sequencing

### Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| Transition doesn't animate | Missing `withAnimation` around state change | Wrap `if` condition change in `withAnimation` |
| Animation happens twice | Using both `withAnimation` and `.animation()` | Pick one approach |
| Choppy animation | Animating non-animatable property | Check type conforms to `Animatable` |
| Spring never settles | `dampingFraction` too low | Use 0.7+ for settling, or add `.speed()` |
| Animation on wrong view | Transaction propagating unexpectedly | Use `.transaction { $0.animation = nil }` to block |
| List items animate weirdly | Missing stable `id` | Ensure `Identifiable` with stable IDs |

## Accessibility

### Respecting Reduced Motion

Users can enable "Reduce Motion" in system settings. Always provide alternatives:

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion

var body: some View {
    Card()
        .transition(reduceMotion ? .opacity : .slide.combined(with: .opacity))
}

// For animations:
func animateChange() {
    if reduceMotion {
        // Instant or simple fade
        withAnimation(.easeOut(duration: 0.15)) {
            isExpanded.toggle()
        }
    } else {
        // Full spring animation
        withAnimation(.spring(duration: 0.4, bounce: 0.3)) {
            isExpanded.toggle()
        }
    }
}
```

### Quick Helper

```swift
extension Animation {
    static func respectful(_ animation: Animation, reducedMotion: Animation = .easeOut(duration: 0.15)) -> Animation {
        // Use at call site with @Environment check
        animation
    }
}

// Or create a View extension:
extension View {
    func animateRespectfully<V: Equatable>(
        _ animation: Animation,
        value: V,
        reduceMotion: Bool
    ) -> some View {
        self.animation(reduceMotion ? .easeOut(duration: 0.15) : animation, value: value)
    }
}
```

### Guidelines

- **Fade is always safe** – `.opacity` transitions work for everyone
- **Reduce, don't remove** – some motion helps comprehension; just make it subtle
- **Avoid vestibular triggers** – large zooms, parallax, spinning are problematic
- **Test with setting enabled** – Settings → Accessibility → Motion → Reduce Motion
