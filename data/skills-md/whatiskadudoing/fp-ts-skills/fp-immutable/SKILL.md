---
name: fp-immutable
description: Practical immutability patterns in TypeScript - spread operators, nested updates, readonly types, and when mutation is actually fine
version: 1.0.0
tags:
  - typescript
  - immutability
  - functional-programming
  - patterns
---

# Practical Immutability in TypeScript

## Why Immutability Helps

```typescript
// Bug: shared state causes unexpected behavior
const filters = { active: true, category: 'all' };
const savedFilters = filters; // Not a copy!
filters.active = false;
console.log(savedFilters.active); // false - oops!

// Fix: immutable update creates a new object
const filters2 = { active: true, category: 'all' };
const savedFilters2 = { ...filters2 }; // Actual copy
filters2.active = false;
console.log(savedFilters2.active); // true - safe!
```

Benefits in practice:
- **Debugging**: Previous state preserved, easy to compare
- **Undo/redo**: Just keep old versions
- **React/Redux**: Change detection with `===`
- **No side effects**: Functions don't break other code

## Spread Patterns

### Arrays

```typescript
const items = [1, 2, 3];

// Add to end
const added = [...items, 4]; // [1, 2, 3, 4]

// Add to start
const prepended = [0, ...items]; // [0, 1, 2, 3]

// Insert at index
const inserted = [...items.slice(0, 1), 99, ...items.slice(1)]; // [1, 99, 2, 3]

// Remove by index
const removed = [...items.slice(0, 1), ...items.slice(2)]; // [1, 3]

// Remove by value
const filtered = items.filter(x => x !== 2); // [1, 3]

// Update by index
const updated = items.map((x, i) => i === 1 ? 99 : x); // [1, 99, 3]

// Replace matching items
const replaced = items.map(x => x === 2 ? 99 : x); // [1, 99, 3]
```

### Objects

```typescript
const user = { name: 'Alice', age: 30, role: 'admin' };

// Update property
const older = { ...user, age: 31 };

// Add property
const withEmail = { ...user, email: 'alice@example.com' };

// Remove property (destructure + spread)
const { role, ...withoutRole } = user; // { name: 'Alice', age: 30 }

// Merge objects (later wins)
const defaults = { theme: 'light', lang: 'en' };
const prefs = { theme: 'dark' };
const merged = { ...defaults, ...prefs }; // { theme: 'dark', lang: 'en' }

// Conditional update
const maybeUpdate = { ...user, ...(shouldUpdate && { age: 31 }) };
```

## Updating Nested Data

The annoying part - every level needs spreading.

```typescript
interface State {
  user: {
    profile: {
      name: string;
      settings: {
        theme: string;
        notifications: boolean;
      };
    };
  };
}

const state: State = {
  user: {
    profile: {
      name: 'Alice',
      settings: {
        theme: 'light',
        notifications: true,
      },
    },
  },
};

// Update deeply nested value
const updated: State = {
  ...state,
  user: {
    ...state.user,
    profile: {
      ...state.user.profile,
      settings: {
        ...state.user.profile.settings,
        theme: 'dark',
      },
    },
  },
};
```

### Helper Function for Nested Updates

```typescript
// Simple lens-like helper
const updateIn = <T>(
  obj: T,
  path: string[],
  updater: (val: any) => any
): T => {
  if (path.length === 0) return updater(obj) as T;
  const [key, ...rest] = path;
  return {
    ...obj,
    [key]: updateIn((obj as any)[key], rest, updater),
  } as T;
};

// Usage
const updated2 = updateIn(state, ['user', 'profile', 'settings', 'theme'], () => 'dark');
```

## Common Tasks

### Toggle Boolean in a List Item

