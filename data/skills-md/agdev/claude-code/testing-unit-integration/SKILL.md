---
name: testing-unit-integration
description: Expert guidance for writing clean, simple, and effective unit, integration, component, microservice, and API tests. Use this skill when reviewing existing tests for violations, writing new tests, or refactoring tests. NOT for end-to-end tests that span multiple processes - use testing-e2e skill instead. Covers AAA pattern, data factories, mocking strategies, DOM testing, database testing, and assertion best practices.
---

# Unit & Integration Testing Best Practices

Expert guidance for keeping tests simple, clean, consistent, and short. When reviewing tests, report violated rule numbers.

**Scope:** Unit, integration, component, microservice, API tests. NOT for e2e tests spanning multiple processes - use `testing-e2e` skill instead.

## The 6 Critical Rules

These are absolutely critical - stop coding if you can't follow them:

1. **Max 10 statements** - No more than 10 statements/expressions per test
2. **Essential details only** - Include only details that directly affect the test result
3. **Flat structure** - No if/else, no loops, no try-catch, no console.log
4. **Cover all layers** - Never mock INTERNAL parts, only external system calls
5. **Smoking gun principle** - Data in assertion must appear first in arrange phase
6. **Self-contained** - Each test creates its own state, never relies on other tests

## Key Principles

### Smoking Gun Principle
Each data point in assertion must appear in arrange phase - shows cause and effect clearly.

```typescript
// Arrange
const activeOrder = buildOrder({ status: 'active' })

// Assert - references arranged data directly
expect(result.id).toBe(activeOrder.id)  // ✅ Clear connection
expect(result.id).toBe('123')           // ❌ Magic value
```

### Breadcrumb Principle
Anything affecting test directly should exist in the test. Implicit effects go in beforeEach, never in external files.

### Extra Mile Principle
Cover a little more than needed. Testing save? Use two items. Testing filter? Also verify items that should NOT appear.

### Deliberate Fire Principle
Choose options more likely to fail. Picking user role? Use least privileged one.

## Section A - Test Structure

- **A.1** Title pattern: `When {scenario}, then {expectation}`
- **A.3** Max 10 statements (multi-line expressions count as one)
- **A.4** Reference arranged data directly in assertions - don't duplicate values (use `activeOrder.id` not `'123'`)
- **A.5** Three phases required: Arrange, Act, Assert (with line breaks between)
- **A.10** Max 3 assertions per test
- **A.13** Totally flat - no try-catch, loops, comments, console.log
- **A.18** All variables typed - no `any`. Use `obj as unknown as Type` for invalid inputs
- **A.23** Assertions only inside test, never in helpers or hooks
- **A.25** Assertions only in Assert phase, never at start or middle
- **A.28** Extract 3+ line setups to `/test/helpers` folder

## Section B - Test Logic

- **B.3** Smoking gun: assertion data must appear in arrange
- **B.5** Exclude details not directly related to test result
- **B.10** No redundant assertions
- **B.15** Don't compare huge datasets - focus on specific topic
- **B.20** If test assumes data exists, create it in Arrange
- **B.23** Don't test implementation details - only user-facing behavior
- **B.25** No time-based waiting (setTimeout, waitForTimeout)
- **B.28** Clean up in beforeEach: mocks, env vars, localStorage, globals
- **B.30** When fixing bugs: amend existing tests that SHOULD have caught it, don't just add new tests
- **B.32** TDD Red phase: verify amended tests FAIL with buggy code before applying fix

## Section C - Test Data

- **C.3** Data from factory files in data folder (buildOrder, buildUser)
- **C.4** Factories return defaults but allow field overrides
- **C.5** Use faker for universal data (dates, addresses, non-domain)
- **C.7** Factory params must be typed (same types as code under test)
- **C.10** Use meaningful domain data, not dummy values
- **C.15** Randomize multi-option fields by default
- **C.20** Arrays: default to 2 items (not 0, 1, or 20)

### Data Factory Example

```typescript
import { faker } from "@faker-js/faker";
import { Order } from "../types";

export function buildOrder(overrides: Partial<Order> = {}): Order {
  return {
    id: faker.string.uuid(),
    customerName: faker.person.fullName(),
    status: faker.helpers.arrayElement(["active", "completed", "cancelled"]),
    items: [buildOrderItem(), buildOrderItem()], // Default 2 items
    ...overrides,
  };
}
```

