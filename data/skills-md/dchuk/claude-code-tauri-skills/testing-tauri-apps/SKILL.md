---
name: testing-tauri-apps
description: Guides developers through testing Tauri applications including unit testing with mock runtime, mocking Tauri APIs, WebDriver end-to-end testing with Selenium and WebdriverIO, and CI integration with GitHub Actions.
---

# Testing Tauri Applications

This skill covers testing strategies for Tauri v2 applications: unit testing with mocks, end-to-end testing with WebDriver, and CI integration.

## Testing Approaches Overview

Tauri supports two primary testing methodologies:

1. **Unit/Integration Testing** - Uses a mock runtime without executing native webview libraries
2. **End-to-End Testing** - Uses WebDriver protocol for browser automation

## Mocking Tauri APIs

The `@tauri-apps/api/mocks` module simulates a Tauri environment during frontend testing.

### Install Mock Dependencies

```bash
npm install -D vitest @tauri-apps/api
```

### Mock IPC Commands

```javascript
import { mockIPC, clearMocks } from '@tauri-apps/api/mocks';
import { invoke } from '@tauri-apps/api/core';
import { vi, describe, it, expect, afterEach } from 'vitest';

afterEach(() => {
  clearMocks();
});

describe('Tauri Commands', () => {
  it('should mock the add command', async () => {
    mockIPC((cmd, args) => {
      if (cmd === 'add') {
        return (args.a as number) + (args.b as number);
      }
    });

    const result = await invoke('add', { a: 12, b: 15 });
    expect(result).toBe(27);
  });

  it('should verify invoke was called', async () => {
    mockIPC((cmd) => {
      if (cmd === 'greet') return 'Hello!';
    });

    const spy = vi.spyOn(window.__TAURI_INTERNALS__, 'invoke');
    await invoke('greet', { name: 'World' });
    expect(spy).toHaveBeenCalled();
  });
});
```

### Mock Sidecar and Shell Commands

```javascript
import { mockIPC } from '@tauri-apps/api/mocks';

mockIPC(async (cmd, args) => {
  if (args.message.cmd === 'execute') {
    const eventCallbackId = `_${args.message.onEventFn}`;
    const eventEmitter = window[eventCallbackId];
    eventEmitter({ event: 'Stdout', payload: 'process output data' });
    eventEmitter({ event: 'Terminated', payload: { code: 0 } });
  }
});
```

### Mock Events (v2.7.0+)

```javascript
import { mockIPC } from '@tauri-apps/api/mocks';
import { emit, listen } from '@tauri-apps/api/event';

mockIPC(() => {}, { shouldMockEvents: true });

const eventHandler = vi.fn();
await listen('test-event', eventHandler);
await emit('test-event', { foo: 'bar' });
expect(eventHandler).toHaveBeenCalled();
```

### Mock Windows

```javascript
import { mockWindows } from '@tauri-apps/api/mocks';
import { getCurrent, getAll } from '@tauri-apps/api/webviewWindow';

mockWindows('main', 'second', 'third');

// First parameter is the "current" window
expect(getCurrent()).toHaveProperty('label', 'main');
expect(getAll().map((w) => w.label)).toEqual(['main', 'second', 'third']);
```

### Vitest Configuration

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./test/setup.js'],
  },
});

// test/setup.js
window.__TAURI_INTERNALS__ = {
  invoke: vi.fn(),
  transformCallback: vi.fn(),
};
```

## WebDriver End-to-End Testing

WebDriver testing uses `tauri-driver` to automate Tauri applications.

### Platform Support

| Platform | Support | Notes |
|----------|---------|-------|
| Windows | Full | Requires Microsoft Edge Driver |
| Linux | Full | Requires WebKitWebDriver |
| macOS | None | WKWebView lacks WebDriver tooling |

### Install tauri-driver

```bash
cargo install tauri-driver --locked
```

### Platform Dependencies

```bash
# Linux (Debian/Ubuntu)
sudo apt install webkit2gtk-driver xvfb
which WebKitWebDriver  # Verify installation

# Windows (PowerShell)
cargo install --git https://github.com/chippers/msedgedriver-tool
& "$HOME/.cargo/bin/msedgedriver-tool.exe"
```

## WebdriverIO Setup

### Project Structure

```
my-tauri-app/
├── src-tauri/
├── src/
└── e2e-tests/
    ├── package.json
    ├── wdio.conf.js
    └── specs/
        └── app.spec.js
```

### Package Configuration

```json
{
  "name": "tauri-e2e-tests",
  "version": "1.0.0",
  "type": "module",
  "scripts": { "test": "wdio run wdio.conf.js" },
  "dependencies": { "@wdio/cli": "^9.19.0" },
  "devDependencies": {
    "@wdio/local-runner": "^9.19.0",
    "@wdio/mocha-framework": "^9.19.0",
    "@wdio/spec-reporter": "^9.19.0"
  }
}
```

### WebdriverIO Configuration

```javascript
// e2e-tests/wdio.conf.js
import { spawn, spawnSync } from 'child_process';

let tauriDriver;

