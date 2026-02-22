---
name: javascript
description: "Modern JavaScript (ES2020+) patterns. Trigger: When writing JavaScript code, using ES2020+ features, or refactoring legacy JS."
license: "Apache 2.0"
metadata:
  version: "1.0"
  type: language
---

# JavaScript Skill

Modern JS/TS patterns for ES2020+ with async code, safe property access, modern syntax.

## When to Use

Use when:

- Writing JavaScript with ES2020+ features
- Refactoring legacy JS to modern syntax
- Implementing async operations (promises, async/await)
- Using destructuring, optional chaining, nullish coalescing

Don't use for TypeScript (typescript skill), React (react skill), or Node.js backend.

## Critical Patterns

### ✅ REQUIRED: ES Module Imports

```javascript
// CORRECT: Named imports (explicit, tree-shakeable)
import { readFileSync, existsSync } from "fs";
import { join, resolve } from "path";

// CORRECT: Default import for modules with single export
import express from "express";

// WRONG: require() in ES modules
const fs = require("fs");

// WRONG: Dynamic import when static works
async function doWork() {
  const fs = await import("fs"); // unnecessary
}
```

### ✅ REQUIRED: No Dead Code

```javascript
// WRONG: Unused variables and imports
import { something } from "./lib"; // never used
const unused = 42;
function neverCalled() {}

// CORRECT: Every import, variable, and function is used
import { needed } from "./lib";
const count = needed();
```

### ✅ REQUIRED: const/let, Never var

```javascript
// CORRECT
const API_URL = "https://api.example.com";
let count = 0;

// WRONG: var (function-scoped, hoisting issues)
var count = 0;
```

### ✅ REQUIRED: async/await for Async Operations

```javascript
// CORRECT
async function fetchData() {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    console.error(error);
  }
}

// WRONG: promise chains
function fetchData() {
  return fetch(url)
    .then((res) => res.json())
    .catch((error) => console.error(error));
}
```

### ✅ REQUIRED: Optional Chaining and Nullish Coalescing

```javascript
// CORRECT: safe access + nullish coalescing
const name = user?.profile?.name ?? "Anonymous";
const result = obj?.method?.();
const port = config.port ?? 3000; // 0 won't fallback

// WRONG: || treats 0, '', false as falsy
const port = config.port || 3000; // 0 fallbacks to 3000!

// WRONG: verbose manual checks
const name = (user && user.profile && user.profile.name) || "Anonymous";
```

### ✅ REQUIRED: Explicit Boolean Coercion

```javascript
// CORRECT
const hasData = !!data;
const isValid = Boolean(value);

// WRONG: implicit coercion hides intent
if (data) { /* unclear: existence or truthiness? */ }
```

### ✅ REQUIRED: Promise.all for Parallel Operations

```javascript
// CORRECT: parallel
const [users, posts, comments] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
  fetchComments(),
]);

// WRONG: sequential (3x slower)
const users = await fetchUsers();
const posts = await fetchPosts();
const comments = await fetchComments();
```

## Decision Tree

**Importing a module?** -> Named imports: `import { x } from 'mod'`. Never `require()` in ES modules.

**Unused import/variable?** -> Delete it. No dead code.

**Async operation?** -> `async/await` with try/catch.

**String concatenation?** -> Template literals: `` `Hello ${name}` ``.

**Default value?** -> `??` for null/undefined; `||` for any falsy.

**Property might not exist?** -> Optional chaining: `obj?.prop?.nested`.

**Iterate array?** -> `.map()`, `.filter()`, `.reduce()`. Use `for...of` for early breaks.

**Copy object/array?** -> Spread: `{...obj}`, `[...arr]`.

**Callback?** -> Arrow function unless `this` context is needed.

**Multiple independent awaits?** -> `Promise.all()` for parallel execution.

## Example

```javascript
const fetchData = async (url) => {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data?.results ?? [];
  } catch (error) {
    console.error("Fetch failed:", error);
    return [];
  }
};

const { name, age = 18 } = user;
const greeting = `Hello, ${name}!`;
```

## Edge Cases

- **Parallel async:** `Promise.all()` for concurrent execution
- **Array holes:** `.filter(Boolean)` to clean sparse arrays
- **Number precision:** Use decimal.js for financial calculations
- **Equality:** Always `===` (never `==`)
- **this binding:** Arrow functions don't bind `this`

## Checklist

- [ ] ES module imports (`import`/`export`), no `require()`
- [ ] Named imports over namespace imports
- [ ] No unused imports, variables, or functions
- [ ] `const`/`let` only (no `var`)
- [ ] `async/await` with try/catch for async code
- [ ] `?.` and `??` for safe access and defaults
- [ ] `Promise.all()` for independent parallel fetches
- [ ] `===` for all equality checks
- [ ] Template literals for string interpolation
- [ ] Destructuring for objects and arrays
- [ ] Arrow functions for callbacks
- [ ] Modern array methods (`.map`, `.filter`, `.reduce`)

## Resources

- https://developer.mozilla.org/en-US/docs/Web/JavaScript
- https://tc39.es/ecma262/
