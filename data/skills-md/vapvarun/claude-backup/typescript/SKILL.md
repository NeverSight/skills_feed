---
name: typescript
description: TypeScript development best practices including type system, generics, utility types, configuration, and patterns for React, Node.js, and full-stack applications. Use when writing TypeScript code, converting JavaScript to TypeScript, debugging type errors, or implementing type-safe patterns.
---

# TypeScript Development

Modern TypeScript patterns and type-safe development.

## Type Fundamentals

### Basic Types

```typescript
// Primitives
const name: string = 'John';
const age: number = 30;
const isActive: boolean = true;
const nothing: null = null;
const notDefined: undefined = undefined;

// Arrays
const numbers: number[] = [1, 2, 3];
const strings: Array<string> = ['a', 'b', 'c'];
const mixed: (string | number)[] = [1, 'two', 3];

// Tuples
const tuple: [string, number] = ['hello', 42];
const namedTuple: [name: string, age: number] = ['John', 30];

// Objects
const user: { name: string; age: number } = { name: 'John', age: 30 };

// Any vs Unknown
const dangerous: any = getData();     // Avoid - no type checking
const safe: unknown = getData();       // Prefer - requires type narrowing
if (typeof safe === 'string') {
    console.log(safe.toUpperCase());   // Now TypeScript knows it's string
}
```

### Interfaces vs Types

```typescript
// Interface - extendable, for objects
interface User {
    id: number;
    name: string;
    email: string;
}

interface AdminUser extends User {
    role: 'admin';
    permissions: string[];
}

// Type - more flexible
type ID = string | number;
type Callback = (data: string) => void;
type Status = 'pending' | 'active' | 'inactive';

// Intersection types
type UserWithTimestamps = User & {
    createdAt: Date;
    updatedAt: Date;
};

// Use interface for objects, type for unions/primitives
```

### Optional & Readonly

```typescript
interface Config {
    required: string;
    optional?: string;              // May be undefined
    readonly immutable: string;     // Can't be reassigned
}

// Readonly utility
type ReadonlyUser = Readonly<User>;

// Partial - all optional
type PartialUser = Partial<User>;

// Required - all required
type RequiredUser = Required<User>;
```

## Generics

### Basic Generics

```typescript
// Generic function
function identity<T>(value: T): T {
    return value;
}

const num = identity(42);        // T inferred as number
const str = identity('hello');   // T inferred as string

// Generic interface
interface Response<T> {
    data: T;
    status: number;
    message: string;
}

const userResponse: Response<User> = {
    data: { id: 1, name: 'John', email: 'john@example.com' },
    status: 200,
    message: 'Success',
};

// Generic class
class Queue<T> {
    private items: T[] = [];

    enqueue(item: T): void {
        this.items.push(item);
    }

    dequeue(): T | undefined {
        return this.items.shift();
    }
}

const numberQueue = new Queue<number>();
numberQueue.enqueue(1);
```

### Constraints

```typescript
// Constrain to specific shape
interface HasId {
    id: number;
}

function findById<T extends HasId>(items: T[], id: number): T | undefined {
    return items.find(item => item.id === id);
}

// Multiple constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
    return { ...a, ...b };
}

// keyof constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const user = { name: 'John', age: 30 };
const name = getProperty(user, 'name');  // string
const age = getProperty(user, 'age');    // number
```

### Utility Types

```typescript
// Pick - select specific properties
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - exclude properties
type UserWithoutEmail = Omit<User, 'email'>;

// Record - map keys to values
type UserRoles = Record<string, 'admin' | 'user' | 'guest'>;

// Extract / Exclude
type Status = 'pending' | 'active' | 'deleted';
type ActiveStatus = Extract<Status, 'pending' | 'active'>;  // 'pending' | 'active'
type WithoutDeleted = Exclude<Status, 'deleted'>;           // 'pending' | 'active'

// ReturnType / Parameters
function createUser(name: string, email: string): User {
    return { id: 1, name, email };
}

type CreateUserReturn = ReturnType<typeof createUser>;      // User
type CreateUserParams = Parameters<typeof createUser>;       // [string, string]

// NonNullable
type MaybeString = string | null | undefined;
type DefinitelyString = NonNullable<MaybeString>;           // string
```

## Type Guards

```typescript
// typeof guard
function process(value: string | number) {
    if (typeof value === 'string') {
        return value.toUpperCase();
    }
    return value * 2;
}

// instanceof guard
class Dog {
    bark() { console.log('Woof!'); }
}

class Cat {
    meow() { console.log('Meow!'); }
}

function speak(animal: Dog | Cat) {
    if (animal instanceof Dog) {
        animal.bark();
    } else {
        animal.meow();
    }
}

// in guard
interface Bird { fly(): void; }
interface Fish { swim(): void; }

function move(animal: Bird | Fish) {
    if ('fly' in animal) {
        animal.fly();
    } else {
        animal.swim();
    }
}

// Custom type guard
interface ApiError {
    code: string;
    message: string;
}

function isApiError(error: unknown): error is ApiError {
    return (
        typeof error === 'object' &&
        error !== null &&
        'code' in error &&
        'message' in error
    );
}

// Usage
try {
    await fetchData();
} catch (error) {
    if (isApiError(error)) {
        console.log(error.code);  // TypeScript knows it's ApiError
    }
}
```

