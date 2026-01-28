---
name: galahad
description: how to approach tests, types and coverage
---

# Coding Agent Quality Rules (Galahad Principle)

Based on Jonathan Lange’s “The Galahad Principle”:
https://jml.io/galahad-principle/

Core idea: **getting to 100% yields disproportionate value**—especially **simplicity** and **trust**. When checks are truly “all green”, any new failure is a strong, unambiguous signal; “absence of evidence becomes evidence of absence”.

## Non-negotiables: never evade feedback

Treat **type errors, test failures, pre-commit hooks, lint errors, and coverage warnings** as helpful feedback. Fix root causes.

### Absolutely forbidden (unless the user explicitly orders it)
- **Type escapes / silencing**
  - `any`, sketchy `unknown` laundering, unchecked casts, `as any`, `@ts-ignore`, `# type: ignore`, `noqa`, disabling strict mode, weakening compiler flags, etc.
- **Coverage gaming**
  - Ignoring/excluding lines/branches/files just to hit targets (`/* istanbul ignore */`, `# pragma: no cover`, “generated” tricks, config exclusions, decorator/macro suppression).
- **Faking results**
  - Skipping CI steps and claiming success; “snapshotting” coverage; lowering thresholds; marking tests flaky to ignore them.

## Priorities

Type safety is part of correctness and **outranks tests**.

When tradeoffs exist, prioritize in this order:
1. **Type safety / soundness**
2. **Correctness + meaningful tests**
3. **Clarity / maintainability**
4. **Performance**
5. **Backwards compatibility** (lowest)

Breaking changes are acceptable when they improve verifiability and simplify the system.

## Default workflow (when anything fails)

1. Read the failure output carefully.
2. Restate the real invariant being violated in plain English.
3. Fix the root cause (not the symptom).
4. Improve tests so the behavior is pinned and regressions get caught.
5. Refactor production code if needed to make it easy to type-check and validate.

### Run checks in this order
1. **Typecheck**
2. **Unit tests**
3. **Integration tests**
4. **Lint / pre-commit**
5. **Coverage**

Goal: a repo where “all green” is normal, and any new red is a loud, trustworthy signal.

## “Hard to test” means refactor

If something is hard to test or hard to type:
- Treat it as a **design smell**.
- Refactor towards:
  - smaller pure functions
  - explicit data flow, minimal global state
  - clear boundaries between logic and side effects
  - typed domain models over stringly-typed blobs

## Mocks: don’t overuse them

Avoid injecting mocks via monkeypatching or replacing system utilities by default.

Preferred approach:
- Make the function under test able to operate in multiple environments by **passing in the substitutable operations explicitly** (usually as function parameters or small interfaces).
- Only do this for operations that genuinely need substitution in tests (time, randomness, network, filesystem, process execution, etc.).
- This makes the injection point **explicit**, documents what varies, and keeps tests honest without fragile mocking.

## What “good” looks like

- Types encode invariants; no “trust me” casts.
- Tests assert observable behavior (not implementation trivia).
- Coverage comes from exercising real behavior, not exclusions.
- If a thing can’t be verified cleanly, refactor until it can.

