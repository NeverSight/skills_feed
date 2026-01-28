---
name: git-flow
description: >
  Standard Git Flow branching model and lifecycle management strategy.
  Trigger: "create release", "hotfix", "branching strategy", "git flow".
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [project]
---

# Git Flow Strategy

## When to Use
- Deciding which branch to base work on.
- Creating a new Release or Hotfix.
- Merging strategies (Squash vs Merge Commit).

## 1. Branching Model

| Branch | Source | Merge Into | Lifespan | Purpose |
|--------|--------|------------|----------|---------|
| `main` | - | - | Infinite | Production-ready code. Stable. |
| `develop` | `main` | `main` | Infinite | Integration branch for next release. |
| `feature/*` | `develop` | `develop` | Short | New features (e.g., `feature/login-page`). |
| `release/*` | `develop` | `develop`, `main`| Medium | Release prep (e.g., `release/v1.0.0`). |
| `hotfix/*` | `main` | `develop`, `main`| Very Short| Production critical fixes (e.g., `hotfix/crash`). |

## 2. Feature Development

1.  **Start:** Update `develop` and branch off.
    ```bash
    git checkout develop && git pull origin develop
    git checkout -b feature/my-feature
    ```
2.  **Work:** Commit changes. Use `github` skill templates for PRs.
3.  **Finish:** PR into `develop`. Squash merge recommended.

## 3. Release Process

1.  **Start:** Branch off `develop` when features are frozen.
    ```bash
    git checkout develop
    git checkout -b release/v1.2.0
    ```
2.  **Work:** Bump versions, update changelogs, fix bugs. NO NEW FEATURES.
3.  **Finish:**
    - Merge into `main` (Tag this commit).
    - Merge into `develop` (Back-propagate fixes).
    - Delete `release/v1.2.0` branch.

## 4. Hotfixes

1.  **Start:** Branch off `main` (Production).
    ```bash
    git checkout main
    git checkout -b hotfix/critical-bug
    ```
2.  **Work:** Fix the critical bug. Minimal changes.
3.  **Finish:**
    - Merge into `main` (Tag this commit).
    - Merge into `develop`.
    - Delete `hotfix` branch.

## 5. Protocols
- **Never commit directly to `main` or `develop`.**
- **Keep history clean.** Use interactive rebase before PRs.
- **Tags are immutable.** Once pushed, do not change.
