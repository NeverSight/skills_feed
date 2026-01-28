---
name: extension-toolchain
description: "Apply modern browser extension toolchain patterns: WXT (default), Plasmo, CRXJS for Chrome/Firefox/Safari extensions. Use when building browser extensions, choosing extension frameworks, or discussing manifest v3 patterns."
---

# Extension Toolchain

Modern browser extension development with Manifest V3, focusing on framework-agnostic solutions.

## Recommended Stack: WXT (Default)

**Why WXT (2025):**
- Framework-agnostic (React, Vue, Svelte, SolidJS, Vanilla)
- Vite-powered (fast HMR, optimized builds)
- Auto-reload on code changes (content scripts too!)
- TypeScript-first with excellent type generation
- Automated publishing to stores
- Manifest V3 by default

```bash
# Create new extension
npm create wxt@latest

# Choose your framework
? Select a template:
  > vanilla
    react
    vue
    svelte
    solid

# Start development
cd my-extension
npm run dev         # Chrome (default)
npm run dev:firefox # Firefox
npm run dev:edge    # Edge
npm run dev:safari  # Safari (experimental)
```

### When to Use WXT
✅ Multi-framework teams (framework-agnostic)
✅ Need cross-browser compatibility
✅ Want modern DX (HMR, TypeScript, auto-reload)
✅ Publishing to multiple stores
✅ Complex extensions with multiple entry points

## Alternative: Plasmo

**Best for React developers:**
- Next.js-like file-based routing
- Automatic code splitting
- Built-in remote code bundling
- Very opinionated (React-centric)

```bash
# Create Plasmo extension
npm create plasmo

# Start development
npm run dev
```

### When to Use Plasmo
✅ React-only team
✅ Want Next.js-like DX
✅ Need remote code bundling
✅ Prefer opinionated frameworks

## Alternative: CRXJS (Vite Plugin)

**Minimal, unopinionated:**
- Just a Vite plugin (you control everything)
- Best-in-class HMR (especially for content scripts)
- Lightweight, minimal overhead
- Requires more manual setup

```bash
# Add to existing Vite project
npm install @crxjs/vite-plugin -D
```

### When to Use CRXJS
✅ Want maximum control
✅ Already using Vite
✅ Minimal tooling preference
✅ Expert developer team

## Toolchain Comparison

| | WXT | Plasmo | CRXJS |
|---|---|---|---|
| **Frameworks** | All | React-focused | All |
| **Setup** | Batteries-included | Opinionated | Manual |
| **DX** | Excellent | Excellent | Great |
| **HMR** | Yes | Yes | Best |
| **Auto-publish** | Yes | Yes | No |
| **Learning Curve** | Low | Low | Medium |
| **Flexibility** | High | Medium | Highest |

## Project Structure (WXT)

```
my-extension/
├── entrypoints/
│   ├── background.ts      # Service worker
│   ├── content.ts         # Content script
│   ├── popup/             # Extension popup
│   │   ├── index.html
│   │   └── main.tsx
│   └── options/           # Options page
│       ├── index.html
│       └── main.tsx
├── components/            # Shared UI components
├── utils/                 # Shared utilities
├── public/                # Static assets
│   └── icon.png          # Extension icon
├── wxt.config.ts         # WXT configuration
└── package.json
```

## Manifest V3 Essentials

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt'

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',
    permissions: ['storage', 'tabs'],
    host_permissions: ['https://*.example.com/*'],
    action: {
      default_title: 'My Extension',
    },
  },
})
```

### Key Manifest V3 Changes
- **Service Workers** replace background pages (no DOM access)
- **`host_permissions`** separate from `permissions`
- **`scripting` API** for dynamic content script injection
- **No remotely hosted code** (bundle everything)
- **Limited `executeScript`** capabilities

## Communication Patterns

### Popup ↔ Background

```typescript
// popup/main.tsx
import browser from 'webextension-polyfill'

const response = await browser.runtime.sendMessage({
  type: 'GET_DATA',
  payload: { key: 'value' },
})

// background.ts
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GET_DATA') {
    // Process and respond
    sendResponse({ data: 'result' })
  }
  return true // Keep channel open for async response
})
```

### Content Script ↔ Background

```typescript
// content.ts
import browser from 'webextension-polyfill'

// Send message to background
const result = await browser.runtime.sendMessage({
  type: 'ANALYZE_PAGE',
  url: window.location.href,
})

