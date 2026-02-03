---
name: testing-strategy
description: Comprehensive test architecture, coverage strategy, and test design beyond API testing. Covers test pyramid design, frontend/component testing (React Testing Library, Vue Test Utils), E2E testing (Playwright, Cypress), visual regression, mocking strategies (MSW), and flaky test prevention. Use this skill when designing test architecture, determining what test type to use, setting up component or E2E testing, debugging flaky tests, reviewing coverage strategy, or organizing test files. Triggers on "test strategy", "what to test", "coverage", "e2e", "playwright", "cypress", "component test", "flaky test", "test pyramid".
---

# Testing Strategy

Comprehensive testing guidance for test architecture, coverage strategy, and test design.

## Test Pyramid

```
                    ▲
                   ╱ ╲   E2E Tests
                  ╱───╲  (5-10% of tests)
                 ╱     ╲  Real browser, full stack
                ╱───────╲
               ╱         ╲  Integration Tests
              ╱───────────╲  (15-25% of tests)
             ╱             ╲  Multiple units, real dependencies
            ╱───────────────╲
           ╱                 ╲  Unit Tests
          ╱───────────────────╲  (65-80% of tests)
         ╱                     ╲  Single units, isolated, fast
```

| Level | Speed | Cost | Confidence | Isolation |
|-------|-------|------|------------|-----------|
| **Unit** | ~1ms | Low | Narrow | High |
| **Integration** | ~100ms | Medium | Medium | Medium |
| **E2E** | ~1-10s | High | High | Low |

### When to Deviate

Invert the pyramid when:
- **Legacy code without unit tests** → Start with E2E for safety net, add units as you refactor
- **Highly integrated systems** → More integration tests, fewer isolated units
- **Critical user journeys** → Extra E2E coverage for checkout, auth, payments
- **UI-heavy apps** → More component/visual tests, fewer traditional units

## Decision Framework

**What test type should I write?**

```
Is it a pure function or utility?
  └─ YES → Unit test
  └─ NO ↓

Does it involve UI rendering?
  └─ YES → Component test (RTL/Vue Test Utils)
  └─ NO ↓

Does it cross system boundaries (DB, API, services)?
  └─ YES → Integration test
  └─ NO ↓

Is it a critical user flow spanning multiple pages?
  └─ YES → E2E test (Playwright/Cypress)
  └─ NO → Unit or integration test
```

**What NOT to test:**

- Framework internals (React hooks work, Next.js routing works)
- Third-party libraries (axios sends requests correctly)
- Implementation details (which internal method was called)
- Styling (unless visual regression is set up)
- Trivial code (getters, setters, type definitions)

## Coverage Strategy

### Meaningful Metrics

Coverage percentage alone is misleading. Focus on:

| Metric | Target | Why |
|--------|--------|-----|
| **Branch coverage** | >80% | Ensures conditionals are tested |
| **Critical path coverage** | 100% | Auth, payments, data mutations |
| **Error path coverage** | >70% | Graceful failure handling |
| **Edge case coverage** | Document, not % | Known boundaries tested |

### Coverage by Layer

```
┌─────────────────────────────────────────────────────────┐
│ UI Components                          Target: 70-80%   │
│ ├─ Render states (loading, error, empty, success)       │
│ ├─ User interactions (click, type, submit)              │
│ └─ Accessibility (keyboard nav, ARIA)                   │
├─────────────────────────────────────────────────────────┤
│ Business Logic / Services              Target: 85-95%   │
│ ├─ Happy paths                                          │
│ ├─ Error cases                                          │
│ ├─ Edge cases (null, empty, boundary)                   │
│ └─ State transitions                                    │
├─────────────────────────────────────────────────────────┤
│ Data Layer / API                       Target: 80-90%   │
│ ├─ CRUD operations                                      │
│ ├─ Validation                                           │
│ ├─ Error handling                                       │
│ └─ Authorization                                        │
├─────────────────────────────────────────────────────────┤
│ E2E Flows                             Target: Critical  │
│ ├─ Authentication flow                                  │
│ ├─ Core purchase/conversion path                        │
│ └─ Critical business workflows                          │
└─────────────────────────────────────────────────────────┘
```

### What to Skip

```typescript
// ❌ Don't test pass-through functions
export const getUser = (id: string) => userService.getById(id);

// ❌ Don't test type definitions
type User = { id: string; name: string };

// ❌ Don't test constants
export const MAX_RETRIES = 3;

// ❌ Don't test simple getters
get fullName() { return `${this.first} ${this.last}`; }
```

## Test Organization

### Folder Structure

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx      # Co-located unit/component tests
│   │   └── Button.stories.tsx   # Storybook stories
│   └── Form/
│       ├── Form.tsx
│       └── Form.test.tsx
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts
├── services/
│   ├── userService.ts
│   └── userService.test.ts
└── utils/
    ├── validation.ts
    └── validation.test.ts

