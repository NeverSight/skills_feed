---
name: pr-summary
description: "Generate a PR title and description from the branch diff vs main. Use when asked for a PR summary or PR description."
---

# PR Summary

## Workflow
- Fetch origin if needed and compute merge base: `base=$(git merge-base HEAD origin/main)`.
- Review `git diff --stat $base` and key file diffs.
- Draft a PR title and short body that explain what changed and why.
- Include tests run or targeted test recommendations and any risks.
