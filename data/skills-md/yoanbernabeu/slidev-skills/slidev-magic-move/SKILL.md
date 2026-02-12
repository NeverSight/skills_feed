---
name: slidev-magic-move
description: Animate code transformations with Shiki Magic Move. Use this skill to create smooth morphing transitions between code states.
---

# Shiki Magic Move

This skill covers Shiki Magic Move, a powerful feature that creates smooth animated transitions between different code states, similar to Keynote's Magic Move effect.

## When to Use This Skill

- Showing code evolution step by step
- Refactoring demonstrations
- Before/after code comparisons
- Tutorial walkthroughs
- Animated code transformations

## How Magic Move Works

Magic Move analyzes two code blocks and:
1. Identifies unchanged tokens
2. Finds moved/renamed tokens
3. Detects added/removed tokens
4. Animates the transition smoothly

## Basic Syntax

Use 4 backticks with `md magic-move`:

`````markdown
````md magic-move
```js
console.log('Hello')
```
```js
console.log('Hello, World!')
```
````
`````

Each code block represents a step, animated on click.

## Step-by-Step Example

### Refactoring Journey

`````markdown
````md magic-move
```js
// Step 1: Original code
function add(a, b) {
  return a + b
}
```

```js
// Step 2: Add types
function add(a: number, b: number) {
  return a + b
}
```

```js
// Step 3: Add return type
function add(a: number, b: number): number {
  return a + b
}
```

```ts
// Step 4: Convert to arrow function
const add = (a: number, b: number): number => a + b
```
````
`````

## Multiple Steps

`````markdown
````md magic-move
```js
const name = 'world'
```
```js
const name = 'world'
const greeting = 'Hello'
```
```js
const name = 'world'
const greeting = 'Hello'
console.log(`${greeting}, ${name}!`)
```
```js
const name = 'world'
const greeting = 'Hello'
console.log(`${greeting}, ${name}!`)
// Output: Hello, world!
```
````
`````

## Combining with Line Highlighting

Add highlights within Magic Move:

`````markdown
````md magic-move {lines: true}
```js {*|1|2|3}
const a = 1
const b = 2
const c = 3
```
```js {*}
const sum = 1 + 2 + 3
```
````
`````

## Advanced Options

### Control Animation Timing

`````markdown
````md magic-move {at: 3}
```js
// Starts at click 3
const x = 1
```
```js
const x = 1
const y = 2
```
````
`````

### Disable Line Numbers

`````markdown
````md magic-move {lines: false}
```js
const x = 1
```
```js
const x = 2
```
````
`````

### Combined Options

`````markdown
````md magic-move {at: 2, lines: true}
```js {*|1|2}
const first = 1
const second = 2
```
```js {*}
const result = first + second
```
````
`````

## Real-World Examples

### React Hook Evolution

`````markdown
````md magic-move
```jsx
// Class component state
class Counter extends React.Component {
  state = { count: 0 }

  increment = () => {
    this.setState({ count: this.state.count + 1 })
  }

  render() {
    return (
      <button onClick={this.increment}>
        {this.state.count}
      </button>
    )
  }
}
```

```jsx
// Function component with useState
function Counter() {
  const [count, setCount] = useState(0)

  const increment = () => {
    setCount(count + 1)
  }

  return (
    <button onClick={increment}>
      {count}
    </button>
  )
}
```

```jsx
// Simplified with inline handler
function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(c => c + 1)}>
      {count}
    </button>
  )
}
```
````
`````

### API Evolution

`````markdown
````md magic-move
```js
// Callbacks
function fetchUser(id, callback) {
  fetch(`/api/users/${id}`)
    .then(res => res.json())
    .then(data => callback(null, data))
    .catch(err => callback(err, null))
}

fetchUser(1, (err, user) => {
  if (err) console.error(err)
  else console.log(user)
})
```

```js
// Promises
function fetchUser(id) {
  return fetch(`/api/users/${id}`)
    .then(res => res.json())
}

fetchUser(1)
  .then(user => console.log(user))
  .catch(err => console.error(err))
