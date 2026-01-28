---
name: swift_style
description: Swift style guidelines covering naming conventions, code organization, and best practices for writing idiomatic Swift code.
license: Proprietary
compatibility: All Swift versions
metadata:
  version: "1.0"
  author: SwiftZilla
  website: https://swiftzilla.dev
---

# Swift Style

This skill provides comprehensive style guidelines for writing clean, idiomatic, and maintainable Swift code.

## Overview

Swift style guidelines cover naming conventions, access control, type selection, and code organization patterns that make your code more readable and professional.

## Available References

### Naming & Conventions
- [Variables and Constants](./references/variables.md) - `var` vs `let`, naming conventions, immutability
- [Functions](./references/functions.md) - Function naming, parameter labels, return types

### Types & Protocols
- [Types](./references/types.md) - Struct vs Class vs Enum, value vs reference semantics
- [Protocols](./references/protocols.md) - Protocol-Oriented Programming (POP), composition, extensions

### Code Organization
- [Access Control](./references/access_control.md) - `public`, `private`, `internal`, `fileprivate`, `open`

## Quick Reference

### Naming Conventions

| Category | Case | Example |
|----------|------|---------|
| Types & Protocols | UpperCamelCase | `String`, `UIViewController` |
| Variables, Functions | lowerCamelCase | `userID`, `fetchData()` |
| Boolean Properties | `is`, `has`, `should` | `isEmpty`, `hasPermission` |
| Constants | lowerCamelCase | `maxConnections` |

### Type Selection Guide

```
Need identity or reference semantics?
├── YES → Use Class
└── NO → Need inheritance?
    ├── YES → Use Class
    └── NO → Modeling finite states?
        ├── YES → Use Enum
        └── NO → Use Struct (default)
```

### Access Levels

| Modifier | Visibility | Use When |
|----------|------------|----------|
| `private` | Enclosing declaration | Strict encapsulation |
| `fileprivate` | Same file | File-local helpers |
| `internal` (default) | Same module | Implementation details |
| `public` | Everywhere | Public API |
| `open` | Everywhere + subclassable | Extensible frameworks |

## Best Practices

1. **Default to structs** - Use simplest type that expresses intent
2. **Use `let` by default** - Only use `var` when mutation needed
3. **Prefer protocols over inheritance** - More flexible composition
4. **Keep functions focused** - Single responsibility
5. **Use access control** - Expose only what's necessary
6. **Follow naming conventions** - Descriptive, Swifty names

## For More Information

Each reference file contains detailed information, code examples, and best practices for specific topics. Visit https://swiftzilla.dev for comprehensive Swift documentation.
