---
name: typescript-interface-vs-type
description: Guides when to use interface vs type in TypeScript. Use this skill when defining object types, extending types, or choosing between interface and type aliases.
---

# TypeScript: Interface vs Type

## Core Principle

**Use `interface` until you need features from `type`.**

This is the official TypeScript recommendation from the [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html).

## When to Use Interface

Use `interface` for:
- Object type definitions
- Extending other object types
- Class implementations
- Declaration merging (augmenting existing types)

## When to Use Type

Use `type` only when you need:
- Union types: `type Status = 'pending' | 'approved' | 'rejected'`
- Mapped types: `type Readonly<T> = { readonly [K in keyof T]: T[K] }`
- Conditional types: `type NonNullable<T> = T extends null | undefined ? never : T`
- Tuple types: `type Point = [number, number]`
- Function types (though interface can also work): `type Handler = (event: Event) => void`

## Prefer `interface extends` Over Intersection (`&`)

When extending object types, always prefer `interface extends` over type intersections.

```typescript
// Preferred
interface User {
  name: string;
}

interface Admin extends User {
  permissions: string[];
}

// Avoid
type User = {
  name: string;
};

type Admin = User & {
  permissions: string[];
};
```

### Reason 1: Better Error Messages

With `interface extends`, TypeScript raises errors at the definition when extending with incompatible properties:

```typescript
interface Base {
  id: number;
}

// Error immediately at definition
interface Extended extends Base {
  id: string; // Error: Type 'string' is not assignable to type 'number'
}
```

With intersections, errors only appear when accessing the incompatible property, making bugs harder to catch:

```typescript
type Base = {
  id: number;
};

// No error at definition
type Extended = Base & {
  id: string;
};

// Error only when used
const item: Extended = { id: 'abc' }; // Error appears here, not at type definition
```

### Reason 2: Better TypeScript Performance

`interface extends` provides better TypeScript performance:
- Interfaces are cached by name - TypeScript computes the type once and reuses it
- Intersections are recomputed every time they're used, which slows down type checking with complex types

See [TypeScript Performance Wiki](https://github.com/microsoft/TypeScript/wiki/Performance#preferring-interfaces-over-intersections) for details.

## References

- [TypeScript Handbook - Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- [TypeScript Performance Wiki](https://github.com/microsoft/TypeScript/wiki/Performance#preferring-interfaces-over-intersections)
- [Total TypeScript - Intersections vs Interface Extends](https://www.totaltypescript.com/books/total-typescript-essentials/objects#intersections-vs-interface-extends)
