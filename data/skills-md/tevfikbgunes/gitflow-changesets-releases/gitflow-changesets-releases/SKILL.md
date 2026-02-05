---
name: gitflow-changesets-releases
description: Follow Gitflow with Changesets for branching, versioning, and releases. Use when (1) creating or merging feature, release, or hotfix branches, (2) writing conventional commits, (3) adding or versioning changesets, (4) running tests before PR or release, or (5) the user asks about releases, changelog, branching, or gitflow.
---

# Git, Changesets and Versioning Workflow

Gitflow with Changesets for version management and releases. Branches: `main` (production), `develop` (integration), `feat/*` / `fix/*` (from develop), `release/*` (to main), `hotfix/*` (from main).

## Branch Model

| Branch       | Purpose              | Created From | Merged To        |
|-------------|----------------------|--------------|------------------|
| `main`      | Production           | -            | `release/*`, `hotfix/*` |
| `develop`   | Integration          | `main`       | `feat/*`, `fix/*` |
| `feat/*`    | New features         | `develop`    | `develop`        |
| `fix/*`     | Bug fixes            | `develop`    | `develop`        |
| `release/*` | Release preparation  | `develop`    | `main`, `develop` |
| `hotfix/*`  | Critical prod fixes  | `main`       | `main`, `develop` |

## Quick Workflows

### Feature

Branch from `develop` → commit (conventional commits) → run `pnpm build && pnpm test:e2e` → `pnpm changeset` → commit changeset → push → PR to `develop`.

```bash
git checkout develop && git pull && git checkout -b feat/my-feature
# ... make changes, commit ...
pnpm build && pnpm test:e2e
pnpm changeset
git add .changeset/ && git commit -m "chore: add changeset"
git push -u origin feat/my-feature
```

### Release

From `develop`: create `release/vX.Y.Z` → `pnpm changeset:version` → commit → run tests → merge to `main` → tag → back-merge to `develop`.

```bash
git checkout develop && git pull && git checkout -b release/v1.1.0
pnpm changeset:version
git add package.json CHANGELOG.md .changeset/ pnpm-workspace.yaml && git commit -m "chore: release v1.1.0"
pnpm build && pnpm test:e2e
git checkout main && git pull && git merge --no-ff release/v1.1.0
git tag -a v1.1.0 -m "Release v1.1.0" && git push origin main --tags
git checkout develop && git merge --no-ff release/v1.1.0 && git push origin develop
```

### Hotfix

From `main`: create `hotfix/name` → fix → `pnpm changeset` (patch) → `pnpm changeset:version` → run tests → merge to `main` → tag → back-merge to `develop`.

```bash
git checkout main && git pull && git checkout -b hotfix/critical-bug
# fix, then:
git commit -am "fix(scope): fix critical bug"
pnpm changeset
pnpm changeset:version
git add package.json CHANGELOG.md .changeset/ && git commit -m "chore: bump version for hotfix"
pnpm build && pnpm test:e2e
git checkout main && git merge --no-ff hotfix/critical-bug
git tag -a v1.1.1 -m "Hotfix v1.1.1" && git push origin main --tags
git checkout develop && git merge --no-ff hotfix/critical-bug && git push origin develop
```

## Testing

Run **before** opening a PR and **before** merging release/hotfix to `main`:

```bash
pnpm build
pnpm test:e2e
```

## Version Bumps

| Change type       | Bump    | Example      |
|-------------------|---------|--------------|
| Breaking changes | `major` | 1.0.0 → 2.0.0 |
| New features     | `minor` | 1.0.0 → 1.1.0 |
| Bug fixes        | `patch` | 1.0.0 → 1.0.1 |

## References

Load when needed for detailed steps, prompts, or troubleshooting:

- **Initial setup (first time)**  
  See [references/initial-setup.md](references/initial-setup.md) for installing Changesets, config, and creating `develop`.

- **Feature development**  
  See [references/feature-development.md](references/feature-development.md) for full feature steps, commit types, and merge options.

- **Release process**  
  See [references/release-process.md](references/release-process.md) for full release steps, staging, and fixing bugs on release branch.

- **Hotfix process**  
  See [references/hotfix-process.md](references/hotfix-process.md) for full hotfix steps.

- **Conventional commits**  
  See [references/conventional-commits.md](references/conventional-commits.md) for format, types, rules, and examples.

- **Changesets and testing**  
  See [references/changesets-testing.md](references/changesets-testing.md) for changeset prompts, file format, and when/how to run tests.

- **Best practices**  
  See [references/best-practices.md](references/best-practices.md) for branch, commit, changeset, and release guidelines.

- **Troubleshooting**  
  See [references/troubleshooting.md](references/troubleshooting.md) for changeset not found, version not updating, CHANGELOG, merge conflicts, wrong bump, tag exists.
