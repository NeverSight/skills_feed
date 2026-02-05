---
name: type-narrowing
description: Use when working with union types. Use when handling nullable values. Use when TypeScript says a value might be undefined. Use when working with discriminated unions.
---

# Understand Type Narrowing

## Overview

**Type narrowing is the process by which TypeScript refines a type from broad to more specific based on control flow.**

Master narrowing to write cleaner code without type assertions, and to help TypeScript understand your logic.

## When to Use This Skill

- Working with `Type | null` or `Type | undefined`
- Handling union types like `string | number`
- Processing discriminated unions (tagged unions)
- Getting "possibly undefined" errors
- Avoiding type assertions in conditionals

## The Iron Rule

```
NEVER use type assertions when narrowing would work.
```

**No exceptions:**
- Not for "it's simpler"
- Not for "I checked it already"
- Not for "TypeScript doesn't understand"

## Detection: The "Assertion in Conditional" Smell

If you're using `as Type` inside an `if` block, you can probably narrow instead.

```typescript
// ❌ VIOLATION: Using assertion instead of narrowing
function process(value: string | null) {
  if (value !== null) {
    console.log((value as string).toUpperCase());  // Unnecessary assertion
  }
}

// ✅ CORRECT: TypeScript narrows automatically
function process(value: string | null) {
  if (value !== null) {
    console.log(value.toUpperCase());  // value is string here
    //          ^? (parameter) value: string
  }
}
```

## Narrowing Techniques

### 1. Null/Undefined Checks

```typescript
const el = document.getElementById('foo');
//    ^? const el: HTMLElement | null

if (el) {
  el.innerHTML = 'Hello';
  // ^? const el: HTMLElement
} else {
  el
  // ^? const el: null
}
```

### 2. typeof Guards

```typescript
function padLeft(value: string, padding: string | number) {
  if (typeof padding === 'number') {
    return ' '.repeat(padding) + value;
    //                ^? (parameter) padding: number
  }
  return padding + value;
  //     ^? (parameter) padding: string
}
```

### 3. instanceof Guards

```typescript
function processDate(input: Date | string) {
  if (input instanceof Date) {
    return input.toISOString();
    //     ^? (parameter) input: Date
  }
  return new Date(input).toISOString();
  //              ^? (parameter) input: string
}
```

### 4. Property Checks (in)

```typescript
interface Bird { fly(): void; }
interface Fish { swim(): void; }

function move(animal: Bird | Fish) {
  if ('fly' in animal) {
    animal.fly();
    // ^? (parameter) animal: Bird
  } else {
    animal.swim();
    // ^? (parameter) animal: Fish
  }
}
```

### 5. Discriminated Unions (Tagged Unions)

```typescript
interface Circle {
  kind: 'circle';
  radius: number;
}
interface Rectangle {
  kind: 'rectangle';
  width: number;
  height: number;
}
type Shape = Circle | Rectangle;

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
      //               ^? (parameter) shape: Circle
    case 'rectangle':
      return shape.width * shape.height;
      //     ^? (parameter) shape: Rectangle
  }
}
```

### 6. Array.isArray

```typescript
function process(input: string | string[]) {
  if (Array.isArray(input)) {
    return input.join(', ');
    //     ^? (parameter) input: string[]
  }
  return input;
  //     ^? (parameter) input: string
}
```

### 7. Throw/Return Early

```typescript
function processElement(el: HTMLElement | null) {
  if (!el) {
    throw new Error('Element not found');
  }
  // After the throw, el is narrowed
  el.innerHTML = 'Hello';
  // ^? (parameter) el: HTMLElement
}
```

## User-Defined Type Guards

When built-in narrowing isn't enough:

```typescript
interface Cat { meow(): void; }
interface Dog { bark(): void; }

// Type predicate: `pet is Cat`
function isCat(pet: Cat | Dog): pet is Cat {
  return 'meow' in pet;
}

function speak(pet: Cat | Dog) {
  if (isCat(pet)) {
    pet.meow();
    // ^? (parameter) pet: Cat
  } else {
    pet.bark();
    // ^? (parameter) pet: Dog
  }
}
```

## Common Narrowing Gotchas

### typeof null is "object"

```typescript
function process(value: string | object | null) {
  if (typeof value === 'object') {
    value  // Still includes null!
    // ^? string | object | null -> object | null
  }
}

// Fix: Check null explicitly first
function process(value: string | object | null) {
  if (value === null) return;
  if (typeof value === 'object') {
    value  // Now just object
    // ^? (parameter) value: object
  }
}
```

### Falsy Values

```typescript
function process(x?: number | string | null) {
  if (!x) {
    x  // Includes 0, "", null, undefined!
    // ^? string | number | null | undefined
  }
}
```

### Callbacks Don't Preserve Narrowing

```typescript
function processLater(value: { name?: string }) {
  if (value.name) {
    setTimeout(() => {
      console.log(value.name.toUpperCase());
      //          ~~~~~~~~~ Object is possibly 'undefined'
    }, 100);
  }
}

// Fix: Capture the narrowed value
function processLater(value: { name?: string }) {
  if (value.name) {
    const name = value.name;  // Capture as const
    setTimeout(() => {
      console.log(name.toUpperCase());  // OK
    }, 100);
  }
}
```

## Pressure Resistance Protocol

### 1. "TypeScript Doesn't Understand My Check"

**Pressure:** "I checked it, but TypeScript doesn't narrow"

**Response:** Rework your check to use a pattern TypeScript understands.

**Action:** Use one of the standard narrowing patterns. Create a type guard if needed.

### 2. "The Assertion Is Simpler"

**Pressure:** "I'll just use `as Type` instead of an if statement"

**Response:** Assertions don't verify at runtime. Narrowing does.

**Action:** Write the check. Your code will be safer.

## Red Flags - STOP and Reconsider

- `as Type` inside an if/switch block
- Narrowing that doesn't work (check the pattern)
- `typeof x === 'object'` without null check
- Falsy checks on values that could be 0 or ""
- Using `!` instead of proper null checks

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "I already checked it" | If TypeScript doesn't see the check, it doesn't count. |
| "The assertion is shorter" | Shorter code isn't always better code. |
| "TypeScript is wrong" | Rework your check to use a pattern TS understands. |

## Quick Reference

| You Have | Use | Narrows To |
|----------|-----|------------|
| `T \| null` | `if (x)` or `if (x !== null)` | `T` |
| `string \| number` | `typeof x === 'string'` | `string` |
| `Dog \| Cat` | `x instanceof Dog` | `Dog` |
| `A \| B` (with `kind`) | `switch (x.kind)` | `A` or `B` |
| Complex check | User-defined type guard | Your type |

## The Bottom Line

**Let TypeScript narrow types through control flow. Don't bypass it with assertions.**

Use standard narrowing patterns. Create type guards when needed. Capture values before callbacks. TypeScript's narrowing is powerful - learn to work with it, not around it.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 22: Understand Type Narrowing.
