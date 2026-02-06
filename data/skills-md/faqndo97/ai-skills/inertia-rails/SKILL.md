---
name: inertia-rails
description: Build Rails + Inertia.js applications from scratch through production. Full lifecycle - setup, pages, forms, validation, shared data, authentication. Covers React/Vue/Svelte frontends with Vite bundling. Includes cookbook for shadcn/ui, modals, meta tags, and error handling.
---

<essential_principles>
## How Inertia Rails Works

Inertia is a bridge between Rails and modern JavaScript frameworks (React, Vue, Svelte). It lets you build SPAs using classic server-side routing and controllers—no client-side routing or separate APIs needed.

### 1. Server-Driven Architecture

Controllers render Inertia responses instead of views. Data flows from Rails to JavaScript components as props:
```ruby
render inertia: 'Users/Show', props: { user: user.as_json }
```

### 2. No Client-Side Routing

Routes live in `config/routes.rb`. Inertia intercepts link clicks and form submissions, making XHR requests that return JSON with component name and props. The client swaps components without full page reloads.

### 3. Convention-Based Component Resolution

By default, `render inertia: { user: }` in `UsersController#show` renders `app/frontend/pages/users/show.(jsx|vue|svelte)`. Override with explicit component names when needed.

### 4. Validation via Redirects

Unlike typical SPAs returning 422 JSON responses, Inertia follows traditional Rails patterns:
1. Controller validates and redirects back on failure
2. Errors are flashed and shared as props
3. Form state is preserved automatically

### 5. Shared Data Pattern

Use `inertia_share` in controllers to provide data to all pages (current_user, flash messages, notifications). Data is included in every response—use sparingly.
</essential_principles>

<intake>
**What would you like to do?**

1. Set up Inertia in a Rails project
2. Create a new page/component
3. Build a form with validation
4. Add shared data (auth, flash, etc.)
5. Handle redirects and navigation
6. Debug an Inertia issue
7. Test an Inertia controller
8. Optimize with partial reloads
9. Something else

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "setup", "install", "start", "new" | `workflows/setup-inertia.md` |
| 2, "page", "component", "create", "render" | `workflows/create-page.md` |
| 3, "form", "validation", "submit", "useForm" | `workflows/build-form.md` |
| 4, "shared", "auth", "flash", "current_user" | `workflows/shared-data.md` |
| 5, "redirect", "navigate", "link", "router" | `workflows/navigation.md` |
| 6, "debug", "fix", "error", "not working" | `workflows/debug-inertia.md` |
| 7, "test", "spec", "minitest", "rspec" | `workflows/testing.md` |
| 8, "partial", "reload", "optimize", "only" | `workflows/partial-reloads.md` |
| 9, other | Clarify, then select workflow or references |

**After reading the workflow, follow it exactly.**
</routing>

<verification_loop>
## After Every Change

1. **Does the page render?** Check Rails logs for Inertia response
2. **Are props received?** Console.log props in component
3. **Does navigation work?** Click links - should not full-reload
4. **Do forms submit?** Check Network tab for XHR requests
5. **Are errors displayed?** Test validation failures

```ruby
# Rails debug - check response type
render inertia: 'Page', props: { debug: true }
```

```javascript
// Frontend debug - log all props
console.log(usePage().props)
```

Report to the user:
- "Inertia response: ✓"
- "Props received: X keys"
- "Navigation: SPA mode ✓/✗"
- "Ready for testing"
</verification_loop>

<reference_index>
## Domain Knowledge

All in `references/`:

**Core:** setup.md, responses.md, forms.md, validation.md
**Data Flow:** shared-data.md, links.md
**Quality:** testing.md
**Cookbook:** cookbook.md (shadcn/ui, Inertia Modal, meta tags, error types)
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| setup-inertia.md | Install and configure Inertia Rails |
| create-page.md | Build new pages with props |
| build-form.md | Forms with validation and useForm |
| shared-data.md | Share auth/flash across all pages |
| navigation.md | Links, redirects, router methods |
| debug-inertia.md | Find and fix Inertia issues |
| testing.md | Test Inertia controllers |
| partial-reloads.md | Optimize with selective data loading |
</workflows_index>
