---
name: compose-state-hoisting
description: Compose state management with a strong state-hoisting preference for Kotlin Compose (Android, Multiplatform, Compose for Web). Use for refactors or new UI that needs clear state ownership, unidirectional data flow, saved state decisions, or guidance on remember/retain/rememberSaveable/rememberSerializable, and for designing stateless composables with event callbacks.
---

# Compose State Hoisting

## Overview
Apply state hoisting and unidirectional data flow to Compose UIs, choosing the right state owner, lifespan, and saving strategy.

For condensed reference and examples, see `references/compose-state-guidance.md`.

## Workflow
1. Identify the state and the logic that reads/writes it.
2. Decide the state owner (lowest common ancestor; or a plain state holder class, or a screen-level state holder like Android ViewModel for complex UI/business logic).
3. Choose the lifespan API (remember/retain/rememberSaveable/rememberSerializable) based on how long it must survive.
4. Make UI composables stateless: pass `value` and event callbacks; state goes down, events go up.
5. Decide what must be saved and how (rememberSaveable, SavedStateHandle, or platform storage).
6. Verify that state and callbacks are not duplicated or leaked.

## Rules of thumb
- Hoist state to the lowest common ancestor of all readers/writers.
- Keep composables stateless: state down, events up.
- Pick the lifespan API explicitly; default to `remember` only for ephemeral UI state.
- Save minimal data and rehydrate anything larger or derived.

## Decision hints
- If multiple parts of the UI must read/write the same state, hoist it.
- If state survives config changes or process death, choose `retain` or `rememberSaveable` and document why.
- For business logic, use a screen-level state holder; do not pass it down the tree.

## Common pitfalls
- Duplicated state owners causing divergence.
- Over-saving large objects in `rememberSaveable`/`SavedStateHandle`.
- Mixing `remember` and `retain` for the same object.

## State Hoisting Rules
- Hoist state to the lowest common ancestor of all composables that read and write it; keep it as close to consumers as possible.
- If multiple states change from the same events, hoist them together.
- Over-hoisting (e.g., hoisting to screen level when a subtree would suffice) is acceptable and safer than under-hoisting; under-hoisting breaks unidirectional flow and creates duplicate sources of truth. Over-hoisting may trigger more recompositions or lose state on navigation.
- Prefer exposing immutable state plus event callbacks from the state owner.

## Stateless vs Stateful Composables
- Provide a stateless API: `value: T` and `onValueChange: (T) -> Unit` (or more specific event lambdas).
- Keep state internal only if no other composable needs to read or change it and the UI logic is simple.
- Offer both stateful and stateless variants when useful; the stateless version is the reusable/testable one.

## Decide Where to Hoist
- **UI element state + simple UI logic**: keep internal or hoist within the UI subtree.
- **Complex UI logic**: move state and UI logic into a plain state holder class scoped to the Composition.
- **Business logic or screen UI state**: hoist to a screen-level state holder (Android: ViewModel; Multiplatform: platform-specific or library solutions like Circuit, Molecule). Do not pass screen-level state holders down the tree; inject at the screen level and pass state/events instead.
- **Deep prop drilling**: for state needed by many distant descendants (theme, user session), consider `CompositionLocal` to avoid passing parameters through many layers. Use sparingly; prefer explicit parameter passing when practical.

## Choose the Correct Lifespan
- `remember`: survives recomposition only; same instance. Use for composition-scoped objects and small internal UI state. Do not use for user input that must be preserved.
- `retain`: survives recomposition + window/configuration changes (Android: activity recreation), not process death. Use for non-serializable objects (players, caches, flows, lambdas). **Do not retain** platform-specific lifecycle objects (Android: Activity, View, Fragment, ViewModel, Context, Lifecycle). **Do not retain** objects that were already created with `remember` by the caller—`retain` and `remember` are mutually exclusive for the same object.
- `rememberSaveable` / `rememberSerializable`: survives recomposition + configuration changes + process death (Android) by saving to the platform's saved state mechanism (Android: Bundle; other platforms may vary). Use for user input or UI state that cannot be reloaded from another source. Restored objects are equal but not the same instance.

**Remember Keys**: Control when state resets by passing keys to `remember(key1, key2) { }`. State recreates when any key changes. Omit keys only when state should survive all recompositions.

## Saving UI State
- Use `rememberSaveable` for UI state hoisted in composables or plain state holders; save only minimal, small data.
- Saved state storage is limited (Android Bundle: ~1MB); do not store large objects or lists. Store IDs/keys and rehydrate from data/persistent storage.
- Android: Use `SavedStateHandle` in a ViewModel for UI element state that must survive process death; keep it small and session-scoped (not persistent app data).
- Do not save full screen UI state; rebuild it from the data layer on restoration.

## Observable Types in Compose
- Convert observable types to `State<T>` before reading in composables.
- `Flow`: use `collectAsState` (platform-agnostic, always collects) or `collectAsStateWithLifecycle` (Android only, lifecycle-aware, pauses collection when UI is not visible).
- `LiveData` (Android): use `observeAsState`.
- For custom observables, create a `State<T>` via `produceState`.

## State Callbacks (RememberObserver / RetainObserver)
- Run initialization side-effects in `onRemembered` / `onRetained`, not in constructors or remember/retain lambdas.
- Always cancel work in `onForgotten` / `onRetired`; handle `onAbandoned` for canceled compositions.
- Keep implementations private; expose safe factory functions like `rememberX()` to avoid misuse.
- Do not remember the same object twice; do not pass parameters that are already wrapped in `State<T>` to another `remember` call—this creates unnecessary nested observability.

## Common Anti-Patterns
- Storing mutable collections or mutable data classes directly as state; prefer immutable containers wrapped in `State` or use snapshot state collections (`mutableStateListOf`, `mutableStateMapOf`).
- Duplicating state in multiple owners instead of hoisting to a single source of truth.
- Mixing remember and retain for the same object; remembering/retaining objects with mismatched lifespans.
- Saving large or complex objects in `rememberSaveable`/`SavedStateHandle` (Android); save IDs and rehydrate instead.
- Computing derived values inside composables without `derivedStateOf`, causing unnecessary recompositions.

## Output Expectations
- Favor stateless composables with `value` + callbacks.
- Prefer lowest common ancestor hoisting.
- Choose lifecycle APIs intentionally; call out saving strategy explicitly.
- Keep state minimal, immutable, and observable.

## References
- Load `references/compose-state-guidance.md` for decision trees, tables, and code examples.