```

```js
// Async/Await
async function fetchUser(id) {
  const res = await fetch(`/api/users/${id}`)
  return res.json()
}

try {
  const user = await fetchUser(1)
  console.log(user)
} catch (err) {
  console.error(err)
}
```
````
`````

### Building a Function

`````markdown
````md magic-move
```typescript
function processData() {

}
```

```typescript
function processData(data) {

}
```

```typescript
function processData(data: string[]) {

}
```

```typescript
function processData(data: string[]): string[] {
  return data
}
```

```typescript
function processData(data: string[]): string[] {
  return data
    .filter(item => item.length > 0)
}
```

```typescript
function processData(data: string[]): string[] {
  return data
    .filter(item => item.length > 0)
    .map(item => item.trim())
}
```

```typescript
function processData(data: string[]): string[] {
  return data
    .filter(item => item.length > 0)
    .map(item => item.trim())
    .sort((a, b) => a.localeCompare(b))
}
```
````
`````

### SQL Query Building

`````markdown
````md magic-move
```sql
SELECT * FROM users
```

```sql
SELECT id, name, email FROM users
```

```sql
SELECT id, name, email FROM users
WHERE active = true
```

```sql
SELECT id, name, email FROM users
WHERE active = true
ORDER BY created_at DESC
```

```sql
SELECT id, name, email FROM users
WHERE active = true
ORDER BY created_at DESC
LIMIT 10
```
````
`````

## Patterns and Tips

### Start Simple, Add Complexity

`````markdown
````md magic-move
```js
// Start with the goal
const result = processData(input)
```

```js
// Show the implementation
function processData(input) {
  return input
}

const result = processData(input)
```

```js
// Add details
function processData(input) {
  return input
    .filter(x => x != null)
    .map(x => transform(x))
}

const result = processData(input)
```
````
`````

### Show Problem Then Solution

`````markdown
````md magic-move
```js
// Problem: Callback hell
getData(function(a) {
  getMoreData(a, function(b) {
    getMoreData(b, function(c) {
      getMoreData(c, function(d) {
        // Finally done
      })
    })
  })
})
```

```js
// Solution: Promises
getData()
  .then(a => getMoreData(a))
  .then(b => getMoreData(b))
  .then(c => getMoreData(c))
  .then(d => {
    // Clean and flat!
  })
```
````
`````

### Highlight Changes with Comments

`````markdown
````md magic-move
```js
const config = {
  debug: true,
  timeout: 1000
}
```

```js
const config = {
  debug: false,    // Changed!
  timeout: 1000
}
```

```js
const config = {
  debug: false,
  timeout: 5000    // Increased!
}
```
````
`````

## Best Practices

1. **Small Steps**: Each transition should show one logical change
2. **Maintain Context**: Keep surrounding code visible when possible
3. **Use Comments**: Add comments to explain what's changing
4. **Consistent Style**: Keep formatting consistent across steps
5. **Test the Animation**: Verify smooth transitions before presenting

## Common Mistakes

❌ **Too many changes at once**
```
Step 1: Original code
Step 2: Completely different code
```

✓ **Incremental changes**
```
Step 1: Original
Step 2: Add one feature
Step 3: Add another feature
Step 4: Refactor
```

❌ **Lost context**
```
Step 1: function foo() { ... }
Step 2: const bar = ...  // Where did foo go?
```

✓ **Preserved context**
```
Step 1: function foo() { ... }
Step 2: function foo() { const bar = ... }
```

## Interactive Playground

Try Magic Move at: https://shiki-magic-move.netlify.app/

## Output Format

When creating Magic Move animations:

```
ANIMATION GOAL: [What transformation are you showing?]

STEPS:
1. [Initial state - describe]
2. [Change 1 - describe]
3. [Change 2 - describe]
...

CODE:
````md magic-move {[options]}
```[lang]
[Step 1 code]
```
```[lang]
[Step 2 code]
```
...
````

SPEAKER NOTES:
- Step 1: [What to say]
- Step 2: [What to say]
```
