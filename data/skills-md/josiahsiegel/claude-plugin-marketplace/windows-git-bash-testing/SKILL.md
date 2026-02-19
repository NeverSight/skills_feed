---
name: windows-git-bash-testing
description: Windows and Git Bash testing compatibility guide for Vitest, Playwright, and MSW with path conversion patterns
---

# Windows and Git Bash Testing Compatibility Guide

## Overview

This guide provides essential knowledge for running Vitest, Playwright, and MSW tests on Windows, particularly in Git Bash/MINGW environments. It addresses common path conversion issues, shell detection, and cross-platform test execution patterns.

## Shell Detection in Test Environments

### Detecting Git Bash/MINGW

When running tests in Git Bash or MINGW environments, use these detection methods:

**Method 1: Environment Variable (Most Reliable)**
```javascript
// Detect Git Bash/MINGW in Node.js test setup
function isGitBash() {
  return !!(process.env.MSYSTEM); // MINGW64, MINGW32, MSYS
}

function isWindows() {
  return process.platform === 'win32';
}

function needsPathConversion() {
  return isWindows() && isGitBash();
}
```

**Method 2: Using uname in Setup Scripts**
```bash
# In bash test setup scripts
case "$(uname -s)" in
  MINGW64*|MINGW32*|MSYS_NT*)
    # Git Bash/MINGW environment
    export TEST_ENV="mingw"
    ;;
  CYGWIN*)
    # Cygwin environment
    export TEST_ENV="cygwin"
    ;;
  Linux*)
    export TEST_ENV="linux"
    ;;
  Darwin*)
    export TEST_ENV="macos"
    ;;
esac
```

**Method 3: Combined Detection for Test Configuration**
```javascript
// vitest.config.js or test setup
import { execSync } from 'child_process';

function detectShell() {
  // Check MSYSTEM first (most reliable for Git Bash)
  if (process.env.MSYSTEM) {
    return { type: 'mingw', subsystem: process.env.MSYSTEM };
  }

  // Try uname if available
  try {
    const uname = execSync('uname -s', { encoding: 'utf8' }).trim();
    if (uname.startsWith('MINGW')) return { type: 'mingw' };
    if (uname.startsWith('CYGWIN')) return { type: 'cygwin' };
    if (uname === 'Darwin') return { type: 'macos' };
    if (uname === 'Linux') return { type: 'linux' };
  } catch {
    // uname not available (likely Windows cmd/PowerShell)
  }

  return { type: 'unknown', platform: process.platform };
}

const shell = detectShell();
console.log('Running tests in:', shell.type);
```

## Path Conversion Issues and Solutions

### Common Path Conversion Problems

Git Bash automatically converts Unix-style paths to Windows paths, which can cause issues with test file paths, module imports, and test configuration.

**Problem Examples:**
```bash
# Git Bash converts these automatically:
/foo → C:/Program Files/Git/usr/foo
/foo:/bar → C:\msys64\foo;C:\msys64\bar
--dir=/foo → --dir=C:/msys64/foo
```

### Solution 1: Disable Path Conversion

For test commands where path conversion causes issues:

```bash
# Disable all path conversion for a single command
MSYS_NO_PATHCONV=1 vitest run

# Disable for specific patterns
export MSYS2_ARG_CONV_EXCL="--coverage.reporter"
vitest run --coverage.reporter=html

# Disable for entire test session
export MSYS_NO_PATHCONV=1
npm test
```

### Solution 2: Use Native Windows Paths in Configuration

When specifying test file paths in configuration, use Windows-style paths:

```javascript
// vitest.config.js - Windows-compatible
export default defineConfig({
  test: {
    include: [
      'tests/unit/**/*.test.js',     // Relative paths work best
      'tests/integration/**/*.test.js'
    ],
    // Avoid absolute paths starting with /c/ or C:
    setupFiles: ['./tests/setup.js'], // Use relative paths
    coverage: {
      reportsDirectory: './coverage'  // Relative, not absolute
    }
  }
});
```

### Solution 3: Path Conversion Helper for Test Utilities

Create a helper for converting paths in test utilities:

```javascript
// tests/helpers/paths.js
import { execSync } from 'child_process';

/**
 * Convert Windows path to Unix path for Git Bash compatibility
 */
export function toUnixPath(windowsPath) {
  if (!needsPathConversion()) return windowsPath;

  try {
    // Use cygpath if available
    return execSync(`cygpath -u "${windowsPath}"`, {
      encoding: 'utf8'
    }).trim();
  } catch {
    // Fallback: manual conversion
    // C:\Users\foo → /c/Users/foo
    return windowsPath
      .replace(/\\/g, '/')
      .replace(/^([A-Z]):/, (_, drive) => `/${drive.toLowerCase()}`);
  }
}

/**
 * Convert Unix path to Windows path
 */
export function toWindowsPath(unixPath) {
  if (!needsPathConversion()) return unixPath;

  try {
    return execSync(`cygpath -w "${unixPath}"`, {
      encoding: 'utf8'
    }).trim();
  } catch {
    // Fallback: manual conversion
    // /c/Users/foo → C:\Users\foo
    return unixPath
      .replace(/^\/([a-z])\//, (_, drive) => `${drive.toUpperCase()}:\\`)
      .replace(/\//g, '\\');
  }
}

function needsPathConversion() {
  return !!(process.env.MSYSTEM ||
           (process.platform === 'win32' && process.env.TERM === 'cygwin'));
}
```

