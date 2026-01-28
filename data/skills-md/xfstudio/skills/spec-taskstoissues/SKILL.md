---
name: spec-taskstoissues
description: Convert tasks.md into GitHub issues with proper dependencies. Use when user says "/spec-taskstoissues", "create GitHub issues", "convert tasks to issues" after /spec-tasks when using GitHub for project management.
---

# Spec-TasksToIssues

Convert tasks.md into GitHub issues.

**Prerequisites**:
- tasks.md must exist
- Git remote must be a GitHub URL
- GitHub CLI (`gh`) must be authenticated

## Workflow

1. **Initialize** - Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`
2. **Get tasks path** - Extract from script output
3. **Verify remote** - Check `git config --get remote.origin.url`
4. **Create issues** - Use GitHub MCP server for each task

## Script Usage

```bash
# Get prerequisites
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks

# Get remote URL
git config --get remote.origin.url
```

## Safety Checks

⚠️ **CRITICAL CONSTRAINTS**:

1. **Remote must be GitHub** - Only proceed if URL matches `github.com`
2. **Match repository** - NEVER create issues in wrong repository
3. **Parse tasks correctly** - Extract ID, description, dependencies

## Issue Format

For each task in tasks.md:

```markdown
Title: [TaskID] Description
Body:
  - Phase: [Phase name]
  - Dependencies: [Dependent task IDs]
  - Files: [File paths mentioned]
  - Parallel: [Yes/No based on [P] marker]
  - Story: [User story if [USx] present]
```

## Task Parsing

From format: `- [ ] T001 [P] [US1] Description with path`

Extract:
- `T001` → Issue title prefix
- `[P]` → Label: `parallel`
- `[US1]` → Label: `user-story-1`
- Description → Issue title
- File path → Issue body

## Labels

Create/use labels:
- `spec-task` - All generated tasks
- `parallel` - Tasks with `[P]` marker
- `user-story-N` - Tasks with `[USx]` marker
- `phase-N` - Based on phase in tasks.md

## GitHub CLI Commands

```bash
# Create issue
gh issue create --title "[T001] Create project structure" \
  --body "Phase: Setup\nDependencies: None" \
  --label "spec-task,phase-1"

# List issues
gh issue list --label "spec-task"
```

## Error Handling

- Skip already-created issues (check by title prefix)
- Report failed creations
- Continue with remaining tasks

## Next Steps

After `/spec-taskstoissues`:
- Assign issues to team members
- Set milestones
- `/spec-implement` - Execute tasks
