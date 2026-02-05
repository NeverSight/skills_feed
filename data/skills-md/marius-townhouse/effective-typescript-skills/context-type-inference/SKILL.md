---
name: context-type-inference
description: Use when extracting values causes type errors. Use when callback types are wrong. Use when const assertions are needed.
---

# Understand How Context Is Used in Type Inference

## Overview

**Separating a value from its context can cause type errors.**

TypeScript infers types based on both the value AND where it's used. When you extract a value to a variable, you lose context, which can cause surprising type errors.

## When to Use This Skill

- Extracting a value to a constant causes type errors
- Callback parameters have wrong types
- Tuple types becoming array types
- String literals becoming general strings

## The Iron Rule

```
When extraction breaks types, restore context with:
annotations, const assertions, or satisfies.
```

**Remember:**
- TypeScript uses context from function parameters
- Extracted values lose that context
- `as const` prevents widening
- `satisfies` preserves context with validation

## Detection: Lost Context

```typescript
type Language = 'JavaScript' | 'TypeScript' | 'Python';

function setLanguage(language: Language) { /* ... */ }

setLanguage('JavaScript');  // OK - context from parameter

let language = 'JavaScript';  // Inferred as string (widened)
setLanguage(language);
//          ~~~~~~~~
// Argument of type 'string' is not assignable to 'Language'
```

The value was widened to `string` when extracted.

## Solution 1: Type Annotation

```typescript
let language: Language = 'JavaScript';
setLanguage(language);  // OK
```

The annotation provides the context.

## Solution 2: const Declaration

```typescript
const language = 'JavaScript';
//    ^? const language: "JavaScript"
setLanguage(language);  // OK
```

`const` variables get narrower types (literal types).

## Solution 3: const Assertion

```typescript
let language = 'JavaScript' as const;
//  ^? let language: "JavaScript"
setLanguage(language);  // OK
```

`as const` prevents widening even with `let`.

## Tuple Types: A Common Case

```typescript
function panTo(where: [number, number]) { /* ... */ }

panTo([10, 20]);  // OK - inferred as tuple from context

const loc = [10, 20];
//    ^? const loc: number[]  (array, not tuple!)
panTo(loc);
//    ~~~
// Argument of type 'number[]' is not assignable to '[number, number]'
```

### Fix with Annotation

```typescript
const loc: [number, number] = [10, 20];
panTo(loc);  // OK
```

### Fix with const Assertion

```typescript
const loc = [10, 20] as const;
//    ^? const loc: readonly [10, 20]
```

Note: `as const` makes it `readonly`. If the function expects a mutable tuple, this won't work:

```typescript
panTo(loc);
//    ~~~
// 'readonly [10, 20]' is not assignable to '[number, number]'
```

The function should accept `readonly [number, number]` if it doesn't mutate the input.

## Object Properties

```typescript
type Point = [number, number];

const capitals1 = { ny: [-73.7562, 42.6526], ca: [-121.4944, 38.5816] };
//    ^? { ny: number[]; ca: number[]; }  (arrays, not tuples)

const capitals2 = {
  ny: [-73.7562, 42.6526],
  ca: [-121.4944, 38.5816],
} satisfies Record<string, Point>;
//    ^? { ny: [number, number]; ca: [number, number]; }  (tuples!)
```

`satisfies` provides context while preserving precise types.

## satisfies vs Annotation

```typescript
const capitals3: Record<string, Point> = capitals2;
capitals3.pr;  // No error! Property 'pr' returns Point (but undefined at runtime)
//        ^? Point

capitals2.pr;
//        ~~
// Property 'pr' does not exist
```

`satisfies` keeps precise keys; annotation doesn't.

## Callback Context

TypeScript infers callback parameter types from context:

```typescript
// Types inferred from app.get declaration
app.get('/health', (request, response) => {
  //                ^? Request<...>
  //                          ^? Response<...>
  response.send('OK');
});

// Don't add redundant annotations:
app.get('/health', (request: express.Request, response: express.Response) => {
  // Redundant and verbose
});
```

## Extracted Callbacks

```typescript
// Context lost when callback is extracted
const handler = (request, response) => {
  //             ^? any    ^? any
  response.send('OK');
};

// Fix: Add types
const handler: express.RequestHandler = (request, response) => {
  //                                      ^? Request  ^? Response
  response.send('OK');
};
```

## Object Methods

```typescript
const config = {
  language: 'JavaScript' as const,
  //        ^? "JavaScript" (not string)
};

setLanguage(config.language);  // OK
```

Without `as const`, `config.language` would be `string`.

## Deep const Assertions

```typescript
const obj = {
  settings: {
    language: 'JavaScript',
    version: 4,
  }
} as const;
// ^? { readonly settings: { readonly language: "JavaScript"; readonly version: 4; } }
```

`as const` is deep - everything becomes readonly with literal types.

## Pressure Resistance Protocol

### 1. "Just Add a Type Assertion"

**Pressure:** "I'll use `as Language` to fix it"

**Response:** Type assertions bypass safety. Use const or satisfies instead.

**Action:** Use `as const` for literal narrowing, not `as Type`.

### 2. "It Worked Inline"

**Pressure:** "Why doesn't it work when I extract it?"

**Response:** Context was lost. Restore it explicitly.

**Action:** Add annotation, use `const`, or use `satisfies`.

## Red Flags - STOP and Reconsider

- Type errors after extracting a value to a variable
- Callback parameters typed as `any`
- Tuples becoming arrays
- String literals becoming `string`

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's the same value" | Same value, different context = different inferred type |
| "TypeScript should know" | TypeScript needs context to infer precise types |
| "I'll use `as` to fix it" | Use `as const` or `satisfies`, not type assertions |

## Quick Reference

```typescript
type Lang = 'JS' | 'TS';
declare function setLang(l: Lang): void;

// DON'T: Lose context
let lang = 'JS';  // string
setLang(lang);    // Error

// DO: Annotation
let lang: Lang = 'JS';

// DO: const
const lang = 'JS';  // "JS"

// DO: const assertion
let lang = 'JS' as const;  // "JS"

// For objects: satisfies
const cfg = { lang: 'JS' } satisfies Record<string, Lang>;
```

## The Bottom Line

**Context matters for type inference.**

When you extract a value, you may lose type context. Restore it with type annotations, `const` declarations, `as const` assertions, or `satisfies`. Understand which tool fits each situation.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 24: Understand How Context Is Used in Type Inference.
