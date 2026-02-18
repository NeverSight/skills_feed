---
name: git-best-practices
description: Git workflow patterns for commits, branching, PRs, and history management across heterogeneous repositories. Use when creating commits, managing branches, opening pull requests, or rewriting history. Do not use for non-git implementation tasks or repo-specific release policy decisions without repository documentation.
---

# Git Best Practices

## Always Active Principles

When this skill is loaded, follow these directives for all git operations:

1. **Discover before acting** — run branch discovery to determine the repo's default and production branches before branching, merging, or opening PRs
2. **Conventional commits** — every commit uses `type(scope): description` format
3. **Stage explicitly** — add files by name so only intended changes are committed
4. **Protect shared history** — use `--force-with-lease` for force pushes; confirm with the user before any force push

## Agent Git Workflow

Follow this sequence when performing git operations:

1. **Check state** — run `git status` and `git diff HEAD`; output: working tree and unstaged/staged delta
2. **Discover branches** — identify and store default/current/(optional) production branch names (see Branch Discovery)
3. **Stage by name** — `git add path/to/file` for each file; verify with `git status`
4. **Write a conventional commit** — `type(scope): description` with optional body
5. **Push safely** — use regular push by default; use `git push --force-with-lease origin {branch}` only for rewritten history and only after user confirmation

### Checkpoint Commits

Agents may create WIP checkpoint commits during long-running tasks. These are development artifacts, cleaned up before PR.

- Prefix with `wip:` or use standard conventional commit format
- Keep changes logically grouped even in WIP state
- Run `/rewrite-history` before opening a PR to craft a clean narrative

### Commit Discipline

- Stage files explicitly by name: `git add src/auth.ts src/auth.test.ts`
- Verify staged content with `git status` before committing
- Keep secrets, `.env` files, credentials, and large binaries out of commits — warn the user if staged files look sensitive
- Target one logical change per commit in final PR-ready state

### Force Push

Use `--force-with-lease` exclusively to protect against overwriting upstream changes:

```bash
git push --force-with-lease origin feat/my-branch
```

Always confirm with the user before any force push, regardless of branch.

## Conventional Commits

Format: `type(scope): description`

Subject line rules:
- Lowercase, imperative mood, no trailing period
- Under 72 characters
- Scope is optional but preferred when a clear subsystem exists

Common types:

| Type | Use for |
|------|---------|
| `feat` | New functionality |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Restructuring without behavior change |
| `perf` | Performance improvement |
| `chore` | Maintenance, dependencies, tooling |
| `test` | Adding or updating tests |
| `ci` | CI/CD pipeline changes |
| `build` | Build system changes |
| `style` | Formatting, whitespace (no logic change) |

### Commit Bodies

Body is optional — only add one when the change is genuinely non-obvious. The subject line carries the "what"; the body explains "why."

Add a body when:
- The motivation or tradeoff is non-obvious
- Multi-part changes benefit from a bullet list
- External context is needed (links, issue references, root cause)

### Examples

<examples>

<example name="simple-fix">
Single-line fix, no body needed:

```
fix(shell): restore Alt+F terminal navigation
```
</example>

<example name="scoped-with-body">
Non-obvious fix with body explaining root cause:

```
fix(shell): use HOMEBREW_PREFIX to avoid path_helper breaking plugins in login shells

macOS path_helper reorders PATH in login shells, putting /usr/local/bin
before /opt/homebrew/bin. This caused `brew --prefix` to resolve the stale
Intel Homebrew, so fzf, zsh-autosuggestions, and zsh-syntax-highlighting
all silently failed to load in Ghostty (which spawns login shells).

Use the HOMEBREW_PREFIX env var (set by brew shellenv in .zshenv) instead
of calling `brew --prefix` — it survives path_helper and is faster.
```
</example>

<example name="multi-part-feature">
Feature with bullet-list body for multi-part changes:

```
feat(install): add claude bootstrap runtime management

- migrate Claude defaults to declarative files under claude/defaults
- add claude-bootstrap check/fix/uninstall with backup-first migration
- stop stowing full claude/codex runtime trees and tighten drift checks
```
</example>

