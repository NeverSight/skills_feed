---
name: react-state-driven-ui
description: Create React UI as a projection of explicit state transitions using reducer + events. Use when building multi-step forms, async operations, cross-component state, navigation integration, real-time updates, or complex validation. Eliminates timing-dependent bugs through explicit state transitions and isolated side effects.
---

# React State-Driven UI

Build predictable, testable React applications by treating UI as a pure projection of explicit state. This architectural pattern eliminates timing-dependent bugs, reduces cognitive overhead, and makes complex workflows manageable through clear state transitions and isolated side effects.

## What this solves
- **Race conditions**: Explicit state transitions prevent timing-dependent bugs
- **Complex workflows**: Multi-step forms, async operations, and navigation blocking become predictable
- **State synchronization**: Clear boundaries between server cache, client workflow, URL, and UI state
- **Testing**: Pure reducers and selectors make behavior deterministic and testable
- **Team collaboration**: Consistent patterns reduce onboarding time and prevent architectural drift

## When to apply
Use this skill when building features that require:

- **Multi-step workflows**: Forms with validation, saving, confirmation dialogs
- **Async operations**: API calls with loading/error states, retries, optimistic updates  
- **Cross-component state**: Shared data that affects multiple parts of the UI
- **Navigation integration**: Deep linking, browser back/forward, unsaved changes warnings
- **Real-time updates**: WebSocket connections, live data synchronization
- **Complex validation**: Field-level, form-level, and server-side validation coordination

## What you get
- **Predictable behavior**: UI always reflects current state, no surprises
- **Easy debugging**: Clear state history and transition paths
- **Better UX**: Optimistic updates, proper loading states, graceful error handling
- **Maintainable code**: Separation of concerns, testable business logic
- **Team consistency**: Shared vocabulary and patterns across features

## Technical approach
Use this skill to design and implement UI behavior as a pure projection of state.
Model behavior with reducer + events.
Isolate side effects in React Query mutation callbacks.
Keep components render-only and intent-only.

## Ideal use cases
- The feature has phases (idle, editing, saving, confirming, error).
- The feature has async behavior (save, validate, retry, generate).
- The feature has cross-component or cross-route behavior.
- The current design relies on boolean soup or lifecycle timing.
- Correctness must survive re-rendering and concurrency.

## Do not use this skill when
- The change is purely presentational.
- The behavior is trivial and isolated to local UI state.
- There is no workflow and no side effects.

## Required approach
Follow this order. Do not skip steps.
Do not write component code before steps 1 to 4 are complete.

1. Define the state model and ownership boundaries.
2. Define events (user intent and system outcomes).
3. Define transitions as a pure reducer (event -> next state).
4. Define side effects and bind them to events.
   - Use React Query mutation callbacks to emit outcome events.
5. Define selectors (derived values).
6. Implement components as projection + intent emission only.

## Output expectations
When using this skill, output in this structure:

1. State model
2. Events
3. Transition map (reducer rules)
4. Side effects plan (React Query mutations and callbacks)
5. Selectors
6. Component boundaries
7. Implementation steps
8. Design rationale (why, what, why not, skipped, trade-offs)

## Canonical documents
- Full compiled guidance for agents: AGENTS.md
- Source rules (modular): rules/
- Patterns and examples: references/

## Rule catalog
Read the relevant rule files from rules/ as needed.
Treat AGENTS.md as canonical when uncertain.

### Construction and modeling
- rules/flow-ui-projection.md
- rules/flow-intents-only.md
- rules/reducer-events-drive-state.md
- rules/reducer-single-phase.md
- rules/fsm-no-boolean-soup.md

### Effects and async (React Query)
- rules/effects-no-effects-in-components.md
- rules/query-mutation-callbacks.md
- rules/query-stale-response-guard.md

### Cross-cutting behavior
- rules/routing-explicit-decision-state.md
- rules/url-validated-boundary.md

### Correctness and maintainability
- rules/derive-derived-state-as-selectors.md
- rules/identity-stable-ids-and-keys.md
- rules/determinism-no-lifecycle-dependence.md

### Documentation and reasoning
- rules/docs-rationale-at-boundaries.md
