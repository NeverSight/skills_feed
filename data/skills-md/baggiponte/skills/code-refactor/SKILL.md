---
name: code-refactor
description: Systematic refactoring of codebase components through a structured 3-phase process. Use when asked to refactor, restructure, or improve specific components, modules, or areas of code. Produces research documentation, change proposals with code samples, and test plans. Triggers on requests like "refactor the authentication module", "restructure the data layer", "improve the API handlers", or "clean up the payment service".
---

# Code Refactor

## Overview

This skill guides systematic refactoring of one or more codebase components through three phases:

1. **Research** - Deep analysis of component behavior, usage patterns, and dependencies
2. **Proposal** - Concrete change suggestions with code samples and impact analysis
3. **Test Plan** - Test strategy to validate changes without regressions

Each phase produces a markdown document, creating a complete refactoring proposal that can be reviewed before implementation.

### Output Structure

**Ask the user for an output directory** (e.g., `./docs/refactoring/` or `./proposals/`).

Create a subfolder for the refactoring effort:
```
{output-directory}/
└── {component-name}-refactor/
    ├── 01-research.md      # Phase 1: Component Analysis
    ├── 02-proposal.md      # Phase 2: Change Proposals
    └── 03-test-plan.md     # Phase 3: Test Strategy
```

For multi-component refactoring, create subfolders:
```
{output-directory}/
└── {thread-name}-refactor/
    ├── component-a/
    │   ├── 01-research.md
    │   ├── 02-proposal.md
    │   └── 03-test-plan.md
    └── component-b/
        ├── 01-research.md
        ├── 02-proposal.md
        └── 03-test-plan.md
```

---

## Phase 1: Research

**Goal**: Comprehensive understanding of the component before proposing changes.

For multi-component refactoring, use **parallel Explore agents** to research each component simultaneously, then synthesize findings.

### Step 1: Component Inventory (Use /codebase-librarian)

Start with the `/codebase-librarian` skill to establish baseline understanding:
- Project foundation (language, tooling)
- Entry points relevant to the component
- Services the component interacts with
- Infrastructure dependencies
- Domain model elements involved

This provides context for the deeper component analysis that follows.

### Step 2: Component Deep Dive

After the inventory, analyze the specific component(s) being refactored.

**Understand how it works:**
- Core responsibilities and behavior
- Internal structure and control flow
- State management and data transformations
- Error handling patterns
- Configuration and initialization

**Understand instantiation and usage:**
- Where is it instantiated?
- How many instantiation patterns exist?
- What parameters/dependencies are injected?
- Is it a singleton, factory-created, or ad-hoc?

**Map the surroundings:**
- **Dependents** (what calls this component)
- **Dependencies** (what this component calls)
- **Before**: What happens before invocation?
- **After**: What happens after invocation?

### Step 3: Call Graph

Create a visual representation of the component's call relationships:

```
┌─────────────────────────────────────────────────────────────┐
│                        CALLERS                              │
├─────────────────────────────────────────────────────────────┤
│  OrderController.create()  ──┐                              │
│  OrderController.update()  ──┼──► PaymentService            │
│  CheckoutWorker.process()  ──┘                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PaymentService                           │
├─────────────────────────────────────────────────────────────┤
│  processPayment()                                           │
│  refundPayment()                                            │
│  validateCard()                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DEPENDENCIES                           │
├─────────────────────────────────────────────────────────────┤
│  StripeClient          │  PaymentRepository                 │
│  FraudDetectionService │  EventEmitter                      │
└─────────────────────────────────────────────────────────────┘
```

### Research Output Format

Write to `01-research.md`:

