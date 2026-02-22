---
name: effector-storage
description: Choose and implement effector-storage persistence patterns for Effector apps. Use when tasks involve persist/createPersist usage, selecting adapters (local/session/query/broadcast/storage/asyncStorage/memory/nil/log), configuring clock/pickup/context/keyPrefix, validating data with contracts, handling done/fail/finally flows, SSR-safe adapter fallback with either, or debugging sync and serialization issues.
---

# Effector Storage Skill

Use this skill to design, implement, and debug `effector-storage` integrations with predictable runtime behavior.

## Workflow

1. Classify the request:
- `adapter-choice`: pick the right adapter for environment and data behavior.
- `integration`: wire `persist`/`createPersist` into existing model flow.
- `contracts-errors`: validate storage payloads and route failures.
- `sync-debug`: investigate cross-tab/query/broadcast synchronization issues.
- `ssr-fallback`: make persistence safe across browser/server runtimes.

2. Load references progressively:
- Start with `references/core-patterns.md`.
- Add `references/adapter-matrix.md` when adapter selection/configuration is needed.
- Add `references/tools-and-composition.md` for `async`, `either`, `farcached`, or composition recipes.
- Add `references/contracts-and-errors.md` for contracts and error channels.
- End with `references/pitfalls-and-checklist.md` before finalizing.

3. Build answer contract:
- Start with a concrete adapter decision and why.
- Provide a minimal working snippet with explicit key strategy.
- List behavior caveats (init timing, sync limits, validation behavior).
- Add verification steps/tests for the chosen flow.

## Defaults

- Target `effector-storage` v7.x behavior.
- Prefer explicit `key` over implicit store names for portability.
- Prefer declarative Effector wiring around `persist` (sample/clock/context units).
- Keep payloads plain and serialization stable (`deserialize(serialize(x))`).

## Guardrails

- Do not omit both `key` and store name.
- Do not use `source === target` for non-store units.
- Do not assume `pickup` still performs automatic initial restore (it disables it).
- Do not assume contract validation prevents writes; invalid values can be persisted and then reported via `fail`.
- Do not treat `broadcast` as durable storage; it is sync-only messaging.

## Practical Extras Boundary

For adapters from `effector-storage-extras`, reuse the same adapter contract and decision flow from this skill, but verify exact API/options in that repository before coding.
