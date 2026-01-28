---
name: particles-router
description: Decision framework for particle system projects. Routes to specialized particle skills (gpu, physics, lifecycle) based on task requirements. Use when building particle effects or needing guidance on which particle techniques to combine.
---

# Particles Router

Routes to 3 specialized particle system skills based on task requirements.

## Routing Protocol

1. **Classify** — Identify particle effect type and scale
2. **Match** — Find skill(s) with highest signal match
3. **Combine** — Most particle systems need 2-3 skills together
4. **Load** — Read matched SKILL.md files before implementation

## Quick Route

### Tier 1: Core (Always Consider)

| Task Type | Skill | Primary Signal Words |
|-----------|-------|---------------------|
| Rendering | `particles-gpu` | points, instanced, buffer, shader, thousands, performance |
| Motion | `particles-physics` | gravity, wind, attract, force, velocity, turbulence, collision |
| Spawning | `particles-lifecycle` | emit, spawn, fade, trail, pool, birth, death, age |

## Signal Matching Rules

### Priority Order

When multiple signals present, resolve by priority:

1. **Performance concern** — "millions of particles" → `particles-gpu` first
2. **Motion type** — "swirling", "attracted to" → `particles-physics`
3. **Emission pattern** — "burst", "continuous", "trails" → `particles-lifecycle`
4. **Default** — All three skills usually needed together

### Confidence Scoring

- **High (3+ signals)** — Route immediately
- **Medium (1-2 signals)** — Include all three skills (typical)
- **Low (0 signals)** — Ask: "Describe the particle effect you want"

## Common Combinations

### Basic Particle System (All 3 skills)

```
particles-gpu       → Buffer setup, shader rendering
particles-physics   → Gravity, basic motion
particles-lifecycle → Emission, fade out
```

Wiring: GPU provides rendering foundation, lifecycle handles spawning/death, physics adds motion.

### Snow/Rain Effect (3 skills)

```
particles-gpu       → Points with texture
particles-physics   → Gravity, wind, turbulence
particles-lifecycle → Continuous emission, recycling
```

Wiring: Lifecycle emits continuously, physics handles falling + drift, GPU renders efficiently.

### Explosion (3 skills)

```
particles-gpu       → Instanced or points rendering
particles-physics   → Radial velocity, drag
particles-lifecycle → Burst emission, fade + shrink
```

Wiring: Lifecycle bursts particles, physics applies outward force + slowdown, GPU handles scale.

### Fire/Smoke (3 skills)

```
particles-gpu       → Custom shader with noise
particles-physics   → Upward force, turbulence
particles-lifecycle → Continuous emit, color gradient, size over life
```

Wiring: Lifecycle manages color/size curves, physics adds flicker motion, GPU renders with blend modes.

### Swarm/Flock (2-3 skills)

```
particles-gpu       → Instanced mesh (if 3D shapes)
particles-physics   → Attractors, flow fields, separation
particles-lifecycle → (Optional) Population management
```

Wiring: Physics dominates with behavioral forces, GPU handles rendering.

### Magic Trail (3 skills)

```
particles-gpu       → Points with glow shader
particles-physics   → Follow path, slight randomness
particles-lifecycle → Trail history, fade along length
```

Wiring: Lifecycle stores position history, GPU renders with alpha gradient.

### Confetti (3 skills)

```
particles-gpu       → Instanced flat planes
particles-physics   → Gravity, tumbling rotation, air resistance
particles-lifecycle → Burst emission, ground collision death
```

Wiring: Physics handles realistic falling, lifecycle manages burst and cleanup.

## Decision Table

| Effect Type | GPU Focus | Physics Focus | Lifecycle Focus |
|-------------|-----------|---------------|-----------------|
| Stars/sparkle | Points, static | Minimal | Twinkle (alpha) |
| Snow/rain | Points, texture | Gravity, wind | Continuous, recycle |
| Fire | Shader, blend | Upward, turbulence | Color/size curves |
| Explosion | High count | Radial, drag | Burst, fade |
| Smoke | Soft shader | Rise, curl | Slow fade, grow |
| Swarm | Instanced | Attractors, fields | Spawn/death |
| Trail | Line or points | Path following | Position history |
| Dust | Small points | Brownian | Random spawn |

## Particle Count Guidelines

| Count | Approach | Skills Priority |
|-------|----------|-----------------|
| < 100 | Simple, any approach | lifecycle > physics > gpu |
| 100 - 1,000 | Points or instanced | All equal |
| 1,000 - 10,000 | GPU-focused | gpu > physics > lifecycle |
| 10,000 - 100,000 | GPU essential | gpu >> physics (shader) > lifecycle |
| > 100,000 | Full GPU/compute | gpu only, physics in shader |

## Skill Dependencies

```
particles-gpu (rendering foundation)
├── particles-physics (motion layer)
└── particles-lifecycle (management layer)
```

- `particles-gpu` is always needed for rendering
- `particles-physics` and `particles-lifecycle` are independent but complementary
- For simple effects, you might skip physics OR lifecycle, rarely both

## Fallback Behavior

- **Unknown effect** → Start with all three skills
- **Performance issues** → Focus on `particles-gpu` optimization
- **Motion problems** → Deep-dive `particles-physics`
- **Spawning/timing issues** → Focus on `particles-lifecycle`

## Quick Decision Flowchart

```
User Request
     │
     ▼
┌─────────────────────────┐
│ Rendering particles?    │──Yes──▶ particles-gpu (always)
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ Movement/forces needed? │──Yes──▶ + particles-physics
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ Birth/death/emission?   │──Yes──▶ + particles-lifecycle
└─────────────────────────┘
     │
     ▼
Most effects need all 3 skills
```

## Effect Recipes

### Quick Start Templates

| Effect | Start With |
|--------|------------|
| Ambient dust | gpu (points) + lifecycle (continuous) |
| Button sparkle | gpu (points) + lifecycle (burst, fade) |
| Character trail | gpu + lifecycle (trail) |
| Weather | All three |
| Magic spell | All three |
| Data visualization | gpu + lifecycle |

## Integration with Other Domains

| Combined With | Use Case |
|---------------|----------|
| `shader-noise` | Turbulent motion, organic shapes |
| `shader-effects` | Glow, chromatic aberration on particles |
| `r3f-performance` | Optimization, culling, LOD |
| `gsap-fundamentals` | Scripted particle animations |
| `audio-reactive` | Music-driven particle effects |

## Reference

See individual skill files for detailed patterns:

- `/mnt/skills/user/particles-gpu/SKILL.md`
- `/mnt/skills/user/particles-physics/SKILL.md`
- `/mnt/skills/user/particles-lifecycle/SKILL.md`
