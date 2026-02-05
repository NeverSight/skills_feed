---
name: avoid-inferable-annotations
description: Use when writing type annotations on variables. Use when TypeScript can infer the type. Use when code feels cluttered with types.
---

# Avoid Cluttering Your Code with Inferable Types

## Overview

**Don't write type annotations when TypeScript can infer the same type.**

Redundant type annotations add noise, increase maintenance burden, and can actually hide bugs. Let TypeScript do its job.

## When to Use This Skill

- Declaring variables with obvious types
- Destructuring assignments
- Writing function implementations
- Reviewing code with verbose annotations
- Refactoring type-heavy code

## The Iron Rule

```
NEVER annotate types that TypeScript can correctly infer.
```

**Exceptions allowed for:**
- Object literals (to enable excess property checking)
- Public API function signatures
- When inference gives the wrong type

## Detection: The "Redundant Annotation Smell"

Hover over a variable. If the inferred type matches your annotation, remove it.

```typescript
// ❌ VIOLATION: Redundant annotations
let x: number = 12;
const name: string = 'Alice';
const numbers: number[] = [1, 2, 3];

// ✅ CORRECT: Let TypeScript infer
let x = 12;
const name = 'Alice';
const numbers = [1, 2, 3];
```

## Complex Objects: Still Inferred

```typescript
// ❌ VERBOSE: Don't do this
const person: {
  name: string;
  born: {
    where: string;
    when: string;
  };
} = {
  name: 'Sojourner Truth',
  born: {
    where: 'Swartekill, NY',
    when: 'c.1797',
  },
};

// ✅ CONCISE: Just write the value
const person = {
  name: 'Sojourner Truth',
  born: {
    where: 'Swartekill, NY',
    when: 'c.1797',
  },
};
// TypeScript infers the exact same type!
```

## Function Parameters: Annotation Required

```typescript
// Parameters need types (TypeScript can't infer them)
function greet(name: string) {
  return `Hello, ${name}`;
}

// Return type is inferred - no need to annotate
function square(x: number) {
  return x * x;  // TypeScript infers number
}
```

## Callback Parameters: Often Inferred

```typescript
// ❌ VERBOSE: Unnecessary parameter types
app.get('/health', (request: express.Request, response: express.Response) => {
  response.send('OK');
});

// ✅ CONCISE: Let context provide the types
app.get('/health', (request, response) => {
  response.send('OK');  // Types are inferred from context
});
```

## When TO Annotate: Object Literals

```typescript
interface Product {
  id: string;
  name: string;
  price: number;
}

// ✅ ANNOTATE: Enables excess property checking
const elmo: Product = {
  id: '123',
  name: 'Tickle Me Elmo',
  price: 28.99,
  inStock: true,  // Error! 'inStock' does not exist in type 'Product'
};

// ❌ NO ANNOTATION: Error appears far from definition
const furby = {
  id: 456,        // Wrong type! But no error here...
  name: 'Furby',
  price: 35,
};
logProduct(furby);  // Error appears here, far from the mistake
//         ~~~~~ Types of property 'id' are incompatible
```

## When TO Annotate: Function Return Types

Consider explicit return types for:

### 1. Functions with Multiple Returns

```typescript
// Without annotation, easy to miss inconsistencies
function getQuote(ticker: string) {
  if (cache[ticker]) {
    return cache[ticker];  // Returns number
  }
  return fetch(`/api/${ticker}`).then(r => r.json());  // Returns Promise<any>
}
// Inferred: number | Promise<any> - probably not what you wanted!

// With annotation, TypeScript catches the bug
function getQuote(ticker: string): Promise<number> {
  if (cache[ticker]) {
    return cache[ticker];  // Error: Type 'number' is not assignable to 'Promise<number>'
  }
  return fetch(`/api/${ticker}`).then(r => r.json());
}
```

### 2. Public API Functions

```typescript
// For library functions, explicit types are documentation
export function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

### 3. Named Return Types

```typescript
interface Vector2D { x: number; y: number; }

// Without annotation: { x: number; y: number; }
function add(a: Vector2D, b: Vector2D) {
  return { x: a.x + b.x, y: a.y + b.y };
}

// With annotation: Vector2D (clearer, documented)
function add(a: Vector2D, b: Vector2D): Vector2D {
  return { x: a.x + b.x, y: a.y + b.y };
}
```

## Destructuring: Especially Bad

```typescript
// ❌ TERRIBLE: Destructuring with types is ugly
function logProduct(product: Product) {
  const {id, name, price}: {id: string; name: string; price: number} = product;
  console.log(id, name, price);
}

// ✅ CLEAN: Just destructure
function logProduct(product: Product) {
  const {id, name, price} = product;
  console.log(id, name, price);
}
```

## Pressure Resistance Protocol

### 1. "Explicit Is Better"

**Pressure:** "I want all types visible in the code"

**Response:** Redundant annotations add noise. Use your editor's hover feature to see types.

**Action:** Remove redundant annotations. Trust the inference.

### 2. "What If Inference Changes?"

**Pressure:** "If I change the value, the type might change"

**Response:** That's often what you want! Your types evolve with your code.

**Action:** Add annotations only where you need to constrain the type.

### 3. "New Developers Won't Know"

**Pressure:** "Junior devs need to see the types"

**Response:** Modern editors show inferred types. Redundant annotations aren't teaching.

**Action:** Rely on editor tooling. Write meaningful type names, not verbose annotations.

## Red Flags - STOP and Reconsider

- `: number` on a variable initialized with a number literal
- `: string` on a variable initialized with a string literal
- Types on destructured variables
- Parameter types in callbacks where context provides them
- Same type appearing in both annotation and value

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's more readable" | Extra noise hurts readability. |
| "What if inference is wrong?" | Then add an annotation for that case. |
| "Code reviews need types" | Reviewers can hover in modern tools. |
| "Consistency" | Consistent non-redundancy is better. |

## Quick Reference

| Situation | Annotate? |
|-----------|-----------|
| Variable with literal value | No |
| Object literal for known type | Yes (excess checking) |
| Destructured variables | No |
| Function parameters | Yes |
| Function return (simple) | Usually no |
| Function return (complex/public) | Yes |
| Callback parameters | Usually no |

## The Bottom Line

**TypeScript is good at inferring types. Let it.**

Annotate function parameters and public APIs. Annotate object literals to get excess property checking. For everything else, let TypeScript infer the types and keep your code clean.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 18: Avoid Cluttering Your Code with Inferable Types.
