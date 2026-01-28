---
name: game-feel
description: >
  Game feel consulting based on Steve Swink's "Game Feel: A Game Designer's
  Guide to Virtual Sensation" (Morgan Kaufmann, 2009). Use when helping with
  control responsiveness, input mapping, physics tuning, avatar movement,
  jump mechanics, polish effects, or analyzing why controls feel "floaty",
  "tight", "responsive", or "sluggish". Covers the psychology of real-time
  control, metrics for measuring feel, and practical tuning guidance.
  NOT for general game design - focused specifically on the tactile sensation
  of controlling virtual objects.
---

# Game Feel Skill

A framework for understanding, measuring, and creating satisfying game controls based on Steve Swink's comprehensive analysis.

## Core Definition

**Game feel** is the tactile, kinesthetic sense of manipulating a virtual object. It's the sensation of control—that visceral feeling of steering, jumping, and interacting that exists somewhere between player and game.

> "Game feel is an invisible art. If a designer's done their job correctly, the player will never notice it. It will just seem right."

---

## The Three Building Blocks

Game feel requires all three elements working together:

| Element | Definition | Without It |
|---------|------------|------------|
| **Real-Time Control** | Continuous, immediate response to input | Feels like giving orders, not controlling |
| **Simulated Space** | Collision and physics in a virtual world | No sense of physical interaction |
| **Polish** | Effects that emphasize interactions | Flat, lifeless, unconvincing |

---

## Human Perception Thresholds

### The Correction Cycle
Players perceive, think, and act in ~240ms cycles:
- Perceptual processor: ~100ms
- Cognitive processor: ~70ms  
- Motor processor: ~70ms

### Critical Thresholds

| Threshold | Value | Effect |
|-----------|-------|--------|
| **Motion illusion** | 10+ fps | Below this, no sense of movement |
| **Smooth motion** | 30+ fps | Movement feels fluid |
| **Instantaneous response** | <50ms | Feels like direct control |
| **Noticeable lag** | 100-200ms | Sluggish but usable |
| **Broken control** | >240ms | Player notices delay, feel breaks down |

> "At 50ms response, the game feels like an extension of your body. Above 100ms, you notice lag. Above 240ms, real-time control is broken."

**See**: `references/perception-thresholds.md`

---

## The Six Metrics of Game Feel

### 1. Input
The physical device and signals it sends.

**Measure**: Sensitivity, states, signal types (Boolean vs continuous), physical ergonomics

### 2. Response
How input maps to game state changes.

**Measure**: Direct vs indirect mapping, simulation complexity, ADSR envelopes

### 3. Context  
The spatial environment providing meaning to motion.

**Measure**: Object spacing relative to avatar speed, collision density, level layout

### 4. Polish
Effects that emphasize and sell interactions.

**Measure**: Particles, screen shake, animation sync, sound design

### 5. Metaphor
What the game represents and expectations it creates.

**Measure**: Realism vs abstraction, player expectations, genre conventions

### 6. Rules
Game rules that affect moment-to-moment feel.

**Measure**: Health systems, risk/reward, state changes, ability unlocks

**See**: `references/six-metrics.md`

---

## The ADSR Envelope for Game Feel

Borrowed from audio synthesis, describes how response changes over time:

```
     Sustain ___________
    /                   \
   / Attack      Decay   \ Release
  /                       \
_/                         \_____
```

| Phase | Description | Example (Mario Jump) |
|-------|-------------|---------------------|
| **Attack** | Time to reach full response | Jump force ramps up as button held |
| **Decay** | Settling to sustained level | Initial burst settles |
| **Sustain** | Maintained level while input held | Maximum jump height maintained |
| **Release** | Falloff after input stops | Gravity takes over on release |

**Key insight**: Most "floaty" vs "tight" feelings come from Attack and Release times.

**See**: `references/adsr-tuning.md`

---

## Common Feel Vocabulary

| Term | Meaning | Typical Cause |
|------|---------|---------------|
| **Tight** | Precise, immediate response | Short attack, high acceleration, low release |
| **Floaty** | Loose, delayed, drifty | Long attack/release, high inertia |
| **Responsive** | Does what you want immediately | <100ms response, direct mapping |
| **Sluggish** | Delayed, heavy feeling | >150ms response, long attack |
| **Slippery** | Hard to stop precisely | Low friction, long release |
| **Sticky** | Hard to start moving | High friction, long attack |
| **Weighty** | Sense of mass and momentum | Acceleration curves, gravity strength |
| **Snappy** | Quick state transitions | Short attack AND release |

---

## Simulation Fundamentals

### Position vs Velocity vs Acceleration

| Level | What Changes | Feel |
|-------|--------------|------|
| **Set Position** | Teleport directly | Stiff, robotic (Donkey Kong) |
| **Set Velocity** | Change speed directly | Responsive but unnatural |
| **Apply Force** | Add acceleration | Fluid, physical (Mario, Asteroids) |