```markdown
# Research: [Component Name]

**Generated**: [Date]
**Scope**: [Component path/module]

## Executive Summary

[2-3 paragraphs covering:]
- Component's purpose and role in the system
- Key findings about current implementation
- Areas of concern or complexity discovered

## Component Analysis

### Core Behavior
[What the component does, its responsibilities]

### Internal Structure
[Classes, functions, modules that compose it]

### State & Data Flow
[How data moves through the component]

## Instantiation Patterns

| Location | Pattern | Parameters | Frequency |
|----------|---------|------------|-----------|
| `src/api/orders.ts:45` | Direct new | config, logger | 3 places |
| `src/workers/checkout.ts:12` | Factory | config | 1 place |

## Dependency Analysis

### Dependents (Who calls this)

| Caller | Method | Context |
|--------|--------|---------|
| `OrderController` | `processPayment()` | HTTP request handling |
| `CheckoutWorker` | `processPayment()` | Background job |

### Dependencies (What this calls)

| Dependency | Usage | Abstracted? |
|------------|-------|-------------|
| `StripeClient` | Payment processing | No - direct SDK |
| `PaymentRepository` | Persistence | Yes - interface |

### Execution Context

**Before invocation**: [What typically happens before this component is called]
**After invocation**: [What happens with the result]

## Call Graph

[ASCII diagram as shown above]

## Key Observations

- [Notable pattern or concern 1]
- [Notable pattern or concern 2]
- [Areas that may need attention during refactoring]
```

---

## Phase 2: Proposal

**Persona: Pragmatic Senior Engineer**

*Mindset: Balance ideal architecture with practical constraints. Quick wins build momentum and trust. Large changes need clear justification. Every change should have a clear "why".*

### Proposal Structure

Order changes from quick wins to complex restructuring:

1. **Quick Wins** - Small, low-risk improvements (hours)
2. **Medium Changes** - Meaningful refactoring (days)
3. **Large Restructuring** - Significant architectural changes (weeks)

### For Each Change

Provide:

1. **Problem Statement** - What's wrong and why it matters
2. **Proposed Solution** - Concrete approach
3. **Code Samples** - Before and after comparisons
4. **Impact Analysis** - Files affected, risks, dependencies
5. **Pros and Cons** - Honest trade-off assessment

### Proposal Output Format

Write to `02-proposal.md`:

```markdown
# Refactoring Proposal: [Component Name]

**Generated**: [Date]
**Based on**: 01-research.md

## Executive Summary

[Overview of proposed changes, expected benefits, and effort distribution]

---

## Quick Wins

### 1. [Change Title]

**Problem**
[What's wrong - reference research findings]

**Solution**
[What to do]

**Before**
```typescript
// src/services/payment.ts:45-52
class PaymentService {
  constructor() {
    this.stripe = new Stripe(process.env.STRIPE_KEY);
  }
}
```

**After**
```typescript
// src/services/payment.ts:45-55
class PaymentService {
  constructor(private readonly paymentGateway: PaymentGateway) {}
}

// src/ports/payment-gateway.ts (new)
interface PaymentGateway {
  charge(amount: number, currency: string): Promise<ChargeResult>;
}
```

**Impact**
- Files modified: `src/services/payment.ts`, `src/composition-root.ts`
- Files created: `src/ports/payment-gateway.ts`
- Risk: Low - constructor signature change requires updating instantiation sites

**Pros**
- Enables unit testing without Stripe sandbox
- Prepares for potential payment provider switch

**Cons**
- Adds indirection layer
- Requires updating 3 instantiation sites

---

## Medium Changes

### 2. [Change Title]

[Same structure as above]

---

## Large Restructuring

### 3. [Change Title]

[Same structure - may be higher level for larger efforts]

---

## Implementation Order

Recommended sequence considering dependencies:

1. [Quick Win 1] - No dependencies
2. [Quick Win 2] - No dependencies
3. [Medium Change 1] - Depends on Quick Win 1
4. [Large Restructuring] - Depends on Medium Change 1

## Risk Assessment

| Change | Risk Level | Mitigation |
|--------|------------|------------|
| [Change 1] | Low | Existing tests cover behavior |
| [Change 2] | Medium | Add integration tests first |
| [Change 3] | High | Feature flag, gradual rollout |
```

---

## Phase 3: Test Plan

**Goal**: Design tests that validate refactoring without regressions.

### Analysis Steps

1. **Audit existing tests** - What's already covered?
2. **Identify gaps** - What behavior lacks test coverage?
3. **Design new tests** - Focus on integration over unit tests
4. **Minimize mocks** - Prefer real dependencies when feasible

### Test Philosophy

- **Favor integration tests** - Test real interactions between components
- **Use mocks sparingly** - Only for external services, not internal dependencies
- **Test behavior, not implementation** - Tests should survive refactoring
- **Cover edge cases discovered in research** - Use Phase 1 findings

