---
name: gitlab
description: Load before running any glab commands to ensure correct CLI syntax. Use when creating/viewing MRs, checking pipelines, managing issues, or any GitLab operations (when remote contains "gitlab").
---

# GitLab Workflow

Work with GitLab repositories, merge requests, issues, and CI/CD pipelines using the `glab` CLI.

## FIRST: Verify GitLab Remote

**Run this before any `glab` command.** If no match, STOP—this skill doesn't apply.

```bash
git remote -v | grep -i gitlab
```

## Key Guidelines

- **Verify remote first**: No GitLab remote = don't use `glab`
- **Check CI before requesting review**: Run `glab ci status` after pushing. Fix failures before requesting reviews.
- **Pull logs immediately on failure**: Run `glab ci trace <job-name>` first. The logs contain the answer.
- **Use draft MRs for WIP**: Create with `--draft`, mark ready with `glab mr update <id> --ready`
- **Reference issues explicitly**: Use `Closes #123` for auto-close, `Relates to #123` for tracking only
- **Retry flaky failures, fix real ones**: Retry a job with `glab ci retry <job-name>`. If it fails again, it's a real issue.

## Quick Start: Branch → MR

The most common workflow—create a branch, make changes, open an MR:

```bash
git checkout -b feature/my-feature
# make changes
git add . && git commit -m "feat: add new feature"
git push -u origin feature/my-feature
glab mr create --fill --target-branch main
```

## Quick Reference: CI Commands

| Task | Command |
|------|---------|
| Check pipeline status | `glab ci status` |
| View pipeline details | `glab ci view` |
| Pull job logs | `glab ci trace <job-name>` |
| Retry failed job | `glab ci retry <job-name>` |
| Run new pipeline | `glab ci run` |
| Download artifacts | `glab job artifact <ref> <job-name>` |

## Prerequisites

This skill requires the `glab` CLI. If `glab` commands fail with "command not found", ask the user to install it:

```bash
# macOS
brew install glab

# Linux (Debian/Ubuntu)
sudo apt install glab

# Other methods: https://gitlab.com/gitlab-org/cli#installation
```

Authentication must be configured. Run `glab auth status` to check. If not authenticated:

```bash
glab auth login
```

---

# Detailed Reference

## Repository Setup

### Clone a Repository

```bash
# Clone via glab (uses authenticated user context)
glab repo clone <owner>/<repo>

# Clone with specific branch
glab repo clone <owner>/<repo> -- --branch <branch>

# Clone to specific directory
glab repo clone <owner>/<repo> <directory>
```

### Fork a Repository

```bash
# Fork to your namespace
glab repo fork <owner>/<repo>

# Fork and clone immediately
glab repo fork <owner>/<repo> --clone
```

### View Repository Info

```bash
glab repo view
glab repo view <owner>/<repo>
```

## Branch and Changes

### Create a Branch

```bash
git checkout -b feature/my-feature
# Make changes, stage, and commit
git add .
git commit -m "feat: add new feature"
```

### Push Branch

```bash
git push -u origin feature/my-feature
```

## Merge Request Operations

### Create a Merge Request

```bash
# Interactive creation
glab mr create

# With specific options
glab mr create \
  --title "feat: add new feature" \
  --description "$(cat <<'EOF'
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
How to test these changes
EOF
)" \
  --target-branch main \
  --assignee @me \
  --label "enhancement"

# Create as draft
glab mr create --draft --title "WIP: feature in progress"

# Create and auto-fill from commits
glab mr create --fill
```

### List Merge Requests

```bash
# List open MRs (default)
glab mr list

# List by state
glab mr list --merged      # merged MRs only
glab mr list --closed      # closed MRs only
glab mr list --all         # all MRs (open, merged, closed)

# Filter by author or assignee
glab mr list --author @me
glab mr list --assignee @me

# Filter by label
glab mr list --label bug,urgent

# Limit results
glab mr list --per-page 10
```

### View Merge Request Details

```bash
# View current branch's MR
glab mr view

# View specific MR
glab mr view 123

# View in browser
glab mr view 123 --web
```

### Update a Merge Request

```bash
# Update title
glab mr update 123 --title "new title"

# Add labels
glab mr update 123 --label "reviewed,approved"

# Change assignees
glab mr update 123 --assignee user1,user2

# Mark ready for review (remove draft)
glab mr update 123 --ready

# Add reviewers
glab mr update 123 --reviewer user1,user2
```

### Merge a Merge Request

