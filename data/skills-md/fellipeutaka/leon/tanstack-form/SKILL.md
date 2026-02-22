---
name: tanstack-form
description: |
  TanStack Form best practices for type-safe form management, validation, field composition, and submission handling in React.
  Use when building forms with complex validation, integrating schema libraries (Zod/Valibot/ArkType), composing reusable form components,
  managing array/dynamic fields, or integrating with meta-frameworks (TanStack Start, Next.js, Remix).
metadata:
  tags: tanstack-form, forms, react, typescript, validation, zod, form-composition, headless-ui
---

# TanStack Form

**Version**: @tanstack/react-form@latest
**Requires**: React 18.0+, TypeScript 5.0+

## Quick Setup

```bash
npm install @tanstack/react-form
```

```tsx
import { useForm } from '@tanstack/react-form'

function App() {
  const form = useForm({
    defaultValues: {
      firstName: '',
      lastName: '',
    },
    onSubmit: async ({ value }) => {
      console.log(value)
    },
  })

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        e.stopPropagation()
        form.handleSubmit()
      }}
    >
      <form.Field
        name="firstName"
        validators={{
          onChange: ({ value }) =>
            !value ? 'Required' : value.length < 3 ? 'Too short' : undefined,
        }}
        children={(field) => (
          <>
            <input
              value={field.state.value}
              onBlur={field.handleBlur}
              onChange={(e) => field.handleChange(e.target.value)}
            />
            {!field.state.meta.isValid && (
              <em>{field.state.meta.errors.join(', ')}</em>
            )}
          </>
        )}
      />
      <form.Subscribe
        selector={(state) => [state.canSubmit, state.isSubmitting]}
        children={([canSubmit, isSubmitting]) => (
          <button type="submit" disabled={!canSubmit}>
            {isSubmitting ? '...' : 'Submit'}
          </button>
        )}
      />
    </form>
  )
}
```

### Production Setup (Recommended)

For production apps, use `createFormHook` to pre-bind reusable UI components and reduce boilerplate:

```tsx
import { createFormHookContexts, createFormHook } from '@tanstack/react-form'
import { TextField, NumberField, SubmitButton } from '~/ui-library'

const { fieldContext, formContext } = createFormHookContexts()

export const { useAppForm } = createFormHook({
  fieldComponents: { TextField, NumberField },
  formComponents: { SubmitButton },
  fieldContext,
  formContext,
})
```

### Devtools

```bash
npm install -D @tanstack/react-devtools @tanstack/react-form-devtools
```

```tsx
import { TanStackDevtools } from '@tanstack/react-devtools'
import { formDevtoolsPlugin } from '@tanstack/react-form-devtools'

<TanStackDevtools
  config={{ hideUntilHover: true }}
  plugins={[formDevtoolsPlugin()]}
/>
```

## Rule Categories

| Priority | Category | Rule File | Impact |
|----------|----------|-----------|--------|
| CRITICAL | Form Setup | `rules/form-setup.md` | Correct form creation and type inference |
| CRITICAL | Validation | `rules/val-validation.md` | Prevents invalid submissions and poor UX |
| CRITICAL | Schema Validation | `rules/val-schema-validation.md` | Type-safe validation with Zod/Valibot/ArkType |
| HIGH | Form Composition | `rules/comp-form-composition.md` | Reduces boilerplate, enables reusable components |
| HIGH | Field State | `rules/field-state.md` | Correct state access and reactivity |
| HIGH | Array Fields | `rules/arr-array-fields.md` | Dynamic list management |
| HIGH | Linked Fields | `rules/link-linked-fields.md` | Cross-field validation (e.g. confirm password) |
| MEDIUM | Listeners | `rules/listen-listeners.md` | Side effects on field events |
| MEDIUM | Submission | `rules/sub-submission.md` | Correct submit handling and meta passing |
| MEDIUM | SSR / Meta-Frameworks | `rules/ssr-meta-frameworks.md` | Server validation with Start/Next.js/Remix |
| LOW | UI Libraries | `rules/ui-libraries.md` | Headless integration with component libraries |

## Critical Rules

### Always Do

- **Type from defaultValues** — never pass generics to `useForm<T>()`, let TS infer from `defaultValues`
- **Prevent default on submit** — `e.preventDefault(); e.stopPropagation(); form.handleSubmit()`
- **Use `children` render prop** — `form.Field` uses render props via `children={(field) => ...}`
- **Use `form.Subscribe` with selector** — subscribe to specific state slices to avoid re-renders
- **Use `useStore` with selector** — `useStore(form.store, (s) => s.values.name)` not `useStore(form.store)`
- **Use `createFormHook`** in production — pre-bind components for consistency and less boilerplate
- **Debounce async validators** — set `onChangeAsyncDebounceMs` or `asyncDebounceMs`

### Never Do

- **Pass generics** — `useForm<MyType>()` breaks the design; use typed `defaultValues` instead
- **Skip `e.preventDefault()`** — native form submission will bypass TanStack Form's handling
- **Use `useField` for reactivity** — use `useStore(form.store)` or `form.Subscribe` instead
- **Omit selector in `useStore`** — causes full re-render on every state change
- **Use `type="reset"` without `e.preventDefault()`** — native reset bypasses TanStack Form; use `form.reset()` explicitly
- **Expect transformed values in `onSubmit`** — Standard Schema transforms aren't applied; parse manually in `onSubmit`

## Key Patterns

```tsx
// Schema validation (form-level with Zod)
const form = useForm({
  defaultValues: { age: 0, name: '' },
  validators: {
    onChange: z.object({ age: z.number().min(13), name: z.string().min(1) }),
  },
  onSubmit: ({ value }) => console.log(value),
})

// Array fields
<form.Field name="hobbies" mode="array" children={(field) => (
  <div>
    {field.state.value.map((_, i) => (
      <form.Field key={i} name={`hobbies[${i}].name`} children={(sub) => (
        <input value={sub.state.value} onChange={(e) => sub.handleChange(e.target.value)} />
      )} />
    ))}
    <button type="button" onClick={() => field.pushValue({ name: '' })}>Add</button>
  </div>
)} />

// Linked fields (confirm password)
<form.Field name="confirm_password" validators={{
  onChangeListenTo: ['password'],
  onChange: ({ value, fieldApi }) =>
    value !== fieldApi.form.getFieldValue('password') ? 'Passwords do not match' : undefined,
}} children={(field) => <input value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />} />

// Listeners (reset province when country changes)
<form.Field name="country" listeners={{
  onChange: ({ value }) => { form.setFieldValue('province', '') },
}} children={(field) => <input value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />} />

// Form composition with withForm
const ChildForm = withForm({
  defaultValues: { firstName: '', lastName: '' },
  render: function Render({ form }) {
    return <form.AppField name="firstName" children={(field) => <field.TextField label="First Name" />} />
  },
})
```
