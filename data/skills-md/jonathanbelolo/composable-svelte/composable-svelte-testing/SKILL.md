---
name: composable-svelte-testing
description: Testing patterns for Composable Svelte. Use when writing tests, using TestStore, mocking dependencies, or testing reducers and effects. Covers the send/receive pattern, mock implementations, testing composition strategies, and testing best practices.
---

# Composable Svelte Testing

This skill covers testing patterns for Composable Svelte applications using TestStore and mock dependencies.

---

## TESTSTORE API

### Core Pattern: send/receive

TestStore provides exhaustive action testing with the send/receive pattern:

```typescript
import { createTestStore } from '@composable-svelte/core/test';

describe('Feature', () => {
  it('loads items successfully', async () => {
    const store = createTestStore({
      initialState: { items: [], isLoading: false, error: null },
      reducer: featureReducer,
      dependencies: {
        api: {
          getItems: async () => ({ ok: true, data: [mockItem1, mockItem2] })
        }
      }
    });

    // User initiates action
    await store.send({ type: 'loadItems' }, (state) => {
      expect(state.isLoading).toBe(true);
      expect(state.error).toBeNull();
    });

    // Effect dispatches action
    await store.receive({ type: 'itemsLoaded' }, (state) => {
      expect(state.items).toHaveLength(2);
      expect(state.isLoading).toBe(false);
    });

    // Assert no more pending actions
    await store.finish();
  });
});
```

### TestStore Methods

```typescript
interface TestStore<State, Action> {
  // Send an action and assert resulting state
  send(action: Action, assert: (state: State) => void): Promise<void>;

  // Receive an action from effects and assert state
  receive(action: Action, assert: (state: State) => void): Promise<void>;

  // Assert no more pending actions
  finish(): Promise<void>;

  // Advance time for debounced/delayed effects
  advanceTime(ms: number): Promise<void>;

  // Get current state
  get state(): State;
}
```

---

## TESTING PATTERNS

### 1. Loading Data with Error Handling

```typescript
it('handles load failure', async () => {
  const store = createTestStore({
    initialState: { items: [], isLoading: false, error: null },
    reducer: featureReducer,
    dependencies: {
      api: {
        getItems: async () => ({ ok: false, error: 'Network error' })
      }
    }
  });

  await store.send({ type: 'loadItems' }, (state) => {
    expect(state.isLoading).toBe(true);
  });

  await store.receive({ type: 'loadFailed' }, (state) => {
    expect(state.error).toBe('Network error');
    expect(state.isLoading).toBe(false);
  });

  await store.finish();
});
```

### 2. Debounced Search

```typescript
import { vi, beforeEach, afterEach } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.restoreAllMocks();
});

it('debounces search input', async () => {
  const store = createTestStore({
    initialState: { query: '', results: [] },
    reducer: searchReducer,
    dependencies: {
      api: {
        search: vi.fn(async (q) => ({ ok: true, data: [`result for ${q}`] }))
      }
    }
  });

  await store.send({ type: 'queryChanged', query: 'a' }, (state) => {
    expect(state.query).toBe('a');
  });

  // Advance 100ms - should not trigger search
  await store.advanceTime(100);

  await store.send({ type: 'queryChanged', query: 'ab' }, (state) => {
    expect(state.query).toBe('ab');
  });

  // Advance 300ms - should trigger search
  await store.advanceTime(300);

  await store.receive({ type: 'searchResults' }, (state) => {
    expect(state.results).toEqual(['result for ab']);
  });

  await store.finish();
});
```

### 3. Form Submission

```typescript
it('validates and submits form', async () => {
  const store = createTestStore({
    initialState: {
      data: { email: '' },
      errors: {},
      isSubmitting: false
    },
    reducer: formReducer,
    dependencies: {
      api: {
        submitForm: vi.fn(async (data) => ({ ok: true }))
      }
    }
  });

  // Invalid email
  await store.send({ type: 'fieldChanged', field: 'email', value: 'invalid' }, (state) => {
    expect(state.data.email).toBe('invalid');
    expect(state.errors.email).toBe('Invalid email address');
  });

  // Valid email
  await store.send({ type: 'fieldChanged', field: 'email', value: 'test@example.com' }, (state) => {
    expect(state.data.email).toBe('test@example.com');
    expect(state.errors.email).toBeUndefined();
  });

  // Submit
  await store.send({ type: 'submit' }, (state) => {
    expect(state.isSubmitting).toBe(true);
  });

  await store.receive({ type: 'submissionSucceeded' }, (state) => {
    expect(state.isSubmitting).toBe(false);
  });

  await store.finish();
});
```

