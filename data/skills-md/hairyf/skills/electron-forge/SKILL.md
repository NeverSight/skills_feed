---
name: electron-forge
description: Package and distribute Electron apps with a full build pipeline. Use when scaffolding, configuring makers/publishers/plugins, or extending Forge.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/electron-forge/electron-forge-docs, scripts located at https://github.com/antfu/skills
---

Electron Forge is an all-in-one tool for packaging and distributing Electron applications. It combines packaging, code signing, installers, and publishing into one pipeline and supports custom plugins, makers, and publishers.

> Skills are based on Electron Forge (docs as of 2026-01-30), generated from electron-forge-docs.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Why Electron Forge | Motivation, value proposition, Forge vs Builder | [core-why-electron-forge](references/core-why-electron-forge.md) |
| Build Lifecycle | Package → Make → Publish; hooks; cross-platform | [core-build-lifecycle](references/core-build-lifecycle.md) |
| CLI | Init, import, package, make, publish, start; flags; programmatic API | [core-cli](references/core-cli.md) |

## Configuration

| Topic | Description | Reference |
|-------|-------------|-----------|
| Configuration | forge.config.js, packagerConfig, makers, publishers, plugins, hooks, buildIdentifier | [config-configuration](references/config-configuration.md) |
| Hooks | generateAssets, preStart, postPackage, preMake, postMake, readPackageJson, etc. | [config-hooks](references/config-hooks.md) |
| TypeScript config | forge.config.ts, ForgeConfig, constructor syntax | [config-typescript](references/config-typescript.md) |
| Plugins overview | Bundler (Webpack, Vite) and utility plugins | [config-plugins-overview](references/config-plugins-overview.md) |
| Webpack plugin | main/renderer config, magic globals, HMR, native modules | [config-plugins-webpack](references/config-plugins-webpack.md) |
| Vite plugin | build/renderer entries, HMR globals, native externals | [config-plugins-vite](references/config-plugins-vite.md) |
| Makers overview | Config, platforms; DMG, ZIP, Squirrel, deb, rpm, etc. | [config-makers-overview](references/config-makers-overview.md) |
| Publishers overview | GitHub, S3, Nucleus; config; auto-update | [config-publishers-overview](references/config-publishers-overview.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Import existing project | import command and manual setup | [features-import-existing-project](references/features-import-existing-project.md) |
| Built-in templates | webpack, vite, TypeScript variants; create-electron-app | [features-templates](references/features-templates.md) |

## Guides

| Topic | Description | Reference |
|-------|-------------|-----------|
| Code signing | macOS and Windows; where to configure | [guides-code-signing](references/guides-code-signing.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Auto update | update.electronjs.org, S3, custom servers (Nucleus, etc.) | [advanced-auto-update](references/advanced-auto-update.md) |
| Debugging | Main process: CLI, VS Code, JetBrains | [advanced-debugging](references/advanced-debugging.md) |
| Writing plugins | PluginBase, getHooks, startLogic | [advanced-extending-plugins](references/advanced-extending-plugins.md) |
| Writing makers | MakerBase, isSupportedOnCurrentPlatform, make | [advanced-extending-makers](references/advanced-extending-makers.md) |
| Writing publishers | PublisherBase, publish; multi-call behavior | [advanced-extending-publishers](references/advanced-extending-publishers.md) |
| Writing templates | ForgeTemplate, requiredForgeVersion, initializeTemplate | [advanced-extending-templates](references/advanced-extending-templates.md) |
