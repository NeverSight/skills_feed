---
name: arch-vscode
description: VSCode extension starter using reactive-vscode and tsdown. Use when scaffolding or maintaining a VSCode extension with reactive APIs, CJS build, and vscode-ext-gen.
metadata:
  author: hairy
  version: "2026.2.1"
  source: Generated from https://github.com/antfu/starter-vscode, scripts located at https://github.com/antfu/skills
---

arch-vscode is a **VSCode extension** starter (based on antfu/starter-vscode) that uses **reactive-vscode** for reactive APIs and composables, **tsdown** for a single CJS bundle, and **vscode-ext-gen** for type-safe contributes metadata. It provides a minimal, opinionated setup: defineExtension entry, defineConfig/defineLogger, Extension Host debugging, and vsce/vsxpub for packaging and publishing.

> The skill is based on starter-vscode (arch-vscode source), generated at 2026-01-30.

**Recommended practices:**
- Keep contributes and generated meta in sync via `pnpm update` (or Run on Save)
- Use reactive-vscode composables for state and disposables; use CJS build with external `vscode`
- Prefer `onCommand` activation when possible

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Project purpose, structure, when to use | [core-overview](references/core-overview.md) |
| Extension Entry | defineExtension, activate, deactivate | [core-extension-entry](references/core-extension-entry.md) |
| Config | defineConfig, generated scoped config | [core-config](references/core-config.md) |
| Logging | defineLogger, displayName | [core-logging](references/core-logging.md) |
| tsdown Build | CJS, external vscode, build:prepare hook | [core-tsdown-build](references/core-tsdown-build.md) |
| Scripts | build, dev, update, release, ext:package, ext:publish | [core-scripts](references/core-scripts.md) |
| Contributes | commands, configuration, activationEvents | [core-contributes](references/core-contributes.md) |
| Development | launch.json, tasks.json, Extension Host | [core-development](references/core-development.md) |
| CI | GitHub Actions workflow — lint, typecheck, build, test | [core-ci](references/core-ci.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| VSCode Extension | entry, contributes, meta, activation, publish | [best-practices-vscode-ext](references/best-practices-vscode-ext.md) |