## Section D - Assertions

- **D.7** No custom coding/loops - use built-in expect APIs
- **D.11** Minimal assertions to catch failures - avoid redundant checks
- **D.13** Use matchers that show full diff on failure
- **D.15** Objects with 3+ fields: use factory, override 3 key values max

### Strong Assertions

```typescript
// ❌ WEAK - Multiple redundant assertions
expect(response).not.toBeNull()
expect(Array.isArray(response)).toBe(true)
expect(response.length).toBe(2)
expect(response[0].id).toBe('123')

// ✅ STRONG - Single assertion catches all issues
expect(response).toEqual([{id: '123'}, {id: '456'}])
```

## Section E - Mocking

- **E.1** Mock ONLY external collaborators (email, payment, external APIs)
- **E.3** Use types/interfaces of mocked code - fails compilation when contract changes
- **E.5** Define mocks in test file (Arrange or beforeEach), never external files
- **E.7** Reset all mocks in beforeEach
- **E.9** Prefer network interception (MSW, Nock) over function mocks for HTTP
- **E.11** Integration tests: use REAL router/navigation, only mock external APIs
- **E.13** Never mock internal systems (routing, state management) in integration tests
- **E.15** Integration tests need same rigor as unit tests - same patterns, same coverage

**Cloud/External SDK mocking:** See [references/aws-sdk-mocking.md](references/aws-sdk-mocking.md) for AWS SDK patterns (also applicable to other cloud SDKs).

## Section F - DOM Testing

For React Testing Library, Playwright component tests, Storybook:

- **F.1** Only user-facing locators: getByRole, getByLabel, getByText. NO test-ids, CSS, xpath
- **F.3** No positional selectors: nth(i), first(), last()
- **F.5** Use framework's assertion mechanism (auto-retriable for Playwright)
- **F.9** No waitForSelector - auto-retriable assertions handle waiting
- **F.14** Don't assert on external systems - assert navigation happened
- **F.16** Test user-VISIBLE state: checkbox checked/unchecked, badge text, button disabled - not just that element exists

```typescript
// ❌ BAD - Only checks element exists, not its state
expect(screen.getByText('App Name')).toBeInTheDocument();

// ✅ GOOD - Verifies actual user-visible state
expect(screen.getByRole('checkbox', { name: /app name/i })).toBeChecked();
expect(within(row).getByText(/associated/i)).toBeInTheDocument();
expect(screen.getByRole('button', { name: /submit/i })).toBeDisabled();
```

## Section G - Database Testing

- **G.3** Test side effects: add multiple records, assert only intended ones changed
- **G.5** Use type matchers for auto-generated fields: `expect.any(Number)`
- **G.7** Add randomness to unique fields: `${faker.internet.email()}-${faker.string.nanoid(5)}`
- **G.9** Assert via public API, not direct DB queries
- **G.12** Pre-seed only metadata (countries, currencies). Create test-specific records in each test
- **G.14** Each test acts on its own records only - never share test data
- **G.18** Test cascading deletes/updates behavior

## Section H - Fake Timers

For testing debounce, throttle, cache TTL, polling, setTimeout/setInterval logic.

**Detailed guide:** See [references/fake-timers.md](references/fake-timers.md) for patterns and anti-patterns.

### Core Rules

- **H.1** Setup/teardown per test: `beforeEach(() => vi.useFakeTimers())`, `afterEach(() => vi.useRealTimers())`
- **H.3** Advance timers BEFORE awaiting promises (promise hangs if you await first)
- **H.5** Use `runAllTimersAsync()` when timer count is unknown
- **H.7** For rejected promises: use `rejects` matcher OR real timers with short delays
- **H.9** Never use fake timers for simple async/await without timer logic

### Quick Pattern

```typescript
// GOOD: Start promise, advance time, then await
const promise = functionWithTimeout();
await vi.advanceTimersByTimeAsync(1000);
const result = await promise;

// BAD: Await immediately (hangs forever - timers frozen)
const result = await functionWithTimeout(); // ❌ Never completes!
```

### Error Testing Pattern

