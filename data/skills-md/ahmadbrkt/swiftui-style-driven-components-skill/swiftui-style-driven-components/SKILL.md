---
name: swiftui-style-driven-components
description: 'Expert guidance on SwiftUI style-driven components following Apple patterns (ButtonStyle, LabelStyle). Use when: building components with style protocols, implementing configuration patterns, adding environment-based styling, creating extensible component libraries, or reviewing component architecture.'
---

# SwiftUI Style-Driven Components

## Overview

This skill provides expert guidance on building, reviewing, and extending SwiftUI components following the style-driven architecture pattern. This pattern emphasizes extensibility, maintainability, and Apple-style API design, making it ideal for building reusable component libraries.

## Agent Behavior Contract

1. Before creating a new component, verify it needs 2+ meaningfully different styles. If not, skip the style protocol.
2. Follow Apple's patterns (`ButtonStyle`, `LabelStyle`) as the gold standard.
3. Use nested type-erased views in configuration (like `LabelStyleConfiguration.Title`).
4. Never expose configuration initializers as `public`.
5. Wrap `style.makeBody` in `AnyView` for type erasure.
6. Use `DynamicProperty` for style protocols, not `Sendable`.
7. Read styles from environment using existential type (`any [Component]Style`).

## Core Architecture Principles

- **Protocol**: `[Component]Style` — defines HOW to render
- **Configuration**: `[Component]StyleConfiguration` — contains WHAT to render
- **Component**: Creates configuration internally, delegates rendering to style
- **Environment**: Enables subtree styling without modifying components

## When to Use Style Protocol

**Use style protocol when:**
- 2+ meaningfully different visual styles needed
- Environment-based style cascading desired
- Building reusable component library
- Styles need environment access (`@Environment`)

**Skip style protocol when:**
- Single visual representation
- Simple, static appearance
- One-off internal component
- No style customization needed

## Quick Decision Tree

### Building a new component?
1. **Needs multiple styles?** → If no, skip style protocol
2. **Create structure** → See `references/component-structure.md`
3. **Define protocol** → See `references/style-protocol.md`
4. **Create configuration** → Nested type-erased views pattern
5. **Implement default style** → Basic rendering
6. **Add environment key** → See `references/environment-keys.md`
7. **Add convenience accessors** → See `references/common-patterns.md`

### Adding a new style?
1. Create struct conforming to `[Component]Style`
2. Implement `makeBody(configuration:)`
3. Add convenience accessor (`.myStyle`)
4. **No component changes needed!**

### Reviewing component architecture?
1. Check protocol uses `DynamicProperty`, `@ViewBuilder @MainActor`
2. Verify configuration uses nested type-erased views
3. Confirm configuration init is `internal`
4. Check component wraps `style.makeBody` in `AnyView`
5. Validate environment key uses existential (`any [Component]Style`)
6. Ensure new styles don't require component changes

## Triage Playbook

- **Creating component file structure** → `references/component-structure.md`
- **Defining style protocol** → `references/style-protocol.md`
- **Creating configuration with content** → `references/style-protocol.md`
- **Setting up environment keys** → `references/environment-keys.md`
- **Adding convenience initializers** → `references/common-patterns.md`
- **Parameterized or adaptive styles** → `references/common-patterns.md`
- **Using design tokens** → `references/design-system.md`
- **Writing snapshot tests** → `references/testing.md`
- **Organizing previews** → `references/previews.md`
- **Accessibility requirements** → `references/accessibility.md`

## Quick Reference

### Component Structure
```
[Component]/
├── EnvironmentKeys/[Component]StyleKey.swift
├── Styles/
│   ├── [Component]Style.swift
│   ├── [Component]StyleConfiguration.swift
│   └── Default[Component]Style.swift
└── [Component].swift
```

### Pattern Summary

- **Style Protocol**: `DynamicProperty`, `@ViewBuilder @MainActor func makeBody`
- **Configuration**: Nested `struct Content: View` with `private let _body: () -> AnyView`
- **Configuration Init**: `internal` (not `public`)
- **Component Body**: `AnyView(style.makeBody(configuration: .init(...)))`
- **Environment Key**: `@Entry public var style: any [Component]Style = .automatic`
- **View Modifier**: `func style(_ style: some [Component]Style) -> some View`

## Best Practices

### DO
- Use `DynamicProperty` for style protocols
- Use nested type-erased views in configuration
- Make configuration initializers `internal`
- Wrap `style.makeBody` in `AnyView`
- Use design tokens, not magic numbers
- Provide convenience accessors (`.compact`, `.outlined`)

### DON'T
- Add explicit `Sendable` to protocols
- Make configuration initializers `public`
- Pass configuration to component initializer
- Put content properties in style protocol
- Use style protocol for single-variant components
- Use `AnyView` directly as configuration property type

## Review Checklist

### Architecture
- [ ] Style protocol uses `DynamicProperty`
- [ ] `makeBody` has `@ViewBuilder @MainActor`
- [ ] Configuration uses nested type-erased views
- [ ] Configuration init is `internal`
- [ ] Component wraps `style.makeBody` in `AnyView`
- [ ] New styles don't require component changes

### Environment
- [ ] Uses `@Entry` macro
- [ ] Stores as existential (`any [Component]Style`)
- [ ] Modifier uses opaque parameter (`some [Component]Style`)
- [ ] Default value provided (`.automatic`)

### Quality
- [ ] Previews cover all styles (see `references/previews.md`)
- [ ] Snapshot tests exist (see `references/testing.md`)
- [ ] Accessibility supported (see `references/accessibility.md`)
- [ ] Design tokens used (see `references/design-system.md`)

## Reference Files

- **`references/component-structure.md`** — Creating new component, file organization
- **`references/style-protocol.md`** — Protocol definition, configuration pattern, adding styles
- **`references/environment-keys.md`** — Environment injection, usage patterns
- **`references/common-patterns.md`** — Convenience initializers/accessors, parameterized styles
- **`references/testing.md`** — Snapshot tests, test organization
- **`references/previews.md`** — Preview structure, checklist
- **`references/design-system.md`** — Design tokens, typography, colors
- **`references/accessibility.md`** — Labels, identifiers, Dynamic Type

## Philosophy

Style-driven components prioritize:
1. **Extensibility** — Add styles without modifying components
2. **Apple Patterns** — Follow `ButtonStyle`, `LabelStyle` conventions
3. **Simplicity** — Skip style protocol for single-variant components
4. **Type Safety** — Generic APIs with internal type erasure
5. **Consistency** — All components follow same patterns
