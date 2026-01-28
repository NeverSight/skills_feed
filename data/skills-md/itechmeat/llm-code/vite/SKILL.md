---
name: vite
description: "Vite next-gen frontend tooling: dev server, HMR, build, config, plugins, Environment API, Rolldown. Keywords: vite.config, bundler."
version: "7.3.1"
release_date: "2026-01-07"
---

# Vite

## When to use

- User asks how to set up or run a Vite project.
- User needs Vite configuration guidance (`vite.config.*`).
- User needs plugin authoring, HMR, or JS API usage.
- User needs environment variables or modes behavior.

## Quick navigation

- Getting started: references/getting-started.md
- Philosophy and rationale: references/philosophy.md, references/why-vite.md
- Features: references/features.md
- CLI: references/cli.md
- Plugins (usage): references/using-plugins.md
- Plugin API: references/api-plugin.md
- HMR API: references/api-hmr.md
- JavaScript API: references/api-javascript.md
- Config reference: references/config.md
- Dependency optimization: references/dep-pre-bundling.md
- Assets: references/assets.md
- Build: references/build.md
- Static deploy: references/static-deploy.md
- Env & modes: references/env-and-mode.md
- SSR: references/ssr.md
- Backend integration: references/backend-integration.md
- Troubleshooting: references/troubleshooting.md
- Performance: references/performance.md
- Rolldown: references/rolldown.md
- Migration: references/migration.md
- Breaking changes: references/breaking-changes.md
- Environment API: references/api-environment.md
- Environment instances: references/api-environment-instances.md
- Env plugins: references/api-environment-plugins.md
- Env frameworks: references/api-environment-frameworks.md
- Env runtimes: references/api-environment-runtimes.md

## Core rules

- Prefer minimal configuration; extend only as needed.
- Keep `index.html` as a first-class entry point when using Vite defaults.
- Treat dev server settings and build settings separately.
- Document mode-dependent behavior for env variables and `define`.
- Use `future` config to opt-in to deprecation warnings before migration.

## Recipes

- Scaffold a project with `npm create vite@latest`.
- Configure aliases, server options, and build outputs in `vite.config.*`.
- Load `.env` values into config with `loadEnv` when config needs them.
- Add plugins with `plugins: []` and define `apply` or `enforce` when needed.
- Use HMR APIs for fine-grained updates when plugin or framework needs it.
- Use `optimizeDeps.include/exclude` when deps aren't discovered on startup.
- Use `build.rollupOptions.input` for multi-page apps.
- Enable deprecation warnings: `future: { removeSsrLoadModule: 'warn' }`.
- Use `hotUpdate` hook instead of `handleHotUpdate` for environment-aware HMR.
- Use `this.environment` instead of `options.ssr` in plugin hooks.

## Prohibitions

- Do not copy large verbatim chunks from vendor docs.
- Do not assume framework-specific behavior without verifying.

## Links

- https://vite.dev/guide/
- https://vite.dev/config/
- https://vite.dev/guide/api-plugin
- https://vite.dev/guide/api-hmr
- https://vite.dev/guide/api-javascript
- https://vite.dev/guide/api-environment
