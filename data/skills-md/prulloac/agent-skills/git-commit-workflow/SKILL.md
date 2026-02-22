---
name: git-commit-workflow
description: Skill for committing git changes following repository guidelines. Use when needing to commit staged or unstaged changes by reading CONTRIBUTING files for standards, analyzing changes with git status and diff, grouping related files, and performing commits according to guidelines or conventional commits as fallback.
---

# Git Commit Workflow

## Overview

This skill provides a structured workflow for committing git changes that respects repository-specific guidelines and falls back to conventional commits when no guidelines exist. It ensures commits are logical, well-grouped, and follow established standards.

## Workflow

Follow these steps to commit changes:

### 1. Read Repository Guidelines
- Look for CONTRIBUTING, CONTRIBUTING.md, or similar files in the repository root
- Extract commit message standards, guidelines, and any specific requirements
- If no guidelines found, prepare to use conventional commits as fallback

### 2. Assess Current Changes
- Run `git status` to see all modified, added, and untracked files
- Note staged vs unstaged changes

### 3. Analyze Changes in Detail
- Run `git diff` (and `git diff --staged` if needed) to understand what changes were made
- Review the nature of changes: bug fixes, features, refactoring, documentation, etc.

### 4. Group Related Changes
- Logically group files by related changes
- See [references/grouping_changes.md](references/grouping_changes.md) for guidance on grouping strategies
- Avoid mixing unrelated changes in the same commit

### 5. Perform Commits
- If CONTRIBUTING guidelines exist, follow their commit message format and grouping requirements
- If no guidelines, use conventional commits standard: See [references/conventional_commits.md](references/conventional_commits.md)
- Stage appropriate files for each commit
- Write descriptive commit messages
- Run `git commit` with proper messages

## Resources

### references/
- `grouping_changes.md`: Guidance on how to group related file changes into logical commits
- `conventional_commits.md`: Reference for conventional commits specification

## Quick Reference: Conventional Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Common types:**
- `feat`: A new feature
- `fix`: A bug fix
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `docs`: Documentation-only changes
- `test`: Adding tests or updating test logic
- `perf`: Code change that improves performance
- `ci`: CI/CD configuration changes
- `chore`: Changes to build scripts, dependencies, or other non-source changes

**Examples:**
- `feat(api): add user authentication endpoints`
- `fix(validation): handle null values in validation utility`
- `docs: update installation instructions`
- `refactor: simplify button component styling`

## Concrete Examples

### Example 1: Multi-Step Commit with Conventional Format

**Initial Repository State:**
```
$ git status
On branch main
Your branch is ahead of 'origin/main' by 0 commits.

Changes not staged for commit:
  modified:   src/auth/login.ts
  modified:   src/auth/logout.ts
  modified:   tests/auth.test.ts
  modified:   docs/README.md
  modified:   .gitignore

Untracked files:
  src/auth/middleware.ts
```

**Step 1: Analyze Changes**
```
$ git diff src/auth/login.ts
  - Added password validation
  - Added JWT token generation
  - Added error handling

$ git diff src/auth/logout.ts
  - Added token cleanup
  - Added session invalidation

$ git diff tests/auth.test.ts
  - Added tests for login validation
  - Added tests for logout flow

$ git diff docs/README.md
  - Updated authentication section
  - Added examples

$ git diff .gitignore
  - Added .env.local to ignore rules
```

**Step 2: Group Related Changes**

Group 1 (Feature: Authentication):
- src/auth/login.ts
- src/auth/logout.ts
- src/auth/middleware.ts

Group 2 (Tests):
- tests/auth.test.ts

Group 3 (Documentation):
- docs/README.md

Group 4 (Configuration):
- .gitignore

**Step 3-4: Create Commits**

```
$ git add src/auth/login.ts src/auth/logout.ts src/auth/middleware.ts
$ git commit -m "feat(auth): implement user login and logout endpoints

- Add password validation with bcrypt hashing
- Implement JWT token generation and refresh
- Add logout handler for session cleanup
- Include middleware for authentication checks
- Improve error handling with specific error codes"

[main a1b2c3d] feat(auth): implement user login and logout endpoints
 3 files changed, 245 insertions(+), 12 deletions(-)

$ git add tests/auth.test.ts
$ git commit -m "test(auth): add comprehensive authentication tests

- Add tests for login validation
- Add tests for password requirements
- Add tests for JWT token generation
- Add tests for logout flow and cleanup
- Achieve 95% coverage for auth module"

[main d4e5f6g] test(auth): add comprehensive authentication tests
 1 file changed, 189 insertions(+)

$ git add docs/README.md
$ git commit -m "docs: update authentication documentation

- Add authentication setup guide
- Include usage examples for login endpoint
- Update API reference section
- Add troubleshooting for common auth errors"

[main h7i8j9k] docs: update authentication documentation
 1 file changed, 67 insertions(+)

$ git add .gitignore
$ git commit -m "chore: update .gitignore for environment files

- Add .env.local to ignore rules
- Add .env.*.local pattern for local overrides"

[main l0m1n2o] chore: update .gitignore for environment files
 1 file changed, 3 insertions(+)
```