### 4. Navigation Flows

```typescript
it('opens and closes modal', async () => {
  const store = createTestStore({
    initialState: { destination: null, items: [] },
    reducer: appReducer,
    dependencies: {}
  });

  // Open modal
  await store.send({ type: 'addButtonTapped' }, (state) => {
    expect(state.destination).not.toBeNull();
    expect(state.destination.name).toBe('');
  });

  // User types name
  await store.send({
    type: 'destination',
    action: { type: 'presented', action: { type: 'nameChanged', name: 'New Item' } }
  }, (state) => {
    expect(state.destination.name).toBe('New Item');
  });

  // Save and close
  await store.send({
    type: 'destination',
    action: { type: 'presented', action: { type: 'saveButtonTapped' } }
  }, (state) => {
    expect(state.destination).toBeNull();
    expect(state.items).toHaveLength(1);
    expect(state.items[0].name).toBe('New Item');
  });

  await store.finish();
});
```

### 5. Animations (PresentationState)

```typescript
it('animates modal presentation', async () => {
  const store = createTestStore({
    initialState: {
      content: null,
      presentation: { status: 'idle' }
    },
    reducer: modalReducer,
    dependencies: {}
  });

  // Show modal
  await store.send({ type: 'show', content: { title: 'Hello' } }, (state) => {
    expect(state.presentation.status).toBe('presenting');
    expect(state.content).toEqual({ title: 'Hello' });
  });

  // Animation completes
  await store.receive({ type: 'presentation', event: { type: 'presentationCompleted' } }, (state) => {
    expect(state.presentation.status).toBe('presented');
  });

  // Hide modal
  await store.send({ type: 'hide' }, (state) => {
    expect(state.presentation.status).toBe('dismissing');
  });

  // Dismissal completes
  await store.receive({ type: 'presentation', event: { type: 'dismissalCompleted' } }, (state) => {
    expect(state.presentation.status).toBe('idle');
    expect(state.content).toBeNull();
  });

  await store.finish();
});
```

---

## MOCK DEPENDENCIES

### MockClock

```typescript
import { MockClock } from '@composable-svelte/core/test';

it('uses mock clock for time-based effects', async () => {
  const mockClock = new MockClock();

  const store = createTestStore({
    initialState: { toast: null },
    reducer: toastReducer,
    dependencies: { clock: mockClock }
  });

  await store.send({ type: 'showToast', message: 'Hello' }, (state) => {
    expect(state.toast).toBe('Hello');
  });

  // Advance time by 3 seconds
  await mockClock.advance(3000);

  await store.receive({ type: 'hideToast' }, (state) => {
    expect(state.toast).toBeNull();
  });

  await store.finish();
});
```

### MockAPIClient

```typescript
import { MockAPIClient } from '@composable-svelte/core/test';

it('uses mock API client', async () => {
  const mockAPI = new MockAPIClient();
  mockAPI.mock('GET', '/users', { ok: true, data: [user1, user2] });
  mockAPI.mock('POST', '/users', { ok: true, data: newUser });

  const store = createTestStore({
    initialState: { users: [] },
    reducer: usersReducer,
    dependencies: { api: mockAPI }
  });

  await store.send({ type: 'loadUsers' }, (state) => {
    expect(state.isLoading).toBe(true);
  });

  await store.receive({ type: 'usersLoaded' }, (state) => {
    expect(state.users).toHaveLength(2);
  });

  await store.finish();
});
```

### MockWebSocket