### Test Plan Output Format

Write to `03-test-plan.md`:

```markdown
# Test Plan: [Component Name] Refactoring

**Generated**: [Date]
**Based on**: 01-research.md, 02-proposal.md

## Executive Summary

[Overview of testing strategy and coverage goals]

## Current Test Coverage

### Existing Tests

| Test File | Type | Coverage | Notes |
|-----------|------|----------|-------|
| `payment.test.ts` | Unit | Core payment flow | Heavy mocking |
| `checkout.integration.ts` | Integration | Happy path only | No error cases |

### Coverage Gaps

- [ ] Error handling in `processPayment()`
- [ ] Concurrent payment attempts
- [ ] Retry behavior after transient failures

## Test Strategy

### Integration Tests (Preferred)

Tests that exercise real component interactions:

**Test: Payment processing end-to-end**
```typescript
// tests/integration/payment.test.ts
describe('PaymentService', () => {
  let service: PaymentService;
  let testDb: TestDatabase;

  beforeEach(async () => {
    testDb = await TestDatabase.create();
    service = new PaymentService(
      new StripeTestGateway(),  // Test mode, real API
      new PaymentRepository(testDb)
    );
  });

  it('processes payment and persists record', async () => {
    const result = await service.processPayment({
      amount: 1000,
      currency: 'usd',
      customerId: 'cust_123'
    });

    expect(result.status).toBe('succeeded');

    const record = await testDb.payments.findById(result.id);
    expect(record).toBeDefined();
    expect(record.amount).toBe(1000);
  });
});
```

**Why integration over unit**: Tests real database interactions, actual service coordination, and catches integration bugs that mocks would hide.

### Unit Tests (When Necessary)

Use unit tests with mocks only when:
- External API calls would be slow/costly
- Testing pure business logic in isolation
- Simulating error conditions difficult to reproduce

**Test: Fraud detection logic**
```typescript
// tests/unit/fraud-detection.test.ts
describe('FraudDetector', () => {
  it('flags high-risk transactions', () => {
    const detector = new FraudDetector();

    const result = detector.assess({
      amount: 10000,
      newCustomer: true,
      internationalCard: true
    });

    expect(result.riskLevel).toBe('high');
    expect(result.requiresReview).toBe(true);
  });
});
```

**Why unit here**: Pure logic, no external dependencies, fast execution.

## Tests Per Proposal Change

### For Change 1: [Extract PaymentGateway Interface]

| Test | Type | Purpose |
|------|------|---------|
| `gateway-contract.test.ts` | Contract | Verify adapter implements interface correctly |
| `payment-with-mock-gateway.test.ts` | Unit | Verify service works with any gateway |

**New test:**
```typescript
// tests/contract/payment-gateway.test.ts
describe('PaymentGateway contract', () => {
  const adapters = [
    ['Stripe', () => new StripePaymentAdapter(stripeTestClient)],
    ['Mock', () => new MockPaymentAdapter()],
  ];

  test.each(adapters)('%s adapter implements contract', (name, createAdapter) => {
    const adapter = createAdapter();

    expect(adapter.charge).toBeDefined();
    expect(adapter.refund).toBeDefined();
  });
});
```

### For Change 2: [Change Title]

[Similar structure]

## Mock Usage Guidelines

**Acceptable mocks:**
- External payment APIs (Stripe, PayPal)
- Email services
- SMS/notification services
- Third-party APIs with rate limits

**Avoid mocking:**
- Internal services (use real implementations)
- Repositories (use test database)
- Domain logic (test directly)

## Verification Checklist

Before considering refactoring complete:

- [ ] All existing tests pass
- [ ] New integration tests cover changed behavior
- [ ] Edge cases from research are tested
- [ ] Error handling paths have coverage
- [ ] No increase in mock usage
- [ ] CI pipeline green
```

---

## References

For detailed guidance on each phase:

- **Phase 1 deep dive**: See [references/research-phase.md](references/research-phase.md) for advanced research techniques
- **Phase 2 patterns**: See [references/proposal-phase.md](references/proposal-phase.md) for common refactoring patterns
- **Phase 3 testing**: See [references/test-plan-phase.md](references/test-plan-phase.md) for test design patterns
