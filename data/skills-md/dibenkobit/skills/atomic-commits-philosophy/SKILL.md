---
name: atomic-commits-philosophy
description: Always make small, focused atomic commits. Apply when writing code, fixing bugs, refactoring, or completing any task that involves git changes.
author: dibenkobit
version: 1.0.0
license: MIT
---

# Atomic Commits Philosophy

You commit atomically. Always. This is not optional.

## Core Principle

**One commit = one logical change.**

After completing ANY unit of work — commit it immediately and separately. Don't accumulate changes. Don't "commit later". Don't bundle.

## What Triggers a Commit

| Completed work | Example |
|----------------|---------|
| Feature works end-to-end | `feat(auth): add password reset flow` |
| Bug is fixed and verified | `fix(cart): prevent duplicate items` |
| Refactor complete and tests pass | `refactor(api): extract validation logic` |
| Dependencies updated | `chore(deps): upgrade react to 18.2` |
| Tests added for a feature | `test(auth): add password reset tests` |
| Config change applied | `chore: configure eslint rules` |

## Commit Flow

1. Finish a unit of work
2. Stage ONLY related files: `git add <specific-files>`
3. Commit with clear message
4. Repeat

Never `git add .` unless ALL changes are related.

## What "Atomic" Means

✓ Can be reverted independently
✓ Has one clear purpose
✓ Message explains WHY, not just WHAT
✓ Related files only

## Anti-Patterns (Never Do This)

```
# WRONG — bundled unrelated changes
feat: add auth, fix typo, update deps

# WRONG — vague
fix: stuff

# WRONG — too big
feat: implement entire user module
```

## Right Patterns

```
feat(auth): add JWT token validation
fix(api): handle null response from /users
refactor(utils): extract date formatting to helper
chore(deps): upgrade react to 18.2
test(auth): add tests for token expiration
```

## Handling Large Tasks

Working on a big feature? Break by **logical boundaries**, not layers:

```
# WRONG — splitting by layer
feat(users): add User model
feat(users): add user service
feat(users): add user controller

# RIGHT — splitting by feature
feat(users): add user registration
feat(users): add user profile editing
feat(users): add password reset
```

Model + service + controller for one feature = one commit. They belong together.

## Priority for Format

1. User's explicit instructions (gitmoji, language, etc.)
2. Project config (.commitlintrc, .czrc)
3. Recent commits style (`git log --oneline -10`)
4. Conventional Commits (default)

## When NOT to Commit

- Work in progress that doesn't compile/run
- Debugging code (console.logs, etc.)
- Commented-out code you might need

Remove these before committing.

## Remember

Every time you touch git:
- Think "is this one logical change?"
- If multiple changes exist → split them
- Commit often, commit small
