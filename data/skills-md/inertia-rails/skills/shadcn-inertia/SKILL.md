---
name: shadcn-inertia
description: >-
  shadcn/ui component integration for Inertia Rails React (NOT Next.js): forms, dialogs, tables, toasts, dark mode,
  command palette, and more. Use when building UI with shadcn/ui components in an Inertia app or adapting shadcn
  examples from Next.js. NEVER react-hook-form/zod — wire shadcn inputs to Inertia Form via name attribute. Flash
  toasts require Rails flash_keys initializer config.
---

# shadcn/ui for Inertia Rails

shadcn/ui patterns adapted for Inertia.js + Rails + React. NOT Next.js.

**Before using a shadcn example, ask:**
- **Does it use `react-hook-form` + `zod`?** → Replace with Inertia `<Form>` + `name` attributes. Inertia handles CSRF, errors, redirects, processing state — react-hook-form would fight all of this.
- **Does it use `'use client'`?** → Remove it. Inertia has no RSC — all components are client components.
- **Does it use `next/link`, `next/head`, `useRouter()`?** → Replace with Inertia `<Link>`, `<Head>`, `router`.

## Key Differences from Next.js Defaults

| shadcn default (Next.js) | Inertia equivalent |
|---|---|
| `'use client'` directive | Remove — not needed (no RSC) |
| `react-hook-form` + `zod` | Inertia `<Form>` component |
| `FormField`, `FormItem`, `FormMessage` | Plain `<Input name="...">` + `errors.field` |
| `next-themes` | CSS class strategy + `@custom-variant` |
| `useRouter()` (Next) | `router` from `@inertiajs/react` |
| `next/link` | `<Link>` from `@inertiajs/react` |
| `next/head` | `<Head>` from `@inertiajs/react` |

**NEVER use shadcn's `FormField`, `FormItem`, `FormLabel`, `FormMessage` components** —
they depend on react-hook-form's `useFormContext` internally and will crash without it.
Use plain shadcn `Input`/`Label`/`Select` with `name` attributes inside Inertia `<Form>`,
and render errors from the render function's `errors` object (see examples below).

## Setup

`npx shadcn@latest init`. add `@/` resolve aliases to `tsconfig.json` if not present,
**Do NOT add `@/` resolve aliases to `vite.config.ts`** — `vite-plugin-ruby` already provides them.

## shadcn Inputs in Inertia `<Form>`

Use plain shadcn `Input`/`Label`/`Button` with `name` attributes inside Inertia `<Form>`.
See `inertia-rails-forms` skill for full `<Form>` API — this section covers shadcn-specific adaptation only.

**The key pattern:** Replace shadcn's `FormField`/`FormItem`/`FormMessage` with plain
components + manual error display:

```tsx
// shadcn error display pattern (replaces FormMessage):
<Label htmlFor="name">Name</Label>
<Input id="name" name="name" />
{errors.name && <p className="text-sm text-destructive">{errors.name}</p>}
```

**`<Select>` requires `name` prop** for Inertia `<Form>` integration — shadcn examples
omit it because react-hook-form manages values differently:

```tsx
<Select name="role" defaultValue="member">
  <SelectTrigger><SelectValue placeholder="Select role" /></SelectTrigger>
  <SelectContent>
    <SelectItem value="admin">Admin</SelectItem>
    <SelectItem value="member">Member</SelectItem>
  </SelectContent>
</Select>
```

## Dialog with Inertia Navigation

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { router } from '@inertiajs/react'

function UserDialog({ open, user }: { open: boolean; user: User }) {
  return (
    <Dialog
      open={open}
      onOpenChange={(isOpen) => {
        if (!isOpen) {
          router.replaceProp('show_dialog', false)
        }
      }}
    >
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{user.name}</DialogTitle>
        </DialogHeader>
        {/* content */}
      </DialogContent>
    </Dialog>
  )
}
```

## Table with Server-Side Sorting

shadcn `<Table>` renders normally. The Inertia-specific part is sorting via `router.get`:

```tsx
const handleSort = (column: string) => {
  router.get('/users', { sort: column }, { preserveState: true })
}

<TableHead onClick={() => handleSort('name')} className="cursor-pointer">
  Name {sort === 'name' && '↑'}
</TableHead>
```

Use `<Link>` (not `<a>`) for row links to preserve SPA navigation.

## Toast with Flash Messages

Flash config (`flash_keys`) is in `inertia-rails-controllers`. Flash access
(`usePage().flash`) is in `inertia-rails-pages`. This section covers **toast UI wiring only**.

**MANDATORY — READ ENTIRE FILE** when implementing flash-based toasts with Sonner:
[`references/flash-toast.md`](references/flash-toast.md) (~80 lines) — full `useFlash`
hook and Sonner toast provider. **Do NOT load** if only reading flash values without toast UI.

Key gotcha: `flash_keys` in the Rails initializer MUST match your `FlashData`
TypeScript type — do NOT use `success`/`error` unless you also update both.

## Dark Mode (No next-themes)

`npx shadcn@latest init` generates CSS variables for light/dark and
`@custom-variant dark (&:is(.dark *));` in your CSS (Tailwind v4). No extra
setup needed for the variables themselves.

**CRITICAL — prevent flash of wrong theme (FOUC):** Next.js handles this
automatically; Inertia does NOT. Add an inline script in `<head>` (before React
hydrates) and call `initializeTheme()` in your Inertia entrypoint:

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

```tsx
// app/frontend/entrypoints/inertia.tsx
import { initializeTheme } from '@/hooks/use-appearance'
initializeTheme() // must run before createInertiaApp
```

Use a `useAppearance` hook (light/dark/system modes, localStorage persistence,
`matchMedia` listener) instead of `next-themes`. Toggle via `.dark` class on
`<html>` — no provider needed.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `FormField`/`FormMessage` crash | Using shadcn form components that depend on react-hook-form | Replace with plain `Input`/`Label` + `errors.field` display |
| `Select` value not submitted | Missing `name` prop | Add `name="field"` to `<Select>` — shadcn examples omit it |
| Dialog closes unexpectedly | Missing or wrong `onOpenChange` handler | Use `onOpenChange={(open) => { if (!open) closeHandler() }}` |
| Flash of wrong theme (FOUC) | Missing inline `<script>` in `<head>` | Add dark mode script before stylesheets (see Dark Mode section) |

## Related Skills
- **Form component** → `inertia-rails-forms` (`<Form>` render function, useForm)
- **Flash config** → `inertia-rails-controllers` (flash_keys initializer)
- **Flash access** → `inertia-rails-pages` (usePage().flash)
- **URL-driven dialogs** → `inertia-rails-pages` (router.get pattern)

## References

Load [`references/components.md`](references/components.md) (~300 lines) when building
shadcn components beyond those shown above (Accordion, Sheet, Tabs, DropdownMenu,
AlertDialog with Inertia patterns).

**Do NOT load** `components.md` for basic Form, Select, Dialog, or Table usage —
the examples above are sufficient.
