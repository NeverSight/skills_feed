---
name: playwright-best-practices
description: Comprehensive guide for writing, debugging, and maintaining Playwright tests in TypeScript. Use when writing new Playwright tests, reviewing test code, fixing flaky tests, debugging test failures, setting up test infrastructure, implementing Page Object Model, configuring CI/CD pipelines, optimizing test performance, fixing selector issues, handling authentication, mocking APIs, organizing test suites, or troubleshooting Playwright issues. Covers E2E, component, API, and visual regression testing.
---

# Playwright Best Practices

This skill provides comprehensive guidance for all aspects of Playwright test development, from writing new tests to debugging and maintaining existing test suites.

## Activity-Based Reference Guide

Consult these references based on what you're doing:

### Writing New Tests

**When to use**: Creating new test files, writing test cases, implementing test scenarios

| Activity | Reference Files |
|----------|----------------|
| **Writing E2E tests** | [test-organization.md](references/test-organization.md), [locators.md](references/locators.md), [assertions-waiting.md](references/assertions-waiting.md) |
| **Writing component tests** | [test-organization.md](references/test-organization.md), [locators.md](references/locators.md) |
| **Writing API tests** | [test-organization.md](references/test-organization.md), [assertions-waiting.md](references/assertions-waiting.md) |
| **Writing visual regression tests** | [test-organization.md](references/test-organization.md) |
| **Structuring test code with POM** | [page-object-model.md](references/page-object-model.md), [test-organization.md](references/test-organization.md) |
| **Setting up test data/fixtures** | [fixtures-hooks.md](references/fixtures-hooks.md), [test-organization.md](references/test-organization.md) |
| **Handling authentication** | [fixtures-hooks.md](references/fixtures-hooks.md), [test-organization.md](references/test-organization.md) |

### Debugging & Troubleshooting

**When to use**: Test failures, element not found, timeouts, unexpected behavior

| Activity | Reference Files |
|----------|----------------|
| **Debugging test failures** | [debugging.md](references/debugging.md), [assertions-waiting.md](references/assertions-waiting.md) |
| **Fixing flaky tests** | [debugging.md](references/debugging.md), [assertions-waiting.md](references/assertions-waiting.md), [fixtures-hooks.md](references/fixtures-hooks.md) |
| **Fixing selector issues** | [locators.md](references/locators.md), [debugging.md](references/debugging.md) |
| **Investigating timeout issues** | [assertions-waiting.md](references/assertions-waiting.md), [debugging.md](references/debugging.md) |
| **Using trace viewer** | [debugging.md](references/debugging.md) |
| **Debugging race conditions** | [debugging.md](references/debugging.md), [assertions-waiting.md](references/assertions-waiting.md) |

### Refactoring & Maintenance

**When to use**: Improving existing tests, code review, reducing duplication

| Activity | Reference Files |
|----------|----------------|
| **Refactoring to Page Object Model** | [page-object-model.md](references/page-object-model.md), [test-organization.md](references/test-organization.md) |
| **Improving test organization** | [test-organization.md](references/test-organization.md), [page-object-model.md](references/page-object-model.md) |
| **Extracting common setup/teardown** | [fixtures-hooks.md](references/fixtures-hooks.md) |
| **Replacing brittle selectors** | [locators.md](references/locators.md) |
| **Removing explicit waits** | [assertions-waiting.md](references/assertions-waiting.md) |

### Infrastructure & Configuration

**When to use**: Setting up projects, configuring CI/CD, optimizing performance

| Activity | Reference Files |
|----------|----------------|
| **Configuring Playwright project** | [test-organization.md](references/test-organization.md), [fixtures-hooks.md](references/fixtures-hooks.md) |
| **Setting up CI/CD pipelines** | [ci-cd.md](references/ci-cd.md), [performance.md](references/performance.md) |
| **Optimizing test performance** | [performance.md](references/performance.md), [test-organization.md](references/test-organization.md) |
| **Configuring parallel execution** | [performance.md](references/performance.md) |
| **Setting up test reporting** | [ci-cd.md](references/ci-cd.md), [debugging.md](references/debugging.md) |

### Advanced Patterns

**When to use**: Complex scenarios, API mocking, network interception

| Activity | Reference Files |
|----------|----------------|
| **Mocking API responses** | [test-organization.md](references/test-organization.md), [fixtures-hooks.md](references/fixtures-hooks.md) |
| **Network interception** | [test-organization.md](references/test-organization.md), [assertions-waiting.md](references/assertions-waiting.md) |
| **Custom fixtures** | [fixtures-hooks.md](references/fixtures-hooks.md) |
| **Advanced waiting strategies** | [assertions-waiting.md](references/assertions-waiting.md) |

## Quick Decision Tree

```
What are you doing?
│
├─ Writing a new test?
│  ├─ E2E test → test-organization.md, locators.md, assertions-waiting.md
│  ├─ Component test → test-organization.md, locators.md
│  ├─ API test → test-organization.md, assertions-waiting.md
│  └─ Visual test → test-organization.md
│
├─ Test is failing/flaky?
│  ├─ Element not found → locators.md, debugging.md
│  ├─ Timeout issues → assertions-waiting.md, debugging.md
│  ├─ Race conditions → debugging.md, assertions-waiting.md
│  └─ General debugging → debugging.md
│
├─ Refactoring existing code?
│  ├─ Implementing POM → page-object-model.md
│  ├─ Improving selectors → locators.md
│  └─ Extracting fixtures → fixtures-hooks.md
│
└─ Setting up infrastructure?
   ├─ CI/CD → ci-cd.md
   ├─ Performance → performance.md
   └─ Project config → test-organization.md, fixtures-hooks.md
```
