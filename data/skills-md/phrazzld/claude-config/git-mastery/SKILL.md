---
name: git-mastery
user-invocable: false
description: |
  Git workflow enforcement and best practices. Use when:
  - Writing commit messages or reviewing commits
  - Creating branches or choosing merge strategies
  - Setting up CI/CD pipelines with git operations
  - Resolving merge conflicts or rebasing
  - Configuring repository settings or git hooks
  - Optimizing large repository performance
  Keywords: git, commit, branch, merge, rebase, PR, pull request, trunk-based,
  conventional commits, atomic commits, git hooks, CODEOWNERS
---

# Git Mastery

Enforce distributed-first, async-friendly git workflows with automated quality gates.

## Commits: Atomic + Conventional

**Every commit must be:**
- Single logical change (use `git add -p` for selective staging)
- Complete (code + tests + docs together)
- Independently buildable and testable
- Describable without "and" in subject

**Format:** `type(scope): subject` (50 chars max)
```
feat(auth): add OAuth2 login flow
fix(api): handle null response in user endpoint
docs(readme): add deployment instructions
refactor(db): extract query builder
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

BREAKING CHANGE: Add footer `BREAKING CHANGE: description` → triggers MAJOR version.

## Branches: Short-Lived + Typed

**Naming:** `type/issue-description` (lowercase, hyphens, <60 chars)
```
feature/123-oauth-login
fix/456-null-pointer-api
hotfix/critical-auth-bypass
```

**Rules:**
- Max 3 days old (escalate if longer)
- Delete immediately after merge
- Rebase onto main daily: `git pull --rebase origin main`
- Never push directly to main

## Merge Strategy (Algorithmic)

| Condition | Strategy |
|-----------|----------|
| <3 days, single author, atomic | **Rebase** (linear history) |
| Multi-author or external PR | **Merge** (preserve context) |
| Many fixup/experimental commits | **Squash** (clean history) |

Main branch: fast-forward only (`git config merge.ff only`).

## PR Workflow

1. CI passes before human review (lint, type-check, test, security)
2. CODEOWNERS auto-assigns reviewers
3. 1-2 approvals required
4. Squash fixup commits before merge
5. Branch auto-deleted on merge

**Context-rich PRs:** Include motivation, alternatives considered, areas of concern.

## Performance (Large Repos)

Enable commit-graph:
```bash
git config core.commitGraph true
git config gc.writeCommitGraph true
```

Clone optimization:
```bash
git clone --filter=blob:none URL  # Partial clone
git sparse-checkout set src/      # Only needed paths
```

Large files (>10MB): Use Git LFS.

## Anti-Patterns

- Mixed commits ("fix auth and update logging")
- Long-lived branches (>1 week without escalation)
- Manual merge strategy choice (use decision tree)
- Requiring sync coordination across timezones
- Large binary files in git history
- WIP/fix typo commits in main history

## References

- [conflict-resolution.md](references/conflict-resolution.md) - Distributed async conflict patterns
- [feature-flags.md](references/feature-flags.md) - Flag-driven development for long features
- [release-automation.md](references/release-automation.md) - Semantic versioning automation

## Commit Conventions

See `references/commit-conventions.md` for detailed commit message standards including:
- Conventional commit format (type(scope): subject)
- Imperative mood rules
- Body and footer conventions
- Breaking change format
