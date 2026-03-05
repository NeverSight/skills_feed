---
name: arc-mastery
description: Use when designing motion paths, character movement trajectories, gesture animations, or any motion that should feel natural rather than robotic.
---

# Arc Mastery

## The Natural Path Principle

Almost all natural movement follows curved paths. Arms swing in arcs. Heads turn on arcs. Thrown objects travel parabolic arcs. When animation moves in straight lines, it immediately feels mechanical and artificial. Arcs are the signature of organic motion.

## Core Theory

**Anatomical basis**: Bodies are systems of hinges and pivots. When a joint rotates, everything attached to it moves in an arc centered on that joint. Straight lines require mechanical rails—biology doesn't have those.

**Physics basis**: Gravity creates parabolic curves on projectiles. Momentum creates curved paths when direction changes. Straight-line direction changes require infinite force.

## Arc Types

**Circular arcs**: Pure rotation around a single pivot (pendulum, door swing)
**Parabolic arcs**: Projectile motion under gravity (jumps, throws)
**S-curves**: Complex motion through multiple pivots (whip crack, spine movement)
**Figure-8 patterns**: Continuous flowing motion (hips during walk, flowing cloth)

## The Pivot Chain

Understanding arcs requires understanding pivot hierarchies:
- Shoulder rotates → elbow travels an arc
- Elbow rotates → wrist travels a compound arc
- Wrist rotates → fingertips travel triple-compound arcs

Each joint adds complexity to the motion path of everything downstream.

## Interaction with Other Principles

**Follow through follows arcs**: Appendages settle along curved paths, not straight returns.

**Anticipation creates arc initiation**: The wind-up often establishes the arc's direction.

**Timing affects arc perception**: Fast motion through arcs needs exaggerated curves to read clearly.

**Overlapping action creates offset arcs**: Secondary elements trace their own arc patterns behind the primary.

## Domain Applications

### UI/Motion Design
- **Page transitions**: Elements should enter/exit on curved paths, not straight slides
- **Menu expansions**: Items fan out on arcs from origin point
- **Gesture responses**: Swipe follow-through curves naturally
- **Notification entries**: Slight arc on slide-in prevents robotic feel
- **Dragging**: Release trajectories should curve based on velocity vector

### Character Animation
- **Walk cycles**: Every limb segment traces arcs; hips follow figure-8
- **Head turns**: Chin traces arc, doesn't translate linearly
- **Arm gestures**: Hand paths curve even during "straight" pointing
- **Jumping**: Parabolic body path with internal rotation arcs

### Motion Graphics
- **Logo reveals**: Elements following arc paths feel choreographed, not random
- **Text animation**: Letter paths curving adds elegance
- **Infographic builds**: Data points connecting along arcs creates flow

### Game Design
- **Projectile physics**: True parabolic arcs for believable ballistics
- **Character controllers**: Turn animations following arcs prevent pivot-in-place
- **Camera movement**: Arc-based camera paths feel cinematic

## Common Mistakes

1. **Straight-line interpolation**: Default animation software behavior—must be corrected manually
2. **Inconsistent arc centers**: Motion arcs should have logical pivot points
3. **Symmetric arcs**: Natural arcs are often asymmetric (fast one way, slow return)
4. **Flat arcs on fast motion**: Quick movements need exaggerated arcs to register

## The 3D Arc Challenge

In 3D, arcs must read from camera view. A perfect arc in world space may look straight or even reversed from certain angles. Always verify arc readability from final camera.

## Arc Drawing Technique

Traditional method: Draw through the motion path with a single stroke. If your pencil naturally curves, the arc is working. If you must consciously redirect, the motion is likely too linear.

## Implementation Heuristic

For any point-to-point motion: add a control point to create a curve. The control point should be offset perpendicular to the direct line, placed closer to the start for ease-out feeling, closer to end for ease-in. For complex motions, trace the intended path first—if it's not curved, it needs work.

Default arc height: 10-20% of travel distance for subtle organic feel, 30-50% for dramatic sweeping motion.
