---
name: xstate-react
description: This skill should be used when the user asks to "create a state machine", "add xState", "use xState with React", "implement actor-based state", "manage complex state with state machines", "use xState with Effect", "integrate Effect-ts with xState", mentions xState hooks (useMachine, useActor, useSelector), or discusses finite state machines in React applications.
---

# xState React

## Your Role

You are an expert in xState v5 actor-based state management with React and TypeScript. You understand state machines,
statecharts, the actor model, and React integration patterns for managing complex application logic.

## Overview

xState is an actor-based state management and orchestration solution for JavaScript and TypeScript applications. It uses
event-driven programming, state machines, statecharts, and the actor model to handle complex logic in predictable,
robust, and visual ways.

**When to use xState:**

- Complex UI flows (multi-step forms, wizards, checkout processes)
- State with many transitions and edge cases
- Logic that needs to be visualized and validated
- Processes with async operations and error handling
- State that can be in multiple "modes" (loading, error, success, idle)

**When to use simpler state instead (useState, Zustand):**

- Simple UI toggles and counters
- Form state confined to a single component
- State without complex transition logic
- CRUD operations with straightforward loading states

## Quick Start

Create a state machine and use it in a React component:

```typescript
"use client";

import { createMachine } from "xstate";
import { useMachine } from "@xstate/react";

const toggleMachine = createMachine({
  id: "toggle",
  initial: "inactive",
  states: {
    inactive: {
      on: { TOGGLE: "active" }
    },
    active: {
      on: { TOGGLE: "inactive" }
    }
  }
});

function Toggle() {
  const [state, send] = useMachine(toggleMachine);

  return (
    <button onClick={() => send({ type: "TOGGLE" })}>
      {state.value === "inactive" ? "Off" : "On"}
    </button>
  );
}
```

## React Hooks API

### `useMachine`

Create and run a machine within a component's lifecycle:

```typescript
import { useMachine } from "@xstate/react";
import { someMachine } from "./machines/someMachine";

function Component() {
  const [state, send, actorRef] = useMachine(someMachine, {
    input: { userId: "123" } // Optional input
  });

  return (
    <div>
      <p>Current state: {JSON.stringify(state.value)}</p>
      <p>Context: {JSON.stringify(state.context)}</p>
      <button onClick={() => send({ type: "SOME_EVENT" })}>Send</button>
    </div>
  );
}
```

### `useActor`

Subscribe to an existing actor (created outside the component):

```typescript
import { createActor } from "xstate";
import { useActor } from "@xstate/react";
import { todoMachine } from "./machines/todoMachine";

// Create actor outside component (e.g., in a module or context)
const todoActor = createActor(todoMachine);
todoActor.start();

function TodoApp() {
  const [state, send] = useActor(todoActor);

  return (
    <ul>
      {state.context.todos.map((todo) => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

### `useSelector`

Optimize re-renders by selecting specific state:

```typescript
import { useSelector } from "@xstate/react";

function TodoCount({ actorRef }) {
  // Only re-renders when todos.length changes
  const count = useSelector(actorRef, (state) => state.context.todos.length);

  return <span>{count} todos</span>;
}

function IsLoading({ actorRef }) {
  // Only re-renders when loading state changes
  const isLoading = useSelector(actorRef, (state) => state.matches("loading"));

  return isLoading ? <Spinner /> : null;
}
```

## TypeScript Patterns

### Typing Machines with `types`

Define context and events using the `types` property:

```typescript
import { createMachine, assign } from "xstate";

type FormContext = {
  name: string;
  email: string;
  errors: string[];
};

type FormEvent =
  | { type: "UPDATE_NAME"; value: string }
  | { type: "UPDATE_EMAIL"; value: string }
  | { type: "SUBMIT" }
  | { type: "RESET" };

const formMachine = createMachine({
  types: {} as {
    context: FormContext;
    events: FormEvent;
  },
  id: "form",
  initial: "editing",
  context: {
    name: "",
    email: "",
    errors: []
  },
  states: {
    editing: {
      on: {
        UPDATE_NAME: {
          actions: assign({
            name: ({ event }) => event.value
          })
        },
        UPDATE_EMAIL: {
          actions: assign({
            email: ({ event }) => event.value
          })
        },
        SUBMIT: "submitting"
      }
    },
    submitting: {
      // ...
    }
  }
});
```

### Using `setup()` for Reusable Definitions

Define actions, guards, actors, and delays in a type-safe way:

```typescript
import { setup, assign } from "xstate";

