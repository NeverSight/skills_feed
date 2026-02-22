---
name: setup-semantic-release
description: |
  Use when setting up automated versioning, when asked to "set up semantic release",
  "add conventional commits", "configure automated versioning", "set up commitlint",
  "add husky hooks", "set up changelog generation", or when initializing a new project
  that needs a commit and release workflow.
license: MIT
metadata:
  author: Antonin Januska
  version: "1.0.0"
tags: [git, semantic-release, commitlint, husky, versioning, changelog, ci-cd]
---

# Setup Semantic Release & Conventional Commits

## Overview

Set up a fully automated versioning and release pipeline using conventional commits, commitlint, husky git hooks, and semantic-release. Version bumps, changelogs, and GitHub releases are derived automatically from commit messages.

**Core principle:** Commits drive releases — enforce commit format at author time, automate everything else.

## When to Use

**Always use when:**
- Setting up a new project that needs automated versioning
- Adding conventional commits to an existing repo
- Asked to "set up semantic release" or "add commitlint"
- Migrating from manual versioning to automated releases

**Useful for:**
- Any npm/Node.js project publishing to npm or GitHub
- Projects that want auto-generated changelogs
- Teams that need consistent commit message formatting

**Avoid when:**
- Project already has semantic-release configured (check for `.releaserc*`)
- Project uses a different release tool (changesets, release-it, standard-version)
- Non-Node.js project without package.json (adapt manually instead)

## Prerequisites

Before starting, verify:

- [ ] Project has a `package.json`
- [ ] Project uses git with a remote on GitHub
- [ ] Node.js >= 18 installed
- [ ] npm or equivalent package manager available
- [ ] A CI/CD environment (GitHub Actions recommended) for automated releases

## Setup Workflow

### Phase 1: Install Dependencies

Install all required dev dependencies:

```bash
npm install --save-dev \
  @commitlint/cli@^19.0.0 \
  @commitlint/config-conventional@^19.0.0 \
  semantic-release@^24.0.0 \
  @semantic-release/changelog@^6.0.0 \
  @semantic-release/git@^10.0.0 \
  husky@^9.0.0
```

**What each package does:**
| Package | Purpose |
|---------|---------|
| `@commitlint/cli` | Validates commit messages against rules |
| `@commitlint/config-conventional` | Preset rules for conventional commit format |
| `semantic-release` | Automates version bumps, changelogs, and releases |
| `@semantic-release/changelog` | Generates/updates CHANGELOG.md |
| `@semantic-release/git` | Commits release artifacts back to repo |
| `husky` | Manages git hooks from package.json |

**Verification:**
- [ ] All packages appear in `devDependencies`
- [ ] No install errors

### Phase 2: Configure Commitlint

Create `commitlint.config.js` in the project root:

```js
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation only
        'style',    // Formatting, no code change
        'refactor', // Code change that neither fixes nor adds
        'perf',     // Performance improvement
        'test',     // Adding/updating tests
        'build',    // Build system or dependencies
        'ci',       // CI configuration
        'chore',    // Maintenance tasks
        'revert',   // Revert previous commit
      ],
    ],
    'subject-case': [2, 'always', 'lower-case'],
    'header-max-length': [2, 'always', 100],
    'body-max-line-length': [0], // Disable for semantic-release changelog
  },
};
```

**IMPORTANT:** If the project does NOT have `"type": "module"` in package.json, use `module.exports = { ... }` instead of `export default`.

**Commit message format:**
```
type(scope): subject

body (optional)

footer (optional)
```

**How types map to version bumps:**
- `feat` = minor bump (1.0.0 -> 1.1.0)
- `fix` = patch bump (1.0.0 -> 1.0.1)
- `feat!` or `BREAKING CHANGE` in footer = major bump (1.0.0 -> 2.0.0)
- All other types (`docs`, `test`, `chore`, etc.) = no release

**Verification:**
- [ ] `commitlint.config.js` exists at project root
- [ ] Module syntax matches project type (ESM vs CJS)

### Phase 3: Configure Semantic Release