**Usage in Tests:**
```javascript
import { toUnixPath, toWindowsPath } from '../helpers/paths.js';

test('loads config file', () => {
  const configPath = toWindowsPath('/c/project/config.json');
  const config = loadConfig(configPath);
  expect(config).toBeDefined();
});
```

## Test Execution Best Practices for Windows/Git Bash

### 1. NPM Scripts for Cross-Platform Compatibility

Define test scripts in package.json that work across all environments:

```json
{
  "scripts": {
    "test": "vitest run",
    "test:unit": "vitest run tests/unit",
    "test:integration": "vitest run tests/integration",
    "test:watch": "vitest watch",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "test:e2e:headed": "playwright test --headed",
    "test:debug": "vitest run --reporter=verbose"
  }
}
```

**Always use npm scripts rather than direct vitest/playwright commands** - this ensures consistent behavior across shells.

### 2. Relative Path Imports

Use relative paths in test files to avoid path conversion issues:

```javascript
// ✅ Good - Relative paths work everywhere
import { myFunction } from '../../src/utils.js';
import { server } from '../mocks/server.js';

// ❌ Bad - Absolute paths can cause issues in Git Bash
import { myFunction } from '/c/project/src/utils.js';
```

### 3. Test File Discovery

Vitest and Playwright handle file patterns differently in Git Bash:

```javascript
// vitest.config.js - Use glob patterns, not absolute paths
export default defineConfig({
  test: {
    // ✅ Good - Glob patterns work cross-platform
    include: ['tests/**/*.test.js', 'src/**/*.test.js'],

    // ❌ Bad - Absolute paths problematic in Git Bash
    include: ['/c/project/tests/**/*.test.js']
  }
});
```

```javascript
// playwright.config.js - Relative directory paths
export default defineConfig({
  // ✅ Good
  testDir: './tests/e2e',

  // ❌ Bad
  testDir: '/c/project/tests/e2e'
});
```

### 4. Temporary File Handling

Git Bash uses Unix-style temp directories, which can cause issues:

```javascript
// tests/setup.js - Cross-platform temp file handling
import os from 'os';
import path from 'path';

function getTempDir() {
  const tmpdir = os.tmpdir();

  // In Git Bash, os.tmpdir() may return Windows path
  // Ensure it's usable by your test framework
  if (process.env.MSYSTEM && !tmpdir.startsWith('/')) {
    // Convert Windows temp path if needed
    return tmpdir.replace(/\\/g, '/');
  }

  return tmpdir;
}

// Use in tests
const testTempDir = path.join(getTempDir(), 'my-tests');
```

## Playwright-Specific Windows/Git Bash Considerations

### 1. Browser Installation in Git Bash

```bash
# Use npx to ensure correct path handling
npx playwright install

# If issues occur, use Windows-native command prompt instead
# Then run tests from Git Bash
```

### 2. Headed Mode in MINGW

When running headed tests in Git Bash, ensure DISPLAY variables are not set:

```bash
# Unset DISPLAY if set (can interfere with Windows GUI)
unset DISPLAY

# Run headed tests
npx playwright test --headed
```

### 3. Screenshot and Video Paths

Use relative paths for artifacts:

```javascript
// playwright.config.js
export default defineConfig({
  use: {
    // ✅ Good - Relative paths
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  // Output directory with relative path
  outputDir: './test-results',
});
```

## MSW (Mock Service Worker) in Git Bash

MSW generally works without issues in Git Bash, but be aware of:

### 1. Handler File Imports

Use relative imports in MSW setup:

```javascript
// tests/mocks/server.js
// ✅ Good
import { handlers } from './handlers.js';

// ❌ Bad - Avoid absolute paths
import { handlers } from '/c/project/tests/mocks/handlers.js';
```

### 2. Fetch Polyfill (Node.js)

Ensure Node.js version 18+ for native Fetch API support:

```bash
# Check Node version
node --version  # Should be 18+

# If using older Node, MSW 2.x won't work properly
```

## Common Windows/Git Bash Test Errors and Fixes

### Error 1: "No such file or directory" in Git Bash

**Symptom:**
```
Error: /usr/bin/bash: line 1: C:UsersUsername...No such file
```

