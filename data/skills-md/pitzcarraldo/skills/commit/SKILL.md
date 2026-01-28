---
name: commit
description: This skill should be used when the user asks to "commit changes", "make a commit", "commit staged files", "create a commit with conventional commit format", or mentions committing code following conventional commit convention.
metadata:
    short-description: Commit with conventional commit format
user-invocable: true
---

# Conventional Commit Skill

## Overview

This skill automatically analyzes staged Git changes and creates commits following the [Conventional Commits](https://www.conventionalcommits.org/) specification. It examines the changes, determines the appropriate commit type and scope, and generates a well-structured commit message without requiring user input.

## Supported Commit Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | Adding user authentication |
| `fix` | Bug fix | Fixing null pointer exception |
| `docs` | Documentation | Updating README |
| `style` | Formatting changes | Code style, whitespace |
| `refactor` | Code restructuring | Extract function to module |
| `perf` | Performance | Optimize database queries |
| `test` | Testing | Add unit tests |
| `build` | Build system | Update dependencies |
| `ci` | CI/CD | Modify GitHub Actions |
| `chore` | Maintenance | Update tooling |

## Commit Message Format

```
<type>(<scope>): <description>

[optional body explaining WHY the change was made]

[optional footer(s)]
```

**Format Rules:**
- **Type**: Required, lowercase, from supported types table
- **Scope**: Optional, component/module name in parentheses
- **Description**: Required, imperative mood, lowercase, no period, under 72 chars
- **Body**: Optional, wrapped at 72 characters, explains motivation
- **Footer**: Optional, for references or metadata

**Author Policy:**
- **Do NOT add Co-Authored-By**: Only the current user should be the author
- Claude assistance should not be credited in commit metadata

## Workflow

### 1. Verify Git Repository

**Check if we're in a git repository:**

```bash
git rev-parse --git-dir 2>&1
```

**Expected output:**
- Success: `.git` or path to git directory
- Failure: "not a git repository" error

**Error message format:**
```
Error: Not in a git repository
Please initialize git with: git init
```

### 2. Check Staged Changes

**Run these commands in parallel to gather context:**

```bash
git diff --cached --stat
git diff --cached
git log --oneline -5
```

**Purpose:**
- `--cached --stat`: Summary of staged files
- `--cached`: Detailed line-by-line changes
- `log --oneline -5`: Recent commit messages for style consistency

**If no staged changes:**
```
No files are staged for commit.

Stage files with:
  git add <file>           # Stage specific file
  git add .                # Stage all changes
  git add -p               # Stage interactively
```

### 3. Analyze Changes

**Determine commit type based on:**

1. **File patterns:**
   - `README.md`, `*.md` in docs/ → `docs`
   - `package.json`, `Gemfile` → `build`
   - `.github/workflows/` → `ci`
   - `*_test.js`, `*_spec.rb` → `test`

2. **Change patterns:**
   - New files/functions → `feat`
   - Bug keywords (fix, bug, issue) → `fix`
   - Refactor keywords (extract, move, rename) → `refactor`
   - Performance keywords (optimize, cache) → `perf`
   - Style keywords (format, lint) → `style`

3. **Scope determination:**
   - Extract from file paths (e.g., `src/auth/` → `auth`)
   - Use module/component names
   - Omit if changes span multiple components

4. **Description generation:**
   - Use imperative mood: "add", "fix", "update"
   - Start with verb, lowercase
   - Be specific but concise
   - No period at end
   - Keep under 72 characters

### 4. Generate Commit Message

**Basic commit (no body needed):**

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>
EOF
)"
```

**Complex commit (with body):**

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

Detailed explanation of WHY this change was made.
Wrap at 72 characters for readability.
Use multiple paragraphs if needed.
EOF
)"
```

**When to include body:**
- Complex refactoring that needs context
- Bug fixes requiring explanation of root cause
- Breaking changes that need migration notes
- Non-obvious design decisions

### 5. Create and Verify Commit

**Create the commit:**
```bash
git commit -m "$(cat <<'EOF'
[generated message]
EOF
)"
```

**Verify the commit:**
```bash
git log -1 --pretty=format:"%h - %s%n%n%b"
```

