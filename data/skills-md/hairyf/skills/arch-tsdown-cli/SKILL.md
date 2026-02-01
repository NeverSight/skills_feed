---
name: arch-tsdown-cli
description: TypeScript CLI starter using tsdown. Use when scaffolding or maintaining an npm CLI package with tsdown, pnpm, Vitest, and npm Trusted Publisher.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/hairyf/starter-cli, scripts located at https://github.com/antfu/skills
---

arch-tsdown-cli is a TypeScript **CLI package** starter (based on hairyf/starter-cli) that uses **tsdown** for building. It provides a minimal, opinionated setup: dual surface (library + bin), ESM-only output, automatic `.d.ts` generation, dev bin via tsx, pnpm, Vitest, ESLint, and optional npm Trusted Publisher for CI-based releases.

> The skill is based on starter-cli (arch-tsdown-cli source), generated at 2026-01-30.

**Recommended practices:**
- Use dev bin (tsx) locally and prod bin (dist) in publishConfig
- Build pure ESM; enable `dts` and keep `external` for dependencies
- Use npm Trusted Publisher for releases

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Project purpose, structure, when to use | [core-overview](references/core-overview.md) |
| Bin Entry | dev vs prod bin, shebang, tsx | [core-bin-entry](references/core-bin-entry.md) |
| tsdown Config | entry, format, dts, external | [core-tsdown-config](references/core-tsdown-config.md) |
| Scripts & Release | build, dev, start, release, npm Trusted Publisher | [core-scripts](references/core-scripts.md) |
| Package Exports | dist, bin, publishConfig, files | [core-package-exports](references/core-package-exports.md) |
| Tooling | ESLint, TypeScript, Vitest config | [core-tooling](references/core-tooling.md) |
| Git Hooks | simple-git-hooks, lint-staged, pre-commit | [core-git-hooks](references/core-git-hooks.md) |
| CI | GitHub Actions — lint, typecheck, test matrix | [core-ci](references/core-ci.md) |
| Testing | Vitest, vitest-package-exports | [core-testing](references/core-testing.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| CLI & Package | bin, ESM, dts, external, release | [best-practices-cli](references/best-practices-cli.md) |
