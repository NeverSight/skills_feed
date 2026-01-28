---
name: create-pr
description: "Create a high-quality pull request: branch, focused changes, lint/build, conventional commit, and a clear PR description with validation steps."
---

# Create a PR

## Goal
Produce a PR that’s easy to review and safe to merge:
- small, scoped changes
- green checks (lint/tests/build as appropriate)
- clear description + validation steps

## Workflow (checklist)
1) Confirm scope
   - Restate the goal and acceptance criteria.
   - Identify files likely to change; avoid unrelated cleanup.
2) Create a branch
   - Use a descriptive name: `fix/<topic>`, `feat/<topic>`, `chore/<topic>`.
3) Implement changes
   - Keep diffs focused; prefer small commits.
4) Run quality gates
   - Run the repo’s standard commands (lint/tests/build).
   - If `bun.lock` exists, prefer `bun lint` / `bun build`.
5) Commit
   - Prefer Conventional Commits: `fix: ...`, `feat: ...`, `chore: ...`.
6) Push + open PR
   - Always use GitHub CLI (`gh`) for PR workflows (e.g. `gh pr create --fill`).
   - If `gh` is not authenticated, run `gh auth login` (or `gh auth status` to check).
7) Fill in PR body
   - Use `references/pr-description-template.md`.

## Notes
- Don't force-push unless you're sure it's safe for collaborators.
- If the PR changes UX, include screenshots or a short GIF.
- Prefer `gh` for create/view/checks (e.g. `gh pr view`, `gh pr checks`).
