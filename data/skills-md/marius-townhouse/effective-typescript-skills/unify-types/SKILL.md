---
name: unify-types
description: Use when similar types have minor differences. Use when union types become complex. Use when choosing between modeling differences.
---

# Prefer Unifying Types to Modeling Differences

## Overview

**Minor differences often don't warrant separate types.**

When types are almost identical, unifying them simplifies your code. The cost of handling small differences is usually less than maintaining parallel type hierarchies.

## When to Use This Skill

- Types that differ by one or two properties
- Union types that are mostly the same
- Considering separate types for variants
- Simplifying complex type relationships

## The Iron Rule

```
Unify types unless differences are fundamental.
Small variations can be handled at runtime.
```

**Remember:**
- Duplicate types = duplicate handling code
- Union of similar types = repeated narrowing
- One flexible type is often simpler than many specific ones
- Question: do the differences REALLY matter to the type system?

## Detection: Parallel Types

```typescript
// Two types that are almost identical
interface Dog {
  name: string;
  breed: string;
  barkVolume: number;
}

interface Cat {
  name: string;
  breed: string;
  meowVolume: number;
}

type Pet = Dog | Cat;

// Every function needs to narrow:
function getPetInfo(pet: Pet): string {
  if ('barkVolume' in pet) {
    return `${pet.name} barks at ${pet.barkVolume}`;
  } else {
    return `${pet.name} meows at ${pet.meowVolume}`;
  }
}
```

## Unified Approach

```typescript
interface Pet {
  name: string;
  breed: string;
  vocalizationType: 'bark' | 'meow';
  vocalizationVolume: number;
}

function getPetInfo(pet: Pet): string {
  return `${pet.name} ${pet.vocalizationType}s at ${pet.vocalizationVolume}`;
}
```

No narrowing needed. One type handles both cases.

## When to Keep Types Separate

### Fundamentally Different Behaviors

```typescript
// These really are different
interface File {
  path: string;
  read(): Buffer;
  write(data: Buffer): void;
}

interface Directory {
  path: string;
  list(): string[];
  create(name: string): void;
}
```

Files and directories have different operations. Unifying would lose type safety.

### Different Cardinalities

```typescript
// Different structures
interface SingleResult {
  value: number;
}

interface MultipleResults {
  values: number[];
  average: number;
}
```

These have genuinely different shapes.

## Practical Example: API Responses

```typescript
// Separate types
interface SuccessResponse {
  status: 'success';
  data: Data;
  timestamp: Date;
}

interface ErrorResponse {
  status: 'error';
  error: string;
  timestamp: Date;
}

type Response = SuccessResponse | ErrorResponse;

// Handling requires narrowing everywhere
function logResponse(res: Response) {
  console.log(`${res.timestamp}: ${res.status}`);
  if (res.status === 'success') {
    console.log(res.data);  // Need to narrow
  }
}
```

Consider if unified is simpler:

```typescript
// Unified type
interface Response {
  status: 'success' | 'error';
  data?: Data;      // Present on success
  error?: string;   // Present on error
  timestamp: Date;
}

// Can access common fields without narrowing
function logResponse(res: Response) {
  console.log(`${res.timestamp}: ${res.status}`);
  if (res.data) {
    console.log(res.data);
  }
}
```

## The Tagged Union Middle Ground

Sometimes a tagged union is the right balance:

```typescript
// Tagged union: explicit about differences, unified handling
interface Animal {
  name: string;
  breed: string;
}

interface Dog extends Animal {
  type: 'dog';
  barkVolume: number;
}

interface Cat extends Animal {
  type: 'cat';
  meowVolume: number;
}

type Pet = Dog | Cat;

// Common operations don't need narrowing
function getName(pet: Pet): string {
  return pet.name;  // Works for both
}

// Type-specific operations are explicit
function getVolume(pet: Pet): number {
  return pet.type === 'dog' ? pet.barkVolume : pet.meowVolume;
}
```

## Cost-Benefit Analysis

Before creating separate types, ask:

1. **How often do I need type-specific behavior?**
   - Rarely → Unify
   - Frequently → Separate

2. **Are the differences structural or semantic?**
   - Same structure, different meaning → Maybe unify
   - Different structure → Keep separate

3. **Will unifying lose important type safety?**
   - Yes → Keep separate
   - No → Unify

## Real Example: Events

```typescript
// Over-differentiated
interface ClickEvent {
  type: 'click';
  x: number;
  y: number;
  target: Element;
}

interface KeyEvent {
  type: 'key';
  key: string;
  target: Element;
}

interface ScrollEvent {
  type: 'scroll';
  scrollTop: number;
  target: Element;
}
```

Could unify common parts:

```typescript
interface BaseEvent {
  type: string;
  target: Element;
}

interface ClickEvent extends BaseEvent {
  type: 'click';
  x: number;
  y: number;
}

// etc.
```

Or fully unify if differences rarely matter:

```typescript
interface UIEvent {
  type: 'click' | 'key' | 'scroll';
  target: Element;
  details: ClickDetails | KeyDetails | ScrollDetails;
}
```

## Pressure Resistance Protocol

### 1. "Types Should Be Precise"

**Pressure:** "Separate types are more accurate"

**Response:** Precision has a cost in code complexity.

**Action:** Weigh precision benefits against handling complexity.

### 2. "They Might Diverge Later"

**Pressure:** "Keep them separate for future flexibility"

**Response:** That's YAGNI. Refactor if they actually diverge.

**Action:** Unify now; separate later if needed.

## Red Flags - STOP and Reconsider

- Union types where most properties are shared
- Repeated narrowing code for similar types
- Types that differ by one property name
- Parallel implementations for "different" types

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "They're conceptually different" | Code doesn't care about concepts |
| "Separate types are cleaner" | More types = more handling code |
| "We might need the distinction" | Cross that bridge when you come to it |

## Quick Reference

```typescript
// DON'T: Separate types for minor differences
interface Dog { name: string; bark: () => void; }
interface Cat { name: string; meow: () => void; }
type Pet = Dog | Cat;

// DO: Unified type
interface Pet {
  name: string;
  sound: 'bark' | 'meow';
  makeSound: () => void;
}

// DO: Keep separate when genuinely different
interface File { read(): Buffer; write(b: Buffer): void; }
interface Directory { list(): string[]; }
```

## The Bottom Line

**Unify types unless differences are fundamental.**

Separate types mean separate handling code everywhere. When types share most properties and differ only in details, a unified type with optional or variant fields is often simpler.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 39: Prefer Unifying Types to Modeling Differences.
