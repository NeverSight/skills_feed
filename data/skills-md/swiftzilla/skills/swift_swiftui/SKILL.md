---
name: swift_swiftui
description: SwiftUI framework concepts including property wrappers, state management, and reactive UI patterns.
license: Proprietary
compatibility: SwiftUI 1.0+
metadata:
  version: "1.0"
  author: SwiftZilla
  website: https://swiftzilla.dev
---

# SwiftUI

This skill covers SwiftUI framework concepts for building declarative user interfaces.

## Overview

SwiftUI is Apple's modern declarative framework for building user interfaces across all Apple platforms using a reactive, state-driven approach.

## Available References

- [Property Wrappers](./references/property_wrappers.md) - @State, @Binding, @ObservedObject, @StateObject, @Environment

## Quick Reference

### State Management Decision Tree

```
Need local mutable state?
├── YES → Is it a value type?
│   ├── YES → Use @State
│   └── NO → Use @StateObject
└── NO → Shared from parent?
    ├── YES → Is it value type?
    │   ├── YES → Use @Binding
    │   └── NO → Use @ObservedObject
    └── NO → Use @Environment
```

### Property Wrappers

| Wrapper | Owns Data | Data Type | Use For |
|---------|-----------|-----------|---------|
| @State | Yes | Value type | Local UI state |
| @Binding | No | Value type | Shared state with parent |
| @ObservedObject | No | Reference type | Injected dependencies |
| @StateObject | Yes | Reference type | Owned view models |
| @Environment | No | Any | Shared resources |

### Common Usage Patterns

```swift
// Local state
struct CounterView: View {
    @State private var count = 0
    
    var body: some View {
        Button("Count: \(count)") { count += 1 }
    }
}

// Shared state (parent to child)
struct ParentView: View {
    @State private var isOn = false
    
    var body: some View {
        ChildView(isOn: $isOn)
    }
}

struct ChildView: View {
    @Binding var isOn: Bool
    
    var body: some View {
        Toggle("Enable", isOn: $isOn)
    }
}

// Observable object
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
}

struct ContentView: View {
    @StateObject private var viewModel = ViewModel()
    
    var body: some View {
        List(viewModel.items) { item in
            Text(item.name)
        }
    }
}

// Environment values
struct EnvironmentView: View {
    @Environment(\.colorScheme) var colorScheme
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        Text(colorScheme == .dark ? "Dark" : "Light")
    }
}
```

## Best Practices

1. **Use @State for local UI state** - Toggles, text fields, counters
2. **Lift state up when shared** - Single source of truth
3. **Use @StateObject for owned view models** - Survives view recreation
4. **Pass @Binding to child views** - Two-way data flow
5. **Keep @State minimal** - Only store what's needed for UI
6. **Use @Environment for system values** - Color scheme, locale, etc.
7. **Access on main thread** - All property wrappers require @MainActor
8. **Initialize with underscore** - `_count = State(initialValue:)`

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Initializing @State directly | Use `_property = State(initialValue:)` |
| Creating @ObservedObject in init | Use @StateObject instead |
| Mutating on background thread | Dispatch to main queue |
| Passing @State instead of Binding | Use `$property` for Binding |

## For More Information

Visit https://swiftzilla.dev for comprehensive SwiftUI documentation.
