---
name: typescript
description: Configures TypeScript projects, defines types and interfaces, writes generics, and implements type guards. Use when setting up tsconfig.json, creating type definitions, or ensuring type safety in JS/TS codebases.
---

# TypeScript

Type-safe JavaScript with static typing and modern features.

## Quick Start

```bash
bun init --typescript    # Initialize project
bunx tsc --noEmit        # Type check
vitest run               # Run tests
```

## Configuration

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "lib": ["ESNext"],
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
```

### Strict Mode Options

| Option                | Description                     |
| --------------------- | ------------------------------- |
| `strictNullChecks`    | Enforce strict null checks      |
| `strictFunctionTypes` | Strict function parameter types |
| `noImplicitAny`       | Disallow implicit any types     |
| `alwaysStrict`        | Apply all strict checks         |

## Type Definitions

### Basic Types

```typescript
let str: string = "hello";
let num: number = 42;
let bool: boolean = true;
let arr: number[] = [1, 2, 3];
let tuple: [string, number] = ["age", 25];
let obj: { name: string; age: number } = { name: "John", age: 30 };
```

### Interfaces vs Types

```typescript
// Interface for object shapes
interface User {
  id: number;
  name: string;
  email: string;
}

// Type for unions and function signatures
type Status = "loading" | "success" | "error";
type CreateUser = (data: Partial<User>) => Promise<User>;

// Discriminated union
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };
```

### Utility Types

```typescript
type PartialUser = Partial<User>;
type RequiredUser = Required<User>;
type ReadonlyUser = Readonly<User>;
type UserName = Pick<User, "name">;
type UserWithoutEmail = Omit<User, "email">;
```

## Functions

```typescript
// Basic function
function add(a: number, b: number): number {
  return a + b;
}

// Arrow function
const add = (a: number, b: number): number => a + b;

// Optional parameters
function greet(name: string, title?: string): string {
  return title ? `${title} ${name}` : name;
}

// Rest parameters
function sum(...nums: number[]): number {
  return nums.reduce((a, b) => a + b, 0);
}

// Function overloads
function format(input: string): string;
function format(input: number): string;
function format(input: string | number): string {
  return String(input);
}

// Async function
async function fetchData(url: string): Promise<unknown> {
  const response = await fetch(url);
  return response.json();
}
```

## Classes

```typescript
class Person {
  constructor(
    public name: string,
    private age: number,
  ) {}

  greet(): string {
    return `Hello, ${this.name}`;
  }
}

// Inheritance
class Employee extends Person {
  constructor(
    name: string,
    age: number,
    public role: string,
  ) {
    super(name, age);
  }
}

// Abstract class
abstract class Shape {
  abstract area(): number;
}
```

## Generics

```typescript
// Generic function
function wrap<T>(value: T): { value: T } {
  return { value };
}

// Generic class
class Container<T> {
  constructor(private value: T) {}
  get(): T {
    return this.value;
  }
}

// Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

## Type Guards

```typescript
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}

function process(value: unknown) {
  if (isString(value)) {
    console.log(value.toUpperCase()); // value is string
  }
}
```

## Error Handling

### Custom Errors

```typescript
class ValidationError extends Error {
  constructor(
    public field: string,
    message: string,
  ) {
    super(message);
    this.name = "ValidationError";
  }
}
```

### Result Type

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

function safeParse(json: string): Result<unknown> {
  try {
    return { ok: true, value: JSON.parse(json) };
  } catch (error) {
    return { ok: false, error: error as Error };
  }
}
```

## Compilation

```bash
tsc                    # Compile
tsc --noEmit           # Type check only
tsc --watch            # Watch mode (use tmux)

tmux new -d -s tsc 'tsc --watch'
```

## Best Practices

- Use `strict: true` in tsconfig
- Avoid `any` - use `unknown` or specific types
- Prefer interfaces for object shapes
- Use branded types for primitives needing validation
- Make invalid states unrepresentable
- Type at boundaries (API inputs/outputs)

## Tips

- `tsc --noEmit` for fast type checking
- Gradual adoption with `allowJs: true`
- Path mapping: `"@/*": ["src/*"]`
- Declaration files: `"declaration": true`
- Use `// @ts-expect-error` with error messages