**Display to user:**
```
✓ Commit created successfully

[short hash] - [commit subject]

[commit body if present]
```

## Output Format

All commit operations follow this consistent format:

```
Analyzing staged changes...

Files changed:
  [file list from git diff --cached --stat]

Creating commit with message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<type>(<scope>): <description>

[body]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Commit created: [hash]
```

## Examples

### Example 1: Simple Feature Addition

**Staged changes:**
```diff
+ src/auth/passwordReset.ts (new file)
+ 45 lines
```

**Generated commit:**
```
feat(auth): add password reset functionality
```

### Example 2: Bug Fix with Context

**Staged changes:**
```diff
M src/api/userProfile.ts
- return user.profile
+ return user.profile || defaultProfile
```

**Generated commit:**
```
fix(api): handle null values in user profile endpoint

Previously the endpoint would crash when users had incomplete profiles.
Added fallback to default profile object to prevent null reference errors.
```

### Example 3: Documentation Update

**Staged changes:**
```diff
M README.md
+ Installation section
+ 20 lines added
```

**Generated commit:**
```
docs: add installation instructions to readme
```

### Example 4: Refactoring

**Staged changes:**
```diff
M src/utils/validation.ts
M src/components/Form.tsx
+ src/utils/validators.ts (new file)
```

**Generated commit:**
```
refactor(utils): extract validation logic into separate module

Moved reusable validators to dedicated module for better code organization
and to enable reuse across multiple components.
```

### Example 5: Multiple File Changes

**Staged changes:**
```diff
M src/components/Button.tsx
M src/components/Input.tsx
M src/styles/global.css
```

**Generated commit:**
```
style: apply consistent formatting to component files
```

## Technical Requirements

### Required Tools

| Tool | Purpose | Check Command |
|------|---------|---------------|
| Git | Version control | `git --version` |
| Git Config | User identity | `git config user.name && git config user.email` |

### Minimum Versions

- **Git**: 2.0 or higher
- **Bash**: 4.0 or higher (for HEREDOC support)

## Best Practices

1. **Analyze recent commits** to match repository's commit style
2. **Keep descriptions concise** but meaningful
3. **Use scope consistently** within a project
4. **Add body for complex changes** to explain reasoning
5. **Group related changes** in a single commit when logical
6. **Review the generated message** before confirming

## Limitations

1. **Single commit only**: Creates one commit for all staged changes
2. **No interactive editing**: Commit message is generated automatically
3. **English descriptions**: Generates descriptions in English by default
4. **No push operation**: Only creates local commit, does not push to remote
5. **No commit signing**: Does not add GPG signatures automatically

## Error Handling

### Common Errors and Solutions

**Error: Not a git repository**
- **Cause**: Current directory is not initialized with git
- **Solution**: Run `git init` or navigate to a git repository

**Error: No staged files**
- **Cause**: No files added to staging area
- **Solution**: Stage files with `git add <file>` or `git add .`

**Error: User identity unknown**
- **Cause**: Git user.name or user.email not configured
- **Solution**: Configure with:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "you@example.com"
  ```

**Error: Empty commit message**
- **Cause**: Commit message generation failed
- **Solution**: Ensure staged changes are readable with `git diff --cached`

**Error: Hook failed**
- **Cause**: Pre-commit hook or commit-msg hook rejected the commit
- **Solution**: Fix issues reported by hook or use `--no-verify` if appropriate

## Advanced Usage

### Breaking Changes

For breaking changes, add an exclamation mark after type/scope and include BREAKING CHANGE in footer.

### Multiple Scopes

If changes affect multiple scopes but are tightly related, use comma-separated scopes.

### Issue References

Include issue references in body or footer (e.g., Fixes #123 or Closes #456).

## References

- **Conventional Commits**: https://www.conventionalcommits.org/
- **Git Documentation**: https://git-scm.com/doc
- **Commit Message Guidelines**: https://cbea.ms/git-commit/

## Notes

- Commits are created locally only; use separate command to push
- Only the current user is credited as the author (no Co-Authored-By)
- Scope is optional but recommended for larger projects
- Description must use imperative mood (not past tense)
- Multi-line descriptions are not allowed (use body instead)
- The skill operates autonomously without prompting for input
