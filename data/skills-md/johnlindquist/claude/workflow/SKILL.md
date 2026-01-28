---
name: workflow
description: Manage GitHub Actions workflows using gh CLI. Use to check CI status, view run logs, analyze failures, and rerun workflows.
---

# GitHub Actions Workflow Manager

Monitor and manage CI/CD workflows using the GitHub CLI.

## Prerequisites

Install GitHub CLI:
```bash
brew install gh
# or
curl -sS https://webi.sh/gh | sh
```

Authenticate:
```bash
gh auth login
```

## CLI Reference

### Quick Status Check
```bash
# Current branch CI status
gh run list --branch $(git branch --show-current) --limit 5

# All recent runs
gh run list --limit 10

# Filter by workflow
gh run list --workflow "CI" --limit 5
```

### View Specific Run
```bash
# Get run details
gh run view <run-id>

# View with logs
gh run view <run-id> --log

# Failed jobs only
gh run view <run-id> --log-failed

# Exit codes for CI scripts
gh run view <run-id> --exit-status
```

### List Runs with Filters
```bash
# By branch
gh run list --branch main --limit 10

# By workflow name
gh run list --workflow "Build and Test" --limit 10

# By status
gh run list --status failure --limit 10
gh run list --status success --limit 10
gh run list --status in_progress --limit 10

# Combined filters
gh run list --branch main --workflow "CI" --status failure --limit 5
```

### Rerun Workflows
```bash
# Rerun entire workflow
gh run rerun <run-id>

# Rerun only failed jobs
gh run rerun <run-id> --failed

# Rerun specific job
gh run rerun <run-id> --job <job-id>
```

### Watch Running Workflow
```bash
# Watch a run in progress
gh run watch <run-id>

# Watch and exit with run's exit code
gh run watch <run-id> --exit-status
```

### Download Artifacts
```bash
# List artifacts from a run
gh run view <run-id> --json artifacts

# Download all artifacts
gh run download <run-id>

# Download specific artifact
gh run download <run-id> --name "artifact-name"

# Download to specific directory
gh run download <run-id> --dir ./artifacts
```

### Cancel a Run
```bash
gh run cancel <run-id>
```

### View Workflow Files
```bash
# List workflow files
gh workflow list

# View specific workflow
gh workflow view "CI"

# Enable/disable workflow
gh workflow enable "CI"
gh workflow disable "CI"
```

### Run Workflow Manually
```bash
# Trigger workflow_dispatch
gh workflow run "CI"

# With inputs
gh workflow run "Deploy" -f environment=staging -f version=1.2.3

# On specific branch
gh workflow run "CI" --ref feature-branch
```

## Output Formats

```bash
# JSON output for parsing
gh run list --json status,conclusion,name,headBranch,url

# Specific fields
gh run view <run-id> --json jobs,status,conclusion
```

## Workflow Patterns

### Quick CI Check
```bash
# Is my branch passing?
gh run list --branch $(git branch --show-current) --limit 1 --json status,conclusion
```

### Debug Failing CI
```bash
# 1. Find the failing run
gh run list --branch main --status failure --limit 1

# 2. View failed logs
gh run view <run-id> --log-failed

# 3. After fixing, rerun
gh run rerun <run-id> --failed
```

### Monitor Deployment
```bash
# Watch deployment in progress
gh run watch <run-id>

# Get notified when done (macOS)
gh run watch <run-id> && osascript -e 'display notification "Deployment complete"'
```

### Retry Flaky Tests
```bash
# Rerun just the failed jobs
gh run rerun <run-id> --failed
```

### Pre-Merge Check
```bash
# Ensure all checks pass before merging
gh run list --branch $(git branch --show-current) --json conclusion --jq '.[0].conclusion'
```

## Common Statuses

| Status | Meaning |
|--------|---------|
| `queued` | Waiting to start |
| `in_progress` | Currently running |
| `completed` | Finished |

| Conclusion | Meaning |
|------------|---------|
| `success` | All jobs passed |
| `failure` | One or more jobs failed |
| `cancelled` | Run was cancelled |
| `skipped` | Run was skipped |
| `timed_out` | Run exceeded time limit |

## Best Practices

1. **Check status before merge** - Ensure CI passes
2. **Use `--log-failed`** - Only see relevant failure logs
3. **Rerun `--failed` first** - Faster than full rerun
4. **Watch long runs** - Don't poll manually
5. **Download artifacts** - For test reports, coverage, etc.
6. **Use JSON output** - For scripting and parsing
