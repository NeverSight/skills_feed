---
name: commit-message-generator
description: Automatically generate conventional commit messages when user has staged changes and mentions committing. Analyzes git diff and status to create properly formatted commit messages following conventional commits specification. Invoke when user mentions "commit", "staged", "committing", or asks for help with commit messages.
---

# Commit Message Generator

Automatically generate conventional commit messages for staged changes.

## Philosophy

Commit messages are the history and documentation of your code's evolution.

### Core Beliefs

1. **Commits Tell a Story**: Each commit should explain what changed and why
2. **Conventional Format Enables Automation**: Structured messages power changelogs and semantic versioning
3. **Clarity Over Brevity**: A clear 2-line message beats a cryptic 5-word one
4. **Context Matters**: Messages should be understandable months later without additional context

### Why Conventional Commits

- **Automated Changelogs**: Generate release notes from commit history
- **Semantic Versioning**: Determine version bumps (major/minor/patch) automatically
- **Better Searchability**: Find specific types of changes quickly
- **Team Communication**: Consistent format aids code review and collaboration

## When to Use This Skill

Activate this skill when the user:
- Mentions "commit", "committing", "staged changes", or "ready to commit"
- Shows `git add` or `git status` output with staged changes
- Asks "what should my commit message be?"
- Says "I need to commit my changes"
- Asks for help writing commit messages

## Decision Framework

Before generating a commit message, ask yourself:

### Is This Ready to Commit?

- ✅ **Yes** - Staged changes represent a single logical unit of work
- ❌ **No** - Multiple unrelated changes staged → Suggest splitting into separate commits
- ⚠️ **Maybe** - Large changeset → Review to ensure it's cohesive

### What Type of Change Is This?

1. **New functionality** → `feat` type
2. **Bug fix** → `fix` type
3. **Code improvement without behavior change** → `refactor` type
4. **Documentation only** → `docs` type
5. **Tests only** → `test` type
6. **Multiple types** → Suggest splitting commits

### What Scope Makes Sense?

- **Module/component name** - For focused changes (e.g., `auth`, `api`, `ui`)
- **Feature area** - For cross-cutting changes (e.g., `validation`, `logging`)
- **No scope** - For global changes (e.g., dependencies, config)

### Should This Be Multiple Commits?

Split if staged changes include:
- ✅ Unrelated features or fixes
- ✅ Refactoring + new feature (split: refactor first, feature second)
- ✅ Multiple bug fixes
- ❌ Feature + tests (keep together)
- ❌ Feature + documentation (keep together)

### Decision Tree

```
User mentions commit
    ↓
Check: Staged changes?
    ↓ Yes
Check: Multiple unrelated changes?
    ↓ No
Check: Follows conventional commits pattern?
    ↓ Generate message
    ↓
Review with user → Commit
```

## Workflow

### 1. Check for Staged Changes

```bash
git status
git diff --staged
```

If no staged changes, inform the user and suggest staging files first.

### 2. Analyze Recent Commits for Style

```bash
git log --oneline -10
```

Learn the repository's commit message conventions.

### 3. Generate Conventional Commit Message

**Format**: `<type>(<scope>): <description>`

**Types**:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, semicolons, etc.)
- `refactor` - Code refactoring (no functional changes)
- `test` - Adding or updating tests
- `chore` - Build process, dependency updates, etc.
- `perf` - Performance improvements
- `ci` - CI/CD changes

**Example**:
```
feat(auth): add two-factor authentication support

- Implement TOTP-based 2FA
- Add backup codes generation
- Include recovery flow for lost devices
- Update user profile settings UI
```

### 4. Drupal/WordPress-Specific Patterns

**Drupal**:
- Config changes: `feat(config): add user profile field configuration`
- Module work: `fix(custom_module): correct permission check in access callback`
- Hooks: `refactor(hooks): simplify hook_form_alter implementation`

**WordPress**:
- Theme work: `style(theme): improve mobile navigation styles`
- Plugin work: `fix(plugin): correct ACF field validation`
- Blocks: `feat(blocks): add testimonial Gutenberg block`

### 5. Present to User for Approval

**When used via workflow-specialist agent:**
The agent will use `AskUserQuestion` to present the commit message for review:
- Show the generated message
- Ask: "Would you like to proceed with this commit message, or would you like to edit it?"
- Options: "Approve and commit" or "Edit message"
- If user selects "Other", they can provide their edited version

**When used conversationally:**
Show the generated commit message and ask:
"Here's a commit message based on your changes. Would you like me to commit with this message, or would you like to modify it?"

### 6. Execute Commit (only after approval)

```bash
git commit -m "commit message here"
```

Or for multi-line messages:
```bash
git commit -m "$(cat <<'EOF'
feat(auth): add two-factor authentication support

- Implement TOTP-based 2FA
- Add backup codes generation
- Include recovery flow
EOF
)"
```

## Integration with CMS Cultivator

This skill complements the `/pr-commit-msg` slash command:

- **This Skill**: Automatically triggered during natural conversation
  - "I'm ready to commit"
  - "What should my commit message say?"

- **`/pr-commit-msg` Command**: Explicitly invoked for staged changes
  - User deliberately wants commit message generation
  - Batch generation workflow

Both use the same analysis approach but different invocation methods.

## Best Practices

1. **Analyze the actual changes** - Don't just use file names, understand what changed
2. **Be specific in scope** - Use module name, component name, or feature area
3. **Include breaking changes** - Add `BREAKING CHANGE:` footer if applicable
4. **Reference tickets** - Include ticket numbers if found in branch name
5. **Follow project conventions** - Match the existing commit style

## Example Interactions

**Example 1: Simple fix**
```
User: "I fixed the login bug, ready to commit"
[Skill analyzes git diff]
Skill: "I'll generate a commit message for your login fix..."

Generated:
fix(auth): resolve session timeout on remember-me login

- Correct cookie expiration logic
- Add test coverage for remember-me flow

Would you like me to commit with this message?
```

**Example 2: Feature addition**
```
User: "Staged my changes, need to commit"
[Skill analyzes extensive changes]
Skill: "I see you've added a new dashboard widget. Here's a commit message..."

Generated:
feat(dashboard): add performance metrics widget

- Create new widget component
- Add database query for metrics
- Include responsive design
- Add widget to admin dashboard page
```

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- [Semantic Commit Messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