Create `.releaserc.json` in the project root:

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    [
      "@semantic-release/changelog",
      {
        "changelogFile": "CHANGELOG.md"
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": ["CHANGELOG.md", "package.json", "package-lock.json"],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ],
    "@semantic-release/github"
  ]
}
```

**Key details:**
- `branches`: Set to your release branch. Change `"main"` if your default branch is `"master"` or something else.
- `[skip ci]` in the release commit message prevents CI from triggering an infinite loop on the release commit.
- The `assets` array lists files that semantic-release commits back to the repo after a release.
- Plugin order matters — they execute sequentially.

**For multi-branch releases** (e.g., pre-releases), adjust `branches`:
```json
{
  "branches": [
    "main",
    { "name": "beta", "prerelease": true },
    { "name": "alpha", "prerelease": true }
  ]
}
```

**Verification:**
- [ ] `.releaserc.json` exists at project root
- [ ] `branches` matches the actual default branch name
- [ ] Plugin order is correct (analyzer first, github last)

### Phase 4: Initialize Husky & Git Hooks

Run husky's init command and add the `prepare` script:

```bash
npx husky init
```

This creates the `.husky/` directory and adds `"prepare": "husky"` to package.json scripts.

#### 4a. Add the commit-msg hook (required)

Write the commitlint hook:

```bash
echo 'npx --no -- commitlint --edit $1' > .husky/commit-msg
```

This validates every commit message against the commitlint rules before allowing the commit.

#### 4b. Add a pre-commit hook (optional, configurable)

**Ask the user what pre-commit hook they want.** Common options:

| Option | Command | Use when |
|--------|---------|----------|
| TypeScript build | `npm run build` | TypeScript projects — ensures every commit compiles |
| Lint | `npm run lint` | Projects with ESLint/Prettier — enforces code style |
| Test | `npm test` | Run test suite before every commit |
| Lint + Test | `npm run lint && npm test` | Both linting and testing |
| None | (delete `.husky/pre-commit`) | No pre-commit checks needed |

Write the chosen command to the pre-commit hook:

```bash
echo '<chosen-command>' > .husky/pre-commit
```

Or remove the default pre-commit hook if not needed:

```bash
rm .husky/pre-commit
```

**Verification:**
- [ ] `.husky/commit-msg` exists and contains commitlint command
- [ ] `.husky/pre-commit` configured or removed per user choice
- [ ] `"prepare": "husky"` exists in package.json scripts

### Phase 5: Add prepare script (if missing)

Check if `package.json` already has a `prepare` script. If `npx husky init` didn't add it, add manually:

```json
{
  "scripts": {
    "prepare": "husky"
  }
}
```

This ensures husky hooks are installed automatically when anyone runs `npm install`.

### Phase 6: Create Initial CHANGELOG

Create a starter `CHANGELOG.md`:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

Semantic-release will prepend entries to this file on each release.

### Phase 7: CI/CD Setup (GitHub Actions)

Create `.github/workflows/release.yml`:

```yaml
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
      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
      - run: npm ci
      - run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**Notes:**
- `fetch-depth: 0` is required — semantic-release needs full git history to analyze commits.
- `GITHUB_TOKEN` is provided automatically by GitHub Actions.
- `NPM_TOKEN` is only needed if publishing to npm. Set it in repo Settings > Secrets. Remove the line if not publishing to npm.
- Update `branches` if your default branch is not `main`.

**Verification:**
- [ ] `.github/workflows/release.yml` exists
- [ ] Branch name matches actual default branch
- [ ] `NPM_TOKEN` secret set (if publishing to npm)

### Phase 8: Verify Everything Works

Run these checks in order:

```bash
# 1. Verify husky hooks are installed
ls .husky/commit-msg

# 2. Test commitlint with a valid message
echo "feat: test message" | npx commitlint

# 3. Test commitlint with an invalid message (should fail)
echo "bad message" | npx commitlint

# 4. Test a real commit (should pass)
git add .
git commit -m "chore: set up semantic release and conventional commits"

# 5. Dry-run semantic-release (optional, requires CI token locally)
npx semantic-release --dry-run
```