```bash
# Merge when pipeline succeeds
glab mr merge 123

# Merge immediately (skip pipeline check)
glab mr merge 123 --when-pipeline-succeeds=false

# Squash and merge
glab mr merge 123 --squash

# Delete source branch after merge
glab mr merge 123 --remove-source-branch
```

## Review and Iteration

### Fetch Review Comments

```bash
# View MR with comments and activities
glab mr view 123 --comments

# View MR diff
glab mr diff 123
```

### Address Review Comments

1. Read the comments:
   ```bash
   glab mr view 123 --comments
   ```

2. Make requested changes locally

3. Commit and push:
   ```bash
   git add .
   git commit -m "fix: address review feedback"
   git push
   ```

4. Reply to comments (via web or API):
   ```bash
   # Add a note to the MR
   glab mr note 123 -m "Addressed feedback in latest commit"
   ```

### Approve a Merge Request

```bash
glab mr approve 123
```

### Check Out an MR Locally

```bash
# Check out MR branch locally for testing
glab mr checkout 123
```

## CI/CD Monitoring and Failure Remediation

CI job failures are the most common blocker for merging MRs.

### Check Pipeline Status

```bash
# Quick status check for current branch
glab ci status

# View detailed pipeline status (shows all jobs and stages)
glab ci view

# List recent pipelines with status
glab ci list

# Check status for a specific MR
glab mr view 123  # Shows pipeline status in MR details
```

**Pipeline states**: `pending`, `running`, `success`, `failed`, `canceled`, `skipped`

### Identify Failed Jobs

When a pipeline fails, first identify which jobs failed:

```bash
# View the current pipeline with job breakdown
glab ci view

# View pipeline for a specific branch
glab ci view main
```

The output shows each job's status. Focus on jobs with `failed` status.

### Pull and Analyze Job Logs

```bash
# Stream logs from a running or completed job
glab ci trace <job-name>

# View logs for a specific job by ID
glab ci trace <job-id>

# Example: view logs for the "test" job
glab ci trace test

# For jobs in specific pipelines
glab ci trace <job-name> --pipeline-id <pipeline-id>
```

**Log analysis tips:**
- Scroll to the end first—the final error is usually the root cause
- Look for `error:`, `Error:`, `FAILED`, `fatal:`, or exit codes
- Check for timeout messages if the job hung
- Note the stage and job name for context

### Common CI Failure Patterns

| Pattern | Log Signature | Typical Fix |
|---------|---------------|-------------|
| Test failure | `FAIL`, `AssertionError`, `expected ... got` | Fix the failing test or the code it tests |
| Lint error | `error:`, style/format violations | Run linter locally, fix issues |
| Build failure | `compilation failed`, `cannot find module` | Check dependencies, imports, syntax |
| Timeout | `Job timed out`, `exceeded limit` | Optimize slow operations or increase timeout |
| Missing env/secret | `undefined`, `missing required`, `authentication failed` | Check CI variables configuration |
| Dependency issue | `404 Not Found`, `version not found` | Update dependency versions, check registry access |

### Address Failures Locally

1. **Reproduce the failure locally** (when possible):
   ```bash
   # Run the same commands from .gitlab-ci.yml
   npm test        # for test failures
   npm run lint    # for lint failures
   npm run build   # for build failures
   ```

2. **Fix the issue and commit**:
   ```bash
   git add .
   git commit -m "fix: resolve CI test failure in auth module"
   git push
   ```

3. **Monitor the new pipeline**:
   ```bash
   # Watch the pipeline status
   glab ci status --live

   # Or view in browser
   glab ci view --web
   ```

### Retry and Rerun Jobs/Pipelines

```bash
# Retry a specific job (interactive selection if no job specified)
glab ci retry
glab ci retry <job-name>
glab ci retry <job-id>

# Retry a job in a specific pipeline
glab ci retry <job-name> --pipeline-id <pipeline-id>

# Trigger a completely new pipeline
glab ci run

# Trigger with CI variables (useful for conditional jobs)
glab ci run --variables "FORCE_FULL_TEST:true"
```

**When to retry vs. fix:**
- **Retry**: Flaky tests, transient network errors, runner issues
- **Fix**: Genuine code errors, missing dependencies, configuration problems

### CI Failure Remediation Workflow

Follow this process when an MR pipeline fails:

1. **Check status**: `glab ci status` or `glab mr view`
2. **Identify failed jobs**: `glab ci view`
3. **Pull logs**: `glab ci trace <job-name>`
4. **Analyze the error**: Find root cause in logs
5. **Fix locally**: Reproduce and fix the issue
6. **Push fix**: `git commit` and `git push`
7. **Verify**: `glab ci status --live` to watch new pipeline
8. **If still failing**: Repeat from step 2