```typescript
import { MockWebSocket } from '@composable-svelte/core/test';

it('uses mock WebSocket', async () => {
  const mockWS = new MockWebSocket();

  const store = createTestStore({
    initialState: { messages: [], connectionStatus: 'disconnected' },
    reducer: chatReducer,
    dependencies: { ws: mockWS }
  });

  await store.send({ type: 'connect' }, (state) => {
    expect(state.connectionStatus).toBe('connecting');
  });

  // Simulate connection
  mockWS.simulateOpen();

  await store.receive({ type: 'connected' }, (state) => {
    expect(state.connectionStatus).toBe('connected');
  });

  // Simulate message
  mockWS.simulateMessage({ type: 'chat', text: 'Hello' });

  await store.receive({ type: 'messageReceived' }, (state) => {
    expect(state.messages).toHaveLength(1);
  });

  await store.finish();
});
```

---

## TESTING COMPOSITION STRATEGIES

### Testing scope() Composition

```typescript
it('composes child reducer with scope', async () => {
  const store = createTestStore({
    initialState: {
      counter: { count: 0 },
      theme: 'light'
    },
    reducer: appReducer,
    dependencies: {}
  });

  await store.send({ type: 'counter', action: { type: 'increment' } }, (state) => {
    expect(state.counter.count).toBe(1);
  });

  await store.send({ type: 'toggleTheme' }, (state) => {
    expect(state.theme).toBe('dark');
  });

  await store.finish();
});
```

### Testing forEach() Composition

```typescript
it('updates individual todo in collection', async () => {
  const store = createTestStore({
    initialState: {
      todos: [
        { id: '1', text: 'Buy milk', completed: false },
        { id: '2', text: 'Walk dog', completed: false }
      ]
    },
    reducer: todosReducer,
    dependencies: {}
  });

  await store.send({ type: 'todo', id: '1', action: { type: 'toggle' } }, (state) => {
    expect(state.todos[0].completed).toBe(true);
    expect(state.todos[1].completed).toBe(false);
  });

  await store.finish();
});
```

---

## TESTING BEST PRACTICES

### 1. Test Reducer Logic, Not Components

**❌ WRONG**:
```typescript
import { render, fireEvent } from '@testing-library/svelte';

test('increments counter', async () => {
  const { getByText } = render(Counter);
  const button = getByText('Increment');
  await fireEvent.click(button);
  expect(getByText('1')).toBeInTheDocument();
});
```

**✅ CORRECT**:
```typescript
test('increments counter', async () => {
  const store = createTestStore({
    initialState: { count: 0 },
    reducer: counterReducer
  });

  await store.send({ type: 'increment' }, (state) => {
    expect(state.count).toBe(1);
  });

  await store.finish();
});
```

**WHY**: TestStore tests are faster, more focused, and test reducer logic in isolation.

---

### 2. Use finish() to Catch Pending Actions

```typescript
it('catches unexpected effects', async () => {
  const store = createTestStore({
    initialState: { count: 0 },
    reducer: counterReducer,
    dependencies: {}
  });

  await store.send({ type: 'increment' }, (state) => {
    expect(state.count).toBe(1);
  });

  // This will fail if there are pending actions from effects
  await store.finish();
});
```

---

### 3. Test Error Cases

```typescript
it('handles network errors gracefully', async () => {
  const store = createTestStore({
    initialState: { data: null, error: null },
    reducer: dataReducer,
    dependencies: {
      api: {
        getData: async () => ({ ok: false, error: 'Network error' })
      }
    }
  });

  await store.send({ type: 'load' }, (state) => {
    expect(state.isLoading).toBe(true);
  });

  await store.receive({ type: 'loadFailed' }, (state) => {
    expect(state.error).toBe('Network error');
    expect(state.data).toBeNull();
  });

  await store.finish();
});
```

---

### 4. Test Edge Cases

```typescript
it('prevents double submission', async () => {
  const submitSpy = vi.fn(async () => ({ ok: true }));

  const store = createTestStore({
    initialState: { isSubmitting: false },
    reducer: formReducer,
    dependencies: { api: { submit: submitSpy } }
  });

  await store.send({ type: 'submit' }, (state) => {
    expect(state.isSubmitting).toBe(true);
  });

  // Try to submit again while submitting
  await store.send({ type: 'submit' }, (state) => {
    // Should still be submitting, not duplicate
    expect(state.isSubmitting).toBe(true);
  });

  // Should only call API once
  expect(submitSpy).toHaveBeenCalledTimes(1);

  await store.receive({ type: 'submissionSucceeded' }, (state) => {
    expect(state.isSubmitting).toBe(false);
  });

  await store.finish();
});
```

