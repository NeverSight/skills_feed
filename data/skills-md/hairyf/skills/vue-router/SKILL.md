---
name: vue-router
description: Vue Router - official router for Vue.js. Use when building single-page applications with routing, navigation guards, nested routes, or programmatic navigation.
metadata:
  author: Anthony Fu
  version: "2026.1.31"
  source: Generated from https://github.com/vuejs/router, scripts located at https://github.com/antfu/skills
---

# Vue Router

> The skill is based on Vue Router v5.0.1, generated at 2026-01-31.

Vue Router is the official router for Vue.js. It deeply integrates with Vue.js core to make building Single Page Applications with Vue.js a breeze. Features include nested routes mapping, dynamic routing, modular component-based router configuration, route params, query, wildcards, view transition effects, fine-grained navigation control, links with automatic active CSS classes, HTML5 history mode or hash mode, customizable scroll behavior, and proper encoding for URLs.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Router Setup | Create router instance, register plugin, access router/route | [core-router-setup](references/core-router-setup.md) |
| Navigation | Programmatic navigation with push, replace, go methods | [core-navigation](references/core-navigation.md) |
| RouterView & RouterLink | Components for rendering routes and creating navigation links | [core-router-view-link](references/core-router-view-link.md) |

## Essentials

### Route Configuration

| Topic | Description | Reference |
|-------|-------------|-----------|
| Dynamic Matching | Dynamic route segments with params, accessing route.params | [essentials-dynamic-matching](references/essentials-dynamic-matching.md) |
| Nested Routes | Nested route configuration with children option | [essentials-nested-routes](references/essentials-nested-routes.md) |
| Named Routes | Named routes for navigation without hardcoded URLs | [essentials-named-routes](references/essentials-named-routes.md) |
| Named Views | Multiple RouterView components for complex layouts | [essentials-named-views](references/essentials-named-views.md) |
| History Mode | HTML5 history, hash mode, memory mode, server configuration | [essentials-history-mode](references/essentials-history-mode.md) |
| Route Matching Syntax | Custom regex, repeatable params, optional params | [essentials-route-matching-syntax](references/essentials-route-matching-syntax.md) |
| Active Links | Active link CSS classes, router-link-active vs exact-active | [essentials-active-links](references/essentials-active-links.md) |
| Passing Props | Pass route params as component props | [essentials-passing-props](references/essentials-passing-props.md) |
| Redirect & Alias | Route redirects and aliases for URL mapping | [essentials-redirect-alias](references/essentials-redirect-alias.md) |

## Advanced

### Navigation & Guards

| Topic | Description | Reference |
|-------|-------------|-----------|
| Navigation Guards | Global guards, per-route guards, in-component guards | [advanced-navigation-guards](references/advanced-navigation-guards.md) |
| Navigation Failures | Detecting aborted/cancelled/duplicated navigations | [advanced-navigation-failures](references/advanced-navigation-failures.md) |

### Composition & TypeScript

| Topic | Description | Reference |
|-------|-------------|-----------|
| Composition API | useRouter, useRoute, navigation guards, useLink | [advanced-composition-api](references/advanced-composition-api.md) |
| Typed Routes | TypeScript typed routes for autocomplete and type safety | [advanced-typed-routes](references/advanced-typed-routes.md) |

### Advanced Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Transitions | Route transitions using RouterView slot | [advanced-transitions](references/advanced-transitions.md) |
| Scroll Behavior | Custom scroll behavior on navigation | [advanced-scroll-behavior](references/advanced-scroll-behavior.md) |
| Meta Fields | Route meta fields for custom data | [advanced-meta](references/advanced-meta.md) |
| Lazy Loading | Lazy loading route components with dynamic imports | [advanced-lazy-loading](references/advanced-lazy-loading.md) |
| Dynamic Routing | Adding and removing routes at runtime | [advanced-dynamic-routing](references/advanced-dynamic-routing.md) |
| RouterView Slot | Advanced RouterView slot API for custom rendering | [advanced-router-view-slot](references/advanced-router-view-slot.md) |
