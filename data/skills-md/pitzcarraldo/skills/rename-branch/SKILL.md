---
name: rename-branch
description: This skill should be used when the user asks to "rename branch", "change branch name", "update branch name based on changes", or wants to create a meaningful branch name based on the changes.
metadata:
    short-description: Rename branch based on changes
user-invocable: true
---

# Branch Rename Skill

## Overview

This skill intelligently analyzes the differences between the current branch and the base branch (typically `origin/main`), then generates and applies a descriptive branch name following conventional commit conventions. The generated name uses kebab-case and accurately reflects the nature of the changes.

## Naming Convention

### Format
```
<type>/<description>
```

### Branch Type Prefixes

| Prefix | Purpose | Examples |
|--------|---------|----------|
| `feat/` | New features | `feat/user-auth`, `feat/dark-mode` |
| `fix/` | Bug fixes | `fix/null-pointer`, `fix/memory-leak` |
| `docs/` | Documentation | `docs/api-guide`, `docs/setup` |
| `style/` | Formatting | `style/prettier`, `style/lint-rules` |
| `refactor/` | Code restructuring | `refactor/extract-utils`, `refactor/simplify-logic` |
| `perf/` | Performance | `perf/cache-queries`, `perf/lazy-load` |
| `test/` | Testing | `test/unit-coverage`, `test/e2e-auth` |
| `build/` | Build system | `build/webpack-config`, `build/deps` |
| `ci/` | CI/CD | `ci/github-actions`, `ci/deploy` |
| `chore/` | Maintenance | `chore/cleanup`, `chore/update-deps` |

### Description Guidelines

- **Kebab-case**: lowercase words separated by hyphens
- **Length**: 20 characters or less (excluding prefix)
- **Imperative mood**: "add" not "added", "fix" not "fixed"
- **Specific**: Clearly describes the primary change
- **Concise**: No unnecessary words

**Good examples:**
- `feat/oauth-login` ✓
- `fix/race-condition` ✓
- `docs/quick-start` ✓

**Bad examples:**
- `feat/AddOAuthLogin` ✗ (not kebab-case)
- `fix/fixed-the-race-condition-in-auth` ✗ (too long, past tense)
- `docs/documentation-updates` ✗ (redundant)

## Workflow

### 1. Verify Git Repository Status

**Check if we're in a valid git repository:**

```bash
git rev-parse --git-dir 2>&1
```

**Expected output:**
- Success: `.git` or path to git directory
- Failure: "not a git repository" error

**Check current branch:**

```bash
git branch --show-current
```

**If detached HEAD state:**
```
Error: Cannot rename branch - currently in detached HEAD state

You are not on any branch. To create a new branch from current state:
  git checkout -b <branch-name>
```

**If on protected branch (main/master/develop):**
```
Warning: You are on the protected branch '[branch-name]'

Creating new branches from protected branches is recommended:
  git checkout -b <new-branch-name>

Proceed with rename anyway? [y/n]
```

### 2. Identify Base Branch

**Attempt to find the base branch in order of preference:**

```bash
# Try origin/main
git rev-parse --verify origin/main 2>/dev/null

# If not found, try origin/master
git rev-parse --verify origin/master 2>/dev/null

# If not found, try local main
git rev-parse --verify main 2>/dev/null

# If not found, try local master
git rev-parse --verify master 2>/dev/null
```

**Store the first successful result as BASE_BRANCH**

**If no base branch found:**
```
Error: Cannot determine base branch

None of the following branches exist:
  - origin/main
  - origin/master
  - main
  - master

Please specify the base branch manually or create one.
```

### 3. Analyze Changes

**Fetch comprehensive change information:**

```bash
# Summary of changed files
git diff $BASE_BRANCH...HEAD --stat

# Detailed line-by-line changes
git diff $BASE_BRANCH...HEAD

# Commit messages on this branch
git log $BASE_BRANCH..HEAD --oneline

# Number of commits
git rev-list --count $BASE_BRANCH..HEAD
```

**If no changes detected:**
```
No changes detected between current branch and $BASE_BRANCH

This branch is either:
  - Fully merged into $BASE_BRANCH
  - Has no commits
  - Is synchronized with $BASE_BRANCH

No rename needed.
```

