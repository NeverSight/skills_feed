---
name: universal-tool
description: Use when implementing Disney's 12 animation principles with any animation tool or framework
---

# Universal Animation Principles

Apply all 12 Disney animation principles regardless of your tool or framework.

## 1. Squash and Stretch

**Concept**: Objects deform when moving, maintaining volume.

**Implementation**:
- When compressing one axis, expand the other
- `scaleX * scaleY ≈ constant`
- Apply on impact, acceleration, or deceleration

**Values**: Compress to 80%, expand to 120%

## 2. Anticipation

**Concept**: Prepare the audience for an action.

**Implementation**:
- Move opposite to the main action first
- ~20% of total duration for wind-up
- Smaller anticipation for faster actions

**Pattern**: Wind-up → Action → Settle

## 3. Staging

**Concept**: Direct viewer attention to what matters.

**Implementation**:
- Blur or fade background elements
- Scale up the focal point
- Use contrast (color, size, motion)
- One clear action at a time

## 4. Straight Ahead / Pose to Pose

**Straight Ahead**: Animate frame-by-frame sequentially. Good for fluid, organic motion.

**Pose to Pose**: Define key poses, then fill in between. Good for precise, planned motion.

**Recommendation**: Use pose-to-pose for UI, straight ahead for particles/effects.

## 5. Follow Through and Overlapping Action

**Concept**: Different parts move at different rates.

**Implementation**:
- Offset timing of child elements
- Add 2-5 frame delay for secondary elements
- Lighter/looser parts drag behind
- Use easing with different curves per element

## 6. Slow In and Slow Out

**Concept**: Natural motion accelerates and decelerates.

**Implementation**:
- Use ease-in-out for most movements
- Ease-out for entrances (arrives gently)
- Ease-in for exits (leaves naturally)
- Linear only for mechanical motion

**Common curve**: `cubic-bezier(0.42, 0, 0.58, 1)`

## 7. Arc

**Concept**: Natural movement follows curved paths.

**Implementation**:
- Avoid straight-line motion for organic elements
- Use motion paths or multi-point keyframes
- Parabolic arcs for thrown objects
- Pendulum arcs for swings

## 8. Secondary Action

**Concept**: Supporting actions reinforce the main action.

**Implementation**:
- Add subtle movements that complement primary
- Examples: hair bounce, shadow movement, particle effects
- Should not distract from main action
- Slightly delayed from primary

## 9. Timing

**Concept**: Speed conveys weight, mood, and character.

| Duration | Feel | Use Case |
|----------|------|----------|
| 50-150ms | Snappy | Micro-interactions |
| 150-300ms | Responsive | Button feedback |
| 300-500ms | Smooth | Page transitions |
| 500-800ms | Deliberate | Modal reveals |
| 1000ms+ | Dramatic | Hero animations |

## 10. Exaggeration

**Concept**: Push beyond realistic to enhance clarity.

**Implementation**:
- Scale movements 20-50% beyond subtle
- Overshoot then settle
- More exaggeration = more cartoony
- UI: subtle exaggeration (5-15% overshoot)

## 11. Solid Drawing

**Concept**: Maintain volume and weight in 3D space.

**Implementation**:
- Consider all three dimensions
- Maintain consistent perspective
- Preserve volume during transformations
- Use shadows to ground elements

## 12. Appeal

**Concept**: Make it pleasing and engaging.

**Implementation**:
- Smooth curves over sharp angles
- Consistent timing patterns
- Clear visual feedback
- Satisfying interaction responses
- Balance between predictable and delightful

## Universal Timing Reference

```
Micro-interaction: 100-200ms
Standard feedback: 200-300ms
Content transition: 300-400ms
Page transition: 400-600ms
```

## Universal Easing Reference

```
Enter screen: ease-out (decelerate)
Leave screen: ease-in (accelerate)
On-screen movement: ease-in-out
Bounce/overshoot: spring physics or elastic
```

## Checklist

Before shipping animation:
- [ ] Does it have easing (not linear)?
- [ ] Is timing appropriate for the action?
- [ ] Does it follow arcs where natural?
- [ ] Is there anticipation for significant actions?
- [ ] Do secondary elements have slight delays?
- [ ] Is the focal point clear?
- [ ] Does it feel satisfying?