export const config = {
  hostname: '127.0.0.1',
  port: 4444,
  specs: ['./specs/**/*.js'],
  maxInstances: 1,
  capabilities: [{
    browserName: 'wry',
    'tauri:options': {
      application: '../src-tauri/target/debug/my-tauri-app',
    },
  }],
  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: { ui: 'bdd', timeout: 60000 },

  onPrepare: () => {
    const result = spawnSync('cargo', ['build', '--manifest-path', '../src-tauri/Cargo.toml'], {
      stdio: 'inherit',
    });
    if (result.status !== 0) throw new Error('Failed to build Tauri app');
  },

  beforeSession: () => {
    tauriDriver = spawn('tauri-driver', [], { stdio: ['ignore', 'pipe', 'pipe'] });
    return new Promise((resolve) => {
      tauriDriver.stdout.on('data', (data) => {
        if (data.toString().includes('listening')) resolve();
      });
    });
  },

  afterSession: () => tauriDriver?.kill(),
};
```

### WebdriverIO Test Example

```javascript
// e2e-tests/specs/app.spec.js
describe('My Tauri App', () => {
  it('should display the header', async () => {
    const header = await $('body > h1');
    expect(await header.getText()).toMatch(/^[hH]ello/);
  });

  it('should interact with a button', async () => {
    const button = await $('#greet-button');
    await button.click();
    const output = await $('#greet-output');
    await output.waitForExist({ timeout: 5000 });
    expect(await output.getText()).toContain('Hello');
  });
});
```

## Selenium Setup

### Package Configuration

```json
{
  "name": "tauri-selenium-tests",
  "version": "1.0.0",
  "scripts": { "test": "mocha" },
  "dependencies": {
    "chai": "^5.2.1",
    "mocha": "^11.7.1",
    "selenium-webdriver": "^4.34.0"
  }
}
```

### Selenium Test Example

```javascript
// e2e-tests/test/test.js
import { spawn, spawnSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import { Builder, By } from 'selenium-webdriver';
import { expect } from 'chai';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
let driver, tauriDriver;
const application = path.resolve(__dirname, '../../src-tauri/target/debug/my-tauri-app');

describe('Tauri App Tests', function () {
  this.timeout(60000);

  before(async function () {
    spawnSync('cargo', ['build', '--manifest-path', '../../src-tauri/Cargo.toml'], {
      cwd: __dirname, stdio: 'inherit',
    });

    tauriDriver = spawn('tauri-driver', [], { stdio: ['ignore', 'pipe', 'pipe'] });
    await new Promise((resolve) => {
      tauriDriver.stdout.on('data', (data) => {
        if (data.toString().includes('listening')) resolve();
      });
    });

    driver = await new Builder()
      .usingServer('http://127.0.0.1:4444/')
      .withCapabilities({ browserName: 'wry', 'tauri:options': { application } })
      .build();
  });

  after(async function () {
    await driver?.quit();
    tauriDriver?.kill();
  });

  it('should display greeting', async function () {
    const header = await driver.findElement(By.css('body > h1'));
    expect(await header.getText()).to.match(/^[hH]ello/);
  });

  it('should click button and show output', async function () {
    const button = await driver.findElement(By.id('greet-button'));
    await button.click();
    const output = await driver.findElement(By.id('greet-output'));
    expect(await output.getText()).to.include('Hello');
  });
});
```

## CI Integration with GitHub Actions

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Install Linux dependencies
        if: matrix.os == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y libwebkit2gtk-4.1-dev build-essential \
            curl wget file libxdo-dev libssl-dev \
            libayatana-appindicator3-dev librsvg2-dev \
            webkit2gtk-driver xvfb

      - uses: dtolnay/rust-action@stable
      - run: cargo install tauri-driver --locked

      - name: Setup Windows WebDriver
        if: matrix.os == 'windows-latest'
        shell: pwsh
        run: |
          cargo install --git https://github.com/chippers/msedgedriver-tool
          & "$HOME/.cargo/bin/msedgedriver-tool.exe"

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm install
      - run: npm run build
      - run: cargo build --manifest-path src-tauri/Cargo.toml

      - name: Run E2E tests (Linux)
        if: matrix.os == 'ubuntu-latest'
        working-directory: e2e-tests
        run: npm install && xvfb-run npm test

      - name: Run E2E tests (Windows)
        if: matrix.os == 'windows-latest'
        working-directory: e2e-tests
        run: npm install && npm test
```

## Best Practices

### Mock Testing
- Always call `clearMocks()` in `afterEach` to prevent state leakage
- Use spies to verify IPC calls were made correctly
- Mock at the right level: IPC for commands, windows for multi-window logic

### WebDriver Testing
- Use debug builds for faster iteration during development
- Set appropriate timeouts as Tauri apps may need time to initialize
- Wait for elements explicitly rather than using implicit waits
- Keep tests independent so each test works in isolation

### CI Integration
- Use `xvfb-run` on Linux for headless WebDriver testing
- Match Edge Driver version on Windows to avoid connection issues
- Build the app before running WebDriver tests
- Run unit tests before e2e tests to catch issues early

## Troubleshooting

### WebDriver Connection Timeout
- Windows: Verify Edge Driver version matches installed Edge
- Linux: Ensure `webkit2gtk-driver` is installed
- Check `tauri-driver` is running and listening on port 4444

### Mock Not Working
- Import `@tauri-apps/api/mocks` before the code under test
- Call `clearMocks()` in `afterEach` to reset state
- Ensure `window.__TAURI_INTERNALS__` is properly mocked in setup

### CI Failures
- Linux: Add `xvfb-run` prefix to test commands
- Windows: Install Edge Driver via `msedgedriver-tool`
- Increase timeout for slower CI runners

## References

- [Tauri Testing Documentation](https://v2.tauri.app/develop/tests/)
- [tauri-driver on crates.io](https://crates.io/crates/tauri-driver)
- [WebDriver Example Repository](https://github.com/tauri-apps/webdriver-example)
