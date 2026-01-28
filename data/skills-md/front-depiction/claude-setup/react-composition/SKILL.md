---
name: react-composition
description: Build composable React components using Effect Atom for state management. Use this skill when implementing React UIs that avoid boolean props, embrace component composition, and integrate with Effect's reactive state system.
---

# React Composition Skill

Build React UIs using compositional patterns, Effect Atom for state management, and the component module pattern. Use this skill when creating React applications that integrate with Effect's ecosystem.

## When to Use This Skill

- Building React components that integrate with Effect Atom state
- Refactoring components away from boolean prop anti-patterns
- Implementing complex UIs through composition of simple pieces
- Creating reusable component libraries with flexible APIs
- Managing shared state across multiple React components
- Lifting state to appropriate levels in component trees

## Core Principles

### 1. Composition over Configuration

Build complex UIs from simple, composable pieces rather than configuring behavior through props.

**Anti-Pattern: Boolean Props**

```tsx
// L WRONG - Configuration through boolean props
interface FormProps {
  isUpdate?: boolean
  hideWelcome?: boolean
  showEmail?: boolean
  redirectOnSuccess?: boolean
  enableValidation?: boolean
}

function UserForm({
  isUpdate,
  hideWelcome,
  showEmail,
  redirectOnSuccess,
  enableValidation
}: FormProps) {
  return (
    <form>
      {!hideWelcome && <WelcomeMessage />}
      <NameField />
      {showEmail && <EmailField />}
      <button type="submit">
        {isUpdate ? "Update" : "Create"}
      </button>
    </form>
  )
}

// Usage becomes unreadable
<UserForm
  isUpdate
  hideWelcome
  showEmail
  redirectOnSuccess
/>
```

**Correct Pattern: Composition**

```tsx
//  CORRECT - Compose specific forms from atomic pieces
export namespace UserForm {
  export const Frame: React.FC<{ children: React.ReactNode }> =
    ({ children }) => <form className="user-form">{children}</form>

  export const WelcomeMessage: React.FC = () =>
    <div className="welcome">Welcome!</div>

  export const NameField: React.FC = () =>
    <input name="name" placeholder="Name" />

  export const EmailField: React.FC = () =>
    <input type="email" name="email" placeholder="Email" />

  export const SubmitButton: React.FC<{ children: React.ReactNode }> =
    ({ children }) => <button type="submit">{children}</button>
}

// Create specific forms through composition
function CreateUserForm() {
  return (
    <UserForm.Frame>
      <UserForm.WelcomeMessage />
      <UserForm.NameField />
      <UserForm.EmailField />
      <UserForm.SubmitButton>Create</UserForm.SubmitButton>
    </UserForm.Frame>
  )
}

function UpdateUserForm() {
  return (
    <UserForm.Frame>
      <UserForm.NameField />
      <UserForm.SubmitButton>Update</UserForm.SubmitButton>
    </UserForm.Frame>
  )
}

// Usage is clear and explicit (in JSX context):
// <CreateUserForm />
// <UpdateUserForm />
```

### 2. Component Module Pattern

Treat components like Effect modules with namespace imports and exported sub-components.