```typescript
interface Todo {
  id: number;
  text: string;
  done: boolean;
}

const todos: Todo[] = [
  { id: 1, text: 'Learn FP', done: false },
  { id: 2, text: 'Use immutability', done: false },
];

// Toggle by ID
const toggleTodo = (todos: Todo[], id: number): Todo[] =>
  todos.map(todo =>
    todo.id === id ? { ...todo, done: !todo.done } : todo
  );

const toggled = toggleTodo(todos, 1);
// [{ id: 1, text: 'Learn FP', done: true }, ...]
```

### Update Item in Array by ID

```typescript
interface User {
  id: number;
  name: string;
  score: number;
}

const users: User[] = [
  { id: 1, name: 'Alice', score: 100 },
  { id: 2, name: 'Bob', score: 85 },
];

// Update specific user
const updateUser = (
  users: User[],
  id: number,
  updates: Partial<User>
): User[] =>
  users.map(user =>
    user.id === id ? { ...user, ...updates } : user
  );

const updated3 = updateUser(users, 1, { score: 110 });
```

### Merge with Defaults

```typescript
interface Config {
  timeout: number;
  retries: number;
  baseUrl: string;
}

const defaults: Config = {
  timeout: 5000,
  retries: 3,
  baseUrl: 'https://api.example.com',
};

const createConfig = (overrides: Partial<Config>): Config => ({
  ...defaults,
  ...overrides,
});

const config = createConfig({ timeout: 10000 });
// { timeout: 10000, retries: 3, baseUrl: 'https://api.example.com' }
```

### Clone with Modifications

```typescript
interface Order {
  id: string;
  items: string[];
  status: 'pending' | 'shipped' | 'delivered';
  metadata: Record<string, string>;
}

const cloneOrder = (order: Order, modifications: Partial<Order>): Order => ({
  ...order,
  ...modifications,
  // Deep clone arrays and objects if needed
  items: modifications.items ?? [...order.items],
  metadata: { ...order.metadata, ...modifications.metadata },
});
```

## The Truth About const

```typescript
// const prevents REASSIGNMENT, not MUTATION
const arr = [1, 2, 3];
arr.push(4);        // Works! arr is now [1, 2, 3, 4]
arr[0] = 99;        // Works! arr is now [99, 2, 3, 4]
// arr = [5, 6, 7]; // Error: Cannot assign to 'arr'

const obj = { name: 'Alice' };
obj.name = 'Bob';   // Works! obj is now { name: 'Bob' }
// obj = {};        // Error: Cannot assign to 'obj'

// Use readonly types for compile-time immutability
const readonlyArr: readonly number[] = [1, 2, 3];
// readonlyArr.push(4);  // Error: Property 'push' does not exist
// readonlyArr[0] = 99;  // Error: Index signature only permits reading

const readonlyObj: Readonly<{ name: string }> = { name: 'Alice' };
// readonlyObj.name = 'Bob'; // Error: Cannot assign to 'name'

// Object.freeze() for runtime immutability (shallow!)
const frozen = Object.freeze({ name: 'Alice', nested: { value: 1 } });
// frozen.name = 'Bob';        // Silently fails (or throws in strict mode)
frozen.nested.value = 2;       // Works! freeze is shallow
```

### readonly Types in TypeScript

```typescript
// Readonly array
type ImmutableList<T> = readonly T[];

// Readonly object
type ImmutableUser = Readonly<{
  name: string;
  age: number;
}>;

// Deep readonly (recursive)
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// Usage
interface State {
  users: Array<{ name: string; active: boolean }>;
  settings: { theme: string };
}

type ImmutableState = DeepReadonly<State>;
// All nested properties are now readonly
```

## When Mutation Is OK

### Inside Functions with Local Variables

```typescript
// Mutation inside function is fine - no external state affected
const sumSquares = (nums: number[]): number => {
  let total = 0;  // Local mutable variable
  for (const n of nums) {
    total += n * n;  // Mutation is fine here
  }
  return total;
};

// Building up a result locally
const groupBy = <T, K extends string>(
  items: T[],
  keyFn: (item: T) => K
): Record<K, T[]> => {
  const result: Record<string, T[]> = {};  // Local mutation
  for (const item of items) {
    const key = keyFn(item);
    if (!result[key]) result[key] = [];
    result[key].push(item);  // Mutating local object
  }
  return result;
};
```