**Parse the data to extract:**
- List of modified files with paths
- Number of insertions and deletions
- Commit messages for context
- File patterns (identify directories/modules)

### 4. Determine Branch Type

**Apply pattern matching logic:**

#### File-based Detection

```bash
# Documentation changes
if files match: *.md, docs/*, README*
  → type: docs

# Test files
if files match: *test.*, *spec.*, __tests__/*, tests/*
  → type: test

# CI/CD configurations
if files match: .github/workflows/*, .gitlab-ci.yml, Jenkinsfile
  → type: ci

# Build configurations
if files match: package.json, Gemfile, requirements.txt, *.config.js
  → type: build

# Style/formatting
if files match: .prettierrc, .eslintrc, .editorconfig
  → type: style
```

#### Content-based Detection

```bash
# Analyze diff and commit messages for keywords

# New features (keyword presence in diffs/commits)
if contains: "add", "implement", "create", "new"
  → type: feat

# Bug fixes
if contains: "fix", "bug", "issue", "resolve", "correct"
  → type: fix

# Refactoring
if contains: "refactor", "restructure", "extract", "move", "rename"
  → type: refactor

# Performance
if contains: "optimize", "performance", "faster", "cache", "speed"
  → type: perf

# Default fallback
if no clear pattern:
  → type: chore
```

#### Multiple Types

If changes span multiple types:
1. Count file changes per type
2. Select the type with most changes
3. If tie, prioritize: feat > fix > refactor > others

### 5. Generate Description

**Extract meaningful description from changes:**

1. **Identify primary module/component:**
   ```bash
   # From file paths: src/auth/login.ts → "auth"
   # From multiple files in same dir → use directory name
   ```

2. **Extract action from commits:**
   ```bash
   # From commit messages like "Add OAuth support"
   # Extract: "oauth-support"
   ```

3. **Combine module + action:**
   ```bash
   # If module: "auth", action: "oauth"
   # Result: "auth-oauth"

   # If action already includes module context
   # Result: just use action
   ```

4. **Sanitize description:**
   ```bash
   # Convert to lowercase
   description=$(echo "$description" | tr '[:upper:]' '[:lower:]')

   # Replace spaces/underscores with hyphens
   description=$(echo "$description" | tr ' _' '-')

   # Remove special characters
   description=$(echo "$description" | sed 's/[^a-z0-9-]//g')

   # Remove consecutive hyphens
   description=$(echo "$description" | sed 's/--*/-/g')

   # Trim to 20 characters
   description=${description:0:20}

   # Remove trailing hyphen if present
   description=${description%-}
   ```

**Examples of description generation:**

| Commits | Files | Generated Description |
|---------|-------|----------------------|
| "Add OAuth login" | `src/auth/oauth.ts` | `oauth-login` |
| "Fix null pointer in payment" | `src/payment/process.ts` | `payment-null-ptr` |
| "Update API docs" | `docs/api.md` | `api-docs` |
| "Refactor validation utils" | `src/utils/validation.ts` | `validation-utils` |
| "Optimize database queries" | `src/db/query.ts` | `db-queries` |

### 6. Construct New Branch Name

**Combine type and description:**

```bash
new_branch="${type}/${description}"
```

**Validate the name:**

```bash
# Check length (should be reasonable, typically < 50 chars total)
if [ ${#new_branch} -gt 50 ]; then
  # Truncate description further
fi

# Check for existing branch with same name
if git show-ref --verify --quiet "refs/heads/$new_branch"; then
  # Append number: feat/user-auth-2
  suffix=2
  while git show-ref --verify --quiet "refs/heads/${new_branch}-${suffix}"; do
    ((suffix++))
  done
  new_branch="${new_branch}-${suffix}"
fi
```

### 7. Check Current Branch Name

**Compare with existing name:**

```bash
current_branch=$(git branch --show-current)

# If already follows convention and is accurate
if [[ "$current_branch" =~ ^(feat|fix|docs|style|refactor|perf|test|build|ci|chore)/ ]]; then
  # Extract current description
  current_desc=${current_branch#*/}

  # Check similarity with generated description
  if [ "$current_desc" == "$description" ]; then
    echo "Current branch name is already appropriate: $current_branch"
    echo "No rename needed."
    exit 0
  fi
fi
```

