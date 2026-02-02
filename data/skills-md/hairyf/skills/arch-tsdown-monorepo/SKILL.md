---
name: arch-tsdown-monorepo
description: pnpm monorepo starter for TypeScript libraries with tsdown per package. Use when scaffolding or maintaining a multi-package TS/ESM repo with workspace deps and npm Trusted Publisher.
metadata:
  author: hairy
  version: "2026.2.2"
  source: Generated from https://github.com/hairyf/starter-monorepo, scripts located at https://github.com/antfu/skills
---

arch-tsdown-monorepo is a **pnpm monorepo** starter for TypeScript libraries (based on [hairyf/starter-monorepo](https://github.com/hairyf/starter-monorepo)). Each package uses **tsdown** for building. It provides shared tooling (ESLint, Vitest, TypeScript), **pnpm catalogs** for versions, **workspace dependencies**, and optional **npm Trusted Publisher** for CI-based releases.

> The skill is based on hairyf/starter-monorepo, generated at 2026-02-02.

**Recommended practices:**
- Use pnpm catalogs for devDependency versions; reference with `catalog:cli`, `catalog:testing`, etc.
- Use `workspace:*` for inter-package dependencies; publish once manually, then use npm Trusted Publisher for CI releases.
- Run build/typecheck/test from root with `pnpm -r run ...` and a single Vitest config with projects (root + packages/*).

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Monorepo purpose, structure, when to use | [core-overview](references/core-overview.md) |
| Workspace | pnpm workspace, catalogs, workspace:* deps | [core-workspace](references/core-workspace.md) |
| Packages | Package layout, exports, inter-package deps | [core-packages](references/core-packages.md) |
| Package Exports | Dual exports (dev vs publish), main/module/types, files, sideEffects | [core-package-exports](references/core-package-exports.md) |
| tsdown (per package) | entry, dts, exports, publint | [core-tsdown-per-package](references/core-tsdown-per-package.md) |
| Scripts | Root and package scripts — build, dev, typecheck, test, release | [core-scripts](references/core-scripts.md) |
| Testing | Vitest projects — root + packages/* | [core-testing](references/core-testing.md) |
| Tooling | ESLint, TypeScript, .gitignore, .vscode | [core-tooling](references/core-tooling.md) |
| CI | GitHub Actions — lint, typecheck, test matrix | [core-ci](references/core-ci.md) |
| Release | npm Trusted Publisher, bumpp, release workflow | [core-release](references/core-release.md) |
| Git Hooks | simple-git-hooks, lint-staged, pre-commit | [core-git-hooks](references/core-git-hooks.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Exports Snapshot | Per-package export snapshot tests (vitest-package-exports, runIf(IS_READY)) | [features-exports-snapshot](references/features-exports-snapshot.md) |
| Add Package | Step-by-step adding a new workspace package | [features-add-package](references/features-add-package.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Monorepo | Catalogs, workspace deps, release, build order | [best-practices-monorepo](references/best-practices-monorepo.md) |
