---
name: types-as-sets
description: Use when reasoning about type relationships. Use when confused by union or intersection types. Use when extends feels counterintuitive.
---

# Think of Types as Sets of Values

## Overview

**A type is a set of possible values. Assignability means subset.**

Understanding types as sets helps you reason about unions, intersections, `extends`, and `never`. This mental model makes TypeScript's behavior intuitive.

## When to Use This Skill

- Confused why `A & B` has MORE properties than `A` or `B`
- Don't understand why `extends` means "subset"
- Reasoning about union and intersection types
- Working with `never` or `unknown` types
- Debugging "not assignable to" errors

## The Iron Rule

```
ALWAYS think "subset" when you see "extends" or "assignable to".
```

**Remember:**
- Union (`|`) = larger set (union of domains)
- Intersection (`&`) = smaller set (intersection of domains)
- `extends` = "is a subset of"
- `never` = empty set (no values)
- `unknown` = universal set (all values)

## Detection: The "Assignability" Confusion

If you're confused by assignability errors, think in terms of sets:

```typescript
type AB = 'A' | 'B';
type AB12 = 'A' | 'B' | 12;

const ab: AB = 'A';        // OK: 'A' is in {'A', 'B'}
const ab12: AB12 = ab;     // OK: {'A', 'B'} ⊆ {'A', 'B', 12}

declare let twelve: AB12;
const back: AB = twelve;   // Error!
// {'A', 'B', 12} is NOT a subset of {'A', 'B'}
```

## The Set Theory Mental Model

### TypeScript to Set Theory Translation

| TypeScript | Set Theory | Meaning |
|------------|------------|---------|
| `never` | ∅ (empty set) | No values |
| Literal type `"A"` | Single element {A} | One value |
| `T1 \| T2` | T1 ∪ T2 (union) | Values in either |
| `T1 & T2` | T1 ∩ T2 (intersection) | Values in both |
| `unknown` | Universal set | All values |
| `extends` | ⊆ (subset) | "Is contained in" |
| "assignable to" | ⊆ (subset) | "Is contained in" |

### Why Intersection `&` ADDS Properties

This seems counterintuitive at first:

```typescript
interface Person { name: string; }
interface Lifespan { birth: Date; death?: Date; }

type PersonSpan = Person & Lifespan;

// PersonSpan has MORE properties, not fewer!
const ps: PersonSpan = {
  name: 'Alan Turing',
  birth: new Date('1912/06/23'),
  death: new Date('1954/06/07'),
};  // OK
```

**Why?** Because we're intersecting SETS OF VALUES, not properties.
- Person = all objects with a `name` property
- Lifespan = all objects with `birth` (and optional `death`)
- Person & Lifespan = objects that have BOTH sets of properties

The set of values is SMALLER, but each value has MORE properties.

### Why Union `|` Has FEWER Guaranteed Properties

```typescript
type K = keyof (Person | Lifespan);
//   ^? type K = never

// No keys are guaranteed on BOTH Person AND Lifespan
```

The set of values is LARGER, but we can rely on FEWER properties.

## The `extends` Keyword

In TypeScript, `extends` means "subset of":

```typescript
interface Vector1D { x: number; }
interface Vector2D extends Vector1D { y: number; }
interface Vector3D extends Vector2D { z: number; }

// Vector3D ⊆ Vector2D ⊆ Vector1D (as sets of values)
// A Vector3D IS-A Vector2D IS-A Vector1D
```

This also applies to generic constraints:

```typescript
function getKey<K extends string>(val: any, key: K) { /* ... */ }

// K can be any subset of string:
getKey({}, 'x');                           // OK: 'x' ⊆ string
getKey({}, Math.random() < 0.5 ? 'a' : 'b'); // OK: 'a'|'b' ⊆ string
getKey({}, 12);                            // Error: number ⊄ string
```

## The `never` Type (Empty Set)

`never` is the empty set - it contains no values:

```typescript
const x: never = 12;
//    ~ Type 'number' is not assignable to type 'never'.

// never is useful for exhaustiveness checking
function assertNever(x: never): never {
  throw new Error('Unexpected value: ' + x);
}
```

## The `unknown` Type (Universal Set)

`unknown` is the universal set - all values are assignable to it:

```typescript
const x: unknown = 'hello';  // OK
const y: unknown = 42;       // OK
const z: unknown = null;     // OK

// But you can't use unknown without narrowing
const str: string = x;  // Error: must narrow first
```

## Arrays vs Tuples

```typescript
const list = [1, 2];
//    ^? const list: number[]

const tuple: [number, number] = list;
// Error! number[] is not assignable to [number, number]
// Because: there exist number[] that aren't pairs ([], [1], [1,2,3])
```

The set `number[]` is NOT a subset of `[number, number]`.

## Practical Applications

### Understanding Generic Constraints

```typescript
// T must be a subset of objects with an 'id' property
function getById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}
```

### Understanding Conditional Types

```typescript
// "If A is a subset of B, then X, else Y"
type IsString<T> = T extends string ? true : false;

type A = IsString<'hello'>;  // true ('hello' ⊆ string)
type B = IsString<number>;   // false (number ⊄ string)
```

## Pressure Resistance Protocol

### 1. "Intersection Should Have Fewer Properties"

**Pressure:** "A & B should have properties common to both"

**Response:** We're intersecting sets of VALUES, not properties.

**Action:** Think: "What objects satisfy BOTH interfaces?"

### 2. "extends Means Inheritance"

**Pressure:** "extends is about class inheritance"

**Response:** In types, `extends` means "subset of".

**Action:** Replace "extends" with "is a subset of" when reading.

## Red Flags - STOP and Reconsider

- Thinking `&` removes properties
- Thinking `|` adds properties
- Confusing `extends` with classical inheritance
- Forgetting that object types are "open" (allow extra properties)

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Intersection means common parts" | It's about VALUES, not properties |
| "extends means inherits" | In types, it means "is subset of" |
| "Union has all properties" | Union only guarantees common properties |

## Quick Reference

| Type Expression | Set Interpretation | Size |
|-----------------|-------------------|------|
| `never` | Empty set | 0 values |
| `"A"` | Singleton | 1 value |
| `"A" \| "B"` | Union | 2 values |
| `string` | All strings | ∞ values |
| `unknown` | Universal set | All values |
| `A & B` | Intersection | Usually smaller |
| `A \| B` | Union | Usually larger |

## The Bottom Line

**Types are sets of values. Assignability is subset checking.**

Understanding this makes TypeScript's behavior intuitive. `extends` means "subset of", `&` intersects value sets (resulting in more required properties), and `|` unions value sets (resulting in fewer guaranteed properties).

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 7: Think of Types as Sets of Values.
