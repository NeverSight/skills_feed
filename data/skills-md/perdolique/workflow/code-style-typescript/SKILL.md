---
name: code-style-typescript
description: TypeScript code style guide and formatting conventions. Use when writing TypeScript code, reviewing TypeScript files, refactoring .ts code, formatting TypeScript, or when working with TypeScript interfaces, classes, functions, or any .ts files. Apply these rules during code generation, code review, and when user mentions TypeScript style, formatting, conventions, semicolons, or code quality.
license: Unlicense
---

# TypeScript Code Style Guide

## When to Apply

- When writing new TypeScript code
- During code review of `.ts` files
- When refactoring existing code
- When generating code snippets, examples, or documentation for TypeScript
- When working with TypeScript-related blocks in Markdown, Vue.js, etc.
- When formatting or cleaning up code

## Rules

### Rule: No semicolons at the end of statements

**No semicolons** at the end of statements.

**Exception**: TypeScript interfaces, types, and similar type definitions **MUST use semicolons** as property separators.

### Examples

**✅ Correct:**

```typescript
// Statements - no semicolons
const result = calculateValue()

function greet(name: string) {
  return `Hello, ${name}`
}

// Interfaces - semicolons required
interface User {
  id: number;
}

type Config = {
  timeout: number;
}

// Classes - no semicolons
class UserService {
  private users: User[]

  constructor() {
    this.users = []
  }

  addUser(user: User) {
    this.users.push(user)
  }
}
```

**❌ Wrong:**

```typescript
// Don't add semicolons to statements
const foo = 'bar';

function greet(name: string) {
  return `Hello, ${name}`;
}

// Don't omit semicolons in interfaces
interface User {
  id: number
}

type Config = {
  apiKey: string
}
```

### Rule: No method calls in conditional statements

**Extract method calls** to separate variables before using them in conditional statements (`if`, `while`, `for`, etc.).

### Examples

**✅ Correct:**

```typescript
const isAdmin = user.isAdmin()

if (isAdmin) {
  console.log('Admin access granted')
}

const hasPermission = checkPermissions(user, 'write')

while (hasPermission) {
  // Do something
}
```

**❌ Wrong:**

```typescript
// Don't call methods directly in conditions
if (user.isAdmin()) {
  console.log('Admin access granted')
}

while (checkPermissions(user, 'write')) {
  // Do something
}
```

### Rule: No function calls as arguments

**Extract function calls** to separate variables before using them as arguments to other functions.

**Exception**: See "Nested function calls as arguments on separate lines" rule for rare cases.

### Examples

**✅ Correct:**

```typescript
const userData = fetchUser()
const result = processData(userData)
const filtered = filterItems(items)
const mapped = mapValues(filtered)
const validation = validateInput(data)

saveToDatabase(validation)
```

**❌ Wrong:**

```typescript
// Don't call functions directly in arguments
const result = processData(fetchUser())
const mapped = mapValues(filterItems(items))

saveToDatabase(validateInput(data))
```

### Rule: Group one-line declarations together, separate multiline declarations

**One-line declarations** should stay together without blank lines. **Multiline declarations** should be separated by blank lines.

### Examples

**✅ Correct:**

```typescript
const age = 30
const city = 'New York'
const name = 'John'

const complexObject = {
  id: 1,

  metadata: {
    created: new Date(),
    updated: new Date()
  },

  name: 'Product'
}

const anotherSimple = 'value'
const moreSimple = 42
```

**❌ Wrong:**

```typescript
// Don't separate one-line declarations
const name = 'John'

const age = 30

const city = 'New York'

// Don't keep multiline declarations together
const complexObject = {
  id: 1,
  name: 'Product'
}
const anotherObject = {
  bar: 'baz',
  foo: 'bar'
}
```

### Rule: Inline JSDoc comments on one line

**One-line JSDoc comments** should be on the same line with `/**` and `*/`.

### Examples

**✅ Correct:**

```typescript
/** User ID */
const userId = 123

/** Calculates the total price */
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0)
}

/**
 * Complex function with detailed documentation
 * @param name - User name
 * @returns Greeting message
 */
function greet(name: string): string {
  return `Hello, ${name}`
}
```

**❌ Wrong:**

```typescript
/**
 * User ID
 */
const userId = 123

/**
 * Calculates the total price
 */
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0)
}
```

### Rule: Object key ordering - shorthand properties first

**Shorthand properties** in objects should be ordered before regular properties.

### Examples

**✅ Correct:**

```typescript
const user = {
  age,
  name,
  city: 'New York',
  country: 'USA'
}

const config = {
  isActive,
  timeout,
  apiKey: 'secret-key',
  baseUrl: 'https://api.example.com'
}
```

