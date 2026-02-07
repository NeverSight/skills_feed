---
name: create-pr
description: Create Pull Request. This skill should be used when creating a pull request from the current branch. It analyzes changes between the current branch and main branch, then generates an appropriate title and description following Conventional Commits format.
---

# Create Pull Request

## Overview

This skill analyzes the differences between the current branch and the main branch, generating an appropriate Pull Request title and description. It follows Conventional Commits format and provides reviewers with sufficient context to begin code review.

## Workflow

### 1. Analyze Changes

First, analyze the differences between the current branch and the main branch in detail.

**Performance Optimization (Parallel Fan-Out Pattern)**

The following 4 git commands have no interdependencies and can be executed in parallel. By running them concurrently, latency can be reduced by approximately 75% compared to sequential execution.

| Command | Purpose |
|---------|---------|
| `git diff main...HEAD --name-only` | List of changed files |
| `git diff main...HEAD --stat` | Change statistics |
| `git log main..HEAD --pretty=format:"- %s"` | Commit history |
| `git diff main...HEAD --unified=3` | Detailed diff |

> **Note for AI agents**: These commands should be invoked as parallel tool calls in a single request, not sequentially. This follows the [Google ADK Parallel Fan-Out pattern](https://google.github.io/adk-docs/agents/multi-agents/#parallel-agent) for optimal performance.

```bash
# The following commands can be run in PARALLEL (no dependencies between them):

# [Parallel 1] List of changed files
echo "=== Changed files ==="
CHANGED_FILES=$(git diff main...HEAD --name-only)
echo "$CHANGED_FILES"

# [Parallel 2] Change statistics
echo -e "\n=== Change statistics ==="
git diff main...HEAD --stat

# [Parallel 3] Commit history
echo -e "\n=== Commit history ==="
COMMIT_MESSAGES=$(git log main..HEAD --pretty=format:"- %s")
echo "$COMMIT_MESSAGES"

# [Parallel 4] Detailed diff (to understand the nature of changes)
echo -e "\n=== Analyzing detailed changes ==="
git diff main...HEAD --unified=3
```

### 2. Confirm Related Information (Claude Code only)

When running in Claude Code, use AskUserQuestion tool to confirm the following before generating PR content:

**Related Issue**:
- Question: "Is there a related GitHub Issue for this PR?"
- Header: "Issue"
- Options:
  - "Enter Issue number" - Specify the issue number to link (e.g., #123)
  - "No related issue" - This PR is not linked to any issue
- If user selects "Enter Issue number", they can provide the number via the "Other" option
- Use the provided number in "Closes #XXX" format in the PR description

**Base Branch** (only if current branch name doesn't clearly indicate the target):
- Question: "Which branch should this PR target?"
- Header: "Base"
- Options:
  - "main (Recommended)" - Standard base branch
  - "develop" - For projects using gitflow
- If user needs a different branch, they can specify via the "Other" option

### 3. Generate PR Title and Description

Analyze the changes and generate an appropriate PR title and description based on:

- Pattern of changed files
- Content of commit messages
- Details of the diff

#### PR Title

Generate from the change content (determine from the **essence of the changes**, not the branch name).

**Title format (Conventional Commits):**
- `feat: ` - New feature addition
- `fix: ` - Bug fix
- `refactor: ` - Refactoring
- `test: ` - Test addition/modification
- `docs: ` - Documentation update
- `chore: ` - Build/configuration changes

#### PR Description

Generate a description that provides the minimum prerequisite knowledge for reviewers to begin code review.

**Required sections:**

**Overview**
- Why this change is needed, what it resolves
- Summary of changes and expected effects
- Provide background information so reviewers understand the necessary context
- Approximately 2-4 paragraphs

**Related Issue**
- Reference issues in `Closes #XXX` format
- Related external links (if applicable)

**Changes**
- Bullet points of main changes (approximately 3-7 items)
- Describe "what was changed and how" concisely
- Specific function names or class names are generally unnecessary
- Example:
  ```
  - Add endpoint `/api/v1/xxx`
  - Improve error handling logic
  - Strengthen validation
  ```

**Impact Scope** (if applicable)
- Which features are affected
- Which environments are affected (if applicable)
- Whether existing features are impacted

**Checklist**
```markdown
- [ ] Code follows the style guidelines
- [ ] Tests have been added/updated
- [ ] Documentation has been updated (if relevant)
- [ ] Build is successful
- [ ] Ready for review
```

**How to Test**
- Describe specific test execution methods
- If automated tests are sufficient, indicate so
- If special manual testing is required, describe the steps

**Additional Information**
- Reasons for design decisions
- Technical notes
- Future improvement plans (if applicable)
- If none, write "n/a"

### 4. Create PR

```bash
# Verify main branch is up to date
echo -e "\n=== Checking remote status ==="
git fetch origin main

# Check if branch exists on remote
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if git ls-remote --heads origin "$CURRENT_BRANCH" | grep -q "$CURRENT_BRANCH"; then
    echo "Branch already pushed to remote"
else
    echo "Pushing branch to remote..."
    git push -u origin "$CURRENT_BRANCH"
fi

# Create PR
echo -e "\n=== Creating Pull Request ==="
gh pr create --base main --title "<generated title>" --body "$(cat <<'EOF'
<generated description>
EOF
)"

echo "Pull request created successfully!"
```

## Important Notes

### General Principles

1. **Balance conciseness and thoroughness**
   - Not too detailed, not too brief
   - Provide minimum+α information for reviewers to begin code review
   - Implementation details (specific function names, etc.) are generally unnecessary

2. **Clarify the intent of changes**
   - Explain not just "what" was changed, but "why"
   - Describe the background of technical decisions

3. **Reviewer's perspective**
   - Has basic knowledge of the project
   - However, not familiar with this specific change area
   - Provide necessary context and background
