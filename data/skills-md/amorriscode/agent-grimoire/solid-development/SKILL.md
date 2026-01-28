---
name: solid-development
description: SolidJS patterns, reactivity model, and best practices. Use when writing Solid components, reviewing Solid code, or debugging Solid issues.
---

# Solid Development

Fine-grained reactivity patterns for SolidJS.

## Instructions

SolidJS is NOT React. The mental model is fundamentally different:

| React | SolidJS |
|-------|---------|
| Components re-run on state change | Components run **once** |
| Virtual DOM diffing | Direct DOM updates |
| Hooks with dependency arrays | Automatic dependency tracking |
| `useState` returns value | `createSignal` returns getter function |

### 1. Signals — Reactive Primitives

Signals are getter/setter pairs that track dependencies automatically:

```jsx
import { createSignal } from "solid-js";

function Counter() {
  const [count, setCount] = createSignal(0);
  //     ^ getter (function!)  ^ setter

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count()}  {/* Call the getter! */}
    </button>
  );
}
```

**Rules:**
- Always call the getter: `count()` not `count`
- The component function runs once — only the reactive parts update
- Signals accessed in JSX are automatically tracked

### 2. Effects — Side Effects

Effects run when their tracked signals change:

```jsx
import { createSignal, createEffect } from "solid-js";

function Logger() {
  const [count, setCount] = createSignal(0);

  // ✅ Tracked — runs when count changes
  createEffect(() => {
    console.log("Count is:", count());
  });

  // ❌ NOT tracked — runs once at setup
  console.log("Initial:", count());

  return <button onClick={() => setCount(c => c + 1)}>Increment</button>;
}
```

**Key insight:** Only signals accessed *inside* the effect are tracked.

### 3. Memos — Derived Values

Cache expensive computations:

```jsx
import { createSignal, createMemo } from "solid-js";

function FilteredList() {
  const [items, setItems] = createSignal([]);
  const [filter, setFilter] = createSignal("");

  // Only recomputes when items or filter change
  const filtered = createMemo(() =>
    items().filter(item => item.includes(filter()))
  );

  return <For each={filtered()}>{item => <div>{item}</div>}</For>;
}
```

### 4. Props — Don't Destructure!

**Critical:** Destructuring props breaks reactivity.

```jsx
// ❌ BROKEN — loses reactivity
function Greeting({ name }) {
  return <h1>Hello {name}</h1>;
}

// ❌ ALSO BROKEN
function Greeting(props) {
  const { name } = props;
  return <h1>Hello {name}</h1>;
}

// ✅ CORRECT — maintains reactivity
function Greeting(props) {
  return <h1>Hello {props.name}</h1>;
}
```

**For defaults, use `mergeProps`:**
```jsx
import { mergeProps } from "solid-js";

function Button(props) {
  const merged = mergeProps({ variant: "primary" }, props);
  return <button class={merged.variant}>{merged.children}</button>;
}
```

**For splitting props, use `splitProps`:**
```jsx
import { splitProps } from "solid-js";

function Input(props) {
  const [local, inputProps] = splitProps(props, ["label"]);
  return (
    <label>
      {local.label}
      <input {...inputProps} />
    </label>
  );
}
```

### 5. Control Flow Components

Don't use JS control flow in JSX — use Solid's components:

**Conditionals with `<Show>`:**
```jsx
import { Show } from "solid-js";

<Show when={isLoggedIn()} fallback={<Login />}>
  <Dashboard />
</Show>
```

**Multiple conditions with `<Switch>`/`<Match>`:**
```jsx
import { Switch, Match } from "solid-js";

<Switch>
  <Match when={status() === "loading"}>Loading...</Match>
  <Match when={status() === "error"}>Error!</Match>
  <Match when={status() === "success"}><Data /></Match>
</Switch>
```

**Lists with `<For>`:**
```jsx
import { For } from "solid-js";

<For each={items()}>
  {(item, index) => <li>{index()}: {item.name}</li>}
</For>
```

**`<For>` vs `<Index>`:**
| Use | When |
|-----|------|
| `<For>` | List order/length changes (general case) |
| `<Index>` | Fixed positions, content changes (performance optimization) |

With `<Index>`, `item` is a signal: `{(item, i) => <div>{item().name}</div>}`

### 6. Stores — Complex State

Use stores for nested objects and shared state:

```jsx
import { createStore } from "solid-js/store";

function TodoApp() {
  const [state, setState] = createStore({
    todos: [],
    filter: "all"
  });

  const addTodo = (text) => {
    setState("todos", todos => [...todos, { text, done: false }]);
  };

  const toggleTodo = (index) => {
    setState("todos", index, "done", done => !done);
  };

  return (/* ... */);
}
```

**When to use:**
- Signals: Simple values, local state
- Stores: Objects, arrays, shared state, nested data

### 7. Data Fetching with Resources

```jsx
import { createResource, Suspense } from "solid-js";

function UserProfile(props) {
  const [user] = createResource(() => props.userId, fetchUser);

  return (
    <Suspense fallback={<Loading />}>
      <Show when={user()} fallback={<NotFound />}>
        <Profile user={user()} />
      </Show>
    </Suspense>
  );
}
```

**Resource properties:**
- `user()` — the data (or undefined)
- `user.loading` — boolean
- `user.error` — error if failed
- `user.latest` — last successful value

### 8. Context for Shared State

```jsx
import { createContext, useContext } from "solid-js";
import { createStore } from "solid-js/store";

const AppContext = createContext();

function AppProvider(props) {
  const [state, setState] = createStore({ user: null, theme: "light" });
  return (
    <AppContext.Provider value={[state, setState]}>
      {props.children}
    </AppContext.Provider>
  );
}

function useApp() {
  return useContext(AppContext);
}
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `const { name } = props` | Breaks reactivity | Access `props.name` directly |
| `count` instead of `count()` | Gets function, not value | Call the signal getter |
| `console.log(count())` outside effect | Only runs once | Put in `createEffect` |
| Using `.map()` for lists | No keyed updates | Use `<For>` component |
| Ternary in JSX for conditionals | Works but less efficient | Use `<Show>` component |
| Multiple signals for related data | Verbose, hard to manage | Use `createStore` |

## Examples

### Complete Component Pattern

```jsx
import { createSignal, createMemo, createEffect, Show, For } from "solid-js";

function TaskList(props) {
  const [filter, setFilter] = createSignal("all");

  // Derived state
  const filteredTasks = createMemo(() => {
    const f = filter();
    if (f === "all") return props.tasks;
    return props.tasks.filter(t => (f === "done" ? t.done : !t.done));
  });

  // Side effect
  createEffect(() => {
    console.log(`Showing ${filteredTasks().length} tasks`);
  });

  return (
    <div>
      <select onChange={e => setFilter(e.target.value)}>
        <option value="all">All</option>
        <option value="done">Done</option>
        <option value="pending">Pending</option>
      </select>

      <Show when={filteredTasks().length > 0} fallback={<p>No tasks</p>}>
        <ul>
          <For each={filteredTasks()}>
            {task => (
              <li classList={{ done: task.done }}>
                {task.text}
              </li>
            )}
          </For>
        </ul>
      </Show>
    </div>
  );
}
```
