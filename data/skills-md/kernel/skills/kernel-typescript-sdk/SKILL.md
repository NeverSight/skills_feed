---
name: kernel-typescript-sdk
description: Build browser automation scripts using the Kernel TypeScript SDK with Playwright, CDP, and remote browser management.
context: fork
---

## When to Use This Skill

Use the Kernel TypeScript SDK when you need to:

- **Build browser automation scripts** - Create TypeScript programs that control remote browsers
- **Execute server-side automation** - Run Playwright code directly in the browser VM without local dependencies
- **Manage browser sessions programmatically** - Create, configure, and control browsers from code
- **Build scalable scraping/testing tools** - Use browser pools and profiles for high-volume automation
- **Deploy automation as actions** - Package scripts as Kernel actions for invocation via API

**When NOT to use:**
- For CLI commands (e.g., `kernel browsers create`), use the `kernel-cli` skill instead
- For quick one-off tasks, the CLI may be simpler than writing code

## Core Concepts

### SDK Architecture

The SDK is organized into resource-based modules:

- `kernel.browsers` - Browser session management (create, list, delete)
- `kernel.browsers.playwright` - Server-side Playwright execution
- `kernel.browsers.computer` - OS-level controls (mouse, keyboard, screenshots)
- `kernel.browserPools` - Pre-warmed browser pool management
- `kernel.profiles` - Persistent browser profiles (auth state)
- `kernel.auth.connections` - Managed auth (create, login, submit, follow, retrieve, delete)
- `kernel.credentialProviders` - External credential providers (1Password)
- `kernel.proxies` - Proxy configuration
- `kernel.extensions` - Chrome extension management
- `kernel.deployments` - App deployment
- `kernel.invocations` - Action invocation

### Two Automation Approaches

**1. Server-side Execution (RECOMMENDED)**
- Execute Playwright code directly in browser VM using `kernel.browsers.playwright.execute()`
- Response accessed via `response.result` - **MUST use `return` in code to get data back**
- Best for: Most use cases, production automation, parallel execution, actions

**2. CDP Connection (Client-side)**
- Connect Playwright/Puppeteer to browser via CDP WebSocket URL (`browser.cdp_ws_url`)
- Code runs locally, browser runs remotely; requires local Playwright installation
- Best for: Complex debugging, specific local development needs

## Patterns Reference

**SDK Initialization**
```typescript
import { Kernel } from "@onkernel/sdk";
const kernel = new Kernel();  // Reads KERNEL_API_KEY from environment
```

**Attribute Access**: Use `snake_case` (e.g., `browser.session_id`, `browser.cdp_ws_url`)

**Binary Data Handling**

Binary data does not serialize through `playwright.execute` (returns `undefined`). Use dedicated APIs:

```typescript
// For screenshots:
const response = await kernel.browsers.computer.captureScreenshot(browser.session_id);
// For files:
const response = await kernel.browsers.filesystem.readFile(browser.session_id, { path: '/path/to/file' });

// Convert to buffer:
const blob = await response.blob();
const buffer = Buffer.from(await blob.arrayBuffer());
```

> **Note:** This differs from the Python SDK where binary data CAN be returned via `playwright.execute` as a Buffer object. In TypeScript, always use dedicated APIs.

## References

- **Kernel Documentation**: https://www.kernel.sh/docs
- **Quickstart Guide**: https://www.kernel.sh/docs/quickstart
- **Templates**: https://www.kernel.sh/docs/reference/cli/create#available-templates
- **TypeScript Types**: Available in `@onkernel/sdk` package
- **Examples**: [examples](./examples/examples.md)
