---
name: arch-unplugin
description: Build universal build-tool plugins with unplugin-starter. Use when scaffolding, building, or maintaining an unplugin (Vite, Rollup, Webpack, Nuxt, esbuild, Farm, Rspack, Astro).
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/unplugin/unplugin-starter, scripts located at https://github.com/antfu/skills
---

arch-unplugin skills cover **unplugin-starter**: a template for writing one plugin API and shipping it across Vite, Rollup, Webpack, Nuxt, esbuild, Farm, Rspack, and Astro. Use these skills when creating or maintaining an unplugin-based package.

> The skill is based on unplugin-starter (unplugin template), generated at 2026-01-30.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | What unplugin-starter is, unplugin architecture, template usage | [core-overview](references/core-overview.md) |
| Project structure | Package exports, src layout, entry points | [core-project-structure](references/core-project-structure.md) |
| Factory and API | UnpluginFactory, createUnplugin, transformInclude, transform | [core-factory-api](references/core-factory-api.md) |
| CI | GitHub Actions — lint, typecheck, build, test | [core-ci](references/core-ci.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Bundlers | Vite, Rollup, Webpack, esbuild, Farm, Rspack integration | [features-bundlers](references/features-bundlers.md) |
| Nuxt module | defineNuxtModule, addVitePlugin, addWebpackPlugin | [features-nuxt](references/features-nuxt.md) |
| Astro | Astro config hook, pushing unplugin.vite() into Vite plugins | [features-astro](references/features-astro.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Options and types | Options interface, typing entry points, exporting types | [best-practices-options-types](references/best-practices-options-types.md) |
| Dev and release | dev, play, test, release workflow, playground | [best-practices-dev-release](references/best-practices-dev-release.md) |
