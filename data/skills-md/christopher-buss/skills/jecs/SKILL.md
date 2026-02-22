---
name: jecs
description:
    Use when building ECS-based games in Roblox with roblox-ts using jecs for
    entities, components, queries, and relationships
metadata:
    author: Christopher Buss
    version: "2026.1.29"
    source:
        Generated from https://github.com/Ukendio/jecs, scripts at
        https://github.com/christopher-buss/skills
---

> Based on jecs v0.9.0, generated 2026-01-29

High-performance Entity Component System for Luau/roblox-ts. Features entity
relationships, archetype storage, 800k entities at 60fps.

## Core References

| Topic            | Description                                            | Reference                                  |
| ---------------- | ------------------------------------------------------ | ------------------------------------------ |
| World & Entities | World creation, entities, components, tags, singletons | [core-basics](references/core-basics.md)   |
| Queries          | Query system, filters (with/without), caching          | [core-queries](references/core-queries.md) |

## Features

| Topic                 | Description                                            | Reference                                                      |
| --------------------- | ------------------------------------------------------ | -------------------------------------------------------------- |
| Pairs & Relationships | Entity pairs, ChildOf, wildcards, relationship queries | [feature-pairs](references/feature-pairs.md)                   |
| Component Hooks       | OnAdd, OnChange, OnRemove lifecycle hooks              | [feature-hooks](references/feature-hooks.md)                   |
| Signals               | Multiple listeners with added/changed/removed signals  | [feature-signals](references/feature-signals.md)               |
| Cleanup Traits        | OnDelete, OnDeleteTarget, cascade deletion policies    | [feature-cleanup-traits](references/feature-cleanup-traits.md) |

## Best Practices

| Topic           | Description                                       | Reference                                                                      |
| --------------- | ------------------------------------------------- | ------------------------------------------------------------------------------ |
| Archetypes      | Archetype storage, transitions, fragmentation     | [best-practices-archetypes](references/best-practices-archetypes.md)           |
| Change Tracking | Delta detection, dirty flags, networking patterns | [best-practices-change-tracking](references/best-practices-change-tracking.md) |

## Advanced

| Topic        | Description                                 | Reference                                  |
| ------------ | ------------------------------------------- | ------------------------------------------ |
| Advanced API | Preregistration, bulk ops, TypeScript types | [advanced-api](references/advanced-api.md) |
