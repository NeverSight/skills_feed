---
name: modern-javascript-patterns
description: "Master ES6+ features including async/await, destructuring, spread operators, arrow functions, promises, modules, iterators, generators, and functional programming patterns for writing clean, efficient JavaScript code. Use when refactoring legacy code, implementing modern patterns, or optimizing JavaScript applications."
layer: 1
tech_stack: [javascript, typescript]
topics: [es6, async-await, destructuring, spread, arrow-functions, modules, functional]
depends_on: []
complements: [typescript-advanced-types]
keywords: [async, await, Promise, const, let, arrow, spread, destructure, import, export]
---

# Modern JavaScript Patterns

Master ES6+ features and functional programming for clean, efficient code.

## Arrow Functions

```javascript
// Basic syntax
const add = (a, b) => a + b;
const double = x => x * 2;
const getRandom = () => Math.random();

// Multi-line (need braces)
const processUser = user => {
  const normalized = user.name.toLowerCase();
  return { ...user, name: normalized };
};

// Returning objects (wrap in parentheses)
const createUser = (name, age) => ({ name, age });

// Lexical 'this' binding
class Counter {
  increment = () => { this.count++; };  // 'this' preserved
}
```

## Destructuring

```javascript
// Object destructuring
const { name, email } = user;
const { name: userName } = user;           // Rename
const { age = 25 } = user;                 // Default value
const { address: { city } } = user;        // Nested
const { id, ...userData } = user;          // Rest

// Array destructuring
const [first, second] = numbers;
const [, , third] = numbers;               // Skip elements
const [head, ...tail] = numbers;           // Rest
let [a, b] = [1, 2]; [a, b] = [b, a];     // Swap

// Function parameters
function greet({ name, age = 18 }) {
  console.log(`Hello ${name}`);
}
```

## Spread & Rest

```javascript
// Spread arrays
const combined = [...arr1, ...arr2];
const copy = [...arr1];

// Spread objects
const settings = { ...defaults, ...userPrefs };
const newObj = { ...user, age: 31 };

// Rest parameters
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}
```

## Async/Await

```javascript
// Basic usage
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Parallel execution
const [user1, user2] = await Promise.all([
  fetchUser(1),
  fetchUser(2)
]);

// Promise combinators
Promise.all(promises);        // Wait for all
Promise.allSettled(promises); // All results, regardless of outcome
Promise.race(promises);       // First to complete
Promise.any(promises);        // First to succeed
```

## Functional Patterns

### Array Methods

```javascript
const users = [{ id: 1, name: 'John', active: true }, ...];

// Map - Transform
const names = users.map(u => u.name);

// Filter - Select
const activeUsers = users.filter(u => u.active);

// Reduce - Aggregate
const totalAge = users.reduce((sum, u) => sum + u.age, 0);

// Chaining
const result = users
  .filter(u => u.active)
  .map(u => u.name)
  .sort()
  .join(', ');

// Other useful methods
users.find(u => u.id === 2);           // First match
users.findIndex(u => u.name === 'Jane'); // Index of first match
users.some(u => u.active);              // At least one matches
users.every(u => u.age >= 18);          // All match
userTags.flatMap(u => u.tags);          // Map and flatten
```

### Higher-Order Functions

```javascript
// Currying
const multiply = a => b => a * b;
const double = multiply(2);

// Memoization
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (!cache.has(key)) cache.set(key, fn(...args));
    return cache.get(key);
  };
}

// Composition
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);
```

### Immutability

```javascript
// Arrays
const withNew = [...arr, newItem];           // Add
const without = arr.filter(x => x !== item); // Remove
const updated = arr.map(x => x.id === id ? { ...x, name } : x);

// Objects
const updated = { ...user, age: 31 };        // Update
const { password, ...safe } = user;          // Remove key
```

## Modern Operators

```javascript
// Optional chaining
const city = user?.address?.city;
const result = obj.method?.();
const first = arr?.[0];

// Nullish coalescing
const value = null ?? 'default';    // 'default'
const value = 0 ?? 'default';       // 0 (not 'default')

// Logical assignment
a ??= 'default';  // a = a ?? 'default'
a ||= 'default';  // a = a || 'default'
a &&= value;      // a = a && value
```

## Modules

```javascript
// Named exports
export const PI = 3.14159;
export function add(a, b) { return a + b; }

// Default export
export default function multiply(a, b) { return a * b; }

// Importing
import multiply, { PI, add } from './math.js';
import * as Math from './math.js';

// Dynamic import
const module = await import('./feature.js');
```

## Performance Patterns

```javascript
// Debounce
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Throttle
function throttle(fn, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
```

## Best Practices

1. **Use const by default** - Only let when reassignment needed
2. **Prefer arrow functions** - Especially for callbacks
3. **Use template literals** - Instead of concatenation
4. **Destructure** - For cleaner code
5. **Use async/await** - Instead of Promise chains
6. **Avoid mutation** - Use spread operator
7. **Use optional chaining** - Prevent undefined errors
8. **Use nullish coalescing** - For defaults
9. **Prefer array methods** - Over loops
10. **Write pure functions** - Easier to test

## Detailed References

For comprehensive patterns, see:
- [references/generators-iterators.md](references/generators-iterators.md)
- [references/class-features.md](references/class-features.md)

## Resources

- **MDN Web Docs**: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **JavaScript.info**: https://javascript.info/