## Advanced Patterns

### Discriminated Unions

```typescript
interface LoadingState {
    status: 'loading';
}

interface SuccessState<T> {
    status: 'success';
    data: T;
}

interface ErrorState {
    status: 'error';
    error: string;
}

type AsyncState<T> = LoadingState | SuccessState<T> | ErrorState;

function handleState<T>(state: AsyncState<T>) {
    switch (state.status) {
        case 'loading':
            return 'Loading...';
        case 'success':
            return state.data;  // TypeScript knows data exists
        case 'error':
            return state.error; // TypeScript knows error exists
    }
}
```

### Template Literal Types

```typescript
type EventName = 'click' | 'focus' | 'blur';
type EventHandler = `on${Capitalize<EventName>}`;  // 'onClick' | 'onFocus' | 'onBlur'

type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Endpoint = `/api/${string}`;

function request(method: HTTPMethod, url: Endpoint) {
    // ...
}

request('GET', '/api/users');    // OK
request('GET', '/users');        // Error: doesn't start with /api/
```

### Mapped Types

```typescript
// Make all properties optional
type Optional<T> = {
    [K in keyof T]?: T[K];
};

// Make all properties nullable
type Nullable<T> = {
    [K in keyof T]: T[K] | null;
};

// Prefix keys
type Prefixed<T, P extends string> = {
    [K in keyof T as `${P}${string & K}`]: T[K];
};

type PrefixedUser = Prefixed<User, 'user_'>;
// { user_id: number; user_name: string; user_email: string }
```

### Conditional Types

```typescript
// Basic conditional
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;  // true
type B = IsString<number>;  // false

// Extract array element type
type ElementOf<T> = T extends (infer E)[] ? E : never;

type StringElement = ElementOf<string[]>;  // string

// Function return type
type AsyncReturnType<T> = T extends (...args: any[]) => Promise<infer R> ? R : never;

async function fetchUser(): Promise<User> {
    return { id: 1, name: 'John', email: 'john@example.com' };
}

type FetchedUser = AsyncReturnType<typeof fetchUser>;  // User
```

## React TypeScript

### Component Types

```tsx
import { FC, ReactNode, ComponentProps } from 'react';

// Props interface
interface ButtonProps {
    variant: 'primary' | 'secondary';
    size?: 'sm' | 'md' | 'lg';
    children: ReactNode;
    onClick?: () => void;
}

// Function component
function Button({ variant, size = 'md', children, onClick }: ButtonProps) {
    return (
        <button className={`btn-${variant} btn-${size}`} onClick={onClick}>
            {children}
        </button>
    );
}

// With FC (includes children)
const Card: FC<{ title: string; children: ReactNode }> = ({ title, children }) => (
    <div className="card">
        <h2>{title}</h2>
        {children}
    </div>
);

// Extending HTML element props
interface InputProps extends ComponentProps<'input'> {
    label: string;
    error?: string;
}

function Input({ label, error, ...props }: InputProps) {
    return (
        <div>
            <label>{label}</label>
            <input {...props} />
            {error && <span className="error">{error}</span>}
        </div>
    );
}
```

### Hooks

```tsx
import { useState, useEffect, useRef, useCallback, useMemo } from 'react';

// useState with type
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<string[]>([]);

// useRef
const inputRef = useRef<HTMLInputElement>(null);
const countRef = useRef<number>(0);

// useCallback with types
const handleClick = useCallback((id: number) => {
    console.log(id);
}, []);

// useMemo
const expensiveValue = useMemo(() => {
    return items.filter(item => item.length > 5);
}, [items]);

// Custom hook
function useLocalStorage<T>(key: string, initialValue: T) {
    const [value, setValue] = useState<T>(() => {
        const stored = localStorage.getItem(key);
        return stored ? JSON.parse(stored) : initialValue;
    });

    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value));
    }, [key, value]);

    return [value, setValue] as const;
}
```

## Configuration

### tsconfig.json

```json
{
    "compilerOptions": {
        "target": "ES2022",
        "module": "ESNext",
        "moduleResolution": "bundler",
        "lib": ["ES2022", "DOM", "DOM.Iterable"],

        "strict": true,
        "noUncheckedIndexedAccess": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true,

        "declaration": true,
        "declarationMap": true,
        "sourceMap": true,

        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true,

        "baseUrl": ".",
        "paths": {
            "@/*": ["src/*"],
            "@components/*": ["src/components/*"]
        },

        "outDir": "dist",
        "rootDir": "src"
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "dist"]
}
```

### Strict Mode Benefits

```typescript
// strictNullChecks - catches null/undefined errors
const user: User | null = getUser();
user.name;              // Error: user might be null
user?.name;             // OK: optional chaining

// noImplicitAny - requires explicit types
function process(data) { }  // Error: implicit 'any'
function process(data: unknown) { }  // OK

// strictPropertyInitialization - ensures class properties are initialized
class User {
    name: string;       // Error: not initialized
    name: string = '';  // OK
}
```
