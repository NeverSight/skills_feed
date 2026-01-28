---
name: building-router
description: Router for 3D building game mechanics in Three.js. Use when creating survival games, sandbox builders, base builders, or any game with player-constructed structures. Routes to 9 specialized skills for performance, physics, multiplayer, terrain, decay, UX, platform support, and design reference. Start here for building mechanics projects.
---

# Building Mechanics Router

Routes to 9 specialized skills based on game requirements.

## Routing Protocol

1. **Classify** — Single/multiplayer + scale + core features
2. **Match** — Apply signal matching rules below
3. **Combine** — Most games need 3-5 skills together
4. **Load** — Read matched SKILL.md files before implementation

## Quick Route

### Tier 1: Core Mechanics
| Need | Skill | Signals |
|------|-------|---------|
| Spatial queries, collision | `performance-at-scale` | slow, lag, optimize, spatial, collision, thousands |
| Stability, damage, collapse | `structural-physics` | stability, collapse, support, damage, Fortnite, Rust, Valheim |
| Network sync, prediction | `multiplayer-building` | network, multiplayer, sync, server, latency, authoritative |

### Tier 2: Enhanced Features
| Need | Skill | Signals |
|------|-------|---------|
| Slopes, foundations, anchoring | `terrain-integration` | slope, terrain, foundation, ground, pillar, heightmap |
| Timer decay, Tool Cupboard | `decay-upkeep` | decay, upkeep, maintenance, tool cupboard, abandoned |
| Blueprints, undo/redo, preview | `builder-ux` | blueprint, prefab, undo, redo, ghost, preview, selection |

### Tier 3: Platform & Reference
| Need | Skill | Signals |
|------|-------|---------|
| Touch, VR, accessibility | `platform-building` | mobile, touch, VR, hand tracking, colorblind |
| Design analysis, trade-offs | `case-studies-reference` | how does Fortnite/Rust do, compare games, trade-offs |

## Signal Priority

When multiple signals present:
1. **Multiplayer explicit** → `multiplayer-building` required
2. **Scale indicator** → >1000 pieces triggers `performance-at-scale`
3. **Persistence** → Long-running servers trigger `decay-upkeep`
4. **Platform constraint** → Mobile/VR triggers `platform-building`
5. **Default** → `structural-physics` always relevant for building games

## Common Combinations

### Full Survival (Rust-style, 6 skills)
```
performance-at-scale → spatial indexing
structural-physics → stability + damage
multiplayer-building → networking
terrain-integration → foundations on slopes
decay-upkeep → Tool Cupboard + upkeep
builder-ux → blueprints + undo
```

### Battle Royale Building (2 skills)
```
performance-at-scale → fast collision
multiplayer-building → low-latency sync
```

### Single-Player Builder (3-4 skills)
```
structural-physics → stability + damage
terrain-integration → natural terrain
builder-ux → blueprints + undo
performance-at-scale → if >1000 pieces
```

### Persistent Server (4 skills)
```
multiplayer-building → networking
structural-physics → stability
decay-upkeep → automatic cleanup
performance-at-scale → entity management
```

## Decision Table

| Mode | Scale | Terrain | Skills |
|------|-------|---------|--------|
| Single | <1K | Grid | physics + ux |
| Single | <1K | Natural | physics + terrain + ux |
| Single | >1K | Any | performance + physics + ux |
| Multi | Fast | Any | performance + multiplayer |
| Multi | Survival | Any | performance + physics + multiplayer + decay |
| Multi | Persistent | Any | performance + physics + multiplayer + decay + ux |

## Integration Order

When combining skills, wire in this sequence:
1. **Spatial index** → Query foundation for all other systems
2. **Validator** → Uses spatial for neighbor/support detection
3. **Damage** → Uses spatial for cascade radius
4. **Network** → Broadcasts all state changes
5. **Client prediction** → Uses local spatial + validator

## Fallback

- **No scale stated** → Ask: "How many pieces expected?"
- **Unclear mode** → Ask: "Single-player or multiplayer?"
- **Generic "building game"** → Start with `structural-physics` + `builder-ux`

## Reference

See `references/integration-guide.md` for complete wiring patterns and code examples.
