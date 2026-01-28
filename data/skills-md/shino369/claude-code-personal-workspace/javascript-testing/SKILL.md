---
name: javascript-testing
description: JavaScript/Node.js testing best practices with Vitest. Use when writing tests, achieving test coverage, or working with JavaScript/TypeScript test files.
allowed-tools: Read, Write, Edit, Bash(pnpm:*, vitest:*)
user-invocable: true
---

# JavaScript Testing Best Practices

## Overview

Comprehensive guidance for writing high-quality JavaScript/Node.js tests using Vitest with 100% code coverage.

## Testing Framework: Vitest

**Why Vitest:**

- Native ESM support (no experimental flags)
- Seamless JSDOM integration
- Faster than Jest
- Jest-compatible API
- Built-in coverage with v8

**Test structure:**

```
your-script-dir/
├── script.js
└── __tests__/
    └── script.test.js
```

## Vitest Globals

Globals available automatically - no imports needed:

```javascript
describe('myFunction', () => {
  test('should work', () => {
    expect(true).toBe(true);
  });

  beforeEach(() => {
    /* Setup */
  });
  afterEach(() => {
    /* Cleanup */
  });
});
```

**Available globals:** `describe`, `test`, `it`, `expect`, `beforeEach`, `afterEach`, `beforeAll`, `afterAll`, `vi`

**Only import vi when mocking:**

```javascript
import { vi } from 'vitest';
vi.mock('module-name');
```

## Coverage Requirements

### 100% Required For

- All scripts in `.claude/hooks/`
- All scripts in `.claude/skills/`
- All utilities in `utils/`
- Business logic scripts
- Data processing scripts
- API interaction scripts

**Check coverage:**

```bash
pnpm test:coverage
# Must show 100% for: Statements, Branches, Functions, Lines
```

### Tests Optional For

- One-off automation scripts
- Shell command wrappers
- Throwaway/experimental scripts in `output/tasks/`

## Core Principles

### 1. Rarely Use Coverage Ignore

**General Rule:** Refactor code to be testable instead of ignoring coverage.

❌ **Don't ignore testable business logic:**

```javascript
/* c8 ignore next */
export function calculateTotal(items) {
  // This SHOULD be tested!
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

✅ **Exception - Browser Automation / Integration Code:**

Use `/* c8 ignore start */` and `/* c8 ignore stop */` for code that runs in browser context or requires complex integration setup:

```javascript
// Browser automation (Playwright, Puppeteer)
/* c8 ignore start -- Browser automation code, tested through integration tests */
export async function fetchContent(url) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url);

  // Browser context code
  const data = await page.evaluate(() => {
    return document.querySelector('h1').innerText;
  });

  await browser.close();
  return data;
}
/* c8 ignore stop */

// CLI entry points
/* c8 ignore start -- CLI entry point, tested through integration tests */
export async function main() {
  // Parse args, handle I/O, etc.
  const args = process.argv.slice(2);
  // ... CLI logic
}
/* c8 ignore stop */
```

**When to use c8 ignore:**

- Browser automation code (Playwright/Puppeteer page interactions)
- CLI entry points with process.exit() and argument parsing
- Code that runs in different contexts (browser vs Node.js)
- Complex integration points that require real dependencies

**Requirements when using c8 ignore:**

1. **Extract testable logic:** Move business logic into separate, testable functions
2. **Create integration tests:** Write integration test file (\*.integration.test.js) to cover the ignored code
3. **Add comment explaining why:** `/* c8 ignore start -- Reason why and how it's tested */`
4. **Minimize ignored code:** Keep ignored blocks as small as possible

✅ **Instead - Refactor for testability:**

```javascript
// Extract business logic (testable)
export function processInput(data) {
  return transform(data);
}

// Thin I/O wrapper
function main() {
  const data = readInput();
  const result = processInput(data); // Tested!
  writeOutput(result);
}
```

### 2. Separate I/O from Business Logic

❌ **Untestable:**

```javascript
function main() {
  process.stdin.on('data', (chunk) => {
    // All logic mixed with I/O
    const data = JSON.parse(chunk);
    const result = complexProcessing(data);
    writeToFile(result);
  });
}
```

✅ **Testable:**

```javascript
export function processHookInput(input) {
  const result = complexProcessing(input);
  return result;
}

function main() {
  process.stdin.on('data', (chunk) => {
    const data = JSON.parse(chunk);
    processHookInput(data); // Tested separately
  });
}
```

### 3. Export for Testing

```javascript
export function main() {
  if (process.argv.length !== 3) {
    console.error('Usage: ...');
    process.exit(1);
  }
  // ... logic
}

runIfMain(import.meta.url, main);
```

### 4. Test All Branches

```javascript
export function processFile(filePath) {
  if (!filePath) throw new Error('Required'); // Branch 1
  if (!fs.existsSync(filePath)) throw new Error('Not found'); // Branch 2
  return fs.readFileSync(filePath); // Branch 3
}

// Test ALL branches
describe('processFile', () => {
  test('missing path', () => expect(() => processFile()).toThrow('Required'));
  test('not found', () => expect(() => processFile('x')).toThrow('Not found'));
  test('exists', () => {
    fs.writeFileSync('t.txt', 'c');
    expect(processFile('t.txt').toString()).toBe('c');
    fs.unlinkSync('t.txt');
  });
});
```

### 5. Test Error Paths

Test both success and error paths for every function:

```javascript
export async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Fetch failed');
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Test both paths
test('success', async () => {
  global.fetch = vi.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ data: 'test' }),
    })
  );
  expect(await fetchData('url')).toEqual({ data: 'test' });
});

