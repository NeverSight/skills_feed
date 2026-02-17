---
name: ship-it
description: >-
  Create branch, commit, push, and open a pull request.
  Use when: user says "ship it", "ship this", "create a PR", "open a PR",
  "push and PR", or wants to go from uncommitted changes to an open pull request.
license: MIT
compatibility: Requires git and GitHub CLI (gh) with authentication
metadata:
  author: Gregory Murray
  repository: github.com/whatifwedigdeeper/agent-skills
  version: "0.3"
---

# Ship: Branch, Commit, Push & PR

## Arguments

Optional text to derive branch name, commit message, or PR title (e.g. `fix login timeout`).

If `$ARGUMENTS` is `help`, `--help`, `-h`, or `?`, skip the workflow and read [references/options.md](references/options.md).

## Process

### 1. Preflight Checks

```bash
git status
git branch --show-current
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
# Fallback if origin/HEAD is unset
if [ -z "$DEFAULT_BRANCH" ]; then
  DEFAULT_BRANCH=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | sed 's/.*: //')
fi
git diff --stat
git diff --stat --cached
gh auth status
```

Determine:
- What is the default branch? (detect from remote ref, do not assume `main`)
- Are there changes to commit? (If no staged or unstaged changes, abort with message)
- Are we on the default branch? (If so, need to create a branch)
- Are we already on a feature branch?
- Is `gh` CLI installed and authenticated? (If not, abort: "Install and authenticate the GitHub CLI: https://cli.github.com")
- Are we in detached HEAD state? (If so, create a branch before proceeding)

### 2. Create Branch (if needed)

Skip this step if already on a feature branch — use the current branch.

If on the default branch or in detached HEAD, create and switch to a new branch:

```bash
git checkout -b <branch-name>
```

**Branch naming:**
- If user provided `$ARGUMENTS`, derive branch name from it (kebab-case, e.g. `fix/handle-null-response`)
- Otherwise, analyze the changes and generate a descriptive branch name
- Use prefixes: `feat/`, `fix/`, `refactor/`, `docs/`, `chore/`, `test/` based on change type
- If a remote branch with the same name already exists, append a short suffix (e.g. `-2`)

### 3. Stage & Commit

Stage specific files rather than using `git add -A`.

```bash
git add <file1> <file2> ...
git diff --cached --name-only
```

Analyze the diff and generate a conventional commit message. If user provided `$ARGUMENTS` that looks like a commit message, use it directly.

```bash
git commit -m "type: description"
```

**Commit fallbacks:**
- If commit fails due to GPG signing errors (sandbox or keyring issues), retry with `--no-gpg-sign`
- If heredoc syntax (`$(cat <<'EOF'...)`) fails with "can't create temp file", use multiple `-m` flags instead (e.g. `git commit -m "subject" -m "body"`)

### 4. Push

```bash
git push -u origin <branch-name>
```

If push fails due to branch protection or permissions, report the error to the user and stop.

### 5. Create Pull Request

Gather context for the PR description:

```bash
git log <default-branch>..HEAD --oneline
git diff <default-branch>..HEAD --stat
```

Check for an existing PR on this branch:

```bash
if gh pr view --json url,title,body > /dev/null 2>&1; then
  gh pr view --json url,title,body
fi
```

If a PR already exists:
1. Compare the current PR title and body against all commits on the branch (`git log <default-branch>..HEAD --oneline`)
2. If the title or body no longer reflects the full set of changes (e.g. new commits were added), update them with `gh pr edit <number> --title "<new title>" --body "<new body>"`
3. Report the PR URL and any updates made, then jump to Step 6

Otherwise, create the PR:

```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
- [2-3 bullet points describing the changes]

## Test Plan
- [ ] [How to test these changes]

---
Generated with [agent name and link, per agent conventions]
EOF
)"
```

If `gh pr create` fails, report the error to the user (common causes: missing repo permissions, network issues, branch protection rules).

**Title:** If user provided `$ARGUMENTS`, use as PR title. Otherwise generate from the commit(s).

### 6. Report

Output:
- Branch name
- Commit hash and message
- PR URL

## Rules

- Never commit files that look like secrets (.env, credentials, keys, tokens, private keys, build artifacts)
- If there are merge conflicts with the default branch, warn the user before creating the PR
- **No sandbox**: This skill uses branch-based isolation. Git and `gh` commands require access to the macOS keyring and credential helpers.
