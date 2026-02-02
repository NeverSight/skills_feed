---
name: unplugin
description: Unified plugin system for Vite, Rollup, webpack, esbuild, Rspack, Farm, Rolldown, and Bun. Use when authoring or consuming build-tool plugins that work across bundlers.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/unjs/unplugin, scripts located at https://github.com/antfu/skills
---

Unplugin provides a single Rollup-style plugin API that runs on Vite, Rollup, webpack, esbuild, Rspack, Rolldown, Farm, and Bun. Use these skills when implementing a new unplugin, integrating an existing one, or debugging hook/context behavior across bundlers.

> The skill is based on unplugin v3.0.0, generated at 2026-01-30.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | What unplugin is, supported bundlers, when to use | [core-overview](references/core-overview.md) |
| Core API | createUnplugin, factory signature, bundler-specific creators | [core-api](references/core-api.md) |
| Hooks and context | Lifecycle hooks, filters, this.parse / emitFile / warn / error | [core-hooks-and-context](references/core-hooks-and-context.md) |
| Hook compatibility | Per-bundler support tables for hooks and context | [core-hook-compatibility](references/core-hook-compatibility.md) |
| Integration | Installing and registering in Vite, Rollup, webpack, etc. | [core-integration](references/core-integration.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Filters | filter option for resolveId, transform, load (performance) | [features-filters](references/features-filters.md) |
| Nested plugins | Returning an array of plugins from the factory | [features-nested-plugins](references/features-nested-plugins.md) |
| Bundler-specific | meta.framework, escape hatches (vite/webpack/esbuild/…), createXxxPlugin | [features-bundler-specific](references/features-bundler-specific.md) |
| Virtual modules | resolveId + load pattern; filter for load | [features-virtual-modules](references/features-virtual-modules.md) |
| Parsing | setParseImpl, this.parse; when needed (esbuild, webpack, etc.) | [features-parsing](references/features-parsing.md) |
| Output and assets | emitFile (EmittedAsset only), writeBundle (timing only) | [features-output-and-assets](references/features-output-and-assets.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Conventions | unplugin- prefix, keyword, default + subpath exports | [best-practices-conventions](references/best-practices-conventions.md) |
| Diagnostics | this.warn / this.error, UnpluginMessage shape | [best-practices-diagnostics](references/best-practices-diagnostics.md) |
| Scaffolding | Templates (unplugin-starter), try online, prerequisites | [best-practices-scaffolding](references/best-practices-scaffolding.md) |
