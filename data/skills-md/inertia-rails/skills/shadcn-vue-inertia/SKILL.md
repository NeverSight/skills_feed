---
name: shadcn-vue-inertia
description: >-
  shadcn-vue component integration for Inertia Rails Vue 3 (NOT Nuxt): forms, dialogs, tables, toasts, dark mode,
  and more. Use when building UI with shadcn-vue components in an Inertia + Vue app or adapting shadcn-vue
  examples from Nuxt. Wire shadcn-vue inputs to Inertia Form via name attribute and #default scoped slot.
  Flash toasts require Rails flash_keys initializer config.
---

# shadcn-vue for Inertia Rails

shadcn-vue patterns adapted for Inertia.js + Rails + Vue 3. NOT Nuxt.

**Before using a shadcn-vue example, ask:**
- **Does it use Nuxt-specific APIs?** (`useRouter`, `useFetch`, `<NuxtLink>`) → Replace with Inertia `router`, server props, `<Link>`
- **Does it use `vee-validate` + `zod`?** → Replace with Inertia `<Form>` + `name` attributes. Inertia handles CSRF, errors, redirects, processing state.

## Key Differences from Nuxt Defaults

| shadcn-vue default (Nuxt) | Inertia equivalent |
|---|---|
| `useFetch` / `useAsyncData` | Server-rendered props via controller |
| `useRouter()` (Nuxt) | `router` from `@inertiajs/vue3` |
| `<NuxtLink>` | `<Link>` from `@inertiajs/vue3` |
| `vee-validate` + `zod` | Inertia `<Form>` component |
| `FormField`, `FormItem`, `FormMessage` | Plain `<Input name="...">` + `errors.field` |
| `useHead()` (Nuxt) | `<Head>` from `@inertiajs/vue3` |

**NEVER use shadcn-vue's `FormField`, `FormItem`, `FormLabel`, `FormMessage` components** —
they depend on vee-validate's form context internally and will crash without it.
Use plain shadcn-vue `Input`/`Label`/`Select` with `name` attributes inside Inertia `<Form>`,
and render errors from the scoped slot's `errors` object.

## Setup

`npx shadcn-vue@latest init`. Add `@/` resolve aliases to `tsconfig.json` if not present.
**Do NOT add `@/` resolve aliases to `vite.config.ts`** — `vite-plugin-ruby` already provides them.

## shadcn-vue Inputs in Inertia `<Form>`

Use plain shadcn-vue `Input`/`Label`/`Button` with `name` attributes inside Inertia `<Form>`.
See `inertia-rails-forms` skill (+ `references/vue.md`) for full `<Form>` API.

**The key pattern:** Replace shadcn-vue's `FormField`/`FormItem`/`FormMessage` with plain
components + manual error display:

```vue
<script setup lang="ts">
import { Form } from '@inertiajs/vue3'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
</script>

<template>
  <Form method="post" action="/users">
    <template #default="{ errors, processing }">
      <div class="space-y-4">
        <div>
          <Label for="name">Name</Label>
          <Input id="name" name="name" />
          <p v-if="errors.name" class="text-sm text-destructive">{{ errors.name }}</p>
        </div>

        <div>
          <Label for="email">Email</Label>
          <Input id="email" name="email" type="email" />
          <p v-if="errors.email" class="text-sm text-destructive">{{ errors.email }}</p>
        </div>

        <Button type="submit" :disabled="processing">
          {{ processing ? 'Creating...' : 'Create User' }}
        </Button>
      </div>
    </template>
  </Form>
</template>
```

**`<Select>` requires `name` prop** for Inertia `<Form>` integration:

```vue
<template>
  <Select name="role" default-value="member">
    <SelectTrigger><SelectValue placeholder="Select role" /></SelectTrigger>
    <SelectContent>
      <SelectItem value="admin">Admin</SelectItem>
      <SelectItem value="member">Member</SelectItem>
    </SelectContent>
  </Select>
</template>
```

## Dialog with Inertia Navigation

```vue
<script setup lang="ts">
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { router } from '@inertiajs/vue3'

defineProps<{ open: boolean; user: User }>()
</script>

<template>
  <Dialog
    :open="open"
    @update:open="(isOpen) => { if (!isOpen) router.replaceProp('show_dialog', false) }"
  >
    <DialogContent>
      <DialogHeader>
        <DialogTitle>{{ user.name }}</DialogTitle>
      </DialogHeader>
      <!-- content -->
    </DialogContent>
  </Dialog>
</template>
```

## Table with Server-Side Sorting

