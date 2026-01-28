---
name: r3f-router
description: Decision framework for React Three Fiber projects. Routes to specialized R3F skills (fundamentals, geometry, materials, performance, drei) based on task requirements. Use when starting an R3F project or needing guidance on which R3F skills to combine.
---

# R3F Router

Routes to 5 specialized React Three Fiber skills based on task requirements.

## Routing Protocol

1. **Classify** — Identify primary task type from user request
2. **Match** — Find skill(s) with highest signal match
3. **Combine** — Most R3F tasks need 2-4 skills together
4. **Load** — Read matched SKILL.md files before implementation

## Quick Route

### Tier 1: Core (Always Consider)

| Task Type | Skill | Primary Signal Words |
|-----------|-------|---------------------|
| Scene setup | `r3f-fundamentals` | canvas, scene, camera, lights, render, useFrame |
| Custom shapes | `r3f-geometry` | geometry, vertices, bufferAttribute, instancing, mesh |
| Surface appearance | `r3f-materials` | material, shader, texture, uniform, color, PBR |

### Tier 2: Enhanced (Add When Needed)

| Task Type | Skill | Primary Signal Words |
|-----------|-------|---------------------|
| Optimization | `r3f-performance` | performance, FPS, draw calls, LOD, culling, memory |
| Helpers/Controls | `r3f-drei` | OrbitControls, useGLTF, Text, Environment, Html |

## Signal Matching Rules

### Priority Order

When multiple signals present, resolve by priority:

1. **Explicit component** — "add OrbitControls" → `r3f-drei`
2. **Specific technique** — "use instancing" → `r3f-geometry`
3. **Problem domain** — "custom shader" → `r3f-materials`
4. **Default tier** — Fall back to `r3f-fundamentals`

### Confidence Scoring

- **High (3+ signals)** — Route immediately
- **Medium (1-2 signals)** — Route with `r3f-fundamentals` as base
- **Low (0 signals)** — Ask user for clarification

## Common Combinations

### Basic 3D Scene (3 skills)

```
r3f-fundamentals → Canvas, camera, lights, render loop
r3f-drei         → OrbitControls, Environment, helpers
r3f-materials    → MeshStandardMaterial, textures
```

Wiring: Fundamentals provides scene structure, drei adds controls and environment, materials define appearance.

### Custom Shader Effect (3 skills)

```
r3f-fundamentals → Scene setup, useFrame for animation
r3f-geometry     → Custom BufferGeometry if needed
r3f-materials    → ShaderMaterial, uniforms, GLSL
```

Wiring: Fundamentals handles render loop, materials provides shader infrastructure.

### Particle System (4 skills)

```
r3f-fundamentals → Scene, camera, render loop
r3f-geometry     → InstancedMesh, buffer attributes
r3f-materials    → Custom particle shader
r3f-performance  → Optimization, draw call reduction
```

Wiring: Geometry provides instancing, materials handles particle rendering, performance ensures smooth animation.

### Product Visualization (4 skills)

```
r3f-fundamentals → Scene structure
r3f-drei         → useGLTF, Environment, ContactShadows, OrbitControls
r3f-materials    → PBR materials, environment mapping
r3f-performance  → LOD, texture optimization
```

Wiring: Drei loads model and provides studio setup, materials ensures realistic rendering.

### Large Scene (4 skills)

```
r3f-fundamentals → Base scene management
r3f-geometry     → Merged geometry, instancing
r3f-performance  → LOD, culling, lazy loading
r3f-drei         → Bounds, Preload, Detailed
```

Wiring: Performance strategies combined with geometry optimization for smooth rendering.

## Decision Table

| Scenario | Model Loading | Custom Shapes | Custom Shaders | Optimization | Route To |
|----------|--------------|---------------|----------------|--------------|----------|
| Simple viewer | Yes | No | No | No | fundamentals + drei |
| Custom geometry | No | Yes | No | No | fundamentals + geometry |
| Shader art | No | Maybe | Yes | No | fundamentals + materials + geometry |
| Game/simulation | Maybe | Yes | Maybe | Yes | all skills |
| Product viz | Yes | No | No | Maybe | fundamentals + drei + materials |
| Particles | No | Yes | Yes | Yes | fundamentals + geometry + materials + performance |

## Skill Dependencies

```
r3f-fundamentals (foundation)
├── r3f-geometry (extends fundamentals)
├── r3f-materials (extends fundamentals)
├── r3f-drei (extends fundamentals)
└── r3f-performance (applies to all)
```

- Always start with `r3f-fundamentals`
- `r3f-geometry` and `r3f-materials` often used together
- `r3f-drei` can replace manual implementations
- `r3f-performance` applies optimization to any combination

## Fallback Behavior

- **Unknown task type** → Start with `r3f-fundamentals` + `r3f-drei`
- **No clear signals** → Ask: "What are you trying to render?" and "Any specific effects needed?"
- **Conflicting signals** → Prefer `r3f-drei` abstractions over manual implementations

## Quick Decision Flowchart

```
User Request
     │
     ▼
┌─────────────────────┐
│ Need 3D model?      │──Yes──▶ r3f-drei (useGLTF)
└─────────────────────┘
     │ No
     ▼
┌─────────────────────┐
│ Custom geometry?    │──Yes──▶ r3f-geometry
└─────────────────────┘
     │ No
     ▼
┌─────────────────────┐
│ Custom shader?      │──Yes──▶ r3f-materials
└─────────────────────┘
     │ No
     ▼
┌─────────────────────┐
│ Performance issues? │──Yes──▶ r3f-performance
└─────────────────────┘
     │ No
     ▼
┌─────────────────────┐
│ Controls/helpers?   │──Yes──▶ r3f-drei
└─────────────────────┘
     │ No
     ▼
r3f-fundamentals (default)
```

## Reference

See individual skill files for detailed patterns:

- `/mnt/skills/user/r3f-fundamentals/SKILL.md`
- `/mnt/skills/user/r3f-geometry/SKILL.md`
- `/mnt/skills/user/r3f-materials/SKILL.md`
- `/mnt/skills/user/r3f-performance/SKILL.md`
- `/mnt/skills/user/r3f-drei/SKILL.md`
