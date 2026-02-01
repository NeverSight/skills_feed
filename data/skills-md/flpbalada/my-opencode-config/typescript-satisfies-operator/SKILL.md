---
name: typescript-satisfies-operator
description: Guides proper usage of TypeScript's satisfies operator vs type annotations. Use this skill when deciding between type annotations (colon) and satisfies, validating object shapes while preserving literal types, or troubleshooting type inference issues.
---

# TypeScript: The `satisfies` Operator

## Core Concept

The `satisfies` operator validates that an expression matches a type **without changing the inferred type**. This is different from type annotations (`:`) which widen the type.

**Key insight from Matt Pocock:**

- "When you use a colon, the type BEATS the value"
- "When you use `satisfies`, the value BEATS the type"

## Type Annotation vs Satisfies

```typescript
type RoutingPathname = "/products" | "/cart" | "/checkout";

// Type annotation - widens to union
const url1: RoutingPathname = "/products";
// url1 is typed as: RoutingPathname (wide)

// Satisfies - keeps literal
const url2 = "/products" satisfies RoutingPathname;
// url2 is typed as: '/products' (narrow)

// Why it matters:
const test1: "/products" = url1; // Error: RoutingPathname not assignable to '/products'
const test2: "/products" = url2; // Works
```

## Classic Use Case: Object Validation with Preserved Types

```typescript
type Colors = "red" | "green" | "blue";
type RGB = [red: number, green: number, blue: number];

// Type annotation loses specific property types
const palette1: Record<Colors, string | RGB> = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255],
};
palette1.green.toUpperCase(); // Error: 'toUpperCase' doesn't exist on string | RGB

// Satisfies validates AND preserves literal types
const palette2 = {
  red: [255, 0, 0],
  green: "#00ff00",
  bleu: [0, 0, 255], // Error: Typo caught!
} satisfies Record<Colors, string | RGB>;
palette2.green.toUpperCase(); // Works - green is inferred as string
```

## When to Use What

| Annotation Style | Type vs Value | Use Case                           |
| ---------------- | ------------- | ---------------------------------- |
| `: Type` (colon) | Type wins     | Need wider type for reassignment   |
| `satisfies Type` | Value wins    | Need validation + narrow inference |
| `as Type`        | Lies to TS    | Escape hatch (use sparingly!)      |
| No annotation    | Inference     | Most common - let TS infer         |

## Rule of Thumb

**Use `satisfies` when:**

1. You want the EXACT type of the variable, not the wider type
2. The type is complex enough that you want validation you didn't mess it up

**Use colon annotation when:**

1. You need to reassign the variable later with different values of the union
2. You explicitly want the wider type

## Common Pattern: `as const satisfies`

Combine `as const` for immutability with `satisfies` for validation:

```typescript
const routes = {
  home: "/",
  products: "/products",
  cart: "/cart",
} as const satisfies Record<string, string>;

// routes.home is typed as '/' (readonly literal)
// But validated against Record<string, string>
```

## Real-World Examples

### Configuration Objects

```typescript
type Config = {
  api: string;
  timeout: number;
  retries: number;
};

// Validates shape, but keeps literal types for autocomplete
const config = {
  api: "https://api.example.com",
  timeout: 5000,
  retries: 3,
} satisfies Config;

// config.api is 'https://api.example.com', not string
```

### Event Handlers Map

```typescript
type EventMap = Record<string, (...args: unknown[]) => void>;

const handlers = {
  click: (x: number, y: number) => console.log(x, y),
  submit: (data: FormData) => console.log(data),
} satisfies EventMap;

// handlers.click is (x: number, y: number) => void
// Not (...args: unknown[]) => void
```

### Exhaustive Checks with Records

```typescript
type Status = "pending" | "approved" | "rejected";

const statusLabels = {
  pending: "Waiting for review",
  approved: "Approved",
  rejected: "Rejected",
} satisfies Record<Status, string>;

// If you add a new Status, TypeScript will error until you add it here
```

## References

- [TypeScript 4.9 Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#the-satisfies-operator)
- [Matt Pocock - Clarifying the satisfies Operator](https://www.totaltypescript.com/clarifying-the-satisfies-operator)
- [GitHub Issue #47920 - Original Proposal](https://github.com/microsoft/TypeScript/issues/47920)
