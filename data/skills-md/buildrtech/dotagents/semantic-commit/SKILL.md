---
name: semantic-commit
description: Create semantic git commits following Conventional Commits specification. Use when committing changes, making commits, or when asked to commit.
---

# Semantic Commit

Create git commits following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Commit Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Guidelines

- Start with a short prefix followed by colon and space (feat:, fix:, docs:, refactor:, test:, chore:, etc.)
- Isolate your changes and commit only what you did (no unrelated files)
- feat: for user-visible features, fix: for bug fixes
- A scope MAY be added in parentheses, e.g. `fix(parser):` - only when it meaningfully improves clarity
- Short description in imperative mood explaining what changed, not how
- Body MAY be included after one blank line for context, rationale, or non-obvious behavior
- Footers MAY be included (Token: value format, use `-` instead of spaces in tokens)
- Breaking changes should be explained clearly in description or body, no special marking required
- **Clarity and usefulness matter more than strict conformance**

## Commit Types

| Type | Description |
|------|-------------|
| `feat` | A new feature (user-visible) |
| `fix` | A bug fix (user-visible) |
| `docs` | Documentation only changes |
| `style` | Changes that do not affect the meaning of the code (formatting, semicolons, etc.) |
| `refactor` | A code change that neither fixes a bug nor adds a feature |
| `perf` | A code change that improves performance |
| `test` | Adding missing tests or correcting existing tests |
| `build` | Changes that affect the build system or external dependencies |
| `ci` | Changes to CI configuration files and scripts |
| `chore` | Other changes that don't modify src or test files |
| `revert` | Reverts a previous commit |

## Workflow

```dot
digraph commit_workflow {
    rankdir=TB;
    node [shape=box];
    
    check [label="Check git status"];
    stage [label="Stage changes\n(if needed)"];
    review [label="Review staged diff"];
    analyze [label="Analyze changes\nDetermine type & scope"];
    write [label="Write commit message"];
    commit [label="Execute git commit"];
    
    check -> stage;
    stage -> review;
    review -> analyze;
    analyze -> write;
    write -> commit;
}
```

### 1. Check Repository State

```bash
git status --short
git diff --cached --stat   # staged changes
git diff --stat            # unstaged changes
```

### 2. Stage Changes

If no changes are staged:
- Ask which files to stage
- Stage only files you changed for this task (avoid unrelated changes)

### 3. Review Staged Changes

```bash
git diff --cached
```

Understand what was modified to write an accurate message.

### 4. Determine Type and Scope

Based on the changes:
- **Type**: What category of change? (feat, fix, refactor, etc.)
- **Scope**: What area of the codebase? Only add when it meaningfully improves clarity
- **Breaking**: Does this break backward compatibility? Explain clearly in description or body

## Writing Good Commit Messages

### Subject Line

- Use imperative mood: "add feature" not "added feature"
- Keep under 50 characters when possible
- Don't end with a period
- Explain what changed, not how

<Good>
```
feat(auth): add OAuth2 login support
fix: prevent crash on empty input
refactor(api): extract validation logic
```
</Good>

<Bad>
```
updated some stuff
fix bug
WIP
changes
```
</Bad>

### Body (Optional)

Include after one blank line when context, rationale, or non-obvious behavior needs explanation:
- Explain motivation for the change
- Contrast with previous behavior
- Note any side effects

```
fix(parser): handle unicode characters in filenames

Previously, filenames with non-ASCII characters would cause
a decode error. Now using UTF-8 decoding with fallback to
latin-1 for legacy files.

Closes #123
```

### Footer (Optional)

Use Token: value format (use `-` instead of spaces in token names):
- `Closes #123` or `Fixes #456` for issue references
- `Co-authored-by: Name <email>` for pair programming
- `Reviewed-by: Name <email>` for review attribution

## Examples

| Changes | Commit |
|---------|--------|
| New endpoint added | `feat(api): add user profile endpoint` |
| Bug causing crash | `fix: prevent null pointer on empty config` |
| Updated README | `docs: add installation instructions` |
| Reformatted code | `style: apply prettier formatting` |
| Renamed internal function | `refactor: rename processData to parseInput` |
| Optimized query | `perf(db): add index for user lookups` |
| Added unit tests | `test: add coverage for auth module` |
| Updated dependencies | `build: upgrade react to v18` |
| Changed CI config | `ci: add node 20 to test matrix` |
| Cleaned up files | `chore: remove unused imports` |
| Breaking API change | `feat(api): change response format to JSON arrays` |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Past tense ("added") | Use imperative ("add") |
| Too vague ("fix bug") | Be specific ("fix null check in parser") |
| Too long subject | Keep concise, move details to body |
| Wrong type | `fix` = bug, `feat` = new capability, `refactor` = no behavior change |
| Combining unrelated changes | Split into multiple commits |
| Overusing scope | Only add scope when it meaningfully improves clarity |

## Quick Reference

```
feat:     New feature for users
fix:      Bug fix for users  
docs:     Documentation only
style:    Formatting, no logic change
refactor: Code change, no behavior change
perf:     Performance improvement
test:     Adding/fixing tests
build:    Build system, dependencies
ci:       CI configuration
chore:    Maintenance, tooling
revert:   Reverting commits
```