```tsx
// components/Composer/Composer.tsx
import * as React from "react"

/**
 * Composer state interface
 */
export interface ComposerState {
  readonly content: string
  readonly attachments: ReadonlyArray<Attachment>
  readonly isSubmitting: boolean
}

/**
 * Composer context for sharing state
 */
const ComposerContext = React.createContext<ComposerState | null>(null)

/**
 * Hook to access composer state
 * @throws when used outside Provider
 */
export const useComposer = (): ComposerState => {
  const context = React.useContext(ComposerContext)
  if (!context) {
    throw new Error("useComposer must be used within Composer.Provider")
  }
  return context
}

/**
 * Provider component for composer state
 */
export const Provider: React.FC<{
  children: React.ReactNode
  state: ComposerState
}> = ({ children, state }) => (
  <ComposerContext.Provider value={state}>
    {children}
  </ComposerContext.Provider>
)

/**
 * Frame component for layout
 */
export const Frame: React.FC<{
  children: React.ReactNode
}> = ({ children }) => (
  <div className="composer-frame">
    {children}
  </div>
)

/**
 * Input component for message content
 */
export const Input: React.FC = () => {
  const { content } = useComposer()
  return (
    <textarea
      value={content}
      className="composer-input"
      placeholder="Type a message..."
    />
  )
}

/**
 * Footer component for actions
 */
export const Footer: React.FC<{
  children: React.ReactNode
}> = ({ children }) => (
  <div className="composer-footer">
    {children}
  </div>
)

/**
 * Submit button component
 */
export const Submit: React.FC = () => {
  const { isSubmitting } = useComposer()
  return (
    <button
      type="submit"
      disabled={isSubmitting}
      className="composer-submit"
    >
      {isSubmitting ? "Sending..." : "Send"}
    </button>
  )
}
```

**Usage with Namespace Import**

```tsx
import * as Composer from "@/components/Composer"

function MessageComposer() {
  const [state, setState] = useState<Composer.ComposerState>({
    content: "",
    attachments: [],
    isSubmitting: false
  })

  return (
    <Composer.Provider state={state}>
      <Composer.Frame>
        <Composer.Input />
        <Composer.Footer>
          <Composer.Submit />
        </Composer.Footer>
      </Composer.Frame>
    </Composer.Provider>
  )
}
```

### 3. State Lifting Pattern

Lift state ABOVE all components that need access, not below.

**Anti-Pattern: State Too Low**

```tsx
// L WRONG - State below components that need it
function Modal() {
  return (
    <ModalFrame>
      <ModalContent>
        <Composer />  {/* State is here */}
      </ModalContent>
      <ModalFooter>
        <ExternalButton />  {/* Cannot access Composer state! */}
      </ModalFooter>
    </ModalFrame>
  )
}
```

**Correct Pattern: Lift State Above**

```tsx
//  CORRECT - State above everything that needs it
function Modal() {
  const [state, setState] = useState(initialComposerState)

  // Provider wraps EVERYTHING that needs access
  return (
    <Composer.Provider state={state}>
      <ModalFrame>
        <ModalContent>
          <Composer.Input />
        </ModalContent>
        <ModalFooter>
          <ExternalButton />  {/* Can access state via useComposer! */}
          <Composer.Submit />
        </ModalFooter>
      </ModalFrame>
    </Composer.Provider>
  )
}

function ExternalButton() {
  const { content } = Composer.useComposer()
  const hasContent = content.length > 0

  return (
    <button disabled={!hasContent}>
      Preview
    </button>
  )
}
```

## Effect Atom Integration

Effect Atom provides reactive state management that integrates seamlessly with React.

### Pattern: Basic Atom State

