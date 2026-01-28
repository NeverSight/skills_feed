---
name: typescript-advanced-types
description: "Master TypeScript's advanced type system including generics, conditional types, mapped types, and React TypeScript patterns. Use when: (1) implementing complex type logic, (2) creating reusable type utilities, (3) typing React components, hooks, and events, (4) ensuring compile-time type safety."
layer: 1
tech_stack: [typescript, react]
topics: [generics, conditional-types, mapped-types, utility-types, react-types]
depends_on: []
complements: [modern-javascript-patterns]
keywords: [Generic, Partial, Pick, Omit, Record, keyof, infer, extends, ReactNode]
---

# TypeScript Advanced Types

Master TypeScript's advanced type system for building robust, type-safe applications.

## Generics

```typescript
// Basic generic function
function identity<T>(value: T): T {
  return value;
}

// Generic with constraint
interface HasLength { length: number; }

function logLength<T extends HasLength>(item: T): T {
  console.log(item.length);
  return item;
}

// Multiple type parameters
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}
```

## Conditional Types

```typescript
// Basic conditional
type IsString<T> = T extends string ? true : false;

// Extract return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

// Nested conditions
type TypeName<T> =
  T extends string ? "string" :
  T extends number ? "number" :
  T extends boolean ? "boolean" :
  "object";
```

## Mapped Types

```typescript
// Make all properties readonly
type Readonly<T> = { readonly [P in keyof T]: T[P] };

// Make all properties optional
type Partial<T> = { [P in keyof T]?: T[P] };

// Key remapping
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
};

// Filter by type
type PickByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K]
};
```

## Template Literal Types

```typescript
type EventName = "click" | "focus" | "blur";
type EventHandler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

// String manipulation
type Upper = Uppercase<"hello">;      // "HELLO"
type Lower = Lowercase<"HELLO">;      // "hello"
type Cap = Capitalize<"john">;        // "John"
```

## Utility Types

```typescript
// Built-in utilities
type PartialUser = Partial<User>;              // All optional
type RequiredUser = Required<PartialUser>;      // All required
type ReadonlyUser = Readonly<User>;             // All readonly
type NameEmail = Pick<User, "name" | "email">;  // Select props
type NoPassword = Omit<User, "password">;       // Remove props

type T1 = Exclude<"a" | "b" | "c", "a">;        // "b" | "c"
type T2 = Extract<"a" | "b" | "c", "a" | "b">;  // "a" | "b"
type T3 = NonNullable<string | null>;           // string
type PageInfo = Record<"home" | "about", { title: string }>;
```

## React TypeScript Patterns

### Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}
```

### Typed Hooks

```typescript
type ApiState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

function useApiState<T>() {
  const [state, setState] = useState<ApiState<T>>({ status: 'idle' });
  return { state, setLoading, setSuccess, setError };
}
```

### Context with Type Safety

```typescript
interface AuthContextValue {
  user: UserDto | null;
  login: (credentials: LoginDto) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
```

### Event Handler Types

```typescript
// Form submit
const handleSubmit: React.FormEventHandler<HTMLFormElement> = (e) => {
  e.preventDefault();
};

// Input change
const handleChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
  console.log(e.target.value);
};

// Button click
const handleClick: React.MouseEventHandler<HTMLButtonElement> = (e) => {
  console.log(e.currentTarget.name);
};
```

### Common Event Types

| Event | Type |
|-------|------|
| Form submit | `React.FormEventHandler<HTMLFormElement>` |
| Input change | `React.ChangeEventHandler<HTMLInputElement>` |
| Button click | `React.MouseEventHandler<HTMLButtonElement>` |
| Key press | `React.KeyboardEventHandler<HTMLInputElement>` |
| Focus | `React.FocusEventHandler<HTMLInputElement>` |

### Ref Types

```typescript
const inputRef = useRef<HTMLInputElement>(null);

// Forward ref
const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, ...props }, ref) => (
    <input ref={ref} {...props} />
  )
);
```

### Children Props

```typescript
interface CardProps {
  children: React.ReactNode;
  title: string;
}

// Render prop
interface DataFetcherProps<T> {
  url: string;
  children: (data: T, loading: boolean) => React.ReactNode;
}
```

## Type Guards

```typescript
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") throw new Error("Not a string");
}
```

## Best Practices

1. **Use `unknown` over `any`** - Enforce type checking
2. **Prefer `interface` for objects** - Better error messages
3. **Use `type` for unions** - More flexible
4. **Leverage inference** - Let TypeScript infer when possible
5. **Create helper types** - Build reusable utilities
6. **Use const assertions** - Preserve literal types
7. **Avoid type assertions** - Use guards instead
8. **Enable strict mode** - All strict options

## Detailed References

For comprehensive patterns, see:
- [references/advanced-patterns.md](references/advanced-patterns.md)
- [references/type-challenges.md](references/type-challenges.md)

## Resources

- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/
- **Type Challenges**: https://github.com/type-challenges/type-challenges
