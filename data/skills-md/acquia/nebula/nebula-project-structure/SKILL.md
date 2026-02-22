---
name: nebula-project-structure
description:
  Project folder structure and package manager detection for Nebula. Reference
  when navigating the codebase, running commands, or determining which package
  manager to use (npm/yarn/pnpm/bun).
---

# Project structure

This project uses a two-folder structure to separate example code from working
code:

```
src/
├── components/     # Working components (Storybook reads from here)
│   └── global.css  # Base styles imported by Storybook
├── stories/        # Working stories (Storybook reads from here)

examples/
├── components/     # Example component implementations (for reference)
└── stories/        # Example stories (for reference)
```

# Package manager

Detect the package manager by checking for lock files in the project root:

- `package-lock.json` → npm (`npm run`, `npx`)
- `yarn.lock` → yarn (`yarn`, `yarn dlx`)
- `pnpm-lock.yaml` → pnpm (`pnpm`, `pnpm dlx`)
- `bun.lockb` → bun (`bun run`, `bunx`)

Use the detected package manager for all commands in these instructions.
