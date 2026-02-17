---
name: data-driven-testing
description: "DEPRECATED: Use testing-best-practices instead. This skill has been retired."
---

## Deprecated

This skill has been replaced by **testing-best-practices**.

Use `testing-best-practices` for all test design, test case generation, and test strategy work.

### What changed

- Test layering policy (unit / integration / e2e) replaces the unit-only DDT focus.
- Markdown tables replace the rigid canonical JSON test-case schema.
- Output is strategy + matrix + implementation plan, not JSON blocks.
- Added: hard rules against fabricated fixtures and invented source locations.
- Added: e2e execution guidance (preflight, async polling, flake handling).
- Added: CI lane guidance (PR smoke vs nightly full).
- Auth-state reuse and idempotent/state-tolerant e2e are first-class concerns.
