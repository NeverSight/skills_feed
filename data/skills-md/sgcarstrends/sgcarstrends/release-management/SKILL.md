---
name: release-management
description: Automate releases using semantic-release, create release notes, manage versions, and publish packages. Use when preparing releases, managing versions, or automating release workflows.
allowed-tools: Read, Edit, Write, Bash, Grep
---

# Release Management Skill

This skill helps you automate releases using semantic-release and manage version control effectively.

## When to Use This Skill

- Creating new releases
- Automating version bumps
- Generating release notes
- Publishing packages
- Managing release branches
- Tagging versions
- Distributing releases

## Release Strategy

The project uses **semantic-release** for automated releases:
- **Automatic Versioning**: Based on conventional commits
- **Changelog Generation**: Auto-generated from commits
- **Git Tagging**: Automatic git tags (v1.0.0, v1.1.0, etc.)
- **GitHub Releases**: Published to GitHub with notes
- **NPM Publishing**: Optional package publishing

## Version Scheme

### Semantic Versioning (SemVer)

```
v1.2.3
│ │ │
│ │ └─ Patch: Bug fixes (backward compatible)
│ └─── Minor: New features (backward compatible)
└───── Major: Breaking changes
```

**Examples:**
- `v1.0.0` → `v1.0.1`: Bug fix
- `v1.0.0` → `v1.1.0`: New feature
- `v1.0.0` → `v2.0.0`: Breaking change

## Semantic Release Configuration

### .releaserc.json

```json
{
  "branches": ["main"],
  "plugins": [
    [
      "@semantic-release/commit-analyzer",
      {
        "preset": "conventionalcommits",
        "releaseRules": [
          { "type": "feat", "release": "minor" },
          { "type": "fix", "release": "patch" },
          { "type": "perf", "release": "patch" },
          { "type": "revert", "release": "patch" },
          { "type": "docs", "release": false },
          { "type": "style", "release": false },
          { "type": "chore", "release": false },
          { "type": "refactor", "release": false },
          { "type": "test", "release": false },
          { "type": "build", "release": false },
          { "type": "ci", "release": false }
        ],
        "parserOpts": {
          "noteKeywords": ["BREAKING CHANGE", "BREAKING CHANGES"]
        }
      }
    ],
    [
      "@semantic-release/release-notes-generator",
      {
        "preset": "conventionalcommits",
        "presetConfig": {
          "types": [
            { "type": "feat", "section": "Features" },
            { "type": "fix", "section": "Bug Fixes" },
            { "type": "perf", "section": "Performance Improvements" },
            { "type": "revert", "section": "Reverts" },
            { "type": "docs", "section": "Documentation", "hidden": true },
            { "type": "style", "section": "Styles", "hidden": true },
            { "type": "chore", "section": "Miscellaneous Chores", "hidden": true },
            { "type": "refactor", "section": "Code Refactoring", "hidden": true },
            { "type": "test", "section": "Tests", "hidden": true },
            { "type": "build", "section": "Build System", "hidden": true },
            { "type": "ci", "section": "Continuous Integration", "hidden": true }
          ]
        }
      }
    ],
    [
      "@semantic-release/changelog",
      {
        "changelogFile": "CHANGELOG.md"
      }
    ],
    [
      "@semantic-release/npm",
      {
        "npmPublish": false
      }
    ],
    [
      "@semantic-release/github",
      {
        "assets": [
          {
            "path": "dist/**",
            "label": "Distribution"
          }
        ]
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": ["CHANGELOG.md", "package.json"],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ]
  ]
}
```

## Release Workflow

### Automatic Release (CI)

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install

      - name: Build packages
        run: pnpm build

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

### Manual Release

```bash
# Dry run (preview release)
npx semantic-release --dry-run

# Create release
npx semantic-release

# Force specific version
npx semantic-release --release-as minor
npx semantic-release --release-as major
npx semantic-release --release-as 1.2.3
```

## Release Process

### 1. Commit Changes

```bash
# Make changes
vim src/feature.ts

# Commit with conventional format
git add .
git commit -m "feat: add new feature X

Implement feature X that does Y

Closes #123"

# Push to main
git push origin main
```