---

## COMMON ANTI-PATTERNS

### 1. Not Using TestStore

**❌ WRONG**: Component tests for business logic
```typescript
import { render, fireEvent } from '@testing-library/svelte';

test('loads data on mount', async () => {
  const { getByText } = render(DataView);
  await waitFor(() => {
    expect(getByText('Item 1')).toBeInTheDocument();
  });
});
```

**✅ CORRECT**: TestStore for reducer logic
```typescript
test('loads data on mount', async () => {
  const store = createTestStore({
    initialState: { items: [], isLoading: false },
    reducer: dataReducer,
    dependencies: { api: mockAPI }
  });

  await store.send({ type: 'loadData' }, (state) => {
    expect(state.isLoading).toBe(true);
  });

  await store.receive({ type: 'dataLoaded' }, (state) => {
    expect(state.items).toHaveLength(2);
  });

  await store.finish();
});
```

---

### 2. Not Testing Effects

**❌ WRONG**: Only testing state updates
```typescript
test('loads data', async () => {
  const store = createTestStore({
    initialState: { isLoading: false },
    reducer: dataReducer,
    dependencies: {}
  });

  await store.send({ type: 'loadData' }, (state) => {
    expect(state.isLoading).toBe(true);
  });

  // Missing: await store.receive for effect dispatch
  await store.finish(); // Will fail!
});
```

**✅ CORRECT**: Testing state + effects
```typescript
test('loads data', async () => {
  const store = createTestStore({
    initialState: { isLoading: false },
    reducer: dataReducer,
    dependencies: { api: mockAPI }
  });

  await store.send({ type: 'loadData' }, (state) => {
    expect(state.isLoading).toBe(true);
  });

  // Test effect dispatch
  await store.receive({ type: 'dataLoaded' }, (state) => {
    expect(state.items).toBeDefined();
  });

  await store.finish();
});
```

---

### 3. Not Using Mock Dependencies

**❌ WRONG**: Real dependencies in tests
```typescript
const store = createTestStore({
  initialState: { users: [] },
  reducer: usersReducer,
  dependencies: {
    api: createRealAPIClient() // ❌ Real HTTP requests!
  }
});
```

**✅ CORRECT**: Mock dependencies
```typescript
const store = createTestStore({
  initialState: { users: [] },
  reducer: usersReducer,
  dependencies: {
    api: {
      getUsers: async () => ({ ok: true, data: [mockUser1, mockUser2] })
    }
  }
});
```

---

## CHECKLISTS

### Pre-Commit Testing Checklist

- [ ] 1. NO `$state` in components (except DOM refs)
- [ ] 2. All application state in store
- [ ] 3. All state changes via actions
- [ ] 4. Immutable updates (no mutations)
- [ ] 5. Effects as data structures
- [ ] 6. Exhaustiveness checks in reducers
- [ ] 7. TestStore tests (not component tests)
- [ ] 8. All actions tested with send/receive
- [ ] 9. All effects tested (receive after send)
- [ ] 10. Error cases tested
- [ ] 11. Edge cases tested
- [ ] 12. finish() called in all tests

---

## SUMMARY

This skill covers testing patterns for Composable Svelte:

1. **TestStore API**: send/receive pattern for exhaustive testing
2. **Testing Patterns**: Loading, debouncing, forms, navigation, animations
3. **Mock Dependencies**: MockClock, MockAPIClient, MockWebSocket
4. **Testing Composition**: scope(), forEach(), tree helpers
5. **Best Practices**: Test reducers not components, use finish(), test errors
6. **Anti-Patterns**: Component tests, not testing effects, real dependencies

**Remember**: Use TestStore for ALL business logic tests. Component tests are only for visual/accessibility testing.

For core architecture, see **composable-svelte-core** skill.
For navigation testing, see **composable-svelte-navigation** skill.
For form testing, see **composable-svelte-forms** skill.
