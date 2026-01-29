---
name: gh-fix-ci
description: Inspect GitHub PR for CI failures, merge conflicts, update-branch requirements, reviewer comments, change requests, and unresolved review threads. Create fix plans and implement after user approval. Resolve review threads and notify reviewers after fixes.
metadata:
  short-description: Fix failing GitHub PRs comprehensively
---

# Gh PR Checks Plan Fix

## Overview

Use gh to inspect PRs for:

- Failing CI checks (GitHub Actions)
- Merge conflicts
- Update Branch requirements (base branch advanced)
- Reviewer comments (review summaries, inline comments, issue comments)
- Change Requests from reviewers
- Unresolved review threads

Then propose a fix plan, implement after explicit approval, and optionally resolve threads and notify reviewers.

- Depends on the `plan` skill for drafting and approving the fix plan.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed.

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `mode`: inspection mode (`checks`, `conflicts`, `reviews`, `all`)
- `max-review-comments`: max reviewer comments to list per category
- `required-only`: limit CI checks to required checks only (uses `gh pr checks --required`)
- `gh` authentication for the repo host

## Quick start

```bash
# Inspect all (CI, conflicts, reviews) - default mode
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>"

# CI checks only
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --mode checks

# Conflicts only
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --mode conflicts

# Reviews only (Change Requests + Unresolved Threads)
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --mode reviews

# JSON output
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --json

# Required checks only (if gh supports --required)
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --mode checks --required-only

# Limit review comment output
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --max-review-comments 30

# Resolve all unresolved threads after fixing
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --resolve-threads

# Add a comment to notify reviewers
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --add-comment "Fixed all issues. Please re-review."
```

## Workflow

1. **Verify gh authentication.**
   - Run `gh auth status` in the repo with escalated scopes (workflow/repo).
   - If unauthenticated, ask the user to log in before proceeding.

2. **Resolve the PR.**
   - Prefer the current branch PR: `gh pr view --json number,url`.
   - If the user provides a PR number or URL, use that directly.

3. **Inspect based on mode:**

   **Conflicts Mode (`--mode conflicts`):**
   - Check `mergeable` and `mergeStateStatus` fields.
   - If `CONFLICTING` or `DIRTY`, report conflict details.
   - If `BEHIND`, report that the base branch advanced and an Update Branch is required.
   - Suggest resolution steps: fetch base branch, merge/rebase, resolve conflicts.

   **Reviews Mode (`--mode reviews`):**
   - Fetch reviews with `CHANGES_REQUESTED` state.
   - Fetch unresolved review threads using GraphQL.
   - Fetch reviewer comments (review summaries, inline review comments, issue comments).
   - Display reviewer, comment body, file path, and line number.
   - Decide if reviewer feedback requires action (any change request, unresolved thread, or reviewer comment).

   **Checks Mode (`--mode checks`):**
   - Run bundled script to inspect failing CI checks.
   - Add `--required-only` to limit output to required checks when supported.
   - Fetch GitHub Actions logs and extract failure snippets.
   - For external checks (Buildkite, etc.), report URL only.

   **All Mode (`--mode all`):**
   - Run all inspections above.

4. **Summarize issues for the user.**
   - Provide clear summary of all detected issues.
   - Call out conflicts, change requests, unresolved threads, and CI failures.

5. **Create a plan.**
   - Use the `plan` skill to draft a fix plan and request approval.

6. **Implement after approval.**
   - Apply the approved plan, summarize diffs/tests.

7. **Resolve review threads (optional).**
   - With `--resolve-threads`, resolve all unresolved threads via GraphQL mutation.
   - Requires `Repository Permissions > Contents: Read and Write`.

8. **Notify reviewers (optional).**
   - With `--add-comment "message"`, post a comment to the PR.
   - Useful for notifying reviewers that issues have been addressed.

9. **Recheck status.**
   - After changes, suggest re-running `gh pr checks` to confirm.

## Bundled Resources

### scripts/inspect_pr_checks.py

Comprehensive PR inspection tool. Exits non-zero when issues remain.

**Arguments:**

| Argument | Default | Description |
|----------|---------|-------------|
| `--repo` | `.` | Path inside the target Git repository |
| `--pr` | (current) | PR number or URL |
| `--mode` | `all` | Inspection mode: `checks`, `conflicts`, `reviews`, `all` |
| `--max-lines` | 160 | Max lines for log snippets |
| `--context` | 30 | Context lines around failure markers |
| `--max-review-comments` | 50 | Max reviewer comments to list per category |
| `--required-only` | false | Limit CI checks to required checks only |
| `--json` | false | Emit JSON output |
| `--resolve-threads` | false | Resolve unresolved review threads |
| `--add-comment` | (none) | Add a comment to the PR |

**Exit codes:**

- `0`: No issues found
- `1`: Issues detected or error occurred

## New Features

### Conflict Detection

Detects merge conflicts via `mergeable` and `mergeStateStatus` fields.

- `CONFLICTING` / `DIRTY`: Conflict detected
- `BEHIND`: Base branch advanced; Update Branch required
- `MERGEABLE` / `CLEAN`: No conflicts

### Change Request Handling

Fetches reviews with `state == "CHANGES_REQUESTED"` and displays:

- Reviewer name
- Review body
- Submission timestamp

### Reviewer Comments

Fetches reviewer feedback beyond change requests:

- Review summaries with comment bodies
- Inline review comments (file/line)
- PR issue comments
- Marks review action required if any reviewer feedback exists

### Unresolved Review Threads

Uses GraphQL to fetch threads where `isResolved == false`:

- File path and line number
- Thread ID (for resolution)
- Comment author and body
- Outdated status

### Resolve Conversation

Use `--resolve-threads` to mark threads as resolved via GraphQL mutation `resolveReviewThread`.

**Required permissions:**

- Fine-grained PAT: `Pull requests` + `Contents: Read and Write`
- Classic PAT: `repo` scope

### Reviewer Notification

Use `--add-comment "message"` to post a summary comment to the PR after fixes.

## Output Examples

### Text Output

```text
PR #123: Comprehensive Check Results
============================================================

MERGE STATUS
------------------------------------------------------------
Mergeable: CONFLICTING
Merge State: DIRTY
Base: main <- Head: feature/my-branch
Action Required: Resolve conflicts before merging

CHANGE REQUESTS
------------------------------------------------------------
From @reviewer1 (2025-01-15):
  "Please fix these issues..."

UNRESOLVED REVIEW THREADS
------------------------------------------------------------
[1] src/main.ts:42
    Thread ID: PRRT_xxx123
    @reviewer1: This needs refactoring...

CI FAILURES
------------------------------------------------------------
Check: build
Details: https://github.com/...
Failure snippet:
  Error: TypeScript compilation failed
  ...
============================================================
```

### JSON Output

```json
{
  "pr": "123",
  "conflicts": {
    "hasConflicts": true,
    "mergeable": "CONFLICTING",
    "mergeStateStatus": "DIRTY",
    "baseRefName": "main",
    "headRefName": "feature/my-branch"
  },
  "changeRequests": [
    {
      "id": 123456,
      "reviewer": "reviewer1",
      "body": "Please fix these issues...",
      "submittedAt": "2025-01-15T12:00:00Z"
    }
  ],
  "unresolvedThreads": [
    {
      "id": "PRRT_xxx123",
      "path": "src/main.ts",
      "line": 42,
      "comments": [
        {"author": "reviewer1", "body": "This needs refactoring"}
      ]
    }
  ],
  "ciFailures": [
    {
      "name": "build",
      "status": "ok",
      "logSnippet": "..."
    }
  ]
}
```