### 2. Automatic Release Triggers

```bash
# CI detects push to main
# → Runs semantic-release
# → Analyzes commits since last release
# → Determines version bump
# → Generates changelog
# → Creates git tag
# → Publishes GitHub release
# → Updates CHANGELOG.md
```

### 3. Verify Release

```bash
# Check GitHub releases
open https://github.com/username/repo/releases

# Check git tags
git fetch --tags
git tag

# Check CHANGELOG.md
cat CHANGELOG.md
```

## Version Bumping

### Patch Release (0.0.x)

```bash
# Bug fix commits trigger patch
git commit -m "fix: resolve login timeout issue"

# Results in: v1.0.0 → v1.0.1
```

### Minor Release (0.x.0)

```bash
# Feature commits trigger minor
git commit -m "feat: add export to CSV functionality"

# Results in: v1.0.0 → v1.1.0
```

### Major Release (x.0.0)

```bash
# Breaking change triggers major
git commit -m "feat!: redesign authentication system

BREAKING CHANGE: Auth tokens now use JWT format.
Update clients to use new authentication flow."

# Results in: v1.0.0 → v2.0.0
```

## Release Notes

### Auto-Generated Release Notes

Semantic-release generates release notes from commits:

```markdown
# v1.2.0 (2024-01-15)

## Features

* add blog post generation with Gemini AI ([#123](https://github.com/user/repo/pull/123)) ([abc1234](https://github.com/user/repo/commit/abc1234))
* add social media integration ([#124](https://github.com/user/repo/pull/124)) ([def5678](https://github.com/user/repo/commit/def5678))

## Bug Fixes

* fix database connection timeout ([#125](https://github.com/user/repo/issues/125)) ([ghi9012](https://github.com/user/repo/commit/ghi9012))
* fix chart rendering on mobile ([#126](https://github.com/user/repo/issues/126)) ([jkl3456](https://github.com/user/repo/commit/jkl3456))

## Performance Improvements

* optimize database queries ([#127](https://github.com/user/repo/pull/127)) ([mno7890](https://github.com/user/repo/commit/mno7890))
```

### Custom Release Notes

Edit after creation:

```bash
# Edit release on GitHub
# 1. Go to Releases page
# 2. Click "Edit release"
# 3. Add custom notes:

## Highlights

🎉 This release adds AI-powered blog generation!

## Migration Guide

If upgrading from v1.0.0, please:
1. Run database migrations: `pnpm db:migrate`
2. Update environment variables (see .env.example)

## Contributors

Thanks to @contributor1 and @contributor2!
```

## Pre-releases

### Beta Releases

```bash
# Create beta branch
git checkout -b beta

# Make changes
git commit -m "feat: add experimental feature"

# Configure semantic-release for beta
# .releaserc.json
{
  "branches": [
    "main",
    {
      "name": "beta",
      "prerelease": true
    }
  ]
}

# Push beta branch
git push origin beta

# Results in: v1.1.0-beta.1
```

### Release Candidates

```bash
# Create RC branch
git checkout -b release/1.1.0-rc

# Configure for RC
{
  "branches": [
    "main",
    {
      "name": "release/+([0-9])?(.{+([0-9]),x}).x",
      "prerelease": "rc"
    }
  ]
}

# Results in: v1.1.0-rc.1
```

## Hotfix Releases

### Emergency Fixes

```bash
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-bug

# Fix the bug
git commit -m "fix: resolve critical security vulnerability"

# Merge to main (triggers release)
git checkout main
git merge hotfix/critical-bug
git push origin main

# Results in: v1.0.1 (patch bump)
```

## Multi-Package Releases

### Independent Versions

```json
// lerna.json or package.json
{
  "version": "independent",
  "packages": ["apps/*", "packages/*"]
}
```

### Synchronized Versions

```json
{
  "version": "1.0.0",
  "packages": ["apps/*", "packages/*"]
}
```

## Release Checklist

### Pre-Release

- [ ] All tests passing
- [ ] No linting errors
- [ ] Type checks pass
- [ ] Documentation updated
- [ ] CHANGELOG.md reviewed
- [ ] Security audit clean
- [ ] Migration guide prepared (if breaking)

