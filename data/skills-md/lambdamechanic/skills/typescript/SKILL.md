---
name: typescript
description: "Default TypeScript stack for Lambda: pnpm workspaces + Turbo, strict TS, and sensible DX helpers."
---

# TypeScript Skill (pnpm + Turbo by default)

Baseline setup to reuse across projects. We standardize on pnpm workspaces and Turborepo for task orchestration.

## Workspace & Package Manager

- Use pnpm (9.x or later) and declare it in `package.json`:
  ```jsonc
  { "packageManager": "pnpm@9.x", "private": true }
  ```
- Add `pnpm-workspace.yaml` with your package globs (e.g., `packages/*`).
- Root scripts should fan out via pnpm: `pnpm -r lint`, `pnpm -r test`, `pnpm -r build`.

## Turbo as the Task Graph

- Add a minimal `turbo.json`:
  ```json
  {
    "pipeline": {
      "lint": { "outputs": [] },
      "test": { "dependsOn": ["^build"], "outputs": [] },
      "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] }
    }
  }
  ```
- Run with `pnpm turbo lint test build` (or shorter aliases).
- Keep per-package scripts named `lint`, `test`, `build`, `typecheck` so Turbo and pnpm can compose them.

## TS Baseline

- Node 18+ (prefer 20), ESM (`"type": "module"`), `target: ES2022+`, `moduleResolution: node16|bundler`, `strict: true`, `resolveJsonModule: true`, `skipLibCheck: true`, `sourceMap: true`.
- Root `tsconfig.base.json`; each package extends it and sets `rootDir: src`, `outDir: dist`. Use `composite: true` + project references for multi-package builds and `tsc -b`.

## Standard Scripts

- `typecheck`: `tsc --noEmit`
- `lint`: ESLint with `@typescript-eslint/*`
- `build`: `tsc -b` for libs/services; use `tsup` when you need bundled ESM+CJS + d.ts
- `test`: Vitest or Jest; keep `typecheck` separate so test runners don’t hide TS errors
- Root aliases: `pnpm -r typecheck`, `pnpm -r lint`, `pnpm -r build`, `pnpm -r test`; Turbo can wrap these when you want caching.

## DX & Code Hygiene

- Use `tsx` for local scripts (`pnpm add -D tsx`), avoid `ts-node` unless necessary.
- Validate inputs/env at boundaries (e.g., `zod`) to turn `unknown` into typed data.
- Prefer `unknown` over `any`; explicit return types on exports; keep `strict` green by fixing code, not loosening config.
- Imports stay in `src/`; never import from build outputs. Prefer ESM; use CJS only if the target requires it.
- Error handling: throw `Error` subclasses with context; avoid silent catches. Use `Promise.allSettled` for fan-out when partial failure is acceptable.

## Lint / Format

- ESLint with `@typescript-eslint/parser` and recommended configs; set `parserOptions.project` when rules need type info.
- Prettier for formatting; keep lint separate. Optional pre-commit via `lint-staged` + `simple-git-hooks`, or enforce in CI.

## Maintenance Extras

- **Knip/depcheck** for unused exports/deps sweeps.
- **Changesets** if you publish/version packages.
- Central `env.ts` that validates and types `process.env`.
