---
name: pr-process
description: Prepare commits and pull requests for this repo following the PR template and Conventional Commits.
---

# PR Process

## Overview

Follow the repo PR template and semantic commit conventions. Use squash merges.

## Steps

1. Commit with Conventional Commits.
2. Fill `.github/PULL_REQUEST_TEMPLATE.md`.
3. Create PR with `gh pr create --body-file`.
4. Merge with squash, no branch delete.

## Resources

- Reference: `references/pr-process.md`
- Helper: `scripts/pr-create.sh`
- Checklist: `assets/pr-checklist.md`
