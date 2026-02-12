---
name: opentui-react
description: Expert assistance for OpenTUI with React. Use for React components, hooks (useKeyboard, useRenderer, useTimeline), JSX patterns, state management, forms, and testing.
---

# OpenTUI React Integration

Expert assistance for building terminal UIs with OpenTUI and React.

## Quick Start

```bash
# Install dependencies
bun install @opentui/core @opentui/react react
```

## Basic Setup

```tsx
import { createCliRenderer } from "@opentui/core"
import { createRoot } from "@opentui/react"

function App() {
  return <text>Hello, OpenTUI React!</text>
}

async function main() {
  const renderer = await createCliRenderer()
  createRoot(renderer).render(<App />)
}

main()
```

## React Hooks

### useKeyboard

Handle keyboard events in React components.

```tsx
import { useKeyboard } from "@opentui/react"

function App() {
  useKeyboard((key) => {
    if (key.name === "c" && key.ctrl) {
      process.exit(0)
    }
    if (key.name === "q") {
      process.exit(0)
    }
  })

  return <text>Press Ctrl+C or q to exit</text>
}
```

### useRenderer

Access the renderer instance.

```tsx
import { useRenderer } from "@opentui/react"

function Component() {
  const renderer = useRenderer()

  const handleClick = () => {
    console.log("Renderer available:", !!renderer)
  }

  return <box onClick={handleClick}>Click me</box>
}
```

### useTerminalDimensions

Get terminal size changes.

```tsx
import { useTerminalDimensions } from "@opentui/react"

function Responsive() {
  const { width, height } = useTerminalDimensions()

  return (
    <box>
      <text>Terminal: {width}x{height}</text>
    </box>
  )
}
```

### useTimeline

Create animations in React.

```tsx
import { useTimeline } from "@opentui/react"
import { useRef } from "react"

function AnimatedBox() {
  const boxRef = useRef<any>(null)

  const timeline = useTimeline({
    duration: 1000,
    easing: (t) => t * (2 - t), // easeOutQuad
  })

  const animate = () => {
    if (boxRef.current) {
      timeline.to(boxRef.current, {
        backgroundColor: { r: 255, g: 0, b: 0 },
      })
      timeline.play()
    }
  }

  return (
    <box ref={boxRef} onClick={animate}>
      <text>Click to animate</text>
    </box>
  )
}
```

## React Components

All OpenTUI components are available as JSX elements:

```tsx
import {
  text,
  box,
  input,
  select,
  scrollbox,
  code,
} from "@opentui/react"

function Form() {
  return (
    <box flexDirection="column" gap={1}>
      <text decoration="bold">User Information</text>

      <input placeholder="Name" />
      <input placeholder="Email" />

      <select
        options={[
          { label: "Option 1", value: "1" },
          { label: "Option 2", value: "2" },
        ]}
      />

      <box borderStyle="single">
        <text>Submit</text>
      </box>
    </box>
  )
}
```

## Styling in React

Styles are passed as props to components:

```tsx
function StyledComponent() {
  return (
    <box
      borderStyle="double"
      borderColor={{ r: 100, g: 149, b: 237 }}
      backgroundColor={{ r: 30, g: 30, b: 30 }}
      padding={1}
    >
      <text
        foregroundColor={{ r: 255, g: 255, b: 255 }}
        decoration="bold underline"
      >
        Styled Text
      </text>
    </box>
  )
}
```

**Color format:** `{ r: number, g: number, b: number, a?: number }`

## State Management

### Local State

```tsx
import { useState } from "react"

function Counter() {
  const [count, setCount] = useState(0)

  useKeyboard((key) => {
    if (key.name === "up") setCount(c => c + 1)
    if (key.name === "down") setCount(c => c - 1)
  })

  return (
    <box>
      <text>Count: {count}</text>
      <text>Use arrow keys</text>
    </box>
  )
}
```

### Form State

```tsx
function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [errors, setErrors] = useState<any>({})

  const handleSubmit = () => {
    const newErrors: any = {}

    if (!email.includes("@")) {
      newErrors.email = "Invalid email"
    }
    if (password.length < 8) {
      newErrors.password = "Password too short"
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    console.log("Login:", { email, password })
  }

  return (
    <box flexDirection="column" gap={1}>
      <text decoration="bold">Login</text>

      <input
        value={email}
        onChange={setEmail}
        placeholder="Email"
      />
      {errors.email && (
        <text foregroundColor={{ r: 231, g: 76, b: 60 }}>
          {errors.email}
        </text>
      )}

      <input
        value={password}
        onChange={setPassword}
        placeholder="Password"
        password
      />
      {errors.password && (
        <text foregroundColor={{ r: 231, g: 76, b: 60 }}>
          {errors.password}
        </text>
      )}

      <box onClick={handleSubmit} borderStyle="single">
        <text>Submit</text>
      </box>
    </box>
  )
}
```

