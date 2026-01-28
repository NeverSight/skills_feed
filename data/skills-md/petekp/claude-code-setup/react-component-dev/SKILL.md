---
name: react-component-dev
description: Build React components with proper patterns, accessibility, and composition. Use when creating new components, refactoring existing ones, or reviewing component architecture. Covers forwardRef, prop design, accessibility, file organization, and testing approaches.
---

# React Component Development

Patterns for building composable, accessible, well-structured React components.

## Core Principles

1. **Composition over configuration** - Props enable customization, not enumerate options
2. **Forwarding refs** - Components that render DOM elements forward refs
3. **Accessibility first** - Keyboard, screen readers, reduced motion
4. **Predictable APIs** - Consistent prop patterns across components

## Component Template

```tsx
import { forwardRef, type ComponentPropsWithoutRef } from "react"
import { cn } from "@/lib/utils"

type ButtonProps = ComponentPropsWithoutRef<"button"> & {
  variant?: "default" | "outline" | "ghost"
  size?: "sm" | "md" | "lg"
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "md", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "base-styles",
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, type ButtonProps }
```

## Prop Design

### Always Include

| Prop | Type | Purpose |
|------|------|---------|
| `className` | `string` | Style composition |
| `children` | `ReactNode` | Content (when applicable) |
| `...rest` | native props | Forward all valid HTML attributes |

### Variant Props

```tsx
// Good: Union of literal types
variant?: "default" | "destructive" | "outline"

// Bad: Boolean props that multiply
isPrimary?: boolean
isDestructive?: boolean
isOutline?: boolean
```

### Render Props / Slots

For complex customization:

```tsx
type DialogProps = {
  trigger?: ReactNode
  title: ReactNode
  description?: ReactNode
  children: ReactNode
  footer?: ReactNode
}
```

## forwardRef Patterns

### When to Use

- Component renders a single DOM element
- Component wraps another forwardRef component
- Users might need to call `.focus()`, measure, or attach refs

### When to Skip

- Component renders multiple root elements
- Component is purely logic (hooks)
- Internal-only component never exposed to consumers

### Extracting Ref Type

```tsx
// From DOM element
forwardRef<HTMLDivElement, Props>

// From another component
forwardRef<ComponentRef<typeof OtherComponent>, Props>
```

## File Organization

```
components/
└── button/
    ├── index.ts              # Re-export: export { Button } from "./button"
    ├── button.tsx            # Implementation
    ├── button.test.tsx       # Tests
    └── use-button-state.ts   # Complex state logic (if needed)
```

### index.ts Pattern

```tsx
export { Button, type ButtonProps } from "./button"
```

Keep index.ts as pure re-exports. No logic.

## Accessibility Checklist

### Keyboard

- [ ] All interactive elements focusable
- [ ] Focus order matches visual order
- [ ] Focus visible (outline or ring)
- [ ] Escape closes modals/dropdowns
- [ ] Enter/Space activates buttons
- [ ] Arrow keys for menu navigation

### ARIA

```tsx
// Buttons with icons only
<button aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>

// Loading states
<button disabled aria-busy={isLoading}>
  {isLoading ? <Spinner /> : "Submit"}
</button>

// Expandable content
<button aria-expanded={isOpen} aria-controls="panel-id">
  Toggle
</button>
```

### Reduced Motion

```tsx
const prefersReducedMotion = useMediaQuery("(prefers-reduced-motion: reduce)")

// Or in CSS
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; }
}
```

## State Management

### Local State

Use `useState` for:
- UI state (open/closed, selected)
- Form inputs (controlled)
- Ephemeral data (hover, focus)

### Derived State

```tsx
// Bad: useEffect to sync
const [fullName, setFullName] = useState("")
useEffect(() => {
  setFullName(`${firstName} ${lastName}`)
}, [firstName, lastName])

// Good: useMemo
const fullName = useMemo(
  () => `${firstName} ${lastName}`,
  [firstName, lastName]
)

// Best: Just compute it (if cheap)
const fullName = `${firstName} ${lastName}`
```

### Complex State

```tsx
// useReducer for multi-field updates
const [state, dispatch] = useReducer(reducer, initialState)

// Or extract to custom hook
const dialog = useDialogState()
```

## Event Handlers

### Prop Naming

```tsx
// Internal handler
const handleClick = () => { ... }

// Prop callbacks: on[Event]
type Props = {
  onClick?: () => void
  onOpenChange?: (open: boolean) => void
  onValueChange?: (value: string) => void
}
```

### Composing Handlers

```tsx
const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ onClick, ...props }, ref) => {
    const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
      // Internal logic
      trackClick()
      // Call user's handler
      onClick?.(e)
    }

    return <button ref={ref} onClick={handleClick} {...props} />
  }
)
```

## Testing Approach

### What to Test

- User interactions (click, type, submit)
- Accessibility (keyboard nav, ARIA states)
- Conditional rendering
- Error states

### What NOT to Test

- Implementation details (internal state values)
- Styling (unless critical to function)
- Third-party library internals

### Test Structure

```tsx
describe("Button", () => {
  it("calls onClick when clicked", async () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)

    await userEvent.click(screen.getByRole("button"))

    expect(handleClick).toHaveBeenCalledOnce()
  })

  it("is disabled when disabled prop is true", () => {
    render(<Button disabled>Disabled</Button>)

    expect(screen.getByRole("button")).toBeDisabled()
  })
})
```

## Anti-Patterns

### Prop Drilling

```tsx
// Bad: Passing props through many layers
<Parent value={x} onChange={y}>
  <Child value={x} onChange={y}>
    <GrandChild value={x} onChange={y} />

// Better: Context for deep trees
<ValueContext.Provider value={{ x, onChange: y }}>
  <Parent>
    <Child>
      <GrandChild /> {/* useContext inside */}
```

### Premature Abstraction

```tsx
// Bad: Generic component nobody asked for
<FlexContainer direction="column" gap={4} align="center" justify="between">

// Good: Specific component for the use case
<CardHeader>
```

### Boolean Prop Explosion

```tsx
// Bad
<Button primary large disabled loading>

// Good
<Button variant="primary" size="lg" disabled isLoading>
```

## Quick Reference

| Pattern | When |
|---------|------|
| `forwardRef` | Wrapping DOM elements |
| `ComponentPropsWithoutRef<"tag">` | Inheriting native props |
| `cn()` | Merging classNames |
| `as const` | Literal type inference |
| `useImperativeHandle` | Custom ref APIs (rare) |
| `React.Children` | Manipulating children (avoid if possible) |
