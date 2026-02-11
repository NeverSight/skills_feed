---
name: opentui-solid
description: Expert assistance for OpenTUI with SolidJS. Use for reactive components, signals, fine-grained reactivity, JSX patterns, and SolidJS-specific optimization.
---

# OpenTUI SolidJS Integration

Expert assistance for building terminal UIs with OpenTUI and SolidJS.

## Quick Start

```bash
# Install dependencies
bun install @opentui/core @opentui/solid solid-js
```

## Basic Setup

```tsx
import { createCliRenderer } from "@opentui/core"
import { createRoot } from "@opentui/solid"

function App() {
  return <text>Hello, OpenTUI SolidJS!</text>
}

async function main() {
  const renderer = await createCliRenderer()
  createRoot(renderer).render(() => <App />)
}

main()
```

## SolidJS Reactivity

### Signals (Core Primitive)

Signals are the core of SolidJS reactivity:

```tsx
import { createSignal } from "solid-js"

function Counter() {
  const [count, setCount] = createSignal(0)

  return (
    <text>
      Count: {count()}
    </text>
  )
}
```

**Key Concepts:**
- `count()` - Access signal value (getter)
- `setCount(newValue)` - Update signal value (setter)
- Signals automatically track dependencies

### Derived Signals (Memo)

```tsx
import { createMemo } from "solid-js"

function DoubleCounter() {
  const [count, setCount] = createSignal(0)
  const doubleCount = createMemo(() => count() * 2)

  return (
    <box flexDirection="column">
      <text>Count: {count()}</text>
      <text>Double: {doubleCount()}</text>
    </box>
  )
}
```

### Effects (createEffect)

```tsx
import { createEffect } from "solid-js"

function Logger() {
  const [count, setCount] = createSignal(0)

  createEffect(() => {
    console.log("Count changed:", count())
  })

  return <text>Count: {count()}</text>
}
```

## OpenTUI SolidJS Hooks

### useKeyboard

```tsx
import { useKeyboard } from "@opentui/solid"

function App() {
  useKeyboard((key) => {
    if (key.name === "c" && key.ctrl) {
      process.exit(0)
    }
  })

  return <text>Press Ctrl+C to exit</text>
}
```

### useRenderer

```tsx
import { useRenderer } from "@opentui/solid"

function Component() {
  const renderer = useRenderer()

  const exit = () => {
    renderer.destroy()
    process.exit(0)
  }

  return <box onClick={exit}>Exit</box>
}
```

### useTerminalDimensions

```tsx
import { useTerminalDimensions } from "@opentui/solid"

function Responsive() {
  const dimensions = useTerminalDimensions()

  return (
    <box>
      <text>Size: {dimensions().width}x{dimensions().height}</text>
    </box>
  )
}
```

### useTimeline

```tsx
import { useTimeline } from "@opentui/solid"
import { onMount } from "solid-js"

function AnimatedBox() {
  let boxRef: any

  const timeline = useTimeline({
    duration: 1000,
    easing: (t) => t,
  })

  onMount(() => {
    timeline.to(boxRef, {
      backgroundColor: { r: 255, g: 0, b: 0 },
    })
    timeline.play()
  })

  return (
    <box ref={boxRef!}>
      <text>Animated</text>
    </box>
  )
}
```

## SolidJS Components

### All OpenTUI components available as JSX:

```tsx
import {
  text,
  box,
  input,
  select,
  scrollbox,
  code,
} from "@opentui/solid"

function Form() {
  const [name, setName] = createSignal("")

  return (
    <box flexDirection="column" gap={1}>
      <text decoration="bold">User Information</text>

      <input
        value={name()}
        onInput={(e) => setName(e.value)}
        placeholder="Name"
      />

      <box borderStyle="single">
        <text>Submit</text>
      </box>
    </box>
  )
}
```

## Styling in SolidJS

Styles are passed as props:

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
        decoration="bold"
      >
        Styled Text
      </text>
    </box>
  )
}
```

**Color format:** `{ r: number, g: number, b: number, a?: number }`

## State Management

### Local Signals

```tsx
function Counter() {
  const [count, setCount] = createSignal(0)
  const [step, setStep] = createSignal(1)

  const increment = () => setCount(c => c + step())
  const decrement = () => setCount(c => c - step())

  useKeyboard((key) => {
    if (key.name === "up") increment()
    if (key.name === "down") decrement()
  })

  return (
    <box flexDirection="column">
      <text>Count: {count()}</text>
      <input
        value={String(step())}
        onInput={(e) => setStep(parseInt(e.value) || 1)}
      />
      <text>Use arrow keys</text>
    </box>
  )
}
```

### Stores (Objects)

```tsx
import { createStore, produce } from "solid-js/store"

