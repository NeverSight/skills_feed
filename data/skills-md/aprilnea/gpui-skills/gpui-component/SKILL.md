---
name: gpui-component
description: gpui-component library patterns for building reusable UI components. Use when creating buttons, inputs, dialogs, forms, or following Longbridge component library conventions in GPUI applications.
license: MIT
metadata:
  author: AprilNEA
  version: "1.0.0"
---

# gpui-component Best Practices

Comprehensive guide for building UI components with [gpui-component](https://github.com/longbridge/gpui-component), a component library for GPUI applications.

## When to Apply

Reference these guidelines when:
- Creating reusable UI components
- Implementing theme-aware styling
- Building dialogs, popovers, or sheets
- Creating form components (Input, Checkbox, etc.)
- Implementing component animations
- Following Longbridge component patterns

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Component Architecture | CRITICAL | `comp-` |
| 2 | Trait System | CRITICAL | `trait-` |
| 3 | Theme System | HIGH | `theme-` |
| 4 | Dialog & Popover | HIGH | `dialog-` |
| 5 | Form Components | MEDIUM | `form-` |
| 6 | Animation | MEDIUM | `anim-` |

## Quick Reference

### 1. Component Architecture (CRITICAL)

- `comp-renderonce` - Use RenderOnce with #[derive(IntoElement)]
- `comp-structure` - Standard component structure template
- `comp-builder` - Fluent builder pattern for components
- `comp-stateful` - Entity + RenderOnce for stateful components
- `comp-callbacks` - Use Rc<dyn Fn> for event callbacks

### 2. Trait System (CRITICAL)

- `trait-styled` - Implement Styled for style customization
- `trait-disableable` - Implement Disableable for disabled state
- `trait-selectable` - Implement Selectable for selection state
- `trait-sizable` - Implement Sizable with Size enum
- `trait-parent-element` - Implement ParentElement for children
- `trait-interactive` - Implement InteractiveElement for events

### 3. Theme System (HIGH)

- `theme-colors` - Use ThemeColor for consistent colors
- `theme-active` - Use ActiveTheme trait for theme access
- `theme-variants` - Implement variant enums (ButtonVariant, etc.)
- `theme-size-system` - Use StyleSized for size-based styling

### 4. Dialog & Popover (HIGH)

- `dialog-root` - Use Root component as window root
- `dialog-window-ext` - Use WindowExt for dialog management
- `dialog-confirm` - Implement confirm/alert dialogs
- `dialog-form` - Build form dialogs with input state
- `popover-pattern` - Popover vs PopupMenu vs Sheet selection

### 5. Form Components (MEDIUM)

- `form-input-state` - Entity-based input state management
- `form-focus` - Focus management with keyed state
- `form-validation` - Input validation patterns

### 6. Animation (MEDIUM)

- `anim-with-animation` - Use with_animation for transitions
- `anim-keyed-state` - Persist animation state with use_keyed_state
- `anim-easing` - Use cubic_bezier for smooth animations

## Component Structure Template

```rust
#[derive(IntoElement)]
pub struct MyComponent {
    // 1. Identifier
    id: ElementId,

    // 2. Base element (for event delegation)
    base: Div,

    // 3. Style override
    style: StyleRefinement,

    // 4. Content
    label: Option<SharedString>,
    children: Vec<AnyElement>,

    // 5. State configuration
    disabled: bool,
    selected: bool,
    size: Size,

    // 6. Callbacks
    on_click: Option<Rc<dyn Fn(&ClickEvent, &mut Window, &mut App)>>,
}
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Window                                                      │
│  ├── Root (Entity, manages overlay state)                   │
│  │   ├── view: AnyView (user's main view)                   │
│  │   ├── active_dialogs: Vec<ActiveDialog>                  │
│  │   ├── active_sheet: Option<ActiveSheet>                  │
│  │   └── notification: Entity<NotificationList>             │
│  │                                                          │
│  └── Render Layers                                          │
│      ├── Layer 0: Root.view (main content)                  │
│      ├── Layer 1: Sheet (side drawer)                       │
│      ├── Layer 2: Dialogs (stackable)                       │
│      └── Layer 3: Notifications                             │
└─────────────────────────────────────────────────────────────┘
```

## Popup Component Comparison

| Feature | Dialog | Popover | PopupMenu | Sheet |
|---------|--------|---------|-----------|-------|
| Position | Centered | Anchored | Anchored | Side |
| Overlay | Yes | No | No | Yes |
| State | Root | keyed_state | Entity | Root |
| Stacking | Multiple | Single | Submenus | Single |
| Close | ESC/Click/Button | ESC/Outside | ESC/Select | ESC/Overlay |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/comp-renderonce.md
rules/trait-styled.md
rules/dialog-root.md
```

Each rule file contains:
- Brief explanation of why it matters
- Code examples with correct patterns
- Common mistakes to avoid
