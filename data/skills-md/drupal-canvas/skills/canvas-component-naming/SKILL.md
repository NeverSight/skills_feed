---
name: canvas-component-naming
description:
  Name Canvas components with clear, portable conventions for machine names and
  folders. Use when (1) Creating a new component, (2) Renaming components, (3)
  Reviewing component names for consistency. Ensures portable, descriptive
  component names.
---

**Use simple, generic names.** Never prefix component names with the project or
site name. Components should be reusable and their names should describe their
purpose, not their origin.

Use `kebab-case` for component names (for example, `machineName`,
`src/components/<name>/`, and story filenames).

When copying and modifying an example component, keep the original name unless
the component serves a fundamentally different purpose. When creating a new
component without an example, choose a simple, descriptive name.

```
# Correct - simple, descriptive names
footer
hero
navigation
contact-form

# Wrong - prefixed with project/site name
nebula-footer
acme-hero
mysite-navigation
projectx-contact-form
```

This ensures components remain portable and their names clearly communicate
their function rather than their project context.
