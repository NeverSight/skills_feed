---
name: commit-message
description: >
  Analyze git changes and generate conventional commit messages. Supports batch commits
  for multiple unrelated changes. Use when: (1) Creating git commits, (2) Reviewing
  staged changes, (3) Splitting large changesets into logical commits.
---

# commit-message

Analyze git changes and generate context-aware commit messages following Conventional Commits.

## Quick Start

```bash
# Analyze all changes
python3 .shared/commit-message/scripts/analyze_changes.py --analyze

# Get batch commit suggestions
python3 .shared/commit-message/scripts/analyze_changes.py --batch

# Generate message for specific files
python3 .shared/commit-message/scripts/analyze_changes.py --generate "src/api/*.py"
```

## Commands

| Command | Description |
|---------|-------------|
| `--analyze` | Show all changed files with status and categories |
| `--batch` | Suggest how to split changes into multiple commits |
| `--generate [pattern]` | Generate commit message for matching files |
| `--staged` | Only analyze staged changes (default: all changes) |

## Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(api): add user authentication` |
| `fix` | Bug fix | `fix(db): resolve connection timeout` |
| `refactor` | Code restructuring | `refactor(utils): simplify helper functions` |
| `docs` | Documentation | `docs: update README` |
| `test` | Tests | `test(api): add user endpoint tests` |
| `chore` | Maintenance | `chore: update dependencies` |
| `style` | Formatting | `style: fix linting errors` |

## Batch Commit Workflow

When you have multiple unrelated changes:

1. Run `--batch` to see suggested commit groups
2. Stage files for first commit: `git add <files>`
3. Commit with suggested message
4. Repeat for remaining groups

## Grouping Strategy

Files are grouped by:
- **Directory/Module**: `src/api/`, `tests/`, `docs/`
- **Change Type**: Added vs Modified vs Deleted
- **Semantic Relationship**: Related files together

## Context-Aware Commit Messages

> **Note**: The `analyze_changes.py` script provides file grouping and basic suggestions. Use its output as a starting point, then read `git diff` to understand the actual changes and generate context-aware messages following the examples below.

When generating commit messages, analyze the **actual code changes** to infer business context. Don't just describe files—describe what the changes accomplish.

### Scope Guidelines

The scope should reflect the **business module or feature**, not just the directory:

| Scope Type | Example | When to Use |
|------------|---------|-------------|
| Feature/Module | `companion`, `calendar`, `inbox` | Changes to a specific product feature |
| Platform | `ios`, `android`, `web` | Platform-specific changes |
| Integration | `outlook`, `gmail`, `slack` | Third-party integration changes |
| Component | `auth`, `api`, `db` | Core infrastructure changes |

### Input/Output Examples

**Example 1: New Feature**
```
Input (code changes):
  + src/companion/pages/AvailabilityDetailPage.tsx
  + src/companion/pages/AvailabilityActionsPage.tsx
  + src/companion/components/AvailabilityCard.tsx
  M src/companion/navigation/routes.ts

Output:
  feat(companion): add availability detail and actions pages for ios

  - New AvailabilityDetailPage showing time slot details
  - New AvailabilityActionsPage for booking/canceling
  - AvailabilityCard component for list display
  - Updated navigation routes
```

**Example 2: Bug Fix**
```
Input (code changes):
  M src/integrations/outlook/email_sender.py
  M src/integrations/outlook/auth.py

Output:
  fix(outlook): resolve email sending failures due to token expiration

  Refresh OAuth token before sending when close to expiry
```

**Example 3: Multi-platform Change**
```
Input (code changes):
  M ios/Calendar/CalendarView.swift
  M android/calendar/CalendarFragment.kt
  M web/src/calendar/Calendar.tsx

Output:
  feat(calendar): add week view across all platforms

  Implement consistent week view UI for iOS, Android, and web
```

**Example 4: Chore/Maintenance**
```
Input (code changes):
  M package.json
  M yarn.lock
  M requirements.txt

Output:
  chore(deps): update dependencies to latest versions
```

### Writing Good Descriptions

|  Bad (Generic) | Good (Context-Aware) |
|-----------------|------------------------|
| `feat: add new file` | `feat(payments): add Stripe webhook handler` |
| `fix: fix bug` | `fix(auth): prevent session timeout on mobile` |
| `chore: update code` | `chore(ci): reduce build time with parallel jobs` |
| `refactor: refactor utils` | `refactor(api): extract rate limiting to middleware` |

### Key Principles

1. **Read the code** - Understand what the changes actually do
2. **Identify the feature** - What user-facing or system capability is affected?
3. **Be specific** - Include relevant details (platform, integration, component)
4. **Use active voice** - "add", "fix", "update", not "added", "fixed", "updated"
5. **Keep it concise** - First line under 72 characters