// background.ts
browser.runtime.onMessage.addListener(async (message) => {
  if (message.type === 'ANALYZE_PAGE') {
    const analysis = await analyzePage(message.url)
    return { analysis }
  }
})
```

### Content Script ↔ Page (Web Page)

```typescript
// content.ts - inject into page context
const script = document.createElement('script')
script.src = browser.runtime.getURL('injected.js')
document.head.appendChild(script)

// Listen for messages from page
window.addEventListener('message', (event) => {
  if (event.source !== window) return
  if (event.data.type === 'FROM_PAGE') {
    // Handle message from page
  }
})

// injected.js (runs in page context, has access to page's window/DOM)
window.postMessage({ type: 'FROM_PAGE', data: 'value' }, '*')
```

## Storage Patterns

```typescript
// Using chrome.storage.sync (syncs across devices)
import browser from 'webextension-polyfill'

// Save
await browser.storage.sync.set({ key: 'value' })

// Load
const { key } = await browser.storage.sync.get('key')

// Listen for changes
browser.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'sync' && changes.key) {
    console.log('Value changed:', changes.key.newValue)
  }
})
```

## Essential Libraries

```bash
# Cross-browser compatibility
npm install webextension-polyfill

# State Management
npm install zustand

# Forms
npm install react-hook-form zod

# UI Components (if using React)
npm install @radix-ui/react-* # Headless components
```

## Testing Strategy

```bash
# Install testing libraries
npm install --save-dev vitest @testing-library/react @testing-library/user-event
npm install --save-dev @wxt-dev/testing
```

**Example test:**
```typescript
// popup/main.test.tsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Popup from './main'

describe('Popup', () => {
  it('renders heading', () => {
    render(<Popup />)
    expect(screen.getByRole('heading')).toBeInTheDocument()
  })
})
```

## Quality Gates Integration

```yaml
# .github/workflows/extension-ci.yml
name: Extension CI

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
      - run: npm run build

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: extension-build
          path: .output/
```

## Publishing Automation

```bash
# Build for all browsers
npm run build              # Chrome
npm run build:firefox      # Firefox
npm run build:safari       # Safari

# Zip for submission
npm run zip                # All stores

# Or use WXT's publish command (requires API keys)
wxt publish --chrome --firefox
```

**Store submission setup:**
```typescript
// wxt.config.ts
export default defineConfig({
  zip: {
    artifactTemplate: '{{name}}-{{version}}-{{browser}}.zip',
  },
  manifest: {
    name: '__MSG_extName__',
    description: '__MSG_extDescription__',
    default_locale: 'en',
  },
})
```

## Performance Best Practices

- **Lazy load content scripts**: Only inject when needed
- **Use storage efficiently**: Minimize sync storage writes
- **Debounce frequent operations**: Especially in content scripts
- **Minimize background script work**: Use alarms/events, not intervals
- **Optimize bundle size**: Code splitting, tree shaking

## Security Considerations

```typescript
// Content Security Policy
manifest: {
  content_security_policy: {
    extension_pages: "script-src 'self'; object-src 'self'"
  }
}

// Validate messages
browser.runtime.onMessage.addListener((message) => {
  // Always validate message structure
  if (typeof message !== 'object' || !message.type) {
    return
  }

  // Type guard
  if (message.type === 'EXPECTED_TYPE') {
    // Process
  }
})

// Never inject user content directly into DOM
// Use textContent, not innerHTML
element.textContent = userInput // Safe
element.innerHTML = userInput   // XSS vulnerability!
```

## Common Gotchas

**Service Worker Lifecycle:**
- Service workers can be terminated anytime
- Use `chrome.storage` for persistence, not in-memory state
- Set up event listeners at top level (not inside async functions)

**Content Script Isolation:**
- Content scripts run in isolated world
- No direct access to page's JavaScript
- Must use `postMessage` to communicate with page

**Manifest V3 Restrictions:**
- No `eval()` or `new Function()`
- No inline scripts in HTML
- All code must be bundled
- Limited service worker APIs

## Recommendation Flow

```
New browser extension:
├─ Multi-framework team → WXT ✅
├─ React-only team → Plasmo
└─ Want maximum control → CRXJS

Existing extension (Manifest V2):
└─ Migrate to WXT (handles V2→V3 migration)
```

When agents design browser extensions, they should:
- Default to WXT for new projects (framework-agnostic, best DX)
- Use Manifest V3 (V2 deprecated in 2024)
- Apply quality-gates skill for testing/CI setup
- Use webextension-polyfill for cross-browser compatibility
- Follow Content Security Policy strictly
- Plan for service worker lifecycle (no persistent background page)
- Use chrome.storage for state persistence
- Validate all messages between components
