---
name: preact-buildless-frontend
description: Build-less ESM frontends that run directly in the browser without bundlers. Use this skill when creating static frontends, SPAs without build tools, prototypes, or when the user explicitly wants no Vite/Webpack/bundler. Covers import maps, CDN imports, cache-busting, hash routing, and performance patterns.
---

# Build-less ESM Frontend

Create frontends that run directly in the browser using ES modules—no bundler, no build step.

## Starter Template

Copy from `assets/starter/` for a working baseline:
- `index.html` — import map + module entry
- `app.js` — Preact + signals + hash routing
- `index.css` — CSS variables, dark mode

Run locally:
```bash
npx serve assets/starter   # or python3 -m http.server 3000
```

## Core Patterns

### 1. Import Maps

Use `<script type="importmap">` to:
- Map bare specifiers (`preact`) to CDN URLs
- Map directory aliases (`@utils/`) to local folders
- Attach `?v=<version>` for cache-busting

```html
<script type="importmap">
{
  "imports": {
    "preact": "https://cdn.jsdelivr.net/npm/preact@10.24.3/dist/preact.module.js",
    "@utils/": "./utils/",
    "./app.js": "./app.js?v=1.0.0"
  }
}
</script>
```

Generate this map dynamically (server middleware) or commit a static version.

### 2. CDN Imports

Import third-party ESM directly from CDN. Pin versions:

```js
import { signal } from 'https://cdn.jsdelivr.net/npm/@preact/signals@1.3.0/dist/signals.module.js';
```

Prefer mapping through import map to keep source clean:
```js
import { signal } from '@preact/signals';  // resolved via import map
```

### 3. Cache-Busting

Two approaches:

**A) Versioned URLs (recommended):**
- Append `?v=<git-sha|version|timestamp>` to local `.js` and `.css`
- Set `Cache-Control: immutable` headers

**B) ETag/Last-Modified:**
- Keep stable URLs, let browser revalidate

For dynamic injection, rewrite `index.html` at serve time. For static hosting, commit versioned URLs manually.

### 4. Subpath Mounting

If served under a subpath (e.g., `/app`), use `<base>`:

```html
<base href="/app/">
```

Ensures relative imports resolve correctly.

## Structure

Minimal:
```
frontend/
  index.html
  index.css
  app.js
```

Growing app:
```
frontend/
  index.html
  index.css
  app.js          # entry + router
  state.js        # signals/atoms
  api.js          # fetch helpers
  components/
    nav.js
  pages/
    home.js
    settings.js
```

## Configuration

Inject environment variables via global `window.ENV` (no build replacement).

**index.html:**
```html
<script src="/config.js"></script>
<script type="module" src="./app.js"></script>
```

**config.js:**
```js
window.ENV = {
  API_URL: "https://api.example.com"
};
```

Exclude `config.js` from caching or generate at runtime.

## Routing

Hash-based routing (no server config needed):

```js
const route = signal(location.hash.slice(1) || '/');
window.addEventListener('hashchange', () => {
  route.value = location.hash.slice(1) || '/';
});

// Links: <a href="#/about">About</a>
// Read: route.value === '/about'
```

For history API routing, the server must serve `index.html` for all routes.

## Lazy Loading

Load features on demand:

```js
button.onclick = async () => {
  const { heavyFeature } = await import('./heavy.js');
  heavyFeature();
};
```

Rule: if not needed for first paint, load lazily.

## Error Handling

Wrap dynamic imports:

```js
async function loadPage(name) {
  try {
    return await import(`./pages/${name}.js`);
  } catch (e) {
    console.error(`Failed to load ${name}:`, e);
    return { default: () => html`<p>Failed to load page.</p>` };
  }
}
```

## Type Safety

Use JSDoc + `jsconfig.json` for full type checking without TypeScript build step.

**jsconfig.json:**
```json
{ "compilerOptions": { "checkJs": true, "module": "ESNext" } }
```

**Code usage:**
```js
/** @type {import('./types.js').User} */
const user = await api.getUser();
```

## Performance

**Startup:**
- One `<script type="module">` entry
- Use `<link rel="modulepreload" href="...">` for critical deps (fixes waterfall)
- Import only what's needed for first paint

**Rendering (with framework):**
- Fine-grained reactivity (signals) over full re-renders
- Memoize expensive computations

**Rendering (vanilla DOM):**
- Event delegation on root
- Batch DOM writes (build fragment, insert once)
- Avoid layout thrash (don't interleave reads/writes)

**CSS:**
- CSS variables for theming
- Shallow selectors
- Avoid large frameworks

## Security

**Content Security Policy (CSP):**
Strict CSP blocks inline scripts. For inline import maps, use:
1. **Nonce:** `<script type="importmap" nonce="...">` (recommended)
2. **Hash:** `'sha256-...'` of the script content

Allow CDNs in `script-src`:
`Content-Security-Policy: script-src 'self' 'nonce-...' https://cdn.jsdelivr.net;`

## Deliverables

When asked to create a build-less frontend:

1. Frontend folder with `index.html`, `index.css`, entry JS
2. Import map with CDN deps + local modules
3. (Optional) Server config for cache headers / HTML rewriting

## Constraints

- No bundler, no transpilation
- `type="module"` everywhere
- Relative imports with `.js` extension (`./utils.js`)
- Bare imports only if mapped in import map

## Pitfalls

- **Bare imports without map** → browser error
- **Import cycles** → keep modules focused
- **Missing `<base>`** → broken imports on subpath
- **Eager imports** → slow startup; use lazy `import()`
- **Browser support** → import maps need Chrome 89+, Firefox 108+, Safari 16.4+

## Verification

After generating:
1. Start server (`npx serve` or `python3 -m http.server`)
2. Open in browser, check console for errors
3. Network panel: confirm `.js` loads as `type="module"`
4. If cache-busting: confirm `?v=...` in URLs