### The Asteroids Principle
**Separate thrust from rotation** for expressive space-feel:
- Rotation: Direct, instant (no simulation)
- Thrust: Adds force in facing direction (simulated)
- Result: Ship feels on-the-edge-of-control but never actually out of control

### The Mario Principle  
**Separate horizontal and vertical systems**:
- Horizontal: Acceleration, max speed, deceleration, run modifier
- Vertical: Jump force, gravity, fall gravity (3x normal!), terminal velocity
- Button hold time affects jump height (with min/max limits)

**See**: `references/simulation-recipes.md`

---

## The Mario Jump Recipe

The most-analyzed jump in game history:

### Horizontal Movement
```
Walk acceleration → Walk max speed
Run acceleration → Run max speed (B held)
Air acceleration (reduced)
Deceleration (same for walk/run)
```

### Vertical Movement
```
Initial jump force (instant, large)
Gravity (constant, moderate)
Jump button hold → extends upward force (with max time)
Early release → force artificially set to low value
Apex detection → gravity triples for descent
Terminal velocity cap
```

### The "Hack" That Makes It Work
When player releases jump early:
1. Check if upward velocity > threshold
2. If yes, instantly set velocity to preset low value
3. This creates consistent arc shapes regardless of release timing

**See**: `references/mario-mechanics.md`

---

## Polish That Matters

### The Three-Tier Impact System
Light / Medium / Hard impacts each get:
- Distinct animation
- Distinct sound
- Distinct visual effect (particles, screen shake)

### Sound-Motion Harmony
- Rising pitch = rising motion (Mario's jump sound)
- Impact sounds match visual scale
- Footsteps sync with animation frames
- Material-specific sounds (metal, grass, stone)

### Crossover Sensation
Multiple mechanics should feel bound by the same physics:
- Swimming feels floaty *because* running feels grounded
- Flying defies *the same gravity* that affects jumping
- Contrast creates perceived consistency

**See**: `references/polish-effects.md`

---

## Context: Level Design for Feel

### Spatial Relationships Must Match Mechanics
- Jump heights → platform heights
- Run speed → corridor widths  
- Stopping distance → gap sizes before hazards

### The "Just Right" Principle
Objects should be spaced so the intended move *just barely* works:
- Long Jump gaps: exactly Long Jump distance
- Triple Jump heights: exactly Triple Jump apex
- Creates sense of mastery when executed

### Soft Boundaries
Use physics to guide, not walls to block:
- Steep inclines cause sliding (Mario 64)
- Water slows movement
- Winds push in intended directions

> "Players don't feel the direct intervention of the designer. The limit feels like a logical consequence rather than an overt constraint."

**See**: `references/spatial-context.md`

---

## Debugging Feel Problems

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| "Floaty" | Long attack/release times | Shorten acceleration curves |
| "Sluggish" | High response lag | Reduce input-to-display latency |
| "Slippery" | Low deceleration | Increase friction/deceleration |
| "Stiff" | No acceleration curve | Add attack phase to movement |
| "Unresponsive" | Input not registering | Check input polling rate |
| "Unpredictable" | Variable trajectories | Use fixed special-move arcs |
| "Weightless" | Weak gravity | Increase fall gravity especially |

---

## Principles of Good Game Feel

1. **Predictable special moves** — Fixed trajectories for precision maneuvers
2. **Variable basic moves** — Expressive range for moment-to-moment control
3. **Consistent abstraction** — Simple physics, but self-consistent
4. **Exceed metaphor expectations** — Feel more real than graphics suggest
5. **Polish harmonizes** — Sound, visual, animation tell same story
6. **Context matches capability** — Level design respects avatar limits
7. **Response < 100ms** — Maintain instantaneous feel
8. **Contrast creates variety** — Different mechanics feel different

---

## Quick Reference: Classic Feel Profiles

### Asteroids (Floaty Space)
- Thrust separate from rotation
- Very low friction (4+ seconds to stop)
- Screen wrap containment
- Rotation: instant, no simulation

### Super Mario Bros (Platformer Gold Standard)
- Separate horizontal/vertical systems
- Variable jump height (button hold)
- Triple gravity on descent  
- Run modifier changes acceleration AND max speed
- Reduced air control

### Mario 64 (3D Translation)
- Camera-relative thumbstick control
- Incline-based sliding physics
- Multiple jump types with fixed trajectories
- Carving turn interpolation
- Ground pound as precision landing tool

**See**: `references/classic-profiles.md`

---

## Key Mantras

- **"The game should feel like an extension of your body."**
- **"Separate systems, consistent world."** — Independent mechanics, unified physics.
- **"Exceed the metaphor."** — Feel better than it looks.
- **"Fixed for precision, variable for expression."** — Special moves vs basic moves.
- **"Polish is not optional."** — Effects sell the interaction.
- **"240ms is the wall."** — Response time ceiling for real-time control.
