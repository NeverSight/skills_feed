---
name: release-prep
description: Prepare repository for a new release. Use before creating a release PR to ensure everything is ready.
---

# Release Preparation Skill

Prepare repository for a new release.

## Usage

Use before creating a release PR to ensure everything is ready.

## Steps

1. Ensure working directory is clean (`git status`)
2. Run full test suite:
   - `pnpm test` for unit tests
   - `pnpm test:storybook` for visual regression
   - `pnpm lint` for code quality
3. Run clean build: `pnpm clean && pnpm i && pnpm build`
4. Verify all packages build successfully
5. Check CHANGELOG.md is up to date
6. Review version numbers in package.json files
7. Test example applications work correctly

## Release Workflow

- Project uses GitHub Actions for automated releases
- Releases triggered by merging PRs from `prepare-release` or `prepare-prerelease` branches
- Manual workflow dispatch available via `.github/workflows/release-dispatch.yml`
- Publishes to npm with appropriate tags

## Notes

- Current version: 0.12.0
- Follows conventional commit messages
- Automated changelog generation
- Linear MCP integration for issue tracking
