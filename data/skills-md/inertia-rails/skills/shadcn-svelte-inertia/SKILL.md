---
name: shadcn-svelte-inertia
description: >-
  shadcn-svelte (bits-ui) component integration for Inertia Rails Svelte (NOT SvelteKit): forms, dialogs,
  tables, toasts, dark mode, and more. Use when building UI with shadcn-svelte components in an Inertia +
  Svelte app or adapting shadcn-svelte examples from SvelteKit. Wire shadcn-svelte inputs to Inertia Form
  via name attribute and {#snippet} syntax. Flash toasts require Rails flash_keys initializer config.
---

# shadcn-svelte for Inertia Rails

shadcn-svelte (bits-ui) patterns adapted for Inertia.js + Rails + Svelte. NOT SvelteKit.

**Before using a shadcn-svelte example, ask:**
- **Does it use SvelteKit-specific APIs?** (`goto`, `$app/navigation`, `load` functions, `+page.svelte`) → Replace with Inertia `router`, server props, page components
- **Does it use `sveltekit-superforms` + `zod`?** → Replace with Inertia `<Form>` + `name` attributes. Inertia handles CSRF, errors, redirects, processing state.

## Key Differences from SvelteKit Defaults

| shadcn-svelte default (SvelteKit) | Inertia equivalent |
|---|---|
| `goto()` from `$app/navigation` | `router` from `@inertiajs/svelte` |
| `load` functions | Server-rendered props via Rails controller |
| `+page.svelte` / `+layout.svelte` | Default exports with module script layout |
| `sveltekit-superforms` + `zod` | Inertia `<Form>` component |
| `<svelte:head>` (SvelteKit auto-manages) | `<svelte:head>` (same — no Inertia `<Head>` in Svelte) |

## Setup

`npx shadcn-svelte@latest init`. Add `@/` resolve aliases to `tsconfig.json` if not present.
**Do NOT add `@/` resolve aliases to `vite.config.ts`** — `vite-plugin-ruby` already provides them.

## shadcn-svelte Inputs in Inertia `<Form>`

Use plain shadcn-svelte `Input`/`Label`/`Button` with `name` attributes inside Inertia `<Form>`.
See `inertia-rails-forms` skill (+ `references/svelte.md`) for full `<Form>` API.

**The key pattern:** Use `{#snippet}` to access form state:

```svelte
<script lang="ts">
  import { Form } from '@inertiajs/svelte'
  import { Input } from '$lib/components/ui/input'
  import { Label } from '$lib/components/ui/label'
  import { Button } from '$lib/components/ui/button'
</script>

<Form method="post" action="/users">
  {#snippet children({ errors, processing })}
    <div class="space-y-4">
      <div>
        <Label for="name">Name</Label>
        <Input id="name" name="name" />
        {#if errors.name}<p class="text-sm text-destructive">{errors.name}</p>{/if}
      </div>

      <div>
        <Label for="email">Email</Label>
        <Input id="email" name="email" type="email" />
        {#if errors.email}<p class="text-sm text-destructive">{errors.email}</p>{/if}
      </div>

      <Button type="submit" disabled={processing}>
        {processing ? 'Creating...' : 'Create User'}
      </Button>
    </div>
  {/snippet}
</Form>
```

Svelte 4: `<Form let:errors let:processing>` instead of `{#snippet}`.

**`<Select>` requires `name` prop** for Inertia `<Form>` integration:

```svelte
<Select name="role" value="member">
  <SelectTrigger><SelectValue placeholder="Select role" /></SelectTrigger>
  <SelectContent>
    <SelectItem value="admin">Admin</SelectItem>
    <SelectItem value="member">Member</SelectItem>
  </SelectContent>
</Select>
```

## Dialog with Inertia Navigation

```svelte
<script lang="ts">
  import { Dialog, DialogContent, DialogHeader, DialogTitle } from '$lib/components/ui/dialog'
  import { router } from '@inertiajs/svelte'

  let { open, user }: { open: boolean; user: User } = $props()
</script>

<Dialog
  {open}
  onOpenChange={(isOpen) => { if (!isOpen) router.replaceProp('show_dialog', false) }}
>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>{user.name}</DialogTitle>
    </DialogHeader>
    <!-- content -->
  </DialogContent>
</Dialog>
```

Svelte 4: `on:openChange` instead of `onOpenChange`.

## Table with Server-Side Sorting

```svelte
<script lang="ts">
  import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '$lib/components/ui/table'
  import { router } from '@inertiajs/svelte'

  let { users, sort }: { users: User[]; sort: string } = $props()

  const handleSort = (column: string) => {
    router.get('/users', { sort: column }, { preserveState: true })
  }
</script>

<Table>
  <TableHeader>
    <TableRow>
      <TableHead class="cursor-pointer" onclick={() => handleSort('name')}>
        Name {sort === 'name' ? '↑' : ''}
      </TableHead>
      <TableHead>Email</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {#each users as user (user.id)}
      <TableRow>
        <TableCell>{user.name}</TableCell>
        <TableCell>{user.email}</TableCell>
      </TableRow>
    {/each}
  </TableBody>
</Table>
```

Use `<Link>` or `use:inertia` (not `<a>`) for row links to preserve SPA navigation.

## Toast with Flash Messages

Flash config (`flash_keys`) is in `inertia-rails-controllers`. Flash access
(`$page.flash`) is in `inertia-rails-pages`. This section covers **toast UI wiring only**.

**MANDATORY — READ ENTIRE FILE** when implementing flash-based toasts with Sonner:
[`references/flash-toast.md`](references/flash-toast.md) (~80 lines) — full flash
watcher and svelte-sonner integration. **Do NOT load** if only reading flash values without toast UI.

## Dark Mode

`npx shadcn-svelte@latest init` generates CSS variables for light/dark and
`@custom-variant dark (&:is(.dark *));` in your CSS (Tailwind v4).

**CRITICAL — prevent flash of wrong theme (FOUC):** Add an inline script in
`<head>` (before Svelte hydrates):

```erb
<%# app/views/layouts/application.html.erb — in <head>, before any stylesheets %>
<script>
  document.documentElement.classList.toggle(
    "dark",
    localStorage.appearance === "dark" ||
      (!("appearance" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches),
  );
</script>
```

Use a `useAppearance` pattern (light/dark/system modes, localStorage persistence,
`matchMedia` listener). Toggle via `.dark` class on `<html>`.

## `<svelte:head>` Instead of `<Head>`

Svelte uses native `<svelte:head>` — there is no Inertia `<Head>` component for Svelte.
This applies in shadcn patterns too (e.g., setting page title in dialog views):

```svelte
<svelte:head>
  <title>{user.name} - Profile</title>
</svelte:head>
```

## Svelte-Specific Gotchas

**`bind:value` does NOT work with Inertia `<Form>`** — `<Form>` reads values
from input `name` attributes on submit, not from Svelte's reactive bindings.
Using `bind:value` creates a second source of truth that `<Form>` ignores:

```svelte
<!-- BAD — bind:value is ignored by <Form> on submit -->
<Form method="post" action="/users">
  <Input bind:value={name} />
</Form>

<!-- GOOD — name attribute is what <Form> reads -->
<Form method="post" action="/users">
  <Input name="name" />
</Form>
```

Use `bind:value` only with `useForm` (where you explicitly manage `$form.name`).

**`$page` store updates are reactive, but destructured values are not:**

```svelte
<script lang="ts">
  import { page } from '@inertiajs/svelte'

  // BAD — snapshot, won't update after navigation:
  // let user = $page.props.auth.user

  // GOOD — use $derived for reactive access:
  let user = $derived($page.props.auth.user)
</script>
```

Svelte 4: use `$: user = $page.props.auth.user` (reactive statement).

**`use:inertia` directive as alternative to `<Link>`** — for elements that
can't be `<Link>` (e.g., table rows, custom components), use the action:

```svelte
<script lang="ts">
  import { inertia } from '@inertiajs/svelte'
</script>

<tr use:inertia={{ href: `/users/${user.id}` }} class="cursor-pointer">
  <td>{user.name}</td>
</tr>
```

**bits-ui transition props and Inertia navigation** — bits-ui components with
`transition*` props may show stale content during Inertia page transitions if
the exit animation outlasts the navigation. Set short durations or use
`forceMount` on content that depends on page props.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Form components crash | Using shadcn-svelte form components that depend on superforms | Replace with plain `Input`/`Label` + `errors.field` display |
| `Select` value not submitted | Missing `name` prop | Add `name="field"` to `<Select>` |
| Dialog closes unexpectedly | Missing or wrong `onOpenChange` handler | Use `onOpenChange={(open) => { if (!open) closeHandler() }}` |
| Flash of wrong theme (FOUC) | Missing inline `<script>` in `<head>` | Add dark mode script before stylesheets |
| `bind:value` not submitted | `<Form>` reads `name` attrs, not Svelte bindings | Use `name` attribute; reserve `bind:value` for `useForm` only |
| Shared props stale after navigation | Destructured `$page` without `$derived` | Use `$derived($page.props.auth.user)` for reactive access |

## Related Skills
- **Form component** → `inertia-rails-forms` + `references/svelte.md` (`<Form>` snippet, useForm)
- **Flash config** → `inertia-rails-controllers` (flash_keys initializer)
- **Flash access** → `inertia-rails-pages` + `references/svelte.md` ($page.flash)
- **URL-driven dialogs** → `inertia-rails-pages` + `references/svelte.md` (router.get pattern)
- **`use:inertia` directive** → `inertia-rails-pages` + `references/svelte.md`

## References

Load [`references/components.md`](references/components.md) (~200 lines) when building
shadcn-svelte components beyond those shown above (Accordion, Sheet, Tabs, DropdownMenu,
AlertDialog with Inertia patterns).

**Do NOT load** `components.md` for basic Form, Select, Dialog, or Table usage —
the examples above are sufficient.