### Performance-Critical Code

```typescript
// When processing large arrays, mutation can be significantly faster
const processLargeArray = (items: number[]): number[] => {
  // Creating new arrays in a hot loop = GC pressure
  // Mutation here is a valid optimization
  const result = new Array(items.length);
  for (let i = 0; i < items.length; i++) {
    result[i] = items[i] * 2;
  }
  return result;
};

// But profile first! Often the difference doesn't matter
// and immutable code is easier to reason about
```

### When Immutability Adds No Value

```typescript
// Single-use object being built up
const buildConfig = () => {
  const config: Record<string, unknown> = {};
  config.env = process.env.NODE_ENV;
  config.debug = process.env.DEBUG === 'true';
  config.port = parseInt(process.env.PORT || '3000');
  return Object.freeze(config); // Freeze before returning
};

// Local array being populated
const fetchAllPages = async <T>(fetchPage: (n: number) => Promise<T[]>): Promise<T[]> => {
  const allItems: T[] = [];
  let page = 1;
  while (true) {
    const items = await fetchPage(page);
    if (items.length === 0) break;
    allItems.push(...items); // Local mutation is fine
    page++;
  }
  return allItems;
};
```

## Immer for Complex Updates

When spread nesting gets painful, use Immer.

```typescript
import { produce } from 'immer';

interface State {
  users: Array<{
    id: number;
    name: string;
    posts: Array<{
      id: number;
      title: string;
      likes: number;
    }>;
  }>;
}

const state: State = {
  users: [
    {
      id: 1,
      name: 'Alice',
      posts: [
        { id: 1, title: 'Hello', likes: 5 },
        { id: 2, title: 'World', likes: 3 },
      ],
    },
  ],
};

// Without Immer - nested spread nightmare
const withoutImmer: State = {
  ...state,
  users: state.users.map(user =>
    user.id === 1
      ? {
          ...user,
          posts: user.posts.map(post =>
            post.id === 1 ? { ...post, likes: post.likes + 1 } : post
          ),
        }
      : user
  ),
};

// With Immer - write mutations, get immutability
const withImmer = produce(state, draft => {
  const user = draft.users.find(u => u.id === 1);
  if (user) {
    const post = user.posts.find(p => p.id === 1);
    if (post) {
      post.likes += 1; // Looks like mutation, but it's safe!
    }
  }
});

// Both produce the same immutable result
```

### Immer with React useState

```typescript
import { useImmer } from 'use-immer';

interface FormState {
  user: { name: string; email: string };
  preferences: { theme: string; notifications: boolean };
}

const MyComponent = () => {
  const [state, updateState] = useImmer<FormState>({
    user: { name: '', email: '' },
    preferences: { theme: 'light', notifications: true },
  });

  const updateName = (name: string) => {
    updateState(draft => {
      draft.user.name = name;
    });
  };

  const toggleNotifications = () => {
    updateState(draft => {
      draft.preferences.notifications = !draft.preferences.notifications;
    });
  };
};
```

## Quick Reference

| Task | Immutable Pattern |
|------|-------------------|
| Add to array end | `[...arr, item]` |
| Add to array start | `[item, ...arr]` |
| Remove from array | `arr.filter(x => x !== item)` |
| Update array item | `arr.map(x => x.id === id ? {...x, ...updates} : x)` |
| Update object prop | `{...obj, prop: newValue}` |
| Remove object prop | `const {prop, ...rest} = obj` |
| Merge objects | `{...defaults, ...overrides}` |
| Deep update | Use Immer or nested spread |
| Prevent mutation | `readonly` types or `Object.freeze()` |