### External State Management

#### Redux Integration

```tsx
import { Provider, useSelector, useDispatch } from "react-redux"

function Counter() {
  const count = useSelector((state: any) => state.count)
  const dispatch = useDispatch()

  useKeyboard((key) => {
    if (key.name === "up") dispatch({ type: "INCREMENT" })
    if (key.name === "down") dispatch({ type: "DECREMENT" })
  })

  return <text>Count: {count}</text>
}
```

#### Zustand Integration

```tsx
import { create } from "zustand"

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state: any) => ({ count: state.count + 1 })),
  decrement: () => set((state: any) => ({ count: state.count - 1 })),
}))

function Counter() {
  const { count, increment, decrement } = useStore()

  useKeyboard((key) => {
    if (key.name === "up") increment()
    if (key.name === "down") decrement()
  })

  return <text>Count: {count}</text>
}
```

## Common Patterns

### List with Selection

```tsx
function SelectList({ items }: { items: string[] }) {
  const [selectedIndex, setSelectedIndex] = useState(0)

  useKeyboard((key) => {
    if (key.name === "down" || (key.name === "tab" && !key.shift)) {
      setSelectedIndex(i => Math.min(i + 1, items.length - 1))
    }
    if (key.name === "up" || (key.name === "tab" && key.shift)) {
      setSelectedIndex(i => Math.max(i - 1, 0))
    }
    if (key.name === "enter") {
      console.log("Selected:", items[selectedIndex])
    }
  })

  return (
    <scrollbox height={20}>
      {items.map((item, index) => (
        <box
          key={index}
          backgroundColor={
            index === selectedIndex
              ? { r: 100, g: 149, b: 237 }
              : { r: 30, g: 30, b: 30 }
          }
        >
          <text
            foregroundColor={
              index === selectedIndex
                ? { r: 255, g: 255, b: 255 }
                : { r: 255, g: 255, b: 255 }
            }
          >
            {index === selectedIndex ? "> " : "  "}{item}
          </text>
        </box>
      ))}
    </scrollbox>
  )
}
```

### Tabs

```tsx
function Tabs({ tabs }: { tabs: Array<{ id: string, label: string, content: any }> }) {
  const [activeTab, setActiveTab] = useState(tabs[0].id)

  return (
    <box flexDirection="column" height={30}>
      {/* Tab headers */}
      <box flexDirection="row">
        {tabs.map(tab => (
          <box
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            borderStyle={activeTab === tab.id ? "single" : "none"}
            backgroundColor={
              activeTab === tab.id
                ? { r: 100, g: 149, b: 237 }
                : { r: 50, g: 50, b: 50 }
            }
            padding={1}
          >
            <text>{tab.label}</text>
          </box>
        ))}
      </box>

      {/* Tab content */}
      <box flexGrow={1} padding={1}>
        {tabs.find(t => t.id === activeTab)?.content}
      </box>
    </box>
  )
}
```

### Modal/Dialog

```tsx
function Modal({ isOpen, onClose, children }: any) {
  if (!isOpen) return null

  return (
    <box
      position="absolute"
      top={0}
      left={0}
      width="100%"
      height="100%"
      backgroundColor={{ r: 0, g: 0, b: 0, a: 0.5 }}
      justifyContent="center"
      alignItems="center"
      onClick={onClose}
    >
      <box
        borderStyle="double"
        backgroundColor={{ r: 30, g: 30, b: 30 }}
        padding={2}
        onClick={(e: any) => e.stopPropagation()}
      >
        {children}
      </box>
    </box>
  )
}
```

## When to Use This Skill

Use `/opentui-react` for:
- Building TUIs with React
- Using hooks (useKeyboard, useRenderer, etc.)
- JSX-style component development
- Integrating with React state management
- Testing React OpenTUI components

For vanilla TypeScript/JavaScript, use `/opentui`
For SolidJS development, use `/opentui-solid`
For project scaffolding, use `/opentui-projects`

## Resources

- [Hooks Reference](references/HOOKS.md) - Complete hook documentation
- [Component Props](references/PROPS.md) - React component props
- [Patterns](references/PATTERNS.md) - Common React patterns
- [State Management](references/STATE.md) - React state integration
- [Testing](references/TESTING.md) - Testing React components

## Key Knowledge Sources

- OpenTUI React GitHub: https://github.com/sst/opentui/tree/main/packages/react
- Context7: `/sst/opentui` - React integration queries
- Research: `.search-data/research/opentui/`
