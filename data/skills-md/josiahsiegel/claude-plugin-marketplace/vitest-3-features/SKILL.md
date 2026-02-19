---
name: vitest-3-features
description: Vitest 3 Features skill
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation

---


# Vitest 3.x Features and Best Practices (2025)

## Overview

Vitest 3.0 was released in January 2025 with major improvements to reporting, browser testing, watch mode, and developer experience. This skill provides comprehensive knowledge of Vitest 3.x features and modern testing patterns.

## Major Features in Vitest 3.0+

### 1. Annotation API (Vitest 3.2+)

The annotation API allows you to add custom metadata, messages, and attachments to any test, visible in UI, HTML, JUnit, TAP, and GitHub Actions reporters.

**Usage:**
```javascript
import { test, expect } from 'vitest';

test('user authentication', async ({ task }) => {
  // Add custom annotation
  task.meta.annotation = {
    message: 'Testing OAuth2 flow with external provider',
    attachments: [
      { name: 'config', content: JSON.stringify(oauthConfig) }
    ]
  };

  const result = await authenticateUser(credentials);
  expect(result.token).toBeDefined();
});
```

**Use Cases:**
- Document complex test scenarios
- Attach debug information
- Link to external resources (tickets, docs)
- Add performance metrics
- Track test metadata for reporting

### 2. Line Number Filtering

Run specific tests by their line number in the file, enabling precise test execution from IDEs.

**CLI Usage:**
```bash
# Run test at specific line
vitest run tests/user.test.js:42

# Run multiple tests by line
vitest run tests/user.test.js:42 tests/user.test.js:67

# Works with ranges
vitest run tests/user.test.js:42-67
```

**IDE Integration:**
- VS Code: Click line number gutter
- JetBrains IDEs: Run from context menu
- Enables "run test at cursor" functionality

### 3. Enhanced Watch Mode

Smarter and more responsive watch mode with improved change detection.

**Features:**
- Detects changes more accurately
- Only re-runs affected tests
- Faster rebuild times
- Better file watching on Windows
- Reduced false positives

**Configuration:**
```javascript
export default defineConfig({
  test: {
    watch: true,
    watchExclude: ['**/node_modules/**', '**/dist/**'],
    // New in 3.0: More intelligent caching
    cache: {
      dir: '.vitest/cache'
    }
  }
});
```

### 4. Improved Test Reporting

Complete overhaul of test run reporting with reduced flicker and clearer output.

**Reporter API Changes:**
```javascript
// Custom reporter with new lifecycle
export default class CustomReporter {
  onInit(ctx) {
    // Called once at start
  }

  onTestStart(test) {
    // More reliable test start hook
  }

  onTestComplete(test) {
    // Includes full test metadata
  }

  onFinished(files, errors) {
    // Final results with all context
  }
}
```

**Benefits:**
- Less terminal flicker during test runs
- Clearer test status indicators
- Better error formatting
- Improved progress tracking

### 5. Workspace Configuration Simplification

No need for separate workspace files - define projects directly in config.

**Old Way (Vitest 2.x):**
```javascript
// vitest.workspace.js
export default ['packages/*'];
```

**New Way (Vitest 3.0):**
```javascript
// vitest.config.js
export default defineConfig({
  test: {
    workspace: [
      {
        test: {
          name: 'unit',
          include: ['tests/unit/**/*.test.js']
        }
      },
      {
        test: {
          name: 'integration',
          include: ['tests/integration/**/*.test.js']
        }
      }
    ]
  }
});
```

### 6. Enhanced Browser Testing

Improved browser mode with better performance and caching.

**Multiple Browser Instances:**
```javascript
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      instances: [
        { browser: 'chromium', name: 'chrome' },
        { browser: 'firefox', name: 'ff' },
        { browser: 'webkit', name: 'safari' }
      ]
    }
  }
});
```

**Benefits:**
- Single Vite server for all browsers
- Cached file processing
- Parallel browser execution
- Reduced startup time

### 7. Improved Coverage

Automatic exclusion of test files from coverage reports.

**Automatic Exclusions (Vitest 3.0):**
```javascript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      // Test files automatically excluded
      // No need to manually exclude *.test.js
      exclude: [
        // Only need to specify custom exclusions
        '**/node_modules/**',
        '**/dist/**'
      ]
    }
  }
});
```

### 8. Enhanced Mocking

New spy reuse and powerful matchers.

**Spy Reuse:**
```javascript
const spy = vi.fn();

// Vitest 3.0: Reuse spy on already mocked method
vi.spyOn(obj, 'method').mockImplementation(spy);
vi.spyOn(obj, 'method'); // Reuses existing spy
```

**New Matchers:**
```javascript
// toHaveBeenCalledExactlyOnceWith
expect(mockFn).toHaveBeenCalledExactlyOnceWith(arg1, arg2);

// Ensures called exactly once with exact arguments
// Fails if called 0 times, 2+ times, or with different args
```

### 9. Project Exclusion Patterns

Exclude specific projects using negative patterns.

**CLI Usage:**
```bash
# Run all except integration tests
vitest run --project=!integration

# Run all except multiple projects
vitest run --project=!integration --project=!e2e

# Combine inclusion and exclusion
vitest run --project=unit --project=!slow
```

### 10. UI Improvements

Significantly enhanced test UI with better debugging and navigation.

**New UI Features:**
- Run individual tests from UI
- Automatic scroll to failed tests
- Toggleable node_modules visibility
- Improved filtering and search
- Better test management controls
- Module graph visualization

**Launch UI:**
```bash
vitest --ui
```

## Best Practices for Vitest 3.x

### 1. Use Annotation API for Complex Tests

