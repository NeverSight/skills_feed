---
name: ecs-design
description:
    Use when designing components, systems, or entity structures for jecs in
    Roblox. Use when deciding if data should be one component or multiple, when
    archetype transitions seem expensive, or when choosing entity members vs
    relationships.
metadata:
    author: Christopher Buss
    version: "2026.1.31"
    source:
        Generated from flecs and ecs-faq, scripts at
        https://github.com/christopher-buss/skills
---

# ECS Design Principles

Design guidance for jecs in Roblox.

## Core Mental Model

Think of ECS as a **columnar database**:

| Database | ECS                                      |
| -------- | ---------------------------------------- |
| Table    | Archetype (unique component combination) |
| Column   | Component type                           |
| Row      | Entity                                   |
| Query    | System iteration                         |

**Design question:** "Would I create a separate database column for this?"

## Core References

| Topic          | Description                                               | Reference                                                |
| -------------- | --------------------------------------------------------- | -------------------------------------------------------- |
| Database Model | ECS as columnar database, normalization, fragmentation    | [core-database-model](references/core-database-model.md) |
| Query Design   | Multi-entity queries, constraint decomposition, traversal | [core-query-design](references/core-query-design.md)     |

## Best Practices

| Topic            | Description                                                | Reference                                                            |
| ---------------- | ---------------------------------------------------------- | -------------------------------------------------------------------- |
| Component Design | Granularity decisions, when to split/combine, tags vs data | [best-practices-components](references/best-practices-components.md) |
| System Design    | Single responsibility, avoiding work, ordering, data flow  | [best-practices-systems](references/best-practices-systems.md)       |
| Entity Design    | When to create entities, lazy creation, scaling patterns   | [best-practices-entities](references/best-practices-entities.md)     |

## Quick Decision Guide

| Question                    | Answer                                                              |
| --------------------------- | ------------------------------------------------------------------- |
| Should this be an entity?   | Only if it needs per-instance state that changes over time          |
| Split or combine?           | "Is there a system that needs A but not B?"                         |
| Tag or data component?      | Tags for stable classification (free to add/remove), data for state |
| Relationship or entity ref? | Relationship if reverse lookup needed, entity member otherwise      |
| Is fragmentation bad?       | Only if thousands of archetypes AND you query broadly               |
| When does DOD matter?       | Thousands of entities, per-frame, CPU-bound                         |

## Common Mistakes

| Mistake                               | Why it's bad                     | Fix                                   |
| ------------------------------------- | -------------------------------- | ------------------------------------- |
| Monolithic components                 | Cache waste, tight coupling      | Split by access pattern               |
| Over-atomic components                | Query complexity, invalid states | Combine semantic units                |
| Frequent add/remove on large entities | Copies all component data        | Mutate data component instead         |
| Relationships for every link          | Fragmentation without benefit    | Use entity members for forward-only   |
| Cached query inside system            | Creates new cache every frame    | Create cached queries at module scope |

## Key Principles

1. **Components by access pattern** — Group data that systems need together
2. **Archetype transitions copy data** — Adding/removing components copies all
   data to new archetype; cheap on small entities, expensive on large ones
3. **Entity members vs relationships** — Use entity members for forward lookup,
   relationships for reverse lookup or grouping
4. **Cache queries at module scope** — Never call `.cached()` inside a system
5. **Filter in query** — Use with/without, not code conditionals
6. **Fragmentation can help** — Relationships enable efficient grouped queries

<!--
Source references:
- https://github.com/SanderMertens/flecs/blob/master/docs/DesignWithFlecs.md
- https://github.com/SanderMertens/ecs-faq
-->
