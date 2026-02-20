---
name: effectorjs
description: Design, refactor, and review Effector state management using modern v23+ patterns. Use when tasks involve createStore/createEvent/createEffect modeling, dataflow with sample/attach/split, scope-safe SSR with fork/allSettled/serialize/hydrate, React integration with useUnit, Solid/Vue integration patterns, fixing scope loss, or replacing anti-patterns such as business logic in watch, imperative calls in effects, and direct getState business reads.
---

# EffectorJS Skill

Use this skill to produce deterministic, scope-safe Effector solutions for new features, refactors, and code reviews.

## Workflow

1. Classify the request:
- `modeling`: create or extend stores/events/effects.
- `refactor`: replace anti-patterns with declarative flows.
- `ssr`: implement or debug scope-safe SSR.
- `review`: assess risks, regressions, and missing tests.
- `legacy-migration`: move old patterns to modern v23+ safely.

2. Load only required references:
- Always start with `references/core-patterns.md`.
- Always load `references/lint-derived-best-practices.md` after core patterns to enforce plugin-backed best practices.
- Add `references/explicit-start.md` when task touches app bootstrap, startup logic, initialization order, tests, scope, or SSR.
- Add `references/computation-priority.md` when task touches ordering, `watch`, sequencing, race-like behavior, or side effects placement.
- Add `references/react-ssr-scope.md` when React/SSR/scope appears.
- Add `references/solid-scope.md` when Solid integration appears.
- Add `references/vue-scope.md` when Vue integration appears.
- Add `references/anti-patterns-and-fixes.md` when fixing or reviewing existing logic.
- Add `references/legacy-migration-map.md` when deprecated APIs/imports are present.
- End with `references/checklists.md` for acceptance criteria.

3. Build solution in this order:
- Model atomic stores and explicit events.
- Define explicit app start (`appStarted`) and keep startup wiring declarative.
- Move side effects to effects.
- Connect units with `sample` first; use `attach` for effect composition.
- Apply scope-first rules (`fork`, `allSettled`) for tests, SPA bootstrap boundaries, and SSR.
- For UI frameworks, use `useUnit` and correct provider wiring.

4. Produce output contract:
- Proposed model topology (stores/events/effects and responsibilities).
- Wiring snippets (`sample`, `attach`, `split` if needed).
- Scope/SSR notes when applicable.
- Lint-derived conformance notes for naming/dataflow/scope/react constraints.
- Test scenarios and acceptance checklist.

## Defaults

- Target Effector modern v23+.
- Treat deprecated/legacy patterns as migration targets, not defaults.
- Prefer minimal, explicit unit graph over clever abstractions.
- Treat lint-derived practices from `eslint-plugin-effector` as baseline constraints.
- Use glossary-consistent terminology in explanations and reviews.

## Glossary Alignment (Effector)

- `Unit`: include `Store`, `Event`, `Effect`, `Domain`, `Scope`.
- `Common unit`: only `Store`, `Event`, `Effect` (reactive update sources for many APIs).
- `Derived store`: read-only store built from other stores (`map`, `combine`, effect-derived stores like `.pending`).
- `Derived store` constraints: do not mutate directly and do not use as `target` in `sample`.
- `Reducer`: `store.on(...)` handlers must return next state; `undefined` or same reference (`===`) means no store update.
- `Watcher`: side effects/debug observability only; watcher return value is ignored.
- `Subscription`: treat unsubscribe handlers as infrastructure concern; avoid manual subscription management in business logic.
- `Purity`: pure functions (`map`, `.on`, transform callbacks) must not imperatively call events/effects.
- `Domain`: namespace for units; `onCreate*` hooks are acceptable for infra-level cross-cutting concerns (logging/instrumentation), not business orchestration.

## Guardrails

- Do not place business logic in `watch`.
- Prefer `sample` over `forward`/`guard` for orchestration.
- Respect computation priority: keep `map`/`.on` pure and avoid side effects in pure computation stages.
- Do not call events/effects imperatively from effect bodies when declarative wiring can express the flow.
- Do not use `$store.getState()` for business dataflow; pass state through `sample` source.
- Do not use derived stores as `target` in `sample`; target writable units/events/effects only.
- Keep `sample`/`guard` options in semantic order: `clock -> source -> filter -> fn -> target`.
- Avoid ambiguous `target` usage (no simultaneous result assignment and explicit `target`).
- Avoid duplicate units in `clock`/`source` arrays and duplicate `.on` handlers for one store-event pair.
- Do not use `sample`/`guard` without runtime effect (must have target or captured result).
- Do not create units dynamically at runtime.
- Keep naming explicit (`$store`, `eventHappened`, `someFx`).
- In React, bind callable units with `useUnit`; avoid raw event/effect usage in JSX handlers.

## Legacy Handling

If legacy code is present:

1. Keep behavior unchanged first.
2. Mark legacy section explicitly.
3. Propose modern replacement with a migration-safe diff strategy.
4. Add tests that prove parity before cleanup.
