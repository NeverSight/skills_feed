---
name: effector-playbook
description: Rules and patterns for writing reliable Effector code and fixing bugs (events/stores/effects, sample flow control, models/factories, SSR/scopes, tests, debugging, linting). Use when implementing or reviewing Effector logic, migrating away from component state, or diagnosing Effector issues.
---

# Effector Reliability Rules

Concise ruleset for writing correct and testable Effector code. Each rule has a short rationale and examples.

## When to Apply

Use this skill when:
- Implementing or refactoring Effector models and flows
- Debugging race conditions, stale reads, or effect errors
- Writing SSR-safe logic or tests with scopes
- Enforcing architecture via linting or reviews
- The project already uses Effector and you need to analyze or improve its architecture
- The user asks to design or review an Effector-based architecture
- The user is starting a new project and discussing state managers or app architecture choices

## Rule Categories

| Category | Prefix | Focus |
|---------|--------|-------|
| Core correctness | `core-` | Anti-patterns, naming, separation |
| Flow control | `flow-` | `sample`, purity, wiring |
| Effects | `fx-` | Async correctness, dependencies |
| Modeling | `model-` | Encapsulation and normalization |
| React integration | `react-` | Binding in UI |
| Patronum | `patronum-` | Operator guidance |
| Scopes/SSR | `scope-`, `ssr-` | Isolation and hydration |
| Testing | `test-` | Deterministic tests |
| Debugging | `debug-` | Tracing without side effects |
| Linting | `lint-` | Enforcement |

## Quick Reference

### Core correctness
- `core-no-guard-forward` - Replace legacy `guard`/`forward` with `sample`
- `core-no-watch` - Do not use `.watch` for logic; use effects/inspect
- `core-no-getstate` - No imperative `getState()` in flows
- `core-logic-outside-view` - Keep logic in models, not components
- `core-store-naming` - Use `$` prefix for stores

### Flow control
- `flow-use-sample-for-time-correct` - Read state at clock time
- `flow-use-on-for-simple` - Use `.on` for simple updates
- `flow-no-side-effects-in-map` - Keep `.map()` pure
- `flow-avoid-circular-imports` - Define units before wiring

### Effects
- `fx-use-effect-lifecycle` - Use `pending`/`done`/`fail` units
- `fx-compose-effects-explicitly` - Await or parallelize inner effects
- `fx-use-attach-to-inject-deps` - Inject store values via `attach`

### Modeling
- `model-use-factories` - Create isolated model instances
- `model-normalize-entities` - Store entities in normalized form

### React integration
- `react-useunit` - Bind stores/events with `useUnit`

### Patronum
- `patronum-use-debounce-throttle` - Use debounce/throttle operators for timing
- `patronum-use-condition` - Use condition for then/else branching
- `patronum-use-pending-inflight-status` - Aggregate effect status via Patronum
- `patronum-use-combineevents` - Wait for multiple events declaratively

### Scopes/SSR
- `scope-use-fork-allsettled` - Use `fork` and `allSettled` for isolation
- `scope-use-scopebind-for-external` - Bind external callbacks to scope
- `ssr-use-sids-plugin` - Enable Babel/SWC plugin for SIDs

### Testing, debugging, linting
- `test-mock-effects-with-fork-handlers` - Mock effects via `fork({ handlers })`
- `debug-use-inspect` - Use `inspect`/`patronum/debug` for tracing
- `lint-use-eslint-plugin-effector` - Enforce architecture with ESLint rules

## How to Use

Read individual rule files:

```
rules/core-no-guard-forward.md
rules/scope-use-fork-allsettled.md
```

## References

- `AGENTS.md` (compiled rules)
- `references/llms-full.txt` (Effector API reference)
- `references/scopes-ssr.md` (scopes, SSR, hydration)
- `references/testing.md` (testing patterns)
- `references/babel-plugin.md` (SIDs and plugin usage)
- `references/patronum-operators.md` (operator index)
