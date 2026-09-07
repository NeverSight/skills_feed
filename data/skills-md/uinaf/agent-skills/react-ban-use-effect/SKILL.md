---
name: react-ban-use-effect
description: "Detect, replace, and mechanically restrict direct React `useEffect` calls. Use when writing, refactoring, reviewing, or migrating React code that fetches, derives state, relays events, resets state, or synchronizes through effects. Do not use for unrelated React work or non-React effect systems."
---

# React Ban useEffect

Treat direct effects as an external-synchronization escape hatch, not a default
state-management tool.

## Workflow

1. Search the touched React surface for direct imports, namespace calls, and
   wrappers around `useEffect`.
2. Classify each effect before editing:
   - render-time derivation
   - server data or client-owned server state
   - user-caused work
   - identity-driven reset
   - external store or system synchronization
   - async UI or performance staging
3. Apply the matching pattern in
   [replacements](references/replacements.md). Read
   [alternatives](references/alternatives.md) only when the effect exposes a
   broader data, form, store, or performance ownership problem.
4. Preserve the repository's framework, data layer, lint shape, and dependency
   policy. Do not introduce a new library without approval.
5. Run lint, type, and test gates plus the smallest real UI or hook check for
   the changed behavior.

## Decision Order

Prefer, in order:

1. render-time calculation
2. server, loader, or framework data API
3. repository-owned server-state layer
4. event handler, action, or mutation
5. keyed component boundary
6. `useSyncExternalStore`
7. reviewed domain-specific hook for a real external system

If none fits, explain the external synchronization contract before keeping an
effect.

## Legitimate Effects

A reviewed integration hook should name the external system, own setup and
cleanup, expose its reactive inputs, and list every value used by setup or
cleanup. Prefer an existing repository hook. Do not accept a callback and
dependency array from callers or suppress exhaustive-dependency checks.

Never use an exception hook to fetch server state, copy props into state, relay
user actions, or hide a reset that belongs at a keyed boundary.

## Enforcement

Extend the repository's existing linter to reject both named `useEffect`
imports and `React.useEffect(...)`. Allow only narrow reviewed integration-hook
files. Keep the canonical local gate and CI on that same lint surface; optional
agent guidance or scanners do not replace mechanical enforcement.

In review, treat new direct effects as findings unless the change documents and
proves a legitimate external-system boundary. Ask for a replacement plan, not
dependency-array tuning.

## Boundaries

- Scope migrations to the touched or requested surface.
- Leave `useLayoutEffect`, framework lifecycle APIs, and non-React effect
  systems alone unless requested.
- Apply performance primitives only for measured behavior or an established
  repository pattern.
- Keep upstream attribution in [upstream](references/upstream.md).
