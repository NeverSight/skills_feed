---
name: inertia-rails-forms
description: >-
  Full-stack form handling for Inertia Rails: create, edit, delete, multi-step wizard, and file upload
  forms with validation errors and progress tracking. React examples inline; Vue and Svelte equivalents
  in references. Use when building any form, handling file uploads, multi-step forms, client-side validation,
  or wiring form submission to Rails controllers. NEVER react-hook-form. Use `<Form>` for simple forms,
  useForm for dynamic/programmatic control.
---

# Inertia Rails Forms

Full-stack form handling for Inertia.js + Rails.

**Before building a form, ask:**
- **Simple create/edit?** → `<Form>` component (no state management needed)
- **Requires per-field UI elements?** → Still `<Form>`.
  React `useState` for UI state (preview URL, file size display) is independent
  of form data — `<Form>` handles the submission; `useState` handles the UI.
- **Multi-step wizard, dynamic fields (add/remove inputs), or form data
  shared with sibling components (e.g., live preview panel)?** → `useForm` hook
- **Tempted by react-hook-form?** → Don't. Inertia's `<Form>` already handles CSRF
  tokens, redirect following, error mapping from Rails, processing state, file upload
  detection, and history state. react-hook-form would duplicate or fight all of this.

**When NOT to use `<Form>` or `useForm`:**
- **Data lookups** — not a form submission. Use `router.get` with debounce + `preserveState`, or raw `fetch` for **large datasets**
- **Inline single-field edits without navigation** – `router.patch` directly, or `useForm` if you need error display on the field

**NEVER:**
- Use `react-hook-form`, `vee-validate`, or `sveltekit-superforms` — Inertia `<Form>` already handles CSRF, redirect following, error mapping, processing state, and file detection. These libraries fight Inertia's request lifecycle.
- Pass `data={...}` to `<Form>` — it has no `data` prop. Data comes from input `name` attributes automatically. `data` is a `useForm` concept.
- Use `useForm` for simple create/edit — `<Form>` handles these without state management. Reserve `useForm` for multi-step wizards, dynamic add/remove fields, or form data shared with sibling components.
- Use controlled `value=` instead of `defaultValue` on inputs — controlled inputs bypass `<Form>`'s dirty tracking, making `isDirty` always `false`.
- Omit `value="1"` on checkboxes — without it, the browser submits `"on"` and Rails won't cast to boolean correctly.
- Call `useForm` inside a loop or conditional — it's a hook (React rules apply). Create one form instance per logical form.

## `<Form>` Component (Preferred)

