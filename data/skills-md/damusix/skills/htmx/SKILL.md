---
name: htmx
description: Complete reference for HTMX — the HTML-first library for modern browser features without JavaScript. Use when tasks involve hx-* attributes, HTMX AJAX requests, swap strategies, server-sent events, WebSockets, or hypermedia-driven UIs.
metadata:
  author: Danilo Alonso
  version: "2.0"
  references: attributes, requests, swapping, events-api, patterns, extensions
---

# HTMX Skill


Use this skill for HTMX implementation and integration. Read only the reference file(s) needed for the task.

## Quick Start

1. Identify the domain of the task (attributes, requests, swapping, events, patterns).
2. Open the matching file from `references/`.
3. Implement using HTML-first, hypermedia-driven patterns.
4. Validate that server responses return HTML fragments, not JSON.

## Critical Rules

- HTMX expects **HTML responses** from the server, not JSON.
- Most attributes **inherit** to child elements. **Not inherited:** `hx-trigger`, `hx-on*`, `hx-swap-oob`, `hx-preserve`, `hx-history-elt`, `hx-validate`. Use `hx-disinherit` or `unset` to stop inheritance of other attributes.
- Default swap strategy is `innerHTML`. Always confirm the intended swap method.
- Non-GET requests automatically include the closest enclosing form's values.
- Use `hx-boost="true"` for progressive enhancement — pages must work without JS.
- Escape all user-supplied content server-side to prevent XSS.
- HTMX adds/removes CSS classes during the request lifecycle — use these for transitions and indicators.
- All `hx-*` attributes can also be written as `data-hx-*` for HTML validation compliance.

## Reference Map

- All `hx-*` attributes, values, and modifiers: `references/attributes.md`
- Triggers, headers, parameters, CSRF, caching, CORS: `references/requests.md`
- Swap methods, targets, OOB swaps, morphing, view transitions: `references/swapping.md`
- Events, JS API, configuration, extensions, debugging: `references/events-api.md`
- Common UI patterns and examples: `references/patterns.md`
- Official extensions (WS, SSE, Idiomorph, response-targets, head-support, preload): `references/extensions.md`
- Cross-file index and routing: `references/REFERENCE.md`

## Task Routing

- Adding HTMX behavior to elements -> `references/attributes.md`
- Configuring how/when requests fire -> `references/requests.md`
- Controlling where/how responses render -> `references/swapping.md`
- Handling events, JS interop, or config -> `references/events-api.md`
- Building common UI patterns (search, infinite scroll, modals, etc.) -> `references/patterns.md`
- Using WebSockets, SSE, morphing, preloading, response targeting, or head merging -> `references/extensions.md`
- Cross-cutting concerns or architecture -> `references/REFERENCE.md` then domain-specific files
