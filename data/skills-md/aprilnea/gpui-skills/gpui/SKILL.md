---
name: gpui
description: GPUI UI framework best practices for building desktop applications. Use when writing GPUI code, creating UI components, handling state/events, async tasks, animations, lists, forms, testing, or working with Zed-style Rust GUI code.
license: MIT
metadata:
  author: AprilNEA
  version: "1.0.0"
---

# GPUI Best Practices

Comprehensive guide for building desktop applications with GPUI, the UI framework powering Zed editor. Contains 40+ rules across 8 categories, prioritized by impact.

## When to Apply

Reference these guidelines when:
- Writing new GPUI views or components
- Implementing state management with Entity
- Handling events and keyboard shortcuts
- Working with async tasks and background work
- Building forms, lists, or dialogs
- Styling components with Tailwind-like API
- Testing GPUI applications

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Core Concepts | CRITICAL | `core-` |
| 2 | Rendering | CRITICAL | `render-` |
| 3 | State Management | HIGH | `state-` |
| 4 | Event Handling | HIGH | `event-` |
| 5 | Async & Concurrency | MEDIUM-HIGH | `async-` |
| 6 | Styling | MEDIUM | `style-` |
| 7 | Components | MEDIUM | `comp-` |
| 8 | Anti-patterns | CRITICAL | `anti-` |

## Quick Reference

### 1. Core Concepts (CRITICAL)

- `core-ownership-model` - Understand GPUI's single ownership model
- `core-entity-operations` - Use read/update/observe/subscribe correctly
- `core-weak-entity` - Use WeakEntity to break circular references
- `core-context-types` - Know when to use App, Context<T>, AsyncApp

### 2. Rendering (CRITICAL)

- `render-render-vs-renderonce` - Choose Render for stateful, RenderOnce for components
- `render-element-composition` - Build element trees with div() and method chaining
- `render-conditional` - Use .when() and .when_some() for conditional styling
- `render-shared-string` - Use SharedString to avoid string copying
- `render-builder-pattern` - Design components with builder pattern

### 3. State Management (HIGH)

- `state-notify` - Always call cx.notify() after state changes
- `state-observe` - Use cx.observe() to react to Entity changes
- `state-subscribe` - Use cx.subscribe() for typed events
- `state-global` - Use Global trait for app-wide state
- `state-keyed-state` - Use window.use_keyed_state() for persistent state

### 4. Event Handling (HIGH)

- `event-actions` - Define and register actions for keyboard shortcuts
- `event-listener` - Use cx.listener() for view-bound event handlers
- `event-focus` - Manage focus with FocusHandle and key_context
- `event-propagation` - Understand event bubbling and stop_propagation

### 5. Async & Concurrency (MEDIUM-HIGH)

- `async-task-lifecycle` - Store or detach tasks to prevent cancellation
- `async-debounce` - Implement debounce with timer + task replacement
- `async-background-spawn` - Use background_spawn for CPU-intensive work
- `async-weak-entity` - Use WeakEntity for safe cross-await access
- `async-error-handling` - Use .log_err() and .detach_and_log_err()

### 6. Styling (MEDIUM)

- `style-flexbox` - Use h_flex() and v_flex() for layouts
- `style-theme-colors` - Always use cx.theme() for colors
- `style-spacing` - Use DynamicSpacing for responsive spacing
- `style-elevation` - Use elevation system for layered surfaces

### 7. Components (MEDIUM)

- `comp-stateless` - Prefer RenderOnce with #[derive(IntoElement)]
- `comp-traits` - Implement Disableable, Selectable, Sizable traits
- `comp-focus-ring` - Add focus ring for accessibility
- `comp-dialog` - Use WindowExt for dialog management
- `comp-variant` - Use variant enums for component styles

### 8. Anti-patterns (CRITICAL)

- `anti-silent-error` - Never silently discard errors with let _ =
- `anti-drop-task` - Never drop Task without storing or detaching
- `anti-drop-subscription` - Always detach or store subscriptions
- `anti-circular-reference` - Avoid Entity cycles, use WeakEntity
- `anti-missing-notify` - Never forget cx.notify() after state changes
- `anti-unwrap` - Avoid unwrap(), use ? or explicit handling

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Application (App)                     │
│              (Single owner of all Entities)              │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───────────┐       ┌───────────┐       ┌──────────┐
    │ Entity<A> │       │ Entity<B> │       │ Global<C>│
    └───────────┘       └───────────┘       └──────────┘
        │                   │                   │
        │ read/update       │ read/update       │ via App
        │ via Context<A>    │ via Context<B>    │
        │
    ┌─────────────────────────────────────────────────┐
    │           UI Rendering (Render trait)           │
    │      Each frame: fn render(&mut self, ...)      │
    │      Returns: impl IntoElement (Element tree)   │
    └─────────────────────────────────────────────────┘
        │
        ├─ observe() → changes trigger render
        ├─ subscribe() → events trigger reactions
        ├─ notify() → signal changes
        └─ emit() → send typed events
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/core-ownership-model.md
rules/render-render-vs-renderonce.md
rules/anti-silent-error.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references
