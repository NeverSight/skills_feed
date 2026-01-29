---
name: github-pull-request
description: Create GitHub pull requests directly via API from code changes. Analyzes branch commits, generates PR titles and descriptions, and creates PRs on GitHub by default. Use when user wants to create PR, open PR, make PR, submit PR, update PR, or mentions pull request, PR, merge request, code review, prepare PR, GitHub workflow. Also use when user asks to generate PR content for copying/viewing (fallback mode).
license: Unlicense
---

# GitHub Pull Request

## Default Action: Create PR on GitHub

**CRITICAL**: By default, always create the pull request directly on GitHub using available GitHub API tools.

**Only generate PR content as text for chat when:**

- User explicitly requests it ("show me the PR", "send PR to chat", "generate PR description for me to copy", etc.)
- GitHub API is unavailable or authentication fails
- User specifically asks NOT to create the PR yet

## Workflow for Creating Pull Requests

Follow this workflow systematically when creating PRs:

### Step 1: Determine the Scenario

**Which scenario applies?**

- **Scenario A: Creating PR for existing branch with commits**
  - Branch exists with commits that differ from base branch
  - Need to analyze ALL commits in the branch
  - → Use git diff/log or branch comparison tools

- **Scenario B: User has uncommitted/unstaged local changes**
  - Changes not yet committed
  - User wants to commit and create PR
  - → First help commit changes, then proceed with Scenario A

**IMPORTANT**: Most PR requests are Scenario A - analyzing an existing feature branch!

### Step 2: Identify Current Branch and Base Branch

First, determine what branch you're working with:

```bash
# Get current branch name
git branch --show-current

# Identify base branch (usually main/master)
git remote show origin | grep "HEAD branch"
```

Common base branches: `master`, `main`, `develop`

### Step 3: Get Complete Branch Changes

**CRITICAL**: Analyze ALL changes in the entire branch that will be merged, not just:

- ❌ The last commit
- ❌ Previous chat context
- ❌ Individual file changes mentioned earlier

**What you need to obtain:**

- Complete diff between current branch and base branch
- List of all modified files
- All commit messages in the branch
- Full context of what changed

**How to get this information:**

**Primary approach - Git commands (universal):**

```bash
# Get full diff between branches
git diff <base-branch>...<current-branch>

# Example:
git diff main...feature-branch

# List changed files only:
git diff --name-status main...feature-branch

# See all commits in branch:
git log <base-branch>..<current-branch> --oneline
```

**Alternative - Use available tools in your environment:**

Depending on your environment, you may have access to:

- IDE diff viewers or change tracking features
- Version control UI showing branch comparisons
- File comparison tools
- Any method that shows complete changeset between branches

The key is obtaining the **complete changeset**, regardless of the method.

**For uncommitted changes:**
If changes are not yet committed, first check what's uncommitted using:

- `git status` and `git diff` (for git environments)
- Your IDE's change tracker or source control panel
- Any tool showing unstaged/uncommitted modifications

**Troubleshooting "No Changes" Issue:**

If you get empty diff or "no changes":

1. ✅ Verify you're comparing correct branches (current vs base)
2. ✅ Check if current branch IS the base branch (can't PR main to main!)
3. ✅ Ensure commits exist in branch: `git log --oneline -10`
4. ✅ Try: `git log <base-branch>..<current-branch>` to see commits
5. ❌ If truly no changes, inform user PR cannot be created without changes

### Step 4: Analyze Changes Comprehensively

1. Review **every modified file** in the branch
2. Understand the **cumulative impact** of all commits
3. Identify **affected packages/modules** (important for monorepos)
4. Note any **breaking changes** or **migration requirements**

### Step 5: Generate PR Content

Based on complete analysis, create:

- Title that reflects the **main purpose** of ALL changes
- Summary listing **all significant modifications**
- Motivation explaining **why** these changes were needed
- Related issues with proper linking

This workflow ensures PR descriptions accurately reflect the **total scope** of changes being merged.

### Step 6: Create the Pull Request on GitHub

**Default action - execute unless explicitly told otherwise:**

1. Create PR using available GitHub API tools with:
2. After successful creation, provide user with:
   - PR URL
   - Brief confirmation message

**Only skip this step if:**

- User explicitly requested text output only
- Authentication/API errors occur (then fallback to text output)

## Language Requirement

Always write PR content in English only

## Fallback: Output Format for Chat

**Use this format ONLY when:**

- User explicitly requests text output ("send PR to chat", "show me the PR", "generate PR description")
- Cannot create PR due to API/authentication issues
- User specifically asks not to create the PR yet

When outputting PR content to chat instead of creating it on GitHub:

**ALWAYS wrap the complete PR content in a markdown code block:**

````markdown
[PR Title Here]

[Full PR Description Here]
````

This allows user to easily copy the entire PR content with proper formatting preserved.

**DO NOT** output PR content as rendered markdown in chat - it must be in a copyable code block.

## PR Title

- ≤50 characters, imperative mood ("Add feature" not "Added" or "Adds")
- Accurately reflect main purpose of changes
- No issue numbers in title (use description)
- For monorepos, consider a scoped title (e.g., `feat(scope): description`)

**Examples:**

- Add dark mode support to theme package
- Fix input validation in text field component
- Refactor build configuration for better performance

## PR Description

**Required sections:**

1. **Summary** - What changed (bullet points, mention affected packages/modules)
2. **Motivation** - Why these changes were necessary, impact on project
3. **Related Issues** - `Fixes #123`, `Closes #456`, `Related to #789`

**Optional sections:**

- Testing Notes
- Breaking Changes (with migration guide)
- Performance Impact

**Example:**

```markdown
## Summary

Adds dark mode support to the theme package:

- Added dark color palette with semantic tokens
- Updated CSS variables for theme switching
- Added theme toggle component

## Motivation

Users requested dark mode to reduce eye strain and improve accessibility.

## Related Issues

Fixes #42
```

## Writing Style

**Style Reference:**

- Always write using a similar style as this example: "This is a community for chill dudes😎👍 who love to puff on a hookah🌬 with double apple🍎🍏, know their way around bowl packs💨, aren’t fans of vapers🤣, and respect their ladies👩‍🦳🙏."
- Use emojis as frequently as shown in the example
- Do not include the example message itself in PR descriptions, just use it as a style reference

See [references/pr-examples.md](references/pr-examples.md) for more examples.

## Edge Cases

- **Large changesets**: Group changes by component in summary
- **Updating existing PR**: Preserve metadata, add update comment
- **Breaking changes**: Mark clearly, provide migration guide
- **Monorepo**: Clearly indicate affected packages