type AuthContext = {
  userId: string | null;
  retries: number;
};

type AuthEvent =
  | { type: "LOGIN"; username: string; password: string }
  | { type: "LOGOUT" }
  | { type: "SUCCESS"; userId: string }
  | { type: "FAILURE" };

const authMachine = setup({
  types: {} as {
    context: AuthContext;
    events: AuthEvent;
  },
  actions: {
    setUser: assign({
      userId: ({ event }) => (event as { userId: string }).userId
    }),
    clearUser: assign({
      userId: null,
      retries: 0
    }),
    incrementRetries: assign({
      retries: ({ context }) => context.retries + 1
    })
  },
  guards: {
    hasReachedMaxRetries: ({ context }) => context.retries >= 3,
    isAuthenticated: ({ context }) => context.userId !== null
  }
}).createMachine({
  id: "auth",
  initial: "loggedOut",
  context: { userId: null, retries: 0 },
  states: {
    loggedOut: {
      on: {
        LOGIN: "authenticating"
      }
    },
    authenticating: {
      on: {
        SUCCESS: {
          target: "loggedIn",
          actions: "setUser"
        },
        FAILURE: [
          {
            guard: "hasReachedMaxRetries",
            target: "loggedOut",
            actions: "clearUser"
          },
          {
            actions: "incrementRetries"
          }
        ]
      }
    },
    loggedIn: {
      on: {
        LOGOUT: {
          target: "loggedOut",
          actions: "clearUser"
        }
      }
    }
  }
});
```

## Core Concepts

### States and Transitions

States represent the possible modes of your system. Transitions define how events move between states:

```typescript
const machine = createMachine({
  initial: "idle",
  states: {
    idle: {
      on: { FETCH: "loading" }
    },
    loading: {
      on: {
        SUCCESS: "success",
        ERROR: "error"
      }
    },
    success: { type: "final" },
    error: {
      on: { RETRY: "loading" }
    }
  }
});
```

### Context

Context holds extended state data:

```typescript
const machine = createMachine({
  context: {
    count: 0,
    user: null
  },
  // ...
});

// Access in component
const count = state.context.count;
```

### Actions

Actions are fire-and-forget side effects:

```typescript
import { assign } from "xstate";

const machine = createMachine({
  // ...
  states: {
    active: {
      entry: assign({ count: ({ context }) => context.count + 1 }),
      exit: () => console.log("Leaving active state")
    }
  }
});
```

## Best Practices

### DO

- Use `setup()` for type-safe action and guard definitions
- Use `useSelector` for optimized state selection
- Define explicit types for context and events
- Use `state.matches()` for hierarchical state checking
- Keep machines pure and side-effect-free (use actions for effects)

### DON'T

- Don't store the entire snapshot object in React state
- Don't mutate context directly (use `assign`)
- Don't use xState for simple toggle/counter state
- Don't forget to handle all possible states in your UI

## Client Component Requirement

xState hooks must be used in Client Components. Add the `"use client"` directive:

```typescript
"use client";

import { useMachine } from "@xstate/react";
```

## Additional Documentation

For comprehensive xState documentation including advanced patterns, use the Context7 MCP:

```
Use Context7 MCP with library ID "/statelyai/xstate" to fetch:
- Detailed invoke/spawn patterns
- Parallel and history states
- Actor communication
- Testing strategies
```

**See `./references/PATTERNS.md`** for common patterns including async operations, guards, parallel states, and
persistence.

**See `./references/EFFECT_TS_INTEGRATION.md`** for integrating Effect-ts with xState for composable, type-safe side
effects.

## Quick Reference

| Task                 | Pattern                                              |
| -------------------- | ---------------------------------------------------- |
| **Create machine**   | `createMachine({ id, initial, states, context })`    |
| **Use in component** | `const [state, send] = useMachine(machine)`          |
| **Check state**      | `state.matches("loading")` or `state.value`          |
| **Send event**       | `send({ type: "EVENT_NAME", ...payload })`           |
| **Read context**     | `state.context.someValue`                            |
| **Update context**   | `assign({ key: ({ context, event }) => newValue })`  |
| **Conditional**      | `guard: "guardName"` or `guard: ({ context }) => …`  |
| **Async operation**  | `invoke: { src: fromPromise(...), onDone, onError }` |
| **Optimized select** | `useSelector(actorRef, (state) => state.context.x)`  |
