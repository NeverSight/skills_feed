---
name: dub-flow
description: Use when turning staged changes into a DubStack branch, commit, and submitted PR stack with clear naming and user confirmation.
---

# DubStack PR Flow

Use this skill when a user asks to "create a PR" or "submit this" from staged changes.

## Goal

Produce a clean, reviewable stack operation with:
1. suggested branch name
2. suggested commit message
3. optional issue linkage
4. execution via `dub create` and `dub submit`

## Preconditions

- Current directory is a git repo.
- Staged changes exist (or user explicitly wants help staging).
- `gh` auth is configured for PR operations.

## Phase 1: Analyze Changes

Run:

```bash
git status --short
git diff --cached --stat
git diff --cached
git log --oneline -5
```

Capture:
- change scope (feature/fix/refactor/docs/test/chore)
- files and line impact
- likely branch scope and commit intent

If nothing is staged, stop and suggest one of:
- `git add <files>`
- `git add -A`
- use `dub create <name> -pm "..."` to stage interactively

## Phase 2: Propose Naming and Metadata

### Branch naming

Prefer:

```text
<type>/<short-kebab-scope>
```

Examples:
- `feat/auth-login`
- `fix/sync-parent-mismatch`
- `refactor/submit-body-builder`

### Commit message

Use conventional commits:

```text
type(scope): summary

optional body

optional issue link
```

If user provided issue ID (for example `A-35`), append:

```text
Completes A-35
```

### PR title/body guidance

Since `dub ss` manages stack submission, focus on high-quality commit messages and branch names first. If user asks to polish PR text, prepare concise title/body recommendations after submission.

## Phase 3: Confirm Before Execution

Present:
- suggested branch name
- suggested commit message
- what command you plan to run

Ask user to choose:
1. proceed
2. edit branch/message
3. cancel

## Phase 4: Execute

### Default path (stage all)

```bash
dub create <branch-name> -am "<commit-message>"
dub ss
```

### If user requested tracked-only staging

```bash
dub create <branch-name> -um "<commit-message>"
dub ss
```

### If user requested patch/hunk selection

```bash
dub create <branch-name> -pm "<commit-message>"
dub ss
```

### Optional: open resulting PR

```bash
dub pr
```

## Error Handling

- **No staged changes**: ask user to stage files or choose `-a/-u/-p` flow.
- **Branch exists already**: suggest alternate name.
- **GitHub auth errors**: prompt `gh auth login`.
- **Submit conflicts/restack issues**: run `dub restack`, resolve conflicts, then rerun `dub ss`.

## Success Output Template

```text
✅ DubStack submission complete
- Branch: <branch-name>
- Commit message: <message>
- Command(s): dub create ..., dub ss
- Next: dub pr (to open PR), dub log (to inspect stack)
```
