---
name: github
description: >
  GitHub interaction templates and standards.
  Trigger: "create issue", "open PR", "draft release note".
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [project]
---

# GitHub Skill

## When to Use
- Creating new Issues or Pull Requests.
- Writing Release Notes.
- Managing Labels and Milestones.

## Assets
- `assets/issue-template.md`: Standard bug/feature issue.
- `assets/pr-template.md`: Standard PR description.
- `assets/release-note.md`: Format for releases.
- `assets/contributing-template.md`: Guidelines for contributors.
- `assets/code-of-conduct-template.md`: Community standards.
- `assets/security-policy-template.md`: Security policy.

## Workflow
1.  **Issues:** Always use the template. Ensure reproduction steps are present for bugs.
2.  **PRs:** Link the PR to the Issue (`Fixes #123`).
3.  **Labels:** Use standard labels (`bug`, `enhancement`, `wontfix`).
