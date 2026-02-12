---
name: slidev-monaco-editor
description: Add live coding with Monaco Editor in Slidev. Use this skill for interactive code demos, executable code, and real-time editing.
---

# Monaco Editor in Slidev

This skill covers integrating Monaco Editor (the editor powering VS Code) into your Slidev presentations for live coding, interactive demos, and executable code blocks.

## When to Use This Skill

- Live coding demonstrations
- Interactive code editing during presentations
- Running code examples in real-time
- Teaching programming concepts
- Showing auto-completion and type hints

## Enabling Monaco Editor

### Basic Monaco Block

Add `{monaco}` to any code block:

````markdown
```typescript {monaco}
const greeting = 'Hello, World!'
console.log(greeting)
```
````

This creates an editable code block with:
- Syntax highlighting
- Auto-completion
- Type checking (for TypeScript)
- Bracket matching

### Monaco with Line Highlighting

````markdown
```typescript {monaco}{2,3}
const a = 1
const b = 2  // highlighted
const c = 3  // highlighted
```
````

## Monaco Runner

Execute code directly in the presentation:

### JavaScript Runner

````markdown
```javascript {monaco-run}
const numbers = [1, 2, 3, 4, 5]
const doubled = numbers.map(n => n * 2)
console.log(doubled)
```
````

Click "Run" to execute and see output.

### TypeScript Runner

````markdown
```typescript {monaco-run}
interface User {
  name: string
  age: number
}

const user: User = {
  name: 'John',
  age: 30
}

console.log(`${user.name} is ${user.age} years old`)
```
````

### Auto-Run on Load

````markdown
```javascript {monaco-run} {autorun:true}
console.log('This runs automatically!')
```
````

### Show Output Only

````markdown
```javascript {monaco-run} {showOutputAt:'+1'}
// Output shows after one click
console.log('Hello!')
```
````

## Configuration Options

### Editor Height

````markdown
```typescript {monaco}{height:'300px'}
// Taller editor
function longFunction() {
  // ...
}
```
````

### Read-Only Mode

````markdown
```typescript {monaco}{readonly:true}
// Cannot be edited
const CONSTANT = 'value'
```
````

### Diff Editor

````markdown
```typescript {monaco-diff}
const original = 'Hello'
~~~
const modified = 'Hello, World!'
```
````

## Monaco Setup Configuration

### setup/monaco.ts

```typescript
import { defineMonacoSetup } from '@slidev/types'

export default defineMonacoSetup((monaco) => {
  // Editor options
  return {
    editorOptions: {
      fontSize: 14,
      fontFamily: 'JetBrains Mono, monospace',
      minimap: { enabled: false },
      lineNumbers: 'on',
      wordWrap: 'on',
      tabSize: 2,
      scrollBeyondLastLine: false,
      automaticLayout: true,
    },
    // Light/dark theme
    theme: {
      light: 'vs',
      dark: 'vs-dark',
    },
  }
})
```

### Custom Themes

```typescript
import { defineMonacoSetup } from '@slidev/types'

export default defineMonacoSetup((monaco) => {
  // Define custom theme
  monaco.editor.defineTheme('my-theme', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'comment', foreground: '6A9955' },
      { token: 'keyword', foreground: 'C586C0' },
    ],
    colors: {
      'editor.background': '#1a1a2e',
    },
  })

  return {
    theme: {
      dark: 'my-theme',
      light: 'vs',
    },
  }
})
```

## Type Definitions

### Adding Types for Libraries

```typescript
// setup/monaco.ts
import { defineMonacoSetup } from '@slidev/types'

export default defineMonacoSetup(async (monaco) => {
  // Add React types
  const reactTypes = await fetch(
    'https://unpkg.com/@types/react/index.d.ts'
  ).then(r => r.text())

  monaco.languages.typescript.typescriptDefaults.addExtraLib(
    reactTypes,
    'file:///node_modules/@types/react/index.d.ts'
  )
})
```

### Inline Type Definitions

````markdown
```typescript {monaco}
// Types defined inline
interface Todo {
  id: number
  text: string
  completed: boolean
}

const todos: Todo[] = [
  { id: 1, text: 'Learn Slidev', completed: true },
  { id: 2, text: 'Create presentation', completed: false },
]
```
````

## Interactive Examples

### Counter Demo

````markdown
```typescript {monaco-run}
// Interactive counter
let count = 0

function increment() {
  count++
  console.log(`Count: ${count}`)
}

// Click Run multiple times!
increment()
```
````

