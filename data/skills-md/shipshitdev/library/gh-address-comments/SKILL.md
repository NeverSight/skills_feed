---
name: gh-address-comments
description: Help address review or issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.
---

# GH Address Comments

Use this skill when a user wants help resolving PR review or issue comments via the GitHub CLI.

## Workflow

1) Verify auth:
   - `gh auth status -h github.com`
   - If not logged in, ask the user to run `gh auth login`.
2) Identify the PR:
   - `gh pr view --json number,title,url`
   - If no PR is found, ask for the PR URL.
3) Collect comments:
   - Review comments: `gh api repos/{owner}/{repo}/pulls/{number}/comments`
   - Issue comments: `gh api repos/{owner}/{repo}/issues/{number}/comments`
4) Summarize each thread and map to code changes.
5) Propose fixes and get user approval before pushing changes.
6) Draft reply text for each thread and ask before posting to GitHub.

## Notes

- Prefer quoting exact comment text in your summary.
- Keep replies short and specific to the change.