### 8. Rename Branch

**Perform the rename operation:**

```bash
old_branch=$(git branch --show-current)

# Rename the branch
git branch -m "$old_branch" "$new_branch"
```

**Verify the rename:**

```bash
# Check new branch name
if [ "$(git branch --show-current)" == "$new_branch" ]; then
  echo "✓ Branch renamed successfully"
else
  echo "✗ Branch rename failed"
  exit 1
fi
```

### 9. Display Results and Instructions

**Show summary:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Branch Renamed Successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Old name: [old_branch]
New name: [new_branch]

Reason: [Brief explanation of type and description choice]

Changes analyzed:
  - [X] files modified
  - [Y] insertions, [Z] deletions
  - [N] commits

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If branch was previously pushed to remote:**

```
⚠ Remote Branch Update Required

This branch was previously pushed to remote as '[old_branch]'.
To update the remote:

1. Push the new branch:
   git push -u origin [new_branch]

2. Delete the old remote branch:
   git push origin --delete [old_branch]

3. (Optional) Update any open pull requests to point to new branch

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Check if branch has remote tracking:**

```bash
# Check for remote tracking branch
if git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null; then
  # Remote tracking exists, show update instructions
fi
```

## Examples

### Example 1: Feature Addition

**Scenario:**
- Current branch: `feature-branch`
- Changes: Added user authentication with OAuth

**Commands executed:**
```bash
git diff origin/main...HEAD --stat
# Output: src/auth/oauth.ts | 120 +++++++
#         src/auth/login.ts  |  45 +++

git log origin/main..HEAD --oneline
# Output: a1b2c3d Add OAuth authentication
#         b2c3d4e Implement login flow
```

**Analysis:**
- Type: `feat` (new functionality)
- Primary module: `auth`
- Action: `oauth-login`
- Description: `oauth-login` (16 chars)

**Result:**
```
Old: feature-branch
New: feat/oauth-login

Reason: Detected new authentication feature in auth module
```

### Example 2: Bug Fix

**Scenario:**
- Current branch: `bugfix`
- Changes: Fixed null pointer exception in payment processing

**Commands executed:**
```bash
git diff origin/main...HEAD --stat
# Output: src/payment/process.ts | 8 ++--

git log origin/main..HEAD --oneline
# Output: c3d4e5f Fix null pointer in payment processor
```

**Analysis:**
- Type: `fix` (bug fix keywords)
- Primary module: `payment`
- Issue: `null-pointer`
- Description: `payment-null-ptr` (17 chars)

**Result:**
```
Old: bugfix
New: fix/payment-null-ptr

Reason: Detected bug fix in payment processing module
```

### Example 3: Documentation

**Scenario:**
- Current branch: `update-docs`
- Changes: Updated API documentation

**Commands executed:**
```bash
git diff origin/main...HEAD --stat
# Output: docs/api/v2.md      | 200 +++++++++++++
#         docs/guides/auth.md |  50 ++++

git log origin/main..HEAD --oneline
# Output: d4e5f6a Update API v2 documentation
#         e5f6g7h Add authentication guide
```

**Analysis:**
- Type: `docs` (documentation files)
- Focus: `api-v2`
- Description: `api-v2-guide` (12 chars)

**Result:**
```
Old: update-docs
New: docs/api-v2-guide

Reason: Detected documentation updates for API v2
```

### Example 4: Refactoring

**Scenario:**
- Current branch: `cleanup`
- Changes: Extracted validation logic into utilities

**Commands executed:**
```bash
git diff origin/main...HEAD --stat
# Output: src/utils/validation.ts | 150 ++++++++++++++
#         src/components/Form.tsx  |  80 ++------

git log origin/main..HEAD --oneline
# Output: f6g7h8i Extract validation to utility module
#         g7h8i9j Simplify form component
```

**Analysis:**
- Type: `refactor` (code restructuring)
- Module: `validation`
- Action: `extract-validation`
- Description: `validation-utils` (16 chars)

**Result:**
```
Old: cleanup
New: refactor/validation-utils