test('failure', async () => {
  global.fetch = vi.fn(() => Promise.resolve({ ok: false }));
  await expect(fetchData('url')).rejects.toThrow('Fetch failed');
});
```

## Test Organization

### Arrange-Act-Assert

```javascript
test('should calculate total', () => {
  const items = [
    { price: 10, qty: 2 },
    { price: 5, qty: 3 },
  ]; // Arrange
  const total = calculateTotal(items); // Act
  expect(total).toBe(35); // Assert
});
```

### Descriptive Names

✅ `test('should throw ValidationError when email invalid')`
❌ `test('works')` or `test('test1')`

### One Focus per Test

✅ Separate tests for status code, headers, body
❌ One test checking 10 different things

## Test Cleanup

```javascript
describe('file operations', () => {
  const testDir = 'test_files';

  beforeAll(() => fs.mkdirSync(testDir, { recursive: true }));
  afterAll(() => fs.rmSync(testDir, { recursive: true, force: true }));

  beforeEach(() => fs.writeFileSync(`${testDir}/temp.txt`, 'initial'));
  afterEach(() => {
    if (fs.existsSync(`${testDir}/temp.txt`)) {
      fs.unlinkSync(`${testDir}/temp.txt`);
    }
  });

  test('modifies file', () => {
    modifyFile(`${testDir}/temp.txt`);
    expect(fs.readFileSync(`${testDir}/temp.txt`, 'utf8')).toBe('modified');
  });
});
```

## Running Tests

```bash
pnpm test                  # Run all tests
pnpm test:watch            # Watch mode
pnpm test:coverage         # With coverage
pnpm test script.test.js   # Specific file
pnpm test --grep "pattern" # Match pattern
```

## Advanced Topics

See detailed guides:

**[mocking-guide.md](mocking-guide.md)** - Mocking patterns:

- Module/function/fs mocking
- process.exit(), process.argv, env vars
- Timers, Date, fetch/HTTP
- When to mock vs use real dependencies

**[coverage-strategies.md](coverage-strategies.md)** - 100% coverage:

- Refactoring I/O-heavy code
- Testing error paths
- Testing all branches
- Handling edge cases

## Quick Reference

### Common Pitfalls

❌ **Don't:**

1. Use coverage ignore comments
2. Skip error paths
3. Test implementation details
4. Over-mock (prefer real integrations)
5. Forget else branch
6. Assume code is untestable

✅ **Do:**

1. Separate I/O from logic
2. Test all branches/errors
3. Use real libs (JSDOM, etc.)
4. Clean up after tests
5. Descriptive names
6. One focus per test

### Integration Testing

Prefer real dependencies:

```javascript
import { JSDOM } from 'jsdom';

test('parses HTML', () => {
  const dom = new JSDOM('<h1>Title</h1>');
  const result = extractContent(dom.window.document);
  expect(result.title).toBe('Title');
});
```

**Mock:** External APIs, slow/destructive fs ops, timers, process.exit
**Use real:** Pure JS libs, internal modules, data transforms, algorithms

### Optimizing Integration Tests

When testing browser automation (Playwright/Puppeteer) or other slow integration points:

**1. Combine related tests:**

❌ Slow (9 tests, 17+ seconds):

```javascript
it('should fetch content', async () => {
  /* ... */
}, 2000);
it('should handle custom selectors', async () => {
  /* ... */
}, 2000);
it('should handle custom timeouts', async () => {
  /* ... */
}, 2000);
// Each launches a new browser
```

✅ Fast (3 tests, <2 seconds):

```javascript
it('should fetch content with custom options', async () => {
  // Test multiple features in one browser launch
  const result = await fetchContent(url, {
    selector: 'article',
    timeout: 5000,
  });
  expect(result).toContain('content');
  expect(result).toContain('expected text');
  expect(result).toMatch(/^# /); // markdown format
}, 10000);
```

**2. Make delays configurable:**

```javascript
// Auto-detect shorter delays for test environments
export async function fetchContent(url, options = {}) {
  const { waitDelay = null } = options;

  // file:// URLs need less wait time than remote sites
  const defaultDelay = url.startsWith('file://') ? 500 : 2000;
  const actualDelay = waitDelay !== null ? waitDelay : defaultDelay;

  await page.waitForTimeout(actualDelay);
}
```

**3. Combine error scenarios:**

```javascript
it('should handle various error conditions', async () => {
  await expect(fetchContent('invalid-url')).rejects.toThrow();
  await expect(fetchContent('file:///not/found')).rejects.toThrow();
  await expect(fetchContent(url, { timeout: 1 })).rejects.toThrow();
}, 20000);
```

**4. Use `c8 ignore` for browser automation:**

```javascript
/* c8 ignore start -- Browser automation, tested in integration tests */
export async function fetchContent(url) {
  const browser = await chromium.launch();
  // ... browser automation
  await browser.close();
}
/* c8 ignore stop */
```

**Result:** 8-10x faster test suites while maintaining full coverage and integration confidence.

## Best Practices

1. Use Vitest (not Jest)
2. Import only `vi` (globals automatic)
3. Achieve 100% coverage for production
4. Refactor for testability; use `c8 ignore` only for browser automation/CLI code
5. Separate I/O from business logic
6. Test all branches and errors
7. Use real dependencies when possible
8. Write descriptive test names
9. Clean up after tests
10. One assertion focus per test
11. Optimize integration tests by combining related assertions
