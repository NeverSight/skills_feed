---
name: critique
description: |
  CRITIQUE
---

---
description: Adversarial expert review from a specific persona
argument-hint: <persona> [context]
---

# CRITIQUE

Channel a specific expert for adversarial feedback.

## Argument

- `persona` — One of: grug, carmack, ousterhout, fowler, beck, jobs, torvalds

## Personas

| Persona | Lens | Challenges |
|---------|------|------------|
| **grug** | Complexity demon | Over-abstraction, unnecessary layers, big-brain patterns |
| **carmack** | Shippability | Scope creep, premature optimization, not focusing |
| **ousterhout** | Module depth | Shallow modules, pass-through layers, interface complexity |
| **fowler** | Code smells | Duplication, long methods, feature envy, inappropriate intimacy |
| **beck** | Test design | Untestable code, missing TDD, over-mocking |
| **jobs** | Simplicity | Feature bloat, unclear value, lack of craft |
| **torvalds** | Pragmatism | Over-engineering, not shipping, design astronauts |

## What This Does

1. **Load persona** — Channel the expert's perspective and values
2. **Analyze target** — Review code, design, or plan through their lens
3. **Challenge ruthlessly** — Find flaws the persona would hate
4. **Recommend** — What would they demand you change?

## Execution

Launch Task agent with persona instructions:
- Read the relevant code/design
- Apply persona's specific lens
- Produce adversarial critique
- Suggest concrete fixes

## Output

Structured critique:
- **This {persona} hates:** Specific issues found
- **{Persona} demands:** Required changes
- **{Persona} would approve if:** Conditions for acceptance
