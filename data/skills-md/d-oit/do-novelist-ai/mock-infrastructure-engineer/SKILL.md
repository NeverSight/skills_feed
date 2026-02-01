---
name: mock-infrastructure-engineer
description:
  Creates and optimizes MSW (Mock Service Worker) handlers for Playwright E2E
  tests, implementing handler caching, fixture management, and AI Gateway
  mocking patterns. Use when mock setup is slow or test data needs
  centralization.
---

# Mock Infrastructure Engineer

## Quick Start

This skill optimizes mock infrastructure for E2E tests:

1. **Handler caching**: Reduce mock setup from 1.7s to 200ms per test (88%
   faster)
2. **Fixture management**: Centralize test data for consistency
3. **AI Gateway mocking**: Mock Gemini API responses efficiently

### When to Use

- Mock setup overhead exceeds 500ms per test
- E2E tests need AI Gateway mocking
- Test data scattered across files
- Inconsistent responses across test runs

## Optimized Mock Pattern

### Handler Caching System

This pattern achieved 88% performance improvement:

```typescript
// tests/utils/mock-ai-gateway.ts
import type { Page, Route } from '@playwright/test';

interface GeminiMockConfig {
  shouldFail?: boolean;
  delay?: number;
  customResponse?: any;
}

// Pre-built static response (Object.freeze prevents mutation)
const DEFAULT_MOCK_RESPONSE = Object.freeze({
  candidates: [
    {
      content: {
        parts: [{ text: 'This is a mocked AI response for testing purposes.' }],
        role: 'model',
      },
      finishReason: 'STOP',
      index: 0,
    },
  ],
});

// Handler cache (reuse handlers across tests)
const handlerCache = new Map<string, (route: Route) => Promise<void>>();

function createGeminiRouteHandler(config: GeminiMockConfig = {}) {
  const { shouldFail = false, delay = 0, customResponse } = config;

  return async (route: Route) => {
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
    }

    if (shouldFail) {
      await route.abort('failed');
      return;
    }

    const response = customResponse || DEFAULT_MOCK_RESPONSE;
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(response),
    });
  };
}

// Optimized setup function
export async function setupGeminiMock(
  page: Page,
  config: GeminiMockConfig = {},
): Promise<void> {
  const cacheKey = JSON.stringify(config);
  let handler = handlerCache.get(cacheKey);

  if (!handler) {
    handler = createGeminiRouteHandler(config);
    handlerCache.set(cacheKey, handler);
  }

  await page.route('**/v1beta/models/**', handler);
}
```

**Performance Results**:

- Mock setup: 1.7s → 200ms (88% faster)
- Memory allocations: 110KB → 6KB (95% reduction)
- Handler creations: 55+ → 2-4 (96% reduction)

## AI Gateway Response Patterns

### Success Response

```typescript
const successResponse = {
  candidates: [
    {
      content: {
        parts: [{ text: 'Generated content here' }],
        role: 'model',
      },
      finishReason: 'STOP',
      index: 0,
      safetyRatings: [
        {
          category: 'HARM_CATEGORY_HARASSMENT',
          probability: 'NEGLIGIBLE',
        },
      ],
    },
  ],
  promptFeedback: { safetyRatings: [] },
};
```

### Error Response

```typescript
const errorResponse = {
  error: {
    code: 429,
    message: 'Resource has been exhausted (e.g. check quota).',
    status: 'RESOURCE_EXHAUSTED',
  },
};
```

### Streaming Response

```typescript
async function handleStreamingRequest(route: Route) {
  const chunks = [
    'data: {"candidates":[{"content":{"parts":[{"text":"First "}]}}]}\\n\\n',
    'data: {"candidates":[{"content":{"parts":[{"text":"chunk "}]}}]}\\n\\n',
    'data: {"candidates":[{"content":{"parts":[{"text":"here"}]}}]}\\n\\n',
    'data: [DONE]\\n\\n',
  ];

  await route.fulfill({
    status: 200,
    contentType: 'text/event-stream',
    body: chunks.join(''),
  });
}
```

## Fixture Management

### Fixture Registry Pattern

```typescript
// tests/fixtures/ai-responses.fixture.ts
export const aiResponseFixtures = {
  outline: {
    text: 'Chapter 1: Introduction\\nChapter 2: Rising Action\\nChapter 3: Climax',
    metadata: { chapters: 3, wordCount: 15 },
  },
  character: {
    text: 'Name: John Doe\\nAge: 35\\nBackground: Former detective',
    metadata: { fields: 3 },
  },
  worldBuilding: {
    text: 'Location: New York City\\nTime Period: 2024\\nSetting: Urban fantasy',
    metadata: { elements: 3 },
  },
};

// Usage in tests
import { aiResponseFixtures } from '../fixtures/ai-responses.fixture';

await setupGeminiMock(page, {
  customResponse: {
    candidates: [
      {
        content: {
          parts: [{ text: aiResponseFixtures.outline.text }],
          role: 'model',
        },
      },
    ],
  },
});
```

