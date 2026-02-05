---
name: review-main
description: "Review branch changes vs main using a merge-base diff and return prioritized findings, risks, and cleanup opportunities. Use when asked to review changes against main/origin/main."
---

# Review Main

## Workflow
- Confirm base branch (default origin/main) and any focus paths.
- Fetch origin if needed, then compute merge base: `base=$(git merge-base HEAD origin/main)`.
- List changed files and review `git diff $base` (limit to focus paths if provided).
- Report prioritized findings (bugs, regressions, risks, unintended changes) with file/line refs.
- Call out simplification or cleanup opportunities and note missing tests.
