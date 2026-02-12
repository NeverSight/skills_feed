---
name: slidev-code-blocks
description: Create beautiful code blocks with Shiki syntax highlighting. Use this skill for code snippets, line highlighting, and code groups.
---

# Slidev Code Blocks

This skill covers everything about displaying code in Slidev presentations, including syntax highlighting with Shiki, line highlighting, code groups, and importing external snippets.

## When to Use This Skill

- Displaying code snippets in presentations
- Highlighting specific lines of code
- Creating step-by-step code reveals
- Showing code comparisons
- Importing code from external files

## Basic Code Blocks

### Simple Code Block

````markdown
```javascript
function greet(name) {
  return `Hello, ${name}!`
}
```
````

### With Language Specification

Shiki supports 100+ languages:

````markdown
```typescript
interface User {
  id: number
  name: string
  email: string
}
```
````

````markdown
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```
````

````markdown
```rust
fn main() {
    println!("Hello, Rust!");
}
```
````

## Line Numbers

### Enable Line Numbers

````markdown
```typescript {lines:true}
const x = 1
const y = 2
const z = x + y
```
````

### Global Configuration

In frontmatter:

```yaml
---
lineNumbers: true
---
```

### Starting Line Number

````markdown
```typescript {startLine:5}
// This starts at line 5
const x = 1
```
````

## Line Highlighting

### Highlight Specific Lines

````markdown
```typescript {2,3}
const a = 1
const b = 2  // highlighted
const c = 3  // highlighted
const d = 4
```
````

### Highlight Ranges

````markdown
```typescript {1-3,5}
line 1  // highlighted
line 2  // highlighted
line 3  // highlighted
line 4
line 5  // highlighted
```
````

### Click-Through Highlighting

Reveal highlights step by step:

````markdown
```typescript {1|2-3|5}
const name = 'Slidev'      // Click 1
const version = '0.50'     // Click 2
const author = 'Anthony'   // Click 2

console.log(name, version) // Click 3
```
````

### Highlight All Then Focus

````markdown
```typescript {*|1|2|3}
const a = 1
const b = 2
const c = 3
```
````

- Click 0: All lines visible
- Click 1: Line 1 highlighted
- Click 2: Line 2 highlighted
- Click 3: Line 3 highlighted

### With Final State

````markdown
```typescript {1|2|all}
const x = 1
const y = 2
```
````

## Code Block Options

### Maximum Height

````markdown
```typescript {maxHeight:'200px'}
// Long code block
// with many lines
// ...
```
````

### Wrapping

````markdown
```typescript {wrap:true}
const veryLongLine = 'This is a very long line that would normally overflow the code block but now it wraps nicely'
```
````

### Combined Options

````markdown
```typescript {2-4|6-8}{lines:true,startLine:10,maxHeight:'300px'}
function example() {
  const a = 1
  const b = 2
  const c = 3

  return {
    sum: a + b + c
  }
}
```
````

## Code Themes

### Configure in setup/shiki.ts

```typescript
// setup/shiki.ts
import { defineShikiSetup } from '@slidev/types'

