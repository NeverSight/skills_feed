---
name: vani-forms-inputs
description: Handle forms and inputs with explicit updates and focus safety
---

# Forms and Inputs

Instructions for building forms that update on submit or preserve focus during controlled input.

## When to Use

Use this when you need form handling, text inputs, or focus-safe controlled inputs.

## Steps

1. Keep input values in local variables and avoid re-rendering on every keystroke.
2. On submit, update local state and call `handle.update()`.
3. For controlled inputs, store a `DomRef`, call `handle.updateSync()`, then restore
   focus/selection.
4. Prefer splitting inputs into their own components if a sibling preview must update live.

## Arguments

- submitOn - submit trigger (`submit` or `blur`, defaults to `submit`)
- useControlledInput - whether to demonstrate controlled input handling (defaults to `false`)
- formName - component name (defaults to `Form`)

## Examples

Example 1 usage pattern:

Create a contact form that updates the UI only after submit.

Example 2 usage pattern:

Implement a controlled input that preserves focus with a `DomRef`.

## Output

Example output:

```
Created: src/contact-form.ts
Notes: Inputs are uncontrolled until submit.
```

## Present Results to User

## Explain the update strategy (submit vs controlled) and where focus is preserved.

name: vani-forms-inputs description: Implement Vani forms and inputs without losing focus.
argument-hint: "[form or input behavior]"

---

# Vani Forms and Inputs Command

## When to use

Use this skill when handling inputs, forms, or focus-sensitive UI in Vani.

## Instructions

Follow these steps:

1. Keep input values in local variables.
2. Read input changes via `oninput` without calling `handle.update()`.
3. On submit or blur, update state and call `handle.update()`.
4. For controlled inputs, use a `DomRef`, call `handle.updateSync()`, then restore focus/selection.

## Output expectations

- Use only `@vanijs/vani` or other public packages.
- Avoid re-rendering on every keystroke unless focus is preserved.
- If $ARGUMENTS is provided, adapt the strategy to that form scenario.
