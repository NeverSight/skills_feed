---
name: xstate
description: Helps create XState v5 state machines in TypeScript and React. Use when building state machines, actors, statecharts, finite state logic, actor systems, or integrating XState with React/Vue/Svelte components.
user-invocable: false
---

# XState v5 Skill

> **CRITICAL: This skill covers XState v5 ONLY.** Do not use v4 patterns, APIs, or documentation. XState v5 requires **TypeScript 5.0+**.

## When to Use

- State machine and statechart design
- Actor system implementation
- XState v5 API usage (`setup`, `createMachine`, `createActor`)
- Framework integration (React, Vue, Svelte)
- Complex async flow orchestration

## Key Concepts

**Actors** are independent entities that communicate by sending messages. XState v5 supports:

| Actor Type | Creator | Use Case |
|------------|---------|----------|
| State Machine | `createMachine()` | Complex state logic with transitions |
| Promise | `fromPromise()` | Async operations (fetch, timers) |
| Callback | `fromCallback()` | Bidirectional streams (WebSocket, EventSource) |
| Observable | `fromObservable()` | RxJS streams |
| Transition | `fromTransition()` | Reducer-like state updates |

## Quick Start

```typescript
import { setup, assign, createActor } from 'xstate';

const machine = setup({
  types: {
    context: {} as { count: number },
    events: {} as { type: 'increment' } | { type: 'decrement' },
  },
  actions: {
    increment: assign({ count: ({ context }) => context.count + 1 }),
    decrement: assign({ count: ({ context }) => context.count - 1 }),
  },
}).createMachine({
  id: 'counter',
  initial: 'active',
  context: { count: 0 },
  states: {
    active: {
      on: {
        increment: { actions: 'increment' },
        decrement: { actions: 'decrement' },
      },
    },
  },
});

// Create and start actor
const actor = createActor(machine);
actor.subscribe((snapshot) => console.log(snapshot.context.count));
actor.start();
actor.send({ type: 'increment' });
```

## v5 API Changes (NEVER use v4 patterns)

| v4 (WRONG) | v5 (CORRECT) |
|------------|--------------|
| `createMachine()` alone | `setup().createMachine()` |
| `interpret()` | `createActor()` |
| `service.start()` | `actor.start()` |
| `state.matches()` | `snapshot.matches()` |
| `services: {}` | `actors: {}` |
| `state.context` | `snapshot.context` |

## Invoke vs Spawn

- **invoke**: Actor lifecycle tied to state (created on entry, stopped on exit)
- **spawn**: Dynamic actors independent of state transitions

## Inspection API (Debugging)

```typescript
const actor = createActor(machine, {
  inspect: (event) => {
    if (event.type === '@xstate.snapshot') {
      console.log(event.snapshot);
    }
  },
});
```

Event types: `@xstate.actor`, `@xstate.event`, `@xstate.snapshot`, `@xstate.microstep`

## File Organization

```
feature/
├── feature.machine.ts    # Machine definition
├── feature.types.ts      # Shared types (optional)
├── feature.tsx           # React component
└── feature.test.ts       # Machine tests
```

## Learning Path

| Level | Focus |
|-------|-------|
| Beginner | Counter, toggle machines; `setup()` pattern |
| Intermediate | Guards, actions, hierarchical states, `fromPromise()` |
| Advanced | Observable actors, spawning, actor orchestration |

## Supporting Documentation

- [PATTERNS.md](PATTERNS.md) - Guards, actions, actors, hierarchical/parallel states
- [REACT.md](REACT.md) - React hooks (`useMachine`, `useActor`, `useSelector`)
- [EXAMPLES.md](EXAMPLES.md) - Complete working examples

## Resources

- [Official Docs](https://stately.ai/docs/xstate)
- [Stately Studio](https://stately.ai/studio) - Visual editor
