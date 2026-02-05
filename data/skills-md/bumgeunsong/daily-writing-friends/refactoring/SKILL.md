---
name: refactoring
description: Use when user explicitly asks to refactor code, or when test coverage is requested for untested code with side effects. Enforces Functional Core Imperative Shell pattern extraction before any changes.
---

# Refactoring with Functional Core, Imperative Shell

Extract pure functions before refactoring. Never refactor code that mixes logic with side effects.

## When to Use

- User asks to "refactor", "consolidate", "extract", or "reduce duplication"
- Test coverage requested for hooks, components, or code with I/O
- Code review reveals logic buried in side-effect-heavy code

## Core Pattern

```
1. ANALYZE → Identify pure logic vs side effects
2. EXTRACT → Move pure logic to utils/ as pure functions
3. TEST → Write output-based tests for extracted functions
4. REFACTOR → Modify imperative shell (now thin wrapper)
```

## Implementation

### Step 1: Analyze Before Touching Code

```typescript
// IDENTIFY in existing code:
// - Pure logic (calculations, transformations, validations)
// - Side effects (API calls, state updates, localStorage, Date.now())

// Example: useCommentSuggestions.ts
// PURE: isCacheValid(entry, currentTime, ttl) → boolean
// IMPURE: localStorage.getItem(), Date.now(), queryClient.setQueryData()
```

### Step 2: Extract Pure Functions

```typescript
// Before: Logic mixed with side effects
const loadFromCache = (key: string) => {
  const cached = localStorage.getItem(key);  // side effect
  if (!cached) return undefined;
  const entry = JSON.parse(cached);
  return Date.now() - entry.timestamp <= TTL ? entry.data : undefined;  // impure
};

// After: Pure function extracted
export const isCacheValid = (timestamp: number, currentTime: number, ttl: number): boolean =>
  currentTime - timestamp <= ttl;

// Imperative shell becomes thin
const loadFromCache = (key: string) => {
  const cached = localStorage.getItem(key);
  if (!cached) return undefined;
  const entry = JSON.parse(cached);
  return isCacheValid(entry.timestamp, Date.now(), TTL) ? entry.data : undefined;
};
```

### Step 3: Test Only Pure Functions

```typescript
describe('isCacheValid', () => {
  it('returns true when within TTL', () => {
    expect(isCacheValid(1000, 2000, 5000)).toBe(true);
  });

  it('returns false when TTL exceeded', () => {
    expect(isCacheValid(1000, 10000, 5000)).toBe(false);
  });
});
```

## Common Mistakes

| Mistake | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| Refactor first, test later | No safety net for regressions | Extract + test pure functions first |
| Mock Date.now() in tests | Testing implementation, not behavior | Inject time as parameter |
| Test hooks directly | Requires QueryClient, context mocking | Extract logic, test pure functions |
| Skip analysis step | Miss extraction opportunities | Always analyze pure vs impure first |

## Red Flags

Stop and re-analyze if you find yourself:
- Writing `vi.mock()` for more than external APIs
- Testing a function that calls `useState`, `useQuery`, or Firebase
- Unable to test without `renderHook()` or `QueryClientProvider`
