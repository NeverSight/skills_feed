---
name: spa-reverse-engineer
description: Reverse engineer Single Page Applications built with React + Vite + Workbox — analyze SPA internals via Chrome DevTools Protocol (CDP), write browser extensions, intercept service workers, and extract runtime state for SDK integration.
context: fork
agent: spa-expert
---

# SPA Reverse Engineering — React + Vite + Workbox + CDP

Reverse engineer modern SPAs to extract APIs, intercept service workers, debug runtime state, and build tooling.

## When to use

Use this skill when:
- Analyzing perplexity.ai SPA internals (React component tree, state, hooks)
- Intercepting Workbox service worker caching and request strategies
- Using Chrome DevTools Protocol (CDP) to automate browser interactions
- Building Chrome extensions for traffic interception or state extraction
- Debugging Vite-bundled source maps and module graph
- Extracting GraphQL/REST schemas from SPA network layer
- Writing Puppeteer/Playwright scripts for automated API discovery

## Instructions

### Step 1: Identify SPA Stack

Detect the technology stack of the target SPA:

```javascript
// In DevTools Console:

// React detection
window.__REACT_DEVTOOLS_GLOBAL_HOOK__  // React DevTools presence
document.querySelector('#__next')  // Next.js
document.querySelector('#root')    // Vite/CRA
document.querySelector('#app')     // Vue (for comparison)

// Vite detection
document.querySelector('script[type="module"]')  // ESM modules
// Check source for /@vite/client or /.vite/ paths

// Workbox / Service Worker
navigator.serviceWorker.getRegistrations()  // List SWs
// Check Application → Service Workers in DevTools

// State management
window.__REDUX_DEVTOOLS_EXTENSION__  // Redux
// React DevTools → Components → hooks for Zustand/Jotai/Recoil
```

### Step 2: React Internals Analysis

#### Component Tree Extraction

```javascript
// Get React fiber tree from any DOM element
function getFiber(element) {
    const key = Object.keys(element).find(k =>
        k.startsWith('__reactFiber$') || k.startsWith('__reactInternalInstance$')
    );
    return element[key];
}

// Walk fiber tree
function walkFiber(fiber, depth = 0) {
    if (!fiber) return;
    const name = fiber.type?.displayName || fiber.type?.name || fiber.type;
    if (typeof name === 'string') {
        console.log('  '.repeat(depth) + name);
    }
    walkFiber(fiber.child, depth + 1);
    walkFiber(fiber.sibling, depth);
}

// Start from root
const root = document.getElementById('root');
walkFiber(getFiber(root));
```

#### State & Props Extraction

```javascript
// Extract component state via fiber
function getComponentState(fiber) {
    const state = [];
    let hook = fiber.memoizedState;
    while (hook) {
        state.push(hook.memoizedState);
        hook = hook.next;
    }
    return state;
}

// Find specific component by name
function findComponent(fiber, name) {
    if (!fiber) return null;
    if (fiber.type?.name === name || fiber.type?.displayName === name) {
        return fiber;
    }
    return findComponent(fiber.child, name) || findComponent(fiber.sibling, name);
}
```

### Step 3: Vite Bundle Analysis

#### Source Map Extraction

```bash
# Find source maps from bundled assets
curl -s https://www.perplexity.ai/ | grep -oP 'src="[^"]*\.js"' | while read src; do
    url=$(echo $src | grep -oP '"[^"]*"' | tr -d '"')
    echo "Checking: $url"
    curl -sI "https://www.perplexity.ai${url}.map" | head -5
done
```

#### Module Graph

```javascript
// In Vite dev mode (if accessible):
// /__vite_module_graph shows dependency graph

// In production — analyze chunks:
// Performance → Network → JS files → Initiator chain
// Sources → Webpack/Vite tree → module paths
```

### Step 4: Service Worker & Workbox Interception

#### Analyze Caching Strategy

```javascript
// List all cached URLs
async function listCaches() {
    const names = await caches.keys();
    for (const name of names) {
        const cache = await caches.open(name);
        const keys = await cache.keys();
        console.log(`Cache: ${name} (${keys.length} entries)`);
        keys.forEach(k => console.log(`  ${k.url}`));
    }
}

// Intercept SW fetch events (from SW scope)
self.addEventListener('fetch', event => {
    console.log('[SW Intercept]', event.request.method, event.request.url);
});
```

#### Workbox Strategy Detection

```javascript
// Common Workbox strategies to look for in SW source:
// - CacheFirst       → Static assets (fonts, images)
// - NetworkFirst     → API calls (dynamic data)
// - StaleWhileRevalidate → Frequently updated content
// - NetworkOnly      → Always fresh (auth endpoints)
// - CacheOnly        → Offline-only content

// Check SW source for workbox patterns:
// workbox.strategies.CacheFirst
// workbox.routing.registerRoute
// workbox.precaching.precacheAndRoute
```

### Step 5: Chrome DevTools Protocol (CDP)

#### Automated Interception via CDP

```python
import asyncio
from playwright.async_api import async_playwright

async def intercept_with_cdp():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Enable CDP domains
        cdp = await page.context.new_cdp_session(page)

        # Intercept network at CDP level
        await cdp.send('Network.enable')
        cdp.on('Network.requestWillBeSent', lambda params:
            print(f"[CDP] {params['request']['method']} {params['request']['url']}")
        )
        cdp.on('Network.responseReceived', lambda params:
            print(f"[CDP] {params['response']['status']} {params['response']['url']}")
        )

        # Intercept WebSocket frames
        await cdp.send('Network.enable')
        cdp.on('Network.webSocketFrameSent', lambda params:
            print(f"[WS→] {params['response']['payloadData'][:200]}")
        )
        cdp.on('Network.webSocketFrameReceived', lambda params:
            print(f"[←WS] {params['response']['payloadData'][:200]}")
        )

        await page.goto('https://www.perplexity.ai/')
        await page.wait_for_timeout(60000)
```

