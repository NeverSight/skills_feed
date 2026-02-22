---
name: nebula-component-validation
description:
  Validate components before uploading to Canvas. Use after creating or
  modifying components, before considering work complete. Runs `npm run
  code:fix` for Prettier, ESLint, and Canvas requirements.
---

# Validate

Before running validation, confirm every new component has a matching
`src/stories/<component-name>.stories.jsx` file (see
`nebula-storybook-stories`).

After creating or modifying components, always validate your code by running the
`code:fix` script. Make sure to use the right package manager. For example, if
using npm, run the following command:

```bash
npm run code:fix
```

This runs Prettier and ESLint with auto-fix, ensuring:

- Consistent formatting
- Common issue detection
- Drupal Canvas Code Component requirements

If errors remain after auto-fix, address them manually and re-run until passing.