Reason: Detected refactoring of validation logic into utils
```

### Example 5: Multiple Change Types

**Scenario:**
- Current branch: `various-updates`
- Changes: Added feature, fixed bugs, updated docs

**Commands executed:**
```bash
git diff origin/main...HEAD --stat
# Output: src/auth/oauth.ts   | 120 +++++++  (new file)
#         src/payment/fix.ts  |   8 +-    (bug fix)
#         docs/readme.md      |  10 +      (docs)

git log origin/main..HEAD --oneline
# Output: h8i9j0k Add OAuth authentication (major)
#         i9j0k1l Fix payment bug         (minor)
#         j0k1l2m Update readme            (minor)
```

**Analysis:**
- Mixed types: feat (120 lines), fix (8 lines), docs (10 lines)
- Primary type: `feat` (most significant change)
- Focus: `oauth` from largest change
- Description: `oauth-auth` (10 chars)

**Result:**
```
Old: various-updates
New: feat/oauth-auth

Reason: Primary change is new OAuth authentication feature
        (Also includes minor bug fix and doc update)
```

## Technical Requirements

### Required Tools

| Tool | Purpose | Check Command |
|------|---------|---------------|
| Git | Version control | `git --version` |
| Bash | Shell scripting | `bash --version` |

### Minimum Versions

- **Git**: 2.0 or higher (for `git diff ... ` syntax)
- **Bash**: 4.0 or higher

### Git Configuration

No special configuration required, but recommended:
```bash
# Set default branch name (optional)
git config --global init.defaultBranch main
```

## Best Practices

1. **Run before pushing**: Rename branches early before pushing to remote
2. **One focus per branch**: Branches with mixed purposes are harder to name
3. **Keep descriptions clear**: Prioritize clarity over brevity
4. **Follow team conventions**: Adjust type prefixes if team uses different standards
5. **Update PR titles**: If PR exists, update title to match new branch name
6. **Communicate changes**: Inform team members if renaming shared branches

## Limitations

1. **Single branch focus**: Best results when branch has one primary purpose
2. **20-character limit**: Very long descriptions get truncated
3. **English descriptions**: Generated names are in English
4. **No semantic analysis**: Cannot understand complex business logic
5. **Pattern-based**: Relies on file patterns and keywords
6. **Local operation**: Does not automatically update remote branches

## Error Handling

### Common Errors and Solutions

**Error: Not a git repository**
- **Cause**: Current directory is not a git repository
- **Solution**: Navigate to git repository or run `git init`

**Error: Detached HEAD state**
- **Cause**: Not on any branch (e.g., checked out specific commit)
- **Solution**: Create new branch with `git checkout -b <name>`

**Error: Cannot determine base branch**
- **Cause**: No main/master branch exists
- **Solution**: Create base branch or specify manually

**Error: No changes detected**
- **Cause**: Branch is synchronized with base or has no commits
- **Solution**: No action needed, branch is up to date

**Error: Branch name already exists**
- **Cause**: Generated name conflicts with existing branch
- **Solution**: Tool automatically appends number (e.g., `feat/auth-2`)

**Error: Invalid ref format**
- **Cause**: Generated name contains invalid characters
- **Solution**: Tool sanitizes automatically, but check for edge cases

## Advanced Features

### Custom Base Branch

Allow user to specify different base branch:
```bash
# Compare against different branch
git diff custom-base...HEAD --stat
```

### Interactive Mode

Confirm before renaming:
```
Generated branch name: feat/oauth-login

Current: feature-branch
New:     feat/oauth-login

Proceed with rename? [y/n]
```

### Dry Run Mode

Show what would happen without actually renaming:
```bash
# Simulate rename
echo "Would rename: $old_branch → $new_branch"
# Skip actual git branch -m command
```

### Preserve Remote Connection

Automatically update remote tracking after rename:
```bash
git branch -m "$old_branch" "$new_branch"
git push origin -u "$new_branch"
git push origin --delete "$old_branch"
```

## References

- **Git Branch Documentation**: https://git-scm.com/docs/git-branch
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Git Best Practices**: https://www.git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project

## Notes

- Branch renaming is a local operation by default
- Remote branches must be updated separately if already pushed
- Pull requests may need manual update after branch rename
- Team members should be notified of branch name changes
- Consider branch protection rules when renaming
- Some CI/CD systems may be configured for specific branch names
