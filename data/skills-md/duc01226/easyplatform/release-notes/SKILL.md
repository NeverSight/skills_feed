---
name: release-notes
description: Generate professional release notes from git commits between two refs with automated categorization. Use when creating release notes from git history.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Release Notes Generation

Generate professional release notes from git commits with automated categorization.

## Invocation

```
/release-notes [base] [head] [--version vX.Y.Z] [--output path]
```

**Examples:**
```bash
/release-notes v1.0.0 HEAD --version v1.1.0
/release-notes main feature/new-auth --version v2.0.0-beta
```

## Workflow

### Step 1: Parse Commits

```bash
node .claude/skills/release-notes/lib/parse-commits.cjs <base> <head> [--with-files]
```

Output: JSON with `hash`, `type`, `scope`, `description`, `breaking`, `author`, `date`, `files`

### Step 2: Categorize Commits

```bash
node .claude/skills/release-notes/lib/parse-commits.cjs <base> <head> | \
node .claude/skills/release-notes/lib/categorize-commits.cjs
```

| Type                                    | Category     | User-Facing           |
| --------------------------------------- | ------------ | --------------------- |
| `feat`                                  | features     | Yes                   |
| `fix`                                   | fixes        | Yes                   |
| `perf`                                  | improvements | Yes                   |
| `docs`                                  | docs         | Yes (unless internal) |
| `refactor`                              | improvements | Technical only        |
| `test`, `ci`, `build`, `chore`, `style` | internal     | No                    |

Excluded: `chore(deps):`, `chore(config):`, `[skip changelog]`, `[ci skip]`

### Step 3: Render Markdown

```bash
node .claude/skills/release-notes/lib/parse-commits.cjs <base> <head> | \
node .claude/skills/release-notes/lib/categorize-commits.cjs | \
node .claude/skills/release-notes/lib/render-template.cjs --version v1.1.0 --output docs/release-notes/250111-v1.1.0.md
```

## Complete Pipeline

```bash
node .claude/skills/release-notes/lib/parse-commits.cjs v1.0.0 HEAD | \
node .claude/skills/release-notes/lib/categorize-commits.cjs | \
node .claude/skills/release-notes/lib/render-template.cjs --version v1.1.0 --output docs/release-notes/250111-v1.1.0.md
```

## Output Structure

```markdown
# Release Notes: v1.1.0
**Date:** 2025-01-11 | **Version:** v1.1.0 | **Status:** Draft

## Summary
## What's New
## Improvements
## Bug Fixes
## Breaking Changes
## Technical Details (collapsed)
## Contributors
```

## Human Review Gate

Generated notes are **Draft** status. Review -> Enhance -> Approve -> Publish.

## Advanced Features

See [references/release-pipeline.md](references/release-pipeline.md) for:
- Service boundary detection, breaking change analysis
- PR metadata extraction, contributor statistics
- Version bumping, quality validation, LLM transforms
- Full enhanced pipeline, configuration, troubleshooting

## Integration

- **`/commit`** - Commit generated notes
- **`/changelog-update`** - Update CHANGELOG.md with new release


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
