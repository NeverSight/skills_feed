---
name: case-studies-reference
description: Game building mechanics case studies and decision frameworks. Use when designing building systems, evaluating trade-offs, or learning from existing games. Reference-only skill with detailed analysis of Fortnite, Rust, Valheim, Minecraft, No Man's Sky, and Satisfactory building systems.
---

# Case Studies Reference

Detailed analysis of building systems from successful games, plus decision frameworks for new projects.

## Quick Reference

| Game | Building Focus | Physics | Scale | Key Innovation |
|------|---------------|---------|-------|----------------|
| Fortnite | Combat/action | Arcade | Small | Edit system, speed |
| Rust | Survival/raids | Heuristic | Large | Tool Cupboard, decay |
| Valheim | Exploration | Heuristic | Medium | Stability from ground |
| Minecraft | Creativity | None | Infinite | Voxel simplicity |
| No Man's Sky | Base building | Minimal | Medium | Snap points, free place |
| Satisfactory | Factory | Grid-based | Large | Hybrid grid/free |

## When to Use This Skill

Use case studies when making design decisions such as which physics model to implement, how to handle multiplayer building, choosing between grid and free placement, and deciding on decay/upkeep systems. The analyses provide concrete examples of trade-offs and their outcomes.

## Reference Documents

See `references/` for detailed documentation covering game-by-game breakdowns of building mechanics and performance strategies, decision matrices for common architectural choices, anti-patterns identified from games that struggled, and architectural recommendations organized by game genre.

## Decision Framework

For quick decisions, use the matrices in `game-analyses.md`:

**Physics Mode Selection:** Are you building a survival game where building is about shelter? Use heuristic physics like Rust or Valheim. Is building core to moment-to-moment combat? Use arcade physics like Fortnite. Is engineering challenge the point? Consider realistic physics with caution since Medieval Engineers showed this approach frustrates most players.

**Multiplayer Architecture:** Competitive and PvP games require server-authoritative building with latency accepted as the cost of security. Cooperative games can use client prediction with server reconciliation for responsive feel. Single-player can use fully client-side for maximum responsiveness.

**Persistence Strategy:** Long-running servers need decay and cleanup. Rust's model combines gameplay balance through resource sinks with server health through automatic cleanup. Without decay, servers accumulate abandoned bases until performance degrades.

## Key Insights Summary

Rust demonstrates that decay serves dual purposes: gameplay balance by forcing maintenance, and server health by cleaning abandoned structures. Valheim shows that "magic force from ground" stability is more intuitive than realistic physics. Fortnite proves that speed and simplicity trump realism for action games. Satisfactory's hybrid approach of grid for structures plus free placement for conveyors satisfies both organized and creative builders.

## Related Skills

This reference skill pairs with implementation skills that provide working code for the patterns discussed here. Use `performance-at-scale` for spatial indexing, `structural-physics` for stability systems, `multiplayer-building` for networking, `terrain-integration` for foundation systems, `decay-upkeep` for maintenance systems, and `builder-ux` for user experience patterns.
