---
name: tanstack-vue-form-skilld
description: "ALWAYS use when writing code importing \"@tanstack/vue-form\". Consult for debugging, best practices, or modifying @tanstack/vue-form, tanstack/vue-form, tanstack vue-form, tanstack vue form, form."
metadata:
  version: 1.28.3
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# TanStack/form `@tanstack/vue-form`

**Version:** 1.28.3 (Feb 2026)
**Deps:** @tanstack/vue-store@^0.8.1, @tanstack/form-core@1.28.3
**Tags:** latest: 1.28.3 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes for `@tanstack/vue-form`.

- BREAKING: `field.errors` — v1.28.0 flattens errors by default (`[error]` not `[[error]]`), use `disableErrorFlat: true` to restore old nested behavior [source](./references/releases/@tanstack/vue-form@1.28.0.md)

- DEPRECATED: `field.getValue()` — use `field.state.value` instead as direct accessor methods on FieldApi are deprecated in favor of state access [source](./references/docs/reference/classes/FieldApi.md)

- NEW: `field.parseValueWithSchema()` — validates field value against Standard Schema V1 without affecting internal field error state [source](./references/docs/reference/classes/FieldApi.md)

- NEW: `form.parseValuesWithSchema()` — form-level Standard Schema V1 validation helper for third-party schemas like Zod or Valibot [source](./references/docs/reference/classes/FormApi.md)

- NEW: `formOptions()` — helper to define reusable, type-safe form options with inference outside of the `useForm` hook [source](./references/docs/reference/functions/formOptions.md)

- NEW: `Field` component — declarative Vue component alternative to `useField` for defining form fields directly in templates [source](./references/docs/framework/vue/reference/variables/Field.md)

- NEW: `Subscribe` component — Vue component for fine-grained subscriptions to form or field state changes to optimize re-renders [source](./references/docs/framework/vue/reference/interfaces/VueFormApi.md)

- NEW: `useStore()` — Vue hook providing direct, reactive access to the underlying TanStack Store state for the form or field [source](./references/docs/framework/vue/reference/functions/useStore.md)

- NEW: `resetField()` — `FormApi` method to reset a specific field's value and metadata back to its default state [source](./references/docs/reference/classes/FormApi.md)

- NEW: `clearFieldValues()` — `FormApi` utility to efficiently remove all items from an array field's data [source](./references/docs/reference/classes/FormApi.md)

- NEW: `setErrorMap()` — allows manual overriding of the internal validation error map for custom validation logic [source](./references/docs/reference/classes/FieldApi.md)

- NEW: `StandardSchemaV1` — native support for the Standard Schema validation protocol across all validator fields [source](./references/docs/reference/type-aliases/StandardSchemaV1.md)

- NEW: `mode` option — `UseFieldOptions` now supports explicit `'value'` or `'array'` modes for better type safety in complex forms

- NEW: `disableErrorFlat` — new option in `FieldApiOptions` to opt-out of automatic error flattening introduced in v1.28.0 [source](./references/releases/@tanstack/vue-form@1.28.0.md)

**Also changed:** `resetFieldMeta()` new helper · `insertFieldValue()` array utility · `moveFieldValues()` array utility · `swapFieldValues()` array utility · `FieldApi.getInfo()` metadata helper · `VueFieldApi` interface stabilization · `VueFormApi` interface stabilization

## Best Practices

- Use `formOptions()` to define type-safe, reusable form configurations that can be shared across components or used for better type inference [source](./references/docs/reference/functions/formOptions.md)

```ts
const options = formOptions({
  defaultValues: { email: '' },
  validators: {
    onChange: z.object({ email: z.string().email() })
  }
})

const form = useForm(options)
```

- Link field validations with `onChangeListenTo` to trigger re-validation when dependent field values change, such as password confirmations [source](./references/docs/framework/vue/guides/linked-fields.md)

```vue
<form.Field
  name="confirm_password"
  :validators="{
    onChangeListenTo: ['password'],
    onChange: ({ value, fieldApi }) =>
      value !== fieldApi.form.getFieldValue('password') ? 'Passwords do not match' : undefined
  }"
>
```

- Implement `async-debounce-ms` at the field or validator level to throttle expensive asynchronous validation calls like API checks [source](./references/docs/framework/vue/guides/validation.md)

```vue
<form.Field
  name="username"
  :async-debounce-ms="500"
  :validators="{
    onChangeAsync: async ({ value }) => checkUsername(value)
  }"
>
```

- Parse Standard Schemas manually within `onSubmit` to retrieve transformed values, as the form state preserves the raw input data [source](./references/docs/framework/vue/guides/submission-handling.md)

```ts
const form = useForm({
  onSubmit: ({ value }) => {
    // schema.parse converts string to number if transform is defined
    const validatedData = loginSchema.parse(value)
    api.submit(validatedData)
  }
})
```

- Pass custom metadata via `onSubmitMeta` to differentiate between multiple submission actions within a single `onSubmit` handler [source](./references/docs/framework/vue/guides/submission-handling.md)

```vue
<button @click="form.handleSubmit({ action: 'save_draft' })">Save Draft</button>
<button @click="form.handleSubmit({ action: 'publish' })">Publish</button>
```

- Combine `canSubmit` with `isPristine` to ensure the submit button remains disabled until the user has actually interacted with the form [source](./references/docs/framework/vue/guides/validation.md)

```vue
<template v-slot="{ canSubmit, isPristine }">
  <button :disabled="!canSubmit || isPristine">Submit</button>
</template>
```

- Use `form.useStore` with a selector in `<script setup>` for granular, reactive access to form state without re-rendering on unrelated changes [source](./references/docs/framework/vue/guides/validation.md)

```ts
const canSubmit = form.useStore((state) => state.canSubmit)
```

- Enable `asyncAlways: true` when you need asynchronous validators to execute regardless of whether synchronous validation has already failed [source](./references/docs/framework/vue/guides/validation.md)

```ts
// Runs async validation even if local regex check fails
const validators = {
  onChange: ({ value }) => !value.includes('@') ? 'Invalid' : undefined,
  onChangeAsync: async ({ value }) => api.check(value),
  asyncAlways: true
}
```

- Return a `fields` mapping from form-level validators to update errors across multiple fields simultaneously from a single validation logic [source](./references/docs/framework/vue/guides/validation.md)

```ts
validators: {
  onChange: ({ value }) => ({
    fields: {
      startDate: value.startDate > value.endDate ? 'Must be before end' : undefined,
      endDate: value.startDate > value.endDate ? 'Must be after start' : undefined
    }
  })
}
```

- Use reactive objects for `defaultValues` when binding the form to dynamic or asynchronous data sources like TanStack Query [source](./references/docs/framework/vue/guides/async-initial-values.md)

```ts
const { data } = useQuery(...)
const defaultValues = reactive({
  name: computed(() => data.value?.name ?? '')
})
const form = useForm({ defaultValues })
```