**❌ Wrong:**

```typescript
// Don't mix shorthand and regular properties
const user = {
  city: 'New York',
  age,
  name,
  country: 'USA'
}

const config = {
  apiKey: 'secret-key',
  isActive,
  baseUrl: 'https://api.example.com',
  timeout
}
```

### Rule: Object keys alphabetically ordered

**Object keys** should be ordered alphabetically, with **shorthand properties** grouped first (also alphabetically).

### Examples

**✅ Correct:**

```typescript
const user = {
  age,
  name,
  city: 'New York',
  country: 'USA'
}

const config = {
  isActive,
  timeout,
  apiKey: 'secret-key',
  baseUrl: 'https://api.example.com'
}
```

**❌ Wrong:**

```typescript
// Keys not in alphabetical order
const user = {
  name,
  age,
  country: 'USA',
  city: 'New York'
}
```

### Rule: Multiple object keys on separate lines

**Objects with more than one key** must have each key on a separate line.

### Examples

**✅ Correct:**

```typescript
// Single key - can stay on one line
const point = { x: 10 }

// Multiple keys - separate lines
const user = {
  age: 30,
  name: 'John'
}

const config = {
  apiKey: 'secret',
  timeout: 5000
}
```

**❌ Wrong:**

```typescript
// Don't put multiple keys on one line
const user = { name: 'John', age: 30 }

const config = { apiKey: 'secret', timeout: 5000 }
```

### Rule: Separate multiline object values with blank lines

**Multiline values** in objects should be separated by blank lines.

### Examples

**✅ Correct:**

```typescript
const config = {
  another: 42,
  lastSimple: 'end',
  simple: 'value',

  array: [
    'item1',
    'item2'
  ],

  complex: {
    deep: 'value',
    nested: true
  }
}
```

**❌ Wrong:**

```typescript
// Don't keep multiline values together
const config = {
  another: 42,
  lastSimple: 'end',
  simple: 'value',
  array: [
    'item1',
    'item2'
  ],
  complex: {
    deep: 'value',
    nested: true
  }
}
```

### Rule: No trailing commas

**Never use trailing commas** in arrays, objects, or other structures.

### Examples

**✅ Correct:**

```typescript
const items = [
  'first',
  'second',
  'third'
]

const user = {
  age: 30,
  city: 'New York',
  name: 'John'
}
```

**❌ Wrong:**

```typescript
// Don't use trailing commas
const items = [
  'first',
  'second',
  'third',
]

const user = {
  age: 30,
  city: 'New York',
  name: 'John'
}
```

### Rule: Separate multiline blocks with blank lines

**Multiline blocks** (if/else, loops, try/catch, functions, etc.) should be separated from other code with blank lines, unless they are at the start or end of a parent block.

### Examples

**✅ Correct:**

```typescript
function processUser(user: User) {
  const isValid = validateUser(user)

  if (isValid) {
    console.log('Valid user')
    saveToDatabase(user)
  }

  return isValid
}

const result = calculate()

for (const item of items) {
  processItem(item)
  updateCounter(item)
}

const total = getTotal()
```

**❌ Wrong:**

```typescript
// Don't keep multiline blocks together with other code
function processUser(user: User) {
  const isValid = validateUser(user)
  if (isValid) {
    console.log('Valid user')
    saveToDatabase(user)
  }
  return isValid
}

const result = calculate()
for (const item of items) {
  processItem(item)
  updateCounter(item)
}
const total = getTotal()
```

**Note:** Blank lines at the start or end of parent blocks are not needed:

```typescript
// ✅ No blank line needed after opening brace
function example() {
  const value = 10

  if (value > 5) {
    doSomething()
  }
  // ✅ No blank line needed before closing brace
}
```

### Rule: Nested function calls as arguments on separate lines

**Exception to the "No function calls as arguments" rule**: In **rare cases** (e.g., validator schemas, DSL configurations) when using a function call as an argument is necessary for readability, **parameters should be on separate lines**.

### Examples

**✅ Correct:**

```typescript
// Validator schemas - rare exception
const schema = v.string(
  v.array()
)

const userSchema = v.object(
  v.optional(
    v.string()
  )
)

const pipeline = pipe(
  transform(config)
)
```

**❌ Wrong:**

```typescript
// Don't keep nested function calls on the same line
const schema = v.string(v.array())
const userSchema = v.object(v.optional(v.string()))
const pipeline = pipe(transform(config))
```

**Note:** Prefer extracting to variables in most cases. Use this exception sparingly.
