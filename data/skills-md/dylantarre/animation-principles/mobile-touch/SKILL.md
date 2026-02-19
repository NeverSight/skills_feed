---
name: mobile-touch
description: Use when designing iOS/Android gestures, haptic feedback, touch interactions, or native mobile animations.
---

# Mobile Touch Animation

Apply Disney's 12 animation principles to mobile gestures, haptics, and native app motion.

## Quick Reference

| Principle | Mobile Implementation |
|-----------|----------------------|
| Squash & Stretch | Rubber-banding, bounce on scroll limits |
| Anticipation | Peek before reveal, long-press preview |
| Staging | Sheet presentations, focus states |
| Straight Ahead / Pose to Pose | Gesture-driven vs preset transitions |
| Follow Through / Overlapping | Momentum scrolling, trailing elements |
| Slow In / Slow Out | iOS spring animations, Material easing |
| Arc | Swipe-to-dismiss curves, card throws |
| Secondary Action | Haptic pulse with visual feedback |
| Timing | Touch response <100ms, transitions 250-350ms |
| Exaggeration | Bounce amplitude, haptic intensity |
| Solid Drawing | Respect safe areas, consistent anchors |
| Appeal | 60fps minimum, gesture continuity |

## Principle Applications

**Squash & Stretch**: Implement rubber-band effect at scroll boundaries. Pull-to-refresh should stretch content naturally. Buttons compress on touch.

**Anticipation**: Long-press shows preview before full action. Drag threshold provides visual hint before item lifts. Swipe shows edge of destination content.

**Staging**: Use sheet presentations to maintain context. Dim and scale background during modal focus. Hero transitions connect views meaningfully.

**Straight Ahead vs Pose to Pose**: Gesture-following animations (drag, pinch) are straight ahead—driven by touch input. System transitions (push, present) are pose to pose—predefined keyframes.

**Follow Through & Overlapping**: Content continues moving after finger lifts (momentum). Navigation bar elements animate slightly after main content. Lists items settle with stagger.

**Slow In / Slow Out**: iOS uses spring physics—configure mass, stiffness, damping. Android Material uses standard easing: `FastOutSlowIn`. Never use linear for user-initiated motion.

**Arc**: Thrown cards follow parabolic arcs. Swipe-to-dismiss curves based on velocity vector. FAB expand/collapse follows natural arc path.

**Secondary Action**: Pair haptic feedback with visual response. Button ripple accompanies press. Success checkmark triggers light haptic.

**Timing**: Touch acknowledgment: <100ms. Quick actions: 150-250ms. View transitions: 250-350ms. Complex animations: 350-500ms. Haptic should sync precisely with visual.

**Exaggeration**: Pull-to-refresh stretches beyond natural—makes feedback clear. Error shake is pronounced. Success animations celebrate appropriately.

**Solid Drawing**: Respect device safe areas during animation. Maintain consistent transform origins. Account for notch/dynamic island in motion paths.

**Appeal**: Minimum 60fps, target 120fps on ProMotion displays. Gesture-driven animation must feel connected to finger. Interruptible animations essential.

## Platform Patterns

### iOS
```swift
// Spring animation with follow-through
UIView.animate(withDuration: 0.5,
               delay: 0,
               usingSpringWithDamping: 0.7,
               initialSpringVelocity: 0.5,
               options: .curveEaseOut)

// Haptic pairing
let feedback = UIImpactFeedbackGenerator(style: .medium)
feedback.impactOccurred()
```

### Android
```kotlin
// Material spring animation
SpringAnimation(view, DynamicAnimation.TRANSLATION_Y)
    .setSpring(SpringForce()
        .setStiffness(SpringForce.STIFFNESS_MEDIUM)
        .setDampingRatio(SpringForce.DAMPING_RATIO_MEDIUM_BOUNCY))
    .start()
```

## Haptic Guidelines

| Action | iOS | Android |
|--------|-----|---------|
| Selection | `.selection` | `EFFECT_TICK` |
| Success | `.success` | `EFFECT_CLICK` |
| Warning | `.warning` | `EFFECT_DOUBLE_CLICK` |
| Error | `.error` | `EFFECT_HEAVY_CLICK` |

Haptics are secondary action—always pair with visual confirmation.
