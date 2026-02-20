---
name: release
description: Release workflow for agent-vault. Follow these steps when publishing a new version.
---

# Release

## Steps

```bash
# 1. Commit all changes first

# 2. Bump version (patch / minor / major)
npm version <patch|minor|major> -m "chore: bump version to %s"

# 3. Push commit and tag
git push && git push --tags
```

CI will automatically run tests, publish to npm, and create a GitHub Release.

## Rules

- Always pass `-m "chore: bump version to %s"` to `npm version`
- Tag format: `v*` (e.g. `v0.2.0`), this is npm's default
- Do NOT manually edit `version` in `package.json` — always use `npm version`
- Do NOT manually create tags — `npm version` creates them
- Ensure all changes are committed before running `npm version`
- CI requires the GitHub repo to be public (for `--provenance`)
- npm trusted publishing via OIDC — no `NPM_TOKEN` secret needed, configured on npmjs.com
