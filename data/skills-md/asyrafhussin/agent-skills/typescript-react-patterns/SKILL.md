---
name: typescript-react-patterns
description: TypeScript best practices for React development. Use when writing typed React components, hooks, events, refs, or generic components. Triggers on tasks involving TypeScript errors, type definitions, props typing, or type-safe React patterns.
license: MIT
metadata:
  author: typescript-react-patterns
  version: "1.0.0"
---

# TypeScript React Patterns

Comprehensive TypeScript patterns for React applications. Contains 35+ rules across 7 categories for building type-safe, maintainable React code.

## When to Apply

Reference these guidelines when:
- Typing React component props
- Creating custom hooks with TypeScript
- Handling events with proper types
- Building generic, reusable components
- Fixing TypeScript errors in React code

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Component Typing | CRITICAL | `comp-` |
| 2 | Hook Typing | CRITICAL | `hook-` |
| 3 | Event Handling | HIGH | `event-` |
| 4 | Ref Typing | HIGH | `ref-` |
| 5 | Generic Components | MEDIUM | `generic-` |
| 6 | Context & State | MEDIUM | `ctx-` |
| 7 | Utility Types | LOW | `util-` |

## Quick Reference

### 1. Component Typing (CRITICAL)

- `comp-props-interface` - Use interface for props, type for unions
- `comp-children-types` - Correct children typing patterns
- `comp-default-props` - Default props with TypeScript
- `comp-forward-ref` - Typing forwardRef components
- `comp-compound` - Compound component patterns
- `comp-polymorphic` - "as" prop typing

### 2. Hook Typing (CRITICAL)

- `hook-usestate` - useState with proper types
- `hook-useref` - useRef for DOM and mutable values
- `hook-useeffect` - useEffect cleanup typing
- `hook-usereducer` - useReducer with discriminated unions
- `hook-custom-return` - Custom hook return types
- `hook-generic` - Generic custom hooks

### 3. Event Handling (HIGH)

- `event-handler-types` - Event handler type patterns
- `event-synthetic` - SyntheticEvent types
- `event-form` - Form event handling
- `event-keyboard` - Keyboard event types
- `event-mouse` - Mouse event types
- `event-custom` - Custom event types

### 4. Ref Typing (HIGH)

- `ref-dom-elements` - Refs for DOM elements
- `ref-mutable` - Mutable ref pattern
- `ref-callback` - Callback ref typing
- `ref-forward` - Forwarding refs
- `ref-imperative-handle` - useImperativeHandle typing

### 5. Generic Components (MEDIUM)

- `generic-list` - Generic list components
- `generic-form` - Generic form components
- `generic-select` - Generic select/dropdown
- `generic-table` - Generic table components
- `generic-constraints` - Generic constraints

### 6. Context & State (MEDIUM)

- `ctx-create` - Creating typed context
- `ctx-provider` - Provider typing patterns
- `ctx-consumer` - useContext with proper types
- `ctx-reducer` - Context with reducer
- `ctx-default-value` - Handling default values

### 7. Utility Types (LOW)

- `util-react-types` - Built-in React types
- `util-component-props` - ComponentProps utility
- `util-pick-omit` - Pick and Omit for props
- `util-discriminated-unions` - State machines
- `util-assertion-functions` - Type assertions

## Essential Patterns

### Component Props

```typescript
// Use interface for props (extendable)
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  children: React.ReactNode
  onClick?: () => void
}

// Use type for unions
type ButtonVariant = 'primary' | 'secondary' | 'danger'

function Button({
  variant,
  size = 'md',
  isLoading = false,
  children,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={`btn-${variant} btn-${size}`}
      onClick={onClick}
      disabled={isLoading}
    >
      {isLoading ? 'Loading...' : children}
    </button>
  )
}
```

### Children Typing

```typescript
// ReactNode - most flexible (string, number, element, array, null)
interface CardProps {
  children: React.ReactNode
}

// ReactElement - only JSX elements
interface WrapperProps {
  children: React.ReactElement
}

// Render prop pattern
interface DataFetcherProps<T> {
  children: (data: T) => React.ReactNode
}

// Specific element type
interface TabsProps {
  children: React.ReactElement<TabProps> | React.ReactElement<TabProps>[]
}
```

### Event Handlers

```typescript
// Form events
function Form() {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    // handle submit
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value)
  }

  const handleSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    console.log(e.target.value)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} />
      <select onChange={handleSelect}>
        <option>A</option>
        <option>B</option>
      </select>
    </form>
  )
}
```

### Refs

```typescript
// DOM element ref
function Input() {
  const inputRef = useRef<HTMLInputElement>(null)

  const focus = () => {
    inputRef.current?.focus()
  }

  return <input ref={inputRef} />
}

// Mutable ref (no null, stores values)
function Timer() {
  const intervalRef = useRef<number | undefined>(undefined)

  useEffect(() => {
    intervalRef.current = window.setInterval(() => {
      // tick
    }, 1000)

    return () => {
      clearInterval(intervalRef.current)
    }
  }, [])
}
```

### Generic Components

```typescript
// Generic list component
interface ListProps<T> {
  items: T[]
  renderItem: (item: T, index: number) => React.ReactNode
  keyExtractor: (item: T) => string | number
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  )
}

// Usage - T is inferred
<List
  items={users}
  renderItem={(user) => <UserCard user={user} />}
  keyExtractor={(user) => user.id}
/>
```

### Context

```typescript
interface AuthContextType {
  user: User | null
  login: (credentials: Credentials) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | null>(null)

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const login = async (credentials: Credentials) => {
    // implementation
  }

  const logout = () => {
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  )
}
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/comp-props-interface.md
rules/hook-usestate.md
rules/event-handler-types.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and edge cases