```typescript
// state/Cart.ts
import * as Atom from "@effect-atom/atom-react"
import { Effect } from "effect"

/**
 * Cart item interface
 */
export interface CartItem {
  readonly id: string
  readonly name: string
  readonly price: number
  readonly quantity: number
}

/**
 * Cart state interface
 */
export interface CartState {
  readonly items: ReadonlyArray<CartItem>
  readonly total: number
}

/**
 * Main cart atom
 */
export const cart = Atom.make<CartState>({
  items: [],
  total: 0
})

/**
 * Derived atom: item count
 */
export const itemCount = Atom.map(cart, (c) => c.items.length)

/**
 * Derived atom: is cart empty
 */
export const isEmpty = Atom.map(cart, (c) => c.items.length === 0)

/**
 * Add item to cart
 */
export const addItem = Atom.fn(
  Effect.fnUntraced(function* (item: CartItem) {
    const current = yield* Atom.get(cart)

    const existingIndex = current.items.findIndex(i => i.id === item.id)

    if (existingIndex >= 0) {
      // Update quantity
      const updatedItems = [...current.items]
      updatedItems[existingIndex] = {
        ...updatedItems[existingIndex],
        quantity: updatedItems[existingIndex].quantity + item.quantity
      }

      yield* Atom.set(cart, {
        items: updatedItems,
        total: current.total + (item.price * item.quantity)
      })
    } else {
      // Add new item
      yield* Atom.set(cart, {
        items: [...current.items, item],
        total: current.total + (item.price * item.quantity)
      })
    }
  })
)

/**
 * Remove item from cart
 */
export const removeItem = Atom.fn(
  Effect.fnUntraced(function* (itemId: string) {
    const current = yield* Atom.get(cart)
    const item = current.items.find(i => i.id === itemId)

    if (!item) return

    yield* Atom.set(cart, {
      items: current.items.filter(i => i.id !== itemId),
      total: current.total - (item.price * item.quantity)
    })
  })
)

/**
 * Clear cart
 */
export const clearCart = Atom.fn(
  Effect.fnUntraced(function* () {
    yield* Atom.set(cart, { items: [], total: 0 })
  })
)
```

### Pattern: React Component with Atoms

```tsx
// components/Cart/CartView.tsx
import { useAtomValue, useAtomSet } from "@effect-atom/atom-react"
import * as Cart from "@/state/Cart"

/**
 * Cart display component
 */
export function CartView() {
  const cartData = useAtomValue(Cart.cart)
  const count = useAtomValue(Cart.itemCount)
  const empty = useAtomValue(Cart.isEmpty)
  const removeItem = useAtomSet(Cart.removeItem)
  const clearCart = useAtomSet(Cart.clearCart)

  if (empty) {
    return <div className="cart-empty">Your cart is empty</div>
  }

  return (
    <div className="cart">
      <h2>Cart ({count} items)</h2>

      <ul className="cart-items">
        {cartData.items.map(item => (
          <li key={item.id} className="cart-item">
            <span>{item.name}</span>
            <span>{item.quantity} x ${item.price}</span>
            <button onClick={() => removeItem(item.id)}>
              Remove
            </button>
          </li>
        ))}
      </ul>

      <div className="cart-total">
        Total: ${cartData.total}
      </div>

      <button onClick={() => clearCart()}>
        Clear Cart
      </button>
    </div>
  )
}
```

### Pattern: Separation of Concerns

Different components can read/write the same atom reactively:

```tsx
// Component A - Read only
function CartBadge() {
  const count = useAtomValue(Cart.itemCount)

  return (
    <div className="cart-badge">
      {count > 0 && <span>{count}</span>}
    </div>
  )
}

// Component B - Write only
function AddToCartButton({ item }: { item: CartItem }) {
  const addItem = useAtomSet(Cart.addItem)

  return (
    <button onClick={() => addItem(item)}>
      Add to Cart
    </button>
  )
}

// Component C - Read and write
function CartControls() {
  const [cartState, setCart] = useAtom(Cart.cart)

  return (
    <div>
      <span>Items: {cartState.items.length}</span>
      <button onClick={() => setCart({ items: [], total: 0 })}>
        Reset
      </button>
    </div>
  )
}

// All components update reactively when atom changes
```

### Pattern: Async Operations with Atoms

```typescript
// state/User.ts
import * as Atom from "@effect-atom/atom-react"
import * as Result from "@effect-atom/atom/Result"
import { Effect, Layer } from "effect"
import type { UserService } from "@/services/UserService"

/**
 * User data with Result type for error handling
 */
export const userData = Atom.make<Result.Result<User, Error>>(
  Result.initial
)

/**
 * Runtime with UserService
 */
const runtime = Atom.runtime(UserService.Live)

/**
 * Load user data
 */
export const loadUser = runtime.fn(
  Effect.fnUntraced(function* (userId: string) {
    const userService = yield* UserService

    // Set loading state
    yield* Atom.set(userData, Result.initial)

    // Fetch data
    const result = yield* Effect.either(
      userService.getUser(userId)
    )

    // Update atom with result
    yield* Atom.set(
      userData,
      result._tag === "Right"
        ? Result.success(result.right)
        : Result.failure(result.left)
    )
  })
)
```

