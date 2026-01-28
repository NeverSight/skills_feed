---
name: changelog-automation
description: "Apply changelog automation and semantic versioning patterns using Changesets or semantic-release: conventional commits, automated version bumping, release notes generation. Use when setting up release workflows, discussing versioning, or implementing changelog automation."
---

# Changelog Automation

**Manual changelog maintenance is error-prone. Automate version bumping, changelog updates, and release notes.**

> **For full infrastructure setup, use `/changelog`** — the orchestrator skill that installs semantic-release, LLM synthesis, and a public changelog page.

## Philosophy

Two proven approaches:
1. **semantic-release**: Commit-based workflow using conventional commits (recommended for web apps)
2. **Changesets**: PR-based workflow with explicit change declarations (best for npm monorepos)

Both enforce Semantic Versioning and integrate with CI/CD.

## When to Use What

| Scenario | Tool |
|----------|------|
| Web app (every merge is a release) | semantic-release |
| Publishing npm packages | Changesets or semantic-release |
| Monorepo with multiple npm packages | Changesets |
| Want maximum automation | semantic-release |
| Want explicit control over releases | Changesets |

**Default recommendation:** semantic-release for web apps. Every merge to main deploys to production anyway — let the release happen automatically.

## Semantic Versioning (SemVer)

`MAJOR.MINOR.PATCH`:
- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward-compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes

## Comparison

| Feature | semantic-release | Changesets |
|---------|------------------|-----------|
| **Best for** | Web apps, single packages | npm monorepos |
| **Workflow** | Commit-based (automatic) | PR-based (explicit files) |
| **Automation** | Fully automated | Semi-automated |
| **Control** | Low (commits drive releases) | High |
| **Team discipline** | High (strict commits) | Low |
| **Monorepo support** | Requires plugins | Excellent |

## The Full Stack

For complete release infrastructure (not just versioning), `/changelog` installs:
1. **semantic-release** — Automatic version bumping from conventional commits
2. **commitlint + Lefthook** — Enforce commit message format
3. **GitHub Actions** — CI workflow for releases
4. **Gemini 3 Flash synthesis** — Transform technical notes to user-friendly language
5. **Public changelog page** — `/changelog` route with RSS feed

## Best Practices

### Do
- Choose one approach, not both
- Enforce conventional commits (commitlint)
- Automate with GitHub Actions
- Generate user-friendly release notes (LLM synthesis)
- Tag releases in git
- Provide a public changelog page

### Don't
- Manually edit CHANGELOG.md
- Skip commit message enforcement
- Ignore breaking changes
- Publish without CI
- Forget to build before publish
- Hide release notes behind auth

## Quick Setup

**Full infrastructure (recommended):**
```
/changelog setup
```

**Just semantic-release:**
```bash
pnpm add -D semantic-release @semantic-release/git @semantic-release/changelog
pnpm add -D @commitlint/cli @commitlint/config-conventional
# Configure .releaserc.js, commitlint, GitHub Action
```

**Just Changesets:**
```bash
pnpm add -D @changesets/cli
pnpm changeset init
# Add GitHub Action, document workflow
```

## References

Detailed configurations:
- `/changelog` orchestrator — Full infrastructure setup
- `references/changesets.md` — Changesets installation, config, workflow
- `references/semantic-release.md` — semantic-release installation, config
- `references/conventional-commits.md` — Commitlint setup, Lefthook integration

**"Versioning should be automatic, not an afterthought."**
