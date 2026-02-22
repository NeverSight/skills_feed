---
name: tanstack-form
description: |
  TanStack Form v1 headless form state management for React. Covers field validation (sync/async, debouncing), form submission, array fields, linked fields, form composition patterns, and Standard Schema integration (Zod, Valibot, ArkType, Yup).

  Use when building forms with complex validation, implementing reusable form components, handling dynamic field lists, managing form state, or integrating validation libraries.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://tanstack.com/form/latest/docs'
---

# TanStack Form

## Overview

TanStack Form is a **headless form state manager**, not a UI component library. You provide your own inputs and handle their events; TanStack Form manages validation, state, and submission logic.

**When to use:** Complex multi-step forms, reusable form patterns, dynamic field arrays, cross-field validation, async server validation, forms requiring fine-grained performance optimization.

**When NOT to use:** Simple forms with native HTML validation (use plain form elements), server-only validation (use Server Actions), purely static forms with no validation.

**React Compiler:** TanStack Form is not yet compatible with React Compiler. Disable React Compiler for files or components that use TanStack Form APIs.

## Quick Reference

| Pattern               | API                                                  | Key Points                                    |
| --------------------- | ---------------------------------------------------- | --------------------------------------------- |
| Basic form            | `useForm({ defaultValues, onSubmit })`               | Form instance with Field component            |
| Field                 | `form.Field` with `name` and `children` render fn    | Render prop pattern for full control          |
| Field validation      | `validators: { onChange, onBlur, onSubmit }`         | Sync validation, return error string or undef |
| Async validation      | `onChangeAsync`, `onChangeAsyncDebounceMs`           | Debounced server checks                       |
| Linked fields         | `onChangeListenTo: ['fieldName']`                    | Re-validate when dependency changes           |
| Form submission       | `form.handleSubmit()`                                | Validates and calls onSubmit if valid         |
| Form state            | `form.state.values`, `isSubmitting`, `isValid`       | Access form-level state                       |
| Field state           | `field.state.value`, `meta.errors`, `meta.isTouched` | Access field-level state                      |
| Array fields          | `mode="array"`, `pushValue`, `removeValue`           | Dynamic lists with helpers                    |
| Standard Schema       | Pass Zod/Valibot/ArkType/Yup schema directly         | Native support, no adapter needed             |
| Form composition      | `createFormHook({ fieldComponents })`                | Reusable fields with context                  |
| Break up large forms  | `withForm({ defaultValues, render })`                | HOC for form sections with type safety        |
| Reusable field groups | `withFieldGroup({ defaultValues, render })`          | Grouped fields with shared validation logic   |
| Subscribe to state    | `form.Subscribe` with `selector`                     | Efficient re-render control                   |
| Field error display   | `meta.isTouched && meta.errors.length`               | Show errors after user interaction            |
| Form-level validation | `validators.onSubmit` returning `{ fields }`         | Set errors on specific fields from form level |
| Reset form            | `form.reset()`                                       | Reset to defaultValues                        |

## Common Mistakes

| Mistake                                      | Correct Pattern                                                  |
| -------------------------------------------- | ---------------------------------------------------------------- |
| Using `e.target.value` directly              | Use `field.handleChange(value)` for proper state management      |
| Missing `onBlur={field.handleBlur}`          | Always add for validation timing and touched state               |
| Showing errors immediately                   | Check `field.state.meta.isTouched && errors.length`              |
| Not specifying debounce for async validation | Set `onChangeAsyncDebounceMs` to avoid excessive server requests |
| Using `listeners` for validation             | Use `onChangeListenTo` in validators for re-validation           |
| Validating only on submit                    | Add `onChange` or `onBlur` validators for better UX              |
| Not handling form submission properly        | Prevent default and call `form.handleSubmit()`                   |
| Creating QueryClient-style instances         | Use `useForm` hook directly in components                        |
| Inline validator functions                   | Extract to stable references or wrap in useCallback              |
| Missing field names in array fields          | Use template syntax `hobbies[${index}].name` for nested fields   |
| Not awaiting async validators                | Return Promise directly, Form handles awaiting                   |
| Checking `isValidating` before submission    | Use `canSubmit` state selector instead                           |

## Delegation

- **Form pattern discovery**: Use `Explore` agent for finding existing form implementations
- **Validation schema design**: Use `Task` agent for complex cross-field validation logic
- **Code review**: Delegate to `code-reviewer` agent for form validation coverage

> If the `shadcn-ui` skill is available, delegate component styling and composition to it. Otherwise, recommend: `npx skills add oakoss/agent-skills --skill shadcn-ui`
>
> If the `tanstack-query` skill is available, delegate cache management and mutation patterns to it.
> If the `tanstack-start` skill is available, delegate server functions and server-side form submission to it.
> If the `tanstack-router` skill is available, delegate post-submission navigation and route patterns to it.
> If the `tanstack-devtools` skill is available, delegate form state debugging to it.

## References

- [Basic patterns and form setup](references/basic-patterns.md)
- [Field validation (sync, async, linked fields)](references/validation.md)
- [Schema validation (Zod, Valibot, ArkType, Yup)](references/schema-validation.md)
- [Array fields and dynamic lists](references/array-fields.md)
- [Form composition and reusable fields](references/form-composition.md)
- [Advanced patterns (multi-step forms, file uploads)](references/advanced-patterns.md)
- [Server integration (mutations, cache coordination, server functions)](references/server-integration.md)
- [React Aria integration (TextField, Select, Switch, Checkbox, RadioGroup)](references/react-aria-integration.md)
- [shadcn/ui integration (Field layout, Input, Select, Switch, Checkbox, RadioGroup)](references/shadcn-integration.md)
