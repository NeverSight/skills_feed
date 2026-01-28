---
name: testing
description: Complete testing setup with Neon database branching, Playwright browser tests, integration tests, and unit tests. Isolated branches with automatic TTL cleanup.
---

# Testing

Complete testing setup with Neon database branching, Playwright browser tests, integration tests, and unit tests. Isolated branches with automatic TTL cleanup.

## Prerequisites

Complete these recipes first (in order):

### Type-Safe Environment Configuration

Type-safe environment variable validation using Zod with a Drizzle-like schema API. Supports server/public fields, feature flags, either-or constraints, and client-side protection.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/config-schema-setup
```

### Neon + Drizzle Setup

Connect a Next.js app to Neon Postgres using Drizzle ORM with optimized connection pooling for Vercel serverless functions.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/neon-drizzle-setup
```

## Cookbook - Complete These Recipes in Order

### Neon Test Branches

Create isolated Neon database branches for testing. Schema-only branches with auto-cleanup via TTL, test server orchestration, and environment variable management.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/neon-test-branches
```

### Unit Tests with Bun

Configure unit testing with Bun's built-in test runner. Fast, Jest-compatible syntax, co-located test files, and mocking support.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/unit-tests
```

### Integration Tests

Test API routes by importing handlers directly with Bun's test runner. Fast, reliable tests without HTTP overhead.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/integration-tests
```

### Browser Tests with Playwright

End-to-end browser testing with Playwright. Test user interactions, form validation, navigation, and visual feedback with full browser automation.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/playwright-tests
```

### Working with Tests

Testing strategy and workflow. Tests run in parallel with isolated data per suite. Prioritize Playwright for UI, integration tests for APIs, unit tests for logic.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/using-tests
```
