---
name: slow-in-out-mastery
description: Use when designing easing curves, controlling motion pacing, creating natural acceleration/deceleration, or making movements feel physically grounded.
---

# Slow In / Slow Out Mastery

## The Physics Principle

Objects in the real world don't move at constant speeds—they accelerate from rest and decelerate to stops. Slow in/slow out (also called ease in/ease out) captures this fundamental truth. Without it, animation looks mechanical. With it, motion feels alive.

## Core Theory

**Slow Out** (Ease Out): More drawings clustered at the start of a movement. The object accelerates away from its starting position gradually.

**Slow In** (Ease In): More drawings clustered at the end of a movement. The object decelerates into its final position gradually.

**Linear motion**: Equal spacing between positions. Rare in nature, useful for mechanical elements or stylistic choice.

## The Spacing Principle

Traditional animators controlled this through drawing spacing:
- **Tight spacing** = slow movement (drawings close together)
- **Wide spacing** = fast movement (drawings far apart)

Digital animators control this through easing curves—mathematical functions that describe how values change over time.

## Common Easing Functions

- **Ease Out**: Fast start, slow end (70% of UI animations)
- **Ease In**: Slow start, fast end (exits, departures)
- **Ease In Out**: Slow start and end (elegant, deliberate)
- **Linear**: Constant rate (mechanical, looping)
- **Custom bezier**: Precise control for specific feels

## Interaction with Other Principles

**Timing is modified by easing**: The same duration feels different with different easing. Ease out feels faster than ease in at identical durations.

**Anticipation often uses ease in**: The wind-up accelerates before the fast action.

**Follow through uses ease out**: Settling motion decelerates to rest.

**Squash/stretch intensity follows easing**: More deformation during fast phases, less during slow phases.

## Domain Applications

### UI/Motion Design
- **Page transitions**: Ease out for entrances (fast appearance, settle), ease in for exits
- **Modals**: Ease out scale-up for friendly, non-jarring appearance
- **Buttons**: Ease out on press feedback (immediate response, smooth settle)
- **Loading**: Linear for progress bars (predictable), ease for spinners (organic)
- **Hover states**: Quick ease out to start, ease in out for smooth feel

### Character Animation
- **Jumps**: Slow out from ground (acceleration), slow in to peak (deceleration), fast middle
- **Head turns**: Slow out from rest, slow in to new direction
- **Blinks**: Fast down (almost linear), slow out up (lids dragging)
- **Weight shifts**: Heavy easing reflects mass

### Motion Graphics
- **Text reveals**: Staggered ease outs create cascading arrivals
- **Logo animations**: Carefully crafted curves define brand personality
- **Data visualization**: Ease out for growth, ease in for decrease

### Game Feel
- **Camera movement**: Ease in out for cinematic, quick ease out for responsive
- **Character control**: Ease curves define how "tight" or "floaty" movement feels
- **Impact effects**: Sharp ease in creates punch

## Common Mistakes

1. **Linear everything**: Motion feels robotic and sterile
2. **Too much easing**: Overly soft motion feels sluggish, unresponsive
3. **Wrong easing direction**: Ease in on entrances feels reluctant; ease out on exits feels like the element doesn't want to leave
4. **Ignoring context**: Playful UIs need bouncier curves; professional UIs need subtler easing

## The Bounce and Elastic Extensions

Beyond basic easing:
- **Bounce**: Overshoot with diminishing oscillation (playful, energetic)
- **Elastic**: Overshoot with wobble (stretchy, cartoony)
- **Back**: Slight pullback before motion (adds anticipation)

## The 80/20 Rule

For most UI work: use ease out for 80% of animations (elements responding to user action). Ease out communicates responsiveness—"I heard you and I'm moving." Reserve ease in for departures and de-emphasis.

## Implementation Heuristic

Default to ease out (fast start, slow end) for element appearances and responses. Use ease in for exits. Use ease in out for autonomous animations (not triggered by user). Adjust curve intensity based on brand personality—aggressive curves for dynamic brands, subtle curves for calm brands.