**Component with Result Handling**

```tsx
import { useAtomValue, useAtomSetPromise } from "@effect-atom/atom-react"
import * as Result from "@effect-atom/atom/Result"
import * as User from "@/state/User"

function UserProfile({ userId }: { userId: string }) {
  const result = useAtomValue(User.userData)
  const loadUser = useAtomSetPromise(User.loadUser)

  React.useEffect(() => {
    loadUser(userId)
  }, [userId, loadUser])

  return Result.match(result, {
    Initial: () => <Loading />,
    Failure: (error) => <Error message={error.message} />,
    Success: (user) => (
      <div className="user-profile">
        <h2>{user.name}</h2>
        <p>{user.email}</p>
      </div>
    )
  })
}
```

## Avoiding useEffect

Most `useEffect` usage is wrong. Consider these alternatives:

### Anti-Pattern: Unnecessary Effects

```tsx
// L WRONG - Using effect for derived state
function UserCard({ user }: { user: User }) {
  const [fullName, setFullName] = useState("")

  useEffect(() => {
    setFullName(`${user.firstName} ${user.lastName}`)
  }, [user])

  return <div>{fullName}</div>
}

//  CORRECT - Calculate during render
function UserCard({ user }: { user: User }) {
  const fullName = `${user.firstName} ${user.lastName}`
  return <div>{fullName}</div>
}
```

### Anti-Pattern: Effect for Expensive Computation

```tsx
// L WRONG - Effect for memoization
function ProductList({ products }: { products: Product[] }) {
  const [filtered, setFiltered] = useState<Product[]>([])

  useEffect(() => {
    setFiltered(products.filter(expensiveFilter))
  }, [products])

  return <div>{filtered.map(renderProduct)}</div>
}

//  CORRECT - useMemo for expensive computation
function ProductList({ products }: { products: Product[] }) {
  const filtered = useMemo(
    () => products.filter(expensiveFilter),
    [products]
  )

  return <div>{filtered.map(renderProduct)}</div>
}
```

### Pattern: useTransition for Non-Blocking Updates

```tsx
import { useTransition } from "react"

function SearchResults() {
  const [query, setQuery] = useState("")
  const [isPending, startTransition] = useTransition()

  const handleSearch = (value: string) => {
    setQuery(value)  // Immediate update

    // Non-blocking update for expensive operation
    startTransition(() => {
      // Expensive filter/sort operation
      updateSearchResults(value)
    })
  }

  return (
    <div>
      <input onChange={e => handleSearch(e.target.value)} />
      {isPending && <LoadingSpinner />}
      <Results />
    </div>
  )
}
```

### Pattern: Keys for Resetting State

```tsx
// L WRONG - Effect to reset state
function UserEditor({ userId }: { userId: string }) {
  const [formData, setFormData] = useState(initialData)

  useEffect(() => {
    setFormData(initialData)  // Reset on user change
  }, [userId])

  return <form>...</form>
}

//  CORRECT - Use key to reset component
function UserEditor({ userId }: { userId: string }) {
  return <UserEditorForm key={userId} />
}

function UserEditorForm() {
  const [formData, setFormData] = useState(initialData)
  // State automatically resets when key changes

  return <form>...</form>
}
```

### When useEffect is Appropriate

Use `useEffect` for:
- Synchronizing with external systems (WebSocket, DOM APIs)
- Side effects that must run after render
- Cleanup of subscriptions