tests/                           # Cross-cutting tests
├── setup.ts                     # Global test setup
├── mocks/
│   ├── handlers.ts              # MSW request handlers
│   └── server.ts                # MSW server setup
├── fixtures/
│   └── users.ts                 # Shared test data
├── integration/                 # Multi-module tests
│   └── checkout.test.ts
└── e2e/                         # Playwright/Cypress
    ├── auth.spec.ts
    ├── checkout.spec.ts
    └── fixtures/
        └── test-user.json
```

### Naming Conventions

```typescript
// File naming
Button.test.tsx          // Co-located with component
Button.spec.tsx          // Alternative (consistency matters)
button.test.ts           // For non-component modules

// Test naming: describe what, not how
describe('LoginForm', () => {
  // ✅ Describes behavior
  it('shows error message when credentials are invalid', () => {});
  it('redirects to dashboard after successful login', () => {});
  it('disables submit button while loading', () => {});

  // ❌ Describes implementation
  it('calls setError with message', () => {});
  it('uses useRouter hook', () => {});
});
```

## Anti-Patterns

### Testing Implementation Details

```typescript
// ❌ Tests internal state
it('updates internal state', () => {
  const { result } = renderHook(() => useCounter());
  act(() => result.current.increment());
  expect(result.current.state.count).toBe(1); // Testing internal state
});

// ✅ Tests behavior
it('displays incremented value', () => {
  render(<Counter />);
  fireEvent.click(screen.getByRole('button', { name: /increment/i }));
  expect(screen.getByText('1')).toBeInTheDocument();
});
```

### Snapshot Abuse

```typescript
// ❌ Snapshot everything
it('renders', () => {
  expect(render(<ComplexPage />)).toMatchSnapshot();
});

// ✅ Snapshot sparingly, for specific output
it('generates correct email template', () => {
  expect(generateEmailHTML(data)).toMatchSnapshot();
});
```

### Test Interdependence

```typescript
// ❌ Tests depend on order
describe('User', () => {
  it('creates user', () => { /* sets userId */ });
  it('updates user', () => { /* uses userId from above */ });
  it('deletes user', () => { /* uses userId from above */ });
});

// ✅ Each test is independent
describe('User', () => {
  it('creates user', async () => {
    const user = await createUser(userData);
    expect(user.id).toBeDefined();
  });

  it('updates user', async () => {
    const user = await createUser(userData);
    const updated = await updateUser(user.id, newData);
    expect(updated.name).toBe(newData.name);
  });
});
```

### Mocking Too Much

```typescript
// ❌ Mock everything = test nothing
it('processes order', () => {
  jest.mock('./inventory');
  jest.mock('./payment');
  jest.mock('./shipping');
  jest.mock('./notifications');
  // What are we even testing?
});

// ✅ Mock boundaries, test logic
it('processes order', () => {
  const mockPaymentGateway = createMockPaymentGateway();
  const result = processOrder(order, mockPaymentGateway);
  expect(result.status).toBe('completed');
  expect(mockPaymentGateway.charge).toHaveBeenCalledWith(order.total);
});
```

### Arbitrary Waits

```typescript
// ❌ Flaky: timing-dependent
it('shows success message', async () => {
  fireEvent.click(submitButton);
  await new Promise(r => setTimeout(r, 1000));
  expect(screen.getByText('Success')).toBeInTheDocument();
});

// ✅ Reliable: wait for condition
it('shows success message', async () => {
  fireEvent.click(submitButton);
  await waitFor(() => {
    expect(screen.getByText('Success')).toBeInTheDocument();
  });
});
```

## Quick Reference: Test Doubles

| Type | Purpose | Use When |
|------|---------|----------|
| **Stub** | Returns canned data | Need predictable responses |
| **Mock** | Records calls, verifiable | Need to verify interactions |
| **Spy** | Wraps real implementation | Need to observe real behavior |
| **Fake** | Working implementation | Need simplified but real behavior |

```typescript
// Stub: returns fixed data
const userServiceStub = { getUser: () => ({ id: '1', name: 'Test' }) };

// Mock: verifiable
const sendEmail = vi.fn();
await processOrder(order);
expect(sendEmail).toHaveBeenCalledWith(order.email);

// Spy: observe real calls
const spy = vi.spyOn(console, 'error');
await riskyOperation();
expect(spy).not.toHaveBeenCalled();

