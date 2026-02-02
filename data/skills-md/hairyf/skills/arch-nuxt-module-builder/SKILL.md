---
name: arch-nuxt-module-builder
description: Build and ship Nuxt modules with @nuxt/module-builder. Use when scaffolding, building, or maintaining a Nuxt module (unbuild preset, types, runtime).
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/nuxt/module-builder, scripts located at https://github.com/antfu/skills
---

arch-nuxt-module-builder skills cover **@nuxt/module-builder**: the complete solution to build and ship Nuxt modules. It uses unbuild, automates module build config, generates types and shims for `@nuxt/schema`, and transforms `src/runtime/` (plugins, composables, components) to `dist/runtime/`. Use these skills when creating or maintaining a Nuxt module with the official module-builder stack.

> The skill is based on @nuxt/module-builder v1.0.2, generated at 2026-01-30.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | What module-builder is, requirements, quick start | [core-overview](references/core-overview.md) |
| Project structure | src/module.ts, src/runtime/, package.json, build.config.ts | [core-project-structure](references/core-project-structure.md) |
| Module definition | defineNuxtModule, ModuleOptions, hooks, runtime config types | [core-module-definition](references/core-module-definition.md) |
| Dist output | module.mjs, module.json, types.d.mts, runtime/* | [core-dist-output](references/core-dist-output.md) |
| CLI | nuxt-module-build build/prepare, args (cwd, outDir, stub) | [core-cli](references/core-cli.md) |
| CI | GitHub Actions — lint, typecheck, build, test | [core-ci](references/core-ci.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Runtime | src/runtime/ layout, plugins/composables/components, mkdist | [features-runtime](references/features-runtime.md) |
| Types generation | types.d.mts, ModuleOptions inference, shims | [features-types-generation](references/features-types-generation.md) |
| Build config | build.config.ts, extra entries, unbuild preset | [features-build-config](references/features-build-config.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Package exports | exports, typesVersions, prepack, files | [best-practices-package-exports](references/best-practices-package-exports.md) |
| Setup patterns | createResolver, addPlugin without extension | [best-practices-setup-patterns](references/best-practices-setup-patterns.md) |

## Assets

| Asset | Description |
|-------|-------------|
| [ci.yml](assets/ci.yml) | GitHub Actions CI workflow template — copy to `.github/workflows/ci.yml` |
