---
name: tdd
description: Test-Driven Development methodology and red-green-refactor workflow (formerly test-tdd). This skill should be used when practicing TDD, writing tests first, designing tests before implementation, or reviewing test-first approaches. Triggers on "write tests first", "test before code", "red green refactor", "test driven development". This skill does NOT cover Vitest framework specifics (use vitest skill) or API mocking with MSW (use msw skill).
---

# Community Test-Driven Development Best Practices

Comprehensive guide to Test-Driven Development practices, designed for AI agents and LLMs. Contains 42 rules across 8 categories, prioritized by impact to guide test writing, refactoring, and code generation.

## When to Apply

Reference these guidelines when:
- Writing new tests using TDD workflow
- Implementing the red-green-refactor cycle
- Designing test structure and organization
- Creating test data and fixtures
- Reviewing or refactoring existing test suites

## TDD Workflow

1. **RED**: Write a failing test that defines desired behavior
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Clean up code while keeping tests green
4. Repeat for each new behavior

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Red-Green-Refactor Cycle | CRITICAL | `cycle-` |
| 2 | Test Design Principles | CRITICAL | `design-` |
| 3 | Test Isolation & Dependencies | HIGH | `isolate-` |
| 4 | Test Data Management | HIGH | `data-` |
| 5 | Assertions & Verification | MEDIUM | `assert-` |
| 6 | Test Organization & Structure | MEDIUM | `org-` |
| 7 | Test Performance & Reliability | MEDIUM | `perf-` |
| 8 | Test Pyramid & Strategy | LOW | `strat-` |

## Quick Reference

### 1. Red-Green-Refactor Cycle (CRITICAL)

- `cycle-write-test-first` - Write the Test Before the Implementation
- `cycle-minimal-code-to-pass` - Write Only Enough Code to Pass the Test
- `cycle-refactor-after-green` - Refactor Immediately After Green
- `cycle-verify-test-fails-first` - Verify the Test Fails Before Writing Code
- `cycle-small-increments` - Take Small Incremental Steps
- `cycle-maintain-test-list` - Maintain a Test List

### 2. Test Design Principles (CRITICAL)

- `design-test-behavior-not-implementation` - Test Behavior Not Implementation
- `design-one-assertion-per-test` - One Logical Assertion Per Test
- `design-descriptive-test-names` - Use Descriptive Test Names
- `design-aaa-pattern` - Follow the Arrange-Act-Assert Pattern
- `design-test-edge-cases` - Test Edge Cases and Boundaries
- `design-avoid-logic-in-tests` - Avoid Logic in Tests

### 3. Test Isolation & Dependencies (HIGH)

- `isolate-mock-external-dependencies` - Mock External Dependencies
- `isolate-no-shared-state` - Avoid Shared Mutable State Between Tests
- `isolate-deterministic-tests` - Write Deterministic Tests
- `isolate-prefer-stubs-over-mocks` - Prefer Stubs Over Mocks for Queries
- `isolate-use-dependency-injection` - Use Dependency Injection for Testability

### 4. Test Data Management (HIGH)

- `data-use-factories` - Use Factories for Test Data Creation
- `data-minimal-setup` - Keep Test Setup Minimal
- `data-avoid-mystery-guests` - Avoid Mystery Guests
- `data-unique-identifiers` - Use Unique Identifiers Per Test
- `data-builder-pattern` - Use Builder Pattern for Complex Objects

### 5. Assertions & Verification (MEDIUM)

- `assert-specific-assertions` - Use Specific Assertions
- `assert-error-messages` - Assert on Error Messages and Types
- `assert-no-assertions-antipattern` - Every Test Must Have Assertions
- `assert-custom-matchers` - Create Custom Matchers for Domain Assertions
- `assert-snapshot-testing` - Use Snapshot Testing Judiciously

### 6. Test Organization & Structure (MEDIUM)

- `org-group-by-behavior` - Group Tests by Behavior Not Method
- `org-file-structure` - Follow Consistent Test File Structure
- `org-setup-teardown` - Use Setup and Teardown Hooks Appropriately
- `org-test-utilities` - Extract Reusable Test Utilities
- `org-parameterized-tests` - Use Parameterized Tests for Variations

### 7. Test Performance & Reliability (MEDIUM)

- `perf-fast-unit-tests` - Keep Unit Tests Under 100ms
- `perf-avoid-network-calls` - Eliminate Network Calls in Unit Tests
- `perf-fix-flaky-tests` - Fix Flaky Tests Immediately
- `perf-parallelize-tests` - Parallelize Independent Tests
- `perf-avoid-sleep` - Avoid Arbitrary Sleep Calls

### 8. Test Pyramid & Strategy (LOW)

- `strat-test-pyramid` - Follow the Test Pyramid
- `strat-mutation-testing` - Use Mutation Testing to Validate Test Quality
- `strat-coverage-targets` - Set Meaningful Coverage Targets
- `strat-integration-boundaries` - Test Integration at Service Boundaries
- `strat-e2e-critical-paths` - Limit E2E Tests to Critical User Paths

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules
- [cycle-write-test-first](references/cycle-write-test-first.md) - Write the Test Before the Implementation
- [design-aaa-pattern](references/design-aaa-pattern.md) - Follow the Arrange-Act-Assert Pattern

## Related Skills

- For Vitest framework specifics, see `vitest` skill
- For API mocking with MSW, see `msw` skill

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