// Fake: real-ish implementation
const fakeDb = new Map<string, User>();
const userService = createUserService({ db: fakeDb });
```

## Design Artifact Integration

### Consuming Accessibility Audits

When accessibility audits exist from the design phase, incorporate their findings into your test strategy.

**Check for design artifacts:**

```bash
# Look for accessibility audit in .claude/design directory
find .claude/design -name "a11y-audit.md" 2>/dev/null
```

**If `.claude/design/*/a11y-audit.md` exists:**

1. **Read the audit findings** — Focus on the "Findings" section
2. **Extract testable requirements** — Each finding with severity (Critical/Major) should have corresponding tests
3. **Map findings to test types:**
   - **WCAG compliance issues** → Component tests (RTL/Vitest) + E2E tests (Playwright)
   - **Keyboard navigation issues** → E2E tests with keyboard-only simulation
   - **Screen reader issues** → Component tests with accessibility tree assertions
   - **Color contrast issues** → Visual regression tests or automated checks
   - **ARIA issues** → Component tests checking roles, labels, states

**Generate accessibility test cases from audit:**

```typescript
// Example: From finding "Form inputs missing labels"
describe('LoginForm accessibility', () => {
  it('all form fields have accessible labels', () => {
    render(<LoginForm />);

    const emailInput = screen.getByRole('textbox', { name: /email/i });
    const passwordInput = screen.getByLabelText(/password/i);

    expect(emailInput).toHaveAccessibleName();
    expect(passwordInput).toHaveAccessibleName();
  });
});

// Example: From finding "Checkout not keyboard accessible"
test('complete checkout flow using keyboard only', async ({ page }) => {
  await page.goto('/checkout');

  // Tab navigation through form
  await page.keyboard.press('Tab');
  await page.keyboard.type('John Doe');
  await page.keyboard.press('Tab');
  await page.keyboard.type('john@example.com');

  // Submit with Enter
  await page.keyboard.press('Enter');

  await expect(page.locator('[role="alert"]')).toContainText('Order confirmed');
});

// Example: From finding "Low contrast on primary buttons"
describe('Button contrast', () => {
  it('meets WCAG AA contrast ratio', () => {
    render(<PrimaryButton>Submit</PrimaryButton>);

    const button = screen.getByRole('button', { name: /submit/i });
    const styles = window.getComputedStyle(button);

    // Can use jest-axe or manual color contrast calculation
    expect(button).toHaveNoViolations(); // jest-axe
  });
});
```

**Mapping WCAG criteria to test approaches:**

| WCAG Criterion | Test Type | Tool/Approach |
|----------------|-----------|---------------|
| **1.1.1 Non-text Content** | Component | Check `alt` attributes, `aria-label` |
| **1.3.1 Info and Relationships** | Component | Validate semantic HTML, heading hierarchy |
| **1.4.3 Contrast (Minimum)** | Visual/Component | jest-axe, color contrast library |
| **2.1.1 Keyboard** | E2E | Playwright keyboard navigation |
| **2.4.3 Focus Order** | E2E | Tab order verification |
| **2.4.7 Focus Visible** | E2E | Assert focus indicator visibility |
| **3.3.1 Error Identification** | Component + E2E | Check error messages are announced |
| **4.1.2 Name, Role, Value** | Component | ARIA role and attribute validation |

**Backward compatibility:**

If no a11y-audit.md exists, the skill works normally. Accessibility testing is still important:

- Add basic keyboard navigation tests for interactive elements
- Validate semantic HTML and ARIA where used
- Include accessibility in component test checklist (see below)

## Checklist: New Feature Testing

### Before Writing Tests

- [ ] Identify the test pyramid distribution for this feature
- [ ] List critical user paths that need E2E coverage
- [ ] Identify external boundaries to mock (APIs, services)
- [ ] Set up test data factories/fixtures
- [ ] **Check for `.claude/design/*/a11y-audit.md` and extract testable requirements**

### Component Tests

- [ ] Renders correctly with default props
- [ ] Renders all visual states (loading, error, empty, success)
- [ ] Handles user interactions
- [ ] Accessibility: keyboard navigation, ARIA labels
- [ ] **If a11y-audit exists: Address specific findings (labels, roles, contrast)**

### Integration Tests

- [ ] Happy path works end-to-end
- [ ] Error paths handled gracefully
- [ ] Edge cases (empty, null, boundary values)
- [ ] Authorization enforced

### E2E Tests

- [ ] Critical path covered (auth, checkout, core workflows)
- [ ] Cross-browser if required
- [ ] Mobile viewport if responsive
- [ ] Test data cleanup after run
- [ ] **If a11y-audit exists: Keyboard-only flows for critical paths**

---

**References:**
- [references/test-architecture.md](references/test-architecture.md) — Folder structure, shared utilities, test configuration
- [references/frontend-testing.md](references/frontend-testing.md) — Component testing with RTL and Vue Test Utils
- [references/e2e-testing.md](references/e2e-testing.md) — Playwright and Cypress patterns, flakiness prevention
- [references/test-design.md](references/test-design.md) — Test case design, boundary analysis, equivalence partitioning
- [references/mocking-strategies.md](references/mocking-strategies.md) — When and how to mock, MSW patterns
- [references/coverage-guide.md](references/coverage-guide.md) — Meaningful coverage metrics and targets
