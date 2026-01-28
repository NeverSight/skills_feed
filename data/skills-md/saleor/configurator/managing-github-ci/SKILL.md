---
name: managing-github-ci
description: "Configures GitHub Actions workflows and CI/CD pipelines. Manages automated releases via Changesets, PR validation, and Husky hooks. Troubleshoots CI failures. Triggers on: GitHub Actions, CI pipeline, workflow, release automation, Husky hooks, gh CLI, workflow failure."
allowed-tools: "Read, Grep, Glob, Write, Edit, Bash(gh:*)"
---

# GitHub CI Automation

## Purpose

Guide the configuration and management of GitHub Actions workflows, release automation, and CI/CD pipelines for the Saleor Configurator project.

## When to Use

- Creating or modifying GitHub Actions workflows
- Setting up automated releases
- Troubleshooting CI failures
- Configuring pre-commit/pre-push hooks
- Managing Changesets releases

## Table of Contents

- [Project CI Architecture](#project-ci-architecture)
- [Workflow: test-on-pr.yml](#workflow-test-on-pryml)
- [Workflow: release.yml](#workflow-releaseyml)
- [Workflow: changeset-bot.yml](#workflow-changeset-botyml)
- [Pre-Push Hooks (Husky)](#pre-push-hooks-husky)
- [Changesets Configuration](#changesets-configuration)
- [GitHub CLI Commands](#github-cli-commands)
- [Troubleshooting CI Failures](#troubleshooting-ci-failures)
- [Adding New Workflows](#adding-new-workflows)
- [Secrets Management](#secrets-management)
- [References](#references)

## Project CI Architecture

```
.github/
├── workflows/
│   ├── test-on-pr.yml      # PR validation
│   ├── release.yml         # Automated releases
│   └── changeset-bot.yml   # Changeset automation
└── ...

.husky/
├── pre-push               # Pre-push hooks
└── ...

.changeset/
├── config.json            # Changeset configuration
└── *.md                   # Pending changesets
```

## Workflow: test-on-pr.yml

**Purpose**: Validate PRs before merge

```yaml
name: Test on PR

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Type check
        run: pnpm typecheck

      - name: Lint
        run: pnpm lint

      - name: Test
        run: pnpm test

      - name: Build
        run: pnpm build
```

### Required Checks

| Check | Command | Purpose |
|-------|---------|---------|
| Type check | `pnpm typecheck` | TypeScript validation |
| Lint | `pnpm lint` | Biome linting |
| Test | `pnpm test` | Vitest test suite |
| Build | `pnpm build` | Compilation check |

## Workflow: release.yml

**Purpose**: Automated npm releases via Changesets

```yaml
name: Release

on:
  push:
    branches: [main]

concurrency: ${{ github.workflow }}-${{ github.ref }}

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm build

      - name: Create Release Pull Request or Publish
        uses: changesets/action@v1
        with:
          publish: pnpm publish:ci-prod
          version: pnpm changeset version
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Release Flow

```
1. Developer creates changeset → pnpm changeset
2. PR merged to main
3. Changesets action runs:
   a. If changesets exist → Creates "Version Packages" PR
   b. If version PR merged → Publishes to npm
```

## Workflow: changeset-bot.yml

**Purpose**: Comment on PRs about missing changesets

```yaml
name: Changeset Bot

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Changeset Bot
        uses: changesets/bot@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Pre-Push Hooks (Husky)

Located in `.husky/pre-push`:

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Generate schema documentation before push
pnpm generate-schema-docs
git add docs/SCHEMA.md

# Check if there are changes to commit
if ! git diff --staged --quiet; then
  git commit -m "docs: update schema documentation"
fi
```

### Hook Behavior

- Runs `generate-schema-docs` before every push
- Auto-commits schema documentation updates
- Ensures docs stay in sync with schema changes

## Changesets Configuration

Located in `.changeset/config.json`:

```json
{
  "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": []
}
```

### Changeset Types

| Type | When to Use |
|------|-------------|
| `patch` | Bug fixes, documentation, refactoring |
| `minor` | New features, non-breaking enhancements |
| `major` | Breaking changes, API modifications |

## GitHub CLI Commands

### Check Workflow Status

```bash
# List recent workflow runs
gh run list --limit 10

# View specific run
gh run view <run-id>

# Watch running workflow
gh run watch <run-id>
```

### PR Management

```bash
# Create PR
gh pr create --title "feat: new feature" --body "Description"

# List PRs
gh pr list

# View PR details
gh pr view <pr-number>

# Check PR status
gh pr checks <pr-number>
```

### Release Management

```bash
# List releases
gh release list

# Create release (manual)
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes"

# View release
gh release view v1.0.0
```

## Troubleshooting CI Failures

### Common Failures

**Type Check Fails**:
```bash
# Reproduce locally
pnpm typecheck
# or
npx tsc --noEmit
```

**Lint Fails**:
```bash
# Check and auto-fix
pnpm lint
pnpm check:fix
```

**Tests Fail**:
```bash
# Run specific test
pnpm test -- --filter=<test-file>

# Run with verbose output
pnpm test -- --reporter=verbose
```

**Build Fails**:
```bash
# Reproduce locally
pnpm build
```

### Debugging Workflow

1. Check workflow logs in GitHub Actions UI
2. Reproduce failure locally
3. Fix the issue
4. Push fix to PR
5. Re-run failed jobs: `gh run rerun <run-id>`

### Rate Limiting

If npm publish fails due to rate limiting:
- Wait and retry
- Check npm status: https://status.npmjs.org/

## Adding New Workflows

### Template Structure

```yaml
name: Workflow Name

on:
  # Trigger events
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      # Add your steps here
```

### Best Practices

- Always use `--frozen-lockfile` for installs
- Cache pnpm store for faster runs
- Use specific action versions (@v4, not @latest)
- Set `concurrency` to prevent duplicate runs
- Use secrets for sensitive values

## Secrets Management

### Required Secrets

| Secret | Purpose | Where Set |
|--------|---------|-----------|
| `GITHUB_TOKEN` | Auto-provided | GitHub |
| `NPM_TOKEN` | npm publishing | Repository Settings |

### Adding Secrets

1. Go to repository Settings
2. Navigate to Secrets and variables → Actions
3. Click "New repository secret"
4. Add name and value

## References

### Skill Reference Files
- **[Workflow Templates](references/workflow-templates.md)** - Reusable workflow patterns
- **[Troubleshooting Guide](references/troubleshooting.md)** - Detailed debugging patterns

### Project Resources
- `{baseDir}/.github/workflows/` - Workflow files
- `{baseDir}/.husky/` - Git hooks
- `{baseDir}/.changeset/` - Changeset configuration

### External Documentation
- GitHub Actions docs: https://docs.github.com/en/actions
- Changesets docs: https://github.com/changesets/changesets

## Related Skills

- **Creating releases**: See `creating-changesets` for changeset creation
- **Local validation**: See `validating-pre-commit` for reproducing CI checks locally