The simplest way to handle forms. Collects data from input `name` attributes
automatically — no manual state management needed. `<Form>` has NO `data` prop —
do NOT pass `data={...}` (that's a `useForm` concept). For edit forms, use
`defaultValue` on inputs.

**Use render function children** `{({ errors, processing }) => (...)}` to
access form state. Plain children work but give no access to errors,
processing, or progress.

```tsx
import { Form } from '@inertiajs/react'

export default function CreateUser() {
  return (
    <Form method="post" action="/users">
      {({ errors, processing }) => (
        <>
          <input type="text" name="name" />
          {errors.name && <span className="error">{errors.name}</span>}

          <input type="email" name="email" />
          {errors.email && <span className="error">{errors.email}</span>}

          <button type="submit" disabled={processing}>
            {processing ? 'Creating...' : 'Create User'}
          </button>
        </>
      )}
    </Form>
  )
}

// Plain children — valid but no access to errors/processing/progress:
// <Form method="post" action="/users">
//   <input name="name" />
//   <button type="submit">Create</button>
// </Form>
```

### Delete Form

```tsx
<Form method="delete" action={`/posts/${post.id}`}>
  {({ processing }) => (
    <button type="submit" disabled={processing}>
      {processing ? 'Deleting...' : 'Delete Post'}
    </button>
  )}
</Form>
```

### Key Render Function Properties

| Property | Type | Purpose |
|----------|------|---------|
| `errors` | `Record<string, string>` | Validation errors keyed by field name |
| `processing` | `boolean` | True while request is in flight |
| `progress` | `{ percentage: number } \| null` | Upload progress (file uploads only) |
| `hasErrors` | `boolean` | True if any errors exist |
| `wasSuccessful` | `boolean` | True after last submit succeeded |
| `recentlySuccessful` | `boolean` | True for 2s after success — ideal for "Saved!" feedback |
| `isDirty` | `boolean` | True if any input changed from initial value |
| `reset` | `(...fields) => void` | Reset specific fields or all fields |
| `clearErrors` | `(...fields) => void` | Clear specific errors or all errors |

Additional `<Form>` props (`errorBag`, `only`, `resetOnSuccess`,
event callbacks like `onBefore`, `onSuccess`, `onError`, `onProgress`) are
documented in `references/advanced-forms.md` — see loading trigger below.

### Edit Form (Pre-populated)

Use `method="patch"` and uncontrolled defaults:
- Text/textarea → `defaultValue`
- Checkbox/radio → `defaultChecked`
- Select → `defaultValue` on `<select>`

> Checkbox without explicit `value` submits `"on"` — set `value="1"` so Rails
> casts to boolean correctly.

```tsx
<Form method="patch" action={`/posts/${post.id}`}>
  {({ errors, processing }) => (
    <>
      <input type="text" name="title" defaultValue={post.title} />
      {errors.title && <span className="error">{errors.title}</span>}

      <label>
        <input type="checkbox" name="published" value="1"
          defaultChecked={post.published} />
        Published
      </label>

      <button type="submit" disabled={processing}>
        {processing ? 'Saving...' : 'Update Post'}
      </button>
    </>
  )}
</Form>
```

### Transforming Data

Use the `transform` prop to reshape data before submission without `useForm`.

For advanced `transform` with `useForm`, see `references/advanced-forms.md`.

### External Access with `formRef`

The ref exposes the same methods and state as render function props (`FormComponentSlotProps`).
Use when you need to interact with the form from outside `<Form>`.
Key ref methods: `submit()`, `reset()`, `clearErrors()`, `setError()`,
`getData()`, `getFormData()`, `validate()`, `touch()`, `defaults()`.
State: `errors`, `processing`, `progress`, `isDirty`, `hasErrors`,
`wasSuccessful`, `recentlySuccessful`.

```tsx
import {useRef} from 'react'
import {Form} from '@inertiajs/react'
import type {FormComponentRef} from '@inertiajs/core'

export default function CreateUser() {
  const formRef = useRef<FormComponentRef>(null)

  return (
    <>
      <Form ref={formRef} method='post' action='/users'>
        {({errors}) => (
          <>
            <input type='text' name='name'/>
            {errors.name && <span className='error'>{errors.name}</span>}
          </>
        )}
      </Form>
      <button onClick={() => formRef.current?.submit()}>Submit</button>
      <button onClick={() => formRef.current?.reset()}>Reset</button>
    </>
  )
}
```

## `useForm` Hook

Use `useForm` only for multi-step wizards, dynamic add/remove fields, or
form data shared with sibling components.

**MANDATORY — READ ENTIRE FILE** when using `useForm` hook, `transform`,
`errorBag`, `resetOnSuccess`, multi-step forms, or client-side validation
with `setError`:
[`references/advanced-forms.md`](references/advanced-forms.md) (~330 lines) — full
`useForm` API, transform examples, error bag scoping, multi-step wizard
patterns, and client-side validation.

**Do NOT load** `advanced-forms.md` when using `<Form>` component for simple
create/edit forms — the examples above are sufficient.

## File Uploads

Both `<Form>` and `useForm` auto-detect files and switch to `FormData`.
Upload progress is built into the render function — destructure `progress`
alongside `errors` and `processing`:

```tsx
type Props = { user: User }

export default function EditProfile({ user }: Props) {
  return (
    <Form method="patch" action="/profile">
      {({ errors, processing, progress }) => (
        <>
          <input type="text" name="name" defaultValue={user.name} />
          {errors.name && <span className="error">{errors.name}</span>}

          <input type="file" name="avatar" />
          {errors.avatar && <span className="error">{errors.avatar}</span>}

          {progress && (
            <progress value={progress.percentage ?? 0} max="100" />
          )}

          <button type="submit" disabled={processing}>
            {processing ? 'Uploading...' : 'Save'}
          </button>
        </>
      )}
    </Form>
  )
}
```

**Choosing `<Form>` vs `useForm` for uploads:**
- **File submits with other fields** (avatar + name, one Save button) → file input inside `<Form>`
- **Standalone immediate upload** (uploads on select, no Save button) → `<Form>` + `formRef.submit()` on change
- **Drag-and-drop upload** → `useForm` (dropped files aren't in DOM inputs, `setData` is cleaner)

Preview / validation → `useState` alongside either approach, see
[`references/file-uploads.md`](references/file-uploads.md).

## Vue / Svelte

All examples above use React syntax. For Vue 3 or Svelte equivalents:

- **Vue 3**: [`references/vue.md`](references/vue.md) — `<Form>` with `#default` scoped slot, `useForm` returns reactive proxy (`form.email` not `setData`), `v-model` binding
- **Svelte**: [`references/svelte.md`](references/svelte.md) — `<Form>` with `{#snippet}` syntax, `useForm` returns Writable store (`$form.email`), `bind:value`, ref exposes methods only (not reactive state)

**MANDATORY — READ THE MATCHING FILE** when the project uses Vue or Svelte.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| No access to `errors`/`processing` | Plain children instead of render function | `<Form>` children should be `{({ errors, processing }) => (...)}` |
| Form sends GET instead of POST | Missing `method` prop | Add `method="post"` (or `"patch"`, `"delete"`) |
| File upload sends empty body | PUT/PATCH with file | Multipart limitation — Inertia auto-adds `_method` field to convert to POST |
| Errors don't clear after fixing field | Stale error state | Errors auto-clear on next submit; use `clearErrors('field')` for immediate clearing |
| `isDirty` always false | Using `value` instead of `defaultValue` | Controlled inputs (`value=`) bypass dirty tracking — use `defaultValue` |
| `progress` is always `null` | No file input in form | Progress tracking only activates when `<Form>` detects a file input |
| Checkbox sends `"on"` | No explicit `value` | Add `value="1"` to checkbox inputs |
| Form submits twice in dev | React StrictMode double-invocation | Normal in development — StrictMode remounts components. Only fires once in production |
| Used `useForm` for file upload with preview | `onChange` + `useState` mistaken for "programmatic data manipulation" | `<Form>` + `useState` for preview UI. `useForm` is only needed when form *submission data* must live in React state (multi-step, dynamic add/remove fields). File preview is local UI state, not form data |

## Related Skills
- **Server-side PRG & errors** → `inertia-rails-controllers` (redirect_back, to_hash, flash)
- **shadcn inputs** → `shadcn-inertia` (Input/Select adaptation, toast UI)
- **Page props typing** → `inertia-rails-typescript` (`type Props` not `interface`, TS2344)

**MANDATORY — READ ENTIRE FILE** when handling file uploads with image preview,
Active Storage, or direct uploads:
[`references/file-uploads.md`](references/file-uploads.md) (~200 lines) — image preview
with `<Form>`, Active Storage integration, direct upload setup, multiple files,
and progress tracking.
