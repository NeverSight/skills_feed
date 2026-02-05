---
name: github-issue
description: V1.0 - Creates well-structured GitHub Issues that serve as implementation specs with proper labels and escape-safe formatting. Use when creating issues via CLI.
license: MIT
compatibility: Requires GitHub CLI (gh)
---

# GitHub Issue Creator

Create GitHub Issues via `gh issue create` that serve as implementation specifications.

## Issue Structure

```markdown
## Overview
{2-3 sentence summary of what will be built}

## Architecture
{Bullet points showing component relationships - avoid ASCII boxes}

## Implementation Steps
### 1. {Step Title}
{Code snippets, file paths, commands}

## Acceptance Criteria
- [ ] {Testable criterion}
```

**Omit empty sections** (Environment Variables, Prerequisites) if not needed.

## PowerShell Execution

**CRITICAL**: Run here-string assignment and `gh issue create` as **separate commands**:

```powershell
# Command 1: Assign body
$body = @'
{markdown content - no escaping needed}
'@

# Command 2: Create issue (run separately)
gh issue create --repo {owner}/{repo} --title "{title}" --body $body --label "{labels}"
```

**Why separate?** Running both in one terminal call truncates output, hiding the issue URL or errors.

**Never use**:

- Inline `--body "..."` with markdown
- Backticks in markdown (PowerShell interprets as escape)
- ASCII art with box-drawing characters (use bullet points instead)

## Label Guidelines

**Labels must exist in the repo.** Check with `gh label list --repo {owner}/{repo}` first.

| Type | Common Labels |
|------|---------------|
| Feature | `enhancement` (NOT `feature` - often doesn't exist) |
| Bug | `bug` |
| Area | `ui`, `database`, `auth`, `ai` |
| Size | `size:small`, `size:large` |

Use only labels confirmed to exist. If a label fails, retry without it.

## Workflow

1. Gather requirements from user
2. Draft issue body following structure
3. **Verify labels exist** or use safe defaults (`enhancement`)
4. Run here-string assignment command
5. Run `gh issue create` command separately
6. Confirm issue URL from output

## Code Snippet Formatting

Use triple backticks with language identifier:

- `typescript` for TS/JS
- `sql` for database
- `bash` for shell commands
