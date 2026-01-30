---
name: overlastic
description: Comprehensive skills for working with Overlastic
metadata:
  author: Hairyf
  version: "2026.01.29"
  source: Internal Documentation
---

> Based on Overlastic v0.8.7. A promise-based modal/dialog/popup library supporting React, Vue, and Svelte.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Constructor | Core method for creating overlay constructors | [core-constructor](references/core-constructor.md) |
| Deferred | Promise variation with external control methods | [core-deferred](references/core-deferred.md) |
| Global Functions | Utilities for mounting elements and name management | [core-defines](references/core-defines.md) |
| useDisclosure | Hook for managing overlay lifecycle and state | [core-disclosure](references/core-disclosure.md) |

## Framework References

| Topic | Description | Reference |
|-------|-------------|-----------|
| React Integration | Using Overlastic with React components | [framework-react](references/framework-react.md) |
| Vue Integration | Using Overlastic with Vue 3 components | [framework-vue](references/framework-vue.md) |
| Svelte Integration | Using Overlastic with Svelte components | [framework-svelte](references/framework-svelte.md) |

## Advanced References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Provider Pattern | Using OverlaysProvider for context inheritance | [advanced-provider](references/advanced-provider.md) |
| Custom Components | Integrating existing component libraries | [advanced-customization](references/advanced-customization.md) |
| External Control | Controlling overlay lifecycle from outside | [advanced-external-control](references/advanced-external-control.md) |
| Declarative Usage | Using overlays in templates/JSX | [advanced-declarative](references/advanced-declarative.md) |

## Key Concepts

- **Constructor**: Receives component, props, and options to mount overlays
- **Deferred**: Promise-like object with `confirm` and `cancel` methods for external control
- **Mount Options**: Configuration for container, ID, index, and deferred instance
- **Lifecycle**: Components are destroyed after `duration` ends when deferred resolves/rejects
- **Imperative Usage**: `defineOverlay` and `renderOverlay` for callback-based invocation
- **Declarative Usage**: Components can be used in templates/JSX with props
- **Provider Pattern**: `OverlaysProvider` for context inheritance
- **Dual Mode Support**: Components work in both imperative and declarative modes
