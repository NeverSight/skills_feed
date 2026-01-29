---
name: jotai-expert
description: Expert guidance for Jotai state management in React applications. Provides best practices, performance optimization, and architectural patterns. Use when designing atom structures, implementing state management, optimizing re-renders, handling async state, integrating with TypeScript, or reviewing Jotai code for performance issues. Triggers on tasks involving Jotai atoms, derived state, focusAtom, splitAtom, atomFamily, or state management architecture decisions.
---

# Jotai Expert

Jotai is a primitive and flexible state management library for React using an atomic approach. Always reference https://jotai.org/ for the latest API details.

## Decision Tree

```
Need state management?
├── Simple local state → useState (no Jotai needed)
├── Shared state across components
│   ├── Few components, same tree → Context may suffice
│   └── Many components, complex → Use Jotai ✓
└── Global app state → Use Jotai ✓

Choosing atom type:
├── Static value → atom(initialValue)
├── Computed from other atoms → atom((get) => ...)
├── Need to modify other atoms → atom(null, (get, set) => ...)
├── Persist to storage → atomWithStorage()
├── List of items → splitAtom() or atoms-in-atom
└── Parameterized data → atomFamily()

Performance issue?
├── Component re-renders too often
│   ├── Only reading? → useAtomValue
│   ├── Only writing? → useSetAtom
│   ├── Large object? → selectAtom / focusAtom
│   └── List items? → splitAtom
└── Async loading states → loadable() or manual loading atoms
```

## Core Patterns

### Atom Types

```typescript
import { atom } from 'jotai'

// 1. Primitive: holds value
const countAtom = atom(0)

// 2. Derived read-only: computed from others
const doubleAtom = atom((get) => get(countAtom) * 2)

// 3. Derived read-write: custom setter
const celsiusAtom = atom(0)
const fahrenheitAtom = atom(
  (get) => get(celsiusAtom) * 9/5 + 32,
  (get, set, newF: number) => set(celsiusAtom, (newF - 32) * 5/9)
)

// 4. Write-only (action): no read value
const incrementAtom = atom(null, (get, set) => {
  set(countAtom, get(countAtom) + 1)
})
```

### Hook Selection

| Need | Hook | Re-renders on change |
|------|------|---------------------|
| Read only | `useAtomValue(atom)` | Yes |
| Write only | `useSetAtom(atom)` | No |
| Both | `useAtom(atom)` | Yes |

### Reference Stability

```typescript
// ❌ WRONG: Creates new atom every render
function Component() {
  const myAtom = atom(0) // Unstable reference
}

// ✅ CORRECT: Define outside component
const myAtom = atom(0)
function Component() {
  const [value] = useAtom(myAtom)
}

// ✅ CORRECT: useMemo for dynamic atoms
function Component({ id }) {
  const itemAtom = useMemo(() => atom(items[id]), [id])
}
```

## Performance Optimization

### 1. Granular Subscriptions

```typescript
// ❌ BAD: Re-renders on any user field change
function UserProfile() {
  const [user] = useAtom(userAtom)
  return <h1>{user.name}</h1>
}

// ✅ GOOD: Only re-renders when name changes
import { selectAtom } from 'jotai/utils'
const nameAtom = selectAtom(userAtom, (u) => u.name)

function UserName() {
  const name = useAtomValue(nameAtom)
  return <h1>{name}</h1>
}
```

### 2. Efficient Lists with splitAtom

```typescript
import { splitAtom } from 'jotai/utils'

const todosAtom = atom<Todo[]>([])
const todoAtomsAtom = splitAtom(todosAtom, (t) => t.id)

function TodoList() {
  const [todoAtoms] = useAtom(todoAtomsAtom)
  return todoAtoms.map((todoAtom) => (
    <TodoItem key={todoAtom.toString()} atom={todoAtom} />
  ))
}

// Each item updates independently
function TodoItem({ atom }) {
  const [todo, setTodo] = useAtom(atom)
  // Changes here don't re-render other items
}
```

### 3. Large Objects with focusAtom

```typescript
import { focusAtom } from 'jotai-optics'

const formAtom = atom({ name: '', email: '', address: { city: '' } })

// Focused atoms for each field
const nameAtom = focusAtom(formAtom, (o) => o.prop('name'))
const cityAtom = focusAtom(formAtom, (o) => o.prop('address').prop('city'))

// Each field component only re-renders when its value changes
```

### 4. Async with loadable

```typescript
import { loadable } from 'jotai/utils'

const asyncDataAtom = atom(async () => fetch('/api').then(r => r.json()))
const loadableDataAtom = loadable(asyncDataAtom)

function Component() {
  const data = useAtomValue(loadableDataAtom)
  if (data.state === 'loading') return <Spinner />
  if (data.state === 'hasError') return <Error />
  return <Data value={data.data} />
}
```

## Anti-Patterns to Avoid

1. **Heavy computation in components**: Move to atom read functions or actions
2. **Creating atoms in render**: Define outside or use useMemo
3. **Using useAtom when only reading/writing**: Use useAtomValue/useSetAtom
4. **Over-fragmenting frequently-updated data**: Batch related updates
5. **Nested Suspense for every async atom**: Use strategic boundaries or loadable

## References

Detailed documentation organized by topic:

- **[references/core-api.md](references/core-api.md)**: atom, hooks, Store, Provider API details
- **[references/utilities.md](references/utilities.md)**: atomWithStorage, loadable, splitAtom, selectAtom, atomFamily
- **[references/performance.md](references/performance.md)**: Optimization strategies, render control, large object handling
- **[references/patterns.md](references/patterns.md)**: Organization, async patterns, testing, TypeScript, SSR, debugging

When implementing or reviewing Jotai code, load the relevant reference file for detailed guidance.
