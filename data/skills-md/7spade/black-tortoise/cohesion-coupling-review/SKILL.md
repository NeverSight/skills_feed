---
name: cohesion-coupling-review
description: Review a proposed change for high cohesion/low coupling; recommends the smallest boundary-safe refactor (ownership, minimal public surface, no reach-in imports).
---

# High Cohesion / Low Coupling (Review Skill)

## Use when
- A change touches multiple folders/layers/capabilities.
- You’re tempted to import a file from another capability.
- “Shared” is being considered for convenience.

## Checklist (fast)
1. Ownership: which capability/bounded context owns the rule/data?
2. Cohesion: is the logic colocated with its change reason?
3. Coupling: are dependencies narrow (ports/events) rather than concrete imports?
4. Public surface: can exports be reduced to the minimal stable interface?
5. Import hygiene: any deep imports into another capability/layer?
6. Promotion: does it truly qualify for `shared` (2+ contexts, no business policy)?

## Smallest fixes (preferred order)
- Move code to the owner (increase cohesion).
- Introduce/adjust a port or event (reduce coupling).
- Narrow exports / add an explicit entry point (stabilize interface).
- Only then consider `shared` (if it meets promotion rules).

## References
- `.github/instructions/06-cohesion-coupling-copilot-instructions.md`
- `.github/instructions/05-design-principles-copilot-instructions.md`
- `scripts/dependency-cruiser.js`

