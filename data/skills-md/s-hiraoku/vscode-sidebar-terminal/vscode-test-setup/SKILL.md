---
name: vscode-test-setup
description: This skill provides comprehensive guidance for setting up and configuring test environments for VS Code extension projects. Use when initializing a new test infrastructure, configuring test runners (Vitest), setting up CI/CD test pipelines, integrating coverage tools (v8/c8), or troubleshooting test configuration issues.
---

# VS Code Extension Test Environment Setup

## Overview

This skill enables rapid and reliable test environment setup for VS Code extension projects. It covers test framework configuration, CI/CD integration, coverage tooling, and best practices for maintainable test infrastructure.

## When to Use This Skill

- Setting up test infrastructure for new VS Code extension projects
- Migrating from one test framework to another
- Configuring CI/CD pipelines for extension testing
- Setting up code coverage tools and thresholds
- Troubleshooting test configuration issues
- Optimizing test execution performance

## Quick Start Setup

### Step 1: Install Dependencies

```bash
# Core testing dependencies
npm install --save-dev \
  vitest \
  @vscode/test-cli \
  @vscode/test-electron

# Coverage is built into Vitest (uses v8 or c8 provider)
# No additional coverage packages needed
```

### Step 2: Create Test Configuration

Run the setup script to create all necessary configuration files:

```bash
# Execute from skill directory
python scripts/setup-test-env.py --project-path /path/to/extension
```

Or manually create the following files:

#### vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/test/unit/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
      exclude: ['src/test/**', '**/*.d.ts'],
      reporter: ['text', 'html', 'lcov'],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80
      }
    },
    testTimeout: 20000,
    retry: process.env.CI ? 2 : 0
  }
});
```

#### tsconfig.test.json

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "bundler",
    "outDir": "./out/test",
    "rootDir": "./src",
    "types": ["vitest/globals", "node"]
  },
  "include": [
    "src/test/**/*.ts"
  ]
}
```

### Step 3: Configure Package.json Scripts

```json
{
  "scripts": {
    "compile": "tsc -p ./",
    "compile:test": "tsc -p ./tsconfig.test.json",
    "watch": "tsc -watch -p ./",
    "pretest": "npm run compile && npm run compile:test",
    "test": "vscode-test",
    "test:unit": "vitest run",
    "test:integration": "vscode-test",
    "test:coverage": "vitest run --coverage",
    "test:watch": "vitest --watch",
    "tdd:red": "npm run test:unit -- --grep 'RED:'",
    "tdd:green": "npm run test:unit",
    "tdd:refactor": "npm run lint && npm run test:unit",
    "tdd:quality-gate": "npm run test:coverage && npm run lint"
  }
}
```

### Step 4: Create Directory Structure

```
src/
├── test/
│   ├── unit/                    # Pure unit tests (no VS Code API)
│   │   ├── setup.ts             # Unit test setup
│   │   ├── utils.test.ts
│   │   └── models.test.ts
│   ├── integration/             # Tests requiring VS Code API
│   │   ├── setup.ts             # Integration test setup
│   │   ├── extension.test.ts
│   │   └── commands.test.ts
│   ├── e2e/                     # End-to-end tests
│   │   └── activation.test.ts
│   ├── fixtures/                # Test data
│   │   ├── sample-workspace/
│   │   └── test-data.json
│   └── helpers/                 # Shared test utilities
│       ├── vscode-mock.ts
│       ├── async-helpers.ts
│       └── test-utils.ts
test-fixtures/                   # VS Code test workspace
└── .vscode/
    └── settings.json
```

## Test Framework Configuration

### Vitest Configuration

#### vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/test/unit/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
      exclude: ['src/test/**', '**/*.d.ts'],
      reporter: ['text', 'html', 'lcov'],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80
      }
    },
    testTimeout: 20000,
    retry: process.env.CI ? 2 : 0
  }
});
```

#### Unit Test Setup (src/test/unit/setup.ts)

```typescript
// Vitest provides expect, vi (mocking), and test utilities out of the box.
// No additional setup libraries (chai, sinon) are needed.

export { expect, vi, describe, it, beforeEach, afterEach } from 'vitest';
```

#### Integration Test Setup (src/test/integration/setup.ts)

> **Note**: Integration/E2E tests that require the VS Code API still use Mocha
> via `@vscode/test-electron`, because the VS Code test host expects a Mocha
> test runner. This section is intentionally kept as-is.

```typescript
import * as path from 'path';
import * as Mocha from 'mocha';
import { glob } from 'glob';