<example name="ticket-linked">
Monorepo commit with ticket reference in branch and scope:

```
fix(pool-party): handle stale settlement state on reconnect

PoolSettlement contract stays in pending state when the participant
disconnects mid-settlement. Check settlement timestamp and expire
stale entries on reconnect.

Fixes SEND-718
```
</example>

<example name="submodule-bump">
Submodule update with downstream commit info:

```
chore(submodule): update claude-code

Bump claude-code to 88d0c75 (feat(skills): add tiltup, specalign, and e2e skills).
```

For trivial bumps, `bump` or `bump claude-code submodule` is acceptable.
</example>

<example name="breaking-change">
Breaking change using `!` suffix:

```
refactor(api)!: change auth endpoint response format

The /auth/token endpoint now returns { access_token, expires_in }
instead of { token, expiry }. All clients must update their parsers.
```
</example>

</examples>

## Branch Discovery

Before branching or opening a PR, discover the repo's branch topology. Run these commands and store the results:

```bash
# Default branch (PR target for most repos)
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'

# Current branch
git branch --show-current

# Production branch (if different from default)
git branch -r --list 'origin/main' 'origin/master' 'origin/production'
```

**Fallback when `gh` is unavailable or the repo has no remote:**

```bash
# Infer default branch from local refs
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'

# Last resort: check local branches and fail loudly if unknown
if git rev-parse --verify main >/dev/null 2>&1; then
  echo main
elif git rev-parse --verify master >/dev/null 2>&1; then
  echo master
else
  echo "ERROR: unable to determine default branch (main/master not found)." >&2
  exit 1
fi
```

Store the discovered branch name and reference it throughout. Use the actual branch name in all subsequent commands.

### Branch Naming

Use repository branch naming conventions first. If no convention is documented, use:

Format: `type/description-TICKET-ID`

Examples:
- `feat/add-login-SEND-77`
- `fix/pool-party-stall-SEN-68`
- `chore/update-deps`
- `hotfix/auth-bypass`

Include the ticket ID when an issue exists. Omit when there is no ticket.

### Branch Flow

Use repository branch flow policy first. If policy is undocumented, a common baseline is:

```
{production-branch} (production deploys)
 └── {default-branch} (staging/testnet deploys, PR target)
      ├── feat/add-feature-TICKET
      ├── fix/bug-description-TICKET
      └── hotfix/* (branches off production branch for hotfixes)
```

- Feature and fix branches start from the default branch
- Hotfix branches start from the production branch
- PRs target the default branch unless the repo uses a single-branch flow
- When default branch and production branch are the same, all PRs target that branch directly

### Merge Strategy

Use repository merge policy first (required in many organizations).

If no policy exists, these defaults are reasonable:

| PR target | Strategy | Rationale |
|-----------|----------|-----------|
| Feature → default branch | Squash merge | Clean history, one commit per feature |
| Default → production | Merge commit | Preserves the release boundary; visible deploy points |
| Hotfix → production | Squash merge | Single atomic fix on production |

## PR Workflow

### Sizing

Pragmatic sizing over arbitrary limits. Each commit tells a clear story regardless of PR size. A PR should be reviewable as a coherent unit — if a reviewer cannot hold the full change in their head, consider splitting.

### PR Creation

Use repo-native PR tooling (`gh pr create`, GitLab CLI, or web UI) with:
- Short title under 70 characters
- Summary section with 1-3 bullet points
- Test plan as a bulleted checklist

### History Rewriting Before PR

For branches with messy WIP history, use `/rewrite-history` to:
1. Backup the branch
2. Reset to the base branch tip
3. Recommit changes as a clean narrative sequence
4. Verify byte-for-byte match with backup
5. Confirm with the user before force-pushing rewritten history
6. Open PR with link to backup branch

Each rewritten commit introduces one coherent idea, building on the previous — like a tutorial teaching the reader how the feature was built.
