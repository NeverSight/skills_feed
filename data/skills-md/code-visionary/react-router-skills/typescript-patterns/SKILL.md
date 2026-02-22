---
name: typescript-patterns
description: TypeScript patterns for React Router v7 - Type-safe loaders, actions, params, generic components, and utility types
tags: [typescript, react-router, type-safety, generics]
version: 1.0.0
author: Code Visionary
---

# TypeScript Patterns

Master TypeScript in React and React Router v7 applications. Learn how to create type-safe loaders, actions, components, and leverage TypeScript's power for better DX.

## Quick Reference

### Type-Safe Loader

```typescript
export async function loader({ params }: LoaderFunctionArgs) {
  const user = await fetchUser(params.userId);
  return { user };
}

// In component
const { user } = useLoaderData<typeof loader>();
```

### Type-Safe Action

```typescript
export async function action({ request }: ActionFunctionArgs) {
  const data = await request.formData();
  return { success: true };
}

// In component
const actionData = useActionData<typeof action>();
```

### Generic Component

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```

## When to Use This Skill

- Setting up TypeScript in React Router project
- Creating type-safe routes
- Building reusable generic components
- Defining API response types
- Improving IDE autocomplete and error detection
- Refactoring JavaScript to TypeScript

## Core TypeScript for React Router

### 1. Loader Types

```typescript
import type { LoaderFunctionArgs } from "react-router";

// Define return type interface
interface LoaderData {
  user: User;
  posts: Post[];
}

export async function loader({ 
  params, 
  request 
}: LoaderFunctionArgs): Promise<LoaderData> {
  const user = await fetchUser(params.userId);
  const posts = await fetchPosts(params.userId);
  
  return { user, posts };
}

// Type-safe component
export default function Profile() {
  const { user, posts } = useLoaderData<typeof loader>();
  //    ^? { user: User; posts: Post[] }
  
  return (
    <div>
      <h1>{user.name}</h1>
      {posts.map(post => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  );
}
```

### 2. Action Types

```typescript
import type { ActionFunctionArgs } from "react-router";

// Define action response types
type ActionSuccess = {
  success: true;
  user: User;
};

type ActionError = {
  success: false;
  errors: Record<string, string[]>;
};

type ActionData = ActionSuccess | ActionError;

export async function action({ 
  request 
}: ActionFunctionArgs): Promise<ActionData> {
  const formData = await request.formData();
  
  // Validation...
  if (hasErrors) {
    return {
      success: false,
      errors: { email: ["Invalid email"] }
    };
  }
  
  const user = await createUser(formData);
  return { success: true, user };
}

// Type-safe component
export default function CreateUser() {
  const actionData = useActionData<typeof action>();
  
  if (actionData?.success === false) {
    // TypeScript knows this is ActionError
    return <div>{actionData.errors.email}</div>;
  }
  
  if (actionData?.success === true) {
    // TypeScript knows this is ActionSuccess
    return <div>Created {actionData.user.name}</div>;
  }
  
  return <Form method="post">{/* ... */}</Form>;
}
```

### 3. Params Typing

```typescript
import type { LoaderFunctionArgs, Params } from "react-router";

// Define expected params
interface RouteParams extends Params {
  userId: string;
  postId: string;
}

export async function loader({ params }: LoaderFunctionArgs) {
  // Type assertion for strict checking
  const { userId, postId } = params as RouteParams;
  
  return { userId, postId };
}

// Alternative: Runtime validation + type safety
import { z } from "zod";

const paramsSchema = z.object({
  userId: z.string(),
  postId: z.string(),
});

export async function loader({ params }: LoaderFunctionArgs) {
  const { userId, postId } = paramsSchema.parse(params);
  //    ^? { userId: string; postId: string }
  
  return { userId, postId };
}
```

### 4. Zod Integration

```typescript
import { z } from "zod";

// Define schema
const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  age: z.number().positive(),
});

// Infer TypeScript type from schema
type CreateUserInput = z.infer<typeof createUserSchema>;
//   ^? { name: string; email: string; age: number }

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  
  const result = createUserSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
    age: Number(formData.get("age")),
  });
  
  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
    };
  }
  
  // result.data is fully typed as CreateUserInput
  const user = await createUser(result.data);
  
  return { user };
}
```

## React Component Patterns

### 1. Props Interface

```typescript
// Define props clearly
interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