```tsx
function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    // Connect to external system
    const connection = connectToRoom(roomId)

    // Cleanup on unmount or roomId change
    return () => {
      connection.disconnect()
    }
  }, [roomId])

  return <div>...</div>
}
```

## Advanced Patterns

### Pattern: Render Props for Flexibility

```tsx
export namespace DataTable {
  export interface RenderProps<T> {
    readonly data: ReadonlyArray<T>
    readonly isLoading: boolean
  }

  export const Frame: React.FC<{
    children: React.ReactNode
  }> = ({ children }) => (
    <div className="data-table">{children}</div>
  )

  export const Header: React.FC<{
    columns: ReadonlyArray<string>
  }> = ({ columns }) => (
    <thead>
      <tr>
        {columns.map(col => <th key={col}>{col}</th>)}
      </tr>
    </thead>
  )

  export const Body: React.FC<{
    children: (props: RenderProps<T>) => React.ReactNode
  }> = ({ children, data, isLoading }) => (
    <tbody>
      {children({ data, isLoading })}
    </tbody>
  )
}

// Usage
function UserTable() {
  const users = useAtomValue(User.list)

  return (
    <DataTable.Frame>
      <DataTable.Header columns={["Name", "Email"]} />
      <DataTable.Body>
        {({ data, isLoading }) =>
          isLoading ? (
            <LoadingRow />
          ) : (
            data.map(user => <UserRow key={user.id} user={user} />)
          )
        }
      </DataTable.Body>
    </DataTable.Frame>
  )
}
```

### Pattern: Compound Components with Context

```tsx
export namespace Tabs {
  interface TabsContext {
    readonly activeTab: string
    readonly setActiveTab: (tab: string) => void
  }

  const Context = React.createContext<TabsContext | null>(null)

  export const Provider: React.FC<{
    children: React.ReactNode
    defaultTab: string
  }> = ({ children, defaultTab }) => {
    const [activeTab, setActiveTab] = useState(defaultTab)

    return (
      <Context.Provider value={{ activeTab, setActiveTab }}>
        {children}
      </Context.Provider>
    )
  }

  export const List: React.FC<{
    children: React.ReactNode
  }> = ({ children }) => (
    <div role="tablist">{children}</div>
  )

  export const Tab: React.FC<{
    id: string
    children: React.ReactNode
  }> = ({ id, children }) => {
    const context = React.useContext(Context)
    if (!context) throw new Error("Tab must be within Provider")

    const isActive = context.activeTab === id

    return (
      <button
        role="tab"
        aria-selected={isActive}
        onClick={() => context.setActiveTab(id)}
      >
        {children}
      </button>
    )
  }

  export const Panel: React.FC<{
    id: string
    children: React.ReactNode
  }> = ({ id, children }) => {
    const context = React.useContext(Context)
    if (!context) throw new Error("Panel must be within Provider")

    if (context.activeTab !== id) return null

    return (
      <div role="tabpanel">{children}</div>
    )
  }
}

// Usage
function Settings() {
  return (
    <Tabs.Provider defaultTab="general">
      <Tabs.List>
        <Tabs.Tab id="general">General</Tabs.Tab>
        <Tabs.Tab id="security">Security</Tabs.Tab>
        <Tabs.Tab id="notifications">Notifications</Tabs.Tab>
      </Tabs.List>

      <Tabs.Panel id="general">
        <GeneralSettings />
      </Tabs.Panel>
      <Tabs.Panel id="security">
        <SecuritySettings />
      </Tabs.Panel>
      <Tabs.Panel id="notifications">
        <NotificationSettings />
      </Tabs.Panel>
    </Tabs.Provider>
  )
}
```

## Testing Compositional Components

### Pattern: Test Atomic Components

