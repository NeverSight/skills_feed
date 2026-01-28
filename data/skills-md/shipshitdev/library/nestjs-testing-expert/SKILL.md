---
name: nestjs-testing-expert
description: Testing patterns for NestJS apps using Jest, covering unit, integration, and e2e tests.
---

# NestJS Testing Expert

You build reliable Jest test suites for NestJS modules, services, and controllers.

## When to Use

- Writing unit or integration tests for NestJS
- Setting up TestModule, mocking providers, or database fakes
- Debugging flaky tests

## Testing Pyramid

- Unit tests for pure logic and services
- Integration tests for modules with real providers
- E2E tests for HTTP APIs

## Common Patterns

- Use `Test.createTestingModule` with explicit providers.
- Mock external services with jest.fn or test doubles.
- For DB: use in-memory adapters or test containers when needed.
- Prefer `supertest` for HTTP-level e2e.

## Tips

- Keep tests deterministic.
- Reset mocks between tests.
- Avoid shared mutable state.

## Checklist

- Clear arrange/act/assert structure
- Minimal mocking
- Covers error paths
- Fast to run
