---
name: writing-typescript
description: Idiomatic TypeScript development. Use when writing TypeScript code, Node.js services, React apps, or discussing TS patterns. Emphasizes strict typing, composition, and modern tooling (bun/vite).
user-invocable: false
context: fork
agent: typescript-engineer
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# TypeScript Development (5.x)

## Core Philosophy

1. **Strict Mode Always**
   - Enable all strict checks in tsconfig
   - Treat `any` as a bug—use `unknown` for untrusted input
   - noUncheckedIndexedAccess, exactOptionalPropertyTypes

2. **Interface vs Type**
   - interface for object shapes (extensible, mergeable)
   - type for unions, intersections, mapped types
   - interface for React props and public APIs

3. **Discriminated Unions**
   - Literal `kind`/`type` tag for variants
   - Exhaustive switch with never check
   - Model states as unions, not boolean flags

4. **Flat Control Flow**
   - Guard clauses with early returns
   - Type guards and predicate helpers
   - Maximum 2 levels of nesting

5. **Result Type Pattern**
   - Result<T, E> for explicit error handling
   - Discriminated union for success/failure
   - Custom Error subclasses for instanceof

## Quick Patterns

### Discriminated Unions (Not Boolean Flags)

```typescript
// GOOD: discriminated union for state
type LoadState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: string };

// BAD: boolean flags
type LoadState = {
  isLoading: boolean;
  isError: boolean;
  data: T | null;
  error: string | null;
};
```

### Flat Control Flow (No Nesting)

```typescript
// GOOD: guard clauses, early returns
function process(user: User | null): Result<Data> {
  if (!user) return err("no user");
  if (!user.isActive) return err("inactive");
  if (user.role !== "admin") return err("not admin");
  return ok(doWork(user)); // happy path at end
}

// BAD: nested conditions
function process(user: User | null): Result<Data> {
  if (user) {
    if (user.isActive) {
      if (user.role === "admin") {
        return ok(doWork(user));
      }
    }
  }
  return err("invalid");
}
```

### Type Guards

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}

// Predicate helper for flat code
const isActiveAdmin = (u: User | null): u is User & { role: "admin" } =>
  !!u && u.isActive && u.role === "admin";
```

### Result Type

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

const ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
const err = <E>(error: E): Result<never, E> => ({ ok: false, error });

async function fetchUser(
  id: string,
): Promise<Result<User, "not-found" | "network">> {
  try {
    const res = await fetch(`/users/${id}`);
    if (res.status === 404) return err("not-found");
    if (!res.ok) return err("network");
    return ok(await res.json());
  } catch {
    return err("network");
  }
}
```

### Exhaustive Switch

```typescript
function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.size ** 2;
    case "rect":
      return shape.width * shape.height;
    default: {
      const _exhaustive: never = shape; // Error if variant missed
      return _exhaustive;
    }
  }
}
```

## tsconfig.json Essentials

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noImplicitOverride": true,
    "isolatedModules": true
  }
}
```

## References

- [PATTERNS.md](PATTERNS.md) - Code patterns and style
- [REACT.md](REACT.md) - React component patterns
- [TESTING.md](TESTING.md) - Testing with vitest

## Commands

```bash
bun install              # Install deps
bun run build            # Build
bun test                 # Test
bun run lint             # Lint
bun run format           # Format
```
