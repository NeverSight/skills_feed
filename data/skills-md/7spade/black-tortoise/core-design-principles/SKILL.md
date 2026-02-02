---
name: core-design-principles
description: Apply Black-Tortoise design principles (Occam, cohesion/coupling, tool-first assembly, explicit boundaries, deletion-friendly evolution) to a concrete change request; use as a pre-flight checklist before writing code.
---

# Core Design Principles (Operational Checklist)

## Use when
- A task feels “easy to overbuild” (new helpers, new layers, new abstractions).
- You’re not sure where code should live.
- You need to choose between “quick fix” vs “correct boundary”.

## Inputs (ask/confirm)
- What capability/bounded context owns this change?
- What is the smallest stable interface needed by the next layer?
- Where are the side effects (if any)?

## Workflow (tool-first → assembly)
1. Identify the **tool**: the smallest reusable unit (pure function, port, adapter, store method).
2. Place it in the **owner** (capability / workspace / eventing / integration) without cross-context imports.
3. Add the **assembly**: facade/effect/component that wires it, preserving unidirectional flow.
4. Verify **deletion path**: removing the feature should be mostly deleting code, not untangling.

## Hard checks (fail fast)
- No new cross-layer imports that violate Presentation → Application → Domain.
- No domain-side framework imports or side effects.
- No “god” utilities; prefer small, intention-revealing APIs.
- State stays centralized; UI binds to signals.

## References
- `.github/instructions/05-design-principles-copilot-instructions.md`
- `AGENTS.md` and `src/app/**/AGENTS.md`