```tsx
import { render, screen } from "@testing-library/react"
import * as Composer from "@/components/Composer"

describe("Composer.Input", () => {
  it("displays content from context", () => {
    const state: Composer.ComposerState = {
      content: "Hello world",
      attachments: [],
      isSubmitting: false
    }

    render(
      <Composer.Provider state={state}>
        <Composer.Input />
      </Composer.Provider>
    )

    expect(screen.getByDisplayValue("Hello world")).toBeInTheDocument()
  })
})
```

### Pattern: Test Composed Features

```tsx
describe("MessageComposer", () => {
  it("composes correctly", () => {
    render(<MessageComposer />)

    expect(screen.getByRole("textbox")).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "Send" })).toBeInTheDocument()
  })

  it("disables submit when submitting", () => {
    const state: Composer.ComposerState = {
      content: "Hello",
      attachments: [],
      isSubmitting: true
    }

    render(
      <Composer.Provider state={state}>
        <Composer.Submit />
      </Composer.Provider>
    )

    expect(screen.getByRole("button")).toBeDisabled()
  })
})
```

## Quality Checklist

When implementing React components with Effect Atom, ensure:

- [ ] No boolean props - use composition instead
- [ ] Components organized in namespaces with namespace imports
- [ ] State lifted to appropriate level (above all components that need it)
- [ ] Atomic components compose into features
- [ ] Effect Atom used for shared/complex state
- [ ] Avoid unnecessary `useEffect` - prefer direct calculation, `useMemo`, or `useTransition`
- [ ] Result types used for async operations with explicit error handling
- [ ] Context only for component-specific state, Atoms for app-wide state
- [ ] All exports documented with JSDoc
- [ ] Components testable in isolation
- [ ] Render props or compound components for maximum flexibility

## Common Mistakes

### Mistake: Mixing Context and Atoms

```tsx
// L WRONG - Using Context for app-wide state
const AppContext = React.createContext<AppState | null>(null)

function App() {
  const [state, setState] = useState(appState)
  return (
    <AppContext.Provider value={state}>
      {/* Deep component tree */}
    </AppContext.Provider>
  )
}

//  CORRECT - Use Atoms for app-wide state
// state/App.ts
export const appState = Atom.make<AppState>(initialState)

// Components access directly
function DeepComponent() {
  const state = useAtomValue(appState)
  return <div>{state.value}</div>
}
```

### Mistake: Not Lifting State High Enough

```tsx
// L WRONG - State trapped in Modal
function Modal() {
  return (
    <div className="modal">
      <Editor />  {/* State is here */}
      <Footer>
        <SaveButton />  {/* Cannot access Editor state */}
      </Footer>
    </div>
  )
}

//  CORRECT - Lift state above Modal
function ModalContainer() {
  const editorState = useAtomValue(Editor.state)

  return (
    <Editor.Provider state={editorState}>
      <Modal>
        <Editor.Input />
        <Footer>
          <SaveButton />  {/* Can access state */}
        </Footer>
      </Modal>
    </Editor.Provider>
  )
}
```

### Mistake: Overusing useEffect

```tsx
// L WRONG - Effect for derived data
function OrderSummary({ order }: { order: Order }) {
  const [total, setTotal] = useState(0)

  useEffect(() => {
    setTotal(order.items.reduce((sum, item) => sum + item.price, 0))
  }, [order])

  return <div>Total: ${total}</div>
}

//  CORRECT - Calculate during render
function OrderSummary({ order }: { order: Order }) {
  const total = order.items.reduce((sum, item) => sum + item.price, 0)
  return <div>Total: ${total}</div>
}
```

## Summary

Build React applications that:
- **Compose** simple components into complex features
- **Avoid** configuration through boolean props
- **Lift** state to appropriate levels
- **Use** Effect Atom for reactive state management
- **Organize** components in namespaces like Effect modules
- **Minimize** `useEffect` usage in favor of direct calculation
- **Handle** errors explicitly with Result types
- **Test** components in isolation

This approach creates flexible, maintainable UIs that integrate seamlessly with Effect's ecosystem while following React best practices.