### API Simulation

````markdown
```typescript {monaco-run}
// Simulated API call
async function fetchUser(id: number) {
  // Simulate network delay
  await new Promise(r => setTimeout(r, 500))

  return {
    id,
    name: 'John Doe',
    email: 'john@example.com'
  }
}

const user = await fetchUser(1)
console.log(user)
```
````

### Algorithm Visualization

````markdown
```typescript {monaco-run}
// Bubble sort with steps
function bubbleSort(arr: number[]) {
  const result = [...arr]
  const steps: string[] = []

  for (let i = 0; i < result.length; i++) {
    for (let j = 0; j < result.length - i - 1; j++) {
      if (result[j] > result[j + 1]) {
        [result[j], result[j + 1]] = [result[j + 1], result[j]]
        steps.push(`Swap: [${result.join(', ')}]`)
      }
    }
  }

  return { result, steps }
}

const { result, steps } = bubbleSort([5, 3, 8, 4, 2])
console.log('Steps:', steps.length)
steps.forEach(s => console.log(s))
console.log('Final:', result)
```
````

## Code Runner Patterns

### Show Concept Then Let Edit

````markdown
# Array Methods

```typescript {monaco-run}
const numbers = [1, 2, 3, 4, 5]

// Try changing the function!
const result = numbers
  .filter(n => n % 2 === 0)
  .map(n => n * 2)

console.log(result)
```

Try modifying the code to:
- Filter odd numbers
- Triple instead of double
````

### Interactive Quiz

````markdown
# Fix the Bug

```typescript {monaco-run}
// This code has a bug - can you fix it?
function reverseString(str: string) {
  return str.split('').reserve().join('')
}

console.log(reverseString('hello'))
// Expected: 'olleh'
```
````

### Live Data Manipulation

````markdown
```typescript {monaco-run}
const data = [
  { name: 'Alice', score: 85 },
  { name: 'Bob', score: 92 },
  { name: 'Charlie', score: 78 },
]

// Calculate statistics
const average = data.reduce((sum, d) => sum + d.score, 0) / data.length
const highest = Math.max(...data.map(d => d.score))
const passing = data.filter(d => d.score >= 80)

console.log(`Average: ${average.toFixed(1)}`)
console.log(`Highest: ${highest}`)
console.log(`Passing: ${passing.map(d => d.name).join(', ')}`)
```
````

## Combining with Animations

### Reveal Then Edit

````markdown
<v-click>

```typescript {monaco}
// Code appears on click, then is editable
function greet(name: string) {
  return `Hello, ${name}!`
}
```

</v-click>
````

### Step-by-Step with Monaco

````markdown
<v-clicks>

Start with this code:

```typescript {monaco}
const x = 1
```

Then try adding more lines!

</v-clicks>
````

## Best Practices

### 1. Keep Examples Focused

````markdown
```typescript {monaco-run}
// GOOD: Single concept
const sum = [1, 2, 3].reduce((a, b) => a + b, 0)
console.log(sum) // 6
```
````

### 2. Provide Starting Point

````markdown
```typescript {monaco-run}
// Complete the function:
function capitalize(str: string): string {
  // Your code here
  return str
}

console.log(capitalize('hello')) // Should print: 'Hello'
```
````

### 3. Show Expected Output

````markdown
```typescript {monaco-run}
// Code example
const result = [1, 2, 3].map(n => n ** 2)
console.log(result)
// Expected output: [1, 4, 9]
```
````

### 4. Handle Errors Gracefully

````markdown
```typescript {monaco-run}
try {
  const result = riskyOperation()
  console.log(result)
} catch (error) {
  console.error('Error:', error.message)
}

function riskyOperation() {
  // Might throw an error
  throw new Error('Oops!')
}
```
````

## Limitations

- **No DOM Access**: Cannot manipulate the page DOM
- **Limited APIs**: Only standard JavaScript APIs available
- **No Imports**: Cannot import external packages
- **Console Only**: Output is console-based

## Output Format

When creating Monaco code blocks:

```
PURPOSE: [What the code demonstrates]
INTERACTION: [How audience should interact]

CODE:
```[language] {monaco-run}
// Clear comments explaining purpose

[Code with good defaults]

// Expected output noted
```

SUGGESTED EDITS:
- Try changing X to Y
- Modify function to do Z
```
