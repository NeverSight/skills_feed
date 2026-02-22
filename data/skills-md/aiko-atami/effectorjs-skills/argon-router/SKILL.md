---
name: argon-router
description: Integrate and use argon-router in React web applications with Effector. Use when tasks involve creating routes and routers, wiring RouterControls/history adapters, composing routes with chainRoute/group/createVirtualRoute, rendering views with RouterProvider/createRoutesView/Outlet, building links with Link/useLink, and managing URL query state with trackQuery and @argon-router/paths.
---

# Argon Router

Use this skill to implement argon-router in React web apps with predictable Effector dataflow and typed paths.

## Workflow

1. Classify the task:
- `setup`: create route map, router, and controls.
- `ui`: connect router to React views, links, and outlet.
- `native`: integrate argon-router with React Navigation in React Native.
- `query`: track URL query state and sync enter/exit flows.
- `composition`: build derived/protected/virtual routes.
- `adapters`: pick and configure history/query/custom adapter.
- `ssr`: scope-safe initialization with memory history and `allSettled`.
- `hooks`: route activity and router access hooks in React.
- `debug`: validate path/router wiring and route lifecycle.

2. Load only required references:
- Always start with `references/core-routing.md`.
- Add `references/react-web.md` for any React integration task.
- Add `references/react-native.md` for React Native stack/tabs integration.
- Add `references/paths-dsl.md` when working with route path syntax or parsing/building URLs.
- Add `references/query-tracking.md` when query params or filters are involved.
- Add `references/route-composition.md` when using auth guards, grouped states, or virtual routes.
- Add `references/adapters-ssr.md` for `historyAdapter`/`queryAdapter`, adapter selection, SSR bootstrap.
- Add `references/react-navigation-apis.md` for `Link`, `useRouter`, `useRouterContext`, `useIsOpened`, `useOpenedViews`.
- Add `references/lazy-layout.md` for `createLazyRouteView` and `withLayout`.
- Add `references/examples.md` for copyable happy-path scaffolds.
- End with `references/checklist.md` before final output.

3. Resolve source of truth before implementation:
- Prefer `../argon-router/packages/*/lib/*.ts` and package `lib/index.ts` exports.
- Use docs as explanatory context and examples.
- If docs and code differ, follow code behavior and note mismatch briefly.

4. Build in this order:
- Define route units with explicit paths and params.
- Create router controls and initialize history adapter.
- Create router with known routes, optional base, and explicit pathless mapping (`{ path, route }`) when needed.
- Create React route views and wire `RouterProvider` + `createRoutesView` (add `otherwise` when fallback behavior is required).
- Add link/navigation actions via route `open` and `Link` first.
- Use `useLink` only for custom interaction surfaces.
- Add dynamic registration (`router.registerRoute(...)`) only if runtime extension is required.
- Add query trackers only when URL query behavior is required.
- Add route composition (`chainRoute`, `group`) after baseline routing works.
- Add lazy/layout organization (`createLazyRouteView`, `withLayout`) when route tree is stable.

5. Produce output contract:
- Router topology: routes, router, controls, view mapping.
- Wiring snippets for navigation and query flows.
- Notes for params/path DSL used by each route.
- Notes on adapter/SSR decisions when relevant.
- Validation checklist with expected lifecycle behavior.

## Defaults

- Target React web only (`@argon-router/react`).
- Switch to React Native patterns only when task explicitly targets mobile/native stack.
- Use happy-path integration patterns.
- Keep route graph explicit and small before adding composition.
- Prefer declarative Effector links (`sample`, `attach`) over imperative glue code.
- Prefer `Link` over `useLink` unless custom interaction requires manual handlers.

## Guardrails

- Initialize controls with `setHistory` before expecting route activation from URL changes.
- Pass router adapters to `setHistory` (`historyAdapter(...)` or `queryAdapter(...)`), not raw history objects.
- Ensure every route used by `useLink` is registered in `createRouter({ routes })`.
- Keep route paths deterministic; avoid ambiguous wildcard-heavy patterns unless required.
- Model query state through `trackQuery`, not ad-hoc parsing in components.
- Keep view rendering centralized in `createRoutesView` and `Outlet` composition.
- Add `createRoutesView({ otherwise })` when no-match fallback is part of requirements.
- Use `historyAdapter` for pathname routing and `queryAdapter` for secondary/modal/tab routing.
- For SSR/testing, initialize router in scope with `allSettled(router.setHistory, { params: historyAdapter(createMemoryHistory(...)) })`.