### Post-Release

- [ ] Verify GitHub release created
- [ ] Check CHANGELOG.md updated
- [ ] Verify git tag created
- [ ] Test deployed version
- [ ] Announce release (if major)
- [ ] Update documentation site
- [ ] Close related issues

## Rollback Strategy

### Revert Release

```bash
# Find release commit
git log --oneline

# Revert release
git revert <release-commit-sha>

# Push revert
git push origin main

# Or: Delete tag and re-release
git tag -d v1.2.0
git push origin :refs/tags/v1.2.0

# Fix issues and re-release
git commit -m "fix: resolve issue from v1.2.0"
git push origin main
```

## Notifications

### Slack Notification

```yaml
# .github/workflows/release.yml
- name: Notify Slack
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "🚀 New release: v${{ steps.version.outputs.version }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*New Release*\nVersion: v${{ steps.version.outputs.version }}\nChangelog: https://github.com/user/repo/releases/tag/v${{ steps.version.outputs.version }}"
            }
          }
        ]
      }
```

## Best Practices

### 1. Conventional Commits

```bash
# ❌ Poor commit messages
git commit -m "fixed stuff"
git commit -m "updates"

# ✅ Conventional commits
git commit -m "fix: resolve login timeout issue"
git commit -m "feat: add CSV export functionality"
git commit -m "feat!: redesign authentication

BREAKING CHANGE: New auth flow required"
```

### 2. Meaningful Changelogs

```markdown
# ❌ Vague changelog
## [1.1.0]
- Added stuff
- Fixed things

# ✅ Clear changelog
## [1.1.0]
### Added
- Blog post generation with Google Gemini AI
- Social media integration (Discord, LinkedIn, Telegram, Twitter)

### Fixed
- Database connection timeout during large imports
- Chart rendering issue on iOS Safari
```

### 3. Test Before Release

```bash
# ❌ Release without testing
git commit -m "feat: add feature"
git push  # Triggers release

# ✅ Test in CI before merge
# 1. Create PR
# 2. CI runs tests
# 3. Review and approve
# 4. Merge to main
# 5. Release triggered
```

### 4. Document Breaking Changes

```bash
# ✅ Always document breaking changes
git commit -m "feat!: redesign API endpoints

BREAKING CHANGE: Endpoint paths changed.
- /api/cars → /api/v1/cars
- /api/coe → /api/v1/coe

Migration guide: docs.sgcarstrends.com/migration"
```

## Troubleshooting

### No Release Created

```bash
# Issue: Semantic release not creating release
# Possible causes:
# 1. No conventional commits since last release
# 2. Only chore/docs commits (don't trigger release)
# 3. Wrong branch

# Solution: Check commits
git log --oneline v1.0.0..HEAD

# Ensure you have feat/fix commits
```

### Wrong Version Bump

```bash
# Issue: Expected minor, got patch
# Cause: Commit type incorrect

# Check commit format
git log --oneline -1

# Should be:
# feat: add feature (minor)
# fix: fix bug (patch)
# feat!: breaking (major)
```

### Release Failed in CI

```bash
# Issue: Release job failed
# Solution: Check CI logs

# Common issues:
# 1. Missing GITHUB_TOKEN permission
# 2. Build failed before release
# 3. Semantic release config error

# Fix permissions:
permissions:
  contents: write
  issues: write
  pull-requests: write
```

## References

- Semantic Release: https://semantic-release.gitbook.io
- Conventional Commits: https://www.conventionalcommits.org
- Semantic Versioning: https://semver.org
- Related files:
  - `.releaserc.json` - Semantic release config
  - `CHANGELOG.md` - Generated changelog
  - Root CLAUDE.md - Release guidelines

## Best Practices Summary

1. **Conventional Commits**: Follow format for automatic versioning
2. **Automate Releases**: Use semantic-release in CI
3. **Test Thoroughly**: Ensure tests pass before merge
4. **Document Changes**: Clear changelogs and migration guides
5. **Tag Versions**: Use git tags for version tracking
6. **Notify Team**: Alert on new releases
7. **Rollback Plan**: Have strategy for reverting bad releases
8. **Pre-releases**: Use beta/rc for testing before stable
