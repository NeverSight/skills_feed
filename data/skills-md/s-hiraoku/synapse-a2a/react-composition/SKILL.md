---
name: react-composition
description: >-
  React component composition patterns for building flexible, maintainable
  UIs. Covers compound components, context-based state, explicit variants,
  and React 19 APIs. Use when designing component APIs, refactoring
  prop-heavy components, or building reusable component libraries.
---

# React Composition

Build flexible component APIs through composition instead of configuration.

## Core Principle

**Composition over configuration.** When a component needs a new behavior, the answer is almost never "add a boolean prop." Instead, compose smaller pieces together.

```tsx
// BAD: Boolean prop explosion
<Modal
  hasHeader
  hasFooter
  hasCloseButton
  isFullScreen
  isDismissable
  hasOverlay
  centerContent
/>

// GOOD: Compose what you need
<Modal>
  <Modal.Header>
    <Modal.Title>Settings</Modal.Title>
    <Modal.Close />
  </Modal.Header>
  <Modal.Body>...</Modal.Body>
  <Modal.Footer>
    <Button onClick={save}>Save</Button>
  </Modal.Footer>
</Modal>
```

## Pattern 1: Compound Components

Share implicit state through context. Each sub-component is independently meaningful.

```tsx
// 1. Define shared context
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}
const TabsContext = createContext<TabsContextValue | null>(null);

function useTabs() {
  const ctx = use(TabsContext); // React 19
  if (!ctx) throw new Error('useTabs must be used within <Tabs>');
  return ctx;
}

// 2. Root component owns the state
function Tabs({ defaultTab, children }: { defaultTab: string; children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext value={{ activeTab, setActiveTab }}>
      <div role="tablist">{children}</div>
    </TabsContext>
  );
}

// 3. Sub-components consume context
function TabTrigger({ value, children }: { value: string; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useTabs();
  return (
    <button
      role="tab"
      aria-selected={activeTab === value}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
}

function TabContent({ value, children }: { value: string; children: React.ReactNode }) {
  const { activeTab } = useTabs();
  if (activeTab !== value) return null;
  return <div role="tabpanel">{children}</div>;
}

// 4. Attach sub-components
Tabs.Trigger = TabTrigger;
Tabs.Content = TabContent;
```

## Pattern 2: Explicit Variants

When components have distinct modes, create explicit variant components instead of boolean switches.

```tsx
// BAD: Boolean modes
<Input bordered />
<Input underlined />
<Input ghost />

// GOOD: Explicit variants
<Input.Bordered placeholder="Name" />
<Input.Underlined placeholder="Name" />
<Input.Ghost placeholder="Name" />

// Implementation: shared base, variant-specific styles
function createInputVariant(className: string) {
  return forwardRef<HTMLInputElement, InputProps>((props, ref) => (
    <InputBase ref={ref} className={cn(className, props.className)} {...props} />
  ));
}

Input.Bordered = createInputVariant('border border-gray-300 rounded-md px-3 py-2');
Input.Underlined = createInputVariant('border-b border-gray-300 px-1 py-2');
Input.Ghost = createInputVariant('bg-transparent px-3 py-2');
```

## Pattern 3: Children Over Render Props

Use `children` for composition. Only use render props when the child needs data from the parent.

```tsx
// BAD: Render prop when children would work
<Card renderHeader={() => <h2>Title</h2>} renderBody={() => <p>Content</p>} />

// GOOD: Children composition
<Card>
  <Card.Header><h2>Title</h2></Card.Header>
  <Card.Body><p>Content</p></Card.Body>
</Card>

// ACCEPTABLE: Render prop when child needs parent data
<Combobox>
  {({ isOpen, selectedItem }) => (
    <>
      <Combobox.Input />
      {isOpen && <Combobox.Options />}
      {selectedItem && <Badge>{selectedItem.label}</Badge>}
    </>
  )}
</Combobox>
```

## Pattern 4: Context Interface Design

Design context interfaces with clear separation of state, actions, and metadata.

```tsx
interface FormContext<T> {
  // State (read-only from consumer perspective)
  values: T;
  errors: Record<string, string>;
  touched: Record<string, boolean>;

  // Actions (stable references)
  setValue: (field: keyof T, value: T[keyof T]) => void;
  setTouched: (field: keyof T) => void;
  validate: () => boolean;
  submit: () => Promise<void>;

  // Metadata
  isSubmitting: boolean;
  isDirty: boolean;
  isValid: boolean;
}
```

### State Lifting

Move state into provider when siblings need access.

```tsx
// BAD: Prop drilling
function Parent() {
  const [selected, setSelected] = useState<string | null>(null);
  return (
    <>
      <Sidebar selected={selected} onSelect={setSelected} />
      <Detail selected={selected} />
    </>
  );
}

// GOOD: Shared context
function Parent() {
  return (
    <SelectionProvider>
      <Sidebar />
      <Detail />
    </SelectionProvider>
  );
}
```

## React 19 APIs

### Drop forwardRef

React 19 passes `ref` as a regular prop.

```tsx
// Before (React 18)
const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => (
  <input ref={ref} {...props} />
));

// After (React 19)
function Input({ ref, ...props }: InputProps & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />;
}
```

### use() Instead of useContext()

```tsx
// Before
const ctx = useContext(ThemeContext);

// After (React 19) — works in conditionals and loops
const ctx = use(ThemeContext);
```

## Decision Guide

| Situation | Pattern |
|-----------|---------|
| Component has 3+ boolean layout props | Compound components |
| Multiple visual modes of same component | Explicit variants |
| Parent data needed in flexible child layout | Render prop |
| Siblings share state | Context provider + state lifting |
| Simple customization of a slot | `children` prop |
| Component needs imperative API | `useImperativeHandle` |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| `<Component isX isY isZ />` | Combinatorial explosion, unclear interactions | Compound components or explicit variants |
| `renderHeader`, `renderFooter` | Couples parent API to child structure | `children` + slot components |
| Deeply nested context providers | Performance + debugging nightmare | Colocate state with consumers, split contexts |
| `React.cloneElement` for injection | Fragile, breaks with wrappers | Context-based composition |
| Single mega-context for all state | Every consumer re-renders on any change | Split into `StateContext` + `ActionsContext` |
