---
name: nextfriday-types
description: Next Friday TypeScript patterns for props, interfaces, and return types. Use when defining types or writing function signatures.
user-invocable: false
---

# Next Friday Types

Rules for TypeScript type definitions and annotations.

## React Props

### Props Suffix

Interfaces in component files must end with `Props`.

```tsx
// Bad: Card.tsx
interface Card {}

// Good: Card.tsx
interface CardProps {}
```

### Readonly Props

Component props must be wrapped with `Readonly<>`.

```tsx
// Bad:
const Card = (props: CardProps) => ...

// Good:
const Card = (props: Readonly<CardProps>) => ...
```

### No Inline Types

Use interface declarations, not inline types.

```tsx
// Bad:
const Card = (props: { title: string; onClick: () => void }) => ...

// Good:
interface CardProps {
  title: string;
  onClick: () => void;
}

const Card = (props: Readonly<CardProps>) => ...
```

## Function Parameters

### Named Param Types

Extract inline object types to named interfaces.

```typescript
// Bad:
function processData({ id, name }: { id: string; name: string }) {}

// Good:
interface ProcessDataParams {
  id: string;
  name: string;
}

function processData(params: ProcessDataParams) {}
```

### Destructuring Params

Use object destructuring for multiple parameters.

```typescript
// Bad:
function createItem(id: string, name: string, price: number, category: string) {}

// Good:
interface CreateItemParams {
  id: string;
  name: string;
  price: number;
  category: string;
}

function createItem(params: CreateItemParams) {}
```

## Return Types

### Explicit Return Types

Always specify return types on functions.

```typescript
// Bad:
function formatValue(value: number) {
  return value.toFixed(2);
}

// Good:
function formatValue(value: number): string {
  return value.toFixed(2);
}
```

## Quick Reference

| Rule | Pattern |
| ---- | ------- |
| Props suffix | `CardProps`, not `Card` |
| Readonly props | `props: Readonly<Props>` |
| No inline types | Use interfaces |
| Named param types | Extract to interfaces |
| Destructuring | `(params: Params)` not `(a, b, c)` |
| Explicit return | `: string`, `: Promise<Data>` |
