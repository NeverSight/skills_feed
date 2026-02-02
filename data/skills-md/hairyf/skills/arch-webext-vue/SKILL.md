---
name: arch-webext-vue
description: Build and run browser extensions with Vue 3 and Vite (Vitesse WebExtension template). Use when scaffolding or maintaining a Chrome/Firefox extension with popup, options, sidepanel, and content script UI.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/antfu-collective/vitesse-webext, scripts located at https://github.com/antfu/skills
---

arch-webext-vue skills cover **Vitesse WebExt**: a Vite-powered WebExtension starter with Vue 3, TypeScript, UnoCSS, and webext-bridge. It uses multi-entry Vite for popup/options/sidepanel, separate configs for background and content script, dynamic manifest generation, and shared setup and storage patterns. Use these skills when creating or maintaining a browser extension with this stack.

> The skill is based on vitesse-webext (antfu-collective/vitesse-webext), generated at 2026-01-30.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Features, stack, when to use | [core-overview](references/core-overview.md) |
| Project structure | Folders, entry points, scripts | [core-project-structure](references/core-project-structure.md) |
| Manifest | Dynamic manifest, MV3, Firefox vs Chrome | [core-manifest](references/core-manifest.md) |
| CI | GitHub Actions — lint, typecheck, build, test, optional E2E | [core-ci](references/core-ci.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Vite build | Multi-config, shared config, background/content, dev stub | [features-vite-build](references/features-vite-build.md) |
| Background | Entry, webext-bridge, side panel, content script HMR | [features-background](references/features-background.md) |
| Content script | Entry, Vue in shadow DOM, styles | [features-content-script](references/features-content-script.md) |
| Views | Popup, options, sidepanel—entry pattern, setupApp | [features-views](references/features-views.md) |
| Storage | useWebExtensionStorage, shared logic | [features-storage](references/features-storage.md) |
| Cross-context | webext-bridge messaging between contexts | [features-cross-context](references/features-cross-context.md) |
| Dev workflow | pnpm dev vs dev-firefox, load extension, stub HTML | [features-dev-workflow](references/features-dev-workflow.md) |
| Pack & release | pack:zip, crx, xpi, clear, start:chromium/firefox | [features-pack-release](references/features-pack-release.md) |
| Testing | Vitest unit tests, Playwright E2E, fixtures, extensionId | [features-testing](references/features-testing.md) |
| Types & env | __DEV__, __NAME__, global/shim/modules.d.ts, env.ts | [features-types-and-env](references/features-types-and-env.md) |
| Components & icons | Auto-import components and icons, Iconify | [features-components-icons](references/features-components-icons.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Setup patterns | setupApp, common-setup, shared components/styles | [best-practices-setup-patterns](references/best-practices-setup-patterns.md) |
| Type-safe messaging | ProtocolMap in shim.d.ts for webext-bridge | [best-practices-type-safe-messaging](references/best-practices-type-safe-messaging.md) |
