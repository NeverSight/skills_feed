---
name: follow-through-overlapping
description: Use when animating multi-part objects, character appendages, fabric, hair, or any motion requiring realistic drag, momentum, and settling behavior.
---

# Follow Through & Overlapping Action Mastery

## The Momentum Principle

Nothing stops all at once. When a character halts, their hair keeps moving. When a car brakes, passengers lurch forward. Follow through and overlapping action capture how different parts of a system respond to forces at different rates—the principle that makes animation feel physically grounded.

## Core Theory: Two Related Concepts

**Follow Through**: When the main body stops, appendages continue moving due to momentum, then settle. The termination behavior of motion.

**Overlapping Action**: Different parts move at different rates throughout motion, not just at stops. Hair doesn't start moving when the head starts—it drags behind, then catches up. The continuous offset of timing.

## The Drag Hierarchy

Parts further from the root of motion drag more:
1. **Root** (hips, torso): Moves first, stops first
2. **Primary extensions** (limbs, head): Slight delay
3. **Secondary extensions** (hands, facial features): More delay
4. **Tertiary elements** (fingers, hair, cloth): Maximum drag

Each level follows the previous, creating cascading waves of motion.

## Physical Properties Affecting Drag

- **Mass**: Heavier elements have more follow through
- **Flexibility**: Softer materials show more overlapping action
- **Air resistance**: Flat/wide surfaces drag more
- **Attachment point**: Loose connections create greater offset

## Interaction with Other Principles

**Timing defines follow through duration**: Fast stops = long follow through; slow stops = subtle settling.

**Arcs govern the follow through path**: Appendages swing through curved trajectories, not linear ones.

**Secondary action is often follow through**: The supporting motion that enriches without distracting.

**Squash/stretch appears in settling**: Objects compress slightly when follow through terminates.

## Domain Applications

### UI/Motion Design
- List scrolling: inertial continuation past finger release
- Card stacks: sequential settling with offset timing
- Modal dismissal: background elements settle after foreground
- Pull-to-refresh: elastic overshoot and return
- Notification badges: bounce and settle on count change

### Character Animation
- Hair and cloth simulation: constant overlapping action
- Tail motion: follows body path with significant delay
- Facial features: cheeks, jowls follow head rotation
- Walk cycles: arm swing offsets from leg timing
- Jump landing: body compresses, then appendages catch up

### Logo and Typography
- Word reveals: letters arrive with staggered settling
- Logo builds: elements land sequentially, each with follow through
- Kinetic typography: phrases move with internal timing offsets

### Physics-Based UI
- Drag and drop: object continues briefly past release point
- Elastic boundaries: content follows finger, then snaps back
- Spring animations: natural overshoot and settling

## Common Mistakes

1. **Everything stopping simultaneously**: Creates robotic, mechanical feel
2. **Excessive follow through**: Elements feel disconnected, floaty
3. **No hierarchy**: All parts moving with same delay
4. **Linear settling**: Follow through should ease out, not stop abruptly

## The Stagger Formula

For believable overlapping action, offset secondary elements by 2-4 frames (at 24fps) per level of hierarchy. Root moves on frame 1, primary on frame 2-3, secondary on frame 4-6, tertiary on frame 6-10.

## The Settling Curve

Follow through should never snap to rest. Use ease-out curves with slight overshoot:
- Quick initial movement past rest position
- Slower return toward rest
- Possible micro-overshoot in opposite direction
- Final ease to stillness

## Implementation Heuristic

Identify all elements that could move independently. Assign each a drag value based on mass, flexibility, and distance from root. Apply timing offsets proportional to drag. Add settling oscillation to termination. When motion feels stiff, you probably need more overlapping action.
