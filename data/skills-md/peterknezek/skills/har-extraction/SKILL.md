---
name: har-extraction
description: Use when user has a HAR file and wants to create API mocks, or when setting up MSW mocking for tests/Storybook from network recordings.
dependencies:
  - har-to-mocks
  - mocks-to-msw
  - msw
---

# HAR Extraction & Mock Generation

Extract JSON mocks from HAR files and integrate with MSW for testing and Storybook.

## Workflow

```
HAR File → har-to-mocks → JSON Mocks → mocks-to-msw → MSW Handlers → Storybook/Tests
```

## Quick Start

### 1. Extract mocks from HAR file

```bash
npx har-to-mocks recording.har ./src/mocks --interactive
```

### 2. Generate type-safe imports

```bash
npx mocks-to-msw generate ./src/mocks
```

### 3. Create handlers

```typescript
// src/mocks/handlers.ts
import { createMockHandler } from 'mocks-to-msw';
import { mocks } from './mocks';

export const { mock, handlers } = createMockHandler<keyof typeof mocks>({
  mocks,
  debug: true,
});
```

### 4. Initialize MSW

```bash
npx msw init ./public --save
```

## Examples

### Example 1: Extract mocks from HAR

**User:** "I have a network.har file, extract the API mocks from it"

**Action:**
```bash
npx har-to-mocks network.har ./src/mocks --interactive
npx mocks-to-msw generate ./src/mocks
```

**Output:** "Extracted 12 endpoints to ./src/mocks and generated mocks.ts registry."

---

### Example 2: Setup MSW for Storybook

**User:** "Set up the mocks to work with Storybook"

**Action:**
1. Install addon: `npm install msw-storybook-addon --save-dev`
2. Add to `.storybook/main.ts`:
   ```typescript
   addons: ['msw-storybook-addon'],
   staticDirs: ['../public'],
   ```
3. Configure `.storybook/preview.tsx`:
   ```typescript
   import { initialize, mswLoader } from 'msw-storybook-addon';
   import { handlers } from '../src/mocks/handlers';

   initialize();

   export default {
     parameters: { msw: { handlers } },
     loaders: [mswLoader],
   };
   ```

**Output:** "Configured MSW addon for Storybook. Mocks are now active in all stories."

---

### Example 3: Filter specific endpoints

**User:** "Extract only POST requests to /api/users from the HAR"

**Action:**
```bash
npx har-to-mocks recording.har ./src/mocks --url "/api/users" --method POST
```

**Output:** "Extracted POST /api/users endpoint to ./src/mocks/api/users/POST.json"

---

### Example 4: Override mocks in a story

**User:** "I want to show an error state in my UserList story"

**Action:** Add to story file:
```typescript
export const WithError: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get('*/api/users', () => HttpResponse.json(null, { status: 500 })),
      ],
    },
  },
};
```

**Output:** "Added error handler override. The story now displays the error state."

## CLI Reference

| Command | Description |
|---------|-------------|
| `npx har-to-mocks <har> <output> --interactive` | Interactive endpoint selection |
| `npx har-to-mocks <har> <output> --url <pattern>` | Filter by URL |
| `npx har-to-mocks <har> <output> --method <GET\|POST\|...>` | Filter by HTTP method |
| `npx har-to-mocks <har> <output> --dry-run` | Preview without writing |
| `npx mocks-to-msw generate <mocks-dir>` | Generate type-safe imports |

## More Information

See [REFERENCE.md](./REFERENCE.md) for detailed documentation including:
- Recording HAR files from browser DevTools
- Full CLI options and output structure
- Complete MSW setup for browser and Node
- Storybook integration details
- Troubleshooting guide
