---
name: typescript-advanced-patterns
description: Advanced TypeScript patterns for type-safe, maintainable code using sophisticated type system features. Use when building type-safe APIs, implementing complex domain models, or leveraging TypeScript's advanced type capabilities.
---

# Skill: typescript

## Scope

- Applies to: TypeScript v5+ advanced type system features, type-safe APIs, complex domain models, sophisticated type inference, compile-time guarantees
- Does NOT cover: Basic TypeScript syntax, framework-specific patterns, runtime validation libraries (use Zod separately)

## Assumptions

- TypeScript v5+
- Strict mode enabled (`"strict": true` in `tsconfig.json`)
- Target: ES2020+ or higher

## Principles

- Use conditional types for type selection based on conditions
- Use mapped types for systematic object type transformations
- Use type guards (`value is Type`) for runtime checking with type narrowing
- Use discriminated unions for type-safe state machines with exhaustiveness checking
- Use branded types to prevent primitive mixing
- Prefer `unknown` over `any` for type safety
- Use type guards over type assertions (`as Type`)
- Keep types composable and shallow (avoid deep nesting)
- Mark immutable data structures as `readonly`

## Constraints

### MUST

- Enable strict mode (`"strict": true` in `tsconfig.json`)
- Use `unknown` instead of `any` for untyped values
- Use type guards (`value is Type`) instead of type assertions when possible

### SHOULD

- Use `type` for unions/utilities, `interface` for object shapes
- Keep types composable and shallow
- Mark immutable data structures as `readonly`
- Use branded types to prevent primitive mixing

### AVOID

- Using `any` (use `unknown` with type guards)
- Type assertions without validation
- Overusing generics (only when types truly vary)
- Deep type nesting (slow compilation, hard to debug)

## Interactions

- Works with [zod](https://zod.dev) for runtime validation with type inference
- Complements [nextjs](@cursor/skills/nextjs-v16/SKILL.md) for type-safe API routes
- Complements [fastify](@cursor/skills/fastify-v5/SKILL.md) for type-safe route schemas

## Patterns

### Mapped Types

Transform object types systematically:

```typescript
type Partial<T> = { [P in keyof T]?: T[P] }
type Readonly<T> = { readonly [P in keyof T]: T[P] }
type Pick<T, K extends keyof T> = { [P in K]: T[P] }
```

### Type Guards

Runtime type checking with type narrowing:

```typescript
function isString(value: unknown): value is string {
  return typeof value === 'string'
}

function isSuccess(result: Result): result is Success {
  return result.status === 'success'
}
```

### Branded Types

Create nominal types for type safety:

```typescript
type UserId = string & { readonly __brand: 'UserId' }
type PostId = string & { readonly __brand: 'PostId' }

function createUserId(id: string): UserId {
  return id as UserId
}
```

### Discriminated Unions

Type-safe state machines with exhaustiveness checking:

```typescript
type LoadingState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: string[] }
  | { status: 'error'; error: Error }
```

## References

- [Conditional Types](references/conditional-types.md) - Type selection based on conditions
- [Advanced Generics](references/advanced-generics.md) - Generic constraints and inference patterns
- [Discriminated Unions](references/discriminated-unions.md) - Type-safe state machines

## Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [Type Challenges](https://github.com/type-challenges/type-challenges)
- [ts-toolbelt](https://github.com/millsp/ts-toolbelt) - Advanced type utilities library
