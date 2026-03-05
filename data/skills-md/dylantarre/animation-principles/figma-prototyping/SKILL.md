---
name: figma-prototyping
description: Use when implementing Disney's 12 animation principles in Figma prototypes and Smart Animate
---

# Figma Prototyping Animation Principles

Implement all 12 Disney animation principles using Figma's prototyping and Smart Animate features.

## 1. Squash and Stretch

1. Create two frames: normal and squashed states
2. Scale element: `width: 120%`, `height: 80%`
3. Connect with Smart Animate
4. Use "Ease In and Out" timing

```
Frame 1: Circle 100x100
Frame 2: Circle 120x80 (squashed)
Interaction: Smart Animate, 150ms
```

## 2. Anticipation

Create 3 frames:
1. **Idle** - Starting position
2. **Anticipate** - Wind-up (move opposite to action)
3. **Action** - Main movement

Connect: Idle → Anticipate (100ms) → Action (After Delay)

## 3. Staging

Techniques:
- Use lower opacity on background elements (60-80%)
- Apply blur effect to non-focus areas
- Scale up the hero element
- Use drop shadows for depth hierarchy

## 4. Straight Ahead / Pose to Pose

**Pose to Pose in Figma:**
1. Design key frames as separate screens
2. Connect with Smart Animate
3. Figma interpolates between states

Create: Pose A → Pose B → Pose C frames

## 5. Follow Through and Overlapping Action

1. Create component variants for each element
2. Stagger the state changes across frames
3. Hair/cloth changes 1-2 frames after body

```
Frame 1: Body at A, Hair at A
Frame 2: Body at B, Hair at A (delayed)
Frame 3: Body at B, Hair at B
```

## 6. Slow In and Slow Out

Figma easing options:
- **Ease In** - Starts slow, ends fast
- **Ease Out** - Starts fast, ends slow
- **Ease In and Out** - Slow at both ends (most natural)
- **Custom Bezier** - Fine-tune curve

Default recommendation: `Ease Out` for most UI interactions.

## 7. Arc

1. Create multiple frames along arc path
2. Position element at key points on the curve
3. Use 3+ frames for smooth arc
4. Smart Animate interpolates the path

Or use component rotation with transform origin offset.

## 8. Secondary Action

Layer interactions:
1. Primary: Button scales on tap
2. Secondary: Icon rotates, shadow expands

```
On Click:
  - Button → Scale 1.1, Smart Animate, 150ms
  - Icon → Rotate 15°, Smart Animate, 100ms (starts simultaneously)
```

## 9. Timing

| Duration | Use Case |
|----------|----------|
| 100ms | Micro-interactions, button feedback |
| 200ms | Standard transitions |
| 300ms | Page transitions, modals |
| 400-500ms | Complex reveals |
| 800ms+ | Dramatic, attention-getting |

## 10. Exaggeration

Push beyond subtle:
- Scale hover: 1.1x instead of 1.02x
- Rotation: 15° instead of 5°
- Movement: 20px instead of 8px
- Use "Spring" easing for overshoot effect

## 11. Solid Drawing

Create depth with:
- Consistent perspective across frames
- Shadow direction consistency
- Layered elements with proper z-order
- 3D transforms (rotation with perspective)

## 12. Appeal

Design principles:
- Rounded corners (friendly)
- Consistent spacing
- Smooth color transitions
- Satisfying interaction feedback
- Clear visual hierarchy

## Smart Animate Setup

1. **Name layers identically** across frames
2. **Use components** for consistent naming
3. **Match layer hierarchy** for best results
4. **Set transform origin** before animating

## Interaction Settings

```
Trigger: On Click / While Hovering / After Delay
Action: Navigate To / Smart Animate
Animation: Smart Animate
Easing: Ease Out
Duration: 200ms
```

## Component Variants for States

Create variants:
- `State=Default`
- `State=Hover`
- `State=Active`
- `State=Disabled`

Use "Change To" interaction with Smart Animate between variants.

## Pro Tips

1. **Use "While Hovering"** for reversible animations
2. **After Delay** chains create sequences
3. **Overflow: Hidden** on frames clips animations
4. **Interactive Components** for reusable micro-interactions
5. Preview with **Present** mode (Play button)