export function Button({ 
  children, 
  onClick, 
  variant = "primary",
  disabled = false 
}: ButtonProps) {
  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      className={`btn-${variant}`}
    >
      {children}
    </button>
  );
}
```

### 2. Generic Components

```typescript
// Generic list component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string | number;
}

export function List<T>({ 
  items, 
  renderItem, 
  keyExtractor 
}: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>
          {renderItem(item, index)}
        </li>
      ))}
    </ul>
  );
}

// Usage with type inference
<List
  items={users}  // users: User[]
  renderItem={(user) => <span>{user.name}</span>}
  //          ^? user: User (inferred!)
  keyExtractor={(user) => user.id}
/>
```

### 3. Event Handlers

```typescript
interface FormProps {
  onSubmit: (data: FormData) => void;
}

export function Form({ onSubmit }: FormProps) {
  // Properly typed event handler
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    onSubmit(formData);
  };
  
  // Properly typed input handler
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} />
    </form>
  );
}
```

### 4. Forwarding Refs

```typescript
import { forwardRef } from "react";

interface InputProps {
  label: string;
  error?: string;
}

// Properly typed ref forwarding
export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error }, ref) => {
    return (
      <div>
        <label>{label}</label>
        <input ref={ref} />
        {error && <span>{error}</span>}
      </div>
    );
  }
);

Input.displayName = "Input";
```

### 5. Children Patterns

```typescript
// Accept any valid React children
interface ContainerProps {
  children: React.ReactNode;
}

// Accept only specific component types
interface TabsProps {
  children: React.ReactElement<TabProps> | React.ReactElement<TabProps>[];
}

// Accept render prop
interface DataProviderProps<T> {
  data: T;
  children: (data: T) => React.ReactNode;
}

export function DataProvider<T>({ data, children }: DataProviderProps<T>) {
  return <>{children(data)}</>;
}
```

## Advanced Patterns

### 1. Discriminated Unions

```typescript
// Define mutually exclusive states
type LoadingState = 
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: User }
  | { status: "error"; error: string };

function UserProfile() {
  const [state, setState] = useState<LoadingState>({ 
    status: "idle" 
  });
  
  // TypeScript narrows type based on status
  switch (state.status) {
    case "idle":
      return <div>Click to load</div>;
      
    case "loading":
      return <div>Loading...</div>;
      
    case "success":
      // TypeScript knows state.data exists here
      return <div>{state.data.name}</div>;
      
    case "error":
      // TypeScript knows state.error exists here
      return <div>Error: {state.error}</div>;
  }
}
```

### 2. Type Guards

```typescript
// Custom type guard
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}

// Usage
const data: unknown = await response.json();

if (isUser(data)) {
  // TypeScript knows data is User here
  console.log(data.name);
}
```

### 3. Utility Types

```typescript
// Pick specific properties
type UserPreview = Pick<User, "id" | "name" | "avatar">;

// Omit properties
type UserWithoutPassword = Omit<User, "password">;

// Make all properties optional
type PartialUser = Partial<User>;

// Make all properties required
type RequiredUser = Required<User>;

// Make all properties readonly
type ReadonlyUser = Readonly<User>;

// Extract keys of certain type
type StringKeys<T> = {
  [K in keyof T]: T[K] extends string ? K : never;
}[keyof T];

type UserStringFields = StringKeys<User>;
//   ^? "name" | "email" | "bio"
```

### 4. Mapped Types

```typescript
// Create form state from model
type FormState<T> = {
  [K in keyof T]: {
    value: T[K];
    error?: string;
    touched: boolean;
  };
};

type UserFormState = FormState<User>;
// {
//   name: { value: string; error?: string; touched: boolean }
//   email: { value: string; error?: string; touched: boolean }
//   ...
// }
```

### 5. Conditional Types

```typescript
// Different return type based on input
type LoaderReturn<T extends boolean> = 
  T extends true 
    ? Promise<Response> 
    : Response;

