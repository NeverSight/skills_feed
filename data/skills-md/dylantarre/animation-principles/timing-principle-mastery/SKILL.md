---
name: timing-principle-mastery
description: Use when determining animation durations, controlling pacing, establishing rhythm, or making motion feel appropriately weighted and emotionally resonant.
---

# Timing Mastery

## The Weight of Time

Timing is the number of frames (or milliseconds) an action takes. It's deceptively simple—just duration—yet it communicates weight, emotion, and energy more powerfully than any other principle. Change the timing, change the meaning.

## Core Theory

**Physical communication**: Timing tells us about mass and force. Heavy objects start slow, stop slow. Light objects respond instantly. A bowling ball and a balloon falling the same distance—timing alone differentiates them.

**Emotional communication**: Timing tells us about character state. Sluggish timing reads as tired, depressed, or massive. Snappy timing reads as alert, nervous, or lightweight.

## The Frame Rate Foundation

At 24fps (film standard):
- 1-2 frames: Instantaneous (impacts, pops)
- 4-6 frames: Quick (snappy responses)
- 8-12 frames: Standard (natural movement)
- 16-24 frames: Deliberate (weighted, considered)
- 24-48 frames: Slow (dramatic, heavy)
- 48+ frames: Very slow (massive, underwater, dream-like)

At 60fps (UI/games), multiply by 2.5 for equivalent feels.

## Timing Categories

**Physical timing**: Governed by mass, gravity, and force (objective)
**Theatrical timing**: Governed by story needs and emotional beats (subjective)
**Musical timing**: Governed by rhythm and tempo (structural)
**UI timing**: Governed by responsiveness and user perception (functional)

## Interaction with Other Principles

**Slow in/slow out is timing's texture**: The overall duration and the internal spacing work together.

**Anticipation affects timing perception**: A long wind-up makes subsequent action feel faster.

**Staging uses timing for hierarchy**: Important elements move on different timing than subordinate ones.

**Exaggeration often means timing exaggeration**: Stretched holds, compressed actions.

## Domain Applications

### UI/Motion Design
- **Instant (0-100ms)**: Button feedback, toggle switches—no perceptible delay
- **Quick (100-200ms)**: Micro-interactions, hover states—responsive but visible
- **Standard (200-300ms)**: Page transitions, modals—comfortable, comprehensible
- **Deliberate (300-500ms)**: Complex transitions, onboarding—time to absorb
- **Slow (500ms+)**: Dramatic reveals, ambient animation—contemplative

### Character Animation
- **Personality through timing**: Bouncy = fast timing; grumpy = slow timing
- **Mass through timing**: Elephant walk = 24+ frames per step; mouse = 4-6 frames
- **Emotional state**: Depression slows timing; excitement speeds it
- **Age indication**: Young = snappy recovery; old = slow, deliberate

### Motion Graphics
- **Rhythm establishment**: Consistent timing creates beat
- **Contrast through timing**: Slow builds, fast reveals
- **Musical sync**: Animation locked to audio tempo

### Game Design
- **Responsiveness**: Input-to-response timing defines "game feel"
- **Hit stop**: Momentary pause on impact (adds weight)
- **Juice**: Quick, satisfying timing on feedback events

## Common Mistakes

1. **Uniform timing**: Everything same duration feels monotonous
2. **Too fast**: Motion becomes invisible, jerky, unpleasant
3. **Too slow**: Interface feels sluggish, unresponsive
4. **Ignoring context**: Casual game timing in enterprise software

## The Timing Contrast Principle

Timing gains meaning through contrast. A fast action feels fast because something before it was slow. A held pose feels dramatic because motion surrounds it. Monotonous timing lacks emphasis.

## The Duration Hierarchy

Create timing systems where relationships are consistent:
- Base unit (e.g., 200ms)
- Quick = base × 0.5 (100ms)
- Slow = base × 1.5 (300ms)
- Dramatic = base × 2 (400ms)

Systematic timing feels cohesive; random durations feel chaotic.

## The Hold

One of timing's most powerful tools is the absence of motion. Held poses create:
- Emphasis (letting a moment land)
- Anticipation (pregnant pause before action)
- Readability (time for audience to register)

Never underestimate the power of stillness.

## Implementation Heuristic

Start with 200-300ms as default duration for standard interactions. Adjust based on: mass (heavier = longer), distance (further = longer), importance (crucial = longer to register), emotional tone (playful = snappier). When something feels "off," timing is often the culprit—experiment with 50% shorter and 50% longer before other adjustments.
