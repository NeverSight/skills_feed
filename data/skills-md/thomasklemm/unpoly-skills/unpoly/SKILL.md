---
name: unpoly
description: >
  Comprehensive guide for building server-rendered apps with Unpoly — a progressive
  enhancement framework that adds SPA-like behavior through HTML attributes.
  Use when working with Unpoly fragment updates, overlays/layers, forms, compilers,
  caching, lazy loading, animations, transitions, error handling, polling, the render lifecycle, or server integration.
  Covers [up-follow], [up-target], [up-layer], [up-submit], [up-validate], up.compiler(),
  up.render(), up.layer.open(), caching, previews, optimistic rendering, and more.
---

# Unpoly

Unpoly enhances server-rendered HTML so links and forms update page fragments instead
of full pages, without building a SPA. The server still renders HTML — Unpoly handles
the smart patching, caching, overlays, and lifecycle.

**Current version:** 3.12 — [API reference](https://unpoly.com/api) | [Changelog](https://unpoly.com/changes)

## Core mental model

1. **Fragments** — CSS-selector-targeted pieces of a page that get swapped on navigation
2. **Layers** — A stack of contexts (root + any number of overlays)
3. **Compilers** — JS functions that run whenever matching elements are inserted into the DOM
4. **Navigation** — Link/form interactions that change history and trigger fragment updates

## Quick reference: key HTML attributes

| Attribute | Purpose |
|-----------|---------|
| `[up-follow]` | Follow link as fragment update |
| `[up-target]` | CSS selector of fragment to replace |
| `[up-layer="new"]` | Open response in overlay |
| `[up-layer="new drawer\|popup\|modal"]` | Open in specific overlay mode |
| `[up-layer="swap"]` | Replace current overlay instead of stacking |
| `[up-layer="shatter"]` | Dismiss all overlays, then open from root |
| `[up-submit]` | Submit form as fragment update |
| `[up-validate]` | Validate field against server on blur |
| `[up-watch]` | Watch field changes and auto-submit |
| `[up-autosubmit]` | Auto-submit form on field change |
| `[up-hungry]` | Optionally update element whenever it appears in any response |
| `[up-preload]` | Preload link on hover (or `insert`/`reveal`) |
| `[up-instant]` | Follow link on mousedown, not click |
| `[up-back]` | Navigate to previous URL |
| `[up-defer]` | Lazy-load a fragment (on `insert`, `reveal`, or `manual`) |
| `[up-poll]` | Periodically reload a fragment |
| `[up-keep]` | Preserve element across fragment updates |
| `[up-id]` | Unique identifier for target derivation (alternative to `[id]`) |
| `[up-transition]` | CSS animation between old and new content |
| `[up-switch]` | Show/hide/enable/disable elements based on field value |
| `[up-disable]` | Disable fields/buttons during request |
| `[up-confirm]` | Show confirmation dialog before following |
| `[up-content]` | Open overlay from inline HTML (no request) |
| `[up-accept-event]` | Close+accept overlay when named event fires (payload becomes `value`) |
| `[up-dismiss-event]` | Close+dismiss overlay when named event fires |
| `[up-form-group]` | Mark container as the validation group for `[up-validate]` |
| `[up-main]` | Declare which element is the main target for a specific overlay mode |
| `[up-nav]` | Mark container as nav — links get `.up-current` when matching URL |
| `[up-alias]` | Additional URL patterns that also trigger `.up-current` on a link |
| `[up-meta]` | Mark `<head>` element for syncing during history changes |
| `[up-flashes]` | Designated container for server flash/notification messages |
| `[up-preview]` | Named preview function(s) to show while loading |
| `[up-placeholder]` | HTML or template selector to show while a fragment loads |
| `[up-emit]` | Emit a custom event on click (no navigation) |
| `[up-clickable]` | Make a non-interactive element behave like a button (adds ARIA role, tabindex) |
| `[up-expand]` | Make a container clickable by delegating to a child link |

## Quick reference: key JS functions

```js
up.render({ target: '.content', url: '/page' })  // Render fragment from URL
up.navigate({ url: '/page' })                    // Navigate (updates history, cache, scroll, focus)
up.follow(linkElement)                            // Follow a link
up.submit(formElement)                            // Submit a form
up.reload('.sidebar')                             // Reload a fragment from its source URL
up.visit('/page')                                 // Navigate to URL, updating main target
up.request('/api/data')                           // Make a raw AJAX request (returns up.Request)

up.layer.open({ url: '/modal', layer: 'new' })   // Open overlay
up.layer.ask({ url: '/picker' })                  // Open overlay as promise (resolves on accept)
up.layer.current                                  // Current layer
up.layer.accept(value)                            // Close overlay with value
up.layer.dismiss(value)                           // Dismiss overlay
up.layer.dismissOverlays()                        // Dismiss all overlays

up.compiler('.widget', (element, data) => { })   // Register compiler
up.macro('[my-attr]', (element) => { })           // Register macro (runs before compilers)
up.preview('name', (preview) => { })              // Register named preview
up.on('up:fragment:inserted', handler)            // Listen to events
up.emit(element, 'my:event', { id: 5 })          // Emit custom event

up.cache.expire()                                 // Mark all cache stale (triggers revalidation)
up.cache.evict()                                  // Clear all cache entries
up.network.isBusy()                               // true if any request in flight

up.fragment.get('.content')                       // Layer-aware element lookup
up.fragment.source(element)                       // URL fragment was loaded from
up.fragment.abort(element)                        // Abort requests for a fragment

up.history.location                               // Current URL
up.history.previousLocation                       // Previous URL
```

## Server response headers

| Header | Purpose |
|--------|---------|
| `X-Up-Target` | Override which fragment to update (`:none` skips rendering) |
| `X-Up-Accept-Layer: value` | Accept overlay from server (JSON value) |
| `X-Up-Dismiss-Layer: value` | Dismiss overlay from server (JSON value) |
| `X-Up-Open-Layer: {}` | Force-open overlay from server |
| `X-Up-Events: [...]` | Emit events on the frontend |
| `X-Up-Context: {}` | Merge JSON into current layer context (only changed keys) |
| `X-Up-Location` | Override the URL pushed to history |
| `X-Up-Title` | Override document title (JSON-encoded string) |
| `X-Up-Method` | HTTP method for history URL |
| `X-Up-Poll: stop` | Stop a polling element |
| `X-Up-Expire-Cache` | Expire matching client-side cache entries |
| `X-Up-Evict-Cache` | Remove matching cache entries entirely |

## Reference files

Load these when the user's question covers that topic:

- **[installation.md](references/installation.md)** — Installing Unpoly via CDN, npm/bundler, or Ruby on Rails (importmap, jsbundling-rails, Sprockets, unpoly-rails gem)
- **[migration.md](references/migration.md)** — Upgrading with `unpoly-migrate.js`: how it works, install, upgrade workflow, keeping it permanently, 3.11 manual migration items
- **[fragments.md](references/fragments.md)** — Targeting, rendering options, client-side templates, handling all links/forms, `:main`, `:layer`, `:maybe`, `:origin`, `[up-hungry]`, `[up-keep]`, `[up-id]`, `[up-expand]`, fragment utility functions (`up.fragment.get/all/closest/source/abort`), `up.fragment.config`, `up.render()` options
- **[forms.md](references/forms.md)** — Form submission, validation (`[up-validate]`, `[up-validate-url/method/batch/params/headers]`), reactive forms (`[up-watch]`, `[up-autosubmit]`), form state switching (`[up-switch]`, `[up-switch-region]`), watch options, disabling forms, form utility functions
- **[layers.md](references/layers.md)** — Opening overlays, layer modes (`modal`, `drawer`, `popup`, `cover`), `[up-layer=swap/shatter]`, subinteractions, close conditions, accepting/dismissing layers, `up.layer.dismissOverlays()`, layer context, targeting layers
- **[performance.md](references/performance.md)** — Caching (`up.cache`, `up.network.config`), revalidation, lazy loading (`[up-defer]` with `insert`/`reveal`/`manual`), preloading, optimizing server responses, polling (`[up-poll]`), `up.network.isBusy()`, `X-Up-Expire-Cache`/`X-Up-Evict-Cache`
- **[loading-state.md](references/loading-state.md)** — CSS loading classes (`.up-active`, `.up-loading`, `.up-focus-visible/hidden`, `.up-scrollbar-away`), placeholders, previews (full `up.Preview` API), optimistic rendering, disabling forms, progress bar, offline handling
- **[compilers.md](references/compilers.md)** — Registering compilers, destructors, passing data, macros, `up.hello()`, integrating JS libraries, context
- **[navigation.md](references/navigation.md)** — Navigation vs rendering, `[up-nav]`/`.up-current` active links, `[up-alias]`, `[up-meta]`, history config, scroll restoration, focus management, URL patterns, `up:click` event, `[up-preload]` timing values, `up:location:changed` properties
- **[animations.md](references/animations.md)** — Built-in animations/transitions, `/` transition composition, custom animations, `up.morph()`, `up.motion.finish()`, duration/easing, disabling animation
- **[error-handling.md](references/error-handling.md)** — Failed responses, `[up-fail-target]`, skipping rendering, conditional requests (ETags), network errors, `[up-flashes]`, flash messages
- **[lifecycle.md](references/lifecycle.md)** — Render lifecycle events (all fragment/layer/network/request events), controlling rendering, complete request/response header reference