```typescript
// For rejected promise tests - use rejects matcher
await expect(handler.execute(mockFn)).rejects.toThrow('fail');

// OR use real timers with short delays
vi.useRealTimers();
const config = { maxRetries: 2, delay: 1 }; // 1ms delay
await expect(retryWithBackoff(mockFn, config)).rejects.toThrow('fail');
```

## Section I - What to Test

- **I.7** Extra mile: testing save? Use two items. Testing filter? Check excluded items too
- **I.10** Deliberate fire: choose options more likely to fail (least privilege role)

## Section J - Contract Testing

When testing frontend-backend integration, validate contracts between layers.

- **J.1** Never use `as never`, `as any`, `as unknown` on mock return values - defeats TypeScript safety
- **J.3** Mocks must match ACTUAL API response structure (not idealized/fantasy data)
- **J.5** Destructure responses in tests exactly as consumers will - catches property name mismatches
- **J.7** Response property names must match TypeScript type definitions exactly
- **J.9** Add runtime validation (Zod/io-ts) for API responses - TypeScript can't validate runtime HTTP

```typescript
// ❌ BAD - Type escape hatch hides contract mismatch
vi.spyOn(api, 'create').mockResolvedValue(mockData as never);

// ❌ BAD - Frontend mock doesn't match actual backend
vi.mocked(api.create).mockResolvedValue({
  application: data,  // Frontend WANTS this
});
// But backend ACTUALLY returns: { data: {...} }

// ✅ GOOD - Mock matches actual backend response
const mockResponse: CreateResponse = {
  data: mockApp,  // Match ACTUAL backend
  created: true,
};
vi.spyOn(api, 'create').mockResolvedValue(mockResponse);

// ✅ GOOD - Destructure as consumers will (catches mismatches)
const { application } = response;  // Will fail if backend uses 'data' not 'application'
```

## Section K - Mock Data Guidelines

Mock data must reflect reality, not fantasy.

- **K.1** Copy real API responses as fixtures - never invent structure from scratch
- **K.3** Document fixture provenance: endpoint, date captured, backend version
- **K.5** Type-check all fixtures against TypeScript interfaces
- **K.7** Include edge cases in fixtures: empty arrays, null values, missing optional fields

```typescript
/**
 * Real API response from: GET /api/users/123/applications
 * Captured: 2025-12-04
 * Backend version: server@1.2.3
 *
 * Update this fixture if backend changes response structure.
 */
export const REAL_USER_APP_MAPPING: UserAppMapping = {
  _id: '',                    // Mapping ID (often empty)
  applicationId: 'app-123',   // CRITICAL: This is the app ID!
  isActiveForApp: true,
  application: { /* ... */ }
};

// Edge case fixtures
export const EDGE_CASES = {
  emptyList: [],
  nullField: { ...REAL_USER_APP_MAPPING, applicationId: null },
  missingOptional: { _id: '', applicationId: 'app-1' },  // No 'application' field
};
```

## Section L - Boolean Flag Testing

Boolean flags in API responses control critical behavior - test both states.

- **L.1** Test helper defaults can hide bugs - be aware of what defaults to true/false
- **L.3** For every boolean flag in response, test BOTH true and false states
- **L.5** Explicitly set boolean values in test data - never rely on helper defaults
- **L.7** Add `@warning` JSDoc to helpers with dangerous defaults that could mask bugs

```typescript
// ❌ BAD - Only tests one state (default true)
const mappings = [
  createMapping({ applicationId: 'app1' })  // isActiveForApp defaults to true
];

// ✅ GOOD - Tests both states explicitly
const mappings = [
  createMapping({ applicationId: 'app1', isActiveForApp: true }),   // Active
  createMapping({ applicationId: 'app2', isActiveForApp: false }),  // Inactive
];

// ✅ GOOD - Document dangerous defaults
/**
 * @warning The default `isActiveForApp` is TRUE. When testing inactive
 * associations, you MUST explicitly set `isActiveForApp: false`.
 * Forgetting this will cause tests to show associations as active
 * when they should be inactive.
 */
export function createMapping(overrides: Partial<Mapping> = {}): Mapping {
  return {
    isActiveForApp: true,  // Dangerous default - document it!
    ...overrides,
  };
}
```

## Section M - Error Handling Testing

Test error scenarios with correct HTTP semantics - 404 is NOT 503.

