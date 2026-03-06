---
name: javascript
description: Write modern JavaScript with ES6+, async patterns, and Node.js. Use for JS development, async debugging, or optimization.
---

# JavaScript Development

Write modern, clean JavaScript and TypeScript.

## When to Use

- Writing JavaScript/TypeScript code
- Async debugging and optimization
- Node.js development
- Browser compatibility issues
- Module system questions

## Modern JavaScript Patterns

### Async/Await

```javascript
// Prefer async/await over promise chains
async function fetchData() {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Fetch failed:", error);
    throw error;
  }
}

// Parallel execution
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);

// Error handling for multiple promises
const results = await Promise.allSettled([task1(), task2(), task3()]);
const succeeded = results.filter((r) => r.status === "fulfilled");
```

### Destructuring and Spread

```javascript
// Object destructuring with defaults
const { name, age = 0, ...rest } = user;

// Array methods
const active = users.filter((u) => u.active).map((u) => u.name);

// Object spread for immutable updates
const updated = { ...user, name: "New Name" };
```

### Classes and Modules

```javascript
// ES modules
export class UserService {
  #privateField; // Private field

  constructor(config) {
    this.#privateField = config.secret;
  }

  async getUser(id) {
    return await this.#fetch(`/users/${id}`);
  }
}

// Named and default exports
export { UserService };
export default UserService;
```

## TypeScript Patterns

```typescript
// Interfaces over types for objects
interface User {
  id: string;
  name: string;
  email?: string;
}

// Generics
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// Utility types
type CreateUser = Omit<User, "id">;
type ReadonlyUser = Readonly<User>;
```

## Node.js Patterns

```javascript
// ESM in Node.js
import { readFile } from "fs/promises";
import { fileURLToPath } from "url";

const __dirname = fileURLToPath(new URL(".", import.meta.url));

// Streams for large files
import { createReadStream, createWriteStream } from "fs";
import { pipeline } from "stream/promises";

await pipeline(
  createReadStream("input"),
  transform,
  createWriteStream("output"),
);
```

## Common Gotchas

- `this` binding (use arrow functions or .bind())
- Floating promises (always await or handle)
- == vs === (always use ===)
- Array mutation (map/filter return new arrays, sort mutates)

## Examples

**Input:** "Fix async issue"
**Action:** Check for unhandled promises, race conditions, proper error handling

**Input:** "Convert to TypeScript"
**Action:** Add types, interfaces, fix type errors, configure tsconfig
