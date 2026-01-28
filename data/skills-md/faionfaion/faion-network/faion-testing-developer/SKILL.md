---
name: faion-testing-developer
description: "Testing: unit, integration, E2E, TDD, mocking, security testing."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Testing Developer Skill

Testing strategies and implementation covering unit tests, integration tests, E2E tests, TDD workflow, and testing best practices.

## Purpose

Handles all aspects of software testing including test design, implementation, mocking, fixtures, and testing frameworks.

## When to Use

- Unit testing strategies
- Integration testing
- End-to-end (E2E) testing
- Test-driven development (TDD)
- Mocking and stubbing
- Test fixtures and factories
- Security testing
- Code coverage analysis
- Language-specific testing (pytest, Jest, Go testing, etc.)

## Methodologies

| Category | Methodology | File |
|----------|-------------|------|
| **Testing Levels** |
| Unit testing | Unit test patterns, isolation, assertions | unit-testing.md |
| Integration testing | Integration test patterns, test containers | integration-testing.md |
| E2E testing basics | End-to-end test patterns | e2e-testing.md |
| E2E testing alt | E2E strategies | testing-e2e.md |
| **Testing Practices** |
| TDD workflow | Red-green-refactor, TDD cycle | tdd-workflow.md |
| Mocking strategies | Mocks, stubs, spies, fakes | mocking-strategies.md |
| Test fixtures | Fixture patterns, factory pattern | test-fixtures.md |
| Testing patterns | General testing patterns | testing-patterns.md |
| **Security** |
| Security testing | SAST, DAST, penetration testing | security-testing.md |
| **Language-Specific** |
| pytest testing | pytest fixtures, parametrize, markers | testing-pytest.md |
| JavaScript testing | Jest, Vitest, React Testing Library | testing-javascript.md |
| Go testing | Go testing stdlib, table tests | testing-go.md |

## Tools by Language

**Python:** pytest, unittest, hypothesis, factory-boy, faker
**JavaScript:** Jest, Vitest, Mocha, Chai, React Testing Library, Cypress, Playwright
**Go:** testing stdlib, testify, gomock
**Java:** JUnit 5, Mockito, AssertJ
**C#:** xUnit, NUnit, Moq, FluentAssertions

**E2E:** Playwright, Cypress, Selenium, Puppeteer
**Security:** OWASP ZAP, Burp Suite, Snyk, SonarQube

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-python-developer | pytest, Django testing |
| faion-javascript-developer | Jest, Vitest testing |
| faion-backend-developer | Language-specific testing |
| faion-api-developer | API testing, contract testing |
| faion-devtools-developer | Code coverage, test automation |

## Integration

Invoked by parent skill `faion-software-developer` for testing-related work.

---

*faion-testing-developer v1.0 | 12 methodologies*
