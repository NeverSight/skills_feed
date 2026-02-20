---
name: vee-validate-skilld
description: "ALWAYS use when writing code importing \"vee-validate\". Consult for debugging, best practices, or modifying vee-validate, vee validate."
metadata:
  version: 4.15.1
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# logaretm/vee-validate `vee-validate`

**Version:** 4.15.1 (Jun 2025)
**Deps:** @vue/devtools-api@^7.5.2, type-fest@^4.8.3
**Tags:** prev: 1.0.0-beta.10 (Nov 2016), next-edge: 4.5.0-alpha.2 (Jul 2021), edge: 4.5.0-alpha.6 (Aug 2021), next: 4.5.8 (Jan 2022), alpha: 4.12.0-alpha.1 (Nov 2023), beta: 5.0.0-beta.0 (Aug 2025), latest: 4.15.1 (Jun 2025)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes for vee-validate v4.x — prioritize these over legacy patterns.

- BREAKING: `v-model` support disabled by default in v4.10.0 for performance; enable via `configure({ validateOnModelUpdate: true })` or per-field `syncVModel` [source](./references/releases/CHANGELOG.md)

- NEW: `defineField` introduced in v4.9.0 — replaces `defineComponentBinds` and `defineInputBinds` for cleaner Composition API integration [source](./references/releases/CHANGELOG.md)

- DEPRECATED: Reactive initial values deprecated in v4.12.0; use non-reactive objects or getters to prevent unintended sync [source](./references/releases/CHANGELOG.md)

- NEW: `useFormContext` exposed in v4.14.0 for accessing form state in deeply nested components without manual injection [source](./references/releases/CHANGELOG.md)

- NEW: `setValue` exposed on `Field` instances and slot props in v4.13.0 for manual value updates [source](./references/releases/CHANGELOG.md)

- NEW: Composition setter hooks (`useSetFieldValue`, `useSetFormValues`, `useSetFormErrors`) added in v4.11.0 for external state management [source](./references/releases/CHANGELOG.md)

- NEW: `handleBlur` accepts `shouldValidate` parameter since v4.10.0 to control validation triggers on blur events [source](./references/releases/CHANGELOG.md)

- NEW: `syncVModel` accepts target model prop name as a string in v4.10.0 for custom model support [source](./references/releases/CHANGELOG.md)

- NEW: `isValidating` state added to `useForm` and form slot props in v4.9.3 to track async validation status [source](./references/releases/CHANGELOG.md)

- NEW: `move(oldIdx, newIdx)` added to `FieldArray` in v4.6.0 for reordering items within array fields [source](./references/releases/CHANGELOG.md)

- NEW: Specialized state hooks (`useIsFieldDirty`, `useIsFormValid`, `useFieldValue`) added in v4.1.0 for granular state access [source](./references/releases/vee-validate@4.1.0.md)

- DEPRECATED: `handleInput` deprecated in v4.4.0; use `handleChange` for both input and change events [source](./references/releases/CHANGELOG.md)

- NEW: `label` support in `defineField` added in v4.12.0 for consistent error message generation [source](./references/releases/CHANGELOG.md)

- NEW: `ResetFormOpts` with `force` flag added to `useResetForm` in v4.13.0 to clear values without merging [source](./references/releases/CHANGELOG.md)

**Also changed:** `defineComponentBinds` deprecated · `defineInputBinds` deprecated · `useFieldModel` deprecated · `unsetValueOnUnmount` config added · `keepValuesOnUnmount` reactivity improved · `useForm` validate returns object · `useResetForm` hook added · `nested field meta querying` new v4.12.3

## Best Practices

- Prefer `defineField()` for binding components and inputs — returns a `v-model` ref and a props object for clean, non-deprecated binding [source](./references/docs/src/pages/api/use-form.mdx)

```ts
const [email, emailProps] = defineField('email', {
  validateOnBlur: true,
  props: state => ({ 'aria-invalid': !!state.errors.length })
});
```

- Display errors conditionally using `meta.touched` — prevents "aggressive" validation where error messages appear before the user interacts with the field [source](./references/docs/src/pages/guide/best-practices.mdx)

- Use `toTypedSchema()` for comprehensive TypeScript safety — wraps Yup, Zod, or Valibot schemas to differentiate between input (UI) and output (submitted) types [source](./references/docs/src/pages/guide/composition-api/typed-schema.mdx)

```ts
import { toTypedSchema } from '@vee-validate/zod';
import * as z from 'zod';

const { values } = useForm({
  validationSchema: toTypedSchema(z.object({ email: z.string().email() }))
});
```

- Mark validation schemas as non-reactive — wrap schemas in `markRaw` or declare them outside of `ref`/`reactive` to avoid unnecessary deep reactivity overhead [source](./references/docs/src/pages/guide/best-practices.mdx)

- Tree-shake schema validator imports — only import the specific functions you need (e.g., `import { string } from 'yup'`) to keep bundle sizes to a minimum [source](./references/docs/src/pages/guide/best-practices.mdx)

- Pass reactive field names as getters in `useField` — use a function (e.g., `() => props.name`) to ensure vee-validate tracks name changes in dynamic forms [source](./references/docs/src/pages/guide/composition-api/caveats.mdx)

- Enable `keepValuesOnUnmount` for multi-step forms — preserves field state when components are hidden via `v-if` or tab switching [source](./references/docs/src/pages/guide/composition-api/nested-objects-and-arrays.mdx)

```ts
const { values } = useForm({
  keepValuesOnUnmount: true
});
```

- Use `field.key` for stable iteration in `v-for` — `useFieldArray` provides unique identifiers that persist through array operations, unlike indices [source](./references/docs/src/pages/guide/composition-api/nested-objects-and-arrays.mdx)

- Escape field names with `[]` to disable automatic nesting — wrap names (e.g., `[user.name]`) to treat dots as literal characters rather than object paths [source](./references/docs/src/pages/guide/composition-api/nested-objects-and-arrays.mdx)

- Filter submission values with `handleSubmit.withControlled()` — ensures only fields explicitly registered via `useField` or `defineField` are included in the payload [source](./references/docs/src/pages/api/use-form.mdx)