#### Runtime JS Evaluation via CDP

```python
# Execute JS in page context
result = await cdp.send('Runtime.evaluate', {
    'expression': 'JSON.stringify(window.__NEXT_DATA__)',
    'returnByValue': True,
})
next_data = json.loads(result['result']['value'])
```

### Step 6: Chrome Extension Development

#### Manifest v3 Extension for Traffic Capture

```json
{
    "manifest_version": 3,
    "name": "pplx-sdk Traffic Capture",
    "version": "1.0",
    "permissions": [
        "webRequest", "activeTab", "storage", "debugger"
    ],
    "host_permissions": ["https://www.perplexity.ai/*"],
    "background": {
        "service_worker": "background.js"
    },
    "content_scripts": [{
        "matches": ["https://www.perplexity.ai/*"],
        "js": ["content.js"],
        "run_at": "document_start"
    }]
}
```

#### Background Script — Request Interception

```javascript
// background.js
chrome.webRequest.onBeforeRequest.addListener(
    (details) => {
        if (details.url.includes('/rest/')) {
            console.log('[pplx-capture]', details.method, details.url);
            if (details.requestBody?.raw) {
                const body = new TextDecoder().decode(
                    new Uint8Array(details.requestBody.raw[0].bytes)
                );
                chrome.storage.local.set({
                    [`req_${Date.now()}`]: {
                        url: details.url,
                        method: details.method,
                        body: JSON.parse(body),
                        timestamp: Date.now()
                    }
                });
            }
        }
    },
    { urls: ["https://www.perplexity.ai/rest/*"] },
    ["requestBody"]
);
```

#### Content Script — React State Extraction

```javascript
// content.js — inject into page context
const script = document.createElement('script');
script.textContent = `
    // Hook into React state updates
    const origSetState = React.Component.prototype.setState;
    React.Component.prototype.setState = function(state, cb) {
        window.postMessage({
            type: 'PPLX_STATE_UPDATE',
            component: this.constructor.name,
            state: JSON.parse(JSON.stringify(state))
        }, '*');
        return origSetState.call(this, state, cb);
    };
`;
document.documentElement.appendChild(script);

// Listen for state updates
window.addEventListener('message', (event) => {
    if (event.data.type === 'PPLX_STATE_UPDATE') {
        chrome.runtime.sendMessage(event.data);
    }
});
```

### Step 7: Map Discoveries to SDK

| SPA Discovery | SDK Target | Action |
|--------------|-----------|--------|
| React component state | `domain/models.py` | Model the state shape |
| API fetch calls | `transport/http.py` | Add endpoint methods |
| SSE event handlers | `transport/sse.py` | Map event types |
| Service worker cache | `shared/` | Understand caching behavior |
| Auth token flow | `shared/auth.py` | Token refresh logic |
| WebSocket frames | `transport/` | New WebSocket transport |
| GraphQL queries | `domain/` | Query/mutation services |

### Step 8: SPA Source Code Graph

After runtime analysis, build a **static code graph** of the SPA source. Delegate to `codegraph` for structural analysis.

#### Source Map Recovery

```bash
# Extract original source paths from source maps
curl -s https://www.perplexity.ai/ | grep -oP 'src="(/[^"]*\.js)"' | while read -r url; do
    echo "Checking: $url"
    curl -s "https://www.perplexity.ai${url}.map" 2>/dev/null | \
        python3 -c "import sys,json; d=json.load(sys.stdin); print('\n'.join(d.get('sources',[])))" 2>/dev/null
done | sort -u
```

#### Static Analysis (from recovered source or public repo)

```bash
# Component tree from source
grep -rn "export \(default \)\?function \|export const .* = (" src/ --include="*.tsx" --include="*.jsx"

# Import graph
grep -rn "import .* from " src/ --include="*.ts" --include="*.tsx" | \
    awk -F: '{print $1 " → " $NF}' | sort -u

# Hook usage map
grep -rn "use[A-Z][a-zA-Z]*(" src/ --include="*.tsx" | \
    grep -oP 'use[A-Z][a-zA-Z]*' | sort | uniq -c | sort -rn

# API call sites (fetch, axios, etc.)
grep -rn "fetch(\|axios\.\|api\.\|apiClient\." src/ --include="*.ts" --include="*.tsx"
```

#### Cross-Reference: Runtime ↔ Static

| Runtime Discovery (spa-expert) | Static Discovery (codegraph) | Cross-Reference |
|-------------------------------|------------------------------|-----------------|
| Fiber tree component names | Source component definitions | Match names to source files |
| Hook state values | Hook implementations | Map state shape to hook logic |
| Network API calls | `fetch()`/`axios` call sites | Confirm endpoints in source |
| Context provider values | `createContext()` definitions | Map runtime state to types |
| Service worker routes | Workbox config in source | Validate caching strategy |

## Perplexity.ai SPA Notes

### Known Stack
- **Framework**: Next.js (React 18+)
- **Bundler**: Webpack (via Next.js, not raw Vite — skill covers both for broader SPA RE)
- **State**: React hooks + context (observed patterns)
- **Streaming**: SSE via fetch() with ReadableStream
- **Auth**: Cookie-based (`pplx.session-id`)

### Key DOM Selectors
```javascript
// Query input
document.querySelector('textarea[placeholder*="Ask"]')
// Response area
document.querySelector('[class*="prose"]')
// Thread list
document.querySelector('[class*="thread"]')
```
