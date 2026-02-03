---
name: quality-gates
description: Auditing, testing, and architecture-governance instructions for Black-Tortoise, covering when to run `architecture:gate`, update docs/AUDIT-*, ship tests, and satisfy `.github/instructions/64-quality-testing-copilot-instructions.md` before merge.
---

# Quality Gates & Audit Master Guide

## Intent
Document the pre-merge checklist: what gates must pass, which audit artefacts to update, and which tests the repo expects, per `.github/instructions/64-quality-testing-copilot-instructions.md`.

## Gates to Run
- Run `pnpm run architecture:gate` after any structural change (new dependencies, cross-layer imports, new modules); this enforces the dependency cruiser rules described in `.github/instructions/61-architectural-governance-copilot-instructions.md`.
- Before PR, execute `pnpm run lint`, `pnpm run build -- --noEmit`, and the relevant unit suites described in the capability instructions.
- Ensure Husky/lint-staged hooks triggered by `git commit` pass (`eslint` and `tsc --noEmit` per `package.json`).

## Documentation & Audit Tracking
- Update `docs/AUDIT-<module>.md` whenever you change a capability, event, or critical workflow; note invariants, boundaries, and audit findings as specified in `.github/instructions/64-quality-testing-copilot-instructions.md`.
- Document requirements/status in `requirements.md` and `tasks.md` (status values: not-started, in-progress, completed, blocked) before completion.
- Capture `architecture:gate` failures’ logs and include them in your notes so reviewers can see what changed since the last passing gate.

## Testing Expectations
- Cover every critical path and domain invariant touched by your change with tests (Jasmine + Karma for unit stores/domains, Playwright for happy-path flows).
- Use Playwright with resilient selectors (`data-testid`, roles) and emulator resets so tests are deterministic (`.github/skills/e2e-playwright` already describes these patterns).
- When introducing async or signal transitions, do full Arrange-Act-Assert cycles and clean up subscriptions with `takeUntilDestroyed()` or `rxMethod` disposal.

## When to Apply This Skill
- Anytime you add/modify tests, instructions, or GA/QA tasks that must mention gating commands, auditors, or docs.
- Whenever you touch documentation or pipeline scripts so that audit assets remain in sync with the `docs/AUDIT-*` expectations.