### Fixture Factory Pattern

```typescript
// tests/fixtures/project.fixture.ts
export function createProjectFixture(
  overrides: Partial<Project> = {},
): Project {
  return {
    id: crypto.randomUUID(),
    title: 'Test Project',
    description: 'Test project description',
    genre: 'fantasy',
    targetWordCount: 50000,
    createdAt: Date.now(),
    updatedAt: Date.now(),
    ...overrides,
  };
}

// Usage
const project = createProjectFixture({ title: 'My Novel', genre: 'scifi' });
```

## Global Setup for Performance

### Browser Warm-Up

Add to `tests/global-setup.ts` for 66% faster first test:

```typescript
import { chromium, type FullConfig } from '@playwright/test';

export default async function globalSetup(config: FullConfig): Promise<void> {
  const browser = await chromium.launch();
  await browser.close();
}
```

Configure in `playwright.config.ts`:

```typescript
export default defineConfig({
  globalSetup: require.resolve('./tests/global-setup'),
  // ... rest of config
});
```

## Test Examples

### Example 1: Custom Response Mock

```typescript
test('should generate character description', async ({ page }) => {
  await setupGeminiMock(page, {
    customResponse: {
      candidates: [
        {
          content: {
            parts: [
              {
                text: 'Name: Sarah Chen\\nAge: 28\\nOccupation: Software Engineer',
              },
            ],
            role: 'model',
          },
          finishReason: 'STOP',
        },
      ],
    },
  });

  await page.goto('/ai-generation');
  await page.getByRole('button', { name: 'Generate Character' }).click();
  await expect(page.getByText('Name: Sarah Chen')).toBeVisible();
});
```

### Example 2: Error Handling

```typescript
test('should handle AI generation failure', async ({ page }) => {
  await setupGeminiMock(page, { shouldFail: true });

  await page.goto('/ai-generation');
  await page.getByRole('button', { name: 'Generate' }).click();

  await expect(page.getByText('Generation failed')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Retry' })).toBeVisible();
});
```

### Example 3: Loading State

```typescript
test('should show loading state during generation', async ({ page }) => {
  await setupGeminiMock(page, { delay: 2000 });

  await page.goto('/ai-generation');
  await page.getByRole('button', { name: 'Generate' }).click();

  // Loading indicator appears
  await expect(page.getByTestId('loading-spinner')).toBeVisible();

  // Wait for response
  await expect(page.getByTestId('loading-spinner')).not.toBeVisible({
    timeout: 5000,
  });
  await expect(page.getByTestId('generated-content')).toBeVisible();
});
```

## Best Practices

### Always Use Handler Caching

```typescript
// ✅ Use caching
await setupGeminiMock(page, config);

// ❌ Create handler inline (slow)
await page.route('**/api/**', async route => {
  // Handler creation on every call
});
```

### Freeze Static Responses

```typescript
// ✅ Frozen response (immutable)
const RESPONSE = Object.freeze({ data: 'value' });

// ❌ Mutable response (can be modified)
const response = { data: 'value' };
```

### Use Fixtures for Test Data

```typescript
// ✅ Reusable fixture
const project = createProjectFixture({ title: 'Test' });

// ❌ Inline test data (hard to maintain)
const project = {
  id: '123',
  title: 'Test',
  createdAt: 1234567890,
  // ... 20 more fields
};
```

### Minimize Async Operations

```typescript
// ✅ Single route registration
await page.route('**/api/**', cachedHandler);

// ❌ Multiple route registrations (slower)
await page.route('**/api/endpoint1', handler1);
await page.route('**/api/endpoint2', handler2);
await page.route('**/api/endpoint3', handler3);
```

## Common Issues

**Mock not intercepting requests**

- Debug route matching:
  `page.route('**/*', route => console.log(route.request().url()))`
- Verify pattern matches actual request URL

**Responses inconsistent across tests**

- Use `Object.freeze()` for static responses
- Implement fixture factories for dynamic data

**Mock setup still slow despite caching**

- Verify cache is working: `console.log('Cache size:', handlerCache.size)`
- Should be small (2-4), not growing per test

**Test isolation broken (state leaking)**

- Clear cache between tests if needed: `handlerCache.clear()`
- Or use unique config per test

## Success Metrics

- Mock setup time < 200ms per test
- Total mock overhead < 15s for full suite
- Cache hit rate > 90%
- Memory usage < 10KB per test
- Handler reuse: 96% reduction in creations

## References

See tests/docs/ for detailed analysis:

- MOCK-OPTIMIZATION-GUIDE.md - Implementation patterns
- MOCK-PERFORMANCE-ANALYSIS.md - Optimization results

External documentation:

- Playwright Network Mocking: https://playwright.dev/docs/network