export default defineShikiSetup(() => {
  return {
    themes: {
      dark: 'vitesse-dark',
      light: 'vitesse-light',
    },
  }
})
```

### Popular Themes

- `vitesse-dark` / `vitesse-light`
- `dracula`
- `one-dark-pro`
- `nord`
- `material-theme`
- `github-dark` / `github-light`

## Code Groups

Show multiple code variants in tabs:

````markdown
```typescript {monaco}
// TypeScript version
interface User {
  name: string
}
```

```javascript
// JavaScript version
const user = {
  name: 'John'
}
```
````

Use `<<< ` to create tabbed code groups (experimental):

````markdown
<<< @/snippets/example.ts
<<< @/snippets/example.js
````

## Importing External Code

### Full File Import

````markdown
<<< @/snippets/example.ts
````

### With Line Range

````markdown
<<< @/snippets/example.ts#L5-10
````

### With Language Override

````markdown
<<< @/snippets/config{json}
````

### With Highlighting

````markdown
<<< @/snippets/example.ts {2,4}
````

## Diff Highlighting

Show code changes:

````markdown
```typescript
function greet(name: string) {
  return `Hello, ${name}!` // [!code --]
  return `Hi, ${name}!`    // [!code ++]
}
```
````

### Highlight Specific Changes

````markdown
```typescript
const config = {
  theme: 'dark',   // [!code highlight]
  debug: false,    // [!code warning]
  timeout: 1000,   // [!code error]
}
```
````

## TwoSlash Integration

TypeScript hover information:

````markdown
```typescript twoslash
const message = 'Hello'
//    ^?
```
````

Hover annotations:

````markdown
```typescript twoslash
interface User {
  name: string
  age: number
}

const user: User = {
  name: 'John',
  age: 30
}
//    ^?
```
````

## Code Focus

### Focus Mode

Dim non-highlighted lines:

````markdown
```typescript {2}{focus}
const a = 1
const b = 2  // Focused, others dimmed
const c = 3
```
````

### Click Focus Transitions

````markdown
```typescript {1|2|3}{focus}
step1()  // First focused
step2()  // Then this
step3()  // Finally this
```
````

## Inline Code

### Simple Inline

```markdown
Use the `useState` hook for state management.
```

### Styled Inline

```markdown
The function returns `true`{.text-green-500} or `false`{.text-red-500}.
```

## Code Block Styling

### Custom CSS Class

````markdown
```typescript {class:'my-code'}
const x = 1
```
````

```css
.my-code {
  font-size: 0.9em;
  border-radius: 8px;
}
```

### Scoped Styles

```markdown
# Code Slide

```js
const x = 1
```

<style>
.slidev-code {
  font-size: 1.2em;
}
</style>
```

## Best Practices

### 1. Keep Code Concise

❌ **Too much code**
````markdown
```typescript
// Full 100-line file
```
````

✓ **Focused snippet**
````markdown
```typescript
// Just the relevant function
function handleClick() {
  setState(value => value + 1)
}
```
````

### 2. Use Meaningful Highlights

❌ **No context**
````markdown
```typescript
const x = 1
```
````

✓ **Guided attention**
````markdown
```typescript {2}
const x = 1
const important = 'focus here'  // highlighted
const y = 2
```
````

### 3. Progressive Reveal for Complex Code

````markdown
```typescript {1-2|4-6|8-10}
// Step 1: Define types
interface User { name: string }

// Step 2: Create function
function greet(user: User) {
  return `Hello, ${user.name}`
}

// Step 3: Usage
const greeting = greet({ name: 'World' })
console.log(greeting)
```
````

### 4. Use Comments for Context

````markdown
```typescript
// BAD: Magic numbers
const delay = 1000

// GOOD: Named constants
const ANIMATION_DELAY_MS = 1000
```
````

## Common Patterns

### Before/After Comparison

````markdown
```typescript
// Before
function add(a, b) {
  return a + b
}

// After
const add = (a: number, b: number): number => a + b
```
````

### Step-by-Step Tutorial

````markdown
```typescript {1|1-4|1-7|1-10}
// Step 1: Import
import { ref } from 'vue'

// Step 2: Create ref
const count = ref(0)

// Step 3: Create function
function increment() {
  count.value++
}
```
````

## Output Format

When creating code slides, provide:

```markdown
---
layout: default
---

# [Topic]

[Brief explanation of what the code does]

```[language] {[highlights]}{[options]}
[code]
```

<!--
Speaker notes:
- Explain line X
- Demo this part
-->
```

**KEY DECISIONS:**
- Language: [chosen language]
- Highlighting: [which lines and why]
- Animation: [click sequence if any]
- Theme: [if non-default]
```