**Cause:** Path conversion issue, often with temp directories.

**Fix:**
```bash
# Option 1: Disable path conversion
MSYS_NO_PATHCONV=1 npm test

# Option 2: Use Claude Code's Git Bash path variable
export CLAUDE_CODE_GIT_BASH_PATH="C:\\Program Files\\git\\bin\\bash.exe"

# Option 3: Run via npm scripts (recommended)
npm test  # npm handles path issues automatically
```

### Error 2: Module Import Failures

**Symptom:**
```
Error: Cannot find module '../src/utils'
```

**Cause:** Path separator confusion (backslash vs forward slash).

**Fix:**
```javascript
// Use path.join() or path.resolve() for cross-platform paths
import path from 'path';

const utilsPath = path.resolve(__dirname, '../src/utils.js');
const utils = await import(utilsPath);
```

### Error 3: Playwright Browser Launch Failure

**Symptom:**
```
Error: Failed to launch browser
```

**Cause:** Git Bash environment variables interfering with browser launch.

**Fix:**
```bash
# Clear problematic environment variables
unset DISPLAY
unset BROWSER

# Run Playwright tests
npx playwright test
```

### Error 4: Coverage Report Path Issues

**Symptom:**
```
Error: Failed to write coverage to /c/project/coverage
```

**Fix:**
```javascript
// vitest.config.js - Use relative paths
export default defineConfig({
  test: {
    coverage: {
      // ✅ Good
      reportsDirectory: './coverage',

      // ❌ Bad
      reportsDirectory: '/c/project/coverage'
    }
  }
});
```

## Testing Strategy for Multi-Platform Support

### 1. CI/CD Configuration

Test on multiple platforms in CI/CD:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}

      - run: npm ci
      - run: npm test
      - run: npm run test:e2e
        if: matrix.os == 'ubuntu-latest'  # Run E2E on Linux only
```

### 2. Shell-Specific Test Setup

Create shell-specific setup if needed:

```javascript
// tests/setup.js
import { detectShell } from './helpers/shell-detect.js';

const shell = detectShell();

// Apply shell-specific configuration
if (shell.type === 'mingw') {
  console.log('Running in Git Bash/MINGW environment');
  // Apply MINGW-specific test setup
  process.env.FORCE_COLOR = '1'; // Enable colors in Git Bash
}

// Standard setup continues...
```

### 3. Path-Safe Test Utilities

Create test utilities that work across all platforms:

```javascript
// tests/helpers/test-utils.js
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Get __dirname equivalent in ESM
export function getCurrentDir(importMetaUrl) {
  return dirname(fileURLToPath(importMetaUrl));
}

// Cross-platform path joining
export function testPath(...segments) {
  return path.join(...segments).replace(/\\/g, '/');
}

// Usage in test file:
// const __dirname = getCurrentDir(import.meta.url);
// const fixturePath = testPath(__dirname, 'fixtures', 'data.json');
```

## Quick Reference

### Shell Detection Commands

```bash
# Check if running in Git Bash
echo $MSYSTEM           # MINGW64, MINGW32, or empty

# Check OS type
uname -s               # MINGW64_NT-* for Git Bash

# Check platform in Node
node -p process.platform  # win32 on Windows
```

### Path Conversion Quick Fixes

```bash
# Disable for single command
MSYS_NO_PATHCONV=1 vitest run

# Disable for session
export MSYS_NO_PATHCONV=1

# Convert path manually
cygpath -u "C:\path"    # Windows → Unix
cygpath -w "/c/path"    # Unix → Windows
```

### Recommended Test Execution (Git Bash on Windows)

```bash
# ✅ Best - Use npm scripts
npm test
npm run test:e2e

# ✅ Good - With path conversion disabled
MSYS_NO_PATHCONV=1 vitest run

# ⚠️ Caution - Direct vitest command may have issues
vitest run  # May encounter path conversion issues
```

## Resources

- [Git Bash Path Conversion](https://www.msys2.org/docs/filesystem-paths/)
- [Vitest Configuration](https://vitest.dev/config/)
- [Playwright on Windows](https://playwright.dev/docs/browsers#install-system-requirements)
- [MSW Node.js Integration](https://mswjs.io/docs/integrations/node)

## Summary

When running tests on Windows with Git Bash:

1. **Use npm scripts** for all test execution (most reliable)
2. **Use relative paths** in configuration and imports
3. **Detect shell environment** when needed for conditional setup
4. **Disable path conversion** (MSYS_NO_PATHCONV=1) if issues occur
5. **Test on multiple platforms** in CI/CD to catch platform-specific issues
6. **Avoid absolute paths** starting with /c/ or C:\ in test files
7. **Use path.join()** for programmatic path construction

Following these practices ensures tests run reliably across Windows Command Prompt, PowerShell, Git Bash, and Unix-like environments.
