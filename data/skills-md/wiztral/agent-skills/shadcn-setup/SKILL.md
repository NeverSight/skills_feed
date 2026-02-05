---
name: shadcn-setup
description: Initialize Shadcn UI in an EXISTING Next.js or React (Vite) project.
---

# Shadcn Setup

Use this skill to add Shadcn UI to a project that already exists but doesn't have it configured.

## Documentation

- [Shadcn Installation](https://ui.shadcn.com/docs/installation)

## Workflow

### 1. Environment & Prerequisites Detection

Before initializing, ensure the environment is ready:

#### A. Framework

- **Next.js**: check for `next.config.js` or `next.config.ts`.
- **Vite**: check for `vite.config.ts` or `vite.config.js`.

#### B. Tailwind CSS (CRITICAL)

Shadcn **requires** Tailwind CSS. Verify it is installed and configured:

- Check for `tailwind.config.js` / `tailwind.config.ts` (v3).
- OR check for specific Tailwind v4 CSS imports in `globals.css`/`index.css`.
- **If missing**: Install Tailwind CSS first (follow official Tailwind guides for the specific framework). **DO NOT** proceed with `shadcn init` without Tailwind.

#### C. Path Aliases (`tsconfig.json`)

Shadcn relies on path aliases (e.g., `@/lib/utils`).

- Read `tsconfig.json` (or `jsconfig.json`).
- Ensure `"paths": { "@/*": ["./src/*"] }` (or similar) is configured.
- **If missing**: Add the alias configuration to `compilerOptions`.

### 2. Initialization

Run the init command using `pnpm`:

```bash
pnpm dlx shadcn@latest init
```

### 3. Configuration

Follow these defaults unless specified otherwise:

- **Style**: New York (Default) or Default.
- **Base Color**: Slate.
- **CSS Variables**: **YES** (Critical for dynamic theming).
- **Aliasing**: Accept defaults (usually `@/components`, `@/lib/utils`) or match `tsconfig.json`.

### 4. Cleanup & Boilerplate Removal

#### For Next.js (`app/`)

1. **Clean `page.tsx`**: Replace default Next.js hero content with a simple shadcn Button to verify setup.
2. **Clean `globals.css`**: Remove all default styling (root variables for foreground/background-rgb) EXCEPT:
    - Tailwind directives (`@tailwind base;`...)
    - Shadcn layer definitions (`@layer base { ... }`)

#### For Vite (`src/`)

1. **Clean `App.tsx`**: Remove `logos`, `count` state, and default boilerplates. Replace with a simple shadcn content.
2. **Clean `index.css`**: Ensure it contains Tailwind directives and Shadcn base layers. Remove legacy `:root` styles if they conflict.

### 5. Verification

- Check `components.json` exists.
- Check `lib/utils.ts` (or configured alias) exists and exports `cn`.

## References
-   [Troubleshooting Common Errors](references/troubleshooting.md)