export async function run(): Promise<void> {
  const mocha = new Mocha({
    ui: 'bdd',
    color: true,
    timeout: 20000,
    retries: process.env.CI ? 2 : 0
  });

  const testsRoot = path.resolve(__dirname, '.');
  const files = await glob('**/*.test.js', { cwd: testsRoot });

  files.forEach((f) => mocha.addFile(path.resolve(testsRoot, f)));

  return new Promise((resolve, reject) => {
    mocha.run((failures) => {
      if (failures > 0) {
        reject(new Error(`${failures} tests failed.`));
      } else {
        resolve();
      }
    });
  });
}
```

### Jest Configuration (Alternative)

#### jest.config.js

```javascript
/** @type {import('jest').Config} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src/test/unit'],
  testMatch: ['**/*.test.ts'],
  moduleFileExtensions: ['ts', 'js', 'json'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/test/**',
    '!**/*.d.ts'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  setupFilesAfterEnv: ['<rootDir>/src/test/unit/setup.ts'],
  moduleNameMapper: {
    '^vscode$': '<rootDir>/src/test/helpers/vscode-mock.ts'
  }
};
```

## Coverage Configuration

### c8 Configuration

#### package.json

```json
{
  "c8": {
    "include": ["src/**/*.ts"],
    "exclude": [
      "src/test/**",
      "**/*.d.ts",
      "**/node_modules/**"
    ],
    "reporter": ["text", "html", "lcov"],
    "all": true,
    "clean": true,
    "check-coverage": true,
    "branches": 80,
    "functions": 80,
    "lines": 80,
    "statements": 80,
    "report-dir": "./coverage"
  }
}
```

### NYC Configuration (Alternative)

#### .nycrc.json

```json
{
  "extends": "@istanbuljs/nyc-config-typescript",
  "include": ["src/**/*.ts"],
  "exclude": ["src/test/**", "**/*.d.ts"],
  "reporter": ["text", "html", "lcov"],
  "all": true,
  "check-coverage": true,
  "branches": 80,
  "functions": 80,
  "lines": 80,
  "statements": 80
}
```

## CI/CD Configuration

### GitHub Actions

#### .github/workflows/test.yml

```yaml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        vscode-version: ['stable', 'insiders']
      fail-fast: false

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Compile
        run: npm run compile

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests (Linux)
        if: runner.os == 'Linux'
        run: xvfb-run -a npm run test:integration
        env:
          VSCODE_TEST_VERSION: ${{ matrix.vscode-version }}

      - name: Run integration tests (Windows/macOS)
        if: runner.os != 'Linux'
        run: npm run test:integration
        env:
          VSCODE_TEST_VERSION: ${{ matrix.vscode-version }}

      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.vscode-version == 'stable'
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage/lcov.info
          fail_ci_if_error: true

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
```

### TDD Quality Gate Workflow

#### .github/workflows/tdd-quality.yml

```yaml
name: TDD Quality Gate

on:
  push:
    branches: [main]
  pull_request:

jobs:
  tdd-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Compile
        run: npm run compile

      - name: Run TDD Quality Gate
        run: npm run tdd:quality-gate

      - name: Check coverage thresholds
        run: vitest run --coverage
        # Vitest checks thresholds automatically via vitest.config.ts

      - name: Generate coverage report
        run: vitest run --coverage --reporter=verbose

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
```

## VS Code Launch Configuration

### .vscode/launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}"
      ],
      "outFiles": ["${workspaceFolder}/out/**/*.js"],
      "preLaunchTask": "npm: compile"
    },
    {
      "name": "Run Integration Tests",
      "type": "extensionHost",
      "request": "launch",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}",
        "--extensionTestsPath=${workspaceFolder}/out/test/integration"
      ],
      "outFiles": ["${workspaceFolder}/out/**/*.js"],
      "preLaunchTask": "npm: compile"
    },
    {
      "name": "Run Unit Tests",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/vitest/vitest.mjs",
      "args": ["run"],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    },
    {
      "name": "Debug Current Test File",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/vitest/vitest.mjs",
      "args": [
        "run",
        "${relativeFile}"
      ],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    }
  ]
}
```