```vue
<script setup lang="ts">
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { router } from '@inertiajs/vue3'

defineProps<{ users: User[]; sort: string }>()

const handleSort = (column: string) => {
  router.get('/users', { sort: column }, { preserveState: true })
}
</script>

<template>
  <Table>
    <TableHeader>
      <TableRow>
        <TableHead class="cursor-pointer" @click="handleSort('name')">
          Name {{ sort === 'name' ? '↑' : '' }}
        </TableHead>
        <TableHead>Email</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow v-for="user in users" :key="user.id">
        <TableCell>{{ user.name }}</TableCell>
        <TableCell>{{ user.email }}</TableCell>
      </TableRow>
    </TableBody>
  </Table>
</template>
```

Use `<Link>` (not `<a>`) for row links to preserve SPA navigation.

## Toast with Flash Messages

Flash config (`flash_keys`) is in `inertia-rails-controllers`. Flash access
(`usePage().flash`) is in `inertia-rails-pages`. This section covers **toast UI wiring only**.

**MANDATORY — READ ENTIRE FILE** when implementing flash-based toasts with Sonner:
[`references/flash-toast.md`](references/flash-toast.md) (~80 lines) — full `useFlash`
composable and Sonner toast provider. **Do NOT load** if only reading flash values without toast UI.

## Dark Mode (No Nuxt color-mode)

`npx shadcn-vue@latest init` generates CSS variables for light/dark and
`@custom-variant dark (&:is(.dark *));` in your CSS (Tailwind v4). No extra
setup needed for the variables themselves.

**CRITICAL — prevent flash of wrong theme (FOUC):** Add an inline script in
`<head>` (before Vue hydrates):

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

Use a `useAppearance` composable (light/dark/system modes, localStorage persistence,
`matchMedia` listener) instead of Nuxt color-mode. Toggle via `.dark` class on
`<html>` — no provider needed.

## Vue-Specific Gotchas

**`v-model` does NOT work with Inertia `<Form>`** — `<Form>` reads values from
input `name` attributes on submit, not from Vue's reactivity system. Using
`v-model` creates a second source of truth that `<Form>` ignores:

```vue
<!-- BAD — v-model value is ignored by <Form> on submit -->
<Form method="post" action="/users">
  <Input v-model="name" />
</Form>

<!-- GOOD — name attribute is what <Form> reads -->
<Form method="post" action="/users">
  <Input name="name" />
</Form>
```

Use `v-model` only with `useForm` (where you explicitly manage `form.name`).

**`usePage()` returns a reactive object — use `computed()` for derived values:**

```vue
<script setup lang="ts">
import { usePage } from '@inertiajs/vue3'
import { computed } from 'vue'

const page = usePage()

// BAD — not reactive, won't update when page changes:
// const user = page.props.auth.user

// GOOD — reactive, updates on navigation:
const user = computed(() => page.props.auth.user)
</script>
```

Without `computed()`, destructured values freeze at their initial state and
won't update after Inertia navigation.

**`@update:open` vs `@close` for Dialog** — shadcn-vue Dialog emits
`update:open`, not `close`. Using `@close` silently does nothing:

```vue
<!-- BAD — @close is not emitted by shadcn-vue Dialog -->
<Dialog @close="handleClose">

<!-- GOOD — @update:open fires on open AND close -->
<Dialog :open="open" @update:open="(isOpen) => { if (!isOpen) handleClose() }">
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `FormField`/`FormMessage` crash | Using shadcn-vue form components that depend on vee-validate | Replace with plain `Input`/`Label` + `errors.field` display |
| `Select` value not submitted | Missing `name` prop | Add `name="field"` to `<Select>` |
| Dialog closes unexpectedly | Missing or wrong `@update:open` handler | Use `@update:open="(open) => { if (!open) closeHandler() }"` |
| Flash of wrong theme (FOUC) | Missing inline `<script>` in `<head>` | Add dark mode script before stylesheets |
| `v-model` value not submitted | `<Form>` reads `name` attrs, not Vue reactive state | Use `name` attribute; reserve `v-model` for `useForm` only |
| Shared props stale after navigation | Destructured `usePage()` without `computed()` | Wrap derived values in `computed(() => ...)` |

## Related Skills
- **Form component** → `inertia-rails-forms` + `references/vue.md` (`<Form>` scoped slot, useForm)
- **Flash config** → `inertia-rails-controllers` (flash_keys initializer)
- **Flash access** → `inertia-rails-pages` + `references/vue.md` (usePage().flash)
- **URL-driven dialogs** → `inertia-rails-pages` + `references/vue.md` (router.get pattern)

## References

Load [`references/components.md`](references/components.md) (~200 lines) when building
shadcn-vue components beyond those shown above (Accordion, Sheet, Tabs, DropdownMenu,
AlertDialog with Inertia patterns).

**Do NOT load** `components.md` for basic Form, Select, Dialog, or Table usage —
the examples above are sufficient.
