---
name: ship
description: "Commit, push, and create a PR in one step. Use when the user says 'ship', 'ship it', '/ship', '提交PR', '发PR', or wants to commit + push + create a pull request in a single action."
version: "1.0.0"
metadata:
  author: qiaoshouqing
---

# Ship - Commit, Push & Create PR in One Step

Ship your changes with a single command. Auto-generates commit messages, pushes to remote, and creates a pull request with a detailed description.

## When to Use

- User says "ship", "ship it", or "/ship"
- User says "提交PR", "发PR", "提交并创建PR"
- User wants to commit all changes, push, and open a PR in one action
- User wants a draft PR (mentions "draft", "--draft", or "草稿")

## Prerequisites

```bash
git --version || { echo "ERROR: git not found"; exit 1; }
gh --version || { echo "ERROR: gh CLI not found. Install: brew install gh"; exit 1; }
gh auth status || { echo "ERROR: gh not authenticated. Run: gh auth login"; exit 1; }
git rev-parse --is-inside-work-tree || { echo "ERROR: Not a git repository"; exit 1; }
git remote -v | grep -q origin || { echo "ERROR: No remote 'origin' configured"; exit 1; }
```

If any prerequisite fails, report the error with the fix command and stop.

## Instructions for Agent

### Step 0: Check Prerequisites

Run the prerequisite checks above. If any fail, inform the user of the specific error and provide the fix command. Do NOT proceed until all pass.

### Step 1: Analyze Current State

```bash
# Check for changes
git status --short

# Get current branch
git branch --show-current

# Get diff stats for commit message generation
git diff --stat
git diff --cached --stat

# Check recent commit style
git log --oneline -5
```

**If no changes exist** (git status --short is empty AND no staged changes), inform the user "Nothing to ship - working tree is clean" and stop.

### Step 2: Smart Branch Handling

```bash
CURRENT_BRANCH=$(git branch --show-current)
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
```

**If on main/master/default branch:**
1. Generate a descriptive branch name from the changes: `<type>/<short-slug>`
2. Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `style`, `test`
3. Create and switch to the new branch:

```bash
git checkout -b "<type>/<slug>"
```

**If already on a feature branch:** Continue on the current branch.

**If on detached HEAD:** Inform user and suggest creating a branch first. Stop.

### Step 3: Stage All Changes and Generate Commit Message

```bash
git add -A
```

Generate a commit message by analyzing the staged diff:

1. Run `git diff --cached` to understand the changes
2. Determine the commit type from the changes:

| Changes Pattern | Type |
|----------------|------|
| New files/features added | `feat` |
| Bug fix patterns | `fix` |
| Restructuring without behavior change | `refactor` |
| Documentation/comments only | `docs` |
| Test files only | `test` |
| Config/build files | `chore` |
| CSS/styling only | `style` |

3. Format: `<type>(<scope>): <description>` (subject line < 72 chars)
4. Add a body paragraph if changes are complex
5. Do NOT ask user for confirmation - auto-generate and proceed

### Step 4: Commit and Push

```bash
# Commit with the generated message (use HEREDOC for multi-line)
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<optional body>
EOF
)"

# Push with upstream tracking
git push -u origin "$(git branch --show-current)"
```

**If push is rejected** (non-fast-forward): Inform user and suggest `git pull --rebase origin <branch>`. Do NOT force push.

### Step 5: Create PR

Detect draft mode: If user mentioned "draft", "--draft", or "草稿", add `--draft` flag.

```bash
# Determine base branch
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")

# Check if PR already exists
EXISTING_PR=$(gh pr list --head "$(git branch --show-current)" --json url --jq '.[0].url' 2>/dev/null)
```

**If PR already exists:** Inform user and show the existing PR URL. Stop.

**Otherwise, create the PR:**

```bash
gh pr create \
  --base "$BASE_BRANCH" \
  --title "<PR title>" \
  --body "$(cat <<'EOF'
## Summary

<1-3 sentence overview of what this PR does and why>

## Changes

| File | Change |
|------|--------|
| `path/to/file` | Description of change |
| ... | ... |

## Impact Analysis

- **Scope**: <What areas are affected>
- **Risk**: <Low/Medium/High>
- **Breaking changes**: <None or description>
- **Dependencies**: <New deps added, if any>

## Test Plan

- [ ] <Specific test step>
- [ ] Verify no regressions

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" [--draft]
```

**PR body generation rules:**
- **Summary**: Synthesize from the commit message and diff context
- **Changes table**: List every changed file with a one-line description
- **Impact Analysis**: Assess scope, risk level, breaking changes based on the diff
- **Test Plan**: Generate actionable test steps relevant to the changes

### Step 6: Report Result

Display the final result:

```
✅ Shipped!
   Branch: <branch-name>
   Commit: <short-hash> - <commit subject>
   PR: <pr-url> [draft]
   Files: <n> changed (+<additions>, -<deletions>)
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `git: command not found` | Git not installed | `brew install git` or `xcode-select --install` |
| `gh: command not found` | GitHub CLI not installed | `brew install gh` |
| `gh auth status` fails | Not authenticated | `gh auth login` |
| `not a git repository` | Not in a repo | Navigate to a git repository |
| `No remote 'origin'` | No remote configured | `git remote add origin <url>` |
| `rejected - non-fast-forward` | Remote has new changes | `git pull --rebase origin <branch>` then retry |
| `gh pr create` 422 error | PR already exists | Show existing PR URL |
| `permission denied` | No write access | Check repo permissions |
| `branch already exists` on remote | Name conflict | Append suffix: `feat/slug-2` |
| Detached HEAD | Not on a branch | `git checkout -b <branch-name>` first |

## Response Guidelines

1. **No confirmation prompts** - "Ship" is the confirmation. Execute immediately.
2. **Show progress** - Display each step as it completes.
3. **Auto-generate everything** - Commit message, branch name, PR title, PR body.
4. **Always end with PR URL** - The clickable PR link is the key output.
5. **Handle errors gracefully** - Report what failed and how to fix it.
6. **Respect --draft** - Create as draft PR when requested.
7. **Never force push** - Suggest rebase on rejection.
8. **Never discard changes** - Do not reset, stash, or drop user's work.