### .vscode/tasks.json

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "npm",
      "script": "compile",
      "problemMatcher": "$tsc",
      "group": "build",
      "label": "npm: compile"
    },
    {
      "type": "npm",
      "script": "watch",
      "problemMatcher": "$tsc-watch",
      "isBackground": true,
      "group": "build",
      "label": "npm: watch"
    },
    {
      "type": "npm",
      "script": "test:unit",
      "problemMatcher": [],
      "group": "test",
      "label": "npm: test:unit"
    },
    {
      "type": "npm",
      "script": "test:coverage",
      "problemMatcher": [],
      "group": "test",
      "label": "npm: test:coverage"
    }
  ]
}
```

## Test Fixtures Setup

### test-fixtures/.vscode/settings.json

```json
{
  "editor.formatOnSave": false,
  "editor.tabSize": 2,
  "files.autoSave": "off",
  "terminal.integrated.defaultProfile.linux": "bash",
  "terminal.integrated.defaultProfile.osx": "zsh",
  "terminal.integrated.defaultProfile.windows": "PowerShell"
}
```

### Test Data Factory

```typescript
// src/test/helpers/test-data-factory.ts
import * as vscode from 'vscode';

export class TestDataFactory {
  static createTerminalOptions(
    overrides: Partial<vscode.TerminalOptions> = {}
  ): vscode.TerminalOptions {
    return {
      name: 'Test Terminal',
      cwd: '/tmp',
      env: { TEST_ENV: 'true' },
      ...overrides
    };
  }

  static createWebviewContent(title: string): string {
    return `<!DOCTYPE html>
    <html>
    <head><title>${title}</title></head>
    <body><h1>Test Content</h1></body>
    </html>`;
  }

  static createMockTerminalState(): any {
    return {
      id: 1,
      name: 'Terminal 1',
      processState: 'running',
      scrollback: 'mock scrollback content',
      cwd: '/home/user'
    };
  }

  static createMockSessionData(): any {
    return {
      version: 1,
      terminals: [this.createMockTerminalState()],
      savedAt: Date.now()
    };
  }
}
```

## Troubleshooting Common Issues

### Issue: Tests timeout in CI

**Symptoms**: Tests pass locally but timeout in GitHub Actions

**Solutions**:
1. Use `xvfb-run` for Linux headless testing
2. Increase timeout in vitest config (`testTimeout` in `vitest.config.ts`)
3. Add retries for flaky tests (`retry` in vitest config)

```yaml
# GitHub Actions
- name: Run tests (Linux)
  if: runner.os == 'Linux'
  run: xvfb-run -a npm run test:integration
```

### Issue: ES Module import errors

**Symptoms**: `ERR_REQUIRE_ESM` or similar ESM/CJS interop errors

**Solutions**:
Vitest handles ESM natively, so most ESM issues do not apply. If you encounter
module resolution problems:
1. Ensure `vitest.config.ts` uses `environment: 'node'`
2. Check that `tsconfig.test.json` has `"module": "ESNext"` and `"moduleResolution": "bundler"`
3. For stubbing ESM modules, use `vi.mock()` which supports ESM out of the box

### Issue: VS Code API not available in unit tests

**Symptoms**: `Cannot find module 'vscode'`

**Solutions**:
1. Separate unit tests from integration tests
2. Use VS Code API mocks for unit tests

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    alias: {
      vscode: path.resolve(__dirname, 'src/test/helpers/vscode-mock.ts')
    }
  }
});
```

### Issue: Coverage not tracking TypeScript files

**Symptoms**: Coverage shows 0% or missing files

**Solutions**:
1. Configure source maps correctly
2. Use proper include/exclude patterns

```json
{
  "compilerOptions": {
    "sourceMap": true,
    "inlineSources": true
  }
}
```

### Issue: Flaky tests due to async timing

**Symptoms**: Tests fail intermittently

**Solutions**:
1. Use proper async/await
2. Add explicit waits for async operations
3. Avoid time-dependent assertions

```typescript
// Bad
setTimeout(() => expect(value).toBe(1), 100);

// Good
await waitForCondition(() => value === 1);
expect(value).toBe(1);
```

## Resources

For detailed reference documentation, see:
- `references/framework-comparison.md` - Framework comparison (Vitest, Mocha, Jest)
- `references/ci-templates.md` - CI/CD pipeline templates
- `scripts/setup-test-env.py` - Automated environment setup
