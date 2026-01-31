---
name: arch-tsdown
description: TypeScript library starter using tsdown. Use when scaffolding or maintaining a TS/ESM library with tsdown, pnpm, Vitest, and npm Trusted Publisher.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/antfu/starter-ts, scripts located at https://github.com/antfu/skills
---

arch-tsdown is a TypeScript library starter (based on antfu/starter-ts) that uses **tsdown** for building. It provides a minimal, opinionated setup: ESM-only output, automatic `.d.ts` generation, pnpm, Vitest, ESLint, and optional npm Trusted Publisher for CI-based releases.

> The skill is based on starter-ts (arch-tsdown source), generated at 2026-01-30.

**Recommended practices:**
- Build pure ESM; enable `dts` and `exports` in tsdown config
- Use npm Trusted Publisher for releases
- Run publint (via tsdown’s `publint: true`) before publishing

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Project purpose, structure, when to use | [core-overview](references/core-overview.md) |
| tsdown Config | entry, dts, exports, publint | [core-tsdown-config](references/core-tsdown-config.md) |
| Scripts & Release | build, dev, release, npm Trusted Publisher | [core-scripts](references/core-scripts.md) |
| Package Exports | dist output, types, exports field | [core-package-exports](references/core-package-exports.md) |
| Tooling | ESLint, TypeScript, Vitest config | [core-tooling](references/core-tooling.md) |
| Git Hooks | simple-git-hooks, lint-staged, pre-commit | [core-git-hooks](references/core-git-hooks.md) |
| CI | GitHub Actions — lint, typecheck, test matrix | [core-ci](references/core-ci.md) |
| Testing | Vitest, vitest-package-exports, export snapshots | [core-testing](references/core-testing.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| tsdown & Package | ESM, dts, exports, tooling alignment | [best-practices-tsdown](references/best-practices-tsdown.md) |