function Form() {
  const [formData, setFormData] = createStore({
    name: "",
    email: "",
    password: "",
  })

  const updateField = (field: string) => (value: string) => {
    setFormData(field, value)
  }

  return (
    <box flexDirection="column" gap={1}>
      <input
        value={formData.name}
        onInput={(e) => updateField("name")(e.value)}
        placeholder="Name"
      />

      <input
        value={formData.email}
        onInput={(e) => updateField("email")(e.value)}
        placeholder="Email"
      />

      <input
        value={formData.password}
        onInput={(e) => updateField("password")(e.value)}
        placeholder="Password"
        password
      />
    </box>
  )
}
```

### Context

```tsx
import { createContext, useContext } from "solid-js"

const ThemeContext = createContext({
  theme: "dark",
  setTheme: (theme: string) => {},
})

function ThemeProvider(props: any) {
  const [theme, setTheme] = createSignal("dark")

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {props.children}
    </ThemeContext.Provider>
  )
}

function ThemedComponent() {
  const { theme } = useContext(ThemeContext)

  return (
    <text>Current theme: {theme()}</text>
  )
}
```

## Common Patterns

### List with Selection

```tsx
function SelectList(props: { items: string[] }) {
  const [selectedIndex, setSelectedIndex] = createSignal(0)

  useKeyboard((key) => {
    const len = props.items.length
    if (key.name === "down" || (key.name === "tab" && !key.shift)) {
      setSelectedIndex(i => Math.min(i + 1, len - 1))
    }
    if (key.name === "up" || (key.name === "tab" && key.shift)) {
      setSelectedIndex(i => Math.max(i - 1, 0))
    }
  })

  return (
    <scrollbox height={20}>
      <For each={props.items}>
        {(item, index) => (
          <box
            backgroundColor={
              index() === selectedIndex()
                ? { r: 100, g: 149, b: 237 }
                : { r: 30, g: 30, b: 30 }
            }
          >
            <text>
              {index() === selectedIndex() ? "> " : "  "}{item}
            </text>
          </box>
        )}
      </For>
    </scrollbox>
  )
}
```

### Show/Hide (Conditional Rendering)

```tsx
function Modal(props: { isOpen: boolean, onClose: () => void }) {
  return (
    <Show when={props.isOpen}>
      <box
        position="absolute"
        backgroundColor={{ r: 0, g: 0, b: 0, a: 0.5 }}
        onClick={props.onClose}
      >
        <text>Modal Content</text>
      </box>
    </Show>
  )
}
```

### Switch (Multiple Conditions)

```tsx
function StatusIndicator(props: { status: "loading" | "success" | "error" }) {
  return (
    <Switch fallback={<text>Unknown status</text>}>
      <Match when={props.status === "loading"}>
        <text>Loading...</text>
      </Match>
      <Match when={props.status === "success"}>
        <text foregroundColor={{ r: 46, g: 204, b: 113 }}>Success!</text>
      </Match>
      <Match when={props.status === "error"}>
        <text foregroundColor={{ r: 231, g: 76, b: 60 }}>Error!</text>
      </Match>
    </Switch>
  )
}
```

### Dynamic Components

```tsx
function DynamicTab(props: { component: () => any }) {
  return (
    <box>
      <Dynamic component={props.component} />
    </box>
  )
}
```

## When to Use This Skill

Use `/opentui-solid` for:
- Building TUIs with SolidJS
- Using signals and fine-grained reactivity
- JSX-style component development
- High-performance reactive UIs
- SolidJS-specific patterns

For vanilla TypeScript/JavaScript, use `/opentui`
For React development, use `/opentui-react`
For project scaffolding, use `/opentui-projects`

## Key SolidJS Differences from React

| Feature | React | SolidJS |
|---------|-------|---------|
| State | `useState` | `createSignal` |
| Effects | `useEffect` | `createEffect` |
| Memos | `useMemo` | `createMemo` |
| Refs | `useRef` | Direct variable assignment |
| Lists | `.map()` | `<For>` component |
| Conditionals | `&&`, `? :` | `<Show>`, `<Switch>` |
| Context | `useContext` | `useContext` (same API) |

## Resources

- [Signals & Reactivity](references/SIGNALS.md) - Deep dive on signals
- [Components](references/COMPONENTS.md) - SolidJS component patterns
- [Performance](references/PERFORMANCE.md) - Optimization techniques
- [Integration](references/INTEGRATION.md) - SolidJS with OpenTUI

## Key Knowledge Sources

- OpenTUI SolidJS GitHub: https://github.com/sst/opentui/tree/main/packages/solid
- SolidJS Docs: https://www.solidjs.com/docs
- Context7: `/sst/opentui` - SolidJS integration queries
- Research: `.search-data/research/opentui/`