- **M.1** Map HTTP status to correct error type: 404→NotFoundError, 401→UnauthorizedError, 403→ForbiddenError, 5xx→ServiceUnavailableError
- **M.3** One test per error scenario - don't combine different error types
- **M.5** Validate error messages contain context (resource name, IDs)
- **M.7** Test error propagation through layers (HTTP client → Service → Controller)
- **M.9** Test business requirements, not implementation - ask "what SHOULD happen?"
- **M.11** No generic assertions - `rejects.toThrow()` needs error type, not just any error

**Detailed guide:** See [references/error-handling-matrix.md](references/error-handling-matrix.md) for HTTP status mapping and test patterns.

```typescript
// ❌ BAD - Wrong error mapping (404 is NOT service unavailable)
it('When user not found, then throws ServiceUnavailableError', async () => {
  nock(API_URL).get('/user/123').reply(404);
  await expect(service.getUser('123')).rejects.toThrow(ServiceUnavailableError);
});

// ❌ BAD - Generic assertion (any error passes)
await expect(service.getUser('123')).rejects.toThrow();

// ✅ GOOD - Correct error type for HTTP 404
it('When user not found (404), then throws NotFoundError', async () => {
  nock(API_URL).get('/user/123').reply(404, { message: 'User not found' });

  await expect(service.getUser('123')).rejects.toThrow(NotFoundError);
  await expect(service.getUser('123')).rejects.toThrow(/user.*not found/i);
});

// ✅ GOOD - Test both error type AND message context
it('When unauthorized (401), then throws UnauthorizedError with context', async () => {
  nock(API_URL).get('/user/123').reply(401);

  await expect(service.getUser('123')).rejects.toThrow(UnauthorizedError);
});
```

## Maximum Coverage, Minimal Tests

Achieve comprehensive coverage efficiently:
- Each test should cover a meaningful scenario, not just a single assertion
- Combine related assertions (max 3) that test the same behavior
- Use parameterized tests for similar scenarios with different inputs
- Focus on behavior, not implementation - fewer tests survive refactoring

## BAD Test Example

```typescript
it('should test orders filtering', async () => { // ❌ A.1 - vague title
  const adminUser = { role: 'admin' } // ❌ I.10 - use least privilege
  const mockOrderService = vi.fn() // ❌ E.1 - mocking internal
  const testData = [{ id: 1, name: 'test1' }] // ❌ C.10 - meaningless data

  render(<OrdersReport data={testData} />)
  const component = screen.getByTestId('orders-report') // ❌ F.1 - test-id

  try { // ❌ A.13 - try-catch not allowed
    await userEvent.click(screen.getByRole('button'))
    let found = [] // ❌ D.7 - custom coding
    for (const row of rows) { found.push(row) } // ❌ A.13 - loop
    expect(found.length).toBe(5) // ❌ B.3 - data not in arrange
    expect(mockOrderService).toHaveBeenCalled() // ❌ B.23 - implementation detail
  } catch (error) {
    console.log('Failed:', error) // ❌ A.13 - console.log
  }
})
```

## GOOD Test Example

```typescript
beforeEach(() => {
  const currentUser = buildUser({ role: 'viewer' }) // Deliberate fire
  http.get('/api/user/1', () => HttpResponse.json(currentUser))
})

test('When filtering by active status, then only active orders displayed', async () => {
  // Arrange
  const activeOrder = buildOrder({ customerName: faker.person.fullName(), status: 'active' })
  const completedOrder = buildOrder({ customerName: faker.person.fullName(), status: 'completed' })
  http.get('/api/orders', () => HttpResponse.json([activeOrder, completedOrder]))
  const screen = render(<OrdersReport />)

  // Act
  await userEvent.click(screen.getByRole('button', { name: 'Filter by Active' }))

  // Assert
  expect.element(screen.getByRole('cell', { name: activeOrder.customerName })).toBeVisible()
  expect.element(screen.getByRole('cell', { name: completedOrder.customerName })).not.toBeVisible() // Extra mile
})
```

## Rule Violation Reporting

When reviewing tests, report violations as:
```
Line X: Violates [RULE_NUMBER] - [Brief explanation]
```

Example:
```
Line 15: Violates A.13 - Contains try-catch block, tests must be flat
Line 23: Violates B.3 - Assertion uses '123' but this value not in Arrange phase
Line 31: Violates F.1 - Uses getByTestId, should use getByRole or getByLabel
```