```javascript
test('complex payment flow', async ({ task }) => {
  task.meta.annotation = {
    message: 'Tests Stripe webhook integration',
    attachments: [
      { name: 'webhook-payload', content: JSON.stringify(payload) },
      { name: 'ticket', content: 'https://jira.company.com/TICKET-123' }
    ]
  };

  // Test implementation
});
```

### 2. Leverage Line Filtering in Development

```bash
# Quick iteration on single test
vitest run src/auth.test.js:145 --watch
```

### 3. Organize with Workspace Projects

```javascript
export default defineConfig({
  test: {
    workspace: [
      {
        test: {
          name: 'unit-fast',
          include: ['tests/unit/**/*.test.js'],
          environment: 'node'
        }
      },
      {
        test: {
          name: 'unit-dom',
          include: ['tests/unit/**/*.dom.test.js'],
          environment: 'happy-dom'
        }
      },
      {
        test: {
          name: 'integration',
          include: ['tests/integration/**/*.test.js'],
          setupFiles: ['tests/setup.js']
        }
      }
    ]
  }
});
```

### 4. Use toHaveBeenCalledExactlyOnceWith for Strict Testing

```javascript
test('should call API exactly once with correct params', () => {
  const apiSpy = vi.spyOn(api, 'fetchUser');

  renderComponent({ userId: 123 });

  // Strict assertion - fails if called 0, 2+ times or wrong args
  expect(apiSpy).toHaveBeenCalledExactlyOnceWith(123);
});
```

### 5. Optimize Watch Mode for Large Projects

```javascript
export default defineConfig({
  test: {
    watch: true,
    watchExclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/.git/**',
      '**/coverage/**'
    ],
    // Run only related tests
    changed: true,
    // Faster reruns
    isolate: false // Use with caution
  }
});
```

### 6. Custom Reporters for CI/CD

```javascript
// reporters/junit-plus.js
export default class JUnitPlusReporter {
  onFinished(files, errors) {
    const results = files.map(file => ({
      name: file.name,
      tests: file.tasks.length,
      failures: file.tasks.filter(t => t.result?.state === 'fail').length,
      // Add annotations from tests
      annotations: file.tasks
        .map(t => t.meta?.annotation)
        .filter(Boolean)
    }));

    // Export to CI system
    exportToCI(results);
  }
}
```

```javascript
// vitest.config.js
export default defineConfig({
  test: {
    reporters: ['default', './reporters/junit-plus.js']
  }
});
```

## Migration from Vitest 2.x to 3.x

### Breaking Changes

1. **Workspace Configuration:**
   - Move workspace projects into main config
   - Update project references

2. **Reporter API:**
   - Update custom reporters to new lifecycle
   - Check reporter method signatures

3. **Browser Mode:**
   - Update provider syntax if using browser mode
   - Review browser configuration

### Migration Steps

```bash
# Update Vitest
npm install -D vitest@^3.0.0

# Update related packages
npm install -D @vitest/ui@^3.0.0
npm install -D @vitest/coverage-v8@^3.0.0

# Run tests to check for issues
npm test

# Update configs based on deprecation warnings
```

## Performance Optimization Tips

### 1. Use Workspace Projects for Isolation

```javascript
// Separate fast unit tests from slower integration tests
workspace: [
  {
    test: {
      name: 'unit',
      include: ['tests/unit/**'],
      environment: 'node' // Fastest
    }
  },
  {
    test: {
      name: 'integration',
      include: ['tests/integration/**'],
      environment: 'happy-dom',
      setupFiles: ['tests/setup.js']
    }
  }
]
```

### 2. Parallelize Test Execution

```bash
# Run projects in parallel
vitest run --project=unit --project=integration

# Exclude slow tests during development
vitest run --project=!e2e --project=!slow
```

### 3. Use Line Filtering for TDD

```bash
# Rapid iteration on single test
vitest run src/feature.test.js:42 --watch
```

### 4. Optimize Browser Testing

```javascript
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      // Reuse context for speed (less isolation)
      isolate: false,
      // Single instance for development
      instances: [{ browser: 'chromium' }]
    }
  }
});
```

## Common Patterns

### Test Annotation for Debugging

```javascript
test('payment processing', async ({ task }) => {
  const startTime = Date.now();

  try {
    const result = await processPayment(data);

    task.meta.annotation = {
      message: `Completed in ${Date.now() - startTime}ms`,
      attachments: [
        { name: 'result', content: JSON.stringify(result) }
      ]
    };

    expect(result.success).toBe(true);
  } catch (error) {
    task.meta.annotation = {
      message: 'Payment processing failed',
      attachments: [
        { name: 'error', content: error.message },
        { name: 'payload', content: JSON.stringify(data) }
      ]
    };
    throw error;
  }
});
```

### Multi-Project Testing Strategy

```javascript
export default defineConfig({
  test: {
    workspace: [
      // Fast feedback loop
      {
        test: {
          name: 'unit-critical',
          include: ['tests/unit/critical/**'],
          environment: 'node'
        }
      },
      // Standard tests
      {
        test: {
          name: 'unit-standard',
          include: ['tests/unit/**'],
          exclude: ['tests/unit/critical/**'],
          environment: 'happy-dom'
        }
      },
      // Slow integration tests
      {
        test: {
          name: 'integration',
          include: ['tests/integration/**'],
          testTimeout: 30000
        }
      }
    ]
  }
});
```

## Resources

- [Vitest 3.0 Release Notes](https://vitest.dev/blog/vitest-3)
- [Vitest 3.2 Release Notes](https://vitest.dev/blog/vitest-3-2)
- [Vitest Documentation](https://vitest.dev/)
- [Migration Guide](https://vitest.dev/guide/migration.html)