**Final Result:**
```
$ git log --oneline -4
l0m1n2o chore: update .gitignore for environment files
h7i8j9k docs: update authentication documentation
d4e5f6g test(auth): add comprehensive authentication tests
a1b2c3d feat(auth): implement user login and logout endpoints

$ git status
On branch main
Your branch is ahead of 'origin/main' by 4 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

### Example 2: Bug Fix with Related Test Update

**Initial State:**
```
$ git status
On branch main
Changes not staged for commit:
  modified:   src/utils/date-parser.ts
  modified:   tests/utils/date-parser.test.ts

$ git diff src/utils/date-parser.ts
  - Fixed timezone handling for UTC offsets
  - Fixed leap year calculation
  - Added validation for invalid dates
```

**Commit Process:**
```
$ git add src/utils/date-parser.ts tests/utils/date-parser.test.ts
$ git commit -m "fix(utils): correct date parsing for timezone offsets

- Fix UTC offset parsing to correctly handle +/-HH:MM format
- Fix leap year calculation for years divisible by 400
- Add validation to reject invalid date strings
- Update tests with edge cases for timezone handling
- Fixes issue #456: Date parsing fails with +05:30 timezone"

[main p3q4r5s] fix(utils): correct date parsing for timezone offsets
 2 files changed, 45 insertions(+), 8 deletions(-)
```

**Output Summary:**
```
✅ COMMIT SUCCESSFUL

Commit: p3q4r5s
Type: fix (Bug Fix)
Scope: utils
Subject: correct date parsing for timezone offsets

Files Changed: 2
- src/utils/date-parser.ts (45 +, 8 -)
- tests/utils/date-parser.test.ts (8 +, 2 -)

Files Staged: 2/2
Working Directory: Clean
```

### Example 3: Refactoring with Multiple Files

**Initial State:**
```
$ git status
On branch main
Changes not staged for commit:
  modified:   src/components/Button.tsx
  modified:   src/components/Form.tsx
  modified:   src/styles/colors.css
  modified:   tests/components/Button.test.tsx
  modified:   tests/components/Form.test.tsx

$ git diff --stat
 src/components/Button.tsx       | 42 ++++++++++++++
 src/components/Form.tsx         | 38 ++++++------
 src/styles/colors.css           | 15 +++--
 tests/components/Button.test.tsx | 22 +++++++
 tests/components/Form.test.tsx   | 18 +++---
```

**Commit Process:**
```
$ git add src/components/Button.tsx src/components/Form.tsx src/styles/colors.css
$ git commit -m "refactor: extract shared styling logic to utility functions

- Extract color constants to dedicated CSS module
- Simplify Button component styling with utility functions
- Reduce CSS duplication in Form component
- Improve maintainability and theme customization
- Maintains 100% backward compatibility"

[main t6u7v8w] refactor: extract shared styling logic to utility functions
 3 files changed, 95 insertions(+)

$ git add tests/components/Button.test.tsx tests/components/Form.test.tsx
$ git commit -m "test(components): update tests after styling refactor

- Update Button component tests for new structure
- Update Form component tests for utility functions
- Add tests for color utility functions
- Maintain 100% code coverage"

[main x9y0z1a] test(components): update tests after styling refactor
 2 files changed, 40 insertions(+)
```

**Commit History View:**
```
$ git log --oneline -2
x9y0z1a test(components): update tests after styling refactor
t6u7v8w refactor: extract shared styling logic to utility functions

$ git log --graph --oneline --all -5
* x9y0z1a test(components): update tests after styling refactor
* t6u7v8w refactor: extract shared styling logic to utility functions
* d4e5f6g Previous commit
* ...
```

## Validation Checklist

After creating commits, verify:

- ✅ All changes are committed (working tree is clean)
- ✅ Each commit has a single, logical purpose
- ✅ Commit messages follow the repository's guidelines (or conventional commits)
- ✅ Related files are grouped together in commits
- ✅ No unrelated changes are mixed in the same commit
- ✅ Commit messages are clear and descriptive
- ✅ Commit history is logical and easy to understand
- ✅ No sensitive information (keys, passwords) in commits