**Expected results:**
- Step 2: exits 0, no errors
- Step 3: exits non-zero, shows validation errors
- Step 4: commit succeeds
- Step 5: shows what version would be released (if token available)

## Quick Reference

### Commit Message Cheat Sheet

```
feat(auth): add login endpoint          # minor bump
fix(api): handle null response           # patch bump
feat!: redesign user model               # MAJOR bump
docs: update readme                      # no release
test: add unit tests for parser          # no release
chore: update dependencies               # no release
refactor(core): simplify error handling  # no release

# With body and breaking change footer:
feat(api): add pagination support

Adds offset/limit parameters to all list endpoints.

BREAKING CHANGE: removed `page` parameter in favor of `offset`
```

### Files Created/Modified

| File | Action | Purpose |
|------|--------|---------|
| `commitlint.config.js` | Created | Commit message rules |
| `.releaserc.json` | Created | Semantic-release config |
| `.husky/commit-msg` | Created | Commitlint git hook |
| `.husky/pre-commit` | Created/Removed | Optional pre-commit hook |
| `CHANGELOG.md` | Created | Auto-updated changelog |
| `.github/workflows/release.yml` | Created | CI release pipeline |
| `package.json` | Modified | Added devDeps + prepare script |

## Troubleshooting

### Problem: Commitlint rejects valid-looking messages

**Cause:** Subject starts with uppercase or header exceeds 100 characters.

**Solution:** Ensure subject is lowercase and under 100 chars total. The `subject-case` rule enforces lowercase. Example: `feat: Add feature` fails, `feat: add feature` passes.

### Problem: Husky hooks don't run

**Cause:** Hooks not installed or `.husky/` directory missing.

**Solution:** Run `npx husky init` again, then re-create the hook files. Verify `"prepare": "husky"` is in package.json scripts. Run `npm install` to trigger the prepare script.

### Problem: Semantic-release creates duplicate changelog entries

**Cause:** The `body-max-line-length` commitlint rule conflicts with semantic-release's generated notes.

**Solution:** Set `'body-max-line-length': [0]` in commitlint config to disable body line length validation. This is already included in the config above.

### Problem: CI release creates infinite loop

**Cause:** Release commit triggers another CI run which tries to release again.

**Solution:** The `[skip ci]` tag in the `.releaserc.json` git commit message prevents this. Verify it's present in the `message` field of `@semantic-release/git` config.

### Problem: "ENOGITHEAD" or "EGITNOBRANCH" in CI

**Cause:** Shallow clone in CI doesn't have full git history.

**Solution:** Ensure `fetch-depth: 0` in the checkout step of GitHub Actions. This fetches full history needed for commit analysis.

## Examples

<Good>
Well-structured commit history:

```
feat(parser): add yaml frontmatter extraction
feat(cli): add interactive selection prompts
fix(writer): handle unicode in file paths
test: add e2e tests for compile workflow
chore(release): 1.0.0 [skip ci]
```

Each commit has a clear type, optional scope, lowercase subject. Semantic-release can analyze this and produce a clean changelog grouped by type.
</Good>

<Bad>
Unstructured commit history:

```
Added parser stuff
WIP
fix things
YAML support
updated tests and also fixed a bug and refactored
```

No types, no scopes, mixed concerns in single commits, uppercase, vague subjects. Commitlint would reject all of these. Semantic-release cannot derive meaningful changelogs.
</Bad>

## Integration

### setup-semantic-release + generate-skill

When creating new skills for projects that use semantic-release:
- The generated skill's commit conventions should align with the project's commitlint config
- Use `feat(skill-name):` for the initial skill commit so semantic-release triggers a minor bump

### setup-semantic-release + track-session

When setting up semantic-release as a multi-step task:
- Use track-session to track progress across the 8 setup phases
- Each phase has verification checkboxes that map well to session checkpoints

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Semantic Versioning (SemVer)](https://semver.org/)
- [semantic-release Documentation](https://semantic-release.gitbook.io/)
- [commitlint Documentation](https://commitlint.js.org/)
- [Husky Documentation](https://typicode.github.io/husky/)
