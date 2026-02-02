---
name: react-router
description: React Router - multi-strategy router for React bridging React 18 to React 19. Use when building React applications with routing, data loading, SSR, or SPA architectures.
metadata:
  author: Hairyf
  version: "2026.1.31"
  source: Generated from https://github.com/remix-run/react-router, scripts located at https://github.com/hairyf/skills
---

# React Router

> The skill is based on React Router v7.13.0, generated at 2026-01-31.

React Router is a multi-strategy router for React bridging the gap from React 18 to React 19. You can use it maximally as a React framework or as minimally as you want. It supports three modes: Declarative (basic routing), Data (with loaders/actions), and Framework (full-featured with type safety and code splitting).

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Modes | Three usage modes: Framework, Data, and Declarative - choosing the right approach | [core-modes](references/core-modes.md) |
| Routing | Route configuration, path patterns, nested routes, layout routes, and route matching | [core-routing](references/core-routing.md) |
| Navigation | Navigation components and hooks: Link, NavLink, Form, useNavigate, redirect | [core-navigation](references/core-navigation.md) |
| Data Loading | Loading data with loaders and clientLoaders in route modules | [core-data-loading](references/core-data-loading.md) |
| Actions | Data mutations with actions and clientActions in route modules | [core-actions](references/core-actions.md) |
| Route Module | Route module API: component, loader, action, error boundary, headers, meta, and more | [core-route-module](references/core-route-module.md) |
| Hooks | Essential React Router hooks: useNavigation, useLocation, useParams, useMatches, and more | [core-hooks](references/core-hooks.md) |

## Features

### Data Management

| Topic | Description | Reference |
|-------|-------------|-----------|
| Fetchers | Using fetchers for concurrent data interactions without navigation | [features-fetchers](references/features-fetchers.md) |
| Error Handling | Error boundaries, error handling, and error responses | [features-error-handling](references/features-error-handling.md) |
| Middleware | Middleware for authentication, logging, and request processing | [features-middleware](references/features-middleware.md) |

### Forms and User Input

| Topic | Description | Reference |
|-------|-------------|-----------|
| Form Validation | Form validation patterns, error handling, and user feedback | [features-form-validation](references/features-form-validation.md) |
| File Uploads | Handling file uploads with multipart form data and file storage | [features-file-uploads](references/features-file-uploads.md) |
| Search Params | Working with URL search parameters using useSearchParams hook | [features-search-params](references/features-search-params.md) |

### Navigation and UX

| Topic | Description | Reference |
|-------|-------------|-----------|
| View Transitions | Smooth page transitions using View Transitions API | [features-view-transitions](references/features-view-transitions.md) |
| Navigation Blocking | Blocking navigation with useBlocker for unsaved form data | [features-navigation-blocking](references/features-navigation-blocking.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Type Safety | Type safety with Route types, automatic type inference, and type generation | [best-practices-type-safety](references/best-practices-type-safety.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Streaming | Streaming with Suspense, deferring non-critical data, and React Suspense integration | [advanced-streaming](references/advanced-streaming.md) |
| Pre-rendering | Pre-rendering static pages at build time for faster page loads | [advanced-pre-rendering](references/advanced-pre-rendering.md) |
| SPA Mode | Single Page App mode with SSR disabled and client-side routing | [advanced-spa-mode](references/advanced-spa-mode.md) |

## Key Recommendations

- **Choose the right mode**: Use Framework mode for new projects, Data mode if you need control over bundling, Declarative mode for simple routing
- **Use Route Module API** in Framework mode for automatic code splitting and type safety
- **Return promises from loaders** for streaming with Suspense
- **Use fetchers** for non-navigating form submissions and concurrent data loading
- **Export ErrorBoundary** in route modules to catch errors gracefully
- **Use middleware** for cross-cutting concerns like authentication and logging
- **Leverage type safety** in Framework mode with generated Route types
- **Prefer declarative navigation** (Link, NavLink, Form) over imperative (useNavigate)

<!--
Source references:
- https://reactrouter.com/
- https://github.com/remix-run/react-router
-->
