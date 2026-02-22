---
name: session-pr
description: Commit changes from the current Claude Code session to a new branch, push to GitHub, and open a PR. Use when the user wants to save their work as a PR, submit session changes, or create a pull request for what was done in this session.
argument-hint: [branch-name]
---

# Session PR

Create a PR from the current session's changes.

## Workflow

1. Run `git status` to see current changes (never use -uall flag)
2. Run `git diff` to understand what changed
3. Run `git log -5 --oneline` to see recent commit style

4. Create and checkout a new branch:
   - If user provided $ARGUMENTS, use that as branch name
   - Otherwise, generate a descriptive branch name from the changes (e.g., `fix-auth-bug`, `add-user-validation`)

5. Stage only the files that were modified in this session (prefer specific files over `git add -A`)

6. Create a commit with a clear message summarizing the session's work:
   - End with: `Co-Authored-By: Claude <noreply@anthropic.com>`

7. Push the branch with `-u` flag

8. If the PR touches frontend code (e.g., files in `app/`, components, routes, styles), capture a screenshot of the relevant UI change and include it in the PR body using the `github-image-upload` skill.

9. Create PR using:
```bash
gh pr create --title "..." --body "$(cat <<'EOF'
## Summary
<bullet points of changes>

## Test plan
<how to verify>

<screenshot if frontend changes>

Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

10. Return the PR URL to the user
