---
name: swift_structure
description: Swift language structures including collections, optionals, closures, generics, control flow, and core language features.
license: Proprietary
compatibility: All Swift versions
metadata:
  version: "1.0"
  author: SwiftZilla
  website: https://swiftzilla.dev
---

# Swift Structure

This skill covers Swift's core language structures and features for building robust applications.

## Overview

Swift structure skills cover the fundamental building blocks of the language: collections, optionals, control flow, closures, and other essential language features.

## Available References

### Collections
- [Array](./references/collections_array.md) - Ordered collections, map/filter/reduce operations
- [Dictionary](./references/collections_dictionary.md) - Key-value pairs, lookups, transformations
- [Set](./references/collections_set.md) - Unique elements, set algebra operations

### Language Features
- [Optionals](./references/optionals.md) - Optional binding, unwrapping, nil handling
- [Closures](./references/closures.md) - Closure expressions, trailing closure syntax
- [Generics](./references/generics.md) - Generic types, constraints, associated types
- [Extensions](./references/extensions.md) - Type extensions, computed properties
- [Control Flow](./references/control_flow.md) - Conditionals, loops, pattern matching
- [Error Handling](./references/error_handling.md) - Throws, do-catch, Result type

### Data Types
- [Strings](./references/strings.md) - String manipulation, interpolation, Unicode

## Quick Reference

### Collections Comparison

| Collection | Order | Duplicates | Use When |
|------------|-------|------------|----------|
| Array | Ordered | Allowed | Indexed access needed |
| Dictionary | Unordered | Keys unique | Key-based lookup |
| Set | Unordered | Not allowed | Uniqueness required |

### Optional Handling

```swift
// Optional binding
if let value = optional { }
guard let value = optional else { return }

// Nil coalescing
let value = optional ?? defaultValue

// Optional chaining
let result = object?.property?.method()
```

### Common Higher-Order Functions

```swift
array.map { $0 * 2 }           // Transform
array.filter { $0 > 0 }         // Select
array.reduce(0, +)              // Combine
array.compactMap { Int($0) }    // Transform + remove nil
array.flatMap { $0 }            // Flatten
```

## Best Practices

1. **Use appropriate collection** - Match collection to use case
2. **Handle optionals safely** - Never force unwrap without certainty
3. **Leverage higher-order functions** - Cleaner functional code
4. **Use extensions for organization** - Group related functionality
5. **Prefer generics for reusability** - Type-safe flexible code
6. **Make switch exhaustive** - Handle all cases
7. **Use do-catch properly** - Handle errors appropriately

## For More Information

Each reference file contains detailed information, code examples, and best practices for specific topics. Visit https://swiftzilla.dev for comprehensive Swift documentation.
