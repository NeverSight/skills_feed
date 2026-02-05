---
name: ecmascript-over-typescript-features
description: Use when choosing between TypeScript and ECMAScript features. Use when writing portable code. Use when considering enum or namespace. Use when targeting multiple JavaScript environments. Use when writing library code.
---

# Prefer ECMAScript Features to TypeScript Features

## Overview

TypeScript includes features like `enum` and `namespace` that are specific to TypeScript and don't exist in JavaScript. Prefer standard ECMAScript features when possible - they're more portable, better understood by the JavaScript ecosystem, and won't lock you into TypeScript-specific patterns.

This doesn't mean avoid TypeScript entirely - use its type system fully. But for runtime features, prefer standard JavaScript.

## When to Use This Skill

- Choosing between TypeScript and ECMAScript features
- Writing portable code that might be used without TypeScript
- Considering enum, namespace, or parameter properties
- Targeting multiple JavaScript environments
- Writing library code for broad consumption

## The Iron Rule

**Prefer standard ECMAScript features over TypeScript-specific runtime features. Use TypeScript for types, JavaScript for runtime behavior.**

## Detection

Watch for TypeScript-specific runtime features:

```typescript
// RED FLAGS - TypeScript-specific features
enum Status { Active, Inactive }  // TypeScript enum
namespace MyLib { }               // TypeScript namespace
class Foo { constructor(public x: number) {} }  // Parameter properties
```

## Enums: Use Const Objects Instead

```typescript
// TypeScript enum - generates runtime code
enum Status {
  Active = 'ACTIVE',
  Inactive = 'INACTIVE',
}
// Generates: var Status = { Active: 'ACTIVE', ... }

// BETTER: Const object with type
const Status = {
  Active: 'ACTIVE',
  Inactive: 'INACTIVE',
} as const;

type Status = typeof Status[keyof typeof Status];
// Status = 'ACTIVE' | 'INACTIVE'

// Usage
function setStatus(status: Status) { }
setStatus(Status.Active);  // OK
setStatus('ACTIVE');       // OK
setStatus('INVALID');      // Error!
```

## Namespaces: Use ES Modules Instead

```typescript
// TypeScript namespace
namespace Utils {
  export function formatDate(d: Date): string {
    return d.toISOString();
  }
  export const PI = 3.14159;
}

// BETTER: ES Module
// utils.ts
export function formatDate(d: Date): string {
  return d.toISOString();
}
export const PI = 3.14159;

// usage.ts
import { formatDate, PI } from './utils';
```

## Parameter Properties: Be Explicit

```typescript
// TypeScript parameter properties
class Person {
  constructor(
    public name: string,
    private age: number,
    protected id: string
  ) {}
}

// BETTER: Explicit declarations
class Person {
  name: string;
  private age: number;
  protected id: string;
  
  constructor(name: string, age: number, id: string) {
    this.name = name;
    this.age = age;
    this.id = id;
  }
}
```

## When TypeScript Features Are OK

```typescript
// Type-only features are fine - no runtime impact
type User = { name: string };  // TypeScript type
interface Config { }           // TypeScript interface
type ID = string;              // Type alias

// These compile away completely!
```

## Pressure Resistance Protocol

When choosing features:

1. **Ask: Is this type-only?** TypeScript types are great
2. **Check runtime impact**: Does this generate special code?
3. **Consider portability**: Will this work without TypeScript?
4. **Prefer standards**: ECMAScript features work everywhere
5. **Document exceptions**: If you must use TS features, explain why

## Red Flags

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `enum` for string unions | TS-specific, generates code | `as const` object |
| `namespace` | TS-specific module system | ES modules |
| Parameter properties | TS-specific syntax | Explicit properties |

## Common Rationalizations

### "Enums are more ergonomic"

**Reality**: Const objects with `as const` provide the same type safety with standard JavaScript.

### "Namespaces organize code"

**Reality**: ES modules are the standard. Use files and imports for organization.

### "Parameter properties save typing"

**Reality**: They're non-standard. Explicit properties are clearer and more portable.

## Quick Reference

| Instead Of | Use | Why |
|------------|-----|-----|
| `enum` | `as const` object | Standard JavaScript |
| `namespace` | ES modules | Standard, better tree-shaking |
| Parameter properties | Explicit properties | Clearer, standard |
| `import =` | ES imports | Standard module system |

## The Bottom Line

Use TypeScript for its type system, but prefer standard ECMAScript features for runtime code. This makes your code more portable, better understood, and future-proof.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 72: Prefer ECMAScript Features to TypeScript Features
