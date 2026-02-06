---
name: rsbuild-v2-upgrade
description: Migrate Rsbuild projects from v1 to v2. Use when a user asks to upgrade Rsbuild, follow the v1-to-v2 guide, update configs/plugins, or validate the upgrade.
---

# Rsbuild v1 to v2 Upgrade

## Workflow

1. **Confirm current setup**
   - Read `package.json` to identify Rsbuild and plugin packages in use.
   - Locate the Rsbuild config file (commonly `rsbuild.config.(ts|js|mjs|cjs)`).

2. **Open the official upgrade guide**
   - Use the v1 → v2 guide as the source of truth:
     - https://v2.rsbuild.rs/guide/upgrade/v1-to-v2

3. **Plan the upgrade path**
   - List breaking changes that apply to the project’s current config and plugins.
   - Note any removed or renamed options, defaults, or plugin APIs.

4. **Update dependencies**
   - Bump `@rsbuild/core` to v2 (currently Beta tag).
   - Bump Rsbuild plugins to latest versions via `npx taze major --include /rsbuild/ -w -r`

5. **Apply config and code changes**
   - Update the Rsbuild config to match v2 options and defaults.
   - Remove deprecated or unsupported settings.

6. **Validate**
   - Run the build and dev server.
   - Run tests or smoke checks relevant to the project.
   - Fix any warnings or errors surfaced by the new version.
