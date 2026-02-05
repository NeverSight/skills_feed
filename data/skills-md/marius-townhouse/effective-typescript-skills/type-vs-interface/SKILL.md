---
name: type-vs-interface
description: Use when defining object types. Use when choosing between type and interface. Use when extending types.
---

# Know the Differences Between type and interface

## Overview

**Use interface for object types, type for everything else.**

Both `type` and `interface` can define object types, but they have different capabilities. Understanding these differences helps you choose the right tool and write consistent code.

## When to Use This Skill

- Defining any named type
- Choosing between type alias and interface
- Extending or composing types
- Working with declaration files
- Understanding library type definitions

## The Iron Rule

```
Use INTERFACE for object types that could be extended.
Use TYPE for unions, tuples, mapped types, and complex compositions.
```

**Remember:**
- Interfaces support declaration merging
- Type aliases can express more complex types
- Both can be extended and implemented
- Consistency within a codebase matters most

## Quick Decision Guide

| Scenario | Use |
|----------|-----|
| Object type (API response, props) | `interface` |
| Union type | `type` |
| Tuple type | `type` |
| Function type | `type` |
| Mapped type | `type` |
| Primitive alias | `type` |
| Library types meant to be extended | `interface` |

## The Similarities

### Both Define Object Shapes

```typescript
type TState = {
  name: string;
  capital: string;
};

interface IState {
  name: string;
  capital: string;
}
// These are interchangeable for most purposes
```

### Both Support Generics

```typescript
type TBox<T> = { value: T };
interface IBox<T> { value: T }
```

### Both Can Be Extended

```typescript
// Interface extending type
interface IStateWithPop extends TState {
  population: number;
}

// Type extending interface
type TStateWithPop = IState & { population: number };
```

### Both Can Be Implemented

```typescript
class StateImpl implements IState {
  name = '';
  capital = '';
}
```

## The Differences

### 1. Union Types (type only)

```typescript
type StringOrNumber = string | number;  // Only with type
type Status = 'pending' | 'fulfilled' | 'rejected';

// Can't do this with interface
```

### 2. Tuple Types (type only)

```typescript
type Pair = [number, number];
type NamedNums = [string, ...number[]];

// Interface syntax is awkward
interface IPair {
  0: number;
  1: number;
  length: 2;
}
```

### 3. Declaration Merging (interface only)

```typescript
interface User {
  name: string;
}

interface User {
  email: string;
}

// Now User has both name and email
const user: User = { name: 'Alice', email: 'alice@example.com' };
```

This is how TypeScript extends standard library types across ES versions.

### 4. Better Error Messages (interface)

```typescript
interface Person {
  name: string;
  age: string;  // Note: string
}

// Type intersection silently creates unusable type
type TPerson = Person & { age: number };  // No error, but age is never

// Interface extension gives helpful error
interface IPerson extends Person {
  age: number;
  // ~~~ Types of property 'age' are incompatible
}
```

### 5. Type Alias Inlining

TypeScript may inline type aliases in error messages and .d.ts files:

```typescript
// In generated .d.ts, type aliases may be expanded
type Point = { x: number; y: number };
export function getOrigin(): Point { ... }

// May become:
export function getOrigin(): { x: number; y: number };

// Interfaces are preserved by name
interface IPoint { x: number; y: number }
export function getOrigin(): IPoint { ... }

// Stays as:
export function getOrigin(): IPoint;
```

## When to Use interface

### Defining Public APIs

```typescript
// Users might want to extend this
export interface RequestOptions {
  url: string;
  method?: string;
  headers?: Record<string, string>;
}

// Declaration merging allows extension
declare module 'my-lib' {
  interface RequestOptions {
    timeout?: number;  // User adds this
  }
}
```

### Object Types in General

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

interface Post {
  id: string;
  title: string;
  author: User;
}
```

## When to Use type

### Union Types

```typescript
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };
type Status = 'loading' | 'success' | 'error';
```

### Tuples and Arrays

```typescript
type Point = [x: number, y: number];
type RGB = [number, number, number];
```

### Function Types

```typescript
type Handler = (event: Event) => void;
type AsyncFn<T> = () => Promise<T>;
```

### Mapped and Conditional Types

```typescript
type Readonly<T> = { readonly [K in keyof T]: T[K] };
type NonNullable<T> = T extends null | undefined ? never : T;
```

### Computed Types

```typescript
type Keys = keyof User;  // 'id' | 'name' | 'email'
type UserValues = User[keyof User];  // string
```

## Extending Patterns

### Interface extends Interface

```typescript
interface Animal {
  name: string;
}

interface Dog extends Animal {
  breed: string;
}
```

### Type intersects Type

```typescript
type Animal = { name: string };
type Dog = Animal & { breed: string };
```

### Mixing (works both ways)

```typescript
// Interface extends type
interface Dog extends Animal { breed: string; }

// Type extends interface
type Cat = Animal & { meows: boolean };
```

## Pressure Resistance Protocol

### 1. "Just Pick One and Stick With It"

**Pressure:** "Consistency matters more than the choice"

**Response:** True, but know WHY you're choosing.

**Action:** Default to interface for objects, type for everything else.

### 2. "I Need Union of Interfaces"

**Pressure:** "My interfaces should form a union"

**Response:** You can union interfaces with a type alias.

**Action:** `type Either = InterfaceA | InterfaceB;`

## Red Flags - STOP and Reconsider

- Using `interface` for tuple types
- Using `type` when you need declaration merging
- Inconsistent usage across similar types in a codebase

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "They're exactly the same" | No, declaration merging and union types differ |
| "Type is always better" | Interface gives better errors and supports merging |
| "Interface is always better" | Can't express unions, tuples, or mapped types |

## Quick Reference

```typescript
// USE INTERFACE FOR:
interface User { name: string; }       // Object types
interface Config extends Base { }       // Extendable types

// USE TYPE FOR:
type ID = string | number;              // Unions
type Point = [number, number];          // Tuples
type Handler = () => void;              // Functions
type Keys = keyof User;                 // Computed types
type Mapped = { [K in Keys]: boolean }; // Mapped types
```

## The Bottom Line

**Use `interface` for object types, `type` for everything else.**

Interfaces support declaration merging and produce better error messages. Type aliases are required for unions, tuples, and complex type operations. Be consistent within your codebase.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 13: Know the Differences Between type and interface.