### Advanced: Debug with CI Variables

```bash
# List CI/CD variables (requires maintainer access)
glab variable list

# Set a variable for debugging
glab variable set DEBUG_CI "true"

# Run pipeline with debug variable
glab ci run --variables "CI_DEBUG_TRACE:true"
```

### Artifacts and Reports

```bash
# Download job artifacts (requires ref and job name)
glab job artifact main build
glab job artifact <branch> <job-name>

# Download to specific path
glab job artifact main build --path="./artifacts/"
```

Use artifacts to inspect test reports, coverage data, or build outputs that might explain failures.

## Searching GitLab

### Search Issues

```bash
# Search in current project
glab issue list --search "bug in login"

# Search by label
glab issue list --label "bug"

# Search across all accessible projects (use API)
glab api "search?scope=issues&search=login+error" | jq '.[] | {id, title, web_url}'
```

### Search Merge Requests

```bash
# Search in current project
glab mr list --search "refactor auth"

# Search across GitLab (use API)
glab api "search?scope=merge_requests&search=auth+refactor" | jq '.[] | {id, title, web_url}'
```

### Search Code/Projects

```bash
# Search for projects
glab api "search?scope=projects&search=my-library" | jq '.[] | {id, name, web_url}'

# Search code (blobs)
glab api "search?scope=blobs&search=deprecated+function" | jq '.[] | {path, project_id, ref}'
```

## Multi-Repository Operations

For coordinated changes across multiple repositories (e.g., dependency updates, security fixes):

### Strategy

1. **List affected repositories**: Identify all repos that need changes
2. **Clone each repository**: Use `glab repo clone`
3. **Create branches with consistent naming**: Use a common prefix (e.g., `fix/security-CVE-2024-XXXX`)
4. **Make changes in each repo**: Apply the fix/update
5. **Create MRs with linked descriptions**: Reference the tracking issue

### Example: Coordinated Security Fix

```bash
# Define repos and fix details
REPOS="group/repo1 group/repo2 group/repo3"
BRANCH="fix/CVE-2024-12345"
ISSUE_URL="https://gitlab.com/group/tracker/-/issues/100"

for repo in $REPOS; do
  echo "Processing $repo..."
  
  # Clone if not exists
  if [ ! -d "$(basename $repo)" ]; then
    glab repo clone "$repo"
  fi
  
  cd "$(basename $repo)"
  
  # Create branch and make changes
  git checkout -b "$BRANCH"
  
  # Apply fix (example: update dependency version)
  # sed -i 's/vulnerable-pkg@1.0/vulnerable-pkg@1.1/g' package.json
  
  git add .
  git commit -m "fix: update vulnerable-pkg to patched version

Addresses $ISSUE_URL"
  
  git push -u origin "$BRANCH"
  
  # Create MR
  glab mr create \
    --title "fix: address CVE-2024-12345" \
    --description "Updates vulnerable-pkg to patched version.

Related to: $ISSUE_URL" \
    --label "security"
  
  cd ..
done
```

## Working with Issues

### Create an Issue

```bash
glab issue create \
  --title "Bug: login fails on mobile" \
  --description "Steps to reproduce..." \
  --label "bug,mobile"
```

### List and View Issues

```bash
glab issue list
glab issue view 42
```

### Close an Issue

```bash
glab issue close 42
```

### Link MR to Issue

When creating an MR, reference the issue in the description:

```bash
glab mr create --description "Closes #42"
```

## Releases

### Create a Release

```bash
glab release create v1.0.0 \
  --name "Version 1.0.0" \
  --notes "$(cat CHANGELOG.md)"

# With assets
glab release create v1.0.0 --assets-links '[{"name":"binary","url":"https://..."}]'
```

### List Releases

```bash
glab release list
```

## API Access

For operations not covered by `glab` subcommands, use the API directly:

```bash
# GET request
glab api projects/:id/merge_requests

# POST request
glab api projects/:id/issues --method POST --field title="New issue"

# With pagination
glab api projects/:id/issues --paginate
```

## Additional Notes

- **Check authentication on errors**: If `glab` commands fail with 401/403, run `glab auth status` and re-authenticate with `glab auth login`.
- **Consistent branch naming**: Use `feature/`, `fix/`, `docs/`, `chore/` prefixes. For security fixes, include the CVE: `fix/CVE-2024-12345`.
- **Self-managed instances**: Set `GITLAB_HOST` environment variable or authenticate with `glab auth login --hostname gitlab.example.com`.
