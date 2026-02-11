---
name: inertia-adonisjs
description: Build AdonisJS 6 + Inertia.js (React) applications from scratch through production. Full lifecycle - setup, pages, forms, shared data, debugging.
---

<essential_principles>
## How Inertia + AdonisJS Works

Inertia is a bridge between AdonisJS and React. You keep server-side routing and controllers, while the client swaps page components without full reloads.

### 1. Server-Driven Pages

Controllers render Inertia responses with props:

```ts
return ctx.inertia.render("users/show", { user: new UserDto(user) });
```

### 2. No Client-Side Routing

Routes live in `start/routes.ts`. Inertia intercepts links and form submissions, making XHR requests and swapping components.

### 3. DTOs for Props

Props are sent to the client. Use DTOs to control the shape and avoid leaking fields.

### 4. Validation at the Edge

Validate on the server with VineJS. Let the validator throw and let Inertia handle the errors.
</essential_principles>

<intake>
**What would you like to do?**

1. Set up Inertia in AdonisJS
2. Create a new page/component
3. Build a form with validation
4. Debug an Inertia issue
5. Something else

**Then read the matching workflow from `workflows/` and follow it.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "setup", "install", "start", "new" | `workflows/setup-inertia.md` |
| 2, "page", "component", "create", "render" | `workflows/create-page.md` |
| 3, "form", "validation", "submit", "useForm" | `workflows/build-form.md` |
| 4, "debug", "fix", "error", "not working" | `workflows/debug-inertia.md` |
| 5, other | Clarify, then select workflow or references |
</routing>

<verification_loop>
## After Every Change

1. **Does the page render?** Check for `X-Inertia` response header
2. **Are props received?** `console.log(usePage().props)`
3. **Does navigation work?** Links should not full-reload
4. **Do forms submit?** Check Network tab for XHR requests
5. **Are errors displayed?** Trigger validation failure

```ts
// Frontend debug
console.log(usePage().props);
```

Report to the user:
- "Inertia response: ok"
- "Props received: X keys"
- "Navigation: SPA mode ok"
</verification_loop>

<reference_index>
## Domain Knowledge

All in `references/`:

**Core:** setup.md, responses.md, forms.md, validation.md
**Data Flow:** shared-data.md, links.md
**Quality:** testing.md
**Cookbook:** cookbook.md
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| setup-inertia.md | Install and configure Inertia for AdonisJS |
| create-page.md | Build new pages with props |
| build-form.md | Forms with validation and useForm |
| debug-inertia.md | Find and fix Inertia issues |
</workflows_index>
