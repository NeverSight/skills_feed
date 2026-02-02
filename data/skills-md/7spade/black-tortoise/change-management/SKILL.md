---
name: change-management
description: Keep interfaces stable and changes reviewable; includes ADR-lite guidance and deprecation/deletion checks.
---

# Change Management (Stable Interface / Deletion)

## Use when
- Changing public APIs across layers (ports, facades, stores).
- Introducing a new pattern or architectural decision.

## Workflow
1. Define minimal stable interface (MSI): smallest API callers need.
2. Prefer additive change; if breaking, include migration notes.
3. Add ADR-lite notes (what/why/risks) when boundaries change.
4. Verify deletion path: feature can be removed without global entanglement.

## References
- `.github/instructions/68-change-management-copilot-instructions.md`