function createLoader<T extends boolean>(
  async: T
): LoaderReturn<T> {
  // Implementation
  return null as any;
}

const syncLoader = createLoader(false);
//    ^? Response

const asyncLoader = createLoader(true);
//    ^? Promise<Response>
```

## API Response Typing

### 1. Domain Model Pattern

```typescript
// API response type (snake_case)
interface UserAPI {
  user_id: string;
  full_name: string;
  email_address: string;
  created_at: string;
}

// Domain model (camelCase)
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

// Transformation functions
export const User = {
  fromAPI(data: UserAPI): User {
    return {
      id: data.user_id,
      name: data.full_name,
      email: data.email_address,
      createdAt: new Date(data.created_at),
    };
  },
  
  toAPI(user: User): UserAPI {
    return {
      user_id: user.id,
      full_name: user.name,
      email_address: user.email,
      created_at: user.createdAt.toISOString(),
    };
  },
};

// Usage in loader
export async function loader() {
  const response = await fetch("/api/users");
  const data: UserAPI = await response.json();
  const user = User.fromAPI(data);
  
  return { user };
}
```

### 2. Generic API Client

```typescript
// Generic fetch function with type safety
async function apiCall<T>(
  url: string, 
  options?: RequestInit
): Promise<T> {
  const response = await fetch(url, options);
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return response.json();
}

// Usage
const user = await apiCall<User>("/api/users/123");
//    ^? User

const posts = await apiCall<Post[]>("/api/posts");
//    ^? Post[]
```

## Common Issues

### Issue 1: Type 'any' Errors

**Symptoms**: TypeScript complains about implicit any
**Cause**: Missing type annotations
**Solution**: Add explicit types

```typescript
// ❌ Implicit any
function processData(data) {
  return data.map(item => item.value);
}

// ✅ Explicit types
function processData(data: DataItem[]): number[] {
  return data.map(item => item.value);
}
```

### Issue 2: Type Assertion Overuse

**Symptoms**: Many `as` casts in code
**Cause**: Fighting TypeScript instead of fixing types
**Solution**: Define proper types

```typescript
// ❌ Too many assertions
const user = data as User;
const name = user.name as string;

// ✅ Proper typing
interface ApiResponse {
  data: User;
}

const response: ApiResponse = await fetch(...);
const user = response.data;
const name = user.name;
```

### Issue 3: Overly Complex Types

**Symptoms**: Unreadable type definitions
**Cause**: Trying to be too clever
**Solution**: Simplify and document

```typescript
// ❌ Too complex
type ComplexType<T, U extends keyof T> = {
  [K in U]: T[K] extends object ? Readonly<T[K]> : T[K]
};

// ✅ Simpler and clearer
type UserFields = Pick<User, "name" | "email">;
```

## Best Practices

- [ ] Enable strict mode in tsconfig.json
- [ ] Use `typeof loader` for type inference
- [ ] Define interfaces for all props
- [ ] Use Zod for runtime validation + type inference
- [ ] Create domain models with fromAPI/toAPI
- [ ] Use discriminated unions for states
- [ ] Avoid `any` - use `unknown` instead
- [ ] Prefer interfaces over type aliases for objects
- [ ] Use generic components for reusability
- [ ] Document complex types with comments

## Anti-Patterns

Things to avoid:

- ❌ Using `any` everywhere
- ❌ Type assertions without validation (`as User`)
- ❌ Disabling TypeScript errors with `@ts-ignore`
- ❌ Not typing function parameters
- ❌ Overly complex generic types
- ❌ Duplicating types instead of reusing
- ❌ Not using discriminated unions for state
- ❌ Mixing runtime and type-only imports

## tsconfig.json Setup

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    
    // Strict type checking
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    
    // React
    "jsx": "react-jsx",
    "jsxImportSource": "react",
    
    // Module resolution
    "resolveJsonModule": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    
    // Output
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

## References

- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Zod Documentation](https://zod.dev/)
- [React Router TypeScript Guide](https://reactrouter.com/start/framework/typescript)
- [type-safety-helper skill](../type-safety-helper/)
- [loader-action-optimizer skill](../loader-action-optimizer/)